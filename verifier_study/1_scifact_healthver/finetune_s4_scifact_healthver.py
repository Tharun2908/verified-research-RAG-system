from __future__ import annotations

import json
import os
import random
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    get_linear_schedule_with_warmup,
)


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
BASE_MODEL_DIR = "/workspace/signal4_model"  # old thesis S4 checkpoint
TRAIN_PATH = "/workspace/project3/data_grouped/verifier_train_grouped.json"
VAL_PATH = "/workspace/project3/data_grouped/verifier_val_grouped.json"
TEST_PATH = "/workspace/project3/data_grouped/verifier_test_grouped.json"

OUTPUT_DIR = "/workspace/project3/signal4_model_scifact_healthver"
RESULTS_DIR = "/workspace/project3/signal4_scifact_healthver_results"
os.makedirs(RESULTS_DIR, exist_ok=True)


# ---------------------------------------------------------------------
# Training config
# ---------------------------------------------------------------------
SEED = 42
MAX_LENGTH = 512
BATCH_SIZE = 16
EPOCHS = 4
LR = 2e-5
WEIGHT_DECAY = 0.01
WARMUP_RATIO = 0.06
PATIENCE = 2
NUM_WORKERS = 2

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
USE_AMP = torch.cuda.is_available()


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------
def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_ece(probs, labels, n_bins: int = 10) -> float:
    """
    Expected Calibration Error for binary P(unsupported/hallucinated).
    labels: 1 = unsupported, 0 = supported
    """
    probs = np.asarray(probs, dtype=float)
    labels = np.asarray(labels, dtype=float)

    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        if i == n_bins - 1:
            mask = (probs >= bins[i]) & (probs <= bins[i + 1])
        else:
            mask = (probs >= bins[i]) & (probs < bins[i + 1])

        if mask.sum() == 0:
            continue

        bin_acc = labels[mask].mean()
        bin_conf = probs[mask].mean()
        ece += (mask.sum() / len(probs)) * abs(bin_acc - bin_conf)

    return round(float(ece), 4)


def best_threshold_by_f1(probs, labels):
    best_t = 0.5
    best_f1 = -1.0

    for t in np.arange(0.05, 0.96, 0.01):
        preds = (probs >= t).astype(int)
        f1 = f1_score(labels, preds, zero_division=0)

        if f1 > best_f1:
            best_f1 = f1
            best_t = float(t)

    return round(best_t, 2), float(best_f1)


def metrics_at_threshold(probs, labels, threshold: float):
    preds = (probs >= threshold).astype(int)

    out = {
        "threshold": float(threshold),
        "f1": float(f1_score(labels, preds, zero_division=0)),
        "precision": float(precision_score(labels, preds, zero_division=0)),
        "recall": float(recall_score(labels, preds, zero_division=0)),
        "auroc": float(roc_auc_score(labels, probs)),
        "auprc": float(average_precision_score(labels, probs)),
        "ece": float(compute_ece(probs, labels)),
        "confusion_matrix": confusion_matrix(labels, preds).tolist(),
    }

    # confusion matrix layout from sklearn:
    # [[TN, FP],
    #  [FN, TP]]
    return out


def summarize_split(name: str, records):
    labels = [int(r["label"]) for r in records]
    n = len(labels)
    pos = sum(labels)
    print(f"{name}: n={n} supported={n-pos} unsupported={pos} pos_rate={100*pos/n:.1f}%")


# ---------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------
class VerifierDataset(Dataset):
    """
    S4 input shape matches thesis:

        tokenizer(answer, context)

    Here:
        answer  = claim
        context = abstract/evidence text
        label   = 1 if unsupported, 0 if supported
    """
    def __init__(self, records, tokenizer, max_length: int = 512):
        self.records = records
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        ex = self.records[idx]

        enc = self.tokenizer(
            ex["answer"],
            ex["context"],
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        item = {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "labels": torch.tensor(int(ex["label"]), dtype=torch.long),
            "idx": torch.tensor(idx, dtype=torch.long),
        }

        return item


# ---------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------
@torch.no_grad()
def predict_probs(model, loader):
    model.eval()

    all_probs = []
    all_labels = []
    all_indices = []

    for batch in tqdm(loader, desc="eval", leave=False):
        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].cpu().numpy()
        indices = batch["idx"].cpu().numpy()

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        probs = torch.softmax(outputs.logits, dim=1)[:, 1].detach().cpu().numpy()

        all_probs.extend(probs.tolist())
        all_labels.extend(labels.tolist())
        all_indices.extend(indices.tolist())

    return np.array(all_probs), np.array(all_labels), np.array(all_indices)


def save_predictions(path, records, probs, labels, indices, threshold):
    rows = []

    for prob, label, idx in zip(probs, labels, indices):
        ex = records[int(idx)]
        pred = int(prob >= threshold)

        rows.append({
            "id": ex["id"],
            "source": ex["source"],
            "orig_split": ex["orig_split"],
            "claim_id": ex["claim_id"],
            "abstract_id": ex["abstract_id"],
            "verdict": ex["verdict"],
            "label": int(label),
            "prob_unsupported": round(float(prob), 6),
            "pred_unsupported": pred,
            "correct": bool(pred == int(label)),
            "answer": ex["answer"],
            "context_preview": ex["context"][:300],
        })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


@torch.no_grad()
def smoke_tests(model, tokenizer):
    print("\n=== Smoke tests with fine-tuned S4 only ===")

    cases = [
        (
            "SUPPORTED",
            "Retrieval-augmented generation combines retrieval with generation.",
            "Retrieval-augmented generation combines a pretrained generator with a retrieval component over external documents.",
        ),
        (
            "UNSUPPORTED",
            "RAG was invented in 1995 by a secret government laboratory and requires quantum hardware.",
            "Retrieval-augmented generation combines a pretrained generator with a retrieval component over external documents.",
        ),
        (
            "PARTIAL",
            "Cross-encoder reranking improves retrieval and always runs in under one millisecond.",
            "Cross-encoder reranking can improve retrieval quality, but it is computationally more expensive than first-stage retrieval.",
        ),
    ]

    model.eval()

    for name, claim, evidence in cases:
        enc = tokenizer(
            claim,
            evidence,
            max_length=MAX_LENGTH,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        input_ids = enc["input_ids"].to(DEVICE)
        attention_mask = enc["attention_mask"].to(DEVICE)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        p_unsup = torch.softmax(outputs.logits, dim=1)[0, 1].item()

        print(f"{name:<12} p_unsupported={p_unsup:.4f} | claim={claim}")


# ---------------------------------------------------------------------
# Main training loop
# ---------------------------------------------------------------------
def main():
    set_seed(SEED)

    print("Device:", DEVICE)
    print("AMP:", USE_AMP)
    print("Base model:", BASE_MODEL_DIR)
    print("Output dir:", OUTPUT_DIR)

    train_records = load_json(TRAIN_PATH)
    val_records = load_json(VAL_PATH)
    test_records = load_json(TEST_PATH)

    summarize_split("TRAIN", train_records)
    summarize_split("VAL", val_records)
    summarize_split("TEST", test_records)

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL_DIR)

    # Make label convention explicit in saved config.
    model.config.id2label = {
        0: "SUPPORTED",
        1: "UNSUPPORTED",
    }
    model.config.label2id = {
        "SUPPORTED": 0,
        "UNSUPPORTED": 1,
    }

    model.to(DEVICE)

    train_ds = VerifierDataset(train_records, tokenizer, MAX_LENGTH)
    val_ds = VerifierDataset(val_records, tokenizer, MAX_LENGTH)
    test_ds = VerifierDataset(test_records, tokenizer, MAX_LENGTH)

    train_loader = DataLoader(
        train_ds,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available(),
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available(),
    )

    test_loader = DataLoader(
        test_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available(),
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LR,
        weight_decay=WEIGHT_DECAY,
    )

    total_steps = EPOCHS * len(train_loader)
    warmup_steps = int(WARMUP_RATIO * total_steps)

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps,
    )

    scaler = torch.cuda.amp.GradScaler(enabled=USE_AMP)

    best_val_auroc = -1.0
    best_epoch = -1
    bad_epochs = 0

    history = []

    print("\n=== Training ===")

    for epoch in range(1, EPOCHS + 1):
        model.train()
        total_loss = 0.0

        pbar = tqdm(train_loader, desc=f"epoch {epoch}/{EPOCHS}")

        for batch in pbar:
            optimizer.zero_grad(set_to_none=True)

            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels = batch["labels"].to(DEVICE)

            with torch.cuda.amp.autocast(enabled=USE_AMP):
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels,
                )
                loss = outputs.loss

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()

            total_loss += float(loss.item())
            pbar.set_postfix(loss=f"{loss.item():.4f}")

        avg_train_loss = total_loss / max(1, len(train_loader))

        val_probs, val_labels, val_indices = predict_probs(model, val_loader)
        val_threshold, val_best_f1 = best_threshold_by_f1(val_probs, val_labels)
        val_metrics = metrics_at_threshold(val_probs, val_labels, val_threshold)

        print(
            f"\nEpoch {epoch}: "
            f"train_loss={avg_train_loss:.4f} | "
            f"val_AUROC={val_metrics['auroc']:.4f} | "
            f"val_AUPRC={val_metrics['auprc']:.4f} | "
            f"val_F1={val_metrics['f1']:.4f} | "
            f"val_P={val_metrics['precision']:.4f} | "
            f"val_R={val_metrics['recall']:.4f} | "
            f"val_ECE={val_metrics['ece']:.4f} | "
            f"thr={val_threshold:.2f}"
        )

        history.append({
            "epoch": epoch,
            "train_loss": avg_train_loss,
            "val_metrics": val_metrics,
        })

        # Model selection by validation AUROC.
        if val_metrics["auroc"] > best_val_auroc:
            best_val_auroc = val_metrics["auroc"]
            best_epoch = epoch
            bad_epochs = 0

            print(f"  New best val AUROC. Saving to {OUTPUT_DIR}")
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            model.save_pretrained(OUTPUT_DIR)
            tokenizer.save_pretrained(OUTPUT_DIR)

            # Save val predictions for the best checkpoint.
            save_predictions(
                os.path.join(RESULTS_DIR, "val_predictions_best.json"),
                val_records,
                val_probs,
                val_labels,
                val_indices,
                val_threshold,
            )

        else:
            bad_epochs += 1
            print(f"  No improvement. bad_epochs={bad_epochs}/{PATIENCE}")

            if bad_epochs >= PATIENCE:
                print("Early stopping.")
                break

    print("\n=== Loading best checkpoint ===")
    print("Best epoch:", best_epoch)
    print("Best val AUROC:", best_val_auroc)

    best_model = AutoModelForSequenceClassification.from_pretrained(OUTPUT_DIR)
    best_model.to(DEVICE)
    best_model.eval()

    # Recompute val threshold using best checkpoint.
    val_probs, val_labels, val_indices = predict_probs(best_model, val_loader)
    final_threshold, _ = best_threshold_by_f1(val_probs, val_labels)
    val_final_metrics = metrics_at_threshold(val_probs, val_labels, final_threshold)

    print("\n=== Final validation metrics ===")
    print(json.dumps(val_final_metrics, indent=2))

    # Final test evaluation: threshold fixed from validation.
    test_probs, test_labels, test_indices = predict_probs(best_model, test_loader)
    test_metrics = metrics_at_threshold(test_probs, test_labels, final_threshold)

    print("\n=== Final grouped test metrics ===")
    print(json.dumps(test_metrics, indent=2))

    save_predictions(
        os.path.join(RESULTS_DIR, "test_predictions.json"),
        test_records,
        test_probs,
        test_labels,
        test_indices,
        final_threshold,
    )

    results = {
        "base_model_dir": BASE_MODEL_DIR,
        "output_dir": OUTPUT_DIR,
        "train_path": TRAIN_PATH,
        "val_path": VAL_PATH,
        "test_path": TEST_PATH,
        "seed": SEED,
        "max_length": MAX_LENGTH,
        "batch_size": BATCH_SIZE,
        "epochs_requested": EPOCHS,
        "best_epoch": best_epoch,
        "selection_metric": "val_auroc",
        "threshold_tuned_on": "validation_f1",
        "final_threshold": final_threshold,
        "history": history,
        "val_metrics": val_final_metrics,
        "test_metrics": test_metrics,
        "label_mapping": {
            "SUPPORTED": 0,
            "CONTRADICT": 1,
            "NEI": 1,
        },
        "split_note": "custom source-stratified grouped split; no claim_id or abstract_id overlaps across train/val/test",
    }

    results_path = os.path.join(RESULTS_DIR, "finetune_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved results to {results_path}")
    print(f"Saved model to {OUTPUT_DIR}")

    smoke_tests(best_model, tokenizer)


if __name__ == "__main__":
    main()
