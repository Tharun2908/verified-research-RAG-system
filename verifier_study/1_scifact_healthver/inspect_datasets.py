from datasets import load_dataset

print("=== SciFact (entailment) ===")
try:
    sf = load_dataset("allenai/scifact_entailment")
    print("splits:", list(sf.keys()))
    ex = sf[list(sf.keys())[0]][0]
    print("fields:", list(ex.keys()))
    print("example:", {k: (str(v)[:120]) for k, v in ex.items()})
    # label distribution
    split0 = list(sf.keys())[0]
    labels = [e.get("label") or e.get("verdict") for e in sf[split0]]
    from collections import Counter
    print("label counts:", Counter(labels))
except Exception as e:
    print("scifact_entailment failed:", e)
    print("trying allenai/scifact...")
    sf = load_dataset("allenai/scifact", "claims")
    print("splits:", list(sf.keys()))
    print("fields:", list(sf[list(sf.keys())[0]][0].keys()))

print("\n=== HealthVer ===")
for name in ["healthver", "dwadden/healthver", "bigbio/healthver"]:
    try:
        hv = load_dataset(name)
        print(f"LOADED as '{name}'. splits:", list(hv.keys()))
        ex = hv[list(hv.keys())[0]][0]
        print("fields:", list(ex.keys()))
        print("example:", {k: str(v)[:120] for k, v in ex.items()})
        break
    except Exception as e:
        print(f"  '{name}' failed: {str(e)[:100]}")
