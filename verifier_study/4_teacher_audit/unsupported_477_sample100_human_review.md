# Blind Human Audit — 100 Opus Disagreements

Fill `FINAL_LABEL` with exactly one of:

- `SUPPORTED`
- `UNSUPPORTED`
- `ABSTENTION`
- `INVALID_EXTRACTION`

The Opus draft label is hidden. Do not use verifier scores or grounded-hard results.

---

## U100_001 — v2_train_r354_cited_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `354`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What are the reported fooled rates for a single polluted page versus full top-3 replacement in the FORGE benchmark?

### Claim

The reported fooled rates for a single polluted page in the FORGE benchmark are up to 27%, and for full top-3 replacement, the rate increases to 73.8%.

### Evidence

```text
[1] One Polluted Page Is Enough: Evaluating Web Content Pollution in Generative Recommenders
Search-augmented LLMs increasingly mediate everyday consumer recommendations by retrieving live web content. This creates a new risk: generative recommenders may consume polluted web content, such as fake reviews and promotional pages crafted to mislead recommendations. We ask: to what extent do search-augmented LLMs become unwitting promoters of fake products when consuming polluted retrieval results? To answer this, we introduce FORGE (Fake Online Recommendations in Generative Environments), a benchmark for measuring fake-product promotion under controlled web-content pollution. Given an upstream search result, FORGE locally rewrites real products in retrieved web pages into fake ones to simulate web-content pollution, and measures how often the LLM recommends the fake product. FORGE covers 225 real-world products across 15 categories and 5 consumer scenarios. Across 12 commercial and open-weights LLMs, all models are vulnerable: a single polluted page yields fooled rates of up to 27%, while the full top-3 replacement raises this to 73.8%. Vulnerability varies substantially across categories, increasing when models lack stable prior knowledge of the relevant products. Reasoning does not mitigate this vulnerability; instead, it often generates spurious social proof to justify false recommendations. We evaluate three defenses: skepticism prompting and consensus filtering (over model priors or cross-document evidence). Skepticism can exacerbate vulnerability, much like reasoning, while filtering risks suppressing legitimate products. We release FORGE at https://github.com/leoluolol/forge-benchmark.
```

---

## U100_002 — v2_train_r362_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `362`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What trade-off does the paper identify between large retrieval units and fine-grained retrieval units?

### Claim

The paper identifies a trade-off between large retrieval units and fine-grained retrieval units in terms of context preservation and relevance.

### Evidence

```text
[1] Uncertainty-Aware Hybrid Retrieval for Long-Document RAG
Retrieval augmented generation (RAG) depends critically on the quality and granularity of retrieved evidence. Large retrieval units preserve context but often introduce irrelevant content, which can dilute answer bearing evidence and worsen long context utilization. Fine-grained units are more compact, but they may be difficult to retrieve reliably because short chunks can lack semantic, lexical, or bridging cues needed to match the query. We propose Uncertainty-aware Multi-Granularity RAG (UMG-RAG), a training-free hybrid retrieval framework that treats chunk granularity as query-specific reliability estimation. Instead of training a new retriever or modifying the generator, UMG-RAG uses existing dense and sparse retrievers as complementary experts across multiple chunk granularities. For each query, it converts each expert-granularity score list into an evidence distribution, estimates reliability from distribution entropy, and fuses candidates according to query-specific semantic, lexical, and granularity confidence. We further introduce UMGP-RAG, a parent promotion variant that uses fine-grained hits to locate relevant evidence while returning broader non-redundant parent chunks for local coherence. Experiments on question answering benchmarks show that uncertainty-aware fusion and parent promotion improve generation quality while maintaining a lightweight, plug-and-play retrieval pipeline.

[2] Retrieval-as-a-Service:A System-Oriented Analysis of Industrial Retrieval Pipelines in Web Systems
Retrieval systems have become a foundational infrastructure component in modern Web services, supporting applications such as content recommendation, advertising targeting, and API discovery. In large-scale industrial environments, retrieval is increasingly deployed as an independent service layer, commonly referred to as Retrieval-as-a-Service (RaaS). This paper presents a system-oriented survey of industrial retrieval pipelines, focusing on architectural design and deployment trade-offs under real-world constraints. Unlike prior surveys that emphasize algorithmic developments, we analyze retrieval systems from an infrastructure perspective, highlighting how latency requirements, scalability constraints, and resource limitations shape system design in production environments. We introduce a unified RaaS pipeline abstraction that models retrieval as a multi-stage service, including high-efficiency candidate generation, embedding-based semantic matching, and resource-aware re-ranking. We further examine the integration of Large Language Model (LLM)-based retrieval mechanisms and analyze their impact on semantic performance, latency, and computational overhead. The results provide a system-level understanding of retrieval as a service-oriented infrastructure and offer practical guidelines for designing scalable, efficient, and QoS-aware retrieval architectures in large-scale Web systems.

[3] MAGE-RAG: Multigranular Adaptive Graph Evidence for Agentic Multimodal RAG in Long-Document QA
Long-document multimodal question answering requires a system to locate sparse evidence in long PDFs and integrate clues from text, tables, images, charts, and complex layouts. Existing RAG methods mostly rely on fixed Top-k retrieval over text chunks or pages. Text retrieval can compress the context but often loses visual and layout information; page-level visual retrieval preserves the original page, yet it also sends large irrelevant regions to the reader, leading to a static trade-off among evidence coverage, noise, and inference cost. This paper proposes MAGE-RAG, a multigranular adaptive graph evidence framework for long-document multimodal QA. MAGE-RAG uses page retrieval as the entry point for query-time evidence construction. Offline, it builds an evidence graph with page nodes and element nodes, encoding containment, reading order, layout adjacency, section hierarchy, and semantic-neighbor relations. At query time, an online evidence controller iteratively activates, opens, searches, and prunes evidence under explicit budgets. The resulting evidence subgraph is then rendered into structured multimodal reader input, allowing the LVLM to consume compact and relevant evidence within a limited context. On LongDocURL and MMLongBench-Doc, we establish a unified comparison and analysis protocol covering Direct MLLM, Text RAG, Page-level Visual RAG, and Graph/Agentic RAG. Experiments show that MAGE-RAG achieves 52.75 overall accuracy on LongDocURL, and 53.26 accuracy with 51.19 F1 on MMLongBench-Doc. Fine-grained breakdowns, budget-performance curves, ablations, and trace-based analysis further show that query-time evidence subgraph construction can balance dispersed evidence coverage with context-noise control. Our code is available at https://github.com/laonuo2004/MAGE-RAG.git.
```

---

## U100_003 — v2_train_r258_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `258`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three key innovations that OneBar introduces for real-time query recommendation in E-Commerce video feeds?

### Claim

A collaborative-multimodal intent grounding module that fuses multimodal video understanding and behavior-derived collaborative anchors. 2.

### Evidence

```text
[1] OneBar: An End-to-End Content-Grounded Generative Query Recommendation Framework for E-Commerce Video Feeds
Short-video platforms now expose clickable search entries beneath the video player, enabling users to easily express content-induced search intent. However, conventional query recommendation systems on short-video platforms suffer from latency constraints and objective misalignment, while recent generative approaches struggle with noisy content-side metadata and preference drift. To address these issues, we propose OneBar, an end-to-end generative framework for real-time query recommendation for E-Commerce video feeds. OneBar features three key innovations: (1) a collaborative-multimodal intent grounding module that fuses multimodal video understanding and behavior-derived collaborative anchors; (2) a Unified End-to-End architecture equipped with a prompt-compression mechanism for efficient online serving; and (3) a progressive preference learning strategy for efficient preference-internalization, which internalizes hierarchical behavior preferences into the generative policy, eliminating the need for a separately trained reward model. Compared with online base, OneBar increases Query Exposure by 16.91\% and Query Click by 18.68\%, while maintaining a slight Query CTR gain of 0.19\%. The additional search traffic further contributes to 20.36\% more guided orders and 21.67\% higher GMV.

[2] VCG: A Multimodal Retrieval Framework for E-Commerce Video Feeds under Extreme Cold-Start Conditions
The digital commerce landscape is shifting from static, search-driven catalogs to dynamic, immersive video feeds. This transition introduces an ``extreme cold-start'' problem: unlike traditional items, new short-form videos lack the dense interaction history required for collaborative filtering. Furthermore, immersive feeds introduce strong position and duration biases that distort standard engagement signals. In this paper, we demonstrate the Video Candidate Generation (VCG) system, a scalable multimodal retrieval engine designed to solve these challenges in a large-scale e-commerce environment. By leveraging a domain-adapted vision-language model (based on CLIP), we map users and videos into a shared semantic space, enabling zero-shot retrieval based on visual content rather than behavioral history. We detail the system's architecture and present a rigorous evaluation comparing generative (LLM) vs. discriminative (CLIP) embeddings. Our results show that while generative models excel at attribute prediction, they suffer from embedding space collapse in retrieval tasks. Online A/B testing demonstrates that VCG effectively mitigates engagement biases, yielding a 50\% uplift in deep video completion. To showcase the system's capabilities, we present an interactive demonstration featuring three bi-directional retrieval scenarios: Product-to-Video, Video-to-Product, and Zero-Shot Semantic Search.

[3] Decoupling Search from Reasoning: A Vendor-Agnostic Grounding Architecture for LLM Agents
Production LLM agents increasingly depend on real-time search, yet native search grounding bundles retrieval policy, provider choice, evidence injection, cost, latency, and generation behavior behind a single model-provider boundary. This coupling makes grounding hard to inspect, tune, reuse, or port, and can trigger Search-Induced Verbosity that breaks strict output contracts. We present Decoupled Search Grounding (DSG), a vendor-agnostic boundary that moves grounding outside the reasoning model through an MCP-compatible gateway, exposing provider routing, source-aware context rendering, configured fallback, retrieval-depth control, and exact plus semantic caching as first-class controls. Across five frontier models on SimpleQA, FreshQA, and HotpotQA, native search leads on recency-sensitive FreshQA, but DSG exposes a stronger frontier when control matters: on SimpleQA it nearly matches native accuracy (86.1% vs. 87.7%) at 91% lower search cost, preserves concise answer contracts, and reaches a 99.4% warm-cache hit rate with 68% lower latency. Deployed as a shared production grounding layer for large-scale agentic workloads with interchangeable models, DSG matches or slightly exceeds native-search accuracy on an e-commerce query-understanding (QIU) workload while cutting search cost by over 98%. Real-time grounding is best treated as an optimizable interface boundary, not a fixed model feature.
```

---

## U100_004 — v2_train_r455_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `455`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

What is the exact size of the training corpus used for pretraining the MedVLM-2 vision-language model, and how many radiology reports were included?

### Claim

However, they mention a large-scale bilingual (German/English) dataset of 1.2M CT and MR image-text pairs derived from clinical practice, which suggests that the training corpus is quite substantial.

### Evidence

```text
[1] Scalable Training of Spatially Grounded 2D Vision-Language Models for Radiology
We study how to train visually grounded vision-language models (VLMs) for radiology without manual spatial annotations. We introduce RefRad2D, a large-scale bilingual (German/English) dataset of 1.2M CT and MR image-text pairs derived from clinical practice, with task-specific VQA and spatial grounding subsets generated automatically via LLM-based curation and automated segmentation. Trained on this data, our model RadGrounder jointly performs report generation, visual question answering, and spatial grounding via bounding-box detection or segmentation. On external VQA benchmarks (Slake, VQA-RAD), RadGrounder achieves competitive results with specialized medical VLMs. Adding our clinical data to the training mixture improves open-ended VQA over fine-tuning on the downstream datasets alone, showing the transferability of our dataset. Crucially, adding grounding supervision does not degrade language quality, enabling spatially verifiable outputs at no cost to VQA performance.

[2] Where Does Social Reasoning Come From? Capability Provenance in Language Models
We use training-data attribution as an interpretable tool for capability discovery, mapping which regions of the pretraining corpus support social-reasoning versus STEM-reasoning in OLMo3-7B. Training-data attribution measures how strongly each training document influences a model's predictions on a benchmark, but document-level scores are too noisy to identify which corpus regions support which capabilities, and prior work has emphasized factual knowledge rather than reasoning. We compute gradient-based attribution (TrackStar via Bergson) over a working set drawn from the de-duplicated Dolma3 mix, aggregate influence across WebOrganizer's 24-format x 24-topic taxonomy (576 bins), and contrast benchmark pairs in a 2x2 design that varies domain (social vs. STEM) and capability type (reasoning vs. knowledge): SocialIQA and MMLU Social Sciences against ARC-Challenge and MMLU STEM. Social and STEM reasoning draw on qualitatively distinct corpus regions, and the contrast is sharper at the reasoning level than at the knowledge level. Targeted machine unlearning provides partial causal validation: forgetting high-attribution topic bins (e.g., Literature for SocialIQA) degrades the aligned benchmark more than within-bin random baselines, and we open-source all code, sampling manifests, the bin-level influence matrix, and unlearning checkpoints.

[3] TASR: Training-Free Adaptive Stopping for Iterative Retrieval
Iterative retrieval-augmented generation agents commonly overspend by continuing to retrieve after the model has converged on an answer, incurring calls that change neither the prediction nor the supporting evidence. Existing remedies learn a stopping policy from labeled trajectories, tying the decision to a trained component that requires retraining for each new model or task. We propose TASR (Training-Free Adaptive Stopping Rule), a one-line predicate that fires when the model repeats its previous-round normalized answer and the isotonically calibrated logit margin exceeds 0.25. No classifier or value head is learned; the threshold is fixed across all twenty-four (model, retriever, corpus) configurations we evaluate. On a 3-model x 2-dataset distractor grid, TASR retains 94.8% of fixed-k=5's macro F1 at 62.6% of its calls and exceeds fixed-k=3 by +3.42 F1. The pattern holds on nine open-domain BM25 cells (55.01 F1 at 2.98 calls vs. 54.33 at 3.00 for fixed-k=3) and, with calibration locked from the distractor split, on nine dense-retrieval cells across two retriever families, with zero significant regressions in either extension. The rule was selected from an exhaustive enumeration of 381 candidate stopping rules; no alternative Pareto-dominates it on any evaluated configuration. A signal-quality analysis shows that verbalized 1-5 confidence collapses on RLHF-tuned models (96.5% of values equal 5, entropy 0.182 nats), while the logit margin achieves 44x better class-conditional separation, grounding the design in a measurable model pathology. TASR is an auditable, training-free Pareto baseline against which learned stopping controllers can be compared. Code is publicly available.
```

---

## U100_005 — v2_train_r185_plain_c004

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `185`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

According to the comparison with eight external systems, which four capabilities does StateGen combine that no single publicly available platform offers?

### Claim

Hierarchical multi-agent support 4.

### Evidence

```text
[1] State-Grounded Multi-Agent Synthetic Data Generation for Tool-Augmented LLMs
Training tool-augmented LLM agents requires large corpora of multi-turn, tool-grounded conversational data that is expensive to annotate, privacy-constrained in production settings, and largely absent from public datasets. We present StateGen, a synthetic data generation platform that produces scored, reasoning-trace-rich training conversations by orchestrating a four-role LLM loop: a persona-conditioned user simulator, an agent under test, a state-grounded tool simulator, and a multi-axis LLM judge. The key architectural contribution is an authoritative state manager that maintains a structured world-state object across turns, enforcing a backend-is-truth invariant that eliminates the dominant class of tool-call hallucinations by construction. StateGen extends naturally to hierarchical multi-agent settings by declaring sub-agents as tools, all sharing a single state object. We report results on 64,698 evaluated conversations across three production corpora: tool-call hallucination scores reach 9.66/10, the system supports persona-driven variation via a 23-dimensional trait vector, and a cleanly separated train and golden evaluation set split confirms the data is not memorization bait (per-criterion gap analysis). Comparison with eight external systems shows that no single publicly available platform combines multi-turn generation, state-grounded tool simulation, hierarchical multi-agent support, and built-in judge scoring.

[2] ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages
Multimodal Large Language Models (MLLMs) have shown promising reasoning capabilities in general domains, yet their performance remains limited in specialized settings such as healthcare, especially in multilingual and low-resource scenarios. This gap is critical in regions like rural India, where patients often express complex medical queries in native Indic languages and rely on multimodal inputs such as medical images. Existing English-centric MLLMs struggle to support such use cases, limiting equitable access to AI-driven healthcare assistance. To address this challenge, we introduce ArogyaBodha, a large-scale multilingual multimodal medical question-answer dataset constructed from eight heterogeneous sources, covering 31 body systems, six imaging modalities, and 21 clinical domains across English and seven major Indian languages. We further propose ArogyaSutra, an actor-critic-based multi-agent framework that integrates tool grounding with dual-memory mechanisms for step-wise, reasoning-aware decision making, and uses stored actor-critic simulation trajectories for distillation. Experiments show that our dataset and framework improve multilingual medical reasoning accuracy across all Indic languages, with ablations validating the contribution of each component. The source code and dataset are available at: https://iitp-cse.github.io/ ArogyaSutra/

[3] Intelligent Multimodal Retrieval and Reasoning for Geospatial Knowledge Discovery on the I-GUIDE Platform
Geospatial knowledge discovery increasingly requires search across heterogeneous artifacts: datasets, maps, notebooks, software, publications, and the provenance links among them. Conventional geoportals support metadata and spatial filtering, but they rarely provide semantic retrieval, graph-aware provenance traversal, and conversational synthesis in one integrated system. This paper presents I-GUIDE Smart Search, a production multimodal geospatial retrieval-augmented generation (RAG) system embedded in the I-GUIDE Platform, and reports on its design, deployment, and evaluation. The system combines production-maintained OpenSearch keyword, vector, and spatial indexes with a Neo4j knowledge graph and an iterative RAG pipeline for memory-aware query augmentation, reasoning, retrieval-method routing, relevance grading, grounded generation, hallucination and relevance checking. In a single-A100 RAG deployment, I-GUIDE Smart Search supports interactive use up to about 100 concurrent simulated users, reaching 4.4 requests per second with p50 latency near 25 seconds despite 20-50 LLM calls per query. For answer quality, we evaluate a four-category benchmark of 170 unique human-filtered user-facing queries, together with ten intent-specific probe sets generated from the deployed indexes and graph. Smart Search improves retrieved evidence coverage and judged answer quality over non-retrieval and naive-RAG baselines, with the clearest gains on exact-identifier, spatially constrained, simple-recommendation, and domain-specific factual queries requiring current indexed evidence. We distill transferable deployment lessons for spatial RAG systems, covering spatial metadata quality, graph provenance, retrieval routing, interface contracts, refusal-aware evaluation, latency-cost tradeoffs, and the role of the user interface in deployed geospatial cyberinfrastructure.
```

---

## U100_006 — v2_train_r196_cited_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `196`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three recurring failure modes identified in LLM-based formal reasoning, and how is scope laundering defined?

### Claim

The three recurring failure modes identified in LLM-based formal reasoning are: 1.

### Evidence

```text
[1] Know Your Limits : On the Faithfulness of LLMs as Solvers and Autoformalizers in Legal Reasoning
Large Language Models (LLMs) achieve strong performance on reasoning tasks, but whether this reflects faithful logical inference or heuristic approximation remains unclear. We study this question in legal entailment by comparing three paradigms, including pure LLM classification, LLM-based Formal Reasoning, and solver-based Formal Reasoning using the Z3 SMT solver, on a re-annotated subset of ContractNLI across five LLMs. Our re-annotation reveals a systematic and measurable gap between pragmatic legal interpretation and strict formal entailment, where a substantial proportion of legally sound inferences are not formally grounded without additional unstated assumptions. While introducing formal structure improves accuracy, with LLM-based Formal Reasoning achieving the highest benchmark performance, we show that this gain does not imply faithful reasoning. We identify three recurring failure modes: scope laundering, where LLMs report solver-inconsistent classifications without executing the underlying formal reasoning, producing conclusions that appear logically grounded but are not; implicit constraint blindness, where LLMs overlook logical constraints present in formal representations; and program synthesis failures, where LLMs generate incorrect Z3 code despite structured prompting. Critically, scope laundering persists across all models, raising serious concerns about the faithfulness of LLM-based formal reasoning as a proxy for symbolic execution. These results reveal a fundamental gap between benchmark accuracy and logical faithfulness.

[2] SIMMER: Benchmarking Latent Failures in LLM Executable Planning with a World Model
Large language models (LLMs) are increasingly deployed as planners for autonomous agents in household environments. While existing benchmarks evaluate whether LLM-generated plans execute successfully, they overlook a critical type of failure: latent failures. Unlike immediate failures that trigger instant feedback at execution time and enable timely correction, latent failures do not immediately halt plan execution but silently compromise goal achievement. In severe cases, they cause irreversible harm. To address this gap, we introduce SIMMER, a benchmark for evaluating latent failures in LLM planning through a human-curated symbolic world model grounded in the kitchen domain. SIMMER defines a world model comprising 77 actions, 262 unique objects, and approximately 46,800 possible interactions that are semantically realistic, derived from real-world cooking scripts. It then leverages a state machine executor that validates plans against the world model and detects immediate precondition violations, latent hazards, and irreversible failures. Experiments across six LLMs show that even frontier models achieve at most 17% error-free plans. Moreover, up to 56% of plans contain latent failures, the majority of which lead to irreversible consequences. We further demonstrate that explicit state reasoning via counterfactual foresight simulation can reduce latent failures by up to 72% and irreversible cases by up to 75%, suggesting a promising direction for more robust LLM planners.

[3] Understanding and Debugging Failures in N-Gram-Based Generative Retrieval
Generative Retrieval (GR) is an emerging Information Retrieval (IR) paradigm that is motivated by increasingly capable language models. In GR, a model directly generates identifiers for relevant documents. While these systems offer unique advantages, they also introduce distinct failure mechanisms. We explore these failure modes in three contributions: (1) We present a taxonomy of GR failure modes based on GR literature. (2) We empirically investigate failure in a subset of GR: ngram-based methods, more specifically, SEAL and MINDER. Our analysis reveals common issues, such as ambiguous docids, low identifier diversity, and the disproportionate impact of specific identifiers. (3) We introduce a new web-based tool that helps the IR community analyze generated ngrams and their respective contribution to the final ranking, providing an intuitive interface to identify where such GR methods go wrong.
```

---

## U100_007 — v2_train_r512_cited_c001

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `512`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

What are the two pretraining stages of the VidLangPro video-language model, and how many hours of video are used in each stage?

### Claim

I'm sorry for any confusion, but the question asks about the pretraining stages of a Large Language Model (LLM), not a VidLangPro video-language model.

### Evidence

```text
[1] Implicit Reasoning for Large Language Model-based Generative Recommendation
Large Language Models (LLMs) are increasingly adopted as backbones for Generative Recommendation (GR), promising access to pretrained world knowledge. Yet reliably invoking this knowledge for GR remains poorly understood. A key obstacle is that LLM-based GR typically represents items with Semantic IDs (SIDs), disrupting LLMs' natural-language reasoning interface because these tokens are unseen by the LLM during pretraining. Existing approaches address this with expensive multi-stage pipelines that ground SIDs and elicit explicit rationales, but offer limited insight into when and why each stage is necessary. In this work, we systematically decompose explicit reasoning training pipelines for LLM-based GR, revealing three key limitations: weakened world-knowledge verbalization, misalignment between SID and natural-language token embedding spaces, and sensitivity to rationale quality, all of which hurt explicit reasoning performance. To circumvent these issues, we propose PauseRec, a lightweight implicit reasoning paradigm tailored for GR. PauseRec is exceptionally practical, avoiding costly reasoning trace acquisition and reasoning alignment training, leading to a multitude of benefits: (1) it outperforms standard explicit CoT methods by up to 6.22%, (2) it reduces training cost by up to 65% GPU hours, and (3) it speeds up inference by up to 71.3%. These results position PauseRec as a lightweight alternative to explicit rationale generation, enabling more effective and efficient LLM-based GR.

[2] IndicContextEval: A Benchmark for Evaluating Context Utilisation in Audio Large Language Models Across 8 Indic Languages
AudioLLMs enable speech recognition conditioned on textual prompts such as domain descriptions or entity lists. However, it remains unclear whether these models genuinely utilise such context or rely on parametric knowledge learned during pretraining. Existing benchmarks cannot answer this question because they evaluate transcription under fixed prompting conditions and rarely include explicit contextual inputs. We introduce IndicContextEval, a 56-hour multilingual benchmark of natural speech from 555 speakers across 8 Indian languages and 23 professional domains. We design a 7-level prompting framework that progressively introduces contextual signals, including metadata, natural-language descriptions, entity lists in English and native script, and adversarial prompts with incorrect entities. Evaluating five models reveals substantial differences in context utilisation behaviour, highlighting the need for explicit evaluation of contextual grounding in AudioLLMs.

[3] Prior over Evidence: Stereotype-Driven Diagnosis in LLM-Based L2 Pronunciation Feedback
Large language models are increasingly deployed for written pronunciation feedback in second-language (L2) English learning, under the assumption that their diagnoses are grounded in the supplied speech evidence rather than in priors from pretraining. This assumption is tested on 1,800 L2-Arctic utterances spanning six L1 backgrounds, three audio-capable LLMs, four pronunciation dimensions, and five evidence conditions ranging from a text-only baseline to numeric acoustic features and raw audio. Each (utterance x model x condition x dimension) cell is scored on three metrics: Rating Accuracy (RA) against gold labels, Evidence Coherence (EC) assessing internal consistency without ground truth, and Grounded Correctness (GC) evaluated against gold evidence. Results show three findings across models. First, rating accuracy and grounded reasoning decouple: 39.6% of judged cells contain internally coherent reasoning that supports a wrong rating, against only 15.8% where the reasoning supports a correct rating. Second, phoneme-level feedback converges to a fixed inventory of L2-English difficulty phones that recurs across all six L1 backgrounds and all evidence conditions. Third, acoustic evidence improves the rating only when the supplied feature directly probes the target dimension: textualised F0 range raises pitch-variation grounding from (0.18-0.19) to (0.45-0.62) across all three models, while stress and phoneme correctness, which require target-to-realisation alignment, remain ungrounded. The same audio waveform without textualised F0 values does not reproduce this improvement. These findings indicate that current general-purpose LLMs are more reliable as verbalisers of externally computed pronunciation evidence than as standalone diagnostic engines.
```

---

## U100_008 — v2_train_r1_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What is the composition and scale of the RefRad2D dataset, including its imaging modalities and languages?

### Claim

It includes task-specific Visual Question Answering (VQA) and spatial grounding subsets generated automatically via LLM-based curation and automated segmentation.

### Evidence

```text
[1] Scalable Training of Spatially Grounded 2D Vision-Language Models for Radiology
We study how to train visually grounded vision-language models (VLMs) for radiology without manual spatial annotations. We introduce RefRad2D, a large-scale bilingual (German/English) dataset of 1.2M CT and MR image-text pairs derived from clinical practice, with task-specific VQA and spatial grounding subsets generated automatically via LLM-based curation and automated segmentation. Trained on this data, our model RadGrounder jointly performs report generation, visual question answering, and spatial grounding via bounding-box detection or segmentation. On external VQA benchmarks (Slake, VQA-RAD), RadGrounder achieves competitive results with specialized medical VLMs. Adding our clinical data to the training mixture improves open-ended VQA over fine-tuning on the downstream datasets alone, showing the transferability of our dataset. Crucially, adding grounding supervision does not degrade language quality, enabling spatially verifiable outputs at no cost to VQA performance.

[2] ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages
Multimodal Large Language Models (MLLMs) have shown promising reasoning capabilities in general domains, yet their performance remains limited in specialized settings such as healthcare, especially in multilingual and low-resource scenarios. This gap is critical in regions like rural India, where patients often express complex medical queries in native Indic languages and rely on multimodal inputs such as medical images. Existing English-centric MLLMs struggle to support such use cases, limiting equitable access to AI-driven healthcare assistance. To address this challenge, we introduce ArogyaBodha, a large-scale multilingual multimodal medical question-answer dataset constructed from eight heterogeneous sources, covering 31 body systems, six imaging modalities, and 21 clinical domains across English and seven major Indian languages. We further propose ArogyaSutra, an actor-critic-based multi-agent framework that integrates tool grounding with dual-memory mechanisms for step-wise, reasoning-aware decision making, and uses stored actor-critic simulation trajectories for distillation. Experiments show that our dataset and framework improve multilingual medical reasoning accuracy across all Indic languages, with ablations validating the contribution of each component. The source code and dataset are available at: https://iitp-cse.github.io/ ArogyaSutra/

[3] NRITYAM: Language Models Meet Art and Heritage of Dance
Language models have become essential tools in shaping modern workflows. However, their global effectiveness hinges on a nuanced understanding of local socio-cultural contexts. To address this gap, we present NRITYAM, a comprehensive benchmark for evaluating the cultural comprehension capabilities of language models in the context of global dance traditions. NRITYAM comprises 9,260 carefully curated question-answer pairs spanning 12 languages, making it the largest dataset dedicated to evaluating cultural knowledge in dance. The dataset has been developed from the ground up through close collaboration with native dance artists and native speakers of the languages, who authored and validated culturally relevant questions specific to their regions. We evaluate a broad set of models, including large language models, small language models, multimodal large language models, and small multimodal language models. As a multilingual and multicultural benchmark, NRITYAM sets a new standard for evaluating the ability of AI systems to understand and reason about traditional performing arts. Detailed dataset samples are available at~\url{https://github.com/niladrighosh03/NRITYAM}.
```

---

## U100_009 — v2_train_r35_plain_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `35`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

Which specific benchmarks are used to represent each cell of the 2x2 design varying domain (social vs. STEM) and capability type (reasoning vs. knowledge)?

### Claim

The specific benchmarks used to represent each cell of the 2x2 design varying domain (social vs.

### Evidence

```text
[1] Where Does Social Reasoning Come From? Capability Provenance in Language Models
We use training-data attribution as an interpretable tool for capability discovery, mapping which regions of the pretraining corpus support social-reasoning versus STEM-reasoning in OLMo3-7B. Training-data attribution measures how strongly each training document influences a model's predictions on a benchmark, but document-level scores are too noisy to identify which corpus regions support which capabilities, and prior work has emphasized factual knowledge rather than reasoning. We compute gradient-based attribution (TrackStar via Bergson) over a working set drawn from the de-duplicated Dolma3 mix, aggregate influence across WebOrganizer's 24-format x 24-topic taxonomy (576 bins), and contrast benchmark pairs in a 2x2 design that varies domain (social vs. STEM) and capability type (reasoning vs. knowledge): SocialIQA and MMLU Social Sciences against ARC-Challenge and MMLU STEM. Social and STEM reasoning draw on qualitatively distinct corpus regions, and the contrast is sharper at the reasoning level than at the knowledge level. Targeted machine unlearning provides partial causal validation: forgetting high-attribution topic bins (e.g., Literature for SocialIQA) degrades the aligned benchmark more than within-bin random baselines, and we open-source all code, sampling manifests, the bin-level influence matrix, and unlearning checkpoints.

[2] Can Agents Read the Room? Benchmarking Visual Social Intelligence in Multimodal Simulation
Social interaction depends on both language and visible social signals, such as facial expressions, posture, gaze, and emotional shifts. Yet existing social-agent benchmarks are largely text-based and rarely test whether multimodal agents can use visual cues to guide interaction. We introduce \textsc{\benchmarkname{}}, a benchmark evaluating visual social intelligence in multimodal social simulation. It contains 240 scenarios, 585 role instances, and 2,340 role-task instances, combining aligned textual-visual evidence, structured role profiles, and four role-level tasks: expression task, characteristic task, interaction regulation task, and interaction outcome task. Evaluating seven recent MLLMs under verbalized-vision and direct-vision reveals a clear gap between local role enactment and interaction management: role-specific expression and conflict handling are near saturation, whereas interaction regulation and visually grounded outcome achievement remain substantially more difficult. The code is released at https://github.com/JunsWan/AgentViSS, and the dataset is available at https://huggingface.co/datasets/JunsWan/AgentViSS.

[3] Weaving Multi-Source Evidence for Biomedical Reasoning: The BioMedHop Benchmark and BioWeave Framework
Biomedical question answering (QA) increasingly requires reasoning over interacting entities, where supporting evidence is scattered across biomedical knowledge graphs, literature documents, and web-accessible resources. However, existing biomedical QA benchmarks mainly focus on exam-style knowledge, literature comprehension, or short-range multi-hop inference, leaving source-conditioned graph reasoning and evidence topology construction underexplored. To fill this gap, we introduce BioMedHop, a multi-source graph-grounded benchmark for evaluating biomedical reasoning over structured evidence topologies. BioMedHop contains 10,045 instances across KG, document, web, and hybrid evidence settings, covering shared-neighbor matching, intersection reasoning, path-based reasoning, and counting, with option-based, open-ended, and numeric count renderings. To support this benchmark, we further propose BioWeave, a source-aware reasoning framework that retrieves biomedical KG paths, gathers supporting clues from documents and web sources, assembles them into a unified evidence graph, and verifies answers through entity-level evidence support. Comprehensive experiments show that BioWeave achieves the best overall performance among compared methods on BioMedHop, outperforming the strong hybrid baseline ToG-2 by 10.5% in the overall average. Moreover, BioWeave consistently improves different LLM backbones and enables smaller models, such as Qwen3-4B, to achieve reasoning performance comparable to GPT-4-Turbo.
```

---

## U100_010 — v2_train_r183_plain_c002

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `183`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the four roles in the LLM loop orchestrated by StateGen to generate training conversations?

### Claim

A persona-conditioned user simulator 2.

### Evidence

```text
[1] State-Grounded Multi-Agent Synthetic Data Generation for Tool-Augmented LLMs
Training tool-augmented LLM agents requires large corpora of multi-turn, tool-grounded conversational data that is expensive to annotate, privacy-constrained in production settings, and largely absent from public datasets. We present StateGen, a synthetic data generation platform that produces scored, reasoning-trace-rich training conversations by orchestrating a four-role LLM loop: a persona-conditioned user simulator, an agent under test, a state-grounded tool simulator, and a multi-axis LLM judge. The key architectural contribution is an authoritative state manager that maintains a structured world-state object across turns, enforcing a backend-is-truth invariant that eliminates the dominant class of tool-call hallucinations by construction. StateGen extends naturally to hierarchical multi-agent settings by declaring sub-agents as tools, all sharing a single state object. We report results on 64,698 evaluated conversations across three production corpora: tool-call hallucination scores reach 9.66/10, the system supports persona-driven variation via a 23-dimensional trait vector, and a cleanly separated train and golden evaluation set split confirms the data is not memorization bait (per-criterion gap analysis). Comparison with eight external systems shows that no single publicly available platform combines multi-turn generation, state-grounded tool simulation, hierarchical multi-agent support, and built-in judge scoring.

[2] Which Models Are Our Models Built On? Auditing Invisible Dependencies in Modern LLMs
Modern LLM training pipelines increasingly rely on other models to generate data, filter corpora, judge outputs, and guide development decisions. These dependencies are recursive: a model may depend on an upstream artifact whose own dependencies are documented only in separate releases and artifacts. As a result, the full dependency structure is fragmented across heterogeneous public artifacts, with complexity and recursive depth far outpacing humans' ability to trace. We introduce ModSleuth, an agentic system that recursively reconstructs LLM dependency graphs from public artifacts with source-grounded evidence. We find that the primary challenge is no longer information extraction, but defining what constitutes a dependency and reconciling artifact references across inconsistent documentation. We address these challenges through a formalization that distinguishes direct and indirect dependencies, represents heterogeneous pipeline roles through operation-centered relationships, and resolves artifact identities across names, versions, and repositories. Applying ModSleuth to four public-artifact-rich LLM releases, we recover 1,060 source-verified dependencies and construct large-scale dependency graphs of modern LLM development. These graphs reveal multi-hop license obligations, train-evaluation coupling, discrepancies between released and training-time artifacts, and documentation inconsistencies that would otherwise be difficult to uncover. We release ModSleuth and the resulting dependency graphs to support transparent analysis of the increasingly complex ecosystems underlying modern LLMs.

[3] Learning User Simulators with Turing Rewards
Learning to simulate human users in interactive settings could advance the training of agent assistants, evaluation of personalization systems, research in the social sciences, and more. Existing approaches generally do so by training a large language model (LLM) to match a single ground truth response, either by maximizing the log probability or by using a similarity reward. We instead propose {Turing-RL}: a Turing-Test-based reinforcement learning approach for training user simulator models. {Turing-RL} uses a discriminative Turing reward with an LLM judge to score how indistinguishable a generated response is from the real user's given the user's history, and the user simulator LLM learns to produce responses indistinguishable from what the user could have said with such rewards. Across two different domains--conversational chat and Reddit forum discussion--we find that {Turing-RL} consistently outperforms baseline methods on both LLM and human evaluation metrics. Our study suggests that optimizing for indistinguishability, rather than response matching, is effective for learning user simulators.
```

---

## U100_011 — v2_train_r449_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `449`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

How many social media posts make up the annotated dataset used in StanceNakba 2026, and which transformer-based models did participating teams primarily fine-tune?

### Claim

Participating teams primarily fine-tuned Arabic and multilingual transformer-based models, including MARBERT, AraBERT, and DeBERTa-v3 variants.

### Evidence

```text
[1] StanceNakba Shared Task: Actor and Topic-Aware Stance Detection in Public Discourse
We present StanceNakba 2026, a shared task on stance detection in polarized social media discourse related to the Palestinian-Israeli conflict, organized as part of Nakba-NLP 2026 at LREC-COLING 2026. The task introduces two subtasks: Subtask A (Actor-Level Stance Detection), which classifies English social media posts as Pro-Palestine, Pro-Israel, or Neutral; and Subtask B (Cross-Topic Stance Detection), which identifies Favor, Against, or Neither stances in Arabic posts toward two conflict-related topics, normalization with Israel and refugee presence in Jordan. The task is grounded in an annotated dataset of 2,606 social media posts. A total of 7 teams participated in Subtask A and 6 teams in Subtask B. Participating systems primarily fine-tuned Arabic and multilingual transformer-based models, including MARBERT, AraBERT, and DeBERTa-v3 variants, with several teams employing cross-validation, ensemble methods, and topic-conditioned architectures. The best-performing systems achieved a Macro F1 of 0.9620 on Subtask A and 0.8724 on Subtask B, demonstrating that transformer-based approaches are highly effective for conflict-domain stance detection while highlighting persistent challenges in cross-topic generalization and neutral class prediction.

[2] QIAS 2026: Overview of the Shared Task on Islamic Inheritance Reasoning
This paper presents a comprehensive overview of the QIAS 2026 shared task, organized as part of the OSACT7 Workshop and co-located with LREC 2026. The shared task was designed to evaluate the ability of large language models to perform complex reasoning in the religious and legal domain of Islamic inheritance. Unlike conventional question-answering benchmarks, QIAS 2026 focuses on end-to-end reasoning from natural language cases, requiring systems to perform the full inheritance calculation process, from identifying the eligible heirs to assigning the correct share to each beneficiary. To support this evaluation, the task was based on the MAWARITH benchmark, a dataset of $12{,}500$ Arabic inheritance cases annotated with intermediate reasoning steps and final answers. System submissions were evaluated using MIR-E, a multi-step metric that measures performance across the main stages of inheritance reasoning. A total of $16$ teams participated in the shared task, investigating a range of approaches, including prompting-based methods, retrieval-augmented generation, and fine-tuning strategies. The results show that Islamic inheritance remains a highly challenging benchmark for current language models, especially in stages that require precise legal interpretation and structured numerical reasoning. This overview summarizes the task design, dataset, evaluation framework, participating systems, and main results.

[3] Findings of the MAGMaR 2026 Shared Task
This overview paper presents the results of the shared task for the second workshop on Multimodal Augmented Generation via Multimodal Retrieval (MAGMaR). In this shared task participants submitted systems focused on either (i) video retrieval or (ii) grounded generation of articles given retrieved videos. Teams could submit to either task. For the retrieval task, we had 2 participating teams that submitted a total of 17 systems -- all of which beat a baseline derived from the winner of last year's shared task. On the generation side, we had 4 teams submit 16 systems. All teams had at least one generated report that was labeled the best by a human annotator.
```

---

## U100_012 — v2_train_r168_cited_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `168`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three agents jointly trained on a shared LLM backbone in daVinci-kernel, and what is the specific function of each?

### Claim

The three agents jointly trained on a shared LLM backbone in daVinci-kernel are: 1.

### Evidence

```text
[1] daVinci-kernel: Co-Evolving Skill Selection, Summarization, and Utilization via RL for GPU Kernel Optimization
GPU kernel optimization represents a paradigm where functional correctness is assumed and execution efficiency is the objective. We present daVinci-kernel, a reinforcement learning framework that couples skill discovery with skill exploitation through a dynamically evolving skill library. daVinci-kernel jointly trains three agents sharing one LLM backbone: a Skill Selection Agent that retrieves relevant techniques via BM25 and LLM reranking, a Policy Agent that generates multi-turn CUDA/Triton kernels conditioned on selected skills, and a Skill Summary Agent that distills successful rollouts into reusable skills. Candidate skills are added only after execution-based verification confirms reproducible speedups. All three agents share a single LLM backbone, are initialized via a structured SFT cold start on diversity-filtered data, and are then jointly optimized end-to-end with multi-turn REINFORCE and per-agent advantage estimation. On KernelBench, daVinci-kernel-14B achieves 37.2%, 70.6%, and 32.2% on Level 1, Level 2, and Level 3 under the Fast$_1$ threshold, outperforming the strongest prior RL-trained model, Dr.Kernel-14B.

[2] GateMem: Benchmarking Memory Governance in Multi-Principal Shared-Memory Agents
Memory benchmarks for LLM agents largely assume single-user settings, leaving shared assistants for hospitals, workplaces, campuses, and households understudied. In these deployments, multiple principals write to a common memory pool and query it under different roles, scopes, and relationships, so memory quality requires governance as well as recall. We introduce GateMem, a benchmark for multi-principal shared-memory agents. GateMem jointly evaluates utility for legitimate long-horizon requests with state updates, access control across contextual authorization boundaries, and agent-facing active forgetting after explicit deletion requests. It spans medical, office, education, and household domains, with long-form multi-party episodes, incremental memory injection, hidden checkpoints, structured judging, and leak-target annotations. Across diverse baselines and backbone models, no method simultaneously achieves strong utility, robust access control, and reliable forgetting. Long-context prompting often yields the best governance score at high token cost, while retrieval-based and external-memory methods reduce cost yet still leak unauthorized or deleted information. These results show current memory agents remain far from reliable shared institutional deployment.

[3] State-Grounded Multi-Agent Synthetic Data Generation for Tool-Augmented LLMs
Training tool-augmented LLM agents requires large corpora of multi-turn, tool-grounded conversational data that is expensive to annotate, privacy-constrained in production settings, and largely absent from public datasets. We present StateGen, a synthetic data generation platform that produces scored, reasoning-trace-rich training conversations by orchestrating a four-role LLM loop: a persona-conditioned user simulator, an agent under test, a state-grounded tool simulator, and a multi-axis LLM judge. The key architectural contribution is an authoritative state manager that maintains a structured world-state object across turns, enforcing a backend-is-truth invariant that eliminates the dominant class of tool-call hallucinations by construction. StateGen extends naturally to hierarchical multi-agent settings by declaring sub-agents as tools, all sharing a single state object. We report results on 64,698 evaluated conversations across three production corpora: tool-call hallucination scores reach 9.66/10, the system supports persona-driven variation via a 23-dimensional trait vector, and a cleanly separated train and golden evaluation set split confirms the data is not memorization bait (per-criterion gap analysis). Comparison with eight external systems shows that no single publicly available platform combines multi-turn generation, state-grounded tool simulation, hierarchical multi-agent support, and built-in judge scoring.
```

---

## U100_013 — v2_train_r137_cited_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `137`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the main stages of the PARSE sanitization pipeline, and what percentage of real enterprise documents does the directiveness gate route to the lightweight path?

### Claim

The main stages of the PARSE sanitization pipeline are as follows: 1.

### Evidence

```text
[1] PARSE: Provenance-Aware Retrieval Sanitization for Professional Domain LLM Agents
Prompt injection defenses evaluated on synthetic benchmarks do not generalize to real enterprise documents, which are longer, denser, and interleave legitimate authority language with factual content. We demonstrate this gap with a real-document benchmark of 122 tasks across five professional domains (financial, legal, medical, scientific, DevOps) using actual SEC filings, Federal Register rules, PubMed abstracts, arXiv papers, and GitHub postmortems. Paraphrasing, the strongest defense on synthetic benchmarks, shows no statistically significant attack success rate reduction on real documents (p=0.500) while degrading utility from 91.8% to 82.8%. We introduce PARSE (Provenance-Aware Retrieval Sanitization), a domain-aware, fact-preserving sanitization pipeline that classifies each sentence by injection likelihood, extracts structured facts before rewriting, and verifies fact preservation via a consistency-checking loop. A directiveness gate routes 59% of real enterprise documents to a lightweight path, concentrating computational cost on high-risk documents. PARSE achieves 15.6% attack success rate -- a 38% reduction versus the 25.4% baseline -- at 86.9% utility, the only condition that is both statistically significant (p=0.014, adequately powered) and maintains near-baseline utility. Practitioners should evaluate defenses on domain-matched real documents, not synthetic proxies.

[2] SafeLLM: Extraction as a Hallucination-Resistant Alternative to Rewriting in Safety-Critical Settings
Large language models (LLMs) are increasingly used to access organisational documentation, including standard operating procedures (SOPs), HR policies and institutional guidelines. However, retrieval-augmented generation (RAG) systems that rely on free-form rewriting can introduce hallucinations and unstable trade-offs between completeness and conciseness, particularly in safety- and compliance-critical settings. Objectives: To evaluate extraction as a hallucination-resistant alternative to rewriting-based RAG and compare strategies that balance precision, recall and safety across document types and model scales. Methods: We compare multiple prompting strategies, including line-number-based source selection, extraction of relevant guideline sentences with explicit safety annotations, and a multi-stage pipeline that refines draft answers using supporting evidence from source guidelines. Experiments are conducted on documents of varying length and structure, including local NHS acute care and oncology guidelines and UK-wide NICE guidelines, using both frontier-scale and locally deployable models. Performance is assessed using automatic metrics and human expert evaluation of relevance and completeness. Results: Line-number selection achieves the strongest results, outperforming direct copying and safety-focused strategies across both large and small models while maintaining high term recall (up to 95%) and close alignment with source text. Safety-oriented approaches improve precision but introduce systematic omissions, while multi-stage filtering further amplifies this trade-off. Performance varies with document structure: line-based extraction excels in protocol-like content, whereas alternative strategies perform better on more verbose documents (up to 97% term recall).

[3] PersonaDrive: Human-Style Retrieval-Augmented VLA Agents for Closed-Loop Driving Simulation
Closed-loop driving simulators typically populate their environments with non-ego traffic agents that behave largely the same way, produced either by rule-based traffic managers or by learned models trained toward a single behavioral mode. Recent work introduces style variation through post-hoc labels on observational data or LLM-inferred reward weights, but these signals act as proxies for what a style should reward rather than demonstrations of humans explicitly asked to drive in that style. We introduce PersonaDrive, a pipeline that conditions a vision-language-action (VLA) driving agent on retrieved demonstrations from a style-instructed human driving dataset, in which participants drive CARLA leaderboard routes under aggressive, neutral, and conservative instructions on a driver-in-the-loop rig. The pipeline has three stages: (i) offline triplet mining over per-style human driving data using a combined image-text similarity score; (ii) training a lightweight retrieval head that fuses frozen visual features with a small control encoder over per-style databases; and (iii) fine-tuning a single VLA backbone to treat retrieved context points as in-context behavioral demonstrations during waypoint prediction. At inference, the same backbone is conditioned on any style by swapping which per-style database the retrieval head queries, so selecting a style requires no per-style retraining while enabling human-style, style-diverse non-ego agents for closed-loop simulation. On Bench2Drive, PersonaDrive (no style) improves the driving score by 4.6% over SimLingo and 2.5% over HiP-AD, and under style conditioning attains the highest driving score in every style within a roughly 2% band (its weakest style surpassing the strongest baseline, DMW, by 5.4%), while average speed and acceleration rise by 18% and 25% from the conservative to the aggressive instruction.
```

---

## U100_014 — v2_train_r394_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `394`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three key modules of the NTS-CoT framework and what function does each serve?

### Claim

Element-CoT: This module captures essential news elements for faithful summarization. 2.

### Evidence

```text
[1] NTS-CoT: Mitigating Hallucinations in LLM-based News Timeline Summarization with Chain-of-Thought Reasoning
The rapid updates of online news make tracking event developments challenging, highlighting the need for timeline summarization (TLS). Hallucinations, where LLM-generated content deviates from source news, still remain a critical issue in LLM-based TLS and are not well studied in existing works. To bridge this gap, we identify two primary types of hallucinations: unfaithful content during news summarization and information omission in date-event summarization. Then, we propose NTS-CoT, a novel framework that leverages Chain-of-Thought (CoT) reasoning to mitigate hallucinations in TLS. The framework consists of three key modules: i) Element-CoT to capture essential news elements for faithful summarization, ii) Date Selection to combine temporal saliency and event prominence for timestamp selection, and iii) Causal-CoT to infer causal relationships and reduce omissions in date-event summarization. Extensive experiments, including quantitative analysis on three TLS benchmarks and human evaluation, demonstrate that NTS-CoT outperforms state-of-the-art baselines, effectively mitigating hallucinations and improving LLM-based TLS performance. Our source code is available at https://anonymous.4open.science/r/NTS-CoT .

[2] CoRA: Confidence-Rationale Alignment for Reliable Chain-of-Thought Reasoning
Chain-of-thought (CoT) reasoning can improve LLM performance, but high answer confidence may be misleading when the accompanying CoT rationale is plausible yet incomplete or poorly supported. We study confidence--rationale alignment: whether a model's confidence in its committed answer is justified by its generated rationale. We introduce a GRPO-based reinforcement learning framework that jointly rewards answer correctness, committed-answer probability, and rubric-based rationale support, where the rubric assesses grounding, coherence, task match, and connection to the selected answer without revealing the gold answer to the judge. Across MedQA, MathQA, and OpenBookQA using three open-weight LLMs, our method reduces the confidence--rationale alignment error by up to 26.51% compared with untuned checkpoints, SFT, and correctness-only GRPO, while maintaining competitive accuracy and often improving calibration. These results show that reliable CoT reasoning requires not only confident answers, but rationales that substantively support them.

[3] GRACE: Step-Level Benchmark for Faithful Reasoning over Context
Many reasoning tasks require models to reason over input context, from document-grounded question answering to rule-based deduction. Chain-of-Thought (CoT) prompting produces traces that appear transparent, yet individual steps can silently deviate from the source evidence, even when the final answer is correct. Existing methods detect hallucinations at the response level but fail to identify where in the chain a failure occurs or what type it is. We introduce GRACE, the first human-annotated step-level faithfulness benchmark with a data-driven error taxonomy for context-grounded textual reasoning. GRACE covers CoT traces from 10 models across 4 source datasets, with each step annotated for faithfulness, error category, and natural language explanation. A data-driven taxonomy, discovered bottom-up via unsupervised clustering, organizes failures into two tracks: GRACE-Inference (deductive errors) and GRACE-Grounding (factual grounding errors), with four categories each. The evaluation set is human-annotated and challenging by design. Our experiments reveal substantial headroom for current models. In addition, integrating step-level faithfulness signals into reinforcement learning pipelines improves both downstream accuracy and reasoning reliability.
```

---

## U100_015 — v2_train_r340_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `340`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What nDCG@10 improvements does ADORE report over BM25 and the strongest prior query expansion method on the BEIR benchmark?

### Claim

ADORE reports an improvement of 24.5% over BM25 and 3.6% over the strongest prior query expansion method on the BEIR benchmark for average nDCG@10.

### Evidence

```text
[1] ADORE: Iterative Query Expansion with Retrieval-Grounded Relevance Feedback
LLM-based query expansion improves retrieval by enriching the original query with additional context. Yet most methods remain generation-driven, producing plausible pseudo-documents or expansions without checking how the target corpus responds. This can introduce retrieval drift, amplify misleading vocabulary, or miss terms that distinguish relevant from non-relevant documents. We argue that effective expansion requires retrieval-grounded feedback, not just single-pass generation or unverified iteration. We introduce ADORE (ADapt, Observe, Relevance Evaluate), an iterative framework that turns retrieval outcomes into feedback for the next expansion. At each round, an LLM generates pseudo-passages, a retriever exposes the corpus response, and a relevance assessor evaluates retrieved documents against the original query. These judgments identify what to reinforce, what remains undercovered, and what to suppress. Across TREC Deep Learning, BEIR, and BRIGHT, ADORE consistently outperforms strong query expansion baselines with notable improvements across nearly all evaluation settings, improving average nDCG@10 by 24.5% over BM25 and 3.6% over the strongest prior query expansion method on BEIR, and by 122.9% over BM25 and 9.2% over the best query expansion baseline on BRIGHT. Our code and data are publicly available.

[2] Dr-DCI: Scaling Direct Corpus Interaction via Dynamic Workspace Expansion
Agentic search over large corpora relies on retriever-mediated interfaces (e.g., BM25 or ColBERT) for scalable candidate discovery. While effective at ranking relevant documents, these interfaces expose evidence only as ranked results or bounded document views, limiting agents' ability to reorganize material and verify constraints across documents. Direct Corpus Interaction (DCI) addresses this limitation by exposing shell-executable corpus operations for flexible search, filtering, comparison, and verification. However, full-corpus terminal commands become slow and unstable as the corpus grows, degrading performance and efficiency. We introduce DR-DCI, a retriever-steered DCI framework that treats retrieval as an agent-callable action for expanding a local workspace. Rather than operating directly over the full corpus, the agent dynamically pulls relevant documents into an evolving workspace and conducts DCI operations within it. This design combines retriever-level recall with DCI-style precision: retrieval keeps exploration scalable, while DCI preserves the local operations needed for effective evidence resolution. Experiments show that DR-DCI is both effective and efficient across scales. On Browsecomp-Plus, DR-DCI reaches 71.2\% accuracy, improving over raw DCI and ablated variants by up to 8.3 points while reducing tool usage, wall time, and estimated cost. With workspace-preserving context reset, accuracy further improves to 73.3\%. In corpus-scaling experiments, DR-DCI remains effective from 100K to 10M documents, whereas raw DCI becomes unstable and BM25 performs substantially worse. DR-DCI also scales to a 20M-scale file-per-document Wiki-18 QA setting, achieving an average score of 63.0 across six benchmarks and outperforming retrieval-based and trained search-agent baselines. Ablation analysis further shows that ranked previews and inter-document DCI are key to performance.

[3] Hybrid Neural Retrieval with Generative Query Refinement for Quranic Passage Retrieval
Quranic Passage Retrieval (PR) could be a challenging task due to the linguistic complexity and the semantic gap between the Modern Standard Arabic (MSA) used in daily queries and the Classical Arabic (CA) of the Holy Quran. These factors hinder conventional retrieval methods. To handle these limitations and improve multi-verse retrieval and filter the zero-answer queries, this paper proposes a four-phase neural architecture designed to enhance retrieval accuracy and contextual understanding. The methodology combines hybrid candidate retrieval using AraColBERT dense indexing and BM25 sparse retrieval, followed by semantic reranking with a CAMeLBERTmix cross-encoder. A confidence gating mechanism is then applied to filter zero-answer queries, and an AraT5-based refinement module for multi-verse aggregation. The system is evaluated on an expanded version of the Quran QA 2022 dataset. Results show improved performance compared to the baseline models, achieving a Recall@10 of 0.7024 and a Mean Average Precision (MAP@10) of 0.4947. While the system exhibits a marginal tradeoff in absolute top-rank precision (MRR = 0.5807) compared to heavily optimised single models, the proposed architecture provides a substantially more comprehensive, reliable, and context aware solution for multi-verse Quranic passage retrieval.
```

---

## U100_016 — v2_train_r56_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `56`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What average performance gains are reported for the Qwen3-4B, 8B, and 30B-A3B models across the seven long-context benchmarks?

### Claim

However, they report average gains of +7.2, +3.2, and +6.4 points for these models, respectively, across the seven long-context benchmarks.

### Evidence

```text
[1] Beyond Reward Engineering: A Data Recipe for Long-Context Reinforcement Learning
Long-context reasoning is an essential capability for large language models, particularly when they are deployed as autonomous agents that must reason over lengthy trajectories. Reinforcement learning (RL) has recently emerged as a dominant paradigm for improving this ability, yet existing work largely focuses on reward engineering while diverse training data remains scarce. We revisit this problem from a data-centric perspective and show that a simple yet effective data recipe alone, paired with a minimal outcome-based GRPO setup, suffices to substantially improve long-context reasoning. Our recipe targets three complementary task families -- retrieval, multi-evidence synthesis, and reasoning -- for which we construct and curate eight datasets totaling ~14K examples. Experiments on three models (Qwen3-4B/8B/30B-A3B) yield average gains of +7.2/+3.2/+6.4 points across seven long-context benchmarks, surpassing prior RL training sets. We further demonstrate that these gains transfer to agentic tasks, where continuing RL training on an agent-tuned model with our data recipe improves GAIA by +4.8 and BrowseComp by +7.0 points. We will release our datasets to facilitate future research.

[2] Weaving Multi-Source Evidence for Biomedical Reasoning: The BioMedHop Benchmark and BioWeave Framework
Biomedical question answering (QA) increasingly requires reasoning over interacting entities, where supporting evidence is scattered across biomedical knowledge graphs, literature documents, and web-accessible resources. However, existing biomedical QA benchmarks mainly focus on exam-style knowledge, literature comprehension, or short-range multi-hop inference, leaving source-conditioned graph reasoning and evidence topology construction underexplored. To fill this gap, we introduce BioMedHop, a multi-source graph-grounded benchmark for evaluating biomedical reasoning over structured evidence topologies. BioMedHop contains 10,045 instances across KG, document, web, and hybrid evidence settings, covering shared-neighbor matching, intersection reasoning, path-based reasoning, and counting, with option-based, open-ended, and numeric count renderings. To support this benchmark, we further propose BioWeave, a source-aware reasoning framework that retrieves biomedical KG paths, gathers supporting clues from documents and web sources, assembles them into a unified evidence graph, and verifies answers through entity-level evidence support. Comprehensive experiments show that BioWeave achieves the best overall performance among compared methods on BioMedHop, outperforming the strong hybrid baseline ToG-2 by 10.5% in the overall average. Moreover, BioWeave consistently improves different LLM backbones and enables smaller models, such as Qwen3-4B, to achieve reasoning performance comparable to GPT-4-Turbo.

[3] MLLP-VRAIN UPV system for the IWSLT 2026 Simultaneous Speech Translation task
This work describes the participation of the MLLP-VRAIN research group in the shared task of the IWSLT 2026 Simultaneous Speech Translation track. Our submission utilizes the recently released Parakeet and Qwen 3.5 models to create a robust, cascaded solution for long-form SimulST through the use of adaptive "black-box" policies. We explore relaxations of these policies to achieve better quality-latency trade-offs. Compared to last year, we participate on all language directions. In addition to this, for the En$\rightarrow${De, It, Zh} directions we also participate in this year's new context track employing a combination of ASR word-boosting and a RAG mechanism of offline pre-translated exemplars to guide generation and enrich our system with domain-specific context. Finally, we provide a detailed latency analysis of our system. Compared to last year, results on the MCIF En$\rightarrow$De test set shows a substantial quality improvement of +5.82 XCOMET-XL. Our context track processing further improves performance by +1.03.
```

---

## U100_017 — v2_train_r246_plain_c004

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `246`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What is the structure of the fine-grained risk taxonomy proposed for Chinese scenarios in terms of macro and micro categories?

### Claim

Harmful Content Micro Categories: 31 (No specific details are provided in the source about the 31 micro categories.

### Evidence

```text
[1] CHILLGuard: Towards Fine-Grained Chinese LLM Safety Guardrail with Scalable Data Construction and Model-aware Preference Alignment
Malicious content generated from large language models (LLMs) could pose severe safety risks and ethical concerns. While existing LLM safety guardrails excel in English or multilingual settings, they lack adaptation to Chinese-specific regulatory policies, cultural context and linguistic nuances, failing to support fine-grained risk classification for diverse deployment needs. In this paper, we introduce a 5-macro, 31-micro category fine-grained risk taxonomy for Chinese scenarios, and build CHILLGuard: a dedicated Chinese LLM content safety guardrail. To address the critical scarcity of high-quality annotated Chinese safety data, we propose a scalable multi-stage data construction pipeline: we expand multi-source corpus via retrieval-augmented generation, generate implicit harmful samples through prompt engineering rewriting, and refine high-quality data via multi-model voting-based label calibration. Based on this, we build CHILLGuardTrain, a large-scale training set with 405,007 samples, and CHILLGuardTest, a rigorously curated annotated test set with 51,745 samples. We then train CHILLGuard on CHILLGuardTrain under a generator-classifier collaborative framework via Model-aware Direct Preference Optimization. Extensive experiments under multiple settings demonstrate the state-of-the-art performance of CHILLGuard, e.g., a 15.92% improvement of F1 score over Qwen3Guard-8B-Strict on our benchmark. We will release our resources at https://github.com/cswbyu/CHILLGuard.

[2] LegalWorld: A Life-Cycle Interactive Environment for Legal Agents
Civil litigation is inherently a life-cycle process: what a lawyer drafts on day one constrains what unfolds at trial months later. Yet existing legal benchmarks evaluate isolated subtasks, and prior legal-agent simulators reinitialize each scenario from shared ground truth, leaving cross-stage causal dependencies unmodeled. We present LegalWorld, a life-cycle interactive environment that models Chinese civil litigation as a causally connected state chain of five stages (seven sub-scenarios), grounded in 75,309 paired Chinese civil judgments. We pair it with reusable infrastructure (local memory, global case memory, a Skill/Tool library) that keeps each dispute consistent across its full life cycle. Building on this environment, we construct LongJud-Bench to evaluate agent capability across all five connected stages. 18,992 ratings from 217 legal-background evaluators confirm that LegalWorld trajectories are procedurally faithful and role-consistent; and a capability-level cross-model evaluation reveals sharp divergences that aggregate scores cannot expose, with no single backbone leading across consultation, drafting, and courtroom advocacy. Detailed resources will be released publicly.

[3] TimeLens: On-Device Artifact Recognition with Retrieval-Augmented Question Answering for the Grand Egyptian Museum
TimeLens is an AI-powered bilingual mobile guide for the Grand Egyptian Museum (GEM). Pointing a phone at an exhibit, a visitor sees the artifact recognized in real time and can ask follow-up questions answered in English or Arabic. The work addresses three problems specific to in-gallery deployment: fine-grained visual similarity among 51 catalogued artifacts (many near-identical Ramesside statues), the gap between curated training data and handheld camera conditions, and the risk of an AI guide stating unsupported historical facts. Two engineering contributions are reported. First, an on-device artifact detector was developed through a data-quality-driven iteration study -- from foundation-model auto-annotation (YOLO-World), through spatial label-cleaning rules, to a fully hand-annotated dataset -- isolating label quality as the decisive factor: the final YOLOv8n model resolves every previously failing class while remaining a 5.97 MB TensorFlow Lite asset that runs in real time on a mid-range phone (mAP@0.5 = 0.995, mAP@0.5:0.95 = 0.924). Second, a bilingual Retrieval-Augmented Generation (RAG) guide, grounded in a 108-record ChromaDB knowledge base, was benchmarked across seven candidate language models, with Gemma 4 E2B (Q4 K M) selected; ten targeted optimizations reduce end-to-end latency from over 30 s to approximately 10 s. Both subsystems are integrated in a production Flutter application with bilingual interface, museum location gating, and text-to-speech support.
```

---

## U100_018 — v2_train_r425_plain_c004

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `425`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three training innovations combined in the MARD pipeline?

### Claim

A leakage-safe mechanism-aware retrieval channel.

### Evidence

```text
[1] MARD: Mirror-Augmented Reasoning Distillation for Mechanism-Level Drug-Drug Interaction Prediction
Mechanism-level drug-drug interaction (DDI) prediction requires identifying which enzyme or pharmacodynamic axis is implicated, in which direction, and with which evidence -- not merely whether two drugs interact. We introduce a reproducible mechanism-level DDI labelling and evaluation protocol with a structured 7-family/147-subtype taxonomy, leakage-safe cold-split protocols, and auditable reasoning metrics for evaluating pharmacological prediction beyond flat interaction classification. We propose a pipeline that produces a 7B reasoning MARD (Mirror-Augmented Reasoning Distillation), combining three training innovations: a single-token KL divergence on direction tag that ties the model's prediction, per-loss PRM-weighted DPO with programmatic hard negatives, and a leakage-safe mechanism-aware retrieval channel. Process-reward step labels are automatically verifiable against DrugBank-structured fields, requiring no human or LLM judges. On the April-2026 DrugBank release, our MARD-7B is the only system in a 32-system comparison whose accuracy survives drug-pair novelty, beating the best baseline by +13.9 pp and GPT-4o by +6.7 pp at ~1% of frontier API cost. Further analysis reveals an anti-memorisation signature where accuracy improves on rarely seen drugs, suggesting that gain comes from structured pharmacological reasoning rather than drug-frequency memorisation. We release corpus, DDI-PRM, retrieval index, and training code.

[2] Which Models Are Our Models Built On? Auditing Invisible Dependencies in Modern LLMs
Modern LLM training pipelines increasingly rely on other models to generate data, filter corpora, judge outputs, and guide development decisions. These dependencies are recursive: a model may depend on an upstream artifact whose own dependencies are documented only in separate releases and artifacts. As a result, the full dependency structure is fragmented across heterogeneous public artifacts, with complexity and recursive depth far outpacing humans' ability to trace. We introduce ModSleuth, an agentic system that recursively reconstructs LLM dependency graphs from public artifacts with source-grounded evidence. We find that the primary challenge is no longer information extraction, but defining what constitutes a dependency and reconciling artifact references across inconsistent documentation. We address these challenges through a formalization that distinguishes direct and indirect dependencies, represents heterogeneous pipeline roles through operation-centered relationships, and resolves artifact identities across names, versions, and repositories. Applying ModSleuth to four public-artifact-rich LLM releases, we recover 1,060 source-verified dependencies and construct large-scale dependency graphs of modern LLM development. These graphs reveal multi-hop license obligations, train-evaluation coupling, discrepancies between released and training-time artifacts, and documentation inconsistencies that would otherwise be difficult to uncover. We release ModSleuth and the resulting dependency graphs to support transparent analysis of the increasingly complex ecosystems underlying modern LLMs.

[3] PersonaDrive: Human-Style Retrieval-Augmented VLA Agents for Closed-Loop Driving Simulation
Closed-loop driving simulators typically populate their environments with non-ego traffic agents that behave largely the same way, produced either by rule-based traffic managers or by learned models trained toward a single behavioral mode. Recent work introduces style variation through post-hoc labels on observational data or LLM-inferred reward weights, but these signals act as proxies for what a style should reward rather than demonstrations of humans explicitly asked to drive in that style. We introduce PersonaDrive, a pipeline that conditions a vision-language-action (VLA) driving agent on retrieved demonstrations from a style-instructed human driving dataset, in which participants drive CARLA leaderboard routes under aggressive, neutral, and conservative instructions on a driver-in-the-loop rig. The pipeline has three stages: (i) offline triplet mining over per-style human driving data using a combined image-text similarity score; (ii) training a lightweight retrieval head that fuses frozen visual features with a small control encoder over per-style databases; and (iii) fine-tuning a single VLA backbone to treat retrieved context points as in-context behavioral demonstrations during waypoint prediction. At inference, the same backbone is conditioned on any style by swapping which per-style database the retrieval head queries, so selecting a style requires no per-style retraining while enabling human-style, style-diverse non-ego agents for closed-loop simulation. On Bench2Drive, PersonaDrive (no style) improves the driving score by 4.6% over SimLingo and 2.5% over HiP-AD, and under style conditioning attains the highest driving score in every style within a roughly 2% band (its weakest style surpassing the strongest baseline, DMW, by 5.4%), while average speed and acceleration rise by 18% and 25% from the conservative to the aggressive instruction.
```

---

## U100_019 — v2_train_r267_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `267`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What two attention mechanisms are integrated in the hybrid linear attention design used in Ling-2.6 and Ring-2.6, and what efficiency goal does this integration serve?

### Claim

This integration serves the efficiency goal of improving the efficiency of long-context training and decoding.

### Evidence

```text
[1] Ling and Ring 2.6 Technical Report: Efficient and Instant Agentic Intelligence at Trillion-Parameter Scale
Efficient and scalable agentic intelligence requires models that can deliver both low-latency responses and strong reasoning capabilities while remaining practical to train, serve, and deploy. In this report, we present Ling-2.6 and Ring-2.6, a family of models designed to address this challenge at scale. Ling-2.6 is optimized for instant response generation and high capability per output token, whereas Ring-2.6 is tailored for deeper reasoning and more advanced agentic workflows. Instead of training from scratch, we upgrade the Ling-2.0 base model through architectural migration pre-training and large-scale post-training. This upgrade is guided by a unified co-design of model architecture, optimization objectives, serving systems, and agent training environments, enabling improvements in both model capability and deployment efficiency. At the architectural level, we introduce a hybrid linear attention design that integrates Lightning Attention with MLA, improving the efficiency of long-context training and decoding. To further enhance token efficiency, we optimize capability per output token through Evolutionary Chain-of-Thought, Linguistic Unit Policy Optimization, bidirectional preference alignment, and shortest-correct-response distillation. For agentic capabilities, we propose KPop, a reinforcement learning framework designed to support stable training of Ring-2.6-1T on large-scale environment-grounded data. KPop improves training efficiency through asynchronous scheduling across coding, search, tool use, and workflow execution, enabling scalable learning from complex agent-environment interactions. Together, Ling-2.6 and Ring-2.6 provide a practical pathway toward efficient, scalable, and open agentic systems. We open-source all checkpoints in the 2.6 family to support further research and development in practical agentic intelligence.
```

---

## U100_020 — v2_train_r77_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `77`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What did the mechanistic analyses on open-weight LLMs reveal about where and when the suppression of evidence-supported answers emerges?

### Claim

This suppression is observed to occur after the instruction training.

### Evidence

```text
[1] The Wrong Kind of Right: Quantifying and Localizing Misfired Alignment in LLMs
Warning: This paper studies stereotypes and biases, and contains potentially disturbing examples, used for illustration purposes only. Our findings should not be interpreted as an argument against alignment. Instead, this paper highlights the need for principled approaches to more advanced alignment. Alignment aims to ensure that large language models (LLMs) behave safely and reliably, including by avoiding unsafe inferences. However, we show that such safety-oriented behaviors can misfire: models may reject warranted conclusions even when they are explicitly supported by context. We call this failure mode misfired alignment, where alignment-induced changes cause LLMs to override explicit evidence. To quantify this phenomenon, specifically on stereotype-related alignment, we introduce VETO, a benchmark consisting of 2,032 BBQ-derived contrastive pairs, and define a new metric, Misfired Alignment Rate (MAR), which measures on a 0 to 100 scale how often a model fails on a stereotype-related question but succeeds on its contrastive counterpart. We benchmark 25 LLMs on VETO, and show that all LLMs, including the most recent ones, exhibit non-trivial (4.7 to 18.9%) MARs while all human participants achieve 0.0% MAR. Controlled priming experiments further show that alignment-induced cues can substantially amplify MAR across LLMs, indicating that these failures are not merely artifacts of individual examples but can be induced by safety-related framing. Mechanistic analyses on open-weight LLMs reveal late-layer suppression of evidence-supported answers, and comparisons between instruct and base LLMs suggest that this suppression emerges after instruction training. These findings show that current alignment methods can overgeneralize surface-level safety cues, to the point of overriding objective evidence, motivating more work on alignment objectives that better preserve contextual grounding.

[2] CoRA: Confidence-Rationale Alignment for Reliable Chain-of-Thought Reasoning
Chain-of-thought (CoT) reasoning can improve LLM performance, but high answer confidence may be misleading when the accompanying CoT rationale is plausible yet incomplete or poorly supported. We study confidence--rationale alignment: whether a model's confidence in its committed answer is justified by its generated rationale. We introduce a GRPO-based reinforcement learning framework that jointly rewards answer correctness, committed-answer probability, and rubric-based rationale support, where the rubric assesses grounding, coherence, task match, and connection to the selected answer without revealing the gold answer to the judge. Across MedQA, MathQA, and OpenBookQA using three open-weight LLMs, our method reduces the confidence--rationale alignment error by up to 26.51% compared with untuned checkpoints, SFT, and correctness-only GRPO, while maintaining competitive accuracy and often improving calibration. These results show that reliable CoT reasoning requires not only confident answers, but rationales that substantively support them.

[3] EHRNote-ChatQA: A Benchmark for Evidence-Grounded Multi-Turn Clinical Question Answering over Longitudinal Discharge Summaries
Discharge summaries are crucial clinical documents containing the context of a patient's overall hospital stay, and are routinely reviewed by medical experts for patient readmission, ongoing care, and diagnostic decision-making. When reviewing them, medical experts often must iteratively synthesize information across multiple summaries while verifying the evidence supporting each answer. Although large language models (LLMs) are increasingly explored for clinical question answering, existing benchmarks do not sufficiently reflect this setting: they often evaluate exam-style medical knowledge or focus on single-turn question answering with limited evidence-grounding evaluation. We introduce EHRNote-ChatQA, the first benchmark for evidence-grounded multi-turn clinical question answering over patients' multiple discharge summaries. Built from de-identified MIMIC-IV discharge summaries, EHRNote-ChatQA contains 967 patient-level multi-turn samples spanning one to five notes and 16,072 medical-expert-verified QA pairs (8,036 content questions, each paired with an evidence-grounding question) across eight clinical categories. The benchmark is constructed through an expert-informed pipeline combining discharge-summary structuring schema, expert-curated multi-turn QA templates, and LLM-based generation, followed by review and revision of every single QA sample by 11 medical experts. Benchmarking 22 open- and closed-source LLMs reveals several challenges, including that LLMs struggle more with evidence grounding than content answering, multi-turn errors compound across turns, and single-turn clinical QA performance does not reliably transfer to this setting. These findings establish EHRNote-ChatQA as a rigorous and practical benchmark for evaluating clinical QA systems. The dataset will be made publicly available through PhysioNet credentialed access.
```

---

## U100_021 — v2_train_r425_cited_c003

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `425`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What are the three training innovations combined in the MARD pipeline?

### Claim

Per-loss PRM-weighted DPO with programmatic hard negatives. 3.

### Evidence

```text
[1] MARD: Mirror-Augmented Reasoning Distillation for Mechanism-Level Drug-Drug Interaction Prediction
Mechanism-level drug-drug interaction (DDI) prediction requires identifying which enzyme or pharmacodynamic axis is implicated, in which direction, and with which evidence -- not merely whether two drugs interact. We introduce a reproducible mechanism-level DDI labelling and evaluation protocol with a structured 7-family/147-subtype taxonomy, leakage-safe cold-split protocols, and auditable reasoning metrics for evaluating pharmacological prediction beyond flat interaction classification. We propose a pipeline that produces a 7B reasoning MARD (Mirror-Augmented Reasoning Distillation), combining three training innovations: a single-token KL divergence on direction tag that ties the model's prediction, per-loss PRM-weighted DPO with programmatic hard negatives, and a leakage-safe mechanism-aware retrieval channel. Process-reward step labels are automatically verifiable against DrugBank-structured fields, requiring no human or LLM judges. On the April-2026 DrugBank release, our MARD-7B is the only system in a 32-system comparison whose accuracy survives drug-pair novelty, beating the best baseline by +13.9 pp and GPT-4o by +6.7 pp at ~1% of frontier API cost. Further analysis reveals an anti-memorisation signature where accuracy improves on rarely seen drugs, suggesting that gain comes from structured pharmacological reasoning rather than drug-frequency memorisation. We release corpus, DDI-PRM, retrieval index, and training code.
```

---

## U100_022 — v2_train_r299_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `299`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What type of models does the paper use to demonstrate that Persuasion Index features carry predictive signal while remaining computationally lightweight?

### Claim

However, the first source mentions the use of linear models, and the second source discusses sparse autoencoders (SAEs) and language models (LMs).

### Evidence

```text
[1] Persuasion Index: A Theory-Guided Framework for Persuasion Analysis
Identifying persuasive rhetorical cues is critical across domains, from detecting information manipulation and improving AI safety to advancing public health communication. We propose Persuasion Index (PI), a taxonomy of 15 dimensions grounded in persuasion theories from psychology and communication, and one transparent implementation using 55 sub-features built from lexicons and rule-based detectors. The taxonomy is modular: individual detectors can be replaced while preserving the theoretical structure. By evaluating PI on four public datasets varying in domain, style, and outcome measures, we show that PI provides a shared feature space for interpreting rhetorical patterns associated with persuasion-related outcomes. Linear models show that PI features carry meaningful predictive signal while remaining computationally lightweight. Dimension-level analyses reveal recurring associations between PI dimensions and persuasion outcomes across datasets, while also highlighting topic- and stance-specific variation. We release PI as an open-source package and web interface for principled and auditable analysis of human and AI-mediated communication.

[2] From Sparse Features to Trustworthy Proxies: Certifying SAE-Based Interpretability
Sparse autoencoders (SAEs) are increasingly used to extract interpretable features from language models (LMs), yet a central question remains: when can an SAE-based explanation be treated as a faithful view of an underlying frozen LM We study this through a post-hoc generalization framework that certifies the LM via a sparse proxy, obtained by replacing a native hidden activation with its pretrained SAE reconstruction. Our framework derives an upper bound on the base model's expected risk using four measurable quantities: proxy risk, SAE reconstruction gap, concept-pool mismatch, and sparse complexity. We interpret this certificate as an operational criterion for explanatory faithfulness. In particular, a non-vacuous bound indicates that the extracted sparse features retain meaningful predictive information, while small reconstruction and mismatch errors indicate that the proxy remains behaviorally close to the original model. Empirically, we show that the bound becomes non-vacuous on GPT-2 Small, Gemma-2B, and Llama-3-8B at practical sample sizes. A detailed layerwise analysis of Llama-3-8B reveals a strong depth dependence, with later layers becoming much easier to certify, associated with both stronger local fidelity and weaker downstream error amplification. Finally, through feature-shuffling ablations, we show that the decomposition distinguishes genuine semantic alignment from mere statistical sparsity, providing a useful diagnostic for when SAE-based explanations become less reliable.

[3] The Wrong Kind of Right: Quantifying and Localizing Misfired Alignment in LLMs
Warning: This paper studies stereotypes and biases, and contains potentially disturbing examples, used for illustration purposes only. Our findings should not be interpreted as an argument against alignment. Instead, this paper highlights the need for principled approaches to more advanced alignment. Alignment aims to ensure that large language models (LLMs) behave safely and reliably, including by avoiding unsafe inferences. However, we show that such safety-oriented behaviors can misfire: models may reject warranted conclusions even when they are explicitly supported by context. We call this failure mode misfired alignment, where alignment-induced changes cause LLMs to override explicit evidence. To quantify this phenomenon, specifically on stereotype-related alignment, we introduce VETO, a benchmark consisting of 2,032 BBQ-derived contrastive pairs, and define a new metric, Misfired Alignment Rate (MAR), which measures on a 0 to 100 scale how often a model fails on a stereotype-related question but succeeds on its contrastive counterpart. We benchmark 25 LLMs on VETO, and show that all LLMs, including the most recent ones, exhibit non-trivial (4.7 to 18.9%) MARs while all human participants achieve 0.0% MAR. Controlled priming experiments further show that alignment-induced cues can substantially amplify MAR across LLMs, indicating that these failures are not merely artifacts of individual examples but can be induced by safety-related framing. Mechanistic analyses on open-weight LLMs reveal late-layer suppression of evidence-supported answers, and comparisons between instruct and base LLMs suggest that this suppression emerges after instruction training. These findings show that current alignment methods can overgeneralize surface-level safety cues, to the point of overriding objective evidence, motivating more work on alignment objectives that better preserve contextual grounding.
```

---

## U100_023 — v2_train_r106_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `106`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

How was the training dataset expanded from the 3,111 ground-truth labels to a combined dataset of 6,283 users?

### Claim

The training dataset was expanded from the 3,111 ground-truth labels to a combined dataset of 6,283 users by augmenting them with pseudolabels generated by a reasoning model (Claude Opus) and iteratively training intermediate models.

### Evidence

```text
[1] Fine-tuning LLMs for Passive Depression Severity Estimation from AI Mental Health Dialogue
Depression is the leading cause of disability worldwide, and early detection of symptom change is essential for timely intervention. Validated instruments such as the Patient Health Questionnaire-9 (PHQ-9) support symptom monitoring at scale, but real-world completion rates are low, introducing response bias and systematic missingness. Passive approaches that infer severity from routinely generated data could close this gap. We address this by predicting PHQ-9 total scores directly from transcripts of conversations between users and an AI mental health application, requiring only conversation text and no additional clinical data. We fine-tune a Qwen3.5-27B backbone with a regression head, augment 3,111 ground-truth labels with pseudolabels generated by a reasoning model (Claude Opus) and iteratively trained intermediate models, for a combined dataset of 6,283 users. On a held-out test set of 842 users, our best model achieves MAE = 2.6, RMSE = 4.0, Pearson r = 0.80, and AUC = 0.91 at the PHQ-9 >= 10 clinical threshold. We also find AUC > 0.87 at every severity threshold from PHQ-9 >= 3 to PHQ-9 >= 24, demonstrating that the model captures depression severity across the full clinical spectrum. This work opens the door to passive, continuous symptom monitoring in AI mental health platforms, without requiring users to complete self-report measures.

[2] NAMESAKES: Probing Identity Memorization in Text-to-Image Models
Text-to-image (T2I) models generate realistic likenesses of some individuals when prompted with their names, raising privacy concerns. However, distinguishing whether a generated face is memorized or fabricated currently requires ground-truth photos, access to training data, or white-box access to model internals, limiting applicability. We introduce a fully black-box behavioral probe that distinguishes between these regimes while requiring no reference photos or prior knowledge of training data. To benchmark this task, we present the NAMESAKES dataset of over one thousand names and faces of public figures spanning a wide range of fame levels, along with perturbed, less famous names. Experiments on state-of-the-art T2I models show that our probe substantially predicts identity memorization and separates memorized from unrecognized names, with further insights into differences across model families.

[3] Before the Labels: How Dataset Construction Shapes Suicidality Detection in Clinical Text
Clinical NLP increasingly relies on electronic health record (EHR) data to detect suicidal behaviors, treating clinical documentation as more reliable ground truth than social media. We argue that this framing obscures how EHR-based suicidality datasets encode a particular operationalization of suicidality, shaped by who authors the data, how episodes are bounded, and how ambiguity is resolved. We ground this argument in a case study of the ScAN dataset, built over MIMIC-III clinical notes. We show how governance constraints, ICD-based cohort selection, single-annotator labeling, and hospital-stay-level aggregation produce labels that reflect clinician-documented judgments, treat suicidality as a bounded episode, and assume that intent can be reliably inferred from documentation. A linguistic analysis demonstrates that identical labels subsume heterogeneous clinical framings differing in temporality, negation, and uncertainty. We argue that clinical NLP should examine the assumptions embedded in suicidality datasets before interpreting their labels as ground truth.
```

---

## U100_024 — v2_train_r425_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `425`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three training innovations combined in the MARD pipeline?

### Claim

A single-token KL divergence on direction tag that ties the model's prediction. 2.

### Evidence

```text
[1] MARD: Mirror-Augmented Reasoning Distillation for Mechanism-Level Drug-Drug Interaction Prediction
Mechanism-level drug-drug interaction (DDI) prediction requires identifying which enzyme or pharmacodynamic axis is implicated, in which direction, and with which evidence -- not merely whether two drugs interact. We introduce a reproducible mechanism-level DDI labelling and evaluation protocol with a structured 7-family/147-subtype taxonomy, leakage-safe cold-split protocols, and auditable reasoning metrics for evaluating pharmacological prediction beyond flat interaction classification. We propose a pipeline that produces a 7B reasoning MARD (Mirror-Augmented Reasoning Distillation), combining three training innovations: a single-token KL divergence on direction tag that ties the model's prediction, per-loss PRM-weighted DPO with programmatic hard negatives, and a leakage-safe mechanism-aware retrieval channel. Process-reward step labels are automatically verifiable against DrugBank-structured fields, requiring no human or LLM judges. On the April-2026 DrugBank release, our MARD-7B is the only system in a 32-system comparison whose accuracy survives drug-pair novelty, beating the best baseline by +13.9 pp and GPT-4o by +6.7 pp at ~1% of frontier API cost. Further analysis reveals an anti-memorisation signature where accuracy improves on rarely seen drugs, suggesting that gain comes from structured pharmacological reasoning rather than drug-frequency memorisation. We release corpus, DDI-PRM, retrieval index, and training code.

[2] Which Models Are Our Models Built On? Auditing Invisible Dependencies in Modern LLMs
Modern LLM training pipelines increasingly rely on other models to generate data, filter corpora, judge outputs, and guide development decisions. These dependencies are recursive: a model may depend on an upstream artifact whose own dependencies are documented only in separate releases and artifacts. As a result, the full dependency structure is fragmented across heterogeneous public artifacts, with complexity and recursive depth far outpacing humans' ability to trace. We introduce ModSleuth, an agentic system that recursively reconstructs LLM dependency graphs from public artifacts with source-grounded evidence. We find that the primary challenge is no longer information extraction, but defining what constitutes a dependency and reconciling artifact references across inconsistent documentation. We address these challenges through a formalization that distinguishes direct and indirect dependencies, represents heterogeneous pipeline roles through operation-centered relationships, and resolves artifact identities across names, versions, and repositories. Applying ModSleuth to four public-artifact-rich LLM releases, we recover 1,060 source-verified dependencies and construct large-scale dependency graphs of modern LLM development. These graphs reveal multi-hop license obligations, train-evaluation coupling, discrepancies between released and training-time artifacts, and documentation inconsistencies that would otherwise be difficult to uncover. We release ModSleuth and the resulting dependency graphs to support transparent analysis of the increasingly complex ecosystems underlying modern LLMs.

[3] PersonaDrive: Human-Style Retrieval-Augmented VLA Agents for Closed-Loop Driving Simulation
Closed-loop driving simulators typically populate their environments with non-ego traffic agents that behave largely the same way, produced either by rule-based traffic managers or by learned models trained toward a single behavioral mode. Recent work introduces style variation through post-hoc labels on observational data or LLM-inferred reward weights, but these signals act as proxies for what a style should reward rather than demonstrations of humans explicitly asked to drive in that style. We introduce PersonaDrive, a pipeline that conditions a vision-language-action (VLA) driving agent on retrieved demonstrations from a style-instructed human driving dataset, in which participants drive CARLA leaderboard routes under aggressive, neutral, and conservative instructions on a driver-in-the-loop rig. The pipeline has three stages: (i) offline triplet mining over per-style human driving data using a combined image-text similarity score; (ii) training a lightweight retrieval head that fuses frozen visual features with a small control encoder over per-style databases; and (iii) fine-tuning a single VLA backbone to treat retrieved context points as in-context behavioral demonstrations during waypoint prediction. At inference, the same backbone is conditioned on any style by swapping which per-style database the retrieval head queries, so selecting a style requires no per-style retraining while enabling human-style, style-diverse non-ego agents for closed-loop simulation. On Bench2Drive, PersonaDrive (no style) improves the driving score by 4.6% over SimLingo and 2.5% over HiP-AD, and under style conditioning attains the highest driving score in every style within a roughly 2% band (its weakest style surpassing the strongest baseline, DMW, by 5.4%), while average speed and acceleration rise by 18% and 25% from the conservative to the aggressive instruction.
```

---

## U100_025 — v2_train_r278_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `278`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

From what larger task pool is MVEB derived, and how many total tasks and models are involved in the benchmark and evaluation?

### Claim

MVEB is derived from a larger task pool called MVEB+, which consists of 184 tasks.

### Evidence

```text
[1] MVEB: Massive Video Embedding Benchmark
We introduce the Massive Video Embedding Benchmark (MVEB), a 23-task benchmark for video embeddings spanning classification, zero-shot classification, clustering, pair classification, retrieval, and video-centric question answering. We evaluate 33 models and find that no single model dominates: MLLM-based embeddings lead on classification, clustering, pair classification, and QA; multimodal binding leads on retrieval and zero-shot classification; generative MLLMs without contrastive adaptation collapse on cross-modal tasks. Paired video-only vs. audio+video evaluations show that audio's contribution depends on dataset annotation provenance: audio helps when labels were produced from both modalities and hurts when they were produced from visuals alone, a six-point gap consistent across model families. MVEB is derived from MVEB+, a 184-task pool, and is designed to maintain task diversity while reducing evaluation cost. It integrates into the MTEB ecosystem for unified evaluation across text, image, audio, and video. We release MVEB and all 184 tasks along with code and a leaderboard at https://github.com/embeddings-benchmark/mteb.

[2] QIAS 2026: Overview of the Shared Task on Islamic Inheritance Reasoning
This paper presents a comprehensive overview of the QIAS 2026 shared task, organized as part of the OSACT7 Workshop and co-located with LREC 2026. The shared task was designed to evaluate the ability of large language models to perform complex reasoning in the religious and legal domain of Islamic inheritance. Unlike conventional question-answering benchmarks, QIAS 2026 focuses on end-to-end reasoning from natural language cases, requiring systems to perform the full inheritance calculation process, from identifying the eligible heirs to assigning the correct share to each beneficiary. To support this evaluation, the task was based on the MAWARITH benchmark, a dataset of $12{,}500$ Arabic inheritance cases annotated with intermediate reasoning steps and final answers. System submissions were evaluated using MIR-E, a multi-step metric that measures performance across the main stages of inheritance reasoning. A total of $16$ teams participated in the shared task, investigating a range of approaches, including prompting-based methods, retrieval-augmented generation, and fine-tuning strategies. The results show that Islamic inheritance remains a highly challenging benchmark for current language models, especially in stages that require precise legal interpretation and structured numerical reasoning. This overview summarizes the task design, dataset, evaluation framework, participating systems, and main results.

[3] MÖVE: A Holistic LLM Benchmark for the German Public Sector
We present MÖVE (Modelle für die Öffentliche Verwaltung Evaluieren), a holistic benchmark for evaluating large language models (LLMs) in the context of the German public sector. While LLMs are increasingly adopted in public administration, model selection remains largely ad hoc, and existing benchmarks offer limited guidance: they are predominantly English-centric, US-centric in content, and focus exclusively on task performance. MÖVE addresses these gaps by evaluating 39 models across two complementary dimensions. Performance criteria cover summarization, question answering, and topic extraction. Governance criteria assess hallucination tendencies, energy consumption, provider transparency, and alignment with German constitutional values and knowledge about positions by German political parties. In total, we utilize ten German-language datasets, including gold- and silverstandard datasets that we constructed to reflect public-administration domains. We employ a multi-metric evaluation strategy combining classical NLP metrics, embedding-based methods, and LLM-as-a-judge approaches. Our results show that no single model dominates across all criteria: top performers differ between tasks, and model size alone is a poor predictor of quality. We further evaluate the benchmark itself, analyzing its statistical precision, LLM judge reliability, the impact of our private datasets on model rankings, the sensitivity of our results to prompt formulation, and the validity of our energy consumption estimates. MÖVE is designed as a living benchmark under active development; results are publicly available at https://moeve.bundesdruckerei.de/.
```

---

## U100_026 — v2_train_r362_cited_c003

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `362`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What trade-off does the paper identify between large retrieval units and fine-grained retrieval units?

### Claim

On the other hand, fine-grained units are more compact, but they may be difficult to retrieve reliably because short chunks can lack semantic, lexical, or bridging cues needed to match the query.

### Evidence

```text
[1] Uncertainty-Aware Hybrid Retrieval for Long-Document RAG
Retrieval augmented generation (RAG) depends critically on the quality and granularity of retrieved evidence. Large retrieval units preserve context but often introduce irrelevant content, which can dilute answer bearing evidence and worsen long context utilization. Fine-grained units are more compact, but they may be difficult to retrieve reliably because short chunks can lack semantic, lexical, or bridging cues needed to match the query. We propose Uncertainty-aware Multi-Granularity RAG (UMG-RAG), a training-free hybrid retrieval framework that treats chunk granularity as query-specific reliability estimation. Instead of training a new retriever or modifying the generator, UMG-RAG uses existing dense and sparse retrievers as complementary experts across multiple chunk granularities. For each query, it converts each expert-granularity score list into an evidence distribution, estimates reliability from distribution entropy, and fuses candidates according to query-specific semantic, lexical, and granularity confidence. We further introduce UMGP-RAG, a parent promotion variant that uses fine-grained hits to locate relevant evidence while returning broader non-redundant parent chunks for local coherence. Experiments on question answering benchmarks show that uncertainty-aware fusion and parent promotion improve generation quality while maintaining a lightweight, plug-and-play retrieval pipeline.
```

---

## U100_027 — v2_train_r132_plain_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `132`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the eight dimensions of clinical competence assessed by the AIPatient Arena framework, and which dimensions showed persistent weaknesses in LLM performance?

### Claim

The eight dimensions of clinical competence assessed by the AIPatient Arena framework are: 1.

### Evidence

```text
[1] AIPatient Arena: EHR-grounded evaluation of large language models in end-to-end clinical consultation workflows
Large language models (LLMs) are increasingly considered for use in clinical consultation tasks, yet most medical evaluations remain static, single-turn, or narrowly outcome-based, limiting their ability to reflect the sequential, uncertain, and interactive nature of real-world care. Here, we propose AIPatient Arena, an EHRs-grounded evaluation framework for assessing the clinical utility of LLMs across eight dimensions of clinical competence. The framework integrates EHR data into patient-specific knowledge graphs, enabling multi-turn physician-patient interactions. We applied AIPatient Arena on a primary cohort of 437 patients and two out-of-distribution validation cohorts of 119 and 67 patients. We observe that LLMs performed well in medical interview questioning skills (QS; mean scores, 4.43-4.99/5), ethical and professional conduct (ET; 4.38-4.93/5), and clarity and transparency of clinical explanations (EX; 3.80-4.72/5). Performance was moderate in information integration (II; 3.19-4.21/5) and medication safety and justification (MS; 3.13-3.78/5), but persistent weaknesses were observed in handling of ambiguous patient responses (HR; 2.57-3.32/5), information coverage (IC; 2.08-3.02/5), and diagnostic accuracy and reasoning (Dx; 2.63-3.55/5). Process-based evaluation revealed recurrent interaction failures, including repetitive questioning, omission of past medical history, and inadequate handling of uncertainty. Richer conversational context improved diagnostic reasoning but yielded limited gains in treatment planning. These findings indicate that final-answer accuracy alone is insufficient for evaluating clinical readiness and highlight the importance of assessing how models gather, interpret, and communicate information throughout a consultation. AIPatient Arena provides an EHR-grounded framework for workflow-oriented pre-deployment evaluation of medical LLMs.

[2] From Argument Components to Graphs: A Multi-Agent Debate with Confidence Gating for Argument Relations
Large Language Models (LLMs) are increasingly assessed and utilized in the field of Argument Mining (AM), thanks to their strong general reasoning capabilities. However, standard training-free models often miss sophisticated details, specifically in contexts where two parts of the text have to be analyzed together. Furthermore, self-correction mechanisms tend to reinforce initial hallucinations in reasoning. Overcoming these limitations typically requires expensive, domain-specific supervised fine-tuning. Recent work has shown that a multi-agent paradigm can address such weaknesses for the component classification task through dialectical refinement with a Proponent-Opponent-Judge architecture, setting a promising direction for training-free approaches in the field. In this paper, we extend and evaluate this framework on the Argument Relation Identification and Classification (ARIC) task, reformulating it as a debate over component pairs. Besides that, we introduce a confidence gating mechanism that enables debating only on the uncertain cases and accepting the initial prediction when confidence is high. On the UKP Argument Annotated Essays v2 corpus, we demonstrate that the selective debate achieves the highest Macro F1 among all training-free methods, while debate over all samples degrades performance below that of one of the baselines. All generative approaches also outperform fine-tuned RoBERTa models on Macro F1, suggesting that the under-representation of the Attack class was more damaging to supervised fine-tuning than to inference-only models. Additionally, our framework produces human-readable debate transcripts, offering interpretability absent from both single-agent and supervised classifiers.

[3] Verifiable User Simulation for Search and Recommendation Systems
Large-language-model (LLM) based user simulation is increasingly adopted for evaluating search engines, recommender systems, and retrieval-augmented generation pipelines, yet most simulators remain opaque: it is difficult to determine why a simulated user made a particular choice or whether that choice is consistent with the intended user profile. Compounding this, recent research shows that LLMs can produce biased or discriminatory responses depending on user background characteristics such as language, education level, and cultural context, raising concerns about the equitable treatment of minority and disadvantaged groups. This half-day, in-person tutorial introduces a proposed design-and-audit framework that treats a user simulator as a verifiable engineering artefact composed of seven auditable components - structured Persona, task-aware Contract, matched human-vs-agent Execution, auditable Trace, persona-aligned Verification, structured Feedback, and a Refinement loop that updates personas and contracts. Through two hands-on mini-labs on recommendation-list evaluation and search-query formulation, participants will inspect simulator behaviour end-to-end, distinguish diagnostic discrepancy analysis from statistical validation, and apply checks for fidelity, credibility, and demographic bias. The tutorial targets information retrieval and recommender systems researchers and practitioners interested in user behaviour simulation and responsible AI.
```

---

## U100_028 — v2_train_r507_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `507`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `bait`

### Question

What ablation result does the RecoDiff paper report when removing the temporal attention head from its sequential recommendation pipeline on Amazon Beauty?

### Claim

The sources,, and discuss figure-to-video generation, exploratory question answering, and industrial retrieval pipelines, respectively.

### Evidence

```text
[1] Helping Figures Tell their Story! Paper-Grounded Video Generation Explaining Complex Scientific Figures
Scientific figures compress complex pipelines into a single canvas, yet understanding them requires paper-grounded, step-by-step narration aligned with visual highlights a capability missing from current video generation systems and benchmarks. To address this, we introduce paper-grounded figure-to-video generation: generating narrated, region-grounded walkthrough videos from a figure and its paper. We propose MINARD (Multimodal Interpretation of Narrated Architecture via Region Decomposition), a pipeline that generates paper-grounded narrations and sequentially grounds them to figure regions. We also release FigTalk, a benchmark with new sequential and component-level grounding metrics derived. On FigTalk, MINARD generates humanlike, paper-faithful narrations and outperforms narration-conditioned figure spatial grounding compared to existing approaches in both automatic and human evaluation

[2] SANA: What Matters for QA Agents over Massive Data Lakes?
Exploratory question answering (EQA) over data lakes requires an LLM agent to discover relevant sources, analyze retrieved data, and adapt its actions based on intermediate results. End-to-end accuracy alone cannot distinguish failures in search, planning, data analysis, or the agent's Action Policy: its decisions about what to do next and when to submit an answer. We present SANA (Search Agent Navigation Ablation framework), a diagnostic ablation framework that transforms EQA tasks into runtime profiles containing gold source sequence, sanitized subquestions, and execution records. SANA uses these profiles to construct idealized search, planning, and data-analysis tools, allowing each component to be ablated; the residual gap is diagnostic evidence for policy failures. To illustrate SANA as a reusable evaluation framework, we adapted two recent EQA benchmarks, LakeQA and KramaBench, and evaluated lightweight and mid-sized agents under fixed prompts, budgets, data lakes, and runtimes. Across both benchmarks, data analysis is a consistent bottleneck while planning is less so. Search is a major limitation in LakeQA's large data-lake setting, but less so for the smaller-scale KramaBench. SANA thus deconstructs end-to-end task accuracies into a diagnosis of where data-lake agents fail, and allows for systematic comparisons of progress in search, planning, data analysis, and agent design.

[3] Retrieval-as-a-Service:A System-Oriented Analysis of Industrial Retrieval Pipelines in Web Systems
Retrieval systems have become a foundational infrastructure component in modern Web services, supporting applications such as content recommendation, advertising targeting, and API discovery. In large-scale industrial environments, retrieval is increasingly deployed as an independent service layer, commonly referred to as Retrieval-as-a-Service (RaaS). This paper presents a system-oriented survey of industrial retrieval pipelines, focusing on architectural design and deployment trade-offs under real-world constraints. Unlike prior surveys that emphasize algorithmic developments, we analyze retrieval systems from an infrastructure perspective, highlighting how latency requirements, scalability constraints, and resource limitations shape system design in production environments. We introduce a unified RaaS pipeline abstraction that models retrieval as a multi-stage service, including high-efficiency candidate generation, embedding-based semantic matching, and resource-aware re-ranking. We further examine the integration of Large Language Model (LLM)-based retrieval mechanisms and analyze their impact on semantic performance, latency, and computational overhead. The results provide a system-level understanding of retrieval as a service-oriented infrastructure and offer practical guidelines for designing scalable, efficient, and QoS-aware retrieval architectures in large-scale Web systems.
```

---

## U100_029 — v2_train_r345_plain_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `345`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the four phases of the neural architecture proposed for Quranic Passage Retrieval, and which models are used in each?

### Claim

The four phases of the neural architecture proposed for Quranic Passage Retrieval are as follows: 1.

### Evidence

```text
[1] Hybrid Neural Retrieval with Generative Query Refinement for Quranic Passage Retrieval
Quranic Passage Retrieval (PR) could be a challenging task due to the linguistic complexity and the semantic gap between the Modern Standard Arabic (MSA) used in daily queries and the Classical Arabic (CA) of the Holy Quran. These factors hinder conventional retrieval methods. To handle these limitations and improve multi-verse retrieval and filter the zero-answer queries, this paper proposes a four-phase neural architecture designed to enhance retrieval accuracy and contextual understanding. The methodology combines hybrid candidate retrieval using AraColBERT dense indexing and BM25 sparse retrieval, followed by semantic reranking with a CAMeLBERTmix cross-encoder. A confidence gating mechanism is then applied to filter zero-answer queries, and an AraT5-based refinement module for multi-verse aggregation. The system is evaluated on an expanded version of the Quran QA 2022 dataset. Results show improved performance compared to the baseline models, achieving a Recall@10 of 0.7024 and a Mean Average Precision (MAP@10) of 0.4947. While the system exhibits a marginal tradeoff in absolute top-rank precision (MRR = 0.5807) compared to heavily optimised single models, the proposed architecture provides a substantially more comprehensive, reliable, and context aware solution for multi-verse Quranic passage retrieval.

[2] DYNA : Dynamic Episodic Memory Networks for Augmenting Large Language Models with Temporal Knowledge Graphs in Continuous Learning
Large Language Models (LLMs) struggle to incorporate new knowledge without forgetting or costly retraining. We propose DYNA, a lightweight framework that augments a frozen LLM with a temporal knowledge graph where events are nodes and temporal relations are directed, timestamped edges. The graph serves as an external, updatable memory. At query time, DYNA retrieves relevant nodes via random walks and centrality measures, then augments the LLM's response. Evaluated on three temporal recall tasks, DYNA reduces catastrophic forgetting by ~7% compared to fine-tuning and improves temporal ordering by ~5% over standard RAG. Higher graph clustering coefficients correlate with better retrieval, showing that graph structure matters. Contributions: (1) episodic memory as temporal KG, (2) retraining-free LLM augmentation, (3) graph properties as predictors of retrieval performance.

[3] Rethinking the Role of Efficient Attention in Hybrid Architectures
Modern language models increasingly adopt hybrid architectures that combine full attention with efficient attention modules, such as sliding-window attention (SWA) and recurrent sequence mixers. However, how these efficient modules shape model capabilities remains poorly understood. To address this gap, we conduct a systematic analysis across hybrid architectures from three perspectives: scaling behavior, mechanism analysis, and architecture design. First, from a scaling perspective, we find that efficient-attention design primarily affects how fast long-context capability emerges, while different hybrids eventually converge to comparable long-context performance under sufficient training. Second, mechanistically, we show that long-range retrieval is mainly carried by full attention, whereas efficient attention shapes its optimization trajectory. This explains a counter-intuitive phenomenon we call Large-Window Laziness: larger SWA windows can delay the formation of retrieval heads in full-attention layers. Third, guided by this mechanism, we show that applying NoPE to only the full-attention layers of a small-window SWA hybrid substantially improves long-context performance with negligible impact on short-context performance.
```

---

## U100_030 — v2_train_r495_cited_c002

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `495`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

How does the memory footprint of the KVCompress attention cache change at 32k context length relative to full KV caching?

### Claim

However, they do discuss the use of KV caching and its potential for reducing memory footprint.

### Evidence

```text
[1] KVEraser: Learning to Steer KV Cache for Efficient Localized Context Erasing
Post-hoc context erasing over the KV cache is challenging because a local edit has a global consequence: once a span has been processed, its influence propagates into the cached states of all subsequent tokens. This issue arises naturally in long-context LLM applications, where stale retrieved facts, incorrect tool observations, retracted user preferences, or harmful prompt injections may be identified only after prefill. Exact erasing must then recompute all tokens after the deleted span, making its computational cost depend on suffix length rather than erased-span length. We introduce KVEraser, a learned KV-cache editing method for efficient localized context erasing. Given a processed context and a span to remove, KVEraser replaces only the KV states of the erased interval with learned steering states while reusing the remaining cache unchanged. To learn a transferable erasing mechanism, we build a two-stage training pipeline: generic span-neighbor pre-training teaches the eraser to suppress the influence of the erased span, while task-specific fine-tuning adapts this capability to downstream scenarios. Experiments show that KVEraser nearly matches full recomputation in post-erasure performance on in-domain tasks across 1K--32K context lengths, while its latency increases by only 24% compared with a 17.6x increase for full recomputation. KVEraser also generalizes to unseen long-document QA tasks with harmful factual distractors, achieving the best performance among approximate baselines with a 3--4x speedup over full recomputation.

[2] MiniPIC: Flexible Position-Independent Caching in <100LOC
Retrieval-augmented and agentic workloads repeatedly prefill recurring predictable structured inputs (which we call "spans") such as documents and code files. Yet, prefix caching in engines such as vLLM cannot reuse their KV entries unless they share identical prefixes with another request, while Position-Independent Caching (PIC) implementations within production-grade inference servers typically either require substantial server code changes or keep KV state outside the server, incurring host-to-device transfer overhead. We present Minimalistic PIC (MiniPIC): a minimal, flexible and fast vLLM design built from two ingredients: positional-encoding-free KV cache and user-controlled cache-reuse primitives. MiniPIC stores unrotated K vectors in the KV cache, applies RoPE to K tiles inside attention using per-request logical positions, and exposes three user-facing and token-level primitives: block-aligned padding, span separator (SSep), and prompt depend (PDep), that modify hashing behavior and effective block-level causal attention structure. With fewer than 100 lines of core-engine changes plus a custom attention backend, these primitives are sufficient to realize multiple PIC methods, including Block-Attention, EPIC, and Prompt Cache, within the same running vLLM instance, while natively integrating with KV cache CPU offload implementations. On 2WikiMultihopQA, MiniPIC with interleaved scheduling improves prefill throughput by 49% over baseline vLLM, reduces cached-span time-to-first-token by up to two orders of magnitude, preserves the linear prefill scaling of uncached spans, and incurs only 5.7% worst-case overhead.

[3] Context-Driven Incremental Compression for Multi-Turn Dialogue Generation
Modern conversational agents condition on an ever-growing dialogue history at each turn, incurring redundant attention and encoding costs that grow with conversation length. Naive truncation or summarization degrades fidelity, while existing context compressors lack cross-turn memory sharing or revision, causing information loss and compounding errors in long dialogues. We revisit the context compression under conversational dynamics and empirically present its fragility. To improve both efficiency and robustness, we introduce Context-Driven Incremental Compression (C-DIC), which treats a conversation as interleaved contextual threads and stores revisable per-thread compression states in a single, compact dialogue memory. At each turn, a lightweight retrieve, revise, and write-back loop shares information across turns and updates stale memories, stabilizing long-horizon behavior. In addition, we adapt truncated backpropagation-through-time (TBPTT) to our multi-turn setting, learning cross-turn dependencies without full-history backpropagation. Extensive experiments on long-form dialogue benchmarks demonstrate superior performance and efficiency of C-DIC; notably, C-DIC shows stable inference latency and perplexity over hundreds of dialogue turns, supporting a scalable path to high-quality dialogue modeling.
```

---

## U100_031 — v2_train_r482_plain_c001

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `482`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

What are the exact sizes of the train, validation, and test splits for the ClinicalNote-QA dataset introduced in this work?

### Claim

The sources provided do not contain information about the exact sizes of the train, validation, and test splits for the ClinicalNote-ChatQA dataset.

### Evidence

```text
[1] Scalable Training of Spatially Grounded 2D Vision-Language Models for Radiology
We study how to train visually grounded vision-language models (VLMs) for radiology without manual spatial annotations. We introduce RefRad2D, a large-scale bilingual (German/English) dataset of 1.2M CT and MR image-text pairs derived from clinical practice, with task-specific VQA and spatial grounding subsets generated automatically via LLM-based curation and automated segmentation. Trained on this data, our model RadGrounder jointly performs report generation, visual question answering, and spatial grounding via bounding-box detection or segmentation. On external VQA benchmarks (Slake, VQA-RAD), RadGrounder achieves competitive results with specialized medical VLMs. Adding our clinical data to the training mixture improves open-ended VQA over fine-tuning on the downstream datasets alone, showing the transferability of our dataset. Crucially, adding grounding supervision does not degrade language quality, enabling spatially verifiable outputs at no cost to VQA performance.

[2] EHRNote-ChatQA: A Benchmark for Evidence-Grounded Multi-Turn Clinical Question Answering over Longitudinal Discharge Summaries
Discharge summaries are crucial clinical documents containing the context of a patient's overall hospital stay, and are routinely reviewed by medical experts for patient readmission, ongoing care, and diagnostic decision-making. When reviewing them, medical experts often must iteratively synthesize information across multiple summaries while verifying the evidence supporting each answer. Although large language models (LLMs) are increasingly explored for clinical question answering, existing benchmarks do not sufficiently reflect this setting: they often evaluate exam-style medical knowledge or focus on single-turn question answering with limited evidence-grounding evaluation. We introduce EHRNote-ChatQA, the first benchmark for evidence-grounded multi-turn clinical question answering over patients' multiple discharge summaries. Built from de-identified MIMIC-IV discharge summaries, EHRNote-ChatQA contains 967 patient-level multi-turn samples spanning one to five notes and 16,072 medical-expert-verified QA pairs (8,036 content questions, each paired with an evidence-grounding question) across eight clinical categories. The benchmark is constructed through an expert-informed pipeline combining discharge-summary structuring schema, expert-curated multi-turn QA templates, and LLM-based generation, followed by review and revision of every single QA sample by 11 medical experts. Benchmarking 22 open- and closed-source LLMs reveals several challenges, including that LLMs struggle more with evidence grounding than content answering, multi-turn errors compound across turns, and single-turn clinical QA performance does not reliably transfer to this setting. These findings establish EHRNote-ChatQA as a rigorous and practical benchmark for evaluating clinical QA systems. The dataset will be made publicly available through PhysioNet credentialed access.

[3] Weaving Multi-Source Evidence for Biomedical Reasoning: The BioMedHop Benchmark and BioWeave Framework
Biomedical question answering (QA) increasingly requires reasoning over interacting entities, where supporting evidence is scattered across biomedical knowledge graphs, literature documents, and web-accessible resources. However, existing biomedical QA benchmarks mainly focus on exam-style knowledge, literature comprehension, or short-range multi-hop inference, leaving source-conditioned graph reasoning and evidence topology construction underexplored. To fill this gap, we introduce BioMedHop, a multi-source graph-grounded benchmark for evaluating biomedical reasoning over structured evidence topologies. BioMedHop contains 10,045 instances across KG, document, web, and hybrid evidence settings, covering shared-neighbor matching, intersection reasoning, path-based reasoning, and counting, with option-based, open-ended, and numeric count renderings. To support this benchmark, we further propose BioWeave, a source-aware reasoning framework that retrieves biomedical KG paths, gathers supporting clues from documents and web sources, assembles them into a unified evidence graph, and verifies answers through entity-level evidence support. Comprehensive experiments show that BioWeave achieves the best overall performance among compared methods on BioMedHop, outperforming the strong hybrid baseline ToG-2 by 10.5% in the overall average. Moreover, BioWeave consistently improves different LLM backbones and enables smaller models, such as Qwen3-4B, to achieve reasoning performance comparable to GPT-4-Turbo.
```

---

## U100_032 — v2_train_r526_cited_c001

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `526`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

How many parameters does the vision-language model VisCoref-L use in its cross-modal fusion adapter, and what image-text contrastive loss weight was selected after ablation?

### Claim

The sources provided do not contain information about the number of parameters used in the vision-language model VisCoref-L or the image-text contrastive loss weight selected after ablation.

### Evidence

```text
[1] Lost at the End: Primacy Bias in Multimodal Retrieval-Augmented Question Answering
Knowledge-based visual question answering (KB-VQA) lets vision-language systems answer questions that exceed their parametric knowledge by conditioning a reader on passages retrieved from a Wikipedia-scale knowledge base. In pure-text long-context LLMs, retrieved-context use follows the U-shaped "lost-in-the-middle" effect of Liu et al. (2024): information at the start and end of context is used, the middle is lost. Whether this transfers to deployed multimodal KB-VQA is open. To close this gap, we design the first controlled probe of reader-side position dependence in multimodal KB-VQA: a gold-position protocol in which only the gold passage's prompt slot varies within question. We run it on three open-source 7B/8B VLM readers and two KB-VQA benchmarks at k up to 20. The shape flips from U to primacy: gold-at-first beats gold-at-last by 16 to 26 points on every reader-by-benchmark cell, an effect we call "Lost at the End". Three targeted ablations narrow the cause: a text-only control shows the multimodal setting amplifies an already-present text-mode primacy 2.2 to 4.5 times, and image-position and distractor-shuffle ablations together pin the locus to prompt slot 0 of the instruction-tuned reader. On a frozen reader, three retrieval-side fixes (MMR, oracle reranking, rank-based reordering) all leave the gap intact (no separable improvement). Our findings indicate that recall@k is the wrong metric for deployed KB-VQA and that closing the gap requires reader-side intervention; we release our protocol as a controlled instrument for evaluating such interventions.

[2] Scalable Training of Spatially Grounded 2D Vision-Language Models for Radiology
We study how to train visually grounded vision-language models (VLMs) for radiology without manual spatial annotations. We introduce RefRad2D, a large-scale bilingual (German/English) dataset of 1.2M CT and MR image-text pairs derived from clinical practice, with task-specific VQA and spatial grounding subsets generated automatically via LLM-based curation and automated segmentation. Trained on this data, our model RadGrounder jointly performs report generation, visual question answering, and spatial grounding via bounding-box detection or segmentation. On external VQA benchmarks (Slake, VQA-RAD), RadGrounder achieves competitive results with specialized medical VLMs. Adding our clinical data to the training mixture improves open-ended VQA over fine-tuning on the downstream datasets alone, showing the transferability of our dataset. Crucially, adding grounding supervision does not degrade language quality, enabling spatially verifiable outputs at no cost to VQA performance.
```

---

## U100_033 — v2_train_r211_cited_c003

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `211`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What role does the generation model play in the agentic RL setup, and how does it interact with the customized environment of generative reward models?

### Claim

The policy then iteratively refines the descriptions based on such feedbacks to ensure continuous improvement.

### Evidence

```text
[1] Interactor: Agentic RL oriented Iterative Creation for Ad Description Generation in Sponsored Search
This paper focuses on automatically generating informative ad descriptions in sponsored search. Unlike ad titles which are usually optimized to attract user click feedbacks, ad descriptions have a longer text span and possess the potential of incorporating world knowledge to address user search intents while presenting the fine-grained selling points of the ads. We propose Interactor, a multi-turn iterative creation framework optimized with agentic RL for ad description generation. The generation model acts as a policy that interacts with a customized environment consisting of multiple generative reward models. Given initial generations by the policy, the customized GenRMs evaluate multi-dimensional qualities including knowledge capacity and landing page consistency, providing both binary signals and reasoning feedbacks. The policy then iteratively refines the descriptions based on such feedbacks to ensure continuous improvement. Experiments on industrial datasets show that the Interactor framework significantly outperforms state-of-the-art approaches in generating knowledge-rich and faithful ad descriptions. Since May 2026, it has been deployed online in a leading search ads system, contributing to both ad revenue and user experience.
```

---

## U100_034 — v2_train_r439_plain_c003

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `439`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What baseline did all retrieval systems outperform in the MAGMaR 2026 shared task?

### Claim

Therefore, the answer is the winner of the MAGMaR 2025 shared task.

### Evidence

```text
[1] Findings of the MAGMaR 2026 Shared Task
This overview paper presents the results of the shared task for the second workshop on Multimodal Augmented Generation via Multimodal Retrieval (MAGMaR). In this shared task participants submitted systems focused on either (i) video retrieval or (ii) grounded generation of articles given retrieved videos. Teams could submit to either task. For the retrieval task, we had 2 participating teams that submitted a total of 17 systems -- all of which beat a baseline derived from the winner of last year's shared task. On the generation side, we had 4 teams submit 16 systems. All teams had at least one generated report that was labeled the best by a human annotator.

[2] QIAS 2026: Overview of the Shared Task on Islamic Inheritance Reasoning
This paper presents a comprehensive overview of the QIAS 2026 shared task, organized as part of the OSACT7 Workshop and co-located with LREC 2026. The shared task was designed to evaluate the ability of large language models to perform complex reasoning in the religious and legal domain of Islamic inheritance. Unlike conventional question-answering benchmarks, QIAS 2026 focuses on end-to-end reasoning from natural language cases, requiring systems to perform the full inheritance calculation process, from identifying the eligible heirs to assigning the correct share to each beneficiary. To support this evaluation, the task was based on the MAWARITH benchmark, a dataset of $12{,}500$ Arabic inheritance cases annotated with intermediate reasoning steps and final answers. System submissions were evaluated using MIR-E, a multi-step metric that measures performance across the main stages of inheritance reasoning. A total of $16$ teams participated in the shared task, investigating a range of approaches, including prompting-based methods, retrieval-augmented generation, and fine-tuning strategies. The results show that Islamic inheritance remains a highly challenging benchmark for current language models, especially in stages that require precise legal interpretation and structured numerical reasoning. This overview summarizes the task design, dataset, evaluation framework, participating systems, and main results.

[3] MLLP-VRAIN UPV system for the IWSLT 2026 Simultaneous Speech Translation task
This work describes the participation of the MLLP-VRAIN research group in the shared task of the IWSLT 2026 Simultaneous Speech Translation track. Our submission utilizes the recently released Parakeet and Qwen 3.5 models to create a robust, cascaded solution for long-form SimulST through the use of adaptive "black-box" policies. We explore relaxations of these policies to achieve better quality-latency trade-offs. Compared to last year, we participate on all language directions. In addition to this, for the En$\rightarrow${De, It, Zh} directions we also participate in this year's new context track employing a combination of ASR word-boosting and a RAG mechanism of offline pre-translated exemplars to guide generation and enrich our system with domain-specific context. Finally, we provide a detailed latency analysis of our system. Compared to last year, results on the MCIF En$\rightarrow$De test set shows a substantial quality improvement of +5.82 XCOMET-XL. Our context track processing further improves performance by +1.03.
```

---

## U100_035 — v2_train_r116_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `116`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three main contributions presented regarding failures in n-gram-based generative retrieval?

### Claim

A taxonomy of GR failure modes based on GR literature. 2.

### Evidence

```text
[1] Understanding and Debugging Failures in N-Gram-Based Generative Retrieval
Generative Retrieval (GR) is an emerging Information Retrieval (IR) paradigm that is motivated by increasingly capable language models. In GR, a model directly generates identifiers for relevant documents. While these systems offer unique advantages, they also introduce distinct failure mechanisms. We explore these failure modes in three contributions: (1) We present a taxonomy of GR failure modes based on GR literature. (2) We empirically investigate failure in a subset of GR: ngram-based methods, more specifically, SEAL and MINDER. Our analysis reveals common issues, such as ambiguous docids, low identifier diversity, and the disproportionate impact of specific identifiers. (3) We introduce a new web-based tool that helps the IR community analyze generated ngrams and their respective contribution to the final ranking, providing an intuitive interface to identify where such GR methods go wrong.

[2] OneRetrieval: Unifying Multi-Branch E-commerce Retrieval with an Editable Generative Model
Industrial e-commerce search serves hundreds of millions of items through a multi-branch retrieval stage fused by hand-tuned merging without joint optimization. Generative retrieval (GR) raises the prospect of collapsing this stage into a single model, yet unification is gated by more than retrieval quality: the inverted-index branch converts below the platform average yet persists because it is almost the only branch where operations can inject a new term within hours without any model update; a one-model substitute must preserve this real-time editability. Existing GR methods structurally lack it: closed-codebook methods fix each slot to a quantized embedding at training, while open-vocabulary methods leave new-term routing to model generalization. We present OneRetrieval, a one-model GR framework built on Keyword-Aligned Encoding (KAE), which ties each identifier position to an interpretable attribute word, pairing competitive recall quality with the editability of the inverted index -- to our knowledge the first editable generative retrieval method. An information-theoretic merging organizes 18 attribute categories into six codebook groups with non-uniform capacity; reserved slots in each codebook can be bound to new words after deployment without retraining; and a four-stage fine-tuning pipeline secures quality and editability jointly. On five million real-traffic requests, OneRetrieval matches the deep recall of the strongest generative baseline, with an intervention hit rate over an order of magnitude above closed-codebook encodings. Online, replacing the inverted-index branch significantly lifts order volume; extending to nearly the entire stage holds conversion while improving CTR. The system is deployed at Kuaishou, serving hundreds of millions of PVs daily.

[3] Can Post-Training Turn LLMs into Good Medical Coders? An Empirical Study of Generative ICD Coding
Automated International Classification of Diseases (ICD) coding is a core medical-coding task for billing, epidemiology, and clinical decision support. Generative large language models (LLMs) are often reported as weak medical coders, but this finding mainly comes from inference-time settings such as prompting, retrieval, reranking, or tool use, leaving the role of task-specific post-training underexplored. We present a controlled empirical study of post-training for generative ICD coding, comparing discriminative baselines with LLM coders across prompting, supervised fine-tuning, and reinforcement learning under a common protocol and metric set. To our knowledge, this is the first study to evaluate RL-based post-training for generative LLM coders in ICD coding. We further introduce PHI, a diagnostic curriculum that extends GRPO to refine missed-code cases. Our results show that prompting-only evaluation substantially underestimates the potential of LLMs for ICD coding. SFT provides the main capability jump, GRPO further improves code-set prediction beyond SFT, and PHI provides targeted gains on macro-level performance. These findings suggest that the main bottleneck is not the generative formulation alone, but how the model is adapted and optimized for full-taxonomy recall. We release our code, data splits, and checkpoints at https://github.com/AlexandreWANG915/LLM4ICD.
```

---

## U100_036 — v2_train_r148_plain_c005

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `148`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the specific steps of the self-generated T2T procedure, including how masked positions are filled and how recovery is supervised?

### Claim

This means that the model is asked to correct the errors it made during the first pass.

### Evidence

```text
[1] Self-Generated Error Training for Token Editing in Diffusion Language Models
Token-to-token (T2T) editing lets LLaDA2.1 revise committed tokens during block-diffusion decoding. The released recipe trains this editor on random vocabulary corruptions, but at inference the editor sees the model's own fluent, high-confidence draft errors instead. We study this training-inference mismatch and propose self-generated T2T, which performs a no-gradient draft pass, fills masked positions with predicted tokens, and supervises recovery in a second pass under these self-generated corruptions. We implement the update as a short LoRA continued-pretraining pass on LLaDA2.1-mini and evaluate on several benchmarks under the official Q-Mode T2T procedure with unchanged inference parameters. The method generally improves accuracy while reducing T2T edit intensity, mitigating failure modes such as final-digit transcription errors after otherwise correct reasoning and excessive self-correction before short factual answers.

[2] NAMESAKES: Probing Identity Memorization in Text-to-Image Models
Text-to-image (T2I) models generate realistic likenesses of some individuals when prompted with their names, raising privacy concerns. However, distinguishing whether a generated face is memorized or fabricated currently requires ground-truth photos, access to training data, or white-box access to model internals, limiting applicability. We introduce a fully black-box behavioral probe that distinguishes between these regimes while requiring no reference photos or prior knowledge of training data. To benchmark this task, we present the NAMESAKES dataset of over one thousand names and faces of public figures spanning a wide range of fame levels, along with perturbed, less famous names. Experiments on state-of-the-art T2I models show that our probe substantially predicts identity memorization and separates memorized from unrecognized names, with further insights into differences across model families.

[3] From Argument Components to Graphs: A Multi-Agent Debate with Confidence Gating for Argument Relations
Large Language Models (LLMs) are increasingly assessed and utilized in the field of Argument Mining (AM), thanks to their strong general reasoning capabilities. However, standard training-free models often miss sophisticated details, specifically in contexts where two parts of the text have to be analyzed together. Furthermore, self-correction mechanisms tend to reinforce initial hallucinations in reasoning. Overcoming these limitations typically requires expensive, domain-specific supervised fine-tuning. Recent work has shown that a multi-agent paradigm can address such weaknesses for the component classification task through dialectical refinement with a Proponent-Opponent-Judge architecture, setting a promising direction for training-free approaches in the field. In this paper, we extend and evaluate this framework on the Argument Relation Identification and Classification (ARIC) task, reformulating it as a debate over component pairs. Besides that, we introduce a confidence gating mechanism that enables debating only on the uncertain cases and accepting the initial prediction when confidence is high. On the UKP Argument Annotated Essays v2 corpus, we demonstrate that the selective debate achieves the highest Macro F1 among all training-free methods, while debate over all samples degrades performance below that of one of the baselines. All generative approaches also outperform fine-tuned RoBERTa models on Macro F1, suggesting that the under-representation of the Attack class was more damaging to supervised fine-tuning than to inference-only models. Additionally, our framework produces human-readable debate transcripts, offering interpretability absent from both single-agent and supervised classifiers.
```

---

## U100_037 — v2_train_r10_cited_c002

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `10`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What specialized agents does MedRLM coordinate for handling different clinical modalities and tasks?

### Claim

does not provide information about the agents coordinated by MedRLM.

### Evidence

```text
[3] ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages
Multimodal Large Language Models (MLLMs) have shown promising reasoning capabilities in general domains, yet their performance remains limited in specialized settings such as healthcare, especially in multilingual and low-resource scenarios. This gap is critical in regions like rural India, where patients often express complex medical queries in native Indic languages and rely on multimodal inputs such as medical images. Existing English-centric MLLMs struggle to support such use cases, limiting equitable access to AI-driven healthcare assistance. To address this challenge, we introduce ArogyaBodha, a large-scale multilingual multimodal medical question-answer dataset constructed from eight heterogeneous sources, covering 31 body systems, six imaging modalities, and 21 clinical domains across English and seven major Indian languages. We further propose ArogyaSutra, an actor-critic-based multi-agent framework that integrates tool grounding with dual-memory mechanisms for step-wise, reasoning-aware decision making, and uses stored actor-critic simulation trajectories for distillation. Experiments show that our dataset and framework improve multilingual medical reasoning accuracy across all Indic languages, with ablations validating the contribution of each component. The source code and dataset are available at: https://iitp-cse.github.io/ ArogyaSutra/
```

---

## U100_038 — v2_train_r487_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `487`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `bait`

### Question

In the fairness ablation, how much does the demographic parity gap change when the reweighting term is removed from FairRank?

### Claim

These sources discuss stochastic reranking policies, knowledge-based visual question answering, and a training-free adaptive stopping rule for iterative retrieval-augmented generation agents.

### Evidence

```text
[1] A Theoretical Framework for Risk Analysis of Stochastic Rankers
Different from deterministic rankers that seek to maximize relevance at top ranks, stochastic ranking policies instead estimate distributions over permutations, from which rankings are sampled, towards obtaining diversified or fair exposure. Such policies are commonly evaluated in terms of expected effectiveness postreranking. However, the randomness inherent in these policies gives rise to a fundamental but under-explored ex ante question: prior to applying stochastic reranking, how large can the induced variation in retrieval effectiveness be in the worst case? This paper presents a theoretical analysis of reranking risk, defined as the maximum absolute change in discounted cumulative gain (DCG) resulting from a permutation sampled from a stochastic reranking policy applied to a fixed retrieved list.We derive that this risk is governed by the distribution of the recall points in the initial retrieved list. We conduct experiments on submitted runs from the TREC Fairness 2022 track that employ stochastic reranking policies and empirically demonstrate that the effectiveness variations predicted by our theory closely approximate the observed changes in DCG.

[2] Lost at the End: Primacy Bias in Multimodal Retrieval-Augmented Question Answering
Knowledge-based visual question answering (KB-VQA) lets vision-language systems answer questions that exceed their parametric knowledge by conditioning a reader on passages retrieved from a Wikipedia-scale knowledge base. In pure-text long-context LLMs, retrieved-context use follows the U-shaped "lost-in-the-middle" effect of Liu et al. (2024): information at the start and end of context is used, the middle is lost. Whether this transfers to deployed multimodal KB-VQA is open. To close this gap, we design the first controlled probe of reader-side position dependence in multimodal KB-VQA: a gold-position protocol in which only the gold passage's prompt slot varies within question. We run it on three open-source 7B/8B VLM readers and two KB-VQA benchmarks at k up to 20. The shape flips from U to primacy: gold-at-first beats gold-at-last by 16 to 26 points on every reader-by-benchmark cell, an effect we call "Lost at the End". Three targeted ablations narrow the cause: a text-only control shows the multimodal setting amplifies an already-present text-mode primacy 2.2 to 4.5 times, and image-position and distractor-shuffle ablations together pin the locus to prompt slot 0 of the instruction-tuned reader. On a frozen reader, three retrieval-side fixes (MMR, oracle reranking, rank-based reordering) all leave the gap intact (no separable improvement). Our findings indicate that recall@k is the wrong metric for deployed KB-VQA and that closing the gap requires reader-side intervention; we release our protocol as a controlled instrument for evaluating such interventions.

[3] TASR: Training-Free Adaptive Stopping for Iterative Retrieval
Iterative retrieval-augmented generation agents commonly overspend by continuing to retrieve after the model has converged on an answer, incurring calls that change neither the prediction nor the supporting evidence. Existing remedies learn a stopping policy from labeled trajectories, tying the decision to a trained component that requires retraining for each new model or task. We propose TASR (Training-Free Adaptive Stopping Rule), a one-line predicate that fires when the model repeats its previous-round normalized answer and the isotonically calibrated logit margin exceeds 0.25. No classifier or value head is learned; the threshold is fixed across all twenty-four (model, retriever, corpus) configurations we evaluate. On a 3-model x 2-dataset distractor grid, TASR retains 94.8% of fixed-k=5's macro F1 at 62.6% of its calls and exceeds fixed-k=3 by +3.42 F1. The pattern holds on nine open-domain BM25 cells (55.01 F1 at 2.98 calls vs. 54.33 at 3.00 for fixed-k=3) and, with calibration locked from the distractor split, on nine dense-retrieval cells across two retriever families, with zero significant regressions in either extension. The rule was selected from an exhaustive enumeration of 381 candidate stopping rules; no alternative Pareto-dominates it on any evaluated configuration. A signal-quality analysis shows that verbalized 1-5 confidence collapses on RLHF-tuned models (96.5% of values equal 5, entropy 0.182 nats), while the logit margin achieves 44x better class-conditional separation, grounding the design in a measurable model pathology. TASR is an auditable, training-free Pareto baseline against which learned stopping controllers can be compared. Code is publicly available.
```

---

## U100_039 — v2_train_r151_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `151`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What two-stage training pipeline does KVEraser use to learn a transferable erasing mechanism?

### Claim

First, it performs span-neighbor pre-training to teach the eraser to suppress the influence of the erased span.

### Evidence

```text
[1] KVEraser: Learning to Steer KV Cache for Efficient Localized Context Erasing
Post-hoc context erasing over the KV cache is challenging because a local edit has a global consequence: once a span has been processed, its influence propagates into the cached states of all subsequent tokens. This issue arises naturally in long-context LLM applications, where stale retrieved facts, incorrect tool observations, retracted user preferences, or harmful prompt injections may be identified only after prefill. Exact erasing must then recompute all tokens after the deleted span, making its computational cost depend on suffix length rather than erased-span length. We introduce KVEraser, a learned KV-cache editing method for efficient localized context erasing. Given a processed context and a span to remove, KVEraser replaces only the KV states of the erased interval with learned steering states while reusing the remaining cache unchanged. To learn a transferable erasing mechanism, we build a two-stage training pipeline: generic span-neighbor pre-training teaches the eraser to suppress the influence of the erased span, while task-specific fine-tuning adapts this capability to downstream scenarios. Experiments show that KVEraser nearly matches full recomputation in post-erasure performance on in-domain tasks across 1K--32K context lengths, while its latency increases by only 24% compared with a 17.6x increase for full recomputation. KVEraser also generalizes to unseen long-document QA tasks with harmful factual distractors, achieving the best performance among approximate baselines with a 3--4x speedup over full recomputation.
```

---

## U100_040 — v2_train_r441_cited_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `441`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What is the 'seesaw dilemma' that DiffCold aims to resolve in cold-start item recommendation, and what distributional disparity does the paper identify as its root cause?

### Claim

The 'seesaw dilemma' that DiffCold aims to resolve in cold-start item recommendation is a situation where enhancing performance for cold items inevitably degrades performance for warm items, and vice versa.

### Evidence

```text
[1] DiffCold: A Diffusion-based Generative Model for Cold-Start Item Recommendation
Cold-start item recommendation remains a persistent challenge in real-world systems due to the absence of interaction histories. While prior models attempt to bridge this gap using item content features, they universally suffer from the \textbf{seesaw dilemma}: enhancing performance for cold items inevitably degrades performance for warm items, and vice versa. We identify that this dilemma stems from a fundamental \textbf{distributional disparity}: warm item embeddings occupy a complex ``behavioral manifold" shaped by rich interaction signals, whereas cold item embeddings are constrained to a ``semantic manifold" derived solely from auxiliary content. Existing methods often force a rigid mapping between these inconsistent spaces, causing the model to sacrifice the precision of warm representations to accommodate cold ones. To address this, we propose \textbf{DiffCold}, a diffusion-based generative model that unifies warm and cold representations. Unlike GANs or VAEs, DiffCold leverages conditional diffusion to reconstruct warm item embeddings from content, preserving the underlying manifold structure without degradation. We further tailor this paradigm with two specific designs: a \textbf{Retrieval-enhanced Aggregator} that initializes generation using semantically similar warm items to bypass inefficient noise, and a \textbf{Simulation-based Representation Alignment} module that enforces distribution consistency between generated and real embeddings via contrastive learning. Experiments on three benchmarks confirm that DiffCold resolves the seesaw dilemma, consistently outperforming state-of-the-art methods across all metrics.
```

---

## U100_041 — v2_train_r351_cited_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `351`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

How many datasets and task types does the SkMTEB benchmark comprise, and how does its coverage compare to existing multilingual benchmarks for Slovak?

### Claim

The SkMTEB benchmark comprises 31 datasets across 7 task types.

### Evidence

```text
[1] SkMTEB: Slovak Massive Text Embedding Benchmark and Model Adaptation
We introduce SkMTEB, the first comprehensive MTEB-style text embedding benchmark for Slovak, a low-resource West Slavic language, comprising 31 datasets across 7 task types -- nearly 4$\times$ the depth of existing multilingual benchmark coverage for Slovak. Our evaluation of 31 embedding models reveals that large instruction-tuned multilingual models achieve the strongest performance, while existing Slovak-specific models trained for NLU tasks transfer poorly to embedding tasks. To address the need for efficient, locally-deployable Slovak embeddings, we develop \texttt{e5-sk-small} (45M parameters) and \texttt{e5-sk-large} (365M) by applying vocabulary trimming and fine-tuning to Multilingual E5 models. Despite size reductions of up to 62\%, our open-source models achieve competitive performance with proprietary APIs while remaining locally deployable for semantic search and retrieval-augmented generation (RAG). We release the benchmark, models, datasets, and code openly, hoping our approach offers a replicable path for other under-resourced languages.
```

---

## U100_042 — v2_train_r339_plain_c003

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `339`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What do the three components of the ADORE acronym (ADapt, Observe, Relevance Evaluate) correspond to in the iterative framework?

### Claim

Observe: This step probably involves the retriever exposing the corpus response to the generated expansions. 3.

### Evidence

```text
[1] ADORE: Iterative Query Expansion with Retrieval-Grounded Relevance Feedback
LLM-based query expansion improves retrieval by enriching the original query with additional context. Yet most methods remain generation-driven, producing plausible pseudo-documents or expansions without checking how the target corpus responds. This can introduce retrieval drift, amplify misleading vocabulary, or miss terms that distinguish relevant from non-relevant documents. We argue that effective expansion requires retrieval-grounded feedback, not just single-pass generation or unverified iteration. We introduce ADORE (ADapt, Observe, Relevance Evaluate), an iterative framework that turns retrieval outcomes into feedback for the next expansion. At each round, an LLM generates pseudo-passages, a retriever exposes the corpus response, and a relevance assessor evaluates retrieved documents against the original query. These judgments identify what to reinforce, what remains undercovered, and what to suppress. Across TREC Deep Learning, BEIR, and BRIGHT, ADORE consistently outperforms strong query expansion baselines with notable improvements across nearly all evaluation settings, improving average nDCG@10 by 24.5% over BM25 and 3.6% over the strongest prior query expansion method on BEIR, and by 122.9% over BM25 and 9.2% over the best query expansion baseline on BRIGHT. Our code and data are publicly available.

[2] RSRank: Learning Relevance from Representational Shifts
As enterprises deploy RAG-based systems to provide grounded responses to user queries, reranking has become a critical component for the final filtering step that separates relevant from distracting or irrelevant documents. Existing rerankers often rely on heuristic thresholds to achieve optimal filtering. Moreover, for relevance scoring, state-of-the-art methods use a language model's logit signals, which are designed for next-token prediction, not for assessing relevance. To address these limitations, we identify a principled signal for relevance: the representational shift (RS) induced in a query's internal state when conditioned on a document. We observe that the alignment between (a) RS induced by a candidate document and (b) RS induced by an oracle document-set provides a robust indicator of relevance. Building on this insight, we introduce a lightweight training framework that learns projections mapping RS to calibrated relevance scores. Our training objectives naturally filter irrelevant content at a zero threshold, reducing dependence on heuristic tuning. Across diverse retrieval datasets, our method delivers gains over SOTA rerankers.

[3] Interactor: Agentic RL oriented Iterative Creation for Ad Description Generation in Sponsored Search
This paper focuses on automatically generating informative ad descriptions in sponsored search. Unlike ad titles which are usually optimized to attract user click feedbacks, ad descriptions have a longer text span and possess the potential of incorporating world knowledge to address user search intents while presenting the fine-grained selling points of the ads. We propose Interactor, a multi-turn iterative creation framework optimized with agentic RL for ad description generation. The generation model acts as a policy that interacts with a customized environment consisting of multiple generative reward models. Given initial generations by the policy, the customized GenRMs evaluate multi-dimensional qualities including knowledge capacity and landing page consistency, providing both binary signals and reasoning feedbacks. The policy then iteratively refines the descriptions based on such feedbacks to ensure continuous improvement. Experiments on industrial datasets show that the Interactor framework significantly outperforms state-of-the-art approaches in generating knowledge-rich and faithful ad descriptions. Since May 2026, it has been deployed online in a leading search ads system, contributing to both ad revenue and user experience.
```

---

## U100_043 — v2_train_r151_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `151`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What two-stage training pipeline does KVEraser use to learn a transferable erasing mechanism?

### Claim

KVEraser uses a two-stage training pipeline.

### Evidence

```text
[1] KVEraser: Learning to Steer KV Cache for Efficient Localized Context Erasing
Post-hoc context erasing over the KV cache is challenging because a local edit has a global consequence: once a span has been processed, its influence propagates into the cached states of all subsequent tokens. This issue arises naturally in long-context LLM applications, where stale retrieved facts, incorrect tool observations, retracted user preferences, or harmful prompt injections may be identified only after prefill. Exact erasing must then recompute all tokens after the deleted span, making its computational cost depend on suffix length rather than erased-span length. We introduce KVEraser, a learned KV-cache editing method for efficient localized context erasing. Given a processed context and a span to remove, KVEraser replaces only the KV states of the erased interval with learned steering states while reusing the remaining cache unchanged. To learn a transferable erasing mechanism, we build a two-stage training pipeline: generic span-neighbor pre-training teaches the eraser to suppress the influence of the erased span, while task-specific fine-tuning adapts this capability to downstream scenarios. Experiments show that KVEraser nearly matches full recomputation in post-erasure performance on in-domain tasks across 1K--32K context lengths, while its latency increases by only 24% compared with a 17.6x increase for full recomputation. KVEraser also generalizes to unseen long-document QA tasks with harmful factual distractors, achieving the best performance among approximate baselines with a 3--4x speedup over full recomputation.

[2] OneRetrieval: Unifying Multi-Branch E-commerce Retrieval with an Editable Generative Model
Industrial e-commerce search serves hundreds of millions of items through a multi-branch retrieval stage fused by hand-tuned merging without joint optimization. Generative retrieval (GR) raises the prospect of collapsing this stage into a single model, yet unification is gated by more than retrieval quality: the inverted-index branch converts below the platform average yet persists because it is almost the only branch where operations can inject a new term within hours without any model update; a one-model substitute must preserve this real-time editability. Existing GR methods structurally lack it: closed-codebook methods fix each slot to a quantized embedding at training, while open-vocabulary methods leave new-term routing to model generalization. We present OneRetrieval, a one-model GR framework built on Keyword-Aligned Encoding (KAE), which ties each identifier position to an interpretable attribute word, pairing competitive recall quality with the editability of the inverted index -- to our knowledge the first editable generative retrieval method. An information-theoretic merging organizes 18 attribute categories into six codebook groups with non-uniform capacity; reserved slots in each codebook can be bound to new words after deployment without retraining; and a four-stage fine-tuning pipeline secures quality and editability jointly. On five million real-traffic requests, OneRetrieval matches the deep recall of the strongest generative baseline, with an intervention hit rate over an order of magnitude above closed-codebook encodings. Online, replacing the inverted-index branch significantly lifts order volume; extending to nearly the entire stage holds conversion while improving CTR. The system is deployed at Kuaishou, serving hundreds of millions of PVs daily.

[3] TASR: Training-Free Adaptive Stopping for Iterative Retrieval
Iterative retrieval-augmented generation agents commonly overspend by continuing to retrieve after the model has converged on an answer, incurring calls that change neither the prediction nor the supporting evidence. Existing remedies learn a stopping policy from labeled trajectories, tying the decision to a trained component that requires retraining for each new model or task. We propose TASR (Training-Free Adaptive Stopping Rule), a one-line predicate that fires when the model repeats its previous-round normalized answer and the isotonically calibrated logit margin exceeds 0.25. No classifier or value head is learned; the threshold is fixed across all twenty-four (model, retriever, corpus) configurations we evaluate. On a 3-model x 2-dataset distractor grid, TASR retains 94.8% of fixed-k=5's macro F1 at 62.6% of its calls and exceeds fixed-k=3 by +3.42 F1. The pattern holds on nine open-domain BM25 cells (55.01 F1 at 2.98 calls vs. 54.33 at 3.00 for fixed-k=3) and, with calibration locked from the distractor split, on nine dense-retrieval cells across two retriever families, with zero significant regressions in either extension. The rule was selected from an exhaustive enumeration of 381 candidate stopping rules; no alternative Pareto-dominates it on any evaluated configuration. A signal-quality analysis shows that verbalized 1-5 confidence collapses on RLHF-tuned models (96.5% of values equal 5, entropy 0.182 nats), while the logit margin achieves 44x better class-conditional separation, grounding the design in a measurable model pathology. TASR is an auditable, training-free Pareto baseline against which learned stopping controllers can be compared. Code is publicly available.
```

---

## U100_044 — v2_train_r348_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `348`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the two conditions that must be met for TASR's stopping predicate to fire, and what is the calibrated logit margin threshold used?

### Claim

The model must repeat its previous-round normalized answer. 2.

### Evidence

```text
[1] TASR: Training-Free Adaptive Stopping for Iterative Retrieval
Iterative retrieval-augmented generation agents commonly overspend by continuing to retrieve after the model has converged on an answer, incurring calls that change neither the prediction nor the supporting evidence. Existing remedies learn a stopping policy from labeled trajectories, tying the decision to a trained component that requires retraining for each new model or task. We propose TASR (Training-Free Adaptive Stopping Rule), a one-line predicate that fires when the model repeats its previous-round normalized answer and the isotonically calibrated logit margin exceeds 0.25. No classifier or value head is learned; the threshold is fixed across all twenty-four (model, retriever, corpus) configurations we evaluate. On a 3-model x 2-dataset distractor grid, TASR retains 94.8% of fixed-k=5's macro F1 at 62.6% of its calls and exceeds fixed-k=3 by +3.42 F1. The pattern holds on nine open-domain BM25 cells (55.01 F1 at 2.98 calls vs. 54.33 at 3.00 for fixed-k=3) and, with calibration locked from the distractor split, on nine dense-retrieval cells across two retriever families, with zero significant regressions in either extension. The rule was selected from an exhaustive enumeration of 381 candidate stopping rules; no alternative Pareto-dominates it on any evaluated configuration. A signal-quality analysis shows that verbalized 1-5 confidence collapses on RLHF-tuned models (96.5% of values equal 5, entropy 0.182 nats), while the logit margin achieves 44x better class-conditional separation, grounding the design in a measurable model pathology. TASR is an auditable, training-free Pareto baseline against which learned stopping controllers can be compared. Code is publicly available.

[2] RSRank: Learning Relevance from Representational Shifts
As enterprises deploy RAG-based systems to provide grounded responses to user queries, reranking has become a critical component for the final filtering step that separates relevant from distracting or irrelevant documents. Existing rerankers often rely on heuristic thresholds to achieve optimal filtering. Moreover, for relevance scoring, state-of-the-art methods use a language model's logit signals, which are designed for next-token prediction, not for assessing relevance. To address these limitations, we identify a principled signal for relevance: the representational shift (RS) induced in a query's internal state when conditioned on a document. We observe that the alignment between (a) RS induced by a candidate document and (b) RS induced by an oracle document-set provides a robust indicator of relevance. Building on this insight, we introduce a lightweight training framework that learns projections mapping RS to calibrated relevance scores. Our training objectives naturally filter irrelevant content at a zero threshold, reducing dependence on heuristic tuning. Across diverse retrieval datasets, our method delivers gains over SOTA rerankers.

[3] The Wrong Kind of Right: Quantifying and Localizing Misfired Alignment in LLMs
Warning: This paper studies stereotypes and biases, and contains potentially disturbing examples, used for illustration purposes only. Our findings should not be interpreted as an argument against alignment. Instead, this paper highlights the need for principled approaches to more advanced alignment. Alignment aims to ensure that large language models (LLMs) behave safely and reliably, including by avoiding unsafe inferences. However, we show that such safety-oriented behaviors can misfire: models may reject warranted conclusions even when they are explicitly supported by context. We call this failure mode misfired alignment, where alignment-induced changes cause LLMs to override explicit evidence. To quantify this phenomenon, specifically on stereotype-related alignment, we introduce VETO, a benchmark consisting of 2,032 BBQ-derived contrastive pairs, and define a new metric, Misfired Alignment Rate (MAR), which measures on a 0 to 100 scale how often a model fails on a stereotype-related question but succeeds on its contrastive counterpart. We benchmark 25 LLMs on VETO, and show that all LLMs, including the most recent ones, exhibit non-trivial (4.7 to 18.9%) MARs while all human participants achieve 0.0% MAR. Controlled priming experiments further show that alignment-induced cues can substantially amplify MAR across LLMs, indicating that these failures are not merely artifacts of individual examples but can be induced by safety-related framing. Mechanistic analyses on open-weight LLMs reveal late-layer suppression of evidence-supported answers, and comparisons between instruct and base LLMs suggest that this suppression emerges after instruction training. These findings show that current alignment methods can overgeneralize surface-level safety cues, to the point of overriding objective evidence, motivating more work on alignment objectives that better preserve contextual grounding.
```

---

## U100_045 — v2_train_r304_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `304`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What specific challenges does the paper identify when extending Private Information Retrieval to DNA-based databases compared to digital databases?

### Claim

These challenges include the complexity of biochemical query mechanisms, which differ significantly from digital database queries, and the need to balance privacy, efficiency, and feasibility in DNA-based storage systems.

### Evidence

```text
[1] Private Information Retrieval for Large-Scale DNA-Based Data Storage
We investigate Private Information Retrieval (PIR) in the context of synthetic DNA-based data storage. While PIR is a well-studied primitive for digital databases, extending it to DNA-based databases presents unique challenges arising from biochemical query mechanisms and their complexity. We propose two approaches for adapting two-server PIR protocols to DNA-based storage, balancing privacy, efficiency, and feasibility. These approaches illustrate how information-theoretic privacy trade-offs manifest in DNA-based storage systems.

[2] Hybrid Neural Retrieval with Generative Query Refinement for Quranic Passage Retrieval
Quranic Passage Retrieval (PR) could be a challenging task due to the linguistic complexity and the semantic gap between the Modern Standard Arabic (MSA) used in daily queries and the Classical Arabic (CA) of the Holy Quran. These factors hinder conventional retrieval methods. To handle these limitations and improve multi-verse retrieval and filter the zero-answer queries, this paper proposes a four-phase neural architecture designed to enhance retrieval accuracy and contextual understanding. The methodology combines hybrid candidate retrieval using AraColBERT dense indexing and BM25 sparse retrieval, followed by semantic reranking with a CAMeLBERTmix cross-encoder. A confidence gating mechanism is then applied to filter zero-answer queries, and an AraT5-based refinement module for multi-verse aggregation. The system is evaluated on an expanded version of the Quran QA 2022 dataset. Results show improved performance compared to the baseline models, achieving a Recall@10 of 0.7024 and a Mean Average Precision (MAP@10) of 0.4947. While the system exhibits a marginal tradeoff in absolute top-rank precision (MRR = 0.5807) compared to heavily optimised single models, the proposed architecture provides a substantially more comprehensive, reliable, and context aware solution for multi-verse Quranic passage retrieval.

[3] VCG: A Multimodal Retrieval Framework for E-Commerce Video Feeds under Extreme Cold-Start Conditions
The digital commerce landscape is shifting from static, search-driven catalogs to dynamic, immersive video feeds. This transition introduces an ``extreme cold-start'' problem: unlike traditional items, new short-form videos lack the dense interaction history required for collaborative filtering. Furthermore, immersive feeds introduce strong position and duration biases that distort standard engagement signals. In this paper, we demonstrate the Video Candidate Generation (VCG) system, a scalable multimodal retrieval engine designed to solve these challenges in a large-scale e-commerce environment. By leveraging a domain-adapted vision-language model (based on CLIP), we map users and videos into a shared semantic space, enabling zero-shot retrieval based on visual content rather than behavioral history. We detail the system's architecture and present a rigorous evaluation comparing generative (LLM) vs. discriminative (CLIP) embeddings. Our results show that while generative models excel at attribute prediction, they suffer from embedding space collapse in retrieval tasks. Online A/B testing demonstrates that VCG effectively mitigates engagement biases, yielding a 50\% uplift in deep video completion. To showcase the system's capabilities, we present an interactive demonstration featuring three bi-directional retrieval scenarios: Product-to-Video, Video-to-Product, and Zero-Shot Semantic Search.
```

---

## U100_046 — v2_train_r434_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `434`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

On how many QA benchmarks is Doc-to-Atom evaluated, and what advantages does it demonstrate over the Doc-to-LoRA baselines?

### Claim

It demonstrates advantages over the Doc-to-LoRA baselines by outperforming them while reducing the memory cost of document internalization.

### Evidence

```text
[1] Doc-to-Atom: Learning to Compile and Compose Memory Atoms
Long input sequences are central to document understanding and multi-step reasoning in Large Language Models, yet the quadratic cost of attention makes inference both memory-intensive and slow. Context distillation mitigates this by compressing contextual information into model parameters, and recent work such as Doc-to-LoRA amortizes context distillation into a single forward pass that generates one LoRA adapter per document. However, producing a single monolithic adapter for all queries leads to irrelevant-query interference, limited compositional recall, and poor scalability to long-document reasoning. To address these challenges, we propose Doc-to-Atom (Doc2Atom), a compositional parametric memory framework that decomposes each document into semantically typed knowledge atoms. Each atom is compiled into an independent micro-LoRA adapter and a provenance retrieval key. At inference time, a lightweight query router selects and assembles only the relevant atoms into a query-specific adapter, which is then injected into a frozen base model. The entire system is trained end-to-end through a multi-objective distillation framework. Experiments on six diverse QA benchmarks demonstrate that Doc2Atom outperforms Doc-to-LoRA baselines while reducing the memory cost of document internalization.

[2] Weaving Multi-Source Evidence for Biomedical Reasoning: The BioMedHop Benchmark and BioWeave Framework
Biomedical question answering (QA) increasingly requires reasoning over interacting entities, where supporting evidence is scattered across biomedical knowledge graphs, literature documents, and web-accessible resources. However, existing biomedical QA benchmarks mainly focus on exam-style knowledge, literature comprehension, or short-range multi-hop inference, leaving source-conditioned graph reasoning and evidence topology construction underexplored. To fill this gap, we introduce BioMedHop, a multi-source graph-grounded benchmark for evaluating biomedical reasoning over structured evidence topologies. BioMedHop contains 10,045 instances across KG, document, web, and hybrid evidence settings, covering shared-neighbor matching, intersection reasoning, path-based reasoning, and counting, with option-based, open-ended, and numeric count renderings. To support this benchmark, we further propose BioWeave, a source-aware reasoning framework that retrieves biomedical KG paths, gathers supporting clues from documents and web sources, assembles them into a unified evidence graph, and verifies answers through entity-level evidence support. Comprehensive experiments show that BioWeave achieves the best overall performance among compared methods on BioMedHop, outperforming the strong hybrid baseline ToG-2 by 10.5% in the overall average. Moreover, BioWeave consistently improves different LLM backbones and enables smaller models, such as Qwen3-4B, to achieve reasoning performance comparable to GPT-4-Turbo.

[3] EHRNote-ChatQA: A Benchmark for Evidence-Grounded Multi-Turn Clinical Question Answering over Longitudinal Discharge Summaries
Discharge summaries are crucial clinical documents containing the context of a patient's overall hospital stay, and are routinely reviewed by medical experts for patient readmission, ongoing care, and diagnostic decision-making. When reviewing them, medical experts often must iteratively synthesize information across multiple summaries while verifying the evidence supporting each answer. Although large language models (LLMs) are increasingly explored for clinical question answering, existing benchmarks do not sufficiently reflect this setting: they often evaluate exam-style medical knowledge or focus on single-turn question answering with limited evidence-grounding evaluation. We introduce EHRNote-ChatQA, the first benchmark for evidence-grounded multi-turn clinical question answering over patients' multiple discharge summaries. Built from de-identified MIMIC-IV discharge summaries, EHRNote-ChatQA contains 967 patient-level multi-turn samples spanning one to five notes and 16,072 medical-expert-verified QA pairs (8,036 content questions, each paired with an evidence-grounding question) across eight clinical categories. The benchmark is constructed through an expert-informed pipeline combining discharge-summary structuring schema, expert-curated multi-turn QA templates, and LLM-based generation, followed by review and revision of every single QA sample by 11 medical experts. Benchmarking 22 open- and closed-source LLMs reveals several challenges, including that LLMs struggle more with evidence grounding than content answering, multi-turn errors compound across turns, and single-turn clinical QA performance does not reliably transfer to this setting. These findings establish EHRNote-ChatQA as a rigorous and practical benchmark for evaluating clinical QA systems. The dataset will be made publicly available through PhysioNet credentialed access.
```

---

## U100_047 — v2_train_r119_plain_c001

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `119`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What did the paper find regarding the culture-neutrality of models' priors when interpreting time and quantity expressions?

### Claim

The paper does not directly address the culture-neutrality of models' priors when interpreting time and quantity expressions.

### Evidence

```text
[1] LLMs Infer Cultural Context but Fail to Apply It When Responding
Recent work has shown that LLMs overrepresent dominant cultures, particularly Western ones, while marginalizing others. We investigate whether this affects models' ability to generate culturally adapted responses by evaluating their use of local measurement units based on the user's perceived cultural background. We introduce Cultural and Pragmatic Response Inference (CAPRI), a dataset of conversations with varying levels of cultural cues. Experiments with state-of-the-art LLMs show that models can infer cultural background and recall relevant conventions, but often fail to utilize the information to adapt their answers to the relevant cultural conventions, unless explicitly prompted to perform the tasks sequentially. We further evaluate adaptation to the interpretation of time and quantity expressions, two subjective language grounding dimensions that are affected by culture. We find that models increasingly adapt their answers as cultural cues accumulate, but their priors are not culture-neutral, sometimes aligning with the model's country of origin. Overall, CAPRI provides a resource for future research aimed at narrowing the gap between cultural knowledge and culturally adaptive language generation.

[2] The Wrong Kind of Right: Quantifying and Localizing Misfired Alignment in LLMs
Warning: This paper studies stereotypes and biases, and contains potentially disturbing examples, used for illustration purposes only. Our findings should not be interpreted as an argument against alignment. Instead, this paper highlights the need for principled approaches to more advanced alignment. Alignment aims to ensure that large language models (LLMs) behave safely and reliably, including by avoiding unsafe inferences. However, we show that such safety-oriented behaviors can misfire: models may reject warranted conclusions even when they are explicitly supported by context. We call this failure mode misfired alignment, where alignment-induced changes cause LLMs to override explicit evidence. To quantify this phenomenon, specifically on stereotype-related alignment, we introduce VETO, a benchmark consisting of 2,032 BBQ-derived contrastive pairs, and define a new metric, Misfired Alignment Rate (MAR), which measures on a 0 to 100 scale how often a model fails on a stereotype-related question but succeeds on its contrastive counterpart. We benchmark 25 LLMs on VETO, and show that all LLMs, including the most recent ones, exhibit non-trivial (4.7 to 18.9%) MARs while all human participants achieve 0.0% MAR. Controlled priming experiments further show that alignment-induced cues can substantially amplify MAR across LLMs, indicating that these failures are not merely artifacts of individual examples but can be induced by safety-related framing. Mechanistic analyses on open-weight LLMs reveal late-layer suppression of evidence-supported answers, and comparisons between instruct and base LLMs suggest that this suppression emerges after instruction training. These findings show that current alignment methods can overgeneralize surface-level safety cues, to the point of overriding objective evidence, motivating more work on alignment objectives that better preserve contextual grounding.

[3] From Awareness to Adherence: Bridging the Context Gap in Spoken Dialogue Systems via Context-Aware Decoding
Despite the success of end-to-end (E2E) spoken dialogue systems, maintaining strict context adherence in multi-round conversations remains a challenge. While prior works attribute these failures to models forgetting dialogue history, we highlight an equally critical but overlooked bottleneck: a gap between latent context awareness and active adherence. Although models internally recognize relevant past utterances, strong parametric priors often overshadow these signals during decoding. To bridge this gap, we propose an audio-adapted Context-Aware Decoding (CAD) approach. By leveraging internal attention mechanisms to isolate key historical rounds, our approach contrasts output distributions with and without this key context during inference, directly amplifying multimodal contextual signals. Evaluations on the Audio MultiChallenge benchmark demonstrate significant improvements in Semantic Memory and Self Coherence subtasks, successfully enforcing strict, context-faithful adherence.
```

---

## U100_048 — v2_train_r270_cited_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `270`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three agents integrated into the proposed LLM-driven framework, and what is the specific function of each?

### Claim

The three agents integrated into the proposed LLM-driven framework are: 1.

### Evidence

```text
[1] Risk-Aware LLM Agents for Geospatial Data Retrieval: Design and Preliminary Adversarial Evaluation
We present an LLM-driven framework for retrieving remote sensing data from cloud-based geospatial catalogues using natural language queries. The system converts user intent into structured API calls, enabling efficient access to satellite imagery and environmental datasets. The architecture integrates three agents: Guardrail for safety and policy enforcement, General-QA for intent interpretation, and Recommender-Analyst for schema-aware API call generation. This coordinated design ensures reliable, semantically aligned interaction with external data services. The modular framework is portable across platforms through API schema substitution and supports applications in environmental monitoring, disaster response, and climate analysis. It establishes a scalable interface between user intent and geospatial infrastructure, enabling streamlined and automated Earth observation workflows. Preliminary experiments under adversarial multi-turn settings show that prompt-level safety instructions improve robustness, although rare high-impact failures persist in API manipulation scenarios and highlight the need for adaptive, system-level defenses that balance safety, usability, and cost efficiency, which motivates the use of our intercept-level Guardrail agent.

[2] ACCORD: Action-Conditioned Contextual Grounding for Language Agents
User instructions are often underspecified because humans rely on implicit assumptions about the surrounding environment. For large language model (LLM) agents operating in information-rich digital and physical environments, these assumptions cannot be inferred from the instruction alone; they must be recovered from the current state of tools, data, interfaces, and observations. Effective execution therefore requires agents to identify missing context, ground it in observed evidence, and carry it forward into subsequent actions. We show that current agents often fail to do so. They act from assumed rather than observed specifics, overlook information they could have gathered, and fail to incorporate evidence that has already been returned. Building on this insight, we propose ACCORD (Action-Conditioned Contextual Grounding), a simple and effective agent framework for adaptive grounding. Before each action, ACCORD actively probes the environment for missing information and integrates relevant context from the agent's trajectory that would otherwise be overlooked. Requiring no additional training or task-success signals, ACCORD improves task-goal completion on AppWorld by up to +20.6 points with GPT-5-mini, from 42.0% to 62.6%, compared to strong baselines. These gains persist with a substantially stronger base model (+10.8 with Claude-4.5-sonnet), an open-weight model (+10.1 with Qwen3.5-27B-FP8), and on the embodied AlfWorld benchmark (+7.4 success rate with GPT-5-mini).

[3] VeriGraph: Towards Verifiable Data-Analytic Agents
LLM-based agents have demonstrated strong capabilities in data-intensive analytical tasks, yet their outputs are rarely verifiable: a reliance on linear text trajectories makes their reasoning difficult to audit. In particular, deterministic computations over raw data and semantic deductions over natural-language claims are often entangled in an unstructured stream, leaving numerical conclusions hard to reproduce and qualitative judgments hard to inspect. To address this, we propose VeriGraph, a traceable neuro-symbolic reasoning framework that enables agents to construct an explicit heterogeneous evidence directed acyclic graph (DAG) during execution. VeriGraph introduces three evidence-expansion primitives, namely computational, grounding, and derivational expansion, to connect raw data, interpreter variables, computed results, and natural-language claims in a unified graph. Under this formulation, structural traceability is reduced to graph reachability from raw data sources to terminal claims, while semantic support is measured by claim-level evidence evaluation. To improve graph construction, we further design a graph-based policy optimization strategy with a composite reward that jointly supervises answer correctness, computational integrity, and derivational coherence. Experiments on four benchmarks show that VeriGraph-8B achieves the highest overall score among all baselines. More importantly, VeriGraph produces auditable evidence graphs with substantially stronger claim grounding, achieving a 87.61\% Grounding Rate under our claim-level evidence support evaluation. These results suggest that explicit evidence-graph construction is a promising path toward verifiable data-analytic agents. Our code is available at https://github.com/ignorejjj/VeriGraph.
```

---

## U100_049 — v2_train_r45_plain_c006

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `45`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the seven levels of contextual signals introduced in the prompting framework, including the types of adversarial prompts used?

### Claim

Level 5, 6, and 7 are not explicitly mentioned in the source, but it can be inferred that they likely involve more complex and challenging contextual inputs.

### Evidence

```text
[1] IndicContextEval: A Benchmark for Evaluating Context Utilisation in Audio Large Language Models Across 8 Indic Languages
AudioLLMs enable speech recognition conditioned on textual prompts such as domain descriptions or entity lists. However, it remains unclear whether these models genuinely utilise such context or rely on parametric knowledge learned during pretraining. Existing benchmarks cannot answer this question because they evaluate transcription under fixed prompting conditions and rarely include explicit contextual inputs. We introduce IndicContextEval, a 56-hour multilingual benchmark of natural speech from 555 speakers across 8 Indian languages and 23 professional domains. We design a 7-level prompting framework that progressively introduces contextual signals, including metadata, natural-language descriptions, entity lists in English and native script, and adversarial prompts with incorrect entities. Evaluating five models reveals substantial differences in context utilisation behaviour, highlighting the need for explicit evaluation of contextual grounding in AudioLLMs.

[2] GRACE: Step-Level Benchmark for Faithful Reasoning over Context
Many reasoning tasks require models to reason over input context, from document-grounded question answering to rule-based deduction. Chain-of-Thought (CoT) prompting produces traces that appear transparent, yet individual steps can silently deviate from the source evidence, even when the final answer is correct. Existing methods detect hallucinations at the response level but fail to identify where in the chain a failure occurs or what type it is. We introduce GRACE, the first human-annotated step-level faithfulness benchmark with a data-driven error taxonomy for context-grounded textual reasoning. GRACE covers CoT traces from 10 models across 4 source datasets, with each step annotated for faithfulness, error category, and natural language explanation. A data-driven taxonomy, discovered bottom-up via unsupervised clustering, organizes failures into two tracks: GRACE-Inference (deductive errors) and GRACE-Grounding (factual grounding errors), with four categories each. The evaluation set is human-annotated and challenging by design. Our experiments reveal substantial headroom for current models. In addition, integrating step-level faithfulness signals into reinforcement learning pipelines improves both downstream accuracy and reasoning reliability.

[3] SICI: A Semantic-Pragmatic Complexity Index Reveals Regime Shifts in LLM Stance Detection
Prompt-based LLMs are increasingly used for stance detection, but harder examples are not always repaired by clearer instructions, reasoning prompts, retrieval, or debate. We introduce SICI (Stance Inference Complexity Index), a seven-dimensional diagnostic measure of the semantic-pragmatic burden imposed by a target--text pair. Across SemEval-2016 and VAST, SICI predicts LLM accuracy better than surface proxies and shows substantial cross-scorer reliability ($α=0.771$). More importantly, LLM errors change regime as SICI increases: low-complexity examples invite over-attribution, especially Against predictions; intermediate examples form an unstable boundary; and high-complexity examples rapidly concentrate on None. This phase-transition-like structure persists across GPT-3.5, GPT-4o-mini, DeepSeek-V3, and GPT-4o, although stronger models move the boundaries. A 15-method intervention study further shows that prompting, retrieval, and debate often shift models along the attribution--abstention axis rather than removing the high-complexity bottleneck.
```

---

## U100_050 — v2_train_r62_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `62`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

Which large-norm backbone encoders does the paper report as being improved by the proposed rescaling correction, and how do the corrected models compare to the BERT-SPLADE baseline?

### Claim

In several settings, the corrected models further match or surpass the classic BERT-SPLADE baseline.

### Evidence

```text
[1] Rescaling MLM-Head for Neural Sparse Retrieval
Learned sparse retrieval (LSR) models such as SPLADE have traditionally used BERT-style masked language models as backbone encoders. A natural expectation is that replacing BERT with stronger pretrained encoders should improve retrieval effectiveness. However, we find that under standard SPLADE training recipes, backbones with large MLM-head L2 norms can suffer performance degradation and even training collapse under standard SPLADE training recipes. We identify this failure as a scale mismatch in the MLM head: SPLADE directly uses MLM-head outputs to construct sparse lexical representations, and query-document relevance is computed by an unnormalized dot product over these representations. As a result, an inflated MLM-head scale can amplify sparse activations, distort matching scores, and destabilize contrastive training under common training settings. To address this issue, we introduce a simple initialization-time correction that rescales the MLM-head projection by a constant factor before SPLADE training. This zero-cost adjustment improves training stability without modifying the model architecture or training objective. Across both in-domain and out-of-domain retrieval benchmarks, this simple correction substantially improves large-norm backbones such as ModernBERT and Ettin, turning unstable training runs into competitive sparse retrievers. In several settings, the corrected models further match or surpass the classic BERT-SPLADE baseline. These findings suggest that the bottleneck in adapting pretrained encoders to LSR is not encoder capacity alone, but the calibration of the MLM-head scale used to construct sparse lexical representations.
```

---

## U100_051 — v2_train_r171_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `171`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

By how many points does gold-at-first outperform gold-at-last across every reader-by-benchmark cell in the multimodal KB-VQA experiments?

### Claim

This effect is referred to as "Lost at the End" in the source.

### Evidence

```text
[1] Lost at the End: Primacy Bias in Multimodal Retrieval-Augmented Question Answering
Knowledge-based visual question answering (KB-VQA) lets vision-language systems answer questions that exceed their parametric knowledge by conditioning a reader on passages retrieved from a Wikipedia-scale knowledge base. In pure-text long-context LLMs, retrieved-context use follows the U-shaped "lost-in-the-middle" effect of Liu et al. (2024): information at the start and end of context is used, the middle is lost. Whether this transfers to deployed multimodal KB-VQA is open. To close this gap, we design the first controlled probe of reader-side position dependence in multimodal KB-VQA: a gold-position protocol in which only the gold passage's prompt slot varies within question. We run it on three open-source 7B/8B VLM readers and two KB-VQA benchmarks at k up to 20. The shape flips from U to primacy: gold-at-first beats gold-at-last by 16 to 26 points on every reader-by-benchmark cell, an effect we call "Lost at the End". Three targeted ablations narrow the cause: a text-only control shows the multimodal setting amplifies an already-present text-mode primacy 2.2 to 4.5 times, and image-position and distractor-shuffle ablations together pin the locus to prompt slot 0 of the instruction-tuned reader. On a frozen reader, three retrieval-side fixes (MMR, oracle reranking, rank-based reordering) all leave the gap intact (no separable improvement). Our findings indicate that recall@k is the wrong metric for deployed KB-VQA and that closing the gap requires reader-side intervention; we release our protocol as a controlled instrument for evaluating such interventions.

[2] When Correct Edges Cannot Be Verified: A Provenance Gap in Incomplete KGQA and a Provenance-Favoring Completion Policy
Incomplete Knowledge Graph Question Answering (IKGQA) requires completing missing edges to continue reasoning. A growing line of work verifies completed edges against retrieved text, treating textual support as a proxy for edge quality. We ask a question that, to our knowledge, has not been systematically tested: does textual verifiability actually track correctness? Exploiting the gold deleted triples provided by the standard random-deletion protocol, we measure both. The finding is counterintuitive: among gold-correct completed edges, 76-96% have no supporting passage even under exhaustive retrieval, robustly across deletion rates (20%/40%), datasets (CWQ/WebQSP), and relation types (structural, commonsense, long-tail). Most Freebase-style facts simply do not occur as head-tail co-mentions in text. Textual faithfulness therefore measures provenance, not correctness -- separated by a paradigm-level gap no in-corpus retrieval closes. This reframes edge completion. Since most completed edges -- correct or not -- are causally redundant for the answer (95-97% of correct answers do not depend on any unsupported edge), the central question shifts from "is the edge correct?" to "admit or abstain under provenance uncertainty?" Within this framing we present TGComplete, a provenance-favoring admission policy that retrieves evidence at a reasoning breakpoint, verifies a candidate through a lightweight loop, and abstains when support is absent. Against the generate-to-complete baseline GoG, it attains higher edge precision against gold (15-21% vs 3-14%), with no statistically detectable EM loss and 3.1-7.4 times higher strict faithfulness of admitted edges -- at the cost of lower recall. We position TGComplete not as uniformly better, but as a principled point on a precision/provenance-recall trade-off, appropriate when auditability matters.

[3] Prior over Evidence: Stereotype-Driven Diagnosis in LLM-Based L2 Pronunciation Feedback
Large language models are increasingly deployed for written pronunciation feedback in second-language (L2) English learning, under the assumption that their diagnoses are grounded in the supplied speech evidence rather than in priors from pretraining. This assumption is tested on 1,800 L2-Arctic utterances spanning six L1 backgrounds, three audio-capable LLMs, four pronunciation dimensions, and five evidence conditions ranging from a text-only baseline to numeric acoustic features and raw audio. Each (utterance x model x condition x dimension) cell is scored on three metrics: Rating Accuracy (RA) against gold labels, Evidence Coherence (EC) assessing internal consistency without ground truth, and Grounded Correctness (GC) evaluated against gold evidence. Results show three findings across models. First, rating accuracy and grounded reasoning decouple: 39.6% of judged cells contain internally coherent reasoning that supports a wrong rating, against only 15.8% where the reasoning supports a correct rating. Second, phoneme-level feedback converges to a fixed inventory of L2-English difficulty phones that recurs across all six L1 backgrounds and all evidence conditions. Third, acoustic evidence improves the rating only when the supplied feature directly probes the target dimension: textualised F0 range raises pitch-variation grounding from (0.18-0.19) to (0.45-0.62) across all three models, while stress and phoneme correctness, which require target-to-realisation alignment, remain ungrounded. The same audio waveform without textualised F0 values does not reproduce this improvement. These findings indicate that current general-purpose LLMs are more reliable as verbalisers of externally computed pronunciation evidence than as standalone diagnostic engines.
```

---

## U100_052 — v2_train_r165_cited_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `165`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What analogy does SkillWiki draw between existing infrastructures like Wikipedia and GitHub and the gap it aims to fill for agent skills?

### Claim

SkillWiki draws an analogy between existing infrastructures like Wikipedia and GitHub and the gap it aims to fill for agent skills by likening knowledge and software to agent skills.

### Evidence

```text
[1] SkillWiki: A Living Knowledge Infrastructure for Agent Skills
While knowledge is managed through Wikipedia and software through GitHub, agent skills still lack an infrastructure for large-scale production, governance, and evolution. SkillWiki is a living knowledge infrastructure that supports the organization, grounding, and continuous evolution of agent skills by transforming heterogeneous knowledge into reusable skill assets linked to their originating evidence. Our demonstration presents the complete skill lifecycle, from knowledge ingestion and skill production to provenance-aware exploration, governance, and execution-driven evolution. SkillWiki highlights a future in which knowledge, skills, and execution experience co-evolve within a shared infrastructure. The live demonstration and source code are publicly available at https://github.com/Huangdingcheng/SkillWiki.

[2] Beyond Domains: Reusing Web Skills via Transferable Interaction Patterns
Large language model (LLM) web agents are usually deployed as tool callers: each turn, the model reads a fresh page observation and emits one structured tool action. When every action is a low-level primitive, horizons grow quickly and so do policy-facing LLM completions, dominating latency and cost on benchmarks such as Mind2Web and WebArena. Recent systems therefore wrap repeated interaction fragments as web skills: callable tools built from successful trajectories or induced programs, so one call can replace several primitives. However, prior skill libraries are still triggered mainly by instruction similarity or coarse site metadata, which yields low skill reuse on held-out sites and leaves much of the potential step and token reduction on the table. We present SkillMigrator, an agent that learns reusable web skills and transfers them across sites by matching layout structure rather than specific element references. Each induced skill is stored as a transferable interaction pattern (TIP): the skill paired with a structural sketch of the snapshot at induction time. At test time, SkillMigrator retrieves TIPs by layout similarity and grounds their references on the live page. The rest of the stack is standard: accessibility-snapshot observations with stable references, and fixed tool calling over primitives plus skill invocations. Compared with the state-of-the-art approaches, SkillMigrator reduces the average LLM-action count on successful trajectories by 8-10% across both WebArena and Mind2Web at matched success rate.

[3] Compositional Skill Routing for LLM Agents: Decompose, Retrieve, and Compose
LLM agents increasingly rely on external skills -- reusable tool specifications -- but real-world tasks often require composing multiple skills, not just selecting one. We formalize this as the Compositional Skill Routing problem: given a complex user query and a large skill library, decompose the query into atomic sub-tasks, retrieve the appropriate skill for each sub-task, and compose an executable plan. We present SkillWeaver, a decompose-retrieve-compose framework combining an LLM task decomposer, a bi-encoder skill retriever with FAISS indexing, and a dependency-aware DAG planner. To support evaluation, we introduce CompSkillBench, a benchmark of 300 compositional queries over 2,209 real MCP server skills spanning 24 functional categories, sourced from the public MCP ecosystem. Our experiments reveal that task decomposition quality is the primary bottleneck: standard LLM decomposition reaches only 34.2% category recall at the step level. To address this, we propose Iterative Skill-Aware Decomposition (SAD), a retrieval-augmented feedback loop that iteratively aligns decomposition with available skills. SAD improves decomposition accuracy from 51.0% to 67.7% (+32.7%, Wilcoxon p < 10^-6) in a single iteration; DA-conditioned analysis confirms that correct granularity is the prerequisite for effective retrieval (CatR@1 rises from 34% to 41% when DA=1). SkillWeaver reduces context window consumption by over 99%, and transfer experiments confirm generalization (+35.6% relative DA gain even when target categories are absent from the retrieval pool).
```

---

## U100_053 — v2_train_r458_cited_c001

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `458`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

Which four graph datasets does the HyperGNN paper evaluate on, and what node classification accuracy does it report on ogbn-arxiv?

### Claim

I could not find the HyperGNN paper in the provided sources.

### Evidence

```text
[1] Intelligent Multimodal Retrieval and Reasoning for Geospatial Knowledge Discovery on the I-GUIDE Platform
Geospatial knowledge discovery increasingly requires search across heterogeneous artifacts: datasets, maps, notebooks, software, publications, and the provenance links among them. Conventional geoportals support metadata and spatial filtering, but they rarely provide semantic retrieval, graph-aware provenance traversal, and conversational synthesis in one integrated system. This paper presents I-GUIDE Smart Search, a production multimodal geospatial retrieval-augmented generation (RAG) system embedded in the I-GUIDE Platform, and reports on its design, deployment, and evaluation. The system combines production-maintained OpenSearch keyword, vector, and spatial indexes with a Neo4j knowledge graph and an iterative RAG pipeline for memory-aware query augmentation, reasoning, retrieval-method routing, relevance grading, grounded generation, hallucination and relevance checking. In a single-A100 RAG deployment, I-GUIDE Smart Search supports interactive use up to about 100 concurrent simulated users, reaching 4.4 requests per second with p50 latency near 25 seconds despite 20-50 LLM calls per query. For answer quality, we evaluate a four-category benchmark of 170 unique human-filtered user-facing queries, together with ten intent-specific probe sets generated from the deployed indexes and graph. Smart Search improves retrieved evidence coverage and judged answer quality over non-retrieval and naive-RAG baselines, with the clearest gains on exact-identifier, spatially constrained, simple-recommendation, and domain-specific factual queries requiring current indexed evidence. We distill transferable deployment lessons for spatial RAG systems, covering spatial metadata quality, graph provenance, retrieval routing, interface contracts, refusal-aware evaluation, latency-cost tradeoffs, and the role of the user interface in deployed geospatial cyberinfrastructure.

[2] MAGE-RAG: Multigranular Adaptive Graph Evidence for Agentic Multimodal RAG in Long-Document QA
Long-document multimodal question answering requires a system to locate sparse evidence in long PDFs and integrate clues from text, tables, images, charts, and complex layouts. Existing RAG methods mostly rely on fixed Top-k retrieval over text chunks or pages. Text retrieval can compress the context but often loses visual and layout information; page-level visual retrieval preserves the original page, yet it also sends large irrelevant regions to the reader, leading to a static trade-off among evidence coverage, noise, and inference cost. This paper proposes MAGE-RAG, a multigranular adaptive graph evidence framework for long-document multimodal QA. MAGE-RAG uses page retrieval as the entry point for query-time evidence construction. Offline, it builds an evidence graph with page nodes and element nodes, encoding containment, reading order, layout adjacency, section hierarchy, and semantic-neighbor relations. At query time, an online evidence controller iteratively activates, opens, searches, and prunes evidence under explicit budgets. The resulting evidence subgraph is then rendered into structured multimodal reader input, allowing the LVLM to consume compact and relevant evidence within a limited context. On LongDocURL and MMLongBench-Doc, we establish a unified comparison and analysis protocol covering Direct MLLM, Text RAG, Page-level Visual RAG, and Graph/Agentic RAG. Experiments show that MAGE-RAG achieves 52.75 overall accuracy on LongDocURL, and 53.26 accuracy with 51.19 F1 on MMLongBench-Doc. Fine-grained breakdowns, budget-performance curves, ablations, and trace-based analysis further show that query-time evidence subgraph construction can balance dispersed evidence coverage with context-noise control. Our code is available at https://github.com/laonuo2004/MAGE-RAG.git.

[3] MVEB: Massive Video Embedding Benchmark
We introduce the Massive Video Embedding Benchmark (MVEB), a 23-task benchmark for video embeddings spanning classification, zero-shot classification, clustering, pair classification, retrieval, and video-centric question answering. We evaluate 33 models and find that no single model dominates: MLLM-based embeddings lead on classification, clustering, pair classification, and QA; multimodal binding leads on retrieval and zero-shot classification; generative MLLMs without contrastive adaptation collapse on cross-modal tasks. Paired video-only vs. audio+video evaluations show that audio's contribution depends on dataset annotation provenance: audio helps when labels were produced from both modalities and hurts when they were produced from visuals alone, a six-point gap consistent across model families. MVEB is derived from MVEB+, a 184-task pool, and is designed to maintain task diversity while reducing evaluation cost. It integrates into the MTEB ecosystem for unified evaluation across text, image, audio, and video. We release MVEB and all 184 tasks along with code and a leaderboard at https://github.com/embeddings-benchmark/mteb.
```

---

## U100_054 — v2_train_r233_cited_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `233`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What key challenges did benchmarking 22 open- and closed-source LLMs reveal about their performance on evidence-grounded multi-turn clinical question answering?

### Claim

The key challenges revealed about the performance of 22 open- and closed-source LLMs on evidence-grounded multi-turn clinical question answering are: 1.

### Evidence

```text
[1] EHRNote-ChatQA: A Benchmark for Evidence-Grounded Multi-Turn Clinical Question Answering over Longitudinal Discharge Summaries
Discharge summaries are crucial clinical documents containing the context of a patient's overall hospital stay, and are routinely reviewed by medical experts for patient readmission, ongoing care, and diagnostic decision-making. When reviewing them, medical experts often must iteratively synthesize information across multiple summaries while verifying the evidence supporting each answer. Although large language models (LLMs) are increasingly explored for clinical question answering, existing benchmarks do not sufficiently reflect this setting: they often evaluate exam-style medical knowledge or focus on single-turn question answering with limited evidence-grounding evaluation. We introduce EHRNote-ChatQA, the first benchmark for evidence-grounded multi-turn clinical question answering over patients' multiple discharge summaries. Built from de-identified MIMIC-IV discharge summaries, EHRNote-ChatQA contains 967 patient-level multi-turn samples spanning one to five notes and 16,072 medical-expert-verified QA pairs (8,036 content questions, each paired with an evidence-grounding question) across eight clinical categories. The benchmark is constructed through an expert-informed pipeline combining discharge-summary structuring schema, expert-curated multi-turn QA templates, and LLM-based generation, followed by review and revision of every single QA sample by 11 medical experts. Benchmarking 22 open- and closed-source LLMs reveals several challenges, including that LLMs struggle more with evidence grounding than content answering, multi-turn errors compound across turns, and single-turn clinical QA performance does not reliably transfer to this setting. These findings establish EHRNote-ChatQA as a rigorous and practical benchmark for evaluating clinical QA systems. The dataset will be made publicly available through PhysioNet credentialed access.

[2] Weaving Multi-Source Evidence for Biomedical Reasoning: The BioMedHop Benchmark and BioWeave Framework
Biomedical question answering (QA) increasingly requires reasoning over interacting entities, where supporting evidence is scattered across biomedical knowledge graphs, literature documents, and web-accessible resources. However, existing biomedical QA benchmarks mainly focus on exam-style knowledge, literature comprehension, or short-range multi-hop inference, leaving source-conditioned graph reasoning and evidence topology construction underexplored. To fill this gap, we introduce BioMedHop, a multi-source graph-grounded benchmark for evaluating biomedical reasoning over structured evidence topologies. BioMedHop contains 10,045 instances across KG, document, web, and hybrid evidence settings, covering shared-neighbor matching, intersection reasoning, path-based reasoning, and counting, with option-based, open-ended, and numeric count renderings. To support this benchmark, we further propose BioWeave, a source-aware reasoning framework that retrieves biomedical KG paths, gathers supporting clues from documents and web sources, assembles them into a unified evidence graph, and verifies answers through entity-level evidence support. Comprehensive experiments show that BioWeave achieves the best overall performance among compared methods on BioMedHop, outperforming the strong hybrid baseline ToG-2 by 10.5% in the overall average. Moreover, BioWeave consistently improves different LLM backbones and enables smaller models, such as Qwen3-4B, to achieve reasoning performance comparable to GPT-4-Turbo.

[3] AIPatient Arena: EHR-grounded evaluation of large language models in end-to-end clinical consultation workflows
Large language models (LLMs) are increasingly considered for use in clinical consultation tasks, yet most medical evaluations remain static, single-turn, or narrowly outcome-based, limiting their ability to reflect the sequential, uncertain, and interactive nature of real-world care. Here, we propose AIPatient Arena, an EHRs-grounded evaluation framework for assessing the clinical utility of LLMs across eight dimensions of clinical competence. The framework integrates EHR data into patient-specific knowledge graphs, enabling multi-turn physician-patient interactions. We applied AIPatient Arena on a primary cohort of 437 patients and two out-of-distribution validation cohorts of 119 and 67 patients. We observe that LLMs performed well in medical interview questioning skills (QS; mean scores, 4.43-4.99/5), ethical and professional conduct (ET; 4.38-4.93/5), and clarity and transparency of clinical explanations (EX; 3.80-4.72/5). Performance was moderate in information integration (II; 3.19-4.21/5) and medication safety and justification (MS; 3.13-3.78/5), but persistent weaknesses were observed in handling of ambiguous patient responses (HR; 2.57-3.32/5), information coverage (IC; 2.08-3.02/5), and diagnostic accuracy and reasoning (Dx; 2.63-3.55/5). Process-based evaluation revealed recurrent interaction failures, including repetitive questioning, omission of past medical history, and inadequate handling of uncertainty. Richer conversational context improved diagnostic reasoning but yielded limited gains in treatment planning. These findings indicate that final-answer accuracy alone is insufficient for evaluating clinical readiness and highlight the importance of assessing how models gather, interpret, and communicate information throughout a consultation. AIPatient Arena provides an EHR-grounded framework for workflow-oriented pre-deployment evaluation of medical LLMs.
```

---

## U100_055 — v2_train_r377_cited_c004

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `377`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What structural components make up the worlds generated by IVIE, and what architecture are they organized around?

### Claim

However, the specific structural components of the executable reasoning process in TGEO, as described in source, are different and not directly related to the worlds generated by IVIE.

### Evidence

```text
[2] Theorem-Grounded Execution Ontologies for Interpretable Machine Reasoning
Large language models have achieved impressive performance on reasoning tasks spanning mathematics, science, programming, and commonsense inference. Despite these advances, their reasoning processes remain largely latent, making them difficult to interpret, verify, replay, debug, and transfer across domains. Existing approaches such as chain-of-thought, tree-of-thoughts, graph-of-thoughts, and tool-augmented reasoning expose intermediate reasoning artifacts but typically lack explicit execution semantics, formal state representations, and verifiable reasoning structures. We introduce Theorem-Grounded Execution Ontologies (TGEO), a framework that models reasoning as an executable state-transition process rather than a sequence of generated tokens. Given an input problem, TGEO identifies relevant theorem families, binds the problem to a domain ontology, discovers semantic objects, instantiates states and operators, constructs predicates and contracts, and synthesizes an executable reasoning graph. The resulting graph provides an interpretable, replayable, and auditable representation of reasoning in which every state transition, operator application, and validation step is explicitly represented. TGEO integrates five architectural components: (1) theorem-grounded reasoning priors, (2) executable ontologies, (3) operator-mediated state transitions, (4) predicate and contract-based execution validation, and (5) architectural auditing and failure localization. We evaluate TGEO on theorem-intensive reasoning tasks derived from mathematical benchmark domains and a curated Golden Execution Suite. Our findings demonstrate the value of executable reasoning representations for interpretable, verifiable, and reproducible AI reasoning systems.
```

---

## U100_056 — v2_train_r208_cited_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `208`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What are the five distinct roles that code can play in a task according to the survey's formulation?

### Claim

The survey formulation identifies five distinct roles that code can play in a task: 1.

### Evidence

```text
[1] Beyond NL2Code: A Structured Survey of Multimodal Code Intelligence
While Large Language Models (LLMs) have substantially advanced text-to-code synthesis, many real programming tasks specify intent through visual artifacts such as screenshots, charts, vector drawings, videos, and interactive states. These tasks require models to connect visual perception to executable programs, because correctness depends not only on syntax but also on layout, data semantics, interaction behavior, and domain-specific constraints that apply after execution. This survey examines Multimodal Code Intelligence, covering systems that generate, edit, refine, or reason with code under visually grounded inputs and outputs. We first formulate the field by the role that code plays in each task, distinguishing code as a rendered artifact, an editable symbolic structure, a scientific representation, an intermediate reasoning trace, or an executable policy or tool interface. We then organize benchmarks and methods into four domains: Graphical User Interface, Scientific Visualization, Structured Graphics, and Frontier Tasks and Frameworks. This taxonomy connects mature artifact-generation problems to emerging agentic and unified settings and allows us to compare how different tasks treat evidence of correctness. Looking ahead, we argue that future research may benefit from four verification-centered directions. Multi-signal validation can combine complementary evidence of correctness, multi-state verification can test behavior across execution trajectories, cross-task transfer testing can probe reusable visual-code skills, and verifiable agent traces can reveal whether agent actions are grounded in visual evidence. Together, these directions may move this field from single-output imitation toward evidence-grounded executable systems. An ongoing project and resources are available on \href{https://github.com/xjywhu/Awesome-Multimodal-LLM-for-Code}{GitHub}.
```

---

## U100_057 — v2_train_r375_cited_c005

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `375`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the four stages of IVIE's incremental generation pipeline, and which tasks are delegated to LLMs versus symbolic validation?

### Claim

Regarding the delegation of tasks, creative decisions are handled by LLMs, while symbolic validation is responsible for grounding the world state.

### Evidence

```text
[1] IVIE: A Neuro-symbolic Approach to Incremental and Validated Generation of Interactive Fiction Worlds
Computational creativity in Interactive Fiction faces a fundamental tension: Large Language Models (LLM) may produce creative narratives but struggle with world coherence, while symbolic systems ensure consistency but lack creative flexibility. We present IVIE (Incremental & Validated Interactive Experiences), a neuro-symbolic approach to generating complete and playable interactive fiction worlds from scratch. Building upon PAYADOR's neuro-symbolic framework, IVIE implements a four-stage incremental generation pipeline that delegates creative decisions--setting and character creation, puzzle design--to LLMs while grounding the world state through symbolic validation. The system generates worlds with interconnected locations, functional items, non-player characters, and coherent puzzles, all structured around a central goal-oriented architecture. Human evaluation shows the approach generates immersive, thematically coherent worlds with high player engagement. Results seem to indicate that the neuro-symbolic approach successfully balances flexibility with narrative coherence: symbolic validation grounds LLM generation without eliminating generative freedom. However, challenges remain: LLM inconsistencies occasionally bypass puzzle constraints, and objective validation gaps allow some structurally impossible goals. We identify key design considerations for future neurosymbolic interactive storytelling systems, particularly regarding LLM capabilities and their limitations.

[2] Beyond NL2Code: A Structured Survey of Multimodal Code Intelligence
While Large Language Models (LLMs) have substantially advanced text-to-code synthesis, many real programming tasks specify intent through visual artifacts such as screenshots, charts, vector drawings, videos, and interactive states. These tasks require models to connect visual perception to executable programs, because correctness depends not only on syntax but also on layout, data semantics, interaction behavior, and domain-specific constraints that apply after execution. This survey examines Multimodal Code Intelligence, covering systems that generate, edit, refine, or reason with code under visually grounded inputs and outputs. We first formulate the field by the role that code plays in each task, distinguishing code as a rendered artifact, an editable symbolic structure, a scientific representation, an intermediate reasoning trace, or an executable policy or tool interface. We then organize benchmarks and methods into four domains: Graphical User Interface, Scientific Visualization, Structured Graphics, and Frontier Tasks and Frameworks. This taxonomy connects mature artifact-generation problems to emerging agentic and unified settings and allows us to compare how different tasks treat evidence of correctness. Looking ahead, we argue that future research may benefit from four verification-centered directions. Multi-signal validation can combine complementary evidence of correctness, multi-state verification can test behavior across execution trajectories, cross-task transfer testing can probe reusable visual-code skills, and verifiable agent traces can reveal whether agent actions are grounded in visual evidence. Together, these directions may move this field from single-output imitation toward evidence-grounded executable systems. An ongoing project and resources are available on \href{https://github.com/xjywhu/Awesome-Multimodal-LLM-for-Code}{GitHub}.

[3] Source-Grounded Data Generation for Text-to-JSON Learning
From financial filings to clinical records, legacy industries rely heavily on long, unstructured documents to store high-value information. Reliably extracting this information into structured, machine-readable representations is a key prerequisite to making the contents accessible to automated systems. JSON is a natural target for such structured extraction, yet constructing reliable and scalable text-to-JSON training data remains challenging. To address this gap, we propose STAGE (Spreadsheet-grounded Text-to-JSON Artifact GEneration), a source-grounded data generation pipeline that constructs reports and JSON schema by using LLMs for scalable synthesis while validating ground-truth values against the underlying spreadsheet. Evaluations on STAGE-Eval, our source-grounded benchmark with an 851-example test set, show that STAGE produces stronger training data than existing approaches. This improves Qwen3-4B exact match from 31.37% to 74.27% and value accuracy from 45.46% to 90.69%.
```

---

## U100_058 — v2_train_r6_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `6`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What limitations of existing counterspeech datasets addressing the overlap of hate and misinformation does the paper identify?

### Claim

The paper identifies several limitations of existing counterspeech datasets addressing the overlap of hate and misinformation.

### Evidence

```text
[1] CATCH-ME if you RAG: a dataset of Contextually Annotated multi-Turn Counterspeech against Hate and Misinformation Exchanges
Online hate speech and misinformation frequently overlap, yet NLP research has mainly treated them in isolation. While LLMs represent a scalable solution for assisting humans in the generation of counterspeech for both threats, zero-shot models frequently generate repetitive and vague responses, underscoring the need for high-quality examples to steer model generation. However, existing counterspeech datasets against the overlap of hate and misinformation are scarce and limited to single-turn English dialogues, while real-life interactions span across multiple turns and languages. To bridge this gap, we introduce the first large-scale, expert-curated, multilingual dataset of dialogues tackling the intersection of hate and misinformation. To ensure factual grounding, the dialogues are also anchored in verified external knowledge (i.e., fact-checking articles and NGO reports) and include document- and chunk-level span annotations, making it directly applicable for RAG systems. Covering five languages and targeting hate directed at seven marginalized groups, this novel resource enables the training and evaluation of more persuasive, factually grounded counterspeech models.

[2] The Wrong Kind of Right: Quantifying and Localizing Misfired Alignment in LLMs
Warning: This paper studies stereotypes and biases, and contains potentially disturbing examples, used for illustration purposes only. Our findings should not be interpreted as an argument against alignment. Instead, this paper highlights the need for principled approaches to more advanced alignment. Alignment aims to ensure that large language models (LLMs) behave safely and reliably, including by avoiding unsafe inferences. However, we show that such safety-oriented behaviors can misfire: models may reject warranted conclusions even when they are explicitly supported by context. We call this failure mode misfired alignment, where alignment-induced changes cause LLMs to override explicit evidence. To quantify this phenomenon, specifically on stereotype-related alignment, we introduce VETO, a benchmark consisting of 2,032 BBQ-derived contrastive pairs, and define a new metric, Misfired Alignment Rate (MAR), which measures on a 0 to 100 scale how often a model fails on a stereotype-related question but succeeds on its contrastive counterpart. We benchmark 25 LLMs on VETO, and show that all LLMs, including the most recent ones, exhibit non-trivial (4.7 to 18.9%) MARs while all human participants achieve 0.0% MAR. Controlled priming experiments further show that alignment-induced cues can substantially amplify MAR across LLMs, indicating that these failures are not merely artifacts of individual examples but can be induced by safety-related framing. Mechanistic analyses on open-weight LLMs reveal late-layer suppression of evidence-supported answers, and comparisons between instruct and base LLMs suggest that this suppression emerges after instruction training. These findings show that current alignment methods can overgeneralize surface-level safety cues, to the point of overriding objective evidence, motivating more work on alignment objectives that better preserve contextual grounding.

[3] Hybrid Neural Retrieval with Generative Query Refinement for Quranic Passage Retrieval
Quranic Passage Retrieval (PR) could be a challenging task due to the linguistic complexity and the semantic gap between the Modern Standard Arabic (MSA) used in daily queries and the Classical Arabic (CA) of the Holy Quran. These factors hinder conventional retrieval methods. To handle these limitations and improve multi-verse retrieval and filter the zero-answer queries, this paper proposes a four-phase neural architecture designed to enhance retrieval accuracy and contextual understanding. The methodology combines hybrid candidate retrieval using AraColBERT dense indexing and BM25 sparse retrieval, followed by semantic reranking with a CAMeLBERTmix cross-encoder. A confidence gating mechanism is then applied to filter zero-answer queries, and an AraT5-based refinement module for multi-verse aggregation. The system is evaluated on an expanded version of the Quran QA 2022 dataset. Results show improved performance compared to the baseline models, achieving a Recall@10 of 0.7024 and a Mean Average Precision (MAP@10) of 0.4947. While the system exhibits a marginal tradeoff in absolute top-rank precision (MRR = 0.5807) compared to heavily optimised single models, the proposed architecture provides a substantially more comprehensive, reliable, and context aware solution for multi-verse Quranic passage retrieval.
```

---

## U100_059 — v2_train_r183_plain_c004

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `183`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the four roles in the LLM loop orchestrated by StateGen to generate training conversations?

### Claim

A state-grounded tool simulator 4.

### Evidence

```text
[1] State-Grounded Multi-Agent Synthetic Data Generation for Tool-Augmented LLMs
Training tool-augmented LLM agents requires large corpora of multi-turn, tool-grounded conversational data that is expensive to annotate, privacy-constrained in production settings, and largely absent from public datasets. We present StateGen, a synthetic data generation platform that produces scored, reasoning-trace-rich training conversations by orchestrating a four-role LLM loop: a persona-conditioned user simulator, an agent under test, a state-grounded tool simulator, and a multi-axis LLM judge. The key architectural contribution is an authoritative state manager that maintains a structured world-state object across turns, enforcing a backend-is-truth invariant that eliminates the dominant class of tool-call hallucinations by construction. StateGen extends naturally to hierarchical multi-agent settings by declaring sub-agents as tools, all sharing a single state object. We report results on 64,698 evaluated conversations across three production corpora: tool-call hallucination scores reach 9.66/10, the system supports persona-driven variation via a 23-dimensional trait vector, and a cleanly separated train and golden evaluation set split confirms the data is not memorization bait (per-criterion gap analysis). Comparison with eight external systems shows that no single publicly available platform combines multi-turn generation, state-grounded tool simulation, hierarchical multi-agent support, and built-in judge scoring.

[2] Which Models Are Our Models Built On? Auditing Invisible Dependencies in Modern LLMs
Modern LLM training pipelines increasingly rely on other models to generate data, filter corpora, judge outputs, and guide development decisions. These dependencies are recursive: a model may depend on an upstream artifact whose own dependencies are documented only in separate releases and artifacts. As a result, the full dependency structure is fragmented across heterogeneous public artifacts, with complexity and recursive depth far outpacing humans' ability to trace. We introduce ModSleuth, an agentic system that recursively reconstructs LLM dependency graphs from public artifacts with source-grounded evidence. We find that the primary challenge is no longer information extraction, but defining what constitutes a dependency and reconciling artifact references across inconsistent documentation. We address these challenges through a formalization that distinguishes direct and indirect dependencies, represents heterogeneous pipeline roles through operation-centered relationships, and resolves artifact identities across names, versions, and repositories. Applying ModSleuth to four public-artifact-rich LLM releases, we recover 1,060 source-verified dependencies and construct large-scale dependency graphs of modern LLM development. These graphs reveal multi-hop license obligations, train-evaluation coupling, discrepancies between released and training-time artifacts, and documentation inconsistencies that would otherwise be difficult to uncover. We release ModSleuth and the resulting dependency graphs to support transparent analysis of the increasingly complex ecosystems underlying modern LLMs.

[3] Learning User Simulators with Turing Rewards
Learning to simulate human users in interactive settings could advance the training of agent assistants, evaluation of personalization systems, research in the social sciences, and more. Existing approaches generally do so by training a large language model (LLM) to match a single ground truth response, either by maximizing the log probability or by using a similarity reward. We instead propose {Turing-RL}: a Turing-Test-based reinforcement learning approach for training user simulator models. {Turing-RL} uses a discriminative Turing reward with an LLM judge to score how indistinguishable a generated response is from the real user's given the user's history, and the user simulator LLM learns to produce responses indistinguishable from what the user could have said with such rewards. Across two different domains--conversational chat and Reddit forum discussion--we find that {Turing-RL} consistently outperforms baseline methods on both LLM and human evaluation metrics. Our study suggests that optimizing for indistinguishability, rather than response matching, is effective for learning user simulators.
```

---

## U100_060 — v2_train_r363_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `363`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What is the core encoding technique behind OneRetrieval, and how does it tie each identifier position to interpretable information?

### Claim

The core encoding technique behind OneRetrieval is Keyword-Aligned Encoding (KAE).

### Evidence

```text
[1] OneRetrieval: Unifying Multi-Branch E-commerce Retrieval with an Editable Generative Model
Industrial e-commerce search serves hundreds of millions of items through a multi-branch retrieval stage fused by hand-tuned merging without joint optimization. Generative retrieval (GR) raises the prospect of collapsing this stage into a single model, yet unification is gated by more than retrieval quality: the inverted-index branch converts below the platform average yet persists because it is almost the only branch where operations can inject a new term within hours without any model update; a one-model substitute must preserve this real-time editability. Existing GR methods structurally lack it: closed-codebook methods fix each slot to a quantized embedding at training, while open-vocabulary methods leave new-term routing to model generalization. We present OneRetrieval, a one-model GR framework built on Keyword-Aligned Encoding (KAE), which ties each identifier position to an interpretable attribute word, pairing competitive recall quality with the editability of the inverted index -- to our knowledge the first editable generative retrieval method. An information-theoretic merging organizes 18 attribute categories into six codebook groups with non-uniform capacity; reserved slots in each codebook can be bound to new words after deployment without retraining; and a four-stage fine-tuning pipeline secures quality and editability jointly. On five million real-traffic requests, OneRetrieval matches the deep recall of the strongest generative baseline, with an intervention hit rate over an order of magnitude above closed-codebook encodings. Online, replacing the inverted-index branch significantly lifts order volume; extending to nearly the entire stage holds conversion while improving CTR. The system is deployed at Kuaishou, serving hundreds of millions of PVs daily.

[2] From Sparse Features to Trustworthy Proxies: Certifying SAE-Based Interpretability
Sparse autoencoders (SAEs) are increasingly used to extract interpretable features from language models (LMs), yet a central question remains: when can an SAE-based explanation be treated as a faithful view of an underlying frozen LM We study this through a post-hoc generalization framework that certifies the LM via a sparse proxy, obtained by replacing a native hidden activation with its pretrained SAE reconstruction. Our framework derives an upper bound on the base model's expected risk using four measurable quantities: proxy risk, SAE reconstruction gap, concept-pool mismatch, and sparse complexity. We interpret this certificate as an operational criterion for explanatory faithfulness. In particular, a non-vacuous bound indicates that the extracted sparse features retain meaningful predictive information, while small reconstruction and mismatch errors indicate that the proxy remains behaviorally close to the original model. Empirically, we show that the bound becomes non-vacuous on GPT-2 Small, Gemma-2B, and Llama-3-8B at practical sample sizes. A detailed layerwise analysis of Llama-3-8B reveals a strong depth dependence, with later layers becoming much easier to certify, associated with both stronger local fidelity and weaker downstream error amplification. Finally, through feature-shuffling ablations, we show that the decomposition distinguishes genuine semantic alignment from mere statistical sparsity, providing a useful diagnostic for when SAE-based explanations become less reliable.

[3] Privacy-Preserving Text Sanitization for Distributed Agents Collaboration via Disentangled Representations
When distributed agents exchange text across organizational boundaries, privacy leakage arises not only from explicit identifiers but also from distributional signatures such as formatting conventions, vocabulary choices, and syntactic patterns. We propose DiSan(Disentangled Sanitization), a privacy-preserving sanitization framework and a built-in component of Intern-Shannon for multi-agent collaboration. DiSan uses a two-stream encoder to factorize text into a source-invariant role subspace that preserves task semantics and a source-identifying style subspace that remains local. Federated proto-type alignment and adversarial regularization enable joint training without centralizing raw text. Experiments show that identifier-level masking is insufficient: masking 19.2% of tokens reduces TF-IDF stylometric attribution by only 18.6%. By contrast, DiSan reduces answer-level PII exposure by 20 times while maintaining 83% answer faithfulness on a distributed multi-agent RAG benchmark, and lowers Enron stylometric attribution by 73.2% under TF-IDF and 70.6% under a neural probe.
```

---

## U100_061 — v2_train_r275_plain_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `275`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

Which three datasets are used to evaluate the CoRA method across the three open-weight LLMs?

### Claim

The question asks for the datasets used to evaluate the CoRA (Confidence--Rationale Alignment) method across the three open-weight LLMs.

### Evidence

```text
[1] CoRA: Confidence-Rationale Alignment for Reliable Chain-of-Thought Reasoning
Chain-of-thought (CoT) reasoning can improve LLM performance, but high answer confidence may be misleading when the accompanying CoT rationale is plausible yet incomplete or poorly supported. We study confidence--rationale alignment: whether a model's confidence in its committed answer is justified by its generated rationale. We introduce a GRPO-based reinforcement learning framework that jointly rewards answer correctness, committed-answer probability, and rubric-based rationale support, where the rubric assesses grounding, coherence, task match, and connection to the selected answer without revealing the gold answer to the judge. Across MedQA, MathQA, and OpenBookQA using three open-weight LLMs, our method reduces the confidence--rationale alignment error by up to 26.51% compared with untuned checkpoints, SFT, and correctness-only GRPO, while maintaining competitive accuracy and often improving calibration. These results show that reliable CoT reasoning requires not only confident answers, but rationales that substantively support them.

[2] MÖVE: A Holistic LLM Benchmark for the German Public Sector
We present MÖVE (Modelle für die Öffentliche Verwaltung Evaluieren), a holistic benchmark for evaluating large language models (LLMs) in the context of the German public sector. While LLMs are increasingly adopted in public administration, model selection remains largely ad hoc, and existing benchmarks offer limited guidance: they are predominantly English-centric, US-centric in content, and focus exclusively on task performance. MÖVE addresses these gaps by evaluating 39 models across two complementary dimensions. Performance criteria cover summarization, question answering, and topic extraction. Governance criteria assess hallucination tendencies, energy consumption, provider transparency, and alignment with German constitutional values and knowledge about positions by German political parties. In total, we utilize ten German-language datasets, including gold- and silverstandard datasets that we constructed to reflect public-administration domains. We employ a multi-metric evaluation strategy combining classical NLP metrics, embedding-based methods, and LLM-as-a-judge approaches. Our results show that no single model dominates across all criteria: top performers differ between tasks, and model size alone is a poor predictor of quality. We further evaluate the benchmark itself, analyzing its statistical precision, LLM judge reliability, the impact of our private datasets on model rankings, the sensitivity of our results to prompt formulation, and the validity of our energy consumption estimates. MÖVE is designed as a living benchmark under active development; results are publicly available at https://moeve.bundesdruckerei.de/.

[3] Know Your Limits : On the Faithfulness of LLMs as Solvers and Autoformalizers in Legal Reasoning
Large Language Models (LLMs) achieve strong performance on reasoning tasks, but whether this reflects faithful logical inference or heuristic approximation remains unclear. We study this question in legal entailment by comparing three paradigms, including pure LLM classification, LLM-based Formal Reasoning, and solver-based Formal Reasoning using the Z3 SMT solver, on a re-annotated subset of ContractNLI across five LLMs. Our re-annotation reveals a systematic and measurable gap between pragmatic legal interpretation and strict formal entailment, where a substantial proportion of legally sound inferences are not formally grounded without additional unstated assumptions. While introducing formal structure improves accuracy, with LLM-based Formal Reasoning achieving the highest benchmark performance, we show that this gain does not imply faithful reasoning. We identify three recurring failure modes: scope laundering, where LLMs report solver-inconsistent classifications without executing the underlying formal reasoning, producing conclusions that appear logically grounded but are not; implicit constraint blindness, where LLMs overlook logical constraints present in formal representations; and program synthesis failures, where LLMs generate incorrect Z3 code despite structured prompting. Critically, scope laundering persists across all models, raising serious concerns about the faithfulness of LLM-based formal reasoning as a proxy for symbolic execution. These results reveal a fundamental gap between benchmark accuracy and logical faithfulness.
```

---

## U100_062 — v2_train_r408_cited_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `408`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

Which extraction strategy achieved the strongest results, and what maximum term recall did it maintain across large and small models?

### Claim

The line-number selection strategy achieved the strongest results, and it maintained a maximum term recall of up to 95% across both large and small models.

### Evidence

```text
[1] SafeLLM: Extraction as a Hallucination-Resistant Alternative to Rewriting in Safety-Critical Settings
Large language models (LLMs) are increasingly used to access organisational documentation, including standard operating procedures (SOPs), HR policies and institutional guidelines. However, retrieval-augmented generation (RAG) systems that rely on free-form rewriting can introduce hallucinations and unstable trade-offs between completeness and conciseness, particularly in safety- and compliance-critical settings. Objectives: To evaluate extraction as a hallucination-resistant alternative to rewriting-based RAG and compare strategies that balance precision, recall and safety across document types and model scales. Methods: We compare multiple prompting strategies, including line-number-based source selection, extraction of relevant guideline sentences with explicit safety annotations, and a multi-stage pipeline that refines draft answers using supporting evidence from source guidelines. Experiments are conducted on documents of varying length and structure, including local NHS acute care and oncology guidelines and UK-wide NICE guidelines, using both frontier-scale and locally deployable models. Performance is assessed using automatic metrics and human expert evaluation of relevance and completeness. Results: Line-number selection achieves the strongest results, outperforming direct copying and safety-focused strategies across both large and small models while maintaining high term recall (up to 95%) and close alignment with source text. Safety-oriented approaches improve precision but introduce systematic omissions, while multi-stage filtering further amplifies this trade-off. Performance varies with document structure: line-based extraction excels in protocol-like content, whereas alternative strategies perform better on more verbose documents (up to 97% term recall).
```

---

## U100_063 — v2_train_r464_cited_c002

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `464`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `bait`

### Question

What quantization bit-width does the QLoRA-Vision paper apply to the CLIP backbone, and what zero-shot ImageNet accuracy does it retain?

### Claim

and discuss video-related topics, while focuses on financial news and stock movements.

### Evidence

```text
[1] VCG: A Multimodal Retrieval Framework for E-Commerce Video Feeds under Extreme Cold-Start Conditions
The digital commerce landscape is shifting from static, search-driven catalogs to dynamic, immersive video feeds. This transition introduces an ``extreme cold-start'' problem: unlike traditional items, new short-form videos lack the dense interaction history required for collaborative filtering. Furthermore, immersive feeds introduce strong position and duration biases that distort standard engagement signals. In this paper, we demonstrate the Video Candidate Generation (VCG) system, a scalable multimodal retrieval engine designed to solve these challenges in a large-scale e-commerce environment. By leveraging a domain-adapted vision-language model (based on CLIP), we map users and videos into a shared semantic space, enabling zero-shot retrieval based on visual content rather than behavioral history. We detail the system's architecture and present a rigorous evaluation comparing generative (LLM) vs. discriminative (CLIP) embeddings. Our results show that while generative models excel at attribute prediction, they suffer from embedding space collapse in retrieval tasks. Online A/B testing demonstrates that VCG effectively mitigates engagement biases, yielding a 50\% uplift in deep video completion. To showcase the system's capabilities, we present an interactive demonstration featuring three bi-directional retrieval scenarios: Product-to-Video, Video-to-Product, and Zero-Shot Semantic Search.

[2] MVEB: Massive Video Embedding Benchmark
We introduce the Massive Video Embedding Benchmark (MVEB), a 23-task benchmark for video embeddings spanning classification, zero-shot classification, clustering, pair classification, retrieval, and video-centric question answering. We evaluate 33 models and find that no single model dominates: MLLM-based embeddings lead on classification, clustering, pair classification, and QA; multimodal binding leads on retrieval and zero-shot classification; generative MLLMs without contrastive adaptation collapse on cross-modal tasks. Paired video-only vs. audio+video evaluations show that audio's contribution depends on dataset annotation provenance: audio helps when labels were produced from both modalities and hurts when they were produced from visuals alone, a six-point gap consistent across model families. MVEB is derived from MVEB+, a 184-task pool, and is designed to maintain task diversity while reducing evaluation cost. It integrates into the MTEB ecosystem for unified evaluation across text, image, audio, and video. We release MVEB and all 184 tasks along with code and a leaderboard at https://github.com/embeddings-benchmark/mteb.

[3] Can News Predict the Market? Limits of Zero-Shot Financial NLP and the Role of Explainable AI
Can financial news reliably predict short-term stock movements? Despite advances in large language models, this question remains unresolved. We revisit this problem using a zero-shot natural language processing framework, investigating whether models can extract actionable signals from financial news without domain-specific training. We design a structured pipeline that combines zero-shot natural language inference with temporal aggregation, explicitly modelling recency and event-dependent impact horizons when integrating information across articles. To address the need for transparency in high-stakes settings, we introduce a multi-layered explainability framework that links predictions to token-level, article-level, and aggregate evidence, and produces grounded natural language rationales. Across multiple models and prediction horizons, we find that zero-shot approaches consistently fail to outperform simple baselines, with particularly weak performance on negative movements, suggesting deeper structural limitations in mapping news sentiment to short-term price dynamics. However, explainability signals reliably distinguish between trustworthy and unreliable predictions, offering practical value even when accuracy is limited. These findings highlight the limits of zero-shot financial NLP and motivate a shift toward decision-support systems that prioritise transparency and uncertainty awareness. Code: https://github.com/alimert05/zero-shot-stock-xai
```

---

## U100_064 — v2_train_r40_plain_c001

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `40`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What dataset characteristics (time span and frequency) are used in the experiments evaluating the DeXposure-Claw system?

### Claim

The sources do not explicitly state the time span and frequency of the dataset used in the experiments evaluating the DeXposure-Claw system.

### Evidence

```text
[1] DeXposure-Claw: An Agentic System for DeFi Risk Supervision
Decentralized finance exposes supervisors to fast-moving, networked credit risks. General-purpose LLM agents fit this setting poorly: they over-read weak evidence and recommend high-stakes interventions, while existing evaluations offer no regulator-aligned way to measure the resulting false alarms. We introduce DeXposure-Claw, a forecast-grounded agentic supervision system that routes LLM decisions through structured evidence: (1) DeXposure-FM, a graph time-series foundation model, forecasts future exposure networks; (2) deterministic monitors and stress scenarios then turn those forecasts into typed alerts, attribution signals, and scenario evidence; and (3) data-health and confidence gates constrain escalation before DeXposure-Claw emits auditable supervisory tickets with rationales. We further develop DeXposure-Bench, a six-axis evaluation harness, whose decision axis scores tickets against a regulator-aligned absolute-loss ground truth and an explicit false-intervention rate. Experiments on five years of weekly real data fully support our system. Code is at https://github.com/EVIEHub/DeXposure-Claw.

[2] LLMs Infer Cultural Context but Fail to Apply It When Responding
Recent work has shown that LLMs overrepresent dominant cultures, particularly Western ones, while marginalizing others. We investigate whether this affects models' ability to generate culturally adapted responses by evaluating their use of local measurement units based on the user's perceived cultural background. We introduce Cultural and Pragmatic Response Inference (CAPRI), a dataset of conversations with varying levels of cultural cues. Experiments with state-of-the-art LLMs show that models can infer cultural background and recall relevant conventions, but often fail to utilize the information to adapt their answers to the relevant cultural conventions, unless explicitly prompted to perform the tasks sequentially. We further evaluate adaptation to the interpretation of time and quantity expressions, two subjective language grounding dimensions that are affected by culture. We find that models increasingly adapt their answers as cultural cues accumulate, but their priors are not culture-neutral, sometimes aligning with the model's country of origin. Overall, CAPRI provides a resource for future research aimed at narrowing the gap between cultural knowledge and culturally adaptive language generation.

[3] Intelligent Multimodal Retrieval and Reasoning for Geospatial Knowledge Discovery on the I-GUIDE Platform
Geospatial knowledge discovery increasingly requires search across heterogeneous artifacts: datasets, maps, notebooks, software, publications, and the provenance links among them. Conventional geoportals support metadata and spatial filtering, but they rarely provide semantic retrieval, graph-aware provenance traversal, and conversational synthesis in one integrated system. This paper presents I-GUIDE Smart Search, a production multimodal geospatial retrieval-augmented generation (RAG) system embedded in the I-GUIDE Platform, and reports on its design, deployment, and evaluation. The system combines production-maintained OpenSearch keyword, vector, and spatial indexes with a Neo4j knowledge graph and an iterative RAG pipeline for memory-aware query augmentation, reasoning, retrieval-method routing, relevance grading, grounded generation, hallucination and relevance checking. In a single-A100 RAG deployment, I-GUIDE Smart Search supports interactive use up to about 100 concurrent simulated users, reaching 4.4 requests per second with p50 latency near 25 seconds despite 20-50 LLM calls per query. For answer quality, we evaluate a four-category benchmark of 170 unique human-filtered user-facing queries, together with ten intent-specific probe sets generated from the deployed indexes and graph. Smart Search improves retrieved evidence coverage and judged answer quality over non-retrieval and naive-RAG baselines, with the clearest gains on exact-identifier, spatially constrained, simple-recommendation, and domain-specific factual queries requiring current indexed evidence. We distill transferable deployment lessons for spatial RAG systems, covering spatial metadata quality, graph provenance, retrieval routing, interface contracts, refusal-aware evaluation, latency-cost tradeoffs, and the role of the user interface in deployed geospatial cyberinfrastructure.
```

---

## U100_065 — v2_train_r228_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `228`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What methods does DYNA use to retrieve relevant nodes from the temporal knowledge graph at query time?

### Claim

DYNA retrieves relevant nodes from the temporal knowledge graph at query time using random walks and centrality measures.

### Evidence

```text
[1] DYNA : Dynamic Episodic Memory Networks for Augmenting Large Language Models with Temporal Knowledge Graphs in Continuous Learning
Large Language Models (LLMs) struggle to incorporate new knowledge without forgetting or costly retraining. We propose DYNA, a lightweight framework that augments a frozen LLM with a temporal knowledge graph where events are nodes and temporal relations are directed, timestamped edges. The graph serves as an external, updatable memory. At query time, DYNA retrieves relevant nodes via random walks and centrality measures, then augments the LLM's response. Evaluated on three temporal recall tasks, DYNA reduces catastrophic forgetting by ~7% compared to fine-tuning and improves temporal ordering by ~5% over standard RAG. Higher graph clustering coefficients correlate with better retrieval, showing that graph structure matters. Contributions: (1) episodic memory as temporal KG, (2) retraining-free LLM augmentation, (3) graph properties as predictors of retrieval performance.

[2] Temporal Preference Optimization for Unsupervised Retrieval
Unsupervised dense retrievers offer scalability by learning semantic similarity from unlabeled documents via contrastive learning, but they struggle to capture the temporal relevance, retrieving semantically related but temporally misaligned documents-an important aspect when a document collection spans multiple time periods (e.g., retrieving documents from 2018-2025 for "Who is the president in 2019?" introduces temporal ambiguity). Existing methods rely on supervised training with explicit timestamps, which are not always feasible. We propose TPOUR (Temporal Preference Optimization for Unsupervised Retriever), which uses our novel training method Temporal Retrieval Preference Optimization (TRPO). TRPO reinterprets preference learning in the temporal dimension, guiding the retriever to favor temporally aligned documents. TPOUR further generalizes to unseen time periods via interpolation in a learned time embedding, enabling continuous temporal alignment. Experiments on temporal information retrieval (T-IR), TPOUR outperforms both unsupervised and supervised baselines. Compared to Qwen-Embedding-8B, despite being about 72.7x smaller, TPOUR Contriever improves average nDCG@5 by +4.04 (+12.15%) on explicit and +4.98 (+15.21%) on implicit queries. We provide our code at https://github.com/agwaBom/TPOUR.

[3] EventConnector: Mining Social Event Relations through Temporal Graphs
Understanding and retrieving related real-world events based on their temporal dynamics is a fundamental challenge in time-sensitive applications such as forecasting, information retrieval, and social analysis. Existing methods often rely on semantic similarity or global time-series alignment, which overlook the transient and directional dependencies that frequently underlie real-world correlations. In this work, we introduce \textit{EventConnector}, a framework that constructs a temporal event graph capturing localized co-fluctuations and lead-lag relationships between events through their time-series trajectories. We further propose \textbf{EC-Fusion}, an adaptive retrieval mechanism that fuses EventConnector's graph-based scores with a complementary Granger-causal signal via a graph-quality-aware mixing weight. Across two real-world prediction market benchmarks (Polymarket and Kalshi) and nine forecasting architectures evaluated over three random seeds, EC-Fusion is the best non-oracle retrieval method on $17/18$ model--dataset cells, reducing RMSE by $6.87\%$ on average (up to $10.86\%$) over the strongest comparable retrieval baseline, with statistical significance at $p < 0.01$ after Holm--Bonferroni correction. These results highlight the effectiveness of temporally grounded graph modeling, augmented with causal-signal fusion, in capturing latent event relationships beyond what semantic similarity or traditional alignment techniques can offer.
```

---

## U100_066 — v2_train_r20_cited_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `20`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What roles do producer and consumer agents play in the MATM framework for trajectory sharing?

### Claim

In the Multi-Agent Transactive Memory (MATM) framework, producer agents contribute trajectories to a shared repository, which are then retrieved by consumer agents to improve task execution.

### Evidence

```text
[1] Multi-Agent Transactive Memory
The decentralized deployment of LLM agents with diverse capabilities across diverse tasks motivates infrastructure for knowledge sharing across heterogeneous agent populations. Just as search engines index human-generated artifacts to support human problem solving, retrieval systems can organize agent-generated artifacts for reuse across agent populations. We extend retrieval-augmented generation - which demonstrates the value of human-authored artifacts to individual agents - to retrieval of agent-generated artifacts supporting a population of agents. In particular, agent trajectories encode reusable procedural knowledge, yet these artifacts are typically discarded after a single use or retained only by the producing agent, forcing newly instantiated agents to repeatedly rediscover existing solutions. We propose Multi-Agent Transactive Memory (MATM), a framework for population-level storage and retrieval of agent-generated trajectories, where producer agents contribute trajectories to a shared repository and consumer agents retrieve them to improve task execution. We focus on interactive environments (ALFWorld and WebArena), where trajectories are long and encode especially rich procedural structure. Our experiments demonstrate that retrieving trajectories from MATM improves downstream task performance and reduces interaction steps without coordination or joint training. These results position MATM as a design pattern for population-level experience sharing in open agent ecosystems.
```

---

## U100_067 — v2_train_r196_cited_c010

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `196`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three recurring failure modes identified in LLM-based formal reasoning, and how is scope laundering defined?

### Claim

Critically, scope laundering persists across all models, raising serious concerns about the faithfulness of LL

### Evidence

```text
[1] Know Your Limits : On the Faithfulness of LLMs as Solvers and Autoformalizers in Legal Reasoning
Large Language Models (LLMs) achieve strong performance on reasoning tasks, but whether this reflects faithful logical inference or heuristic approximation remains unclear. We study this question in legal entailment by comparing three paradigms, including pure LLM classification, LLM-based Formal Reasoning, and solver-based Formal Reasoning using the Z3 SMT solver, on a re-annotated subset of ContractNLI across five LLMs. Our re-annotation reveals a systematic and measurable gap between pragmatic legal interpretation and strict formal entailment, where a substantial proportion of legally sound inferences are not formally grounded without additional unstated assumptions. While introducing formal structure improves accuracy, with LLM-based Formal Reasoning achieving the highest benchmark performance, we show that this gain does not imply faithful reasoning. We identify three recurring failure modes: scope laundering, where LLMs report solver-inconsistent classifications without executing the underlying formal reasoning, producing conclusions that appear logically grounded but are not; implicit constraint blindness, where LLMs overlook logical constraints present in formal representations; and program synthesis failures, where LLMs generate incorrect Z3 code despite structured prompting. Critically, scope laundering persists across all models, raising serious concerns about the faithfulness of LLM-based formal reasoning as a proxy for symbolic execution. These results reveal a fundamental gap between benchmark accuracy and logical faithfulness.

[2] SIMMER: Benchmarking Latent Failures in LLM Executable Planning with a World Model
Large language models (LLMs) are increasingly deployed as planners for autonomous agents in household environments. While existing benchmarks evaluate whether LLM-generated plans execute successfully, they overlook a critical type of failure: latent failures. Unlike immediate failures that trigger instant feedback at execution time and enable timely correction, latent failures do not immediately halt plan execution but silently compromise goal achievement. In severe cases, they cause irreversible harm. To address this gap, we introduce SIMMER, a benchmark for evaluating latent failures in LLM planning through a human-curated symbolic world model grounded in the kitchen domain. SIMMER defines a world model comprising 77 actions, 262 unique objects, and approximately 46,800 possible interactions that are semantically realistic, derived from real-world cooking scripts. It then leverages a state machine executor that validates plans against the world model and detects immediate precondition violations, latent hazards, and irreversible failures. Experiments across six LLMs show that even frontier models achieve at most 17% error-free plans. Moreover, up to 56% of plans contain latent failures, the majority of which lead to irreversible consequences. We further demonstrate that explicit state reasoning via counterfactual foresight simulation can reduce latent failures by up to 72% and irreversible cases by up to 75%, suggesting a promising direction for more robust LLM planners.

[3] Understanding and Debugging Failures in N-Gram-Based Generative Retrieval
Generative Retrieval (GR) is an emerging Information Retrieval (IR) paradigm that is motivated by increasingly capable language models. In GR, a model directly generates identifiers for relevant documents. While these systems offer unique advantages, they also introduce distinct failure mechanisms. We explore these failure modes in three contributions: (1) We present a taxonomy of GR failure modes based on GR literature. (2) We empirically investigate failure in a subset of GR: ngram-based methods, more specifically, SEAL and MINDER. Our analysis reveals common issues, such as ambiguous docids, low identifier diversity, and the disproportionate impact of specific identifiers. (3) We introduce a new web-based tool that helps the IR community analyze generated ngrams and their respective contribution to the final ranking, providing an intuitive interface to identify where such GR methods go wrong.
```

---

## U100_068 — v2_train_r430_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `430`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

How does the paper adapt truncated backpropagation-through-time (TBPTT) for the multi-turn dialogue setting, and what benefit does it provide?

### Claim

The paper adapts truncated backpropagation-through-time (TBPTT) for the multi-turn dialogue setting by applying it to their context-driven incremental compression (C-DIC) method.

### Evidence

```text
[1] Context-Driven Incremental Compression for Multi-Turn Dialogue Generation
Modern conversational agents condition on an ever-growing dialogue history at each turn, incurring redundant attention and encoding costs that grow with conversation length. Naive truncation or summarization degrades fidelity, while existing context compressors lack cross-turn memory sharing or revision, causing information loss and compounding errors in long dialogues. We revisit the context compression under conversational dynamics and empirically present its fragility. To improve both efficiency and robustness, we introduce Context-Driven Incremental Compression (C-DIC), which treats a conversation as interleaved contextual threads and stores revisable per-thread compression states in a single, compact dialogue memory. At each turn, a lightweight retrieve, revise, and write-back loop shares information across turns and updates stale memories, stabilizing long-horizon behavior. In addition, we adapt truncated backpropagation-through-time (TBPTT) to our multi-turn setting, learning cross-turn dependencies without full-history backpropagation. Extensive experiments on long-form dialogue benchmarks demonstrate superior performance and efficiency of C-DIC; notably, C-DIC shows stable inference latency and perplexity over hundreds of dialogue turns, supporting a scalable path to high-quality dialogue modeling.

[2] From Awareness to Adherence: Bridging the Context Gap in Spoken Dialogue Systems via Context-Aware Decoding
Despite the success of end-to-end (E2E) spoken dialogue systems, maintaining strict context adherence in multi-round conversations remains a challenge. While prior works attribute these failures to models forgetting dialogue history, we highlight an equally critical but overlooked bottleneck: a gap between latent context awareness and active adherence. Although models internally recognize relevant past utterances, strong parametric priors often overshadow these signals during decoding. To bridge this gap, we propose an audio-adapted Context-Aware Decoding (CAD) approach. By leveraging internal attention mechanisms to isolate key historical rounds, our approach contrasts output distributions with and without this key context during inference, directly amplifying multimodal contextual signals. Evaluations on the Audio MultiChallenge benchmark demonstrate significant improvements in Semantic Memory and Self Coherence subtasks, successfully enforcing strict, context-faithful adherence.

[3] Doc-to-Atom: Learning to Compile and Compose Memory Atoms
Long input sequences are central to document understanding and multi-step reasoning in Large Language Models, yet the quadratic cost of attention makes inference both memory-intensive and slow. Context distillation mitigates this by compressing contextual information into model parameters, and recent work such as Doc-to-LoRA amortizes context distillation into a single forward pass that generates one LoRA adapter per document. However, producing a single monolithic adapter for all queries leads to irrelevant-query interference, limited compositional recall, and poor scalability to long-document reasoning. To address these challenges, we propose Doc-to-Atom (Doc2Atom), a compositional parametric memory framework that decomposes each document into semantically typed knowledge atoms. Each atom is compiled into an independent micro-LoRA adapter and a provenance retrieval key. At inference time, a lightweight query router selects and assembles only the relevant atoms into a query-specific adapter, which is then injected into a frozen base model. The entire system is trained end-to-end through a multi-objective distillation framework. Experiments on six diverse QA benchmarks demonstrate that Doc2Atom outperforms Doc-to-LoRA baselines while reducing the memory cost of document internalization.
```

---

## U100_069 — v2_train_r162_cited_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `162`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What are the three evidence-expansion primitives introduced by VeriGraph for constructing the evidence DAG?

### Claim

The three evidence-expansion primitives introduced by VeriGraph for constructing the evidence DAG are computational expansion, grounding expansion, and derivational expansion.

### Evidence

```text
[1] VeriGraph: Towards Verifiable Data-Analytic Agents
LLM-based agents have demonstrated strong capabilities in data-intensive analytical tasks, yet their outputs are rarely verifiable: a reliance on linear text trajectories makes their reasoning difficult to audit. In particular, deterministic computations over raw data and semantic deductions over natural-language claims are often entangled in an unstructured stream, leaving numerical conclusions hard to reproduce and qualitative judgments hard to inspect. To address this, we propose VeriGraph, a traceable neuro-symbolic reasoning framework that enables agents to construct an explicit heterogeneous evidence directed acyclic graph (DAG) during execution. VeriGraph introduces three evidence-expansion primitives, namely computational, grounding, and derivational expansion, to connect raw data, interpreter variables, computed results, and natural-language claims in a unified graph. Under this formulation, structural traceability is reduced to graph reachability from raw data sources to terminal claims, while semantic support is measured by claim-level evidence evaluation. To improve graph construction, we further design a graph-based policy optimization strategy with a composite reward that jointly supervises answer correctness, computational integrity, and derivational coherence. Experiments on four benchmarks show that VeriGraph-8B achieves the highest overall score among all baselines. More importantly, VeriGraph produces auditable evidence graphs with substantially stronger claim grounding, achieving a 87.61\% Grounding Rate under our claim-level evidence support evaluation. These results suggest that explicit evidence-graph construction is a promising path toward verifiable data-analytic agents. Our code is available at https://github.com/ignorejjj/VeriGraph.
```

---

## U100_070 — v2_train_r178_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `178`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What two actions does ACCORD perform before each action to enable adaptive grounding?

### Claim

ACCORD, the Action-Conditioned Contextual Grounding framework, performs two actions before each action: 1.

### Evidence

```text
[1] ACCORD: Action-Conditioned Contextual Grounding for Language Agents
User instructions are often underspecified because humans rely on implicit assumptions about the surrounding environment. For large language model (LLM) agents operating in information-rich digital and physical environments, these assumptions cannot be inferred from the instruction alone; they must be recovered from the current state of tools, data, interfaces, and observations. Effective execution therefore requires agents to identify missing context, ground it in observed evidence, and carry it forward into subsequent actions. We show that current agents often fail to do so. They act from assumed rather than observed specifics, overlook information they could have gathered, and fail to incorporate evidence that has already been returned. Building on this insight, we propose ACCORD (Action-Conditioned Contextual Grounding), a simple and effective agent framework for adaptive grounding. Before each action, ACCORD actively probes the environment for missing information and integrates relevant context from the agent's trajectory that would otherwise be overlooked. Requiring no additional training or task-success signals, ACCORD improves task-goal completion on AppWorld by up to +20.6 points with GPT-5-mini, from 42.0% to 62.6%, compared to strong baselines. These gains persist with a substantially stronger base model (+10.8 with Claude-4.5-sonnet), an open-weight model (+10.1 with Qwen3.5-27B-FP8), and on the embodied AlfWorld benchmark (+7.4 success rate with GPT-5-mini).

[2] TASR: Training-Free Adaptive Stopping for Iterative Retrieval
Iterative retrieval-augmented generation agents commonly overspend by continuing to retrieve after the model has converged on an answer, incurring calls that change neither the prediction nor the supporting evidence. Existing remedies learn a stopping policy from labeled trajectories, tying the decision to a trained component that requires retraining for each new model or task. We propose TASR (Training-Free Adaptive Stopping Rule), a one-line predicate that fires when the model repeats its previous-round normalized answer and the isotonically calibrated logit margin exceeds 0.25. No classifier or value head is learned; the threshold is fixed across all twenty-four (model, retriever, corpus) configurations we evaluate. On a 3-model x 2-dataset distractor grid, TASR retains 94.8% of fixed-k=5's macro F1 at 62.6% of its calls and exceeds fixed-k=3 by +3.42 F1. The pattern holds on nine open-domain BM25 cells (55.01 F1 at 2.98 calls vs. 54.33 at 3.00 for fixed-k=3) and, with calibration locked from the distractor split, on nine dense-retrieval cells across two retriever families, with zero significant regressions in either extension. The rule was selected from an exhaustive enumeration of 381 candidate stopping rules; no alternative Pareto-dominates it on any evaluated configuration. A signal-quality analysis shows that verbalized 1-5 confidence collapses on RLHF-tuned models (96.5% of values equal 5, entropy 0.182 nats), while the logit margin achieves 44x better class-conditional separation, grounding the design in a measurable model pathology. TASR is an auditable, training-free Pareto baseline against which learned stopping controllers can be compared. Code is publicly available.

[3] LLMs Infer Cultural Context but Fail to Apply It When Responding
Recent work has shown that LLMs overrepresent dominant cultures, particularly Western ones, while marginalizing others. We investigate whether this affects models' ability to generate culturally adapted responses by evaluating their use of local measurement units based on the user's perceived cultural background. We introduce Cultural and Pragmatic Response Inference (CAPRI), a dataset of conversations with varying levels of cultural cues. Experiments with state-of-the-art LLMs show that models can infer cultural background and recall relevant conventions, but often fail to utilize the information to adapt their answers to the relevant cultural conventions, unless explicitly prompted to perform the tasks sequentially. We further evaluate adaptation to the interpretation of time and quantity expressions, two subjective language grounding dimensions that are affected by culture. We find that models increasingly adapt their answers as cultural cues accumulate, but their priors are not culture-neutral, sometimes aligning with the model's country of origin. Overall, CAPRI provides a resource for future research aimed at narrowing the gap between cultural knowledge and culturally adaptive language generation.
```

---

## U100_071 — v2_train_r74_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `74`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

On which tasks do heavier contextual encoders like BGE-M3 and BERTurk outperform Morpheus, and what does the paper attribute this trade-off to?

### Claim

Heavier contextual encoders like BGE-M3 and BERTurk outperform Morpheus on context- and inflection-dependent tasks such as Named Entity Recognition (NER) and case/number probing.

### Evidence

```text
[1] Morpheus: A Morphology-Aware Neural Tokenizer and Word Embedder for Turkish
Turkish is agglutinative: meaning is carried by morphemes, yet the subword tokenizers that drive modern language models split words by corpus statistics, fragmenting semantically loaded suffixes and -- in the case of WordPiece and rule-based analyzers -- failing to decode their output back to the original text. This paper presents \textbf{Morpheus}, a neural morpheme-boundary model for Turkish that is at once a lossless, morphology-aware tokenizer and a word-embedding producer. A differentiable Poisson-binomial dynamic program turns per-character boundary probabilities into soft morpheme memberships during training and exact segments at inference, with no string normalization, so $\mathrm{decode}(\mathrm{encode}(w)) = w$ holds by construction. Because the model is neural, the same forward pass that tokenizes also emits a structured word embedding. Among reversible tokenizers -- the only ones valid for generation -- Morpheus attains the lowest bits-per-character ($1.425$), roughly doubles the gold morphological alignment of the subword family (MorphScore macro-F1 $0.61$ vs.\ ${\sim}0.32$), and uses ${\sim}19\%$ less GPU memory than 64K-vocabulary subword tokenizers. As an embedder, frozen Morpheus vectors lead on lexical retrieval (root-family MAP $0.85$) and same-root verification (ROC-AUC $1.00$), surpassing the multilingual retriever BGE-M3 and BERTurk; on context- and inflection-dependent tasks (NER, case/number probing) the heavier contextual encoders remain ahead -- a trade-off we attribute to Morpheus's root-centric geometry. Code: https://github.com/lonewolf-rd/TurkishMorpheus; model: https://huggingface.co/lonewolflab/Morpheus-TR-50K; interactive demo: https://huggingface.co/spaces/lonewolflab/morpheus-tr-demo.

[2] Rescaling MLM-Head for Neural Sparse Retrieval
Learned sparse retrieval (LSR) models such as SPLADE have traditionally used BERT-style masked language models as backbone encoders. A natural expectation is that replacing BERT with stronger pretrained encoders should improve retrieval effectiveness. However, we find that under standard SPLADE training recipes, backbones with large MLM-head L2 norms can suffer performance degradation and even training collapse under standard SPLADE training recipes. We identify this failure as a scale mismatch in the MLM head: SPLADE directly uses MLM-head outputs to construct sparse lexical representations, and query-document relevance is computed by an unnormalized dot product over these representations. As a result, an inflated MLM-head scale can amplify sparse activations, distort matching scores, and destabilize contrastive training under common training settings. To address this issue, we introduce a simple initialization-time correction that rescales the MLM-head projection by a constant factor before SPLADE training. This zero-cost adjustment improves training stability without modifying the model architecture or training objective. Across both in-domain and out-of-domain retrieval benchmarks, this simple correction substantially improves large-norm backbones such as ModernBERT and Ettin, turning unstable training runs into competitive sparse retrievers. In several settings, the corrected models further match or surpass the classic BERT-SPLADE baseline. These findings suggest that the bottleneck in adapting pretrained encoders to LSR is not encoder capacity alone, but the calibration of the MLM-head scale used to construct sparse lexical representations.

[3] IndicContextEval: A Benchmark for Evaluating Context Utilisation in Audio Large Language Models Across 8 Indic Languages
AudioLLMs enable speech recognition conditioned on textual prompts such as domain descriptions or entity lists. However, it remains unclear whether these models genuinely utilise such context or rely on parametric knowledge learned during pretraining. Existing benchmarks cannot answer this question because they evaluate transcription under fixed prompting conditions and rarely include explicit contextual inputs. We introduce IndicContextEval, a 56-hour multilingual benchmark of natural speech from 555 speakers across 8 Indian languages and 23 professional domains. We design a 7-level prompting framework that progressively introduces contextual signals, including metadata, natural-language descriptions, entity lists in English and native script, and adversarial prompts with incorrect entities. Evaluating five models reveals substantial differences in context utilisation behaviour, highlighting the need for explicit evaluation of contextual grounding in AudioLLMs.
```

---

## U100_072 — v2_train_r8_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `8`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

How does ELVA treat negative samples differently, and what two objectives does its rule-based reward jointly optimize?

### Claim

Instead of treating all negatives as equally dissimilar, ELVA ranks them according to their similarity, enabling the model to learn distinct grain information from each negative.

### Evidence

```text
[1] ELVA: Exploring Ranking-Driven Universal Multimodal Retrieval
Leveraging Multimodal Large Language Models (MLLMs) via contrastive learning has become a mainstream paradigm for improving the performance of Universal Multimodal Retrieval (UMR). However, previous works have ignored the grain blindness when adapting the contrastive paradigm into retrieval tasks. Grain blindness refers to the tendency of the model to overlook grain-level information contained in the query, which is crucial for effectively handling complex queries. This stems from contrastive learning treating samples as a binary classification (positive/negative), while ignoring the different information carried by each negative sample. To address this, we argue that negatives should be treated differently according to their similarity to the positive sample, enabling the model to learn distinct grain information from each negative. In this paper, we introduce a simple but effective framework, called ELVA, a novel rule-based RL framework that mitigates grain blindness through ranking-driven MLLMs. 1) Instead of relying on reward models, we extend Reinforcement Learning with Verifiable Rewards (RLVR) to retrieval tasks, allowing the model to explore new ranking behaviors without explicit ranking labels. 2) By utilizing rule-based rewards, our approach jointly optimizes the ranking of negative samples while enlarging the similarity gap between positive and negative. To more precisely measure grain blindness, we further introduce MRBench, a new benchmark specifically designed for multi-grain query scenarios. ELVA achieves state-of-the-art results across standard retrieval benchmarks, and its notable 13.1% improvement on MRBench further demonstrates its effectiveness in alleviating grain blindness.
```

---

## U100_073 — v2_train_r62_cited_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `62`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

Which large-norm backbone encoders does the paper report as being improved by the proposed rescaling correction, and how do the corrected models compare to the BERT-SPLADE baseline?

### Claim

The paper reports that large-norm backbone encoders such as ModernBERT and Ettin are improved by the proposed rescaling correction.

### Evidence

```text
[1] Rescaling MLM-Head for Neural Sparse Retrieval
Learned sparse retrieval (LSR) models such as SPLADE have traditionally used BERT-style masked language models as backbone encoders. A natural expectation is that replacing BERT with stronger pretrained encoders should improve retrieval effectiveness. However, we find that under standard SPLADE training recipes, backbones with large MLM-head L2 norms can suffer performance degradation and even training collapse under standard SPLADE training recipes. We identify this failure as a scale mismatch in the MLM head: SPLADE directly uses MLM-head outputs to construct sparse lexical representations, and query-document relevance is computed by an unnormalized dot product over these representations. As a result, an inflated MLM-head scale can amplify sparse activations, distort matching scores, and destabilize contrastive training under common training settings. To address this issue, we introduce a simple initialization-time correction that rescales the MLM-head projection by a constant factor before SPLADE training. This zero-cost adjustment improves training stability without modifying the model architecture or training objective. Across both in-domain and out-of-domain retrieval benchmarks, this simple correction substantially improves large-norm backbones such as ModernBERT and Ettin, turning unstable training runs into competitive sparse retrievers. In several settings, the corrected models further match or surpass the classic BERT-SPLADE baseline. These findings suggest that the bottleneck in adapting pretrained encoders to LSR is not encoder capacity alone, but the calibration of the MLM-head scale used to construct sparse lexical representations.
```

---

## U100_074 — v2_train_r348_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `348`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the two conditions that must be met for TASR's stopping predicate to fire, and what is the calibrated logit margin threshold used?

### Claim

The model repeats its previous-round normalized answer. 2.

### Evidence

```text
[1] TASR: Training-Free Adaptive Stopping for Iterative Retrieval
Iterative retrieval-augmented generation agents commonly overspend by continuing to retrieve after the model has converged on an answer, incurring calls that change neither the prediction nor the supporting evidence. Existing remedies learn a stopping policy from labeled trajectories, tying the decision to a trained component that requires retraining for each new model or task. We propose TASR (Training-Free Adaptive Stopping Rule), a one-line predicate that fires when the model repeats its previous-round normalized answer and the isotonically calibrated logit margin exceeds 0.25. No classifier or value head is learned; the threshold is fixed across all twenty-four (model, retriever, corpus) configurations we evaluate. On a 3-model x 2-dataset distractor grid, TASR retains 94.8% of fixed-k=5's macro F1 at 62.6% of its calls and exceeds fixed-k=3 by +3.42 F1. The pattern holds on nine open-domain BM25 cells (55.01 F1 at 2.98 calls vs. 54.33 at 3.00 for fixed-k=3) and, with calibration locked from the distractor split, on nine dense-retrieval cells across two retriever families, with zero significant regressions in either extension. The rule was selected from an exhaustive enumeration of 381 candidate stopping rules; no alternative Pareto-dominates it on any evaluated configuration. A signal-quality analysis shows that verbalized 1-5 confidence collapses on RLHF-tuned models (96.5% of values equal 5, entropy 0.182 nats), while the logit margin achieves 44x better class-conditional separation, grounding the design in a measurable model pathology. TASR is an auditable, training-free Pareto baseline against which learned stopping controllers can be compared. Code is publicly available.

[2] RSRank: Learning Relevance from Representational Shifts
As enterprises deploy RAG-based systems to provide grounded responses to user queries, reranking has become a critical component for the final filtering step that separates relevant from distracting or irrelevant documents. Existing rerankers often rely on heuristic thresholds to achieve optimal filtering. Moreover, for relevance scoring, state-of-the-art methods use a language model's logit signals, which are designed for next-token prediction, not for assessing relevance. To address these limitations, we identify a principled signal for relevance: the representational shift (RS) induced in a query's internal state when conditioned on a document. We observe that the alignment between (a) RS induced by a candidate document and (b) RS induced by an oracle document-set provides a robust indicator of relevance. Building on this insight, we introduce a lightweight training framework that learns projections mapping RS to calibrated relevance scores. Our training objectives naturally filter irrelevant content at a zero threshold, reducing dependence on heuristic tuning. Across diverse retrieval datasets, our method delivers gains over SOTA rerankers.

[3] The Wrong Kind of Right: Quantifying and Localizing Misfired Alignment in LLMs
Warning: This paper studies stereotypes and biases, and contains potentially disturbing examples, used for illustration purposes only. Our findings should not be interpreted as an argument against alignment. Instead, this paper highlights the need for principled approaches to more advanced alignment. Alignment aims to ensure that large language models (LLMs) behave safely and reliably, including by avoiding unsafe inferences. However, we show that such safety-oriented behaviors can misfire: models may reject warranted conclusions even when they are explicitly supported by context. We call this failure mode misfired alignment, where alignment-induced changes cause LLMs to override explicit evidence. To quantify this phenomenon, specifically on stereotype-related alignment, we introduce VETO, a benchmark consisting of 2,032 BBQ-derived contrastive pairs, and define a new metric, Misfired Alignment Rate (MAR), which measures on a 0 to 100 scale how often a model fails on a stereotype-related question but succeeds on its contrastive counterpart. We benchmark 25 LLMs on VETO, and show that all LLMs, including the most recent ones, exhibit non-trivial (4.7 to 18.9%) MARs while all human participants achieve 0.0% MAR. Controlled priming experiments further show that alignment-induced cues can substantially amplify MAR across LLMs, indicating that these failures are not merely artifacts of individual examples but can be induced by safety-related framing. Mechanistic analyses on open-weight LLMs reveal late-layer suppression of evidence-supported answers, and comparisons between instruct and base LLMs suggest that this suppression emerges after instruction training. These findings show that current alignment methods can overgeneralize surface-level safety cues, to the point of overriding objective evidence, motivating more work on alignment objectives that better preserve contextual grounding.
```

---

## U100_075 — v2_train_r355_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `355`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

How many real-world products, categories, and consumer scenarios does the FORGE benchmark cover, and how many LLMs were evaluated?

### Claim

Across these experiments, 12 commercial and open-weights LLMs were evaluated.

### Evidence

```text
[1] One Polluted Page Is Enough: Evaluating Web Content Pollution in Generative Recommenders
Search-augmented LLMs increasingly mediate everyday consumer recommendations by retrieving live web content. This creates a new risk: generative recommenders may consume polluted web content, such as fake reviews and promotional pages crafted to mislead recommendations. We ask: to what extent do search-augmented LLMs become unwitting promoters of fake products when consuming polluted retrieval results? To answer this, we introduce FORGE (Fake Online Recommendations in Generative Environments), a benchmark for measuring fake-product promotion under controlled web-content pollution. Given an upstream search result, FORGE locally rewrites real products in retrieved web pages into fake ones to simulate web-content pollution, and measures how often the LLM recommends the fake product. FORGE covers 225 real-world products across 15 categories and 5 consumer scenarios. Across 12 commercial and open-weights LLMs, all models are vulnerable: a single polluted page yields fooled rates of up to 27%, while the full top-3 replacement raises this to 73.8%. Vulnerability varies substantially across categories, increasing when models lack stable prior knowledge of the relevant products. Reasoning does not mitigate this vulnerability; instead, it often generates spurious social proof to justify false recommendations. We evaluate three defenses: skepticism prompting and consensus filtering (over model priors or cross-document evidence). Skepticism can exacerbate vulnerability, much like reasoning, while filtering risks suppressing legitimate products. We release FORGE at https://github.com/leoluolol/forge-benchmark.
```

---

## U100_076 — v2_train_r435_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `435`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

How many source-verified dependencies does ModSleuth recover when applied to the four public-artifact-rich LLM releases?

### Claim

ModSleuth recovers 1,060 source-verified dependencies when applied to the four public-artifact-rich LLM releases.

### Evidence

```text
[1] Which Models Are Our Models Built On? Auditing Invisible Dependencies in Modern LLMs
Modern LLM training pipelines increasingly rely on other models to generate data, filter corpora, judge outputs, and guide development decisions. These dependencies are recursive: a model may depend on an upstream artifact whose own dependencies are documented only in separate releases and artifacts. As a result, the full dependency structure is fragmented across heterogeneous public artifacts, with complexity and recursive depth far outpacing humans' ability to trace. We introduce ModSleuth, an agentic system that recursively reconstructs LLM dependency graphs from public artifacts with source-grounded evidence. We find that the primary challenge is no longer information extraction, but defining what constitutes a dependency and reconciling artifact references across inconsistent documentation. We address these challenges through a formalization that distinguishes direct and indirect dependencies, represents heterogeneous pipeline roles through operation-centered relationships, and resolves artifact identities across names, versions, and repositories. Applying ModSleuth to four public-artifact-rich LLM releases, we recover 1,060 source-verified dependencies and construct large-scale dependency graphs of modern LLM development. These graphs reveal multi-hop license obligations, train-evaluation coupling, discrepancies between released and training-time artifacts, and documentation inconsistencies that would otherwise be difficult to uncover. We release ModSleuth and the resulting dependency graphs to support transparent analysis of the increasingly complex ecosystems underlying modern LLMs.

[2] Compositional Skill Routing for LLM Agents: Decompose, Retrieve, and Compose
LLM agents increasingly rely on external skills -- reusable tool specifications -- but real-world tasks often require composing multiple skills, not just selecting one. We formalize this as the Compositional Skill Routing problem: given a complex user query and a large skill library, decompose the query into atomic sub-tasks, retrieve the appropriate skill for each sub-task, and compose an executable plan. We present SkillWeaver, a decompose-retrieve-compose framework combining an LLM task decomposer, a bi-encoder skill retriever with FAISS indexing, and a dependency-aware DAG planner. To support evaluation, we introduce CompSkillBench, a benchmark of 300 compositional queries over 2,209 real MCP server skills spanning 24 functional categories, sourced from the public MCP ecosystem. Our experiments reveal that task decomposition quality is the primary bottleneck: standard LLM decomposition reaches only 34.2% category recall at the step level. To address this, we propose Iterative Skill-Aware Decomposition (SAD), a retrieval-augmented feedback loop that iteratively aligns decomposition with available skills. SAD improves decomposition accuracy from 51.0% to 67.7% (+32.7%, Wilcoxon p < 10^-6) in a single iteration; DA-conditioned analysis confirms that correct granularity is the prerequisite for effective retrieval (CatR@1 rises from 34% to 41% when DA=1). SkillWeaver reduces context window consumption by over 99%, and transfer experiments confirm generalization (+35.6% relative DA gain even when target categories are absent from the retrieval pool).

[3] Beyond NL2Code: A Structured Survey of Multimodal Code Intelligence
While Large Language Models (LLMs) have substantially advanced text-to-code synthesis, many real programming tasks specify intent through visual artifacts such as screenshots, charts, vector drawings, videos, and interactive states. These tasks require models to connect visual perception to executable programs, because correctness depends not only on syntax but also on layout, data semantics, interaction behavior, and domain-specific constraints that apply after execution. This survey examines Multimodal Code Intelligence, covering systems that generate, edit, refine, or reason with code under visually grounded inputs and outputs. We first formulate the field by the role that code plays in each task, distinguishing code as a rendered artifact, an editable symbolic structure, a scientific representation, an intermediate reasoning trace, or an executable policy or tool interface. We then organize benchmarks and methods into four domains: Graphical User Interface, Scientific Visualization, Structured Graphics, and Frontier Tasks and Frameworks. This taxonomy connects mature artifact-generation problems to emerging agentic and unified settings and allows us to compare how different tasks treat evidence of correctness. Looking ahead, we argue that future research may benefit from four verification-centered directions. Multi-signal validation can combine complementary evidence of correctness, multi-state verification can test behavior across execution trajectories, cross-task transfer testing can probe reusable visual-code skills, and verifiable agent traces can reveal whether agent actions are grounded in visual evidence. Together, these directions may move this field from single-output imitation toward evidence-grounded executable systems. An ongoing project and resources are available on \href{https://github.com/xjywhu/Awesome-Multimodal-LLM-for-Code}{GitHub}.
```

---

## U100_077 — v2_train_r425_plain_c003

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `425`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three training innovations combined in the MARD pipeline?

### Claim

Per-loss PRM-weighted DPO with programmatic hard negatives. 3.

### Evidence

```text
[1] MARD: Mirror-Augmented Reasoning Distillation for Mechanism-Level Drug-Drug Interaction Prediction
Mechanism-level drug-drug interaction (DDI) prediction requires identifying which enzyme or pharmacodynamic axis is implicated, in which direction, and with which evidence -- not merely whether two drugs interact. We introduce a reproducible mechanism-level DDI labelling and evaluation protocol with a structured 7-family/147-subtype taxonomy, leakage-safe cold-split protocols, and auditable reasoning metrics for evaluating pharmacological prediction beyond flat interaction classification. We propose a pipeline that produces a 7B reasoning MARD (Mirror-Augmented Reasoning Distillation), combining three training innovations: a single-token KL divergence on direction tag that ties the model's prediction, per-loss PRM-weighted DPO with programmatic hard negatives, and a leakage-safe mechanism-aware retrieval channel. Process-reward step labels are automatically verifiable against DrugBank-structured fields, requiring no human or LLM judges. On the April-2026 DrugBank release, our MARD-7B is the only system in a 32-system comparison whose accuracy survives drug-pair novelty, beating the best baseline by +13.9 pp and GPT-4o by +6.7 pp at ~1% of frontier API cost. Further analysis reveals an anti-memorisation signature where accuracy improves on rarely seen drugs, suggesting that gain comes from structured pharmacological reasoning rather than drug-frequency memorisation. We release corpus, DDI-PRM, retrieval index, and training code.

[2] Which Models Are Our Models Built On? Auditing Invisible Dependencies in Modern LLMs
Modern LLM training pipelines increasingly rely on other models to generate data, filter corpora, judge outputs, and guide development decisions. These dependencies are recursive: a model may depend on an upstream artifact whose own dependencies are documented only in separate releases and artifacts. As a result, the full dependency structure is fragmented across heterogeneous public artifacts, with complexity and recursive depth far outpacing humans' ability to trace. We introduce ModSleuth, an agentic system that recursively reconstructs LLM dependency graphs from public artifacts with source-grounded evidence. We find that the primary challenge is no longer information extraction, but defining what constitutes a dependency and reconciling artifact references across inconsistent documentation. We address these challenges through a formalization that distinguishes direct and indirect dependencies, represents heterogeneous pipeline roles through operation-centered relationships, and resolves artifact identities across names, versions, and repositories. Applying ModSleuth to four public-artifact-rich LLM releases, we recover 1,060 source-verified dependencies and construct large-scale dependency graphs of modern LLM development. These graphs reveal multi-hop license obligations, train-evaluation coupling, discrepancies between released and training-time artifacts, and documentation inconsistencies that would otherwise be difficult to uncover. We release ModSleuth and the resulting dependency graphs to support transparent analysis of the increasingly complex ecosystems underlying modern LLMs.

[3] PersonaDrive: Human-Style Retrieval-Augmented VLA Agents for Closed-Loop Driving Simulation
Closed-loop driving simulators typically populate their environments with non-ego traffic agents that behave largely the same way, produced either by rule-based traffic managers or by learned models trained toward a single behavioral mode. Recent work introduces style variation through post-hoc labels on observational data or LLM-inferred reward weights, but these signals act as proxies for what a style should reward rather than demonstrations of humans explicitly asked to drive in that style. We introduce PersonaDrive, a pipeline that conditions a vision-language-action (VLA) driving agent on retrieved demonstrations from a style-instructed human driving dataset, in which participants drive CARLA leaderboard routes under aggressive, neutral, and conservative instructions on a driver-in-the-loop rig. The pipeline has three stages: (i) offline triplet mining over per-style human driving data using a combined image-text similarity score; (ii) training a lightweight retrieval head that fuses frozen visual features with a small control encoder over per-style databases; and (iii) fine-tuning a single VLA backbone to treat retrieved context points as in-context behavioral demonstrations during waypoint prediction. At inference, the same backbone is conditioned on any style by swapping which per-style database the retrieval head queries, so selecting a style requires no per-style retraining while enabling human-style, style-diverse non-ego agents for closed-loop simulation. On Bench2Drive, PersonaDrive (no style) improves the driving score by 4.6% over SimLingo and 2.5% over HiP-AD, and under style conditioning attains the highest driving score in every style within a roughly 2% band (its weakest style surpassing the strongest baseline, DMW, by 5.4%), while average speed and acceleration rise by 18% and 25% from the conservative to the aggressive instruction.
```

---

## U100_078 — v2_train_r422_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `422`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What is the 'decompression gap' that the paper identifies in current LLMs, and what techniques does the paper find can partially mitigate it?

### Claim

This gap is particularly evident in the task of converting abstract proverbs into engaging narratives.

### Evidence

```text
[1] Constrained Semantic Decompression in LLMs through Persian Proverb-Conditioned Story Generation
Transforming a dense, abstract proverb into an engaging and morally faithful narrative requires deep cultural understanding and robust semantic grounding. We frame this problem as a \emph{constrained semantic decompression} task and study proverb-conditioned story generation as a testbed for abstraction-to-realization in large language models (LLMs). Focusing on Persian, we introduce the Proverb Aligned Narrative Dataset (PAND), pairing proverbs with human-written stories and explicit meanings. By a hybrid evaluation framework that combines human-calibrated LLM-as-a-Judge with structural metrics, we analyze model behavior across multiple prompting regimes. Our findings reveal a persistent \emph{decompression gap}: current LLMs often achieve strong surface-level fluency while failing to faithfully instantiate the underlying moral and causal structure encoded in proverbs. We further show that explicit reasoning and iterative refinement can partially mitigate these failures, suggesting that many decompression errors arise from difficulties in translating abstract meaning into narrative form rather than a complete lack of relevant knowledge. Our proposed task naturally extends to other forms of compressed cultural knowledge.

[2] Know Your Limits : On the Faithfulness of LLMs as Solvers and Autoformalizers in Legal Reasoning
Large Language Models (LLMs) achieve strong performance on reasoning tasks, but whether this reflects faithful logical inference or heuristic approximation remains unclear. We study this question in legal entailment by comparing three paradigms, including pure LLM classification, LLM-based Formal Reasoning, and solver-based Formal Reasoning using the Z3 SMT solver, on a re-annotated subset of ContractNLI across five LLMs. Our re-annotation reveals a systematic and measurable gap between pragmatic legal interpretation and strict formal entailment, where a substantial proportion of legally sound inferences are not formally grounded without additional unstated assumptions. While introducing formal structure improves accuracy, with LLM-based Formal Reasoning achieving the highest benchmark performance, we show that this gain does not imply faithful reasoning. We identify three recurring failure modes: scope laundering, where LLMs report solver-inconsistent classifications without executing the underlying formal reasoning, producing conclusions that appear logically grounded but are not; implicit constraint blindness, where LLMs overlook logical constraints present in formal representations; and program synthesis failures, where LLMs generate incorrect Z3 code despite structured prompting. Critically, scope laundering persists across all models, raising serious concerns about the faithfulness of LLM-based formal reasoning as a proxy for symbolic execution. These results reveal a fundamental gap between benchmark accuracy and logical faithfulness.

[3] Lost at the End: Primacy Bias in Multimodal Retrieval-Augmented Question Answering
Knowledge-based visual question answering (KB-VQA) lets vision-language systems answer questions that exceed their parametric knowledge by conditioning a reader on passages retrieved from a Wikipedia-scale knowledge base. In pure-text long-context LLMs, retrieved-context use follows the U-shaped "lost-in-the-middle" effect of Liu et al. (2024): information at the start and end of context is used, the middle is lost. Whether this transfers to deployed multimodal KB-VQA is open. To close this gap, we design the first controlled probe of reader-side position dependence in multimodal KB-VQA: a gold-position protocol in which only the gold passage's prompt slot varies within question. We run it on three open-source 7B/8B VLM readers and two KB-VQA benchmarks at k up to 20. The shape flips from U to primacy: gold-at-first beats gold-at-last by 16 to 26 points on every reader-by-benchmark cell, an effect we call "Lost at the End". Three targeted ablations narrow the cause: a text-only control shows the multimodal setting amplifies an already-present text-mode primacy 2.2 to 4.5 times, and image-position and distractor-shuffle ablations together pin the locus to prompt slot 0 of the instruction-tuned reader. On a frozen reader, three retrieval-side fixes (MMR, oracle reranking, rank-based reordering) all leave the gap intact (no separable improvement). Our findings indicate that recall@k is the wrong metric for deployed KB-VQA and that closing the gap requires reader-side intervention; we release our protocol as a controlled instrument for evaluating such interventions.
```

---

## U100_079 — v2_train_r137_plain_c003

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `137`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the main stages of the PARSE sanitization pipeline, and what percentage of real enterprise documents does the directiveness gate route to the lightweight path?

### Claim

Structured Fact Extraction: Structured facts are extracted before rewriting. 3.

### Evidence

```text
[1] PARSE: Provenance-Aware Retrieval Sanitization for Professional Domain LLM Agents
Prompt injection defenses evaluated on synthetic benchmarks do not generalize to real enterprise documents, which are longer, denser, and interleave legitimate authority language with factual content. We demonstrate this gap with a real-document benchmark of 122 tasks across five professional domains (financial, legal, medical, scientific, DevOps) using actual SEC filings, Federal Register rules, PubMed abstracts, arXiv papers, and GitHub postmortems. Paraphrasing, the strongest defense on synthetic benchmarks, shows no statistically significant attack success rate reduction on real documents (p=0.500) while degrading utility from 91.8% to 82.8%. We introduce PARSE (Provenance-Aware Retrieval Sanitization), a domain-aware, fact-preserving sanitization pipeline that classifies each sentence by injection likelihood, extracts structured facts before rewriting, and verifies fact preservation via a consistency-checking loop. A directiveness gate routes 59% of real enterprise documents to a lightweight path, concentrating computational cost on high-risk documents. PARSE achieves 15.6% attack success rate -- a 38% reduction versus the 25.4% baseline -- at 86.9% utility, the only condition that is both statistically significant (p=0.014, adequately powered) and maintains near-baseline utility. Practitioners should evaluate defenses on domain-matched real documents, not synthetic proxies.

[2] SafeLLM: Extraction as a Hallucination-Resistant Alternative to Rewriting in Safety-Critical Settings
Large language models (LLMs) are increasingly used to access organisational documentation, including standard operating procedures (SOPs), HR policies and institutional guidelines. However, retrieval-augmented generation (RAG) systems that rely on free-form rewriting can introduce hallucinations and unstable trade-offs between completeness and conciseness, particularly in safety- and compliance-critical settings. Objectives: To evaluate extraction as a hallucination-resistant alternative to rewriting-based RAG and compare strategies that balance precision, recall and safety across document types and model scales. Methods: We compare multiple prompting strategies, including line-number-based source selection, extraction of relevant guideline sentences with explicit safety annotations, and a multi-stage pipeline that refines draft answers using supporting evidence from source guidelines. Experiments are conducted on documents of varying length and structure, including local NHS acute care and oncology guidelines and UK-wide NICE guidelines, using both frontier-scale and locally deployable models. Performance is assessed using automatic metrics and human expert evaluation of relevance and completeness. Results: Line-number selection achieves the strongest results, outperforming direct copying and safety-focused strategies across both large and small models while maintaining high term recall (up to 95%) and close alignment with source text. Safety-oriented approaches improve precision but introduce systematic omissions, while multi-stage filtering further amplifies this trade-off. Performance varies with document structure: line-based extraction excels in protocol-like content, whereas alternative strategies perform better on more verbose documents (up to 97% term recall).

[3] PersonaDrive: Human-Style Retrieval-Augmented VLA Agents for Closed-Loop Driving Simulation
Closed-loop driving simulators typically populate their environments with non-ego traffic agents that behave largely the same way, produced either by rule-based traffic managers or by learned models trained toward a single behavioral mode. Recent work introduces style variation through post-hoc labels on observational data or LLM-inferred reward weights, but these signals act as proxies for what a style should reward rather than demonstrations of humans explicitly asked to drive in that style. We introduce PersonaDrive, a pipeline that conditions a vision-language-action (VLA) driving agent on retrieved demonstrations from a style-instructed human driving dataset, in which participants drive CARLA leaderboard routes under aggressive, neutral, and conservative instructions on a driver-in-the-loop rig. The pipeline has three stages: (i) offline triplet mining over per-style human driving data using a combined image-text similarity score; (ii) training a lightweight retrieval head that fuses frozen visual features with a small control encoder over per-style databases; and (iii) fine-tuning a single VLA backbone to treat retrieved context points as in-context behavioral demonstrations during waypoint prediction. At inference, the same backbone is conditioned on any style by swapping which per-style database the retrieval head queries, so selecting a style requires no per-style retraining while enabling human-style, style-diverse non-ego agents for closed-loop simulation. On Bench2Drive, PersonaDrive (no style) improves the driving score by 4.6% over SimLingo and 2.5% over HiP-AD, and under style conditioning attains the highest driving score in every style within a roughly 2% band (its weakest style surpassing the strongest baseline, DMW, by 5.4%), while average speed and acceleration rise by 18% and 25% from the conservative to the aggressive instruction.
```

---

## U100_080 — v2_train_r100_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `100`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What did the psycholinguistic analysis reveal about differences in first-person and past-focused language between human peer responses and peer-like AI responses?

### Claim

This suggests that when providing support, human peers tend to use more personal narratives and focus more on past experiences compared to AI systems designed to sound peer-like.

### Evidence

```text
[1] When AI Says "I have been in similar situations": Synthetic Lived Experience in Peer-Like Caregiver Support
Caregivers often turn to online communities for informational and emotional support. In these spaces, peer supporters frequently draw on personal narratives to respond to emotionally complex caregiving situations. As LLMs are increasingly designed as peer-like sources of support, they introduce a critical tension: AI can provide immediate, private, and nonjudgmental support, but it cannot authentically possess the lived experiences that make human peer support meaningful. Yet, when prompted to sound peer-like, LLMs may generate language that implies lived experience. This creates a synthetic lived experience paradox: the same experiential language that may make AI support feel warm, relatable, and peer-like can also falsely position the system as someone with lived experience. We examine this paradox in the context of family caregivers of people living with Alzheimer's Disease and Related Dementias (ADRD). Drawing on caregiver support exchanges from online communities and prompted peer-like responses from three LLMs -- LLaMA, GPT-4o-mini, and MedGemma -- we analyze how human peers use personal narratives and how AI incorporates similar narrative forms. Psycholinguistic analysis shows that peer responses used significantly more first-person and past-focused language than peer-like AI responses. Qualitatively, we identify seven types of personal narratives in human peer support and show that AI often captures their emotional work, but can fabricate experiential grounding. These findings reveal a narrative authenticity gap: peer-like AI can generate synthetic lived experience without the real experience that makes peer support meaningful. We argue that caregiver-support AI systems need mechanisms to distinguish supportive peer-like framing from fabricated lived experience, ensuring that models can offer warmth and validation without falsely positioning themselves as experiential peers.

[2] Human-AI Coevolution Dynamics: A Formal Theory of Social Intelligence Emergence Through Long-Term Interaction
Current conversational AI systems have made significant progress in language generation, personalization, and long-context interaction. However, most existing methods model social behavior through isolated components such as emotion modeling, memory retrieval, or persona conditioning, lacking a unified framework to explain the emergence of stable social relationships and social intelligence in long-term human-AI interaction.To address this, we propose the Human-AI Coevolution Dynamics Framework (HACD-H), a formal model of human-AI interaction as a self-organizing social cognitive system. HACD-H integrates emotional adaptation, relational organization, social memory, and personality consistency into a unified dynamical framework and introduces principles including multi-timescale social cognition, relational attractors, trust basins, developmental phase transitions, and social cognitive energy dynamics.We construct a conversational dataset with approximately 14,700 interaction turns and develop a theory-driven empirical evaluation framework. Results reveal a hierarchy of temporal persistence in social cognition, stable relational attractors, phase-transition-like developmental patterns, and a structured social cognitive energy landscape. Social intelligence shows a significant negative correlation with social cognitive energy (r = -0.391, p < 0.001), and interaction trajectories exhibit progressive energy reduction over time.These findings suggest that social intelligence emerges from long-term social cognitive coevolution rather than isolated conversational capabilities. HACD-H provides a unified theoretical foundation for modeling adaptive human-AI social interaction and developing socially intelligent AI systems.

[3] Verifiable User Simulation for Search and Recommendation Systems
Large-language-model (LLM) based user simulation is increasingly adopted for evaluating search engines, recommender systems, and retrieval-augmented generation pipelines, yet most simulators remain opaque: it is difficult to determine why a simulated user made a particular choice or whether that choice is consistent with the intended user profile. Compounding this, recent research shows that LLMs can produce biased or discriminatory responses depending on user background characteristics such as language, education level, and cultural context, raising concerns about the equitable treatment of minority and disadvantaged groups. This half-day, in-person tutorial introduces a proposed design-and-audit framework that treats a user simulator as a verifiable engineering artefact composed of seven auditable components - structured Persona, task-aware Contract, matched human-vs-agent Execution, auditable Trace, persona-aligned Verification, structured Feedback, and a Refinement loop that updates personas and contracts. Through two hands-on mini-labs on recommendation-list evaluation and search-query formulation, participants will inspect simulator behaviour end-to-end, distinguish diagnostic discrepancy analysis from statistical validation, and apply checks for fidelity, credibility, and demographic bias. The tutorial targets information retrieval and recommender systems researchers and practitioners interested in user behaviour simulation and responsible AI.
```

---

## U100_081 — v2_train_r489_cited_c002

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `489`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

What are the four modules of the VLN-Explorer embodied navigation agent, and which one handles subgoal decomposition?

### Claim

However, based on the context of the sources, it can be inferred that a similar system might include: 1.

### Evidence

```text
[1] Compositional Skill Routing for LLM Agents: Decompose, Retrieve, and Compose
LLM agents increasingly rely on external skills -- reusable tool specifications -- but real-world tasks often require composing multiple skills, not just selecting one. We formalize this as the Compositional Skill Routing problem: given a complex user query and a large skill library, decompose the query into atomic sub-tasks, retrieve the appropriate skill for each sub-task, and compose an executable plan. We present SkillWeaver, a decompose-retrieve-compose framework combining an LLM task decomposer, a bi-encoder skill retriever with FAISS indexing, and a dependency-aware DAG planner. To support evaluation, we introduce CompSkillBench, a benchmark of 300 compositional queries over 2,209 real MCP server skills spanning 24 functional categories, sourced from the public MCP ecosystem. Our experiments reveal that task decomposition quality is the primary bottleneck: standard LLM decomposition reaches only 34.2% category recall at the step level. To address this, we propose Iterative Skill-Aware Decomposition (SAD), a retrieval-augmented feedback loop that iteratively aligns decomposition with available skills. SAD improves decomposition accuracy from 51.0% to 67.7% (+32.7%, Wilcoxon p < 10^-6) in a single iteration; DA-conditioned analysis confirms that correct granularity is the prerequisite for effective retrieval (CatR@1 rises from 34% to 41% when DA=1). SkillWeaver reduces context window consumption by over 99%, and transfer experiments confirm generalization (+35.6% relative DA gain even when target categories are absent from the retrieval pool).

[2] ACCORD: Action-Conditioned Contextual Grounding for Language Agents
User instructions are often underspecified because humans rely on implicit assumptions about the surrounding environment. For large language model (LLM) agents operating in information-rich digital and physical environments, these assumptions cannot be inferred from the instruction alone; they must be recovered from the current state of tools, data, interfaces, and observations. Effective execution therefore requires agents to identify missing context, ground it in observed evidence, and carry it forward into subsequent actions. We show that current agents often fail to do so. They act from assumed rather than observed specifics, overlook information they could have gathered, and fail to incorporate evidence that has already been returned. Building on this insight, we propose ACCORD (Action-Conditioned Contextual Grounding), a simple and effective agent framework for adaptive grounding. Before each action, ACCORD actively probes the environment for missing information and integrates relevant context from the agent's trajectory that would otherwise be overlooked. Requiring no additional training or task-success signals, ACCORD improves task-goal completion on AppWorld by up to +20.6 points with GPT-5-mini, from 42.0% to 62.6%, compared to strong baselines. These gains persist with a substantially stronger base model (+10.8 with Claude-4.5-sonnet), an open-weight model (+10.1 with Qwen3.5-27B-FP8), and on the embodied AlfWorld benchmark (+7.4 success rate with GPT-5-mini).

[3] SANA: What Matters for QA Agents over Massive Data Lakes?
Exploratory question answering (EQA) over data lakes requires an LLM agent to discover relevant sources, analyze retrieved data, and adapt its actions based on intermediate results. End-to-end accuracy alone cannot distinguish failures in search, planning, data analysis, or the agent's Action Policy: its decisions about what to do next and when to submit an answer. We present SANA (Search Agent Navigation Ablation framework), a diagnostic ablation framework that transforms EQA tasks into runtime profiles containing gold source sequence, sanitized subquestions, and execution records. SANA uses these profiles to construct idealized search, planning, and data-analysis tools, allowing each component to be ablated; the residual gap is diagnostic evidence for policy failures. To illustrate SANA as a reusable evaluation framework, we adapted two recent EQA benchmarks, LakeQA and KramaBench, and evaluated lightweight and mid-sized agents under fixed prompts, budgets, data lakes, and runtimes. Across both benchmarks, data analysis is a consistent bottleneck while planning is less so. Search is a major limitation in LakeQA's large data-lake setting, but less so for the smaller-scale KramaBench. SANA thus deconstructs end-to-end task accuracies into a diagnosis of where data-lake agents fail, and allows for systematic comparisons of progress in search, planning, data analysis, and agent design.
```

---

## U100_082 — v2_train_r527_cited_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `527`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

What are the four reward components in the RLHF reward decomposition used by the AgentForge planning framework, and what relative weights are assigned to each?

### Claim

The question asks for the four reward components in the RLHF reward decomposition used by the AgentForge planning framework, and what relative weights are assigned to each.

### Evidence

```text
[1] TASR: Training-Free Adaptive Stopping for Iterative Retrieval
Iterative retrieval-augmented generation agents commonly overspend by continuing to retrieve after the model has converged on an answer, incurring calls that change neither the prediction nor the supporting evidence. Existing remedies learn a stopping policy from labeled trajectories, tying the decision to a trained component that requires retraining for each new model or task. We propose TASR (Training-Free Adaptive Stopping Rule), a one-line predicate that fires when the model repeats its previous-round normalized answer and the isotonically calibrated logit margin exceeds 0.25. No classifier or value head is learned; the threshold is fixed across all twenty-four (model, retriever, corpus) configurations we evaluate. On a 3-model x 2-dataset distractor grid, TASR retains 94.8% of fixed-k=5's macro F1 at 62.6% of its calls and exceeds fixed-k=3 by +3.42 F1. The pattern holds on nine open-domain BM25 cells (55.01 F1 at 2.98 calls vs. 54.33 at 3.00 for fixed-k=3) and, with calibration locked from the distractor split, on nine dense-retrieval cells across two retriever families, with zero significant regressions in either extension. The rule was selected from an exhaustive enumeration of 381 candidate stopping rules; no alternative Pareto-dominates it on any evaluated configuration. A signal-quality analysis shows that verbalized 1-5 confidence collapses on RLHF-tuned models (96.5% of values equal 5, entropy 0.182 nats), while the logit margin achieves 44x better class-conditional separation, grounding the design in a measurable model pathology. TASR is an auditable, training-free Pareto baseline against which learned stopping controllers can be compared. Code is publicly available.

[2] Beyond Reward Engineering: A Data Recipe for Long-Context Reinforcement Learning
Long-context reasoning is an essential capability for large language models, particularly when they are deployed as autonomous agents that must reason over lengthy trajectories. Reinforcement learning (RL) has recently emerged as a dominant paradigm for improving this ability, yet existing work largely focuses on reward engineering while diverse training data remains scarce. We revisit this problem from a data-centric perspective and show that a simple yet effective data recipe alone, paired with a minimal outcome-based GRPO setup, suffices to substantially improve long-context reasoning. Our recipe targets three complementary task families -- retrieval, multi-evidence synthesis, and reasoning -- for which we construct and curate eight datasets totaling ~14K examples. Experiments on three models (Qwen3-4B/8B/30B-A3B) yield average gains of +7.2/+3.2/+6.4 points across seven long-context benchmarks, surpassing prior RL training sets. We further demonstrate that these gains transfer to agentic tasks, where continuing RL training on an agent-tuned model with our data recipe improves GAIA by +4.8 and BrowseComp by +7.0 points. We will release our datasets to facilitate future research.

[3] Learning User Simulators with Turing Rewards
Learning to simulate human users in interactive settings could advance the training of agent assistants, evaluation of personalization systems, research in the social sciences, and more. Existing approaches generally do so by training a large language model (LLM) to match a single ground truth response, either by maximizing the log probability or by using a similarity reward. We instead propose {Turing-RL}: a Turing-Test-based reinforcement learning approach for training user simulator models. {Turing-RL} uses a discriminative Turing reward with an LLM judge to score how indistinguishable a generated response is from the real user's given the user's history, and the user simulator LLM learns to produce responses indistinguishable from what the user could have said with such rewards. Across two different domains--conversational chat and Reddit forum discussion--we find that {Turing-RL} consistently outperforms baseline methods on both LLM and human evaluation metrics. Our study suggests that optimizing for indistinguishability, rather than response matching, is effective for learning user simulators.
```

---

## U100_083 — v2_train_r403_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `403`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

How many models and how many German-language datasets does MÖVE use in its evaluation, and what types of datasets were constructed for public-administration domains?

### Claim

The evaluation involves ten German-language datasets, including gold- and silver-standard datasets that were constructed to reflect public-administration domains.

### Evidence

```text
[1] MÖVE: A Holistic LLM Benchmark for the German Public Sector
We present MÖVE (Modelle für die Öffentliche Verwaltung Evaluieren), a holistic benchmark for evaluating large language models (LLMs) in the context of the German public sector. While LLMs are increasingly adopted in public administration, model selection remains largely ad hoc, and existing benchmarks offer limited guidance: they are predominantly English-centric, US-centric in content, and focus exclusively on task performance. MÖVE addresses these gaps by evaluating 39 models across two complementary dimensions. Performance criteria cover summarization, question answering, and topic extraction. Governance criteria assess hallucination tendencies, energy consumption, provider transparency, and alignment with German constitutional values and knowledge about positions by German political parties. In total, we utilize ten German-language datasets, including gold- and silverstandard datasets that we constructed to reflect public-administration domains. We employ a multi-metric evaluation strategy combining classical NLP metrics, embedding-based methods, and LLM-as-a-judge approaches. Our results show that no single model dominates across all criteria: top performers differ between tasks, and model size alone is a poor predictor of quality. We further evaluate the benchmark itself, analyzing its statistical precision, LLM judge reliability, the impact of our private datasets on model rankings, the sensitivity of our results to prompt formulation, and the validity of our energy consumption estimates. MÖVE is designed as a living benchmark under active development; results are publicly available at https://moeve.bundesdruckerei.de/.

[2] SkMTEB: Slovak Massive Text Embedding Benchmark and Model Adaptation
We introduce SkMTEB, the first comprehensive MTEB-style text embedding benchmark for Slovak, a low-resource West Slavic language, comprising 31 datasets across 7 task types -- nearly 4$\times$ the depth of existing multilingual benchmark coverage for Slovak. Our evaluation of 31 embedding models reveals that large instruction-tuned multilingual models achieve the strongest performance, while existing Slovak-specific models trained for NLU tasks transfer poorly to embedding tasks. To address the need for efficient, locally-deployable Slovak embeddings, we develop \texttt{e5-sk-small} (45M parameters) and \texttt{e5-sk-large} (365M) by applying vocabulary trimming and fine-tuning to Multilingual E5 models. Despite size reductions of up to 62\%, our open-source models achieve competitive performance with proprietary APIs while remaining locally deployable for semantic search and retrieval-augmented generation (RAG). We release the benchmark, models, datasets, and code openly, hoping our approach offers a replicable path for other under-resourced languages.

[3] NRITYAM: Language Models Meet Art and Heritage of Dance
Language models have become essential tools in shaping modern workflows. However, their global effectiveness hinges on a nuanced understanding of local socio-cultural contexts. To address this gap, we present NRITYAM, a comprehensive benchmark for evaluating the cultural comprehension capabilities of language models in the context of global dance traditions. NRITYAM comprises 9,260 carefully curated question-answer pairs spanning 12 languages, making it the largest dataset dedicated to evaluating cultural knowledge in dance. The dataset has been developed from the ground up through close collaboration with native dance artists and native speakers of the languages, who authored and validated culturally relevant questions specific to their regions. We evaluate a broad set of models, including large language models, small language models, multimodal large language models, and small multimodal language models. As a multilingual and multicultural benchmark, NRITYAM sets a new standard for evaluating the ability of AI systems to understand and reason about traditional performing arts. Detailed dataset samples are available at~\url{https://github.com/niladrighosh03/NRITYAM}.
```

---

## U100_084 — v2_train_r376_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `376`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What specific limitations does IVIE exhibit regarding puzzle constraints and objective validation?

### Claim

IVIE exhibits specific limitations regarding puzzle constraints and objective validation.

### Evidence

```text
[1] IVIE: A Neuro-symbolic Approach to Incremental and Validated Generation of Interactive Fiction Worlds
Computational creativity in Interactive Fiction faces a fundamental tension: Large Language Models (LLM) may produce creative narratives but struggle with world coherence, while symbolic systems ensure consistency but lack creative flexibility. We present IVIE (Incremental & Validated Interactive Experiences), a neuro-symbolic approach to generating complete and playable interactive fiction worlds from scratch. Building upon PAYADOR's neuro-symbolic framework, IVIE implements a four-stage incremental generation pipeline that delegates creative decisions--setting and character creation, puzzle design--to LLMs while grounding the world state through symbolic validation. The system generates worlds with interconnected locations, functional items, non-player characters, and coherent puzzles, all structured around a central goal-oriented architecture. Human evaluation shows the approach generates immersive, thematically coherent worlds with high player engagement. Results seem to indicate that the neuro-symbolic approach successfully balances flexibility with narrative coherence: symbolic validation grounds LLM generation without eliminating generative freedom. However, challenges remain: LLM inconsistencies occasionally bypass puzzle constraints, and objective validation gaps allow some structurally impossible goals. We identify key design considerations for future neurosymbolic interactive storytelling systems, particularly regarding LLM capabilities and their limitations.

[2] AIPatient Arena: EHR-grounded evaluation of large language models in end-to-end clinical consultation workflows
Large language models (LLMs) are increasingly considered for use in clinical consultation tasks, yet most medical evaluations remain static, single-turn, or narrowly outcome-based, limiting their ability to reflect the sequential, uncertain, and interactive nature of real-world care. Here, we propose AIPatient Arena, an EHRs-grounded evaluation framework for assessing the clinical utility of LLMs across eight dimensions of clinical competence. The framework integrates EHR data into patient-specific knowledge graphs, enabling multi-turn physician-patient interactions. We applied AIPatient Arena on a primary cohort of 437 patients and two out-of-distribution validation cohorts of 119 and 67 patients. We observe that LLMs performed well in medical interview questioning skills (QS; mean scores, 4.43-4.99/5), ethical and professional conduct (ET; 4.38-4.93/5), and clarity and transparency of clinical explanations (EX; 3.80-4.72/5). Performance was moderate in information integration (II; 3.19-4.21/5) and medication safety and justification (MS; 3.13-3.78/5), but persistent weaknesses were observed in handling of ambiguous patient responses (HR; 2.57-3.32/5), information coverage (IC; 2.08-3.02/5), and diagnostic accuracy and reasoning (Dx; 2.63-3.55/5). Process-based evaluation revealed recurrent interaction failures, including repetitive questioning, omission of past medical history, and inadequate handling of uncertainty. Richer conversational context improved diagnostic reasoning but yielded limited gains in treatment planning. These findings indicate that final-answer accuracy alone is insufficient for evaluating clinical readiness and highlight the importance of assessing how models gather, interpret, and communicate information throughout a consultation. AIPatient Arena provides an EHR-grounded framework for workflow-oriented pre-deployment evaluation of medical LLMs.

[3] OneBar: An End-to-End Content-Grounded Generative Query Recommendation Framework for E-Commerce Video Feeds
Short-video platforms now expose clickable search entries beneath the video player, enabling users to easily express content-induced search intent. However, conventional query recommendation systems on short-video platforms suffer from latency constraints and objective misalignment, while recent generative approaches struggle with noisy content-side metadata and preference drift. To address these issues, we propose OneBar, an end-to-end generative framework for real-time query recommendation for E-Commerce video feeds. OneBar features three key innovations: (1) a collaborative-multimodal intent grounding module that fuses multimodal video understanding and behavior-derived collaborative anchors; (2) a Unified End-to-End architecture equipped with a prompt-compression mechanism for efficient online serving; and (3) a progressive preference learning strategy for efficient preference-internalization, which internalizes hierarchical behavior preferences into the generative policy, eliminating the need for a separately trained reward model. Compared with online base, OneBar increases Query Exposure by 16.91\% and Query Click by 18.68\%, while maintaining a slight Query CTR gain of 0.19\%. The additional search traffic further contributes to 20.36\% more guided orders and 21.67\% higher GMV.
```

---

## U100_085 — v2_train_r239_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `239`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

According to the evaluations, along what dimensions does ARVRE outperform existing approaches for generating Physics Word Problems?

### Claim

According to the evaluations, ARVRE outperforms existing approaches for generating Physics Word Problems in the dimensions of complexity, novelty, and solvability.

### Evidence

```text
[1] Agentic Retrieval and Reinforcement Learned Equation Chains: A Controlled Generation Framework for Complex and Novel Physics Word Problems
Generating high-quality Physics Word Problems (PWPs) that are novel, complex, and solvable remains a challenging and underexplored problem in educational content generation. Existing approaches, many adapted from Math Word Problem (MWP) generation, often produce ambiguous, unsolvable, or structurally simple questions with limited linguistic diversity. We introduce ARVRE (Agentic Retrieval Value Reinforced Equation-chain), a two-stage framework for generating diverse and mathematically valid PWPs. In the first stage, a form of offline temporal-difference learning is used to construct valid chains of physics equations, while an agentic retrieval-augmented generation (RAG) framework dynamically selects topic-specific concepts and vocabulary. This design enables explicit control over problem structure and difficulty. In the second stage, a Large Language Model (LLM) converts the equation chain and retrieved concepts into a natural-language physics question. By grounding generation in valid equation chains, our method preserves mathematical correctness while promoting linguistic diversity and contextual richness. Human and automated evaluations demonstrate that ARVRE generates PWPs that are more complex, novel, and solvable than those produced by existing approaches. These results highlight the potential of combining reinforcement learning, retrieval, and LLMs for reliable generation of educational physics content.

[2] Learning User Simulators with Turing Rewards
Learning to simulate human users in interactive settings could advance the training of agent assistants, evaluation of personalization systems, research in the social sciences, and more. Existing approaches generally do so by training a large language model (LLM) to match a single ground truth response, either by maximizing the log probability or by using a similarity reward. We instead propose {Turing-RL}: a Turing-Test-based reinforcement learning approach for training user simulator models. {Turing-RL} uses a discriminative Turing reward with an LLM judge to score how indistinguishable a generated response is from the real user's given the user's history, and the user simulator LLM learns to produce responses indistinguishable from what the user could have said with such rewards. Across two different domains--conversational chat and Reddit forum discussion--we find that {Turing-RL} consistently outperforms baseline methods on both LLM and human evaluation metrics. Our study suggests that optimizing for indistinguishability, rather than response matching, is effective for learning user simulators.

[3] AIPatient Arena: EHR-grounded evaluation of large language models in end-to-end clinical consultation workflows
Large language models (LLMs) are increasingly considered for use in clinical consultation tasks, yet most medical evaluations remain static, single-turn, or narrowly outcome-based, limiting their ability to reflect the sequential, uncertain, and interactive nature of real-world care. Here, we propose AIPatient Arena, an EHRs-grounded evaluation framework for assessing the clinical utility of LLMs across eight dimensions of clinical competence. The framework integrates EHR data into patient-specific knowledge graphs, enabling multi-turn physician-patient interactions. We applied AIPatient Arena on a primary cohort of 437 patients and two out-of-distribution validation cohorts of 119 and 67 patients. We observe that LLMs performed well in medical interview questioning skills (QS; mean scores, 4.43-4.99/5), ethical and professional conduct (ET; 4.38-4.93/5), and clarity and transparency of clinical explanations (EX; 3.80-4.72/5). Performance was moderate in information integration (II; 3.19-4.21/5) and medication safety and justification (MS; 3.13-3.78/5), but persistent weaknesses were observed in handling of ambiguous patient responses (HR; 2.57-3.32/5), information coverage (IC; 2.08-3.02/5), and diagnostic accuracy and reasoning (Dx; 2.63-3.55/5). Process-based evaluation revealed recurrent interaction failures, including repetitive questioning, omission of past medical history, and inadequate handling of uncertainty. Richer conversational context improved diagnostic reasoning but yielded limited gains in treatment planning. These findings indicate that final-answer accuracy alone is insufficient for evaluating clinical readiness and highlight the importance of assessing how models gather, interpret, and communicate information throughout a consultation. AIPatient Arena provides an EHR-grounded framework for workflow-oriented pre-deployment evaluation of medical LLMs.
```

---

## U100_086 — v2_train_r527_plain_c001

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `527`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `bait`

### Question

What are the four reward components in the RLHF reward decomposition used by the AgentForge planning framework, and what relative weights are assigned to each?

### Claim

The sources provided do not contain information about the reward components in the RLHF reward decomposition used by the AgentForge planning framework, or the relative weights assigned to each.

### Evidence

```text
[1] TASR: Training-Free Adaptive Stopping for Iterative Retrieval
Iterative retrieval-augmented generation agents commonly overspend by continuing to retrieve after the model has converged on an answer, incurring calls that change neither the prediction nor the supporting evidence. Existing remedies learn a stopping policy from labeled trajectories, tying the decision to a trained component that requires retraining for each new model or task. We propose TASR (Training-Free Adaptive Stopping Rule), a one-line predicate that fires when the model repeats its previous-round normalized answer and the isotonically calibrated logit margin exceeds 0.25. No classifier or value head is learned; the threshold is fixed across all twenty-four (model, retriever, corpus) configurations we evaluate. On a 3-model x 2-dataset distractor grid, TASR retains 94.8% of fixed-k=5's macro F1 at 62.6% of its calls and exceeds fixed-k=3 by +3.42 F1. The pattern holds on nine open-domain BM25 cells (55.01 F1 at 2.98 calls vs. 54.33 at 3.00 for fixed-k=3) and, with calibration locked from the distractor split, on nine dense-retrieval cells across two retriever families, with zero significant regressions in either extension. The rule was selected from an exhaustive enumeration of 381 candidate stopping rules; no alternative Pareto-dominates it on any evaluated configuration. A signal-quality analysis shows that verbalized 1-5 confidence collapses on RLHF-tuned models (96.5% of values equal 5, entropy 0.182 nats), while the logit margin achieves 44x better class-conditional separation, grounding the design in a measurable model pathology. TASR is an auditable, training-free Pareto baseline against which learned stopping controllers can be compared. Code is publicly available.

[2] Beyond Reward Engineering: A Data Recipe for Long-Context Reinforcement Learning
Long-context reasoning is an essential capability for large language models, particularly when they are deployed as autonomous agents that must reason over lengthy trajectories. Reinforcement learning (RL) has recently emerged as a dominant paradigm for improving this ability, yet existing work largely focuses on reward engineering while diverse training data remains scarce. We revisit this problem from a data-centric perspective and show that a simple yet effective data recipe alone, paired with a minimal outcome-based GRPO setup, suffices to substantially improve long-context reasoning. Our recipe targets three complementary task families -- retrieval, multi-evidence synthesis, and reasoning -- for which we construct and curate eight datasets totaling ~14K examples. Experiments on three models (Qwen3-4B/8B/30B-A3B) yield average gains of +7.2/+3.2/+6.4 points across seven long-context benchmarks, surpassing prior RL training sets. We further demonstrate that these gains transfer to agentic tasks, where continuing RL training on an agent-tuned model with our data recipe improves GAIA by +4.8 and BrowseComp by +7.0 points. We will release our datasets to facilitate future research.

[3] Learning User Simulators with Turing Rewards
Learning to simulate human users in interactive settings could advance the training of agent assistants, evaluation of personalization systems, research in the social sciences, and more. Existing approaches generally do so by training a large language model (LLM) to match a single ground truth response, either by maximizing the log probability or by using a similarity reward. We instead propose {Turing-RL}: a Turing-Test-based reinforcement learning approach for training user simulator models. {Turing-RL} uses a discriminative Turing reward with an LLM judge to score how indistinguishable a generated response is from the real user's given the user's history, and the user simulator LLM learns to produce responses indistinguishable from what the user could have said with such rewards. Across two different domains--conversational chat and Reddit forum discussion--we find that {Turing-RL} consistently outperforms baseline methods on both LLM and human evaluation metrics. Our study suggests that optimizing for indistinguishability, rather than response matching, is effective for learning user simulators.
```

---

## U100_087 — v2_train_r309_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `309`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

How does GitOfThoughts map an agent's reasoning tree onto git primitives, such as commits, notes, and tags?

### Claim

In GitOfThoughts, every scored thought is mapped to a commit.

### Evidence

```text
[1] GitOfThoughts: Version-Controlled Reasoning and Agent Memory You Can Replay, Diff, and Merge
Large language model (LLM) reasoning is ephemeral: chains of thought vanish with the context window, pruned search branches leave no record, and memory buffers cannot be diffed, merged, or audited. Every other complex software process (code, infrastructure, data, experiments) is version-controlled; reasoning is not. We introduce GitOfThoughts, which stores an agent's reasoning tree as a git repository: every scored thought is a commit, scores are notes, outcomes are tags, and retrieval is "git log" over the agent's own history. This makes reasoning replayable, auditable, and mergeable across agents at near-zero engineering cost. We then ask the harder question: does memory, in any substrate, actually improve accuracy? Across five substrates (none, markdown, vector, graph, git), two benchmarks, two model scales, and pre-registered replications, the answer for novel problems is no. No memory format reliably helps, and a promising early result collapsed under its own pre-registered replication. Memory pays only above what we call the copyability threshold: when the retrieved case is a near-duplicate of the current problem (similarity >~ 0.8), accuracy jumps sharply; below it, nothing. The gain is answer retrieval, not method transfer: a 4.5x larger model doubles the near-duplicate payoff yet still cannot extract a transferable method from a worked example. The only general lever we find is test-time sampling. The case for git-as-substrate is therefore auditability, provenance, and mergeability at accuracy parity. We document a retracted result and a refuted hypothesis to model the evaluation standard we hold ourselves to.

[2] VeriGraph: Towards Verifiable Data-Analytic Agents
LLM-based agents have demonstrated strong capabilities in data-intensive analytical tasks, yet their outputs are rarely verifiable: a reliance on linear text trajectories makes their reasoning difficult to audit. In particular, deterministic computations over raw data and semantic deductions over natural-language claims are often entangled in an unstructured stream, leaving numerical conclusions hard to reproduce and qualitative judgments hard to inspect. To address this, we propose VeriGraph, a traceable neuro-symbolic reasoning framework that enables agents to construct an explicit heterogeneous evidence directed acyclic graph (DAG) during execution. VeriGraph introduces three evidence-expansion primitives, namely computational, grounding, and derivational expansion, to connect raw data, interpreter variables, computed results, and natural-language claims in a unified graph. Under this formulation, structural traceability is reduced to graph reachability from raw data sources to terminal claims, while semantic support is measured by claim-level evidence evaluation. To improve graph construction, we further design a graph-based policy optimization strategy with a composite reward that jointly supervises answer correctness, computational integrity, and derivational coherence. Experiments on four benchmarks show that VeriGraph-8B achieves the highest overall score among all baselines. More importantly, VeriGraph produces auditable evidence graphs with substantially stronger claim grounding, achieving a 87.61\% Grounding Rate under our claim-level evidence support evaluation. These results suggest that explicit evidence-graph construction is a promising path toward verifiable data-analytic agents. Our code is available at https://github.com/ignorejjj/VeriGraph.

[3] Beyond Domains: Reusing Web Skills via Transferable Interaction Patterns
Large language model (LLM) web agents are usually deployed as tool callers: each turn, the model reads a fresh page observation and emits one structured tool action. When every action is a low-level primitive, horizons grow quickly and so do policy-facing LLM completions, dominating latency and cost on benchmarks such as Mind2Web and WebArena. Recent systems therefore wrap repeated interaction fragments as web skills: callable tools built from successful trajectories or induced programs, so one call can replace several primitives. However, prior skill libraries are still triggered mainly by instruction similarity or coarse site metadata, which yields low skill reuse on held-out sites and leaves much of the potential step and token reduction on the table. We present SkillMigrator, an agent that learns reusable web skills and transfers them across sites by matching layout structure rather than specific element references. Each induced skill is stored as a transferable interaction pattern (TIP): the skill paired with a structural sketch of the snapshot at induction time. At test time, SkillMigrator retrieves TIPs by layout similarity and grounds their references on the live page. The rest of the stack is standard: accessibility-snapshot observations with stable references, and fixed tool calling over primitives plus skill invocations. Compared with the state-of-the-art approaches, SkillMigrator reduces the average LLM-action count on successful trajectories by 8-10% across both WebArena and Mind2Web at matched success rate.
```

---

## U100_088 — v2_train_r212_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `212`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What types of feedback do the generative reward models provide to enable the policy to iteratively refine ad descriptions?

### Claim

This feedback includes evaluations of knowledge capacity, landing page consistency, and reasoning feedbacks.

### Evidence

```text
[1] Interactor: Agentic RL oriented Iterative Creation for Ad Description Generation in Sponsored Search
This paper focuses on automatically generating informative ad descriptions in sponsored search. Unlike ad titles which are usually optimized to attract user click feedbacks, ad descriptions have a longer text span and possess the potential of incorporating world knowledge to address user search intents while presenting the fine-grained selling points of the ads. We propose Interactor, a multi-turn iterative creation framework optimized with agentic RL for ad description generation. The generation model acts as a policy that interacts with a customized environment consisting of multiple generative reward models. Given initial generations by the policy, the customized GenRMs evaluate multi-dimensional qualities including knowledge capacity and landing page consistency, providing both binary signals and reasoning feedbacks. The policy then iteratively refines the descriptions based on such feedbacks to ensure continuous improvement. Experiments on industrial datasets show that the Interactor framework significantly outperforms state-of-the-art approaches in generating knowledge-rich and faithful ad descriptions. Since May 2026, it has been deployed online in a leading search ads system, contributing to both ad revenue and user experience.

[2] BALTO: Balanced Token-Level Policy Optimization for Hallucination Mitigation
Hallucinations remain a major obstacle to deploying large language models (LLMs) in knowledge-intensive settings, where generated responses must be faithfully grounded in provided evidence. Reinforcement learning (RL) is a promising direction for hallucination mitigation, but response-level faithfulness rewards suffer from a granularity mismatch: localized hallucinations can cause supported content to receive spurious penalties. Although recent work introduces fine-grained feedback such as claim-level verification and token-level rewards, unbalanced credit assignment can still induce length, verbosity, or optimization-noise biases. We propose BALTO, a Balanced Token-level Policy Optimization framework for hallucination mitigation. BALTO extracts checkable factual claims, verifies them against the reference context, and projects claim-level judgments to token-level labels. A balanced token-level credit assignment mechanism is introduced into the framework. This design redistributes probability mass from unsupported content toward faithful content, rather than suppressing the entire response. We systematically analyze the limitations of response-level rewards from a theoretical standpoint, and prove BALTO's advantages in training stability and optimization efficiency for hallucination mitigation. Experiments on ConFiQA, RAGTruth, and FinLLM-Eval show that BALTO achieves the highest faithfulness across all six model--benchmark settings and consistently outperforms existing post-training baselines in Q-Score, demonstrating a stronger faithfulness--informativeness trade-off.

[3] Be My Tutor: On-Policy Co-Distillation for Mutual LLM Improvement via Peer Feedback
We study multi-domain LLM training in which two models, each stronger in a different domain, co-evolve by tutoring each other through on-policy feedback. Unlike one-way distillation or single-model fine-tuning, our goal is mutual Pareto improvement: each model improves across domains without losing its original strength. To this end, we propose On-Policy Co-Distillation (OPCoD), where each student's self-distillation is conditioned on its own correct rollout and feedback from its peer. To make feedback exchange effective, OPCoD uses cognizance-based gating to decide when to give feedback and feedback anchoring to ground feedback in the problem. On Science Q\&A tasks, OPCoD consistently outperforms baselines and achieves Pareto improvement across all evaluated domain pairs and students.
```

---

## U100_089 — v2_train_r72_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `72`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What mechanism does Morpheus use to convert per-character boundary probabilities into soft morpheme memberships during training while ensuring exact segments at inference?

### Claim

This program turns these probabilities into soft morpheme memberships during training, and at inference, it produces exact segments with no string normalization, so $\mathrm{decode}(\mathrm{encode}(w)) = w$ holds by construction.

### Evidence

```text
[1] Morpheus: A Morphology-Aware Neural Tokenizer and Word Embedder for Turkish
Turkish is agglutinative: meaning is carried by morphemes, yet the subword tokenizers that drive modern language models split words by corpus statistics, fragmenting semantically loaded suffixes and -- in the case of WordPiece and rule-based analyzers -- failing to decode their output back to the original text. This paper presents \textbf{Morpheus}, a neural morpheme-boundary model for Turkish that is at once a lossless, morphology-aware tokenizer and a word-embedding producer. A differentiable Poisson-binomial dynamic program turns per-character boundary probabilities into soft morpheme memberships during training and exact segments at inference, with no string normalization, so $\mathrm{decode}(\mathrm{encode}(w)) = w$ holds by construction. Because the model is neural, the same forward pass that tokenizes also emits a structured word embedding. Among reversible tokenizers -- the only ones valid for generation -- Morpheus attains the lowest bits-per-character ($1.425$), roughly doubles the gold morphological alignment of the subword family (MorphScore macro-F1 $0.61$ vs.\ ${\sim}0.32$), and uses ${\sim}19\%$ less GPU memory than 64K-vocabulary subword tokenizers. As an embedder, frozen Morpheus vectors lead on lexical retrieval (root-family MAP $0.85$) and same-root verification (ROC-AUC $1.00$), surpassing the multilingual retriever BGE-M3 and BERTurk; on context- and inflection-dependent tasks (NER, case/number probing) the heavier contextual encoders remain ahead -- a trade-off we attribute to Morpheus's root-centric geometry. Code: https://github.com/lonewolf-rd/TurkishMorpheus; model: https://huggingface.co/lonewolflab/Morpheus-TR-50K; interactive demo: https://huggingface.co/spaces/lonewolflab/morpheus-tr-demo.

[2] Self-Generated Error Training for Token Editing in Diffusion Language Models
Token-to-token (T2T) editing lets LLaDA2.1 revise committed tokens during block-diffusion decoding. The released recipe trains this editor on random vocabulary corruptions, but at inference the editor sees the model's own fluent, high-confidence draft errors instead. We study this training-inference mismatch and propose self-generated T2T, which performs a no-gradient draft pass, fills masked positions with predicted tokens, and supervises recovery in a second pass under these self-generated corruptions. We implement the update as a short LoRA continued-pretraining pass on LLaDA2.1-mini and evaluate on several benchmarks under the official Q-Mode T2T procedure with unchanged inference parameters. The method generally improves accuracy while reducing T2T edit intensity, mitigating failure modes such as final-digit transcription errors after otherwise correct reasoning and excessive self-correction before short factual answers.

[3] MARD: Mirror-Augmented Reasoning Distillation for Mechanism-Level Drug-Drug Interaction Prediction
Mechanism-level drug-drug interaction (DDI) prediction requires identifying which enzyme or pharmacodynamic axis is implicated, in which direction, and with which evidence -- not merely whether two drugs interact. We introduce a reproducible mechanism-level DDI labelling and evaluation protocol with a structured 7-family/147-subtype taxonomy, leakage-safe cold-split protocols, and auditable reasoning metrics for evaluating pharmacological prediction beyond flat interaction classification. We propose a pipeline that produces a 7B reasoning MARD (Mirror-Augmented Reasoning Distillation), combining three training innovations: a single-token KL divergence on direction tag that ties the model's prediction, per-loss PRM-weighted DPO with programmatic hard negatives, and a leakage-safe mechanism-aware retrieval channel. Process-reward step labels are automatically verifiable against DrugBank-structured fields, requiring no human or LLM judges. On the April-2026 DrugBank release, our MARD-7B is the only system in a 32-system comparison whose accuracy survives drug-pair novelty, beating the best baseline by +13.9 pp and GPT-4o by +6.7 pp at ~1% of frontier API cost. Further analysis reveals an anti-memorisation signature where accuracy improves on rarely seen drugs, suggesting that gain comes from structured pharmacological reasoning rather than drug-frequency memorisation. We release corpus, DDI-PRM, retrieval index, and training code.
```

---

## U100_090 — v2_train_r60_plain_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `60`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What root cause does the paper identify for the performance degradation and training collapse observed when using backbones with large MLM-head L2 norms under standard SPLADE training?

### Claim

This mismatch amplifies sparse activations, distorts matching scores, and destabilizes contrastive training under common training settings.

### Evidence

```text
[1] Rescaling MLM-Head for Neural Sparse Retrieval
Learned sparse retrieval (LSR) models such as SPLADE have traditionally used BERT-style masked language models as backbone encoders. A natural expectation is that replacing BERT with stronger pretrained encoders should improve retrieval effectiveness. However, we find that under standard SPLADE training recipes, backbones with large MLM-head L2 norms can suffer performance degradation and even training collapse under standard SPLADE training recipes. We identify this failure as a scale mismatch in the MLM head: SPLADE directly uses MLM-head outputs to construct sparse lexical representations, and query-document relevance is computed by an unnormalized dot product over these representations. As a result, an inflated MLM-head scale can amplify sparse activations, distort matching scores, and destabilize contrastive training under common training settings. To address this issue, we introduce a simple initialization-time correction that rescales the MLM-head projection by a constant factor before SPLADE training. This zero-cost adjustment improves training stability without modifying the model architecture or training objective. Across both in-domain and out-of-domain retrieval benchmarks, this simple correction substantially improves large-norm backbones such as ModernBERT and Ettin, turning unstable training runs into competitive sparse retrievers. In several settings, the corrected models further match or surpass the classic BERT-SPLADE baseline. These findings suggest that the bottleneck in adapting pretrained encoders to LSR is not encoder capacity alone, but the calibration of the MLM-head scale used to construct sparse lexical representations.

[2] The Wrong Kind of Right: Quantifying and Localizing Misfired Alignment in LLMs
Warning: This paper studies stereotypes and biases, and contains potentially disturbing examples, used for illustration purposes only. Our findings should not be interpreted as an argument against alignment. Instead, this paper highlights the need for principled approaches to more advanced alignment. Alignment aims to ensure that large language models (LLMs) behave safely and reliably, including by avoiding unsafe inferences. However, we show that such safety-oriented behaviors can misfire: models may reject warranted conclusions even when they are explicitly supported by context. We call this failure mode misfired alignment, where alignment-induced changes cause LLMs to override explicit evidence. To quantify this phenomenon, specifically on stereotype-related alignment, we introduce VETO, a benchmark consisting of 2,032 BBQ-derived contrastive pairs, and define a new metric, Misfired Alignment Rate (MAR), which measures on a 0 to 100 scale how often a model fails on a stereotype-related question but succeeds on its contrastive counterpart. We benchmark 25 LLMs on VETO, and show that all LLMs, including the most recent ones, exhibit non-trivial (4.7 to 18.9%) MARs while all human participants achieve 0.0% MAR. Controlled priming experiments further show that alignment-induced cues can substantially amplify MAR across LLMs, indicating that these failures are not merely artifacts of individual examples but can be induced by safety-related framing. Mechanistic analyses on open-weight LLMs reveal late-layer suppression of evidence-supported answers, and comparisons between instruct and base LLMs suggest that this suppression emerges after instruction training. These findings show that current alignment methods can overgeneralize surface-level safety cues, to the point of overriding objective evidence, motivating more work on alignment objectives that better preserve contextual grounding.

[3] Implicit Reasoning for Large Language Model-based Generative Recommendation
Large Language Models (LLMs) are increasingly adopted as backbones for Generative Recommendation (GR), promising access to pretrained world knowledge. Yet reliably invoking this knowledge for GR remains poorly understood. A key obstacle is that LLM-based GR typically represents items with Semantic IDs (SIDs), disrupting LLMs' natural-language reasoning interface because these tokens are unseen by the LLM during pretraining. Existing approaches address this with expensive multi-stage pipelines that ground SIDs and elicit explicit rationales, but offer limited insight into when and why each stage is necessary. In this work, we systematically decompose explicit reasoning training pipelines for LLM-based GR, revealing three key limitations: weakened world-knowledge verbalization, misalignment between SID and natural-language token embedding spaces, and sensitivity to rationale quality, all of which hurt explicit reasoning performance. To circumvent these issues, we propose PauseRec, a lightweight implicit reasoning paradigm tailored for GR. PauseRec is exceptionally practical, avoiding costly reasoning trace acquisition and reasoning alignment training, leading to a multitude of benefits: (1) it outperforms standard explicit CoT methods by up to 6.22%, (2) it reduces training cost by up to 65% GPU hours, and (3) it speeds up inference by up to 71.3%. These results position PauseRec as a lightweight alternative to explicit rationale generation, enabling more effective and efficient LLM-based GR.
```

---

## U100_091 — v2_train_r489_cited_c006

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `489`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `bait`

### Question

What are the four modules of the VLN-Explorer embodied navigation agent, and which one handles subgoal decomposition?

### Claim

Action-Conditioned Contextual Grounding (from ) The source does present a decompose-retrieve-compose framework, but it does not explicitly state that it is part of a VLN-Explorer agent.

### Evidence

```text
[1] Compositional Skill Routing for LLM Agents: Decompose, Retrieve, and Compose
LLM agents increasingly rely on external skills -- reusable tool specifications -- but real-world tasks often require composing multiple skills, not just selecting one. We formalize this as the Compositional Skill Routing problem: given a complex user query and a large skill library, decompose the query into atomic sub-tasks, retrieve the appropriate skill for each sub-task, and compose an executable plan. We present SkillWeaver, a decompose-retrieve-compose framework combining an LLM task decomposer, a bi-encoder skill retriever with FAISS indexing, and a dependency-aware DAG planner. To support evaluation, we introduce CompSkillBench, a benchmark of 300 compositional queries over 2,209 real MCP server skills spanning 24 functional categories, sourced from the public MCP ecosystem. Our experiments reveal that task decomposition quality is the primary bottleneck: standard LLM decomposition reaches only 34.2% category recall at the step level. To address this, we propose Iterative Skill-Aware Decomposition (SAD), a retrieval-augmented feedback loop that iteratively aligns decomposition with available skills. SAD improves decomposition accuracy from 51.0% to 67.7% (+32.7%, Wilcoxon p < 10^-6) in a single iteration; DA-conditioned analysis confirms that correct granularity is the prerequisite for effective retrieval (CatR@1 rises from 34% to 41% when DA=1). SkillWeaver reduces context window consumption by over 99%, and transfer experiments confirm generalization (+35.6% relative DA gain even when target categories are absent from the retrieval pool).

[2] ACCORD: Action-Conditioned Contextual Grounding for Language Agents
User instructions are often underspecified because humans rely on implicit assumptions about the surrounding environment. For large language model (LLM) agents operating in information-rich digital and physical environments, these assumptions cannot be inferred from the instruction alone; they must be recovered from the current state of tools, data, interfaces, and observations. Effective execution therefore requires agents to identify missing context, ground it in observed evidence, and carry it forward into subsequent actions. We show that current agents often fail to do so. They act from assumed rather than observed specifics, overlook information they could have gathered, and fail to incorporate evidence that has already been returned. Building on this insight, we propose ACCORD (Action-Conditioned Contextual Grounding), a simple and effective agent framework for adaptive grounding. Before each action, ACCORD actively probes the environment for missing information and integrates relevant context from the agent's trajectory that would otherwise be overlooked. Requiring no additional training or task-success signals, ACCORD improves task-goal completion on AppWorld by up to +20.6 points with GPT-5-mini, from 42.0% to 62.6%, compared to strong baselines. These gains persist with a substantially stronger base model (+10.8 with Claude-4.5-sonnet), an open-weight model (+10.1 with Qwen3.5-27B-FP8), and on the embodied AlfWorld benchmark (+7.4 success rate with GPT-5-mini).
```

---

## U100_092 — v2_train_r477_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `477`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `bait`

### Question

In the ablation study for GraphAlign, how much does removing the cross-node attention module reduce node classification accuracy on ogbn-arxiv?

### Claim

The sources,, and discuss RankGraph-2, a framework for graph-based retrieval, stance detection using LLMs, and exploratory question answering over data lakes, respectively.

### Evidence

```text
[1] RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation
Graph-based retrieval at billion-node scale requires jointly solving three tightly coupled problems -- graph construction, representation learning, and real-time serving -- yet existing work addresses each in isolation. We present RankGraph-2, a framework deployed at Meta that co-designs all three lifecycle stages for similarity-based retrieval (U2U2I and U2I2I), where each stage's requirements shape the others. Serving requires a co-learned cluster index to avoid expensive online KNN -- this pushes index co-training into the training objective. Training benefits from the observation that similarity-based retrieval tolerates pre-computed neighborhoods, eliminating online graph infrastructure -- this requires construction to produce self-contained data. Construction must also support hour-level refresh for item coverage. Acting on these cascading requirements, RankGraph-2 reduces hundreds of trillions of edges to hundreds of billions via subsampling with popularity bias correction, pre-computes multi-hop neighborhoods via personalized PageRank, and co-learns a residual-quantization cluster index that reduces serving computational cost by 83%. This lifecycle co-design enables a simple architecture to achieve 3.8 x higher recall than a GAT + Deep Graph Infomax model on a bipartite graph and 2.1 x higher than PyTorch-BigGraph on item retrieval. RankGraph-2 delivers up to +0.96% CTR and +2.75% CVR, and has powered 20+ retrieval launches across major surfaces.

[2] SICI: A Semantic-Pragmatic Complexity Index Reveals Regime Shifts in LLM Stance Detection
Prompt-based LLMs are increasingly used for stance detection, but harder examples are not always repaired by clearer instructions, reasoning prompts, retrieval, or debate. We introduce SICI (Stance Inference Complexity Index), a seven-dimensional diagnostic measure of the semantic-pragmatic burden imposed by a target--text pair. Across SemEval-2016 and VAST, SICI predicts LLM accuracy better than surface proxies and shows substantial cross-scorer reliability ($α=0.771$). More importantly, LLM errors change regime as SICI increases: low-complexity examples invite over-attribution, especially Against predictions; intermediate examples form an unstable boundary; and high-complexity examples rapidly concentrate on None. This phase-transition-like structure persists across GPT-3.5, GPT-4o-mini, DeepSeek-V3, and GPT-4o, although stronger models move the boundaries. A 15-method intervention study further shows that prompting, retrieval, and debate often shift models along the attribution--abstention axis rather than removing the high-complexity bottleneck.

[3] SANA: What Matters for QA Agents over Massive Data Lakes?
Exploratory question answering (EQA) over data lakes requires an LLM agent to discover relevant sources, analyze retrieved data, and adapt its actions based on intermediate results. End-to-end accuracy alone cannot distinguish failures in search, planning, data analysis, or the agent's Action Policy: its decisions about what to do next and when to submit an answer. We present SANA (Search Agent Navigation Ablation framework), a diagnostic ablation framework that transforms EQA tasks into runtime profiles containing gold source sequence, sanitized subquestions, and execution records. SANA uses these profiles to construct idealized search, planning, and data-analysis tools, allowing each component to be ablated; the residual gap is diagnostic evidence for policy failures. To illustrate SANA as a reusable evaluation framework, we adapted two recent EQA benchmarks, LakeQA and KramaBench, and evaluated lightweight and mid-sized agents under fixed prompts, budgets, data lakes, and runtimes. Across both benchmarks, data analysis is a consistent bottleneck while planning is less so. Search is a major limitation in LakeQA's large data-lake setting, but less so for the smaller-scale KramaBench. SANA thus deconstructs end-to-end task accuracies into a diagnosis of where data-lake agents fail, and allows for systematic comparisons of progress in search, planning, data analysis, and agent design.
```

---

## U100_093 — v2_train_r116_plain_c005

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `116`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three main contributions presented regarding failures in n-gram-based generative retrieval?

### Claim

A new web-based tool that helps the IR community analyze generated ngrams and their respective contribution to the final ranking, providing an intuitive interface to identify where such GR methods go wrong.

### Evidence

```text
[1] Understanding and Debugging Failures in N-Gram-Based Generative Retrieval
Generative Retrieval (GR) is an emerging Information Retrieval (IR) paradigm that is motivated by increasingly capable language models. In GR, a model directly generates identifiers for relevant documents. While these systems offer unique advantages, they also introduce distinct failure mechanisms. We explore these failure modes in three contributions: (1) We present a taxonomy of GR failure modes based on GR literature. (2) We empirically investigate failure in a subset of GR: ngram-based methods, more specifically, SEAL and MINDER. Our analysis reveals common issues, such as ambiguous docids, low identifier diversity, and the disproportionate impact of specific identifiers. (3) We introduce a new web-based tool that helps the IR community analyze generated ngrams and their respective contribution to the final ranking, providing an intuitive interface to identify where such GR methods go wrong.

[2] OneRetrieval: Unifying Multi-Branch E-commerce Retrieval with an Editable Generative Model
Industrial e-commerce search serves hundreds of millions of items through a multi-branch retrieval stage fused by hand-tuned merging without joint optimization. Generative retrieval (GR) raises the prospect of collapsing this stage into a single model, yet unification is gated by more than retrieval quality: the inverted-index branch converts below the platform average yet persists because it is almost the only branch where operations can inject a new term within hours without any model update; a one-model substitute must preserve this real-time editability. Existing GR methods structurally lack it: closed-codebook methods fix each slot to a quantized embedding at training, while open-vocabulary methods leave new-term routing to model generalization. We present OneRetrieval, a one-model GR framework built on Keyword-Aligned Encoding (KAE), which ties each identifier position to an interpretable attribute word, pairing competitive recall quality with the editability of the inverted index -- to our knowledge the first editable generative retrieval method. An information-theoretic merging organizes 18 attribute categories into six codebook groups with non-uniform capacity; reserved slots in each codebook can be bound to new words after deployment without retraining; and a four-stage fine-tuning pipeline secures quality and editability jointly. On five million real-traffic requests, OneRetrieval matches the deep recall of the strongest generative baseline, with an intervention hit rate over an order of magnitude above closed-codebook encodings. Online, replacing the inverted-index branch significantly lifts order volume; extending to nearly the entire stage holds conversion while improving CTR. The system is deployed at Kuaishou, serving hundreds of millions of PVs daily.

[3] Can Post-Training Turn LLMs into Good Medical Coders? An Empirical Study of Generative ICD Coding
Automated International Classification of Diseases (ICD) coding is a core medical-coding task for billing, epidemiology, and clinical decision support. Generative large language models (LLMs) are often reported as weak medical coders, but this finding mainly comes from inference-time settings such as prompting, retrieval, reranking, or tool use, leaving the role of task-specific post-training underexplored. We present a controlled empirical study of post-training for generative ICD coding, comparing discriminative baselines with LLM coders across prompting, supervised fine-tuning, and reinforcement learning under a common protocol and metric set. To our knowledge, this is the first study to evaluate RL-based post-training for generative LLM coders in ICD coding. We further introduce PHI, a diagnostic curriculum that extends GRPO to refine missed-code cases. Our results show that prompting-only evaluation substantially underestimates the potential of LLMs for ICD coding. SFT provides the main capability jump, GRPO further improves code-set prediction beyond SFT, and PHI provides targeted gains on macro-level performance. These findings suggest that the main bottleneck is not the generative formulation alone, but how the model is adapted and optimized for full-taxonomy recall. We release our code, data splits, and checkpoints at https://github.com/AlexandreWANG915/LLM4ICD.
```

---

## U100_094 — v2_train_r200_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `200`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_type: `grounded`

### Question

What multi-agent architecture is extended in this work for the ARIC task, and what explanation does the paper give for why the Attack class was more damaging to supervised fine-tuning than to inference-only models?

### Claim

The paper suggests that the under-representation of the Attack class was more damaging to supervised fine-tuning than to inference-only models because all generative approaches outperform fine-tuned RoBERTa models on Macro F1.

### Evidence

```text
[1] From Argument Components to Graphs: A Multi-Agent Debate with Confidence Gating for Argument Relations
Large Language Models (LLMs) are increasingly assessed and utilized in the field of Argument Mining (AM), thanks to their strong general reasoning capabilities. However, standard training-free models often miss sophisticated details, specifically in contexts where two parts of the text have to be analyzed together. Furthermore, self-correction mechanisms tend to reinforce initial hallucinations in reasoning. Overcoming these limitations typically requires expensive, domain-specific supervised fine-tuning. Recent work has shown that a multi-agent paradigm can address such weaknesses for the component classification task through dialectical refinement with a Proponent-Opponent-Judge architecture, setting a promising direction for training-free approaches in the field. In this paper, we extend and evaluate this framework on the Argument Relation Identification and Classification (ARIC) task, reformulating it as a debate over component pairs. Besides that, we introduce a confidence gating mechanism that enables debating only on the uncertain cases and accepting the initial prediction when confidence is high. On the UKP Argument Annotated Essays v2 corpus, we demonstrate that the selective debate achieves the highest Macro F1 among all training-free methods, while debate over all samples degrades performance below that of one of the baselines. All generative approaches also outperform fine-tuned RoBERTa models on Macro F1, suggesting that the under-representation of the Attack class was more damaging to supervised fine-tuning than to inference-only models. Additionally, our framework produces human-readable debate transcripts, offering interpretability absent from both single-agent and supervised classifiers.
```

---

## U100_095 — v2_train_r330_plain_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `330`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What two deployment settings does MedLatentDx support for hospital agents with same versus different LLM backbones, and what technique is used for each?

### Claim

MedLatentDx supports two deployment settings for hospital agents. 1.

### Evidence

```text
[1] MedLatentDx: Latent Multi-Agent Communication for Cross-Hospital Rare-Disease Diagnosis
Rare diseases affect over $300$ million patients across more than $7{,}000$ conditions, yet no single hospital encounters enough cases of any one condition for reliable diagnosis. Cross-hospital collaboration could help by allowing a diagnosing institution to use distributed, case-specific diagnostic evidence, but privacy regulations restrict the transmission of identifiable clinical text across institutional boundaries. This setting raises two challenges: existing medical agent systems often rely on textual evidence exchange, while raw latent states such as hidden states and KV caches may still reveal prompt-derived clinical content. We introduce MedLatentDx, a latent multi-agent communication framework in which hospital agents keep private clinical records and retrieved cases local, and send compact latent KV blocks to a host agent for rare-disease diagnosis. MedLatentDx supports two deployment settings: same-backbone hospital agents use latent KV distillation, while hospitals with different LLM backbones use cross-family latent alignment. On CrossRare-Bench, a self-built large-scale rare-disease benchmark with hospital-level partitions, MedLatentDx improves cross-hospital diagnostic performance while reducing reconstructable clinical content relative to raw-latent communication baselines.

[2] GateMem: Benchmarking Memory Governance in Multi-Principal Shared-Memory Agents
Memory benchmarks for LLM agents largely assume single-user settings, leaving shared assistants for hospitals, workplaces, campuses, and households understudied. In these deployments, multiple principals write to a common memory pool and query it under different roles, scopes, and relationships, so memory quality requires governance as well as recall. We introduce GateMem, a benchmark for multi-principal shared-memory agents. GateMem jointly evaluates utility for legitimate long-horizon requests with state updates, access control across contextual authorization boundaries, and agent-facing active forgetting after explicit deletion requests. It spans medical, office, education, and household domains, with long-form multi-party episodes, incremental memory injection, hidden checkpoints, structured judging, and leak-target annotations. Across diverse baselines and backbone models, no method simultaneously achieves strong utility, robust access control, and reliable forgetting. Long-context prompting often yields the best governance score at high token cost, while retrieval-based and external-memory methods reduce cost yet still leak unauthorized or deleted information. These results show current memory agents remain far from reliable shared institutional deployment.

[3] State-Grounded Multi-Agent Synthetic Data Generation for Tool-Augmented LLMs
Training tool-augmented LLM agents requires large corpora of multi-turn, tool-grounded conversational data that is expensive to annotate, privacy-constrained in production settings, and largely absent from public datasets. We present StateGen, a synthetic data generation platform that produces scored, reasoning-trace-rich training conversations by orchestrating a four-role LLM loop: a persona-conditioned user simulator, an agent under test, a state-grounded tool simulator, and a multi-axis LLM judge. The key architectural contribution is an authoritative state manager that maintains a structured world-state object across turns, enforcing a backend-is-truth invariant that eliminates the dominant class of tool-call hallucinations by construction. StateGen extends naturally to hierarchical multi-agent settings by declaring sub-agents as tools, all sharing a single state object. We report results on 64,698 evaluated conversations across three production corpora: tool-call hallucination scores reach 9.66/10, the system supports persona-driven variation via a 23-dimensional trait vector, and a cleanly separated train and golden evaluation set split confirms the data is not memorization bait (per-criterion gap analysis). Comparison with eight external systems shows that no single publicly available platform combines multi-turn generation, state-grounded tool simulation, hierarchical multi-agent support, and built-in judge scoring.
```

---

## U100_096 — v2_train_r357_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `357`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

How many body systems, imaging modalities, and clinical domains does the ArogyaBodha dataset cover, and across how many languages?

### Claim

The ArogyaBodha dataset covers 31 body systems, 6 imaging modalities, and 21 clinical domains across English and seven major Indian languages.

### Evidence

```text
[1] ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages
Multimodal Large Language Models (MLLMs) have shown promising reasoning capabilities in general domains, yet their performance remains limited in specialized settings such as healthcare, especially in multilingual and low-resource scenarios. This gap is critical in regions like rural India, where patients often express complex medical queries in native Indic languages and rely on multimodal inputs such as medical images. Existing English-centric MLLMs struggle to support such use cases, limiting equitable access to AI-driven healthcare assistance. To address this challenge, we introduce ArogyaBodha, a large-scale multilingual multimodal medical question-answer dataset constructed from eight heterogeneous sources, covering 31 body systems, six imaging modalities, and 21 clinical domains across English and seven major Indian languages. We further propose ArogyaSutra, an actor-critic-based multi-agent framework that integrates tool grounding with dual-memory mechanisms for step-wise, reasoning-aware decision making, and uses stored actor-critic simulation trajectories for distillation. Experiments show that our dataset and framework improve multilingual medical reasoning accuracy across all Indic languages, with ablations validating the contribution of each component. The source code and dataset are available at: https://iitp-cse.github.io/ ArogyaSutra/

[2] Scalable Training of Spatially Grounded 2D Vision-Language Models for Radiology
We study how to train visually grounded vision-language models (VLMs) for radiology without manual spatial annotations. We introduce RefRad2D, a large-scale bilingual (German/English) dataset of 1.2M CT and MR image-text pairs derived from clinical practice, with task-specific VQA and spatial grounding subsets generated automatically via LLM-based curation and automated segmentation. Trained on this data, our model RadGrounder jointly performs report generation, visual question answering, and spatial grounding via bounding-box detection or segmentation. On external VQA benchmarks (Slake, VQA-RAD), RadGrounder achieves competitive results with specialized medical VLMs. Adding our clinical data to the training mixture improves open-ended VQA over fine-tuning on the downstream datasets alone, showing the transferability of our dataset. Crucially, adding grounding supervision does not degrade language quality, enabling spatially verifiable outputs at no cost to VQA performance.

[3] MedRLM: Recursive Multimodal Health Intelligence for Long-Context Clinical Reasoning, Sensor-Guided Screening, Evidence-Grounded Decision Support, and Community-to-Tertiary Referral Optimization
Real-world clinical decision support requires reasoning over heterogeneous and longitudinal patient information rather than answering isolated medical questions. However, current medical large language models and retrieval-augmented generation systems often rely on single-step prompting or retrieval, which can be fragile when clinical evidence is distributed across long electronic health records, medical images, sensor streams, guidelines, and referral constraints. This paper proposes MedRLM, a Recursive Multimodal Health Intelligence framework for long-context clinical reasoning, sensor-guided screening, and community-to-tertiary referral support. Instead of compressing all patient information into one prompt, MedRLM treats the patient case as an external clinical environment that can be recursively inspected, decomposed, retrieved, verified, and synthesized. The framework coordinates specialized agents for clinical text, longitudinal EHR, medical imaging, physiological sensor signals, guideline retrieval, uncertainty auditing, and referral planning. It further introduces a Clinical Evidence Graph Memory to connect patient-specific observations with retrieved evidence, standardized definitions, sensor-derived biomarkers, and referral criteria. A sensor-guided recursive triggering mechanism activates deeper reasoning when abnormal physiological or behavioral patterns are detected, while uncertainty-gated refinement supports clinician review for high-risk or low-confidence cases. We also outline a real-data evaluation design using public and credentialed clinical datasets spanning EHR, radiology, ECG, ICU time series, and referral-proxy outcomes. MedRLM aims to move medical AI from static question answering toward auditable, multimodal, and workflow-aware clinical decision support.
```

---

## U100_097 — v2_train_r1_plain_c003

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What is the composition and scale of the RefRad2D dataset, including its imaging modalities and languages?

### Claim

The dataset covers two imaging modalities, CT and MR.

### Evidence

```text
[1] Scalable Training of Spatially Grounded 2D Vision-Language Models for Radiology
We study how to train visually grounded vision-language models (VLMs) for radiology without manual spatial annotations. We introduce RefRad2D, a large-scale bilingual (German/English) dataset of 1.2M CT and MR image-text pairs derived from clinical practice, with task-specific VQA and spatial grounding subsets generated automatically via LLM-based curation and automated segmentation. Trained on this data, our model RadGrounder jointly performs report generation, visual question answering, and spatial grounding via bounding-box detection or segmentation. On external VQA benchmarks (Slake, VQA-RAD), RadGrounder achieves competitive results with specialized medical VLMs. Adding our clinical data to the training mixture improves open-ended VQA over fine-tuning on the downstream datasets alone, showing the transferability of our dataset. Crucially, adding grounding supervision does not degrade language quality, enabling spatially verifiable outputs at no cost to VQA performance.

[2] ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages
Multimodal Large Language Models (MLLMs) have shown promising reasoning capabilities in general domains, yet their performance remains limited in specialized settings such as healthcare, especially in multilingual and low-resource scenarios. This gap is critical in regions like rural India, where patients often express complex medical queries in native Indic languages and rely on multimodal inputs such as medical images. Existing English-centric MLLMs struggle to support such use cases, limiting equitable access to AI-driven healthcare assistance. To address this challenge, we introduce ArogyaBodha, a large-scale multilingual multimodal medical question-answer dataset constructed from eight heterogeneous sources, covering 31 body systems, six imaging modalities, and 21 clinical domains across English and seven major Indian languages. We further propose ArogyaSutra, an actor-critic-based multi-agent framework that integrates tool grounding with dual-memory mechanisms for step-wise, reasoning-aware decision making, and uses stored actor-critic simulation trajectories for distillation. Experiments show that our dataset and framework improve multilingual medical reasoning accuracy across all Indic languages, with ablations validating the contribution of each component. The source code and dataset are available at: https://iitp-cse.github.io/ ArogyaSutra/

[3] NRITYAM: Language Models Meet Art and Heritage of Dance
Language models have become essential tools in shaping modern workflows. However, their global effectiveness hinges on a nuanced understanding of local socio-cultural contexts. To address this gap, we present NRITYAM, a comprehensive benchmark for evaluating the cultural comprehension capabilities of language models in the context of global dance traditions. NRITYAM comprises 9,260 carefully curated question-answer pairs spanning 12 languages, making it the largest dataset dedicated to evaluating cultural knowledge in dance. The dataset has been developed from the ground up through close collaboration with native dance artists and native speakers of the languages, who authored and validated culturally relevant questions specific to their regions. We evaluate a broad set of models, including large language models, small language models, multimodal large language models, and small multimodal language models. As a multilingual and multicultural benchmark, NRITYAM sets a new standard for evaluating the ability of AI systems to understand and reason about traditional performing arts. Detailed dataset samples are available at~\url{https://github.com/niladrighosh03/NRITYAM}.
```

---

## U100_098 — v2_train_r223_plain_c001

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `223`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What edge precision against gold does TGComplete achieve compared to the GoG baseline, and how many times higher is its strict faithfulness of admitted edges?

### Claim

TGComplete achieves higher edge precision against gold compared to the GoG baseline.

### Evidence

```text
[1] When Correct Edges Cannot Be Verified: A Provenance Gap in Incomplete KGQA and a Provenance-Favoring Completion Policy
Incomplete Knowledge Graph Question Answering (IKGQA) requires completing missing edges to continue reasoning. A growing line of work verifies completed edges against retrieved text, treating textual support as a proxy for edge quality. We ask a question that, to our knowledge, has not been systematically tested: does textual verifiability actually track correctness? Exploiting the gold deleted triples provided by the standard random-deletion protocol, we measure both. The finding is counterintuitive: among gold-correct completed edges, 76-96% have no supporting passage even under exhaustive retrieval, robustly across deletion rates (20%/40%), datasets (CWQ/WebQSP), and relation types (structural, commonsense, long-tail). Most Freebase-style facts simply do not occur as head-tail co-mentions in text. Textual faithfulness therefore measures provenance, not correctness -- separated by a paradigm-level gap no in-corpus retrieval closes. This reframes edge completion. Since most completed edges -- correct or not -- are causally redundant for the answer (95-97% of correct answers do not depend on any unsupported edge), the central question shifts from "is the edge correct?" to "admit or abstain under provenance uncertainty?" Within this framing we present TGComplete, a provenance-favoring admission policy that retrieves evidence at a reasoning breakpoint, verifies a candidate through a lightweight loop, and abstains when support is absent. Against the generate-to-complete baseline GoG, it attains higher edge precision against gold (15-21% vs 3-14%), with no statistically detectable EM loss and 3.1-7.4 times higher strict faithfulness of admitted edges -- at the cost of lower recall. We position TGComplete not as uniformly better, but as a principled point on a precision/provenance-recall trade-off, appropriate when auditability matters.

[2] Prior over Evidence: Stereotype-Driven Diagnosis in LLM-Based L2 Pronunciation Feedback
Large language models are increasingly deployed for written pronunciation feedback in second-language (L2) English learning, under the assumption that their diagnoses are grounded in the supplied speech evidence rather than in priors from pretraining. This assumption is tested on 1,800 L2-Arctic utterances spanning six L1 backgrounds, three audio-capable LLMs, four pronunciation dimensions, and five evidence conditions ranging from a text-only baseline to numeric acoustic features and raw audio. Each (utterance x model x condition x dimension) cell is scored on three metrics: Rating Accuracy (RA) against gold labels, Evidence Coherence (EC) assessing internal consistency without ground truth, and Grounded Correctness (GC) evaluated against gold evidence. Results show three findings across models. First, rating accuracy and grounded reasoning decouple: 39.6% of judged cells contain internally coherent reasoning that supports a wrong rating, against only 15.8% where the reasoning supports a correct rating. Second, phoneme-level feedback converges to a fixed inventory of L2-English difficulty phones that recurs across all six L1 backgrounds and all evidence conditions. Third, acoustic evidence improves the rating only when the supplied feature directly probes the target dimension: textualised F0 range raises pitch-variation grounding from (0.18-0.19) to (0.45-0.62) across all three models, while stress and phoneme correctness, which require target-to-realisation alignment, remain ungrounded. The same audio waveform without textualised F0 values does not reproduce this improvement. These findings indicate that current general-purpose LLMs are more reliable as verbalisers of externally computed pronunciation evidence than as standalone diagnostic engines.

[3] Know Your Limits : On the Faithfulness of LLMs as Solvers and Autoformalizers in Legal Reasoning
Large Language Models (LLMs) achieve strong performance on reasoning tasks, but whether this reflects faithful logical inference or heuristic approximation remains unclear. We study this question in legal entailment by comparing three paradigms, including pure LLM classification, LLM-based Formal Reasoning, and solver-based Formal Reasoning using the Z3 SMT solver, on a re-annotated subset of ContractNLI across five LLMs. Our re-annotation reveals a systematic and measurable gap between pragmatic legal interpretation and strict formal entailment, where a substantial proportion of legally sound inferences are not formally grounded without additional unstated assumptions. While introducing formal structure improves accuracy, with LLM-based Formal Reasoning achieving the highest benchmark performance, we show that this gain does not imply faithful reasoning. We identify three recurring failure modes: scope laundering, where LLMs report solver-inconsistent classifications without executing the underlying formal reasoning, producing conclusions that appear logically grounded but are not; implicit constraint blindness, where LLMs overlook logical constraints present in formal representations; and program synthesis failures, where LLMs generate incorrect Z3 code despite structured prompting. Critically, scope laundering persists across all models, raising serious concerns about the faithfulness of LLM-based formal reasoning as a proxy for symbolic execution. These results reveal a fundamental gap between benchmark accuracy and logical faithfulness.
```

---

## U100_099 — v2_train_r110_cited_c002

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- source_split: `train`
- qid: `110`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What specific weaknesses in game generation do the evaluations reveal about how agents implement mechanics versus delivering complete games?

### Claim

This suggests a weakness in the agents' ability to generate games that are not just mechanically sound, but also fully-fledged and engaging.

### Evidence

```text
[1] GameCraft-Bench: Can Agents Build Playable Games End-to-End in a Real Game Engine?
Game generation is an emerging application of coding agents, requiring models to transform natural-language specifications into playable interactive systems. Unlike traditional coding tasks, game generation takes place within a game engine, where scripts, scenes, assets, rendering, and runtime interactions must jointly produce coherent gameplay. We formalize end-to-end game generation as the problem of producing a complete game artifact that realizes a specification through observable player-game interaction in a target environment. We argue that evaluating this setting requires three desiderata: Engine Grounding, Artifact Completeness, and Interactive Verification. We propose an interaction-grounded evaluation framework that assesses executable gameplay through replayed demonstrations and rubric-guided multimodal judging. We instantiate this framework as GameCraft-Bench, a benchmark comprising 140 Godot tasks across 15 game families. Evaluations of frontier coding agents show that end-to-end game generation remains highly challenging: the strongest agent achieves only 41.46%, and most agents score below 40%. Further analysis reveals that while agents often implement recognizable mechanics, they struggle to deliver complete games with sufficient content, functional visual feedback, and coherent presentation. See https://tongxuluo.github.io/gamecraft-bench-website for demos, code, and data.

[2] Dialogue SWE-Bench: A Benchmark for Dialogue-Driven Coding Agents
AI coding agents have rapidly transformed software engineering, powering widely used interactive coding assistants. Despite their interactive real-world use, existing benchmarks evaluate them as fully-autonomous systems. In this work, we introduce Dialogue SWE-Bench, an automatic benchmark dataset for evaluating the ability of coding agents to resolve real-world software engineering problems through dialogue with a user. We design a novel, persona-grounded user simulator to support our task evaluation, and augment our task evaluation with automatic evaluations of dialogue quality. We also propose a new schema-guided agent, aimed at improving the dialogue capabilities of off-the-shelf coding agents, which improves over strong baselines by 3-14%. Our results indicate that better coding models do not always correspond to better dialogue models, suggesting that dialogue capability is a distinct and currently understudied dimension of coding agent performance.

[3] ACCORD: Action-Conditioned Contextual Grounding for Language Agents
User instructions are often underspecified because humans rely on implicit assumptions about the surrounding environment. For large language model (LLM) agents operating in information-rich digital and physical environments, these assumptions cannot be inferred from the instruction alone; they must be recovered from the current state of tools, data, interfaces, and observations. Effective execution therefore requires agents to identify missing context, ground it in observed evidence, and carry it forward into subsequent actions. We show that current agents often fail to do so. They act from assumed rather than observed specifics, overlook information they could have gathered, and fail to incorporate evidence that has already been returned. Building on this insight, we propose ACCORD (Action-Conditioned Contextual Grounding), a simple and effective agent framework for adaptive grounding. Before each action, ACCORD actively probes the environment for missing information and integrates relevant context from the agent's trajectory that would otherwise be overlooked. Requiring no additional training or task-success signals, ACCORD improves task-goal completion on AppWorld by up to +20.6 points with GPT-5-mini, from 42.0% to 62.6%, compared to strong baselines. These gains persist with a substantially stronger base model (+10.8 with Claude-4.5-sonnet), an open-weight model (+10.1 with Qwen3.5-27B-FP8), and on the embodied AlfWorld benchmark (+7.4 success rate with GPT-5-mini).
```

---

## U100_100 — v2_train_r270_plain_c001

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- source_split: `val`
- qid: `270`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_type: `grounded`

### Question

What are the three agents integrated into the proposed LLM-driven framework, and what is the specific function of each?

### Claim

The three agents integrated into the proposed LLM-driven framework are: 1.

### Evidence

```text
[1] Risk-Aware LLM Agents for Geospatial Data Retrieval: Design and Preliminary Adversarial Evaluation
We present an LLM-driven framework for retrieving remote sensing data from cloud-based geospatial catalogues using natural language queries. The system converts user intent into structured API calls, enabling efficient access to satellite imagery and environmental datasets. The architecture integrates three agents: Guardrail for safety and policy enforcement, General-QA for intent interpretation, and Recommender-Analyst for schema-aware API call generation. This coordinated design ensures reliable, semantically aligned interaction with external data services. The modular framework is portable across platforms through API schema substitution and supports applications in environmental monitoring, disaster response, and climate analysis. It establishes a scalable interface between user intent and geospatial infrastructure, enabling streamlined and automated Earth observation workflows. Preliminary experiments under adversarial multi-turn settings show that prompt-level safety instructions improve robustness, although rare high-impact failures persist in API manipulation scenarios and highlight the need for adaptive, system-level defenses that balance safety, usability, and cost efficiency, which motivates the use of our intercept-level Guardrail agent.

[2] ACCORD: Action-Conditioned Contextual Grounding for Language Agents
User instructions are often underspecified because humans rely on implicit assumptions about the surrounding environment. For large language model (LLM) agents operating in information-rich digital and physical environments, these assumptions cannot be inferred from the instruction alone; they must be recovered from the current state of tools, data, interfaces, and observations. Effective execution therefore requires agents to identify missing context, ground it in observed evidence, and carry it forward into subsequent actions. We show that current agents often fail to do so. They act from assumed rather than observed specifics, overlook information they could have gathered, and fail to incorporate evidence that has already been returned. Building on this insight, we propose ACCORD (Action-Conditioned Contextual Grounding), a simple and effective agent framework for adaptive grounding. Before each action, ACCORD actively probes the environment for missing information and integrates relevant context from the agent's trajectory that would otherwise be overlooked. Requiring no additional training or task-success signals, ACCORD improves task-goal completion on AppWorld by up to +20.6 points with GPT-5-mini, from 42.0% to 62.6%, compared to strong baselines. These gains persist with a substantially stronger base model (+10.8 with Claude-4.5-sonnet), an open-weight model (+10.1 with Qwen3.5-27B-FP8), and on the embodied AlfWorld benchmark (+7.4 success rate with GPT-5-mini).

[3] VeriGraph: Towards Verifiable Data-Analytic Agents
LLM-based agents have demonstrated strong capabilities in data-intensive analytical tasks, yet their outputs are rarely verifiable: a reliance on linear text trajectories makes their reasoning difficult to audit. In particular, deterministic computations over raw data and semantic deductions over natural-language claims are often entangled in an unstructured stream, leaving numerical conclusions hard to reproduce and qualitative judgments hard to inspect. To address this, we propose VeriGraph, a traceable neuro-symbolic reasoning framework that enables agents to construct an explicit heterogeneous evidence directed acyclic graph (DAG) during execution. VeriGraph introduces three evidence-expansion primitives, namely computational, grounding, and derivational expansion, to connect raw data, interpreter variables, computed results, and natural-language claims in a unified graph. Under this formulation, structural traceability is reduced to graph reachability from raw data sources to terminal claims, while semantic support is measured by claim-level evidence evaluation. To improve graph construction, we further design a graph-based policy optimization strategy with a composite reward that jointly supervises answer correctness, computational integrity, and derivational coherence. Experiments on four benchmarks show that VeriGraph-8B achieves the highest overall score among all baselines. More importantly, VeriGraph produces auditable evidence graphs with substantially stronger claim grounding, achieving a 87.61\% Grounding Rate under our claim-level evidence support evaluation. These results suggest that explicit evidence-graph construction is a promising path toward verifiable data-analytic agents. Our code is available at https://github.com/ignorejjj/VeriGraph.
```

---
