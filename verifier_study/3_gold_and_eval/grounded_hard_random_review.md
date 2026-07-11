# Grounded-Hard Random Human Review

Fill `FINAL_LABEL` with exactly one of: `SUPPORTED`, `UNSUPPORTED`, `ABSTENTION`.

Label rules:
- `SUPPORTED`: the substantive claim is supported by the provided evidence.
- `UNSUPPORTED`: the claim adds/changes/overstates information not supported by the evidence.
- `ABSTENTION`: refusal, insufficient-evidence statement, or meta statement such as 'the sources do not mention X'.

Sampling:
- Input claim pool: 1245
- Selected claims: 150
- Sampling is stratified random by `hard_policy × answer_variant`.
- No evaluated model was used for sampling.

---

## GHR0139 — gh_118_plain_answer_1

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 1
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese'?

### Claim

The paper 'Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese' is not among the sources provided.

### Evidence

```text
[1] Operadic consistency: a label-free signal for compositional reasoning failures in LLMs
Detecting LLM reasoning failures at inference time without ground-truth labels has motivated a wide range of confidence baselines, including self-consistency, semantic entropy, and P(True), built on within-question sampling and self-evaluation. Operad theory, the formalism for systems built by iterated substitution, suggests a complementary diagnostic: a model's direct answer to a compositional query should agree with the answer it produces by composing a stated decomposition of the same query. We instantiate this idea as operadic consistency (OC), a per-question signal. Across twelve instruction-tuned LLMs (4B to 671B parameters, open-weights and closed-source) on four multi-hop QA datasets, OC is strongly correlated with accuracy on every dataset (Pearson $r \in [0.86, 0.94]$, all $p \leq 0.0004$), and is the only signal we evaluate with $r \geq 0.85$ uniformly across all four datasets. Chain-of-thought self-consistency (CoT-SC; Wang et al., 2023) matches OC on HotpotQA and DROP ($r = 0.93, 0.87$) but drops to $r \approx 0.45$ on MuSiQue and StrategyQA. At the per-question level, OC contributes information beyond CoT-SC and semantic entropy on every dataset (cluster-robust $p \leq 10^{-16}$ for the OC coefficient), and the conclusion is robust to additionally controlling for constructed decomposition-aware baselines ($p \leq 10^{-13}$). The same signal yields selective-prediction improvements (accuracy at fixed coverage) over a tuned CoT-SC baseline at the equal-cost $K = 3$ budget (AUARC lifts of +0.086 to +0.096 and AUROC lifts of +0.092 to +0.164; 95% CIs exclude zero on every cell). On five frontier thinking models, where the decomposition is extracted from the model's own chain of thought, the same equal-cost comparison gives positive selective-prediction point-estimate lift on all 16 (dataset, budget, metric) cells tested, with 95% CIs excluding zero on 12 of the 16.

[2] Benchmarking Agentic Review Systems
A new class of agentic review systems are emerging as a remedy to the pressure placed on peer review systems by AI-assisted research, but it is unclear how they should be evaluated. We evaluate two open-source systems (OpenAIReview and coarse), one proprietary system (Reviewer3), and a zero-shot baseline, across six LLMs spanning frontier and efficient models. First, we study whether AI reviews on ICLR/NeurIPS papers track with papers' quality as approximated by external signals such as citations and acceptance decisions. Every system performs above chance in pairwise accuracy, and the best is OpenAIReview + GPT-5.5 at 83.0%. Second, to test whether systems can catch errors with known ground truth, we construct a perturbation benchmark that injects four categories of errors into papers across eight arXiv subject classes and measure detection recall. The strongest configuration (OpenAIReview + GPT-5.5) catches 71.6% of injected errors, leaving substantial room for improvement. The union of detections across six models reaches 83.3% recall, suggesting different models detect different errors and better harness design can potentially increase performance. Beyond these benchmarks, we study a public deployment of OpenAIReview with real users. Votes on its comments skew positive at 1.44 to 1, and the most common complaints are about false positives and minor nitpicks. Together, by evaluating full review systems backed by state-of-the-art models on real research papers, we show that while AI reviews still have room for improvement, they can already track human quality judgments well, catch important errors, and earn positive feedback from real users.
```

---

## GHR0105 — gh_34_plain_answer_8

**FINAL_LABEL:** `UNSUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 2
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese'?

### Claim

This suggests that while TOTEN is effective in many aspects, it may not always match the performance of specialized tools like Pint for certain tasks.

### Evidence

```text
[1] Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese
Byte-Pair Encoding tokenization is statistically efficient for vocabulary compression, but semantically blind to structured technical entities, fragmenting physical quantities, numbers, units, and symbolic expressions into lexically arbitrary subwords. We present TOTEN, a knowledge-based ontological tokenization framework that replaces statistical derivation with declarative classification grounded in a formal ontology of engineering entities (OEE). We formalize TOTEN as the triple <O, classify, {inst_tau}>: the ontology gathers types, structural principles, composition relations, and preservable invariants; the classification function maps raw text into typed regions; and the instantiator family yields a self-descriptive structured representation. Robustness derives from deterministic coupling with three external oracles: Pint (dimensional), Unicode Character Database (typographic), and RSLP (Portuguese morphology). Intrinsic evaluation covers four properties verifiable by construction -- ontological atomicity, dimensional equivalence, typographic robustness, and numerical reconstruction -- over an internal, physically validated benchmark (EngQuant, N=800) and four Brazilian Portuguese external corpora (N=1771 eligible cases). We also report detection recall, distinguishing coverage from conditional atomicity. Against eight state-of-the-art baselines, TOTEN achieves unit ontological atomicity in all contrasts and numerical reconstruction of 0.775-0.904 on external corpora, vs. 0.627-0.703 for the best baseline (Quantulum3); on EngQuant, 0.780 vs. 0.340. Differences are statistically significant (McNemar with Holm correction). Spearman correlation between internal and external rankings confirms concurrent validity of the control benchmark. Dimensional equivalence shows statistical parity with Pint, the oracle from which the system inherits dimensional authority.

[2] Operadic consistency: a label-free signal for compositional reasoning failures in LLMs
Detecting LLM reasoning failures at inference time without ground-truth labels has motivated a wide range of confidence baselines, including self-consistency, semantic entropy, and P(True), built on within-question sampling and self-evaluation. Operad theory, the formalism for systems built by iterated substitution, suggests a complementary diagnostic: a model's direct answer to a compositional query should agree with the answer it produces by composing a stated decomposition of the same query. We instantiate this idea as operadic consistency (OC), a per-question signal. Across twelve instruction-tuned LLMs (4B to 671B parameters, open-weights and closed-source) on four multi-hop QA datasets, OC is strongly correlated with accuracy on every dataset (Pearson $r \in [0.86, 0.94]$, all $p \leq 0.0004$), and is the only signal we evaluate with $r \geq 0.85$ uniformly across all four datasets. Chain-of-thought self-consistency (CoT-SC; Wang et al., 2023) matches OC on HotpotQA and DROP ($r = 0.93, 0.87$) but drops to $r \approx 0.45$ on MuSiQue and StrategyQA. At the per-question level, OC contributes information beyond CoT-SC and semantic entropy on every dataset (cluster-robust $p \leq 10^{-16}$ for the OC coefficient), and the conclusion is robust to additionally controlling for constructed decomposition-aware baselines ($p \leq 10^{-13}$). The same signal yields selective-prediction improvements (accuracy at fixed coverage) over a tuned CoT-SC baseline at the equal-cost $K = 3$ budget (AUARC lifts of +0.086 to +0.096 and AUROC lifts of +0.092 to +0.164; 95% CIs exclude zero on every cell). On five frontier thinking models, where the decomposition is extracted from the model's own chain of thought, the same equal-cost comparison gives positive selective-prediction point-estimate lift on all 16 (dataset, budget, metric) cells tested, with 95% CIs excluding zero on 12 of the 16.

[3] Benchmarking Agentic Review Systems
A new class of agentic review systems are emerging as a remedy to the pressure placed on peer review systems by AI-assisted research, but it is unclear how they should be evaluated. We evaluate two open-source systems (OpenAIReview and coarse), one proprietary system (Reviewer3), and a zero-shot baseline, across six LLMs spanning frontier and efficient models. First, we study whether AI reviews on ICLR/NeurIPS papers track with papers' quality as approximated by external signals such as citations and acceptance decisions. Every system performs above chance in pairwise accuracy, and the best is OpenAIReview + GPT-5.5 at 83.0%. Second, to test whether systems can catch errors with known ground truth, we construct a perturbation benchmark that injects four categories of errors into papers across eight arXiv subject classes and measure detection recall. The strongest configuration (OpenAIReview + GPT-5.5) catches 71.6% of injected e

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0006 — gh_151_cited_answer_2

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 3
- sampling_stratum: `drop_home_related::cited_answer`
- sampling_weight: `4.166666666666667`
- hard_policy: `drop_home_related`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems', and what problem is it designed to address?

### Claim

I cannot answer the question based on the given sources.

### Evidence

```text
[1] MLT-Dedup: Efficient Large-Scale Online Video Deduplication via Multi-Level Representations and Spatial-Temporal Matching
The explosive growth of user-generated video content on online platforms is accompanied by the emergence of numerous near-duplicate videos--videos that are identical or highly similar but differ by partial edits. These duplicates degrade user experience and increase storage and bandwidth costs, making large-scale video deduplication a critical task. Existing video deduplication frameworks face a fundamental challenge in retrieving sufficient high-quality candidates under a limited index budget, as well as trade-offs between efficiency and precision. To address these issues, we propose MLT-Dedup, an efficient large-scale online video deduplication framework with Multi-Level representations and spatial-Temporal matching. Our approach employs a Multi-Level Video Encoder (ML-VE) to extract both fine-grained frame-level and sparse clip-level embeddings: sparse embeddings support efficient candidate retrieval, while fine-grained embeddings are loaded for precise pairwise matching. During matching, we introduce DiF-SiM, a Differential Feature-enhanced Similarity Module capable of locating duplicated temporal segments and providing reliable similarity evidence to support policy-driven deduplication decisions. Extensive experiments on a real-world large-scale platform demonstrate that MLT-Dedup reduces online repetition rates by 91% at 90% precision. Furthermore, our sparse retrieval design achieves a 5x increase in indexing capacity, enabling broader candidate coverage in real-world deployment.

[2] CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents
Personalized dialogue agents require continuous long-term memory to maintain coherent interactions across multiple sessions. However, deploying these capabilities on consumer-grade hardware (e.g., 8 GB VRAM edge devices) introduces severe memory and compute bottlenecks. Existing systems typically rely on isotropic cosine similarity for retrieval and heuristic rules for context compression. These approaches lack a unified theoretical foundation, frequently suffering from the hubness problem in high-dimensional retrieval and syntactic fragmentation during compression. To overcome these limitations, we propose CoreMem, a resource-efficient edge-cloud memory architecture fundamentally unified by information geometry. First, Riemannian retrieval replaces cosine matching with a locally adaptive Fisher-Rao metric, effectively penalizing hub memories via Mahalanobis distance with O(Ndr) Woodbury acceleration for real-time search. Second, Fisher-guided discrete token distillation (FDTD) introduces a hierarchical sentence-to-token compression mechanism. It derives sensitivity scores from Fisher information traces, providing a principled compression-KL tradeoff augmented with explicit structural syntax protection. Evaluated on the LOCOMO and LongMemEval-S benchmarks, CoreMem achieves strong accuracy improvements, yielding substantial gains in Open-domain (+4.51 pp) and Temporal (+4.17 pp) reasoning. Extensive profiling confirms that CoreMem operates seamlessly within a strict 8 GB VRAM budget, successfully bridging the gap between resource-constrained edge devices and the demand for theoretically grounded, lifelong memory agents.
```

---

## GHR0121 — gh_48_plain_answer_6

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 4
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Understanding the Behaviors of Environment-aware Information Retrieval'?

### Claim

To facilitate learning over multi-retrieval-step trajectories, they introduce a branching-based rollout technique that improves training stability.

### Evidence

```text
[1] Understanding the Behaviors of Environment-aware Information Retrieval
Recent retrieval-augmented generation (RAG) approaches have demonstrated strong capability in handling complex queries, yet current research overlooks a critical challenge: different retrievers require fundamentally different query formulation strategies for optimal performance. In this work, we present the first systematic analysis of how LLMs can learn to adapt their query formulation strategies for different retrievers via reinforcement learning (RL). Our empirical study reveals that RL effectively teaches an LLM to tailor its queries to specific retriever characteristics. We discover that different retrievers exhibit surprisingly distinct optimal query styles (e.g., descriptive vs. question-like), suggesting strategies learned for one retriever ineffective for another. We further show that performance can be enhanced by incorporating retriever-specific human guidance and by scaling model size. To facilitate learning over multi-retrieval-step trajectories, we introduce a branching-based rollout technique that improves training stability. Our work provides the first empirical evidence and actionable insights for building truly retriever-aware RAG systems. Code and resources are available at https://github.com/LCO-Embedding/Envs-aware-Information-Retrieval.

[2] When Does Mixing Help? Analyzing Query Embedding Interpolation in Multilingual Dense Retrieval
While mixed-language querying is ubiquitous in multilingual communities, the sensitivity of dense retrievers to such queries remains poorly understood. We present a ratio-controlled study on mMARCO that systematically evaluates retrieval performance by varying the mixing proportion of parallel query translations via embedding-level mixing -- constructing mixed queries as an interpolation of monolingual embeddings. Experiments with BGE-M3 demonstrate that an optimal mixing ratio outperforms the best monolingual endpoint in 88/105 cases. We uncover a distinct asymmetry driven by English dominance: mixing is uniformly beneficial when retrieving from non-English document indices, whereas indices containing English are best served by pure English queries. Furthermore, English acts as the strongest mixing partner for every non-English document language. Finally, when controlling for English dominance, mixing gains correlate negatively with typological distance. We conclude that language-mix sensitivity is structured and predictable, and we validate the robustness of these patterns across model families and scales.

[3] RL-Index: Reinforcement Learning for Retrieval Index Reasoning
Retrieving external knowledge is essential for solving real-world tasks, yet it remains challenging when the relationship between a query and its relevant knowledge involves implicit and complex reasoning beyond surface-level semantic or lexical matching (e.g., mathematical problems relying on the same theorem or coding requiring deep reasoning). Existing approaches primarily rely on query-side reasoning (e.g., query rewriting), which introduces significant online latency and underutilizes the opportunity to perform reasoning over the knowledge corpus itself (i.e., index-side reasoning). In this paper, we propose RL-Index, an agentic indexing framework that formulates retrieval index reasoning as a reinforcement learning problem. Instead of performing reasoning at query time, RL-Index shifts reasoning to the indexing stage by augmenting documents with LLM-generated rationales that explicitly encode the latent query-knowledge relationship. To optimize the quality of these rationales, we employ Group Relative Policy Optimization (GRPO) and use retrieval similarity as a verifiable reward signal, enabling direct optimization of indexing decisions for retrieval effectiveness. Extensive experiments on the BRIGHT benchmark demonstrate that RL-Index consistently improves both retrieval and downstream question-answering performance, while significantly reducing online inference latency. Moreover, the learned rationale augmentation generalizes across diverse retrievers and generators, highlighting its robustness as a plug-and-play indexing strategy across different retrieval systems.
```

---

## GHR0015 — gh_72_cited_answer_3

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 5
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval'?

### Claim

It is used to evaluate image retrieval performance in crowded scenes.

### Evidence

```text
[1] LARE: Low-Attention Region Encoding for Text-Image Retrieval
Image retrieval in crowded scenes is particularly challenging due to the salience bias of conventional visual encoders, which tend to focus on dominant objects while neglecting low-attention regions that are often crucial for fine-grained retrieval. We propose LARE (Low-Attention Region Encoding), a framework that explicitly models these overlooked regions. LARE adopts a dual-encoding strategy that encodes low-attention regions of an image and the full image in parallel, leading to more diverse and informative image embeddings. To evaluate image retrieval performance in challenging crowded scenes, we introduce Dense-Set, a challenging subset derived from COCO and Flickr30K. In this subset, images are re-captioned to provide richer descriptions of low-attention or previously overlooked regions. This dataset highlights the limitations of existing retrieval models and enables a more rigorous evaluation under densely crowded scene conditions. Experimental results demonstrate that the proposed framework improves retrieval performance by preserving subtle, non-dominant visual cues within the shared latent space.
```

---

## GHR0082 — gh_38_cited_answer_2

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 6
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments', and what problem is it designed to address?

### Claim

This benchmark is designed to address the problem of insufficient benchmarks for systematically evaluating agentic academic search under realistic open literature environments.

### Evidence

```text
[1] ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments
Academic paper search is a core step in scientific research, and LLM-based search agents are emerging as a promising paradigm for iterative, intent-driven literature exploration. However, existing benchmarks are insufficient for systematically evaluating agentic academic search under realistic open literature environments. We propose ScholarQuest, a large-scale, taxonomy-guided benchmark for agentic academic paper search. ScholarQuest is constructed from over 1,000 computer science topics and four representative research intents, including method-oriented, setting-anchored, comparison-based, and scope-controlled queries. It further provides scalable answer construction and a shared retrieval backend ScholarBase for reproducible evaluation. Benchmarking results show that agentic methods outperform single-shot retrieval baselines, yet the best-performing agent only achieves 0.314 Recall@100 and 0.355 Recall@All, indicating substantial room for improvement. In addition, analyses of search efficiency, intent-level robustness, and failure cases further highlight the benchmark's ability to provide multi-dimensional evaluation signals for academic paper search agents.

[2] EComAgentBench: Benchmarking Shopping Agents on Long-Horizon Tasks with Distributed Hidden Intent
As LLM-based shopping agents enter production, existing benchmarks fail to capture how a shopper's requirements arrive: stated implicitly in the query, recorded in a profile, or revealed only when the right question is asked. Benchmarks that expose full intent upfront and grade only the final choice can neither pose this long-horizon challenge nor explain which requirement an agent missed. To address this gap, we introduce EComAgentBench, a benchmark of 662 tasks grounded in real Amazon products and reviews. Each task scatters these requirements across a visible query, a tool-gated profile, and scripted clarification; an agent must uncover hidden intent, verify candidates against attributes and review evidence, and commit to a single product within 100 tool calls. Moreover, typed, source-tagged rubrics grade every task, attributing each failure to a requirement and its source. Construction is automated yet reliable, with every answer fixed in code before any text is generated and every sample validated. Our evaluation of seven models reveals that even the strongest attains only 57.1% overall accuracy, and rubric satisfaction degrades from visible to hidden sources. Overall, we believe EComAgentBench will serve as a reproducible foundation for moving shopping agents from single-query search toward dependable assistance over long horizons.

[3] SAERec: Constructing Fine-grained Interpretable Intents Priors via Sparse Autoencoders for Recommendation
Intent-based recommender systems have gained significant attention for improving accuracy and interpretability by modeling the underlying motivations behind user behaviors. Most existing models derive intents directly from user sequences via clustering or prototype learning. However, they are sensitive to sequence quality, require presetting the number of intents, and lack explicit semantic grounding. These issues lead to an incomplete and coarse intent set and limit the effectiveness of recommendation. In this paper, we propose the Sparse Autoencoder for intent-based recommendation (SAERec), a novel recommender that automatically constructs a fine-grained and interpretable intent space from a textual corpus to guide recommendation. Rather than treating texts as side signals, SAERec leverages them as high information density evidence for intent construction. Specifically, we first extract a comprehensive set of fine-grained interpretable intents from the latent space of large language models (LLMs) by using a sparse autoencoder (SAE) to disentangle and interpret text embeddings, which isolates intent-related semantics from textual noise. Then, for each user, we retrieve relevant intents from this set as priors to guide recommendation. It contains personal intents matching a user's current interests and public intents capturing general item patterns shared across users (e.g., quality, price). Finally, to integrate retrieved intents into sequence modeling, we propose a multi-branch attention mechanism that captures temporal dependencies and injects both personal and public intent signals, followed by an adaptive fusion layer to construct the final user representation for recommendation. Extensive experiments on public datasets demonstrate the superiority of SAERec, consistently outperforming state-of-the-art baselines while providing human-understandable explanations.
```

---

## GHR0073 — gh_41_cited_answer_3

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 7
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation'?

### Claim

To address this, the paper proposes DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently, and aggregates them back into a single vector while preserving the standard one-query-one-document interface.

### Evidence

```text
[1] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.

[2] Context Compression Is Not One Thing: Readable Symbolic Re-expression vs. Coherent Summary at Matched Budget
We study context compression for multi-hop question answering with small language models. We propose Telegraph English, a readable symbolic format that rewrites retrieved passages into structured entity-relation statements, preserving reasoning evidence at lower token cost. In controlled experiments on MuSiQue, TwoWiki, and HotpotQA, Telegraph English outperforms three matched-budget compression baselines (character-level deletion, truncation, and random sub-sampling) on every dataset, with gains of 13 to 20 F1 percentage point. It also outperforms a coherent prose summary produced by the same encoder on the hardest dataset. A pre-registered depth-interaction hypothesis is null: the advantage does not grow with reasoning depth within datasets. We interpret these results as evidence that readable symbolic re-expression preserves entity content more densely than either natural language or coherent summarization at matched token budget.

[3] Query-aware Routing for Filtered Approximate Nearest Neighbors Search
Filtered ANN search, which combines vector similarity with attribute predicates, is a core primitive in modern vector databases and retrieval-augmented generation. We benchmark all major categorical filtered ANN methods across multiple datasets under three predicates and find that no single method dominates. Moreover, even within a single dataset and predicate type, the best method for a query can vary. Therefore, we propose a query-aware routing framework. A lightweight ML model predicts each candidate method's recall on the query, and the router consults an offline benchmark table that maps every method and parameter setting to its measured recall and QPS, then selects the method with the best recall--QPS trade-off. Our ablation study narrows 22 candidate features to a minimal set of three and we adopt regression rather than classification as the prediction target to sharpen accuracy. Our model is trained on six real-world datasets and applied to five unseen validation datasets. The final result shows that our router achieves state-of-the-art recall and QPS balance across all five validation datasets compared to existing filtered ANN baselines, while incurring negligible latency overhead.
```

---

## GHR0144 — gh_141_plain_answer_1

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 8
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'Compact Geometric Representations of Hierarchies'?

### Claim

The paper 'Compact Geometric Representations of Hierarchies' is not mentioned in the sources provided.

### Evidence

```text
[1] Querit-Reranker: Training Compact Multilingual Rerankers via Efficient Label-Free Distribution Adaptation
Deployable multilingual rerankers must generalize across languages, domains, and target ranking tasks while remaining efficient enough for second-stage reranking. However, adapting them to new target distributions typically requires extensive task-specific relevance annotations, which are costly to obtain. We present Querit-Reranker, a family of multilingual cross-encoder rerankers trained with a data-centric pipeline for label-efficient adaptation. We instantiate it as Querit-Reranker-A0.4B, initialized from an in-house MoE backbone with 0.4B activated parameters, and Querit-Reranker-4B, initialized from Qwen3-Embedding-4B. Our pipeline first learns general relevance modeling from large-scale ranking-oriented data, then adapts to target distributions through synthetic-query mining with teacher scores as continuous soft labels. To consolidate complementary task-adapted strengths, we further merge checkpoints via spherical linear interpolation, obtaining a single deployable model without runtime ensembling overhead. Using Qwen3-Embedding-0.6B as the shared first-stage retriever, Querit-Reranker-A0.4B improves average nDCG@10 from 54.11 to 59.28 on BEIR and from 59.87 to 67.70 on MIRACL. On MTEB Multilingual v2 Reranking, it also substantially outperforms larger embedding-based baselines, while Querit-Reranker-4B further achieves state-of-the-art performance among publicly available models. We release both models on Hugging Face.

[2] Non-negative Elastic Net Decoding for Information Retrieval
Dense retrieval has become the dominant paradigm in information retrieval, in which each document is scored against a query by the inner product of their vector embeddings, and the top-$k$ documents by score are retrieved for this query. However, since each document's score depends solely on the embedding of the query and itself, the retrieval process is oblivious to the content of the entire corpus. Therefore, dense retrieval cannot avoid selecting semantically similar documents from the corpus, which may result in a non-diverse, redundant set of retrieved documents. To this end, we approach retrieval as a joint decoding problem, in which documents are selected as a set with regard to the context of the rest of the corpus. To achieve this, we propose Non-Negative elastic Net (NNN) decoding, which selects documents whose embeddings jointly reconstruct the query embedding as a sparse non-negative linear combination. Our main theoretical result establishes a strict separation between dense retrieval and NNN decoding. For any corpus, every query correctly handled by dense retrieval is also handled by NNN decoding, while on corpora containing correlated documents, NNN decoding additionally handles queries that dense retrieval cannot. Experimental results indicate that applying NNN decoding to frozen embeddings trained for inner-product scoring yields consistent improvements across several benchmarks. Moreover, we introduce an end-to-end training procedure which optimizes the embeddings for NNN decoding, producing significant performance gains surpassing in all metrics and benchmarks compared to dense retrieval. Our work establishes a new paradigm for leveraging dense embeddings in information retrieval, beyond the standard practice of inner-product scoring.
```

---

## GHR0076 — gh_23_cited_answer_3

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 9
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems', and what problem is it designed to address?

### Claim

MonaVec targets the deployment profile of SQLite: one file, one function call, runs anywhere.

### Evidence

```text
[1] MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems
We present MonaVec, a deterministic, embedded vector-search kernel for edge and offline AI -- settings where server infrastructure, network connectivity, and training data are all unavailable. Existing vector-search systems assume a persistent server, gigabytes of RAM, or a training pass over the corpus; MonaVec instead targets the deployment profile of SQLite: one file, one function call, runs anywhere. Its quantization core is training-free by default and data-oblivious: a Randomized Hadamard Transform (RHDH) conditions any input distribution toward N(0,1), so precomputed Lloyd-Max tables quantize to 4 bits (8x smaller) with no learned codebook and no data pass. The index persists as a single .mvec file whose embedded ChaCha20 rotation seed makes results reproducible across architectures and byte-identical within a build -- a determinism guarantee that parallel-build graph libraries cannot offer. On semantic embeddings (AG News, 45K x 1024-dim BGE-M3, cosine), MonaVec 4-bit BruteForce reaches 0.960 Recall@10 in 27 MB -- leading float32 FAISS-IVF and 8-bit usearch on recall -- while trading peak throughput for byte-identical determinism. A single-pass global standardization (fit()) extends the same data-oblivious pipeline to magnitude-sensitive L2 data, and optional IvfFlat and HNSW backends carry it to million-vector corpora. MonaVec is implemented in pure Rust with Python bindings and runtime SIMD dispatch (AVX-512/AVX2/NEON/scalar). It targets on-device RAG, offline agents, and embedded retrieval -- the niche SQLite occupies for relational data: one file, one call, runs anywhere.

[2] SCAR: Semantic Continuity-Aware Retrieval for Efficient Context Expansion in RAG
Fixed-length chunking in Retrieval-Augmented Generation (RAG) often leads to boundary fragmentation, where critical evidence is split across segments, degrading retrieval recall. While static windowing and parent retrieval improve recall, they introduce significant token overhead. We propose SCAR (Semantic Continuity-Aware Retrieval), an adaptive retrieval policy that selectively expands neighboring chunks by weighing query-neighbor relevance against a structural continuity penalty. SCAR uses a relative expansion threshold tied to each retrieved chunk's own query-relevance, yielding an approximately scale-invariant decision rule that transfers across embedding models without recalibration. Across four diverse corpora (RFC, GDPR, a 10-K report, and a Merger agreement; N=320 queries; 160 boundary-fragmented), SCAR achieves 92.8% recall on boundary-fragmented queries with only 7.84 chunks, a 22.9% reduction compared to static windowing (10.16 chunks). Paired bootstrap tests (B=10,000) confirm the chunk reduction is highly significant (p<0.0001, Cohen's d=-1.49, large effect), with a small recall difference (Cohen's d=-0.33). The policy transfers across three embedding models (text-embedding-3-large, BGE-large-en-v1.5, zembed-1) using the same single hyperparameter setting, and downstream RAGAS evaluation on the 10-K corpus confirms SCAR preserves generation faithfulness while reducing context tokens by 27.1%.

[3] Charge as a Construct-Validity Factor in Chinese Legal Case Retrieval: A Cross-Benchmark Audit
Chinese Legal Case Retrieval (LCR) benchmarks grade a reference judgment relevant when its legal characterization matches the query, and strong systems now reach NDCG@10 of 0.85-0.88. Most of the BM25-to-best-trained gap is recoverable with no retrieval model: ranking candidates only by shared primary charge, broken by BM25, closes 99.2% of it on LeCaRDv2 -- with no detectable difference from the best-trained system. This reflects benchmark design: LeCaRDv2 defines top relevance via the crime's key constitutive elements, which encode the charge, so same-charge cases are relevant by construction (relevance lift 4.49; charge-to-relevance macro-AUC 0.871). Holding charge fixed, the trained reranker's advantage over BM25 collapses to a small within-charge residual (+0.026 NDCG@10, cluster-bootstrap CI excluding zero, about a quarter), the only non-definitional positive. The effect is not uniform: the same rule recovers 84.3% on LeCaRDv1 and is out of spec on CAIL2022, with the charge-to-relevance signal weakening in step (macro-AUC 0.871/0.759/0.728); a predicted-charge cascade reproduces 76.6% on LeCaRDv2 but does not transfer. The construct is also cashable at first stage: an exploratory zero-training charge-pool channel lifts LeCaRDv2 recall (R@100 +0.025, wrong-charge controls hurt), reported as a positive control for the confound, not a retrieval method or novelty claim. Charge is thus a high-leverage construct-validity factor at the benchmark level -- not auniform explanation of NDCG@10, and not evidence that any system relies on charge. We package established construct-validity and partial-input checks as a reusable charge-controlled protocol (CCE); o

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0102 — gh_43_plain_answer_3

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 10
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'EComAgentBench: Benchmarking Shopping Agents on Long-Horizon Tasks with Distributed Hidden Intent'?

### Claim

The agent must uncover hidden intent, verify candidates against attributes and review evidence, and commit to a single product within 100 tool calls.

### Evidence

```text
[1] EComAgentBench: Benchmarking Shopping Agents on Long-Horizon Tasks with Distributed Hidden Intent
As LLM-based shopping agents enter production, existing benchmarks fail to capture how a shopper's requirements arrive: stated implicitly in the query, recorded in a profile, or revealed only when the right question is asked. Benchmarks that expose full intent upfront and grade only the final choice can neither pose this long-horizon challenge nor explain which requirement an agent missed. To address this gap, we introduce EComAgentBench, a benchmark of 662 tasks grounded in real Amazon products and reviews. Each task scatters these requirements across a visible query, a tool-gated profile, and scripted clarification; an agent must uncover hidden intent, verify candidates against attributes and review evidence, and commit to a single product within 100 tool calls. Moreover, typed, source-tagged rubrics grade every task, attributing each failure to a requirement and its source. Construction is automated yet reliable, with every answer fixed in code before any text is generated and every sample validated. Our evaluation of seven models reveals that even the strongest attains only 57.1% overall accuracy, and rubric satisfaction degrades from visible to hidden sources. Overall, we believe EComAgentBench will serve as a reproducible foundation for moving shopping agents from single-query search toward dependable assistance over long horizons.

[2] DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents
Deep research agents synthesize long-form reports by searching and reasoning over retrieved evidence. Reinforcement learning with rubric-based rewards improves these agents by optimizing them against checkable criteria that translate report quality into reward signals, but its efficiency depends on whether those criteria reliably capture the task scope and evidence needs. Most existing studies ask an LLM to generate rubrics for a given query, but when the model fails to infer the underlying information needs, the generated rubrics may be incomplete and reduce RL efficiency. To obtain more reliable query--rubric supervision, we introduce DeepRubric, a data construction framework that reverses this process: instead of inferring evaluation criteria for a given query, it first determines what an evidence-backed report should be evaluated on and then synthesizes aligned query--rubric pairs from those evaluation targets. Starting from a sampled seed topic, DeepRubric builds an evidence tree by recursively expanding evidence-backed sub-questions, whose leaves serve as atomic and verifiable evaluation targets. It then uses the evidence tree to synthesize the training query and rubrics, ensuring that the reward evaluates exactly the information requested by the query. Using DeepRubric, we construct 9K query--rubric supervision examples and train DeepRubric-8B with rubric-based GRPO, achieving comparable performance to prior open state-of-the-art deep research models across three benchmarks with roughly 13x fewer RL GPU-hours.

[3] Let LLMs Judge Each Other: Multi-Agent Peer-Reviewed Reasoning for Medical Question Answering
Objective: To enhance the accuracy, interpretability, and robustness of large language models (LLMs) in medical question answering (MedQA). Method: We designed a multi-agent peer-reviewed reasoning method in which multiple LLM agents independently generate chain-of-thought reasoning with candidate answers, then act as peer reviewers to evaluate each other's reasoning for factual correctness and logical soundness. The highest-rated reasoning chain is selected to produce the final answer. Experiments were conducted with five state-of-the-art LLMs (Llama-3.1-8B, Qwen2.5-7B, Phi-4, DeepSeek-LLM-7B, GPT-oss-20B) on three benchmark datasets: HeadQA, MedQA-USMLE, and PubMedQA. Performance was compared against single-model chain-of-thought reasoning and chain-of-thought-based majority voting. Results: Peer-reviewed reasoning consistently outperformed both baselines. The best model combination achieved an average accuracy of 0.820 across datasets, exceeding the strongest single model (0.777) and majority voting ensembles (up to 0.789). The method also scaled effectively with more participating models, while peer assessments reliably distinguished high- from low-quality reasoning chains. Conclusion: The proposed multi-agent peer-reviewed reasoning method enables LLMs to act as both solvers and evaluators, yielding superior performance in MedQA. By emphasizing reasoning quality rather than answer agreement alone, this approach improves accuracy, interpretability, and robustness, offering a promising direction for trustworthy biomedical AI systems.
```

---

## GHR0021 — gh_55_cited_answer_3

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 11
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio', and what problem is it designed to address?

### Claim

The dataset provides expert-curated meta-analyses from Nature Portfolio journals, including research questions, PI/ECO criteria, retrieval corpora, verified positive studies, hard negatives, search strategies, and date bounds.

### Evidence

```text
[1] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.
```

---

## GHR0135 — gh_114_cited_answer_2

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 12
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

I cannot report the main experimental results or comparisons from that paper using the given sources.

### Evidence

```text
[1] ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents
Tool-using LLM agents increasingly use the Model Context Protocol (MCP) to answer from heterogeneous evidence sources, including search, APIs, databases, clinical records, and formulary tools. Standard factuality metrics usually test whether an answer is supported by pooled evidence, missing a provenance-sensitive failure mode: a claim may be supported somewhere while being attributed to the wrong source. We call this cross-source conflation. We introduce ProvenanceGuard, a source-aware verifier for MCP-grounded answers. It consumes captured MCP traces with stable tool IDs, source IDs, and raw outputs; decomposes answers into atomic claims; routes claims to source-specific evidence; checks support with NLI and a token-alignment proxy; compares stated attribution with the routed source; and returns per-claim verdicts plus an answer-level allow/block decision. Blocked answers can be repaired with retrieval-augmented answer revision and re-verified. We evaluate on 281 medical-domain MCP-agent traces. A 266-trace adjudicated subset yields 2,325 LLM-assisted claim labels split by trace; 361 held-out labels are human-verified. On the 40-trace held-out split, ProvenanceGuard achieves block F1 0.802 and source accuracy 0.858 over 260 source-eligible claims, outperforming source-blind baselines that do not emit claim-to-source IDs. On a harder multi-source benchmark it reaches block F1 0.846, while source-plus-relation accuracy drops to 0.229, showing that exact source ownership remains difficult with semantically close sources. Repair-and-reverify resolves all blocked answers in the full trace set, often via conservative fallback. In 50 controlled clinical conflation probes, ProvenanceGuard detects all injected attribution swaps with no retained wrong attribution. These results show that source attribution is an independent axis for factuality verification in MCP-based agents.

[2] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.
```

---

## GHR0085 — gh_49_cited_answer_2

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 13
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation'?

### Claim

DICE (Document Inference via Chunk Evidence), a training-free document-side strategy, improves retrieval across four backbones on LongEmbed.

### Evidence

```text
[1] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.

[2] Context Compression Is Not One Thing: Readable Symbolic Re-expression vs. Coherent Summary at Matched Budget
We study context compression for multi-hop question answering with small language models. We propose Telegraph English, a readable symbolic format that rewrites retrieved passages into structured entity-relation statements, preserving reasoning evidence at lower token cost. In controlled experiments on MuSiQue, TwoWiki, and HotpotQA, Telegraph English outperforms three matched-budget compression baselines (character-level deletion, truncation, and random sub-sampling) on every dataset, with gains of 13 to 20 F1 percentage point. It also outperforms a coherent prose summary produced by the same encoder on the hardest dataset. A pre-registered depth-interaction hypothesis is null: the advantage does not grow with reasoning depth within datasets. We interpret these results as evidence that readable symbolic re-expression preserves entity content more densely than either natural language or coherent summarization at matched token budget.

[3] Adaptive Multi-Resolution Procedural Knowledge Compression for Large Language Models
Large language models (LLMs) are widely used to tackle complex tasks with autonomous workflows. Recently, reusable natural language skills have emerged as a popular paradigm to inject procedural knowledge into LLM applications. Since popular skills are often invoked repeatedly, placing their full text in every context significantly increases prefill cost and latency. While text compression techniques have the potential to solve this problem, most existing methods are designed to compress factual knowledge in documents instead of procedural knowledge, making them insufficient for skill compression. In this paper, we argue that an effective skill compression method should: 1) preserve logical dependencies among workflows and tool protocols, 2) enable lightweight, offline compression for frequently updated community skills, and 3) be adaptable to varying complexities across skills. To address this, we present SKIM (SKIll coMpression), an adaptive multi-resolution soft token compression framework for procedural skills. Depending on the complexity of each skill, SKIM creates different numbers of soft tokens that not only improve the efficiency of LLM inference, but also preserve the effectiveness of skill usage. Experiments indicate that SKIM compresses skills to 30 to 60 percent of their original token length while preserving task performance better than existing compression methods.We have released our code at https://github.com/bebr2/SKIM .
```

---

## GHR0147 — gh_136_plain_answer_1

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 14
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval'?

### Claim

The sources provided do not discuss the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval'.

### Evidence

```text
[1] Vision-language models for chest radiography do not always need the image
Medical vision-language models report strong chest radiograph accuracy, and this is increasingly read as evidence that they use the image. That inference is unsafe: a model exploiting finding-name priors scores like one that reads the scan, and no standard benchmark separates them. We introduce a causal audit that intervenes on the image, occluding the relevant region, occluding an irrelevant one, and swapping in another patient's same-label scan, and combines three behavioral metrics to test whether a correct answer depends on the image. Across nine systems, a text-only model with no image access reaches within 5.7 accuracy points of the best multimodal one, and a 119-billion-parameter multimodal model is statistically indistinguishable from a 7-billion text-only baseline. The audit splits the cohort into three models that ignore the image, one that is unstable, and five that use it selectively, for a subset of findings; the categories hold across a second dataset, resolution, and prompt phrasing. Against board-certified radiologists, a text-only model is statistically indistinguishable from a radiologist's accuracy while grounding at zero, whereas the image-using models ground at radiologist-comparable rates. Reported confidence flags ungrounded answers only when a model uses the image. Grounding audits, not accuracy, should gate clinical deployment.

[2] Visuals Lie, Consistency Speaks: Disentangling Spatial Attention from Reliability in Vision-Language Models
Multimodal Foundation Models are increasingly used as reasoning agents, making reliability, knowing when a model may hallucinate, critical. A common intuition, which we call the Attention-Confidence Assumption, holds that reliability follows from "structural" visual perception: tight attention on relevant regions should signal a trustworthy answer, while scattered attention signals confusion. We challenge this through the VLM Reliability Probe (VRP), a systematic cross-family study of reliability signals in contemporary Vision-Language Models (VLMs). We introduce structural-attention metrics, cluster counts (C_k) and spatial entropy (H_s), to quantify the visual encoder's gaze, and track its evolution (Delta H_s) across layers. This reveals a "Symbolic Detachment": models often "Early Lock" visual features only to diffuse attention later, severing early perception from final generation. Contrary to the grounding hypothesis, we find a "Cluster Failure": spatial attention has near-zero correlation (R approx 0.001) with accuracy. Instead, reliability is a phenomenon of generation dynamics and internal-state distributions. Self-Consistency, the agreement rate across sampled reasoning paths, is the dominant predictor of truth (R = 0.429). Scaling causal interventions exposes a sharp architectural divergence: LLaVA locks its prediction in a fragile late-stage bottleneck, whereas PaliGemma and Qwen2-VL distribute reliability globally, staying resilient even when ~50% or more of their most predictive layer is destroyed. For current VLMs, reliability signals are detached from visual grounding maps and are best inferred from generation-time dynamics and hidden-state probes.
```

---

## GHR0011 — gh_151_plain_answer_2

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 15
- sampling_stratum: `drop_home_related::plain_answer`
- sampling_weight: `4.333333333333333`
- hard_policy: `drop_home_related`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems', and what problem is it designed to address?

### Claim

I cannot answer the question based on the information in the sources.

### Evidence

```text
[1] MLT-Dedup: Efficient Large-Scale Online Video Deduplication via Multi-Level Representations and Spatial-Temporal Matching
The explosive growth of user-generated video content on online platforms is accompanied by the emergence of numerous near-duplicate videos--videos that are identical or highly similar but differ by partial edits. These duplicates degrade user experience and increase storage and bandwidth costs, making large-scale video deduplication a critical task. Existing video deduplication frameworks face a fundamental challenge in retrieving sufficient high-quality candidates under a limited index budget, as well as trade-offs between efficiency and precision. To address these issues, we propose MLT-Dedup, an efficient large-scale online video deduplication framework with Multi-Level representations and spatial-Temporal matching. Our approach employs a Multi-Level Video Encoder (ML-VE) to extract both fine-grained frame-level and sparse clip-level embeddings: sparse embeddings support efficient candidate retrieval, while fine-grained embeddings are loaded for precise pairwise matching. During matching, we introduce DiF-SiM, a Differential Feature-enhanced Similarity Module capable of locating duplicated temporal segments and providing reliable similarity evidence to support policy-driven deduplication decisions. Extensive experiments on a real-world large-scale platform demonstrate that MLT-Dedup reduces online repetition rates by 91% at 90% precision. Furthermore, our sparse retrieval design achieves a 5x increase in indexing capacity, enabling broader candidate coverage in real-world deployment.

[2] CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents
Personalized dialogue agents require continuous long-term memory to maintain coherent interactions across multiple sessions. However, deploying these capabilities on consumer-grade hardware (e.g., 8 GB VRAM edge devices) introduces severe memory and compute bottlenecks. Existing systems typically rely on isotropic cosine similarity for retrieval and heuristic rules for context compression. These approaches lack a unified theoretical foundation, frequently suffering from the hubness problem in high-dimensional retrieval and syntactic fragmentation during compression. To overcome these limitations, we propose CoreMem, a resource-efficient edge-cloud memory architecture fundamentally unified by information geometry. First, Riemannian retrieval replaces cosine matching with a locally adaptive Fisher-Rao metric, effectively penalizing hub memories via Mahalanobis distance with O(Ndr) Woodbury acceleration for real-time search. Second, Fisher-guided discrete token distillation (FDTD) introduces a hierarchical sentence-to-token compression mechanism. It derives sensitivity scores from Fisher information traces, providing a principled compression-KL tradeoff augmented with explicit structural syntax protection. Evaluated on the LOCOMO and LongMemEval-S benchmarks, CoreMem achieves strong accuracy improvements, yielding substantial gains in Open-domain (+4.51 pp) and Temporal (+4.17 pp) reasoning. Extensive profiling confirms that CoreMem operates seamlessly within a strict 8 GB VRAM budget, successfully bridging the gap between resource-constrained edge devices and the demand for theoretically grounded, lifelong memory agents.
```

---

## GHR0055 — gh_64_plain_answer_10

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 16
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Understanding the Behaviors of Environment-aware Information Retrieval'?

### Claim

the paper does not discuss any specific ablations or control groups in the context of the experiments conducted.

### Evidence

```text
[1] Understanding the Behaviors of Environment-aware Information Retrieval
Recent retrieval-augmented generation (RAG) approaches have demonstrated strong capability in handling complex queries, yet current research overlooks a critical challenge: different retrievers require fundamentally different query formulation strategies for optimal performance. In this work, we present the first systematic analysis of how LLMs can learn to adapt their query formulation strategies for different retrievers via reinforcement learning (RL). Our empirical study reveals that RL effectively teaches an LLM to tailor its queries to specific retriever characteristics. We discover that different retrievers exhibit surprisingly distinct optimal query styles (e.g., descriptive vs. question-like), suggesting strategies learned for one retriever ineffective for another. We further show that performance can be enhanced by incorporating retriever-specific human guidance and by scaling model size. To facilitate learning over multi-retrieval-step trajectories, we introduce a branching-based rollout technique that improves training stability. Our work provides the first empirical evidence and actionable insights for building truly retriever-aware RAG systems. Code and resources are available at https://github.com/LCO-Embedding/Envs-aware-Information-Retrieval.
```

---

## GHR0138 — gh_131_plain_answer_2

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 17
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World', and what problem is it designed to address?

### Claim

I cannot answer the question using the information in the sources.

### Evidence

```text
[1] ComAct: Reframing Professional Software Manipulation via COM-as-Action Paradigm
Existing computer-use agents remain fundamentally limited in professional software manipulation: GUI-based agents suffer from fragile visual grounding and long-horizon error accumulation, while API-basedapproaches struggle with heterogeneous protocols and inaccessible commercial interfaces. In this work,we identify the Component Object Model (COM) as a unified executable abstraction, proposing COM-as-Action: a new paradigm that reframes professional software interaction as deterministic program synthesisrather than sequential visual control. To validate this paradigm in the most demanding environments, weintroduce ComCADBench, the first benchmark for agents operating real industrial CAD software. Ourexperiments reveal a substantial paradigm gap: frontier proprietary models achieve near-zero successunder GUI-based interaction, whereas COM-based execution yields substantial immediate gains. Tobridge the remaining gap between syntactic correctness and geometric accuracy, we develop ComActor, aself-correcting agent trained through a progressive three-stage framework, alongside ComForge, a scalableplatform for large-scale training in Windows containers. Extensive experiments show that ComActorachieves state-of-the-art performance on ComCADBench, with strong resilience in long-horizon taskswhere baselines collapse, and generalizes to external CAD benchmark.

[2] PACMS: Submodular Context Selection as a Pluggable Engine for LLM Agents
Conversational and tool-using LLM agents operate over a context window that fills from several directions simultaneously. As a session proceeds, the agent accumulates user and assistant turns, entries drawn from a persistent memory store, and often largest of all, the verbatim outputs of tool calls such as file reads, search results, and API responses. Once the cumulative context exceeds the model's token budget, the framework must decide what to keep. The prevailing mechanism is recency truncation, sometimes paired with periodic summarization. This is topic-blind: a fact established early in a session is discarded simply because it is old, even when the current user query is about exactly that fact; conversely, verbose but irrelevant recent material is retained. Agents that must recall information across many turns, the defining case for memory, are precisely where recency truncation fails. Existing alternatives sit outside the agent's assembly step. Retrieval augmented generation fetches external documents into the prompt but does not arbitrate the agent's \emph{already-present} pooled context. Context-compression methods reduce token count by rewriting or pruning text, but operate query-blind and lossily. Neither treats memory entries, conversation turns, and tool outputs as a single candidate pool to be selected from by relevance at the moment the prompt is assembled.
```

---

## GHR0075 — gh_41_cited_answer_7

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 18
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation'?

### Claim

Regarding analysis findings, the paper establishes document-level encoding as a practical and underexplored lever for long-document retrieval.

### Evidence

```text
[1] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.

[2] Context Compression Is Not One Thing: Readable Symbolic Re-expression vs. Coherent Summary at Matched Budget
We study context compression for multi-hop question answering with small language models. We propose Telegraph English, a readable symbolic format that rewrites retrieved passages into structured entity-relation statements, preserving reasoning evidence at lower token cost. In controlled experiments on MuSiQue, TwoWiki, and HotpotQA, Telegraph English outperforms three matched-budget compression baselines (character-level deletion, truncation, and random sub-sampling) on every dataset, with gains of 13 to 20 F1 percentage point. It also outperforms a coherent prose summary produced by the same encoder on the hardest dataset. A pre-registered depth-interaction hypothesis is null: the advantage does not grow with reasoning depth within datasets. We interpret these results as evidence that readable symbolic re-expression preserves entity content more densely than either natural language or coherent summarization at matched token budget.

[3] Query-aware Routing for Filtered Approximate Nearest Neighbors Search
Filtered ANN search, which combines vector similarity with attribute predicates, is a core primitive in modern vector databases and retrieval-augmented generation. We benchmark all major categorical filtered ANN methods across multiple datasets under three predicates and find that no single method dominates. Moreover, even within a single dataset and predicate type, the best method for a query can vary. Therefore, we propose a query-aware routing framework. A lightweight ML model predicts each candidate method's recall on the query, and the router consults an offline benchmark table that maps every method and parameter setting to its measured recall and QPS, then selects the method with the best recall--QPS trade-off. Our ablation study narrows 22 candidate features to a minimal set of three and we adopt regression rather than classification as the prediction target to sharpen accuracy. Our model is trained on six real-world datasets and applied to five unseen validation datasets. The final result shows that our router achieves state-of-the-art recall and QPS balance across all five validation datasets compared to existing filtered ANN baselines, while incurring negligible latency overhead.
```

---

## GHR0093 — gh_50_plain_answer_9

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 19
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio'?

### Claim

Additional Insight: The study introduces MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals.

### Evidence

```text
[1] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.

[2] LAUKIN: A Multi-jurisdictional Common Law Contract Dataset
Multinational companies increasingly require cross-jurisdictional contract review, yet existing legal NLP datasets are largely restricted to a single jurisdiction. We introduce LAUKIN (Legal equivalence dataset of Australia, UK, and INdia), a dataset of clause pairs (AU-UK, UK-IN, IN-AU) labelled for boolean legal equivalence. We develop a novel multi-stage retrieval and reranking pipeline to construct the initial clause pair mapping, with a subset of clause pairs subsequently annotated by legal experts as Equivalent or Not Equivalent. The dataset comprises 14,727 clause pairs from 204 contracts across 8 agreement types, of which 3,000 are manually labelled: 900 train, 600 dev, and 1,500 test. We evaluate 12 models across 4 techniques, achieving a best macro-F1 of 65.11%, establishing LAUKIN as a challenging benchmark. Results reveal that, despite shared legal heritage, drafting conventions diverge significantly across jurisdictions, making cross-jurisdictional equivalence classification non-trivial. LAUKIN also includes 11,727 unlabelled training pairs to support future semi-supervised learning research in legal NLP.

[3] Query-aware Routing for Filtered Approximate Nearest Neighbors Search
Filtered ANN search, which combines vector similarity with attribute predicates, is a core primitive in modern vector databases and retrieval-augmented generation. We benchmark all major categorical filtered ANN methods across multiple datasets under three predicates and find that no single method dominates. Moreover, even within a single dataset and predicate type, the best method for a query can vary. Therefore, we propose a query-aware routing framework. A lightweight ML model predicts each candidate method's recall on the query, and the router consults an offline benchmark table that maps every method and parameter setting to its measured recall and QPS, then selects the method with the best recall--QPS trade-off. Our ablation study narrows 22 candidate features to a minimal set of three and we adopt regression rather than classification as the prediction target to sharpen accuracy. Our model is trained on six real-world datasets and applied to five unseen validation datasets. The final result shows that our router achieves state-of-the-art recall and QPS balance across all five validation datasets compared to existing filtered ANN baselines, while incurring negligible latency overhead.
```

---

## GHR0026 — gh_69_cited_answer_3

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 20
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese'?

### Claim

Four Brazilian Portuguese external corpora (N=1771 eligible cases)

### Evidence

```text
[1] Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese
Byte-Pair Encoding tokenization is statistically efficient for vocabulary compression, but semantically blind to structured technical entities, fragmenting physical quantities, numbers, units, and symbolic expressions into lexically arbitrary subwords. We present TOTEN, a knowledge-based ontological tokenization framework that replaces statistical derivation with declarative classification grounded in a formal ontology of engineering entities (OEE). We formalize TOTEN as the triple <O, classify, {inst_tau}>: the ontology gathers types, structural principles, composition relations, and preservable invariants; the classification function maps raw text into typed regions; and the instantiator family yields a self-descriptive structured representation. Robustness derives from deterministic coupling with three external oracles: Pint (dimensional), Unicode Character Database (typographic), and RSLP (Portuguese morphology). Intrinsic evaluation covers four properties verifiable by construction -- ontological atomicity, dimensional equivalence, typographic robustness, and numerical reconstruction -- over an internal, physically validated benchmark (EngQuant, N=800) and four Brazilian Portuguese external corpora (N=1771 eligible cases). We also report detection recall, distinguishing coverage from conditional atomicity. Against eight state-of-the-art baselines, TOTEN achieves unit ontological atomicity in all contrasts and numerical reconstruction of 0.775-0.904 on external corpora, vs. 0.627-0.703 for the best baseline (Quantulum3); on EngQuant, 0.780 vs. 0.340. Differences are statistically significant (McNemar with Holm correction). Spearman correlation between internal and external rankings confirms concurrent validity of the control benchmark. Dimensional equivalence shows statistical parity with Pint, the oracle from which the system inherits dimensional authority.
```

---

## GHR0078 — gh_44_cited_answer_3

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 21
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio'?

### Claim

The paper also mentions the use of existing benchmarks, but does not specify their names .

### Evidence

```text
[1] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.
```

---

## GHR0115 — gh_34_plain_answer_4

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 22
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese'?

### Claim

They find that all three oracles contribute to the robustness of TOTEN.

### Evidence

```text
[1] Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese
Byte-Pair Encoding tokenization is statistically efficient for vocabulary compression, but semantically blind to structured technical entities, fragmenting physical quantities, numbers, units, and symbolic expressions into lexically arbitrary subwords. We present TOTEN, a knowledge-based ontological tokenization framework that replaces statistical derivation with declarative classification grounded in a formal ontology of engineering entities (OEE). We formalize TOTEN as the triple <O, classify, {inst_tau}>: the ontology gathers types, structural principles, composition relations, and preservable invariants; the classification function maps raw text into typed regions; and the instantiator family yields a self-descriptive structured representation. Robustness derives from deterministic coupling with three external oracles: Pint (dimensional), Unicode Character Database (typographic), and RSLP (Portuguese morphology). Intrinsic evaluation covers four properties verifiable by construction -- ontological atomicity, dimensional equivalence, typographic robustness, and numerical reconstruction -- over an internal, physically validated benchmark (EngQuant, N=800) and four Brazilian Portuguese external corpora (N=1771 eligible cases). We also report detection recall, distinguishing coverage from conditional atomicity. Against eight state-of-the-art baselines, TOTEN achieves unit ontological atomicity in all contrasts and numerical reconstruction of 0.775-0.904 on external corpora, vs. 0.627-0.703 for the best baseline (Quantulum3); on EngQuant, 0.780 vs. 0.340. Differences are statistically significant (McNemar with Holm correction). Spearman correlation between internal and external rankings confirms concurrent validity of the control benchmark. Dimensional equivalence shows statistical parity with Pint, the oracle from which the system inherits dimensional authority.

[2] Operadic consistency: a label-free signal for compositional reasoning failures in LLMs
Detecting LLM reasoning failures at inference time without ground-truth labels has motivated a wide range of confidence baselines, including self-consistency, semantic entropy, and P(True), built on within-question sampling and self-evaluation. Operad theory, the formalism for systems built by iterated substitution, suggests a complementary diagnostic: a model's direct answer to a compositional query should agree with the answer it produces by composing a stated decomposition of the same query. We instantiate this idea as operadic consistency (OC), a per-question signal. Across twelve instruction-tuned LLMs (4B to 671B parameters, open-weights and closed-source) on four multi-hop QA datasets, OC is strongly correlated with accuracy on every dataset (Pearson $r \in [0.86, 0.94]$, all $p \leq 0.0004$), and is the only signal we evaluate with $r \geq 0.85$ uniformly across all four datasets. Chain-of-thought self-consistency (CoT-SC; Wang et al., 2023) matches OC on HotpotQA and DROP ($r = 0.93, 0.87$) but drops to $r \approx 0.45$ on MuSiQue and StrategyQA. At the per-question level, OC contributes information beyond CoT-SC and semantic entropy on every dataset (cluster-robust $p \leq 10^{-16}$ for the OC coefficient), and the conclusion is robust to additionally controlling for constructed decomposition-aware baselines ($p \leq 10^{-13}$). The same signal yields selective-prediction improvements (accuracy at fixed coverage) over a tuned CoT-SC baseline at the equal-cost $K = 3$ budget (AUARC lifts of +0.086 to +0.096 and AUROC lifts of +0.092 to +0.164; 95% CIs exclude zero on every cell). On five frontier thinking models, where the decomposition is extracted from the model's own chain of thought, the same equal-cost comparison gives positive selective-prediction point-estimate lift on all 16 (dataset, budget, metric) cells tested, with 95% CIs excluding zero on 12 of the 16.

[3] Benchmarking Agentic Review Systems
A new class of agentic review systems are emerging as a remedy to the pressure placed on peer review systems by AI-assisted research, but it is unclear how they should be evaluated. We evaluate two open-source systems (OpenAIReview and coarse), one proprietary system (Reviewer3), and a zero-shot baseline, across six LLMs spanning frontier and efficient models. First, we study whether AI reviews on ICLR/NeurIPS papers track with papers' quality as approximated by external signals such as citations and acceptance decisions. Every system performs above chance in pairwise accuracy, and the best is OpenAIReview + GPT-5.5 at 83.0%. Second, to test whether systems can catch errors with known ground truth, we construct a perturbation benchmark that injects four categories of errors into papers across eight arXiv subject classes and measure detection recall. The strongest configuration (OpenAIReview + GPT-5.5) catches 71.6% of injected e

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0034 — gh_84_cited_answer_1

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 23
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems'?

### Claim

The paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems' discusses the following limitations, ablations, or analysis findings:

### Evidence

```text
[1] MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems
We present MonaVec, a deterministic, embedded vector-search kernel for edge and offline AI -- settings where server infrastructure, network connectivity, and training data are all unavailable. Existing vector-search systems assume a persistent server, gigabytes of RAM, or a training pass over the corpus; MonaVec instead targets the deployment profile of SQLite: one file, one function call, runs anywhere. Its quantization core is training-free by default and data-oblivious: a Randomized Hadamard Transform (RHDH) conditions any input distribution toward N(0,1), so precomputed Lloyd-Max tables quantize to 4 bits (8x smaller) with no learned codebook and no data pass. The index persists as a single .mvec file whose embedded ChaCha20 rotation seed makes results reproducible across architectures and byte-identical within a build -- a determinism guarantee that parallel-build graph libraries cannot offer. On semantic embeddings (AG News, 45K x 1024-dim BGE-M3, cosine), MonaVec 4-bit BruteForce reaches 0.960 Recall@10 in 27 MB -- leading float32 FAISS-IVF and 8-bit usearch on recall -- while trading peak throughput for byte-identical determinism. A single-pass global standardization (fit()) extends the same data-oblivious pipeline to magnitude-sensitive L2 data, and optional IvfFlat and HNSW backends carry it to million-vector corpora. MonaVec is implemented in pure Rust with Python bindings and runtime SIMD dispatch (AVX-512/AVX2/NEON/scalar). It targets on-device RAG, offline agents, and embedded retrieval -- the niche SQLite occupies for relational data: one file, one call, runs anywhere.
```

---

## GHR0024 — gh_94_cited_answer_1

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 24
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments'?

### Claim

The paper 'ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments' describes a dataset constructed from over 1,000 computer science topics .

### Evidence

```text
[1] ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments
Academic paper search is a core step in scientific research, and LLM-based search agents are emerging as a promising paradigm for iterative, intent-driven literature exploration. However, existing benchmarks are insufficient for systematically evaluating agentic academic search under realistic open literature environments. We propose ScholarQuest, a large-scale, taxonomy-guided benchmark for agentic academic paper search. ScholarQuest is constructed from over 1,000 computer science topics and four representative research intents, including method-oriented, setting-anchored, comparison-based, and scope-controlled queries. It further provides scalable answer construction and a shared retrieval backend ScholarBase for reproducible evaluation. Benchmarking results show that agentic methods outperform single-shot retrieval baselines, yet the best-performing agent only achieves 0.314 Recall@100 and 0.355 Recall@All, indicating substantial room for improvement. In addition, analyses of search efficiency, intent-level robustness, and failure cases further highlight the benchmark's ability to provide multi-dimensional evaluation signals for academic paper search agents.
```

---

## GHR0101 — gh_17_plain_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 25
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science'?

### Claim

The paper 'Which Sections of a Research Paper Best Reveal Its Research Methods?

### Evidence

```text
[1] Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science
Research methods are essential carriers of knowledge contribution in academic papers. Automatic multi-label classification of research methods can support knowledge services such as method retrieval, review generation, and research intelligence analysis. While existing studies primarily rely on titles and abstracts, abstracts often provide only limited methodological information, whereas utilizing full-text content faces challenges related to excessive length and information redundancy. Therefore, this paper proposes a segment combination strategy by partitioning the full-text content according to its physical postion. Using an annotated corpus of 1,954 full-text articles from three representative journals in Library and Information Science (JASIST, LISR, and JDoc), we evaluate the classification performance of various segments and their combinations across multiple models. Experimental results indicate that methodological information is distributed unevenly within the full-text content, with the middle-to-late and final segments exhibiting greater discriminative power. Furthermore, integrating bibliographic metadata with cross-segment combination strategies effectively enhances classification performance.

[2] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.

[3] LEDGER: A Long-Context Benchmark of Corporate Annual Reports for Grounded Financial Retrieval and Extraction
Finance reporting is a natural proving ground for large language models, and the very-long-context capabilities of recent models across all sizes make rigorous evaluation in this domain an increasingly pressing need. Yet most public financial resources reduce the task to plain-text SEC 10-K filings paired with a handful of question-answer items. We release LEDGER (Long-context Evaluation of Documents for Grounded Extraction and Retrieval), a corpus of 4,999 digitized corporate annual reports - full documents with figures, tables, and narrative, not just regulatory filings. Each report is labeled with 31 consolidated financial KPIs to be extracted and linked to the market's reaction at the earnings date. From this data we derive three evaluation benchmarks spanning the difficulty spectrum: a pure page-level KPI retrieval task with TREC-style relevance judgments over 118,048 questions in natural language, a conversational "needle-in-a-haystack" single-value lookup, and a full KPI extraction task, both from long, numerically dense reports. We additionally provide human OCR-quality annotations with inter-annotator agreement and the complete extraction, validation, and scoring toolchain. We further demonstrate the dataset's research utility with a case study linking CEO-letter rhetoric to post-publication market impact.
```

---

## GHR0008 — gh_154_plain_answer_1

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 26
- sampling_stratum: `drop_home_related::plain_answer`
- sampling_weight: `4.333333333333333`
- hard_policy: `drop_home_related`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'NEST: Narrative Event Structures in Time for Long Video Understanding', and what problem is it designed to address?

### Claim

The paper 'NEST: Narrative Event Structures in Time for Long Video Understanding' does not appear to be among the sources provided.

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.

[2] Knowledge Graph Enhanced Memory-Augmented Retrieval for Long Context Modeling
Long-context language modeling requires not only extending context windows but maintaining coherent understanding of entity states and relationships across thousands of tokens -- a challenge that semantic similarity alone cannot address. KGERMAR addresses this by constructing dynamic, context-specific knowledge graphs from input text during inference, enabling domain-adaptive retrieval that leverages both semantic similarity and explicit entity relationships. The framework performs real-time entity and relation extraction to build contextual knowledge graphs, then integrates graph-structural embeddings with textual semantics through a multi-component memory architecture. Three memory banks -- contextual, semantic, and structural -- are maintained with retrieval signals fused via learned weights to capture both surface-level semantics and deeper relational patterns. Evaluated on SlimPajama (84.7K training examples), WikiText-103 (4,358 examples), PG-19 (100 examples), and Proof-pile (46.3K examples), KGERMAR achieves up to 8.5\% lower perplexity and 2--2.5x better memory efficiency than memory-augmented baselines across context lengths from 1K to 32K tokens, with superior in-context learning performance across five NLU tasks. The dynamic knowledge graph construction approach advances memory-augmented language modeling by enabling domain-specific knowledge representation that adapts to input contexts rather than relying on fixed knowledge bases.
```

---

## GHR0134 — gh_123_cited_answer_1

**FINAL_LABEL:** `UNSUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 27
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation'?

### Claim

The paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation' discusses the limitations of fixed-length chunking in Retrieval-Augmented Generation (RAG) leading to boundary fragmentation .

### Evidence

```text
[1] SCAR: Semantic Continuity-Aware Retrieval for Efficient Context Expansion in RAG
Fixed-length chunking in Retrieval-Augmented Generation (RAG) often leads to boundary fragmentation, where critical evidence is split across segments, degrading retrieval recall. While static windowing and parent retrieval improve recall, they introduce significant token overhead. We propose SCAR (Semantic Continuity-Aware Retrieval), an adaptive retrieval policy that selectively expands neighboring chunks by weighing query-neighbor relevance against a structural continuity penalty. SCAR uses a relative expansion threshold tied to each retrieved chunk's own query-relevance, yielding an approximately scale-invariant decision rule that transfers across embedding models without recalibration. Across four diverse corpora (RFC, GDPR, a 10-K report, and a Merger agreement; N=320 queries; 160 boundary-fragmented), SCAR achieves 92.8% recall on boundary-fragmented queries with only 7.84 chunks, a 22.9% reduction compared to static windowing (10.16 chunks). Paired bootstrap tests (B=10,000) confirm the chunk reduction is highly significant (p<0.0001, Cohen's d=-1.49, large effect), with a small recall difference (Cohen's d=-0.33). The policy transfers across three embedding models (text-embedding-3-large, BGE-large-en-v1.5, zembed-1) using the same single hyperparameter setting, and downstream RAGAS evaluation on the 10-K corpus confirms SCAR preserves generation faithfulness while reducing context tokens by 27.1%.
```

---

## GHR0103 — gh_35_plain_answer_1

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 28
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization'?

### Claim

The paper 'Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization' discusses several limitations, ablations, and analysis findings.

### Evidence

```text
[1] Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization
Optimal transport (OT) has been shown to detect hallucinations in neural machine translation (NMT) by measuring the geometric distance between cross-attention distributions and a reference distribution, without any supervision. We extend this analysis to all six decoder layers of the Fairseq DE-EN model ($N=3{,}414$), showing that Wass-to-Unif and Wass-to-Data are complementary detectors specialised across hallucination types, that detection is concentrated in layers L1--L4 with L5 anti-predictive for subtler types, and that hallucinated translations lack the exploratory attention phase present in correct translations from the first decoding step. We further evaluate whether the geometric signal transfers to abstractive summarization faithfulness detection: our unsupervised OT detector on AggreFact ($N=1{,}116$) achieves $57.2\%$/$57.6\%$ balanced accuracy on CNN/XSum -- above chance but substantially below supervised MiniCheck-Flan-T5-L($69.9\%$/$74.3\%$). This gap is principled: unlike NMT hallucinations, unfaithful summaries can attend correctly to source tokens while misrepresenting their content, a failure mode invisible to concentration-based OT metrics by construction. Structural experiments on T5-base confirm consistent decoder organisation across depth, with Layer~3 showing peak concentration and Layer~12 being most critical for generation quality. Together, the results establish OT on cross-attention as a reliable detector when the failure mode is source disengagement, a principled interpretability tool regardless of task, and fundamentally limited when faithfulness failures occur downstream of attention.

[2] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.

[3] Connecting Speech to Words through Images
How can we learn the mapping between written words and their spoken counterparts in the absence of explicit textual supervision? We present a visually grounded method for building a vocabulary of spoken words using only images and their spoken descriptions. First, image captioning systems are used to build a vocabulary of written words representing salient visual concepts in the images. For each word, we then find utterances whose image captions contain that word. Then we use an unsupervised word discovery technique to align these utterances to locate instances of the target word. The result is spoken word segments that are linked to written words -- all accomplished without any text supervision. In spoken word retrieval and keyword spotting experiments, the proposed approach outperforms a strong neural baseline while being more interpretable. These results demonstrate the feasibility of the approach in English and motivate future work on low-resource languages without transcripts.
```

---

## GHR0017 — gh_96_cited_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 29
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World'?

### Claim

The paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World' reports the following main experimental results and comparisons:

### Evidence

```text
[1] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3.2% for Claude Code (Sonnet 4.6) over no-evolution baselines, with a -9.5% cost reduction compared to the uniform-sampled baseline. These properties make VisualClaw a natural fit for edge applications, where the cascade reduces a 1-hour streaming session from ~3,600 API uploads down to only 5-20 calls and the self-evolution makes it a perfect personalized assistant.
```

---

## GHR0132 — gh_100_cited_answer_5

**FINAL_LABEL:** `UNSUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 30
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems'?

### Claim

Across 12,779 filtered samples, DICE yields lower Evidence Dilution Index (EDI) than the single-vector baseline in 92.8% of cases, indicating that DICE preserves the strongest chunk-level evidence within the same gold document more effectively.

### Evidence

```text
[1] Multi-Bitwidth Quantization for LLMs Using Additive Codebooks
As large language models (LLMs) are increasingly deployed across heterogeneous hardware with varying resource constraints, the ability to adaptively manage the trade-off between performance and efficiency without retraining is critical. We propose Drop-by-Drop, a novel multi-bitwidth post-training quantization framework that enables inference-time precision control over LLM weights from a single trained model. Our method is theoretically grounded in information theory and successive refinement. We establish that LLM weights, which commonly follow a Gaussian distribution, can be optimally reconstructed with increasing fidelity as additional bits are incorporated, under a weighted mean squared error distortion motivated by LLM loss functions. To realize this in practice, Drop-by-Drop incorporates Matryoshka-style supervision into the loss function, exploiting the structure of additive codebooks. Drop-by-Drop produces a single model where ordered subsets of codebooks yield accurate partial reconstructions at each precision level. This approach significantly reduces storage and memory overhead by allowing a single checkpoint to serve multiple bitwidths, while maintaining competitive perplexity and accuracy across major architectures, such as Qwen, LLaMA, Gemma, and Mistral.

[2] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.
```

---

## GHR0143 — gh_144_plain_answer_1

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 31
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval'?

### Claim

The paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval' is not among the sources provided.

### Evidence

```text
[1] Non-negative Elastic Net Decoding for Information Retrieval
Dense retrieval has become the dominant paradigm in information retrieval, in which each document is scored against a query by the inner product of their vector embeddings, and the top-$k$ documents by score are retrieved for this query. However, since each document's score depends solely on the embedding of the query and itself, the retrieval process is oblivious to the content of the entire corpus. Therefore, dense retrieval cannot avoid selecting semantically similar documents from the corpus, which may result in a non-diverse, redundant set of retrieved documents. To this end, we approach retrieval as a joint decoding problem, in which documents are selected as a set with regard to the context of the rest of the corpus. To achieve this, we propose Non-Negative elastic Net (NNN) decoding, which selects documents whose embeddings jointly reconstruct the query embedding as a sparse non-negative linear combination. Our main theoretical result establishes a strict separation between dense retrieval and NNN decoding. For any corpus, every query correctly handled by dense retrieval is also handled by NNN decoding, while on corpora containing correlated documents, NNN decoding additionally handles queries that dense retrieval cannot. Experimental results indicate that applying NNN decoding to frozen embeddings trained for inner-product scoring yields consistent improvements across several benchmarks. Moreover, we introduce an end-to-end training procedure which optimizes the embeddings for NNN decoding, producing significant performance gains surpassing in all metrics and benchmarks compared to dense retrieval. Our work establishes a new paradigm for leveraging dense embeddings in information retrieval, beyond the standard practice of inner-product scoring.

[2] Operadic consistency: a label-free signal for compositional reasoning failures in LLMs
Detecting LLM reasoning failures at inference time without ground-truth labels has motivated a wide range of confidence baselines, including self-consistency, semantic entropy, and P(True), built on within-question sampling and self-evaluation. Operad theory, the formalism for systems built by iterated substitution, suggests a complementary diagnostic: a model's direct answer to a compositional query should agree with the answer it produces by composing a stated decomposition of the same query. We instantiate this idea as operadic consistency (OC), a per-question signal. Across twelve instruction-tuned LLMs (4B to 671B parameters, open-weights and closed-source) on four multi-hop QA datasets, OC is strongly correlated with accuracy on every dataset (Pearson $r \in [0.86, 0.94]$, all $p \leq 0.0004$), and is the only signal we evaluate with $r \geq 0.85$ uniformly across all four datasets. Chain-of-thought self-consistency (CoT-SC; Wang et al., 2023) matches OC on HotpotQA and DROP ($r = 0.93, 0.87$) but drops to $r \approx 0.45$ on MuSiQue and StrategyQA. At the per-question level, OC contributes information beyond CoT-SC and semantic entropy on every dataset (cluster-robust $p \leq 10^{-16}$ for the OC coefficient), and the conclusion is robust to additionally controlling for constructed decomposition-aware baselines ($p \leq 10^{-13}$). The same signal yields selective-prediction improvements (accuracy at fixed coverage) over a tuned CoT-SC baseline at the equal-cost $K = 3$ budget (AUARC lifts of +0.086 to +0.096 and AUROC lifts of +0.092 to +0.164; 95% CIs exclude zero on every cell). On five frontier thinking models, where the decomposition is extracted from the model's own chain of thought, the same equal-cost comparison gives positive selective-prediction point-estimate lift on all 16 (dataset, budget, metric) cells tested, with 95% CIs excluding zero on 12 of the 16.
```

---

## GHR0114 — gh_48_plain_answer_5

**FINAL_LABEL:** `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 32
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Understanding the Behaviors of Environment-aware Information Retrieval'?

### Claim

The paper shows that performance can be enhanced by incorporating retriever-specific human guidance and by scaling model size.

### Evidence

```text
[1] Understanding the Behaviors of Environment-aware Information Retrieval
Recent retrieval-augmented generation (RAG) approaches have demonstrated strong capability in handling complex queries, yet current research overlooks a critical challenge: different retrievers require fundamentally different query formulation strategies for optimal performance. In this work, we present the first systematic analysis of how LLMs can learn to adapt their query formulation strategies for different retrievers via reinforcement learning (RL). Our empirical study reveals that RL effectively teaches an LLM to tailor its queries to specific retriever characteristics. We discover that different retrievers exhibit surprisingly distinct optimal query styles (e.g., descriptive vs. question-like), suggesting strategies learned for one retriever ineffective for another. We further show that performance can be enhanced by incorporating retriever-specific human guidance and by scaling model size. To facilitate learning over multi-retrieval-step trajectories, we introduce a branching-based rollout technique that improves training stability. Our work provides the first empirical evidence and actionable insights for building truly retriever-aware RAG systems. Code and resources are available at https://github.com/LCO-Embedding/Envs-aware-Information-Retrieval.

[2] When Does Mixing Help? Analyzing Query Embedding Interpolation in Multilingual Dense Retrieval
While mixed-language querying is ubiquitous in multilingual communities, the sensitivity of dense retrievers to such queries remains poorly understood. We present a ratio-controlled study on mMARCO that systematically evaluates retrieval performance by varying the mixing proportion of parallel query translations via embedding-level mixing -- constructing mixed queries as an interpolation of monolingual embeddings. Experiments with BGE-M3 demonstrate that an optimal mixing ratio outperforms the best monolingual endpoint in 88/105 cases. We uncover a distinct asymmetry driven by English dominance: mixing is uniformly beneficial when retrieving from non-English document indices, whereas indices containing English are best served by pure English queries. Furthermore, English acts as the strongest mixing partner for every non-English document language. Finally, when controlling for English dominance, mixing gains correlate negatively with typological distance. We conclude that language-mix sensitivity is structured and predictable, and we validate the robustness of these patterns across model families and scales.

[3] RL-Index: Reinforcement Learning for Retrieval Index Reasoning
Retrieving external knowledge is essential for solving real-world tasks, yet it remains challenging when the relationship between a query and its relevant knowledge involves implicit and complex reasoning beyond surface-level semantic or lexical matching (e.g., mathematical problems relying on the same theorem or coding requiring deep reasoning). Existing approaches primarily rely on query-side reasoning (e.g., query rewriting), which introduces significant online latency and underutilizes the opportunity to perform reasoning over the knowledge corpus itself (i.e., index-side reasoning). In this paper, we propose RL-Index, an agentic indexing framework that formulates retrieval index reasoning as a reinforcement learning problem. Instead of performing reasoning at query time, RL-Index shifts reasoning to the indexing stage by augmenting documents with LLM-generated rationales that explicitly encode the latent query-knowledge relationship. To optimize the quality of these rationales, we employ Group Relative Policy Optimization (GRPO) and use retrieval similarity as a verifiable reward signal, enabling direct optimization of indexing decisions for retrieval effectiveness. Extensive experiments on the BRIGHT benchmark demonstrate that RL-Index consistently improves both retrieval and downstream question-answering performance, while significantly reducing online inference latency. Moreover, the learned rationale augmentation generalizes across diverse retrievers and generators, highlighting its robustness as a plug-and-play indexing strategy across different retrieval systems.
```

---

## GHR0142 — gh_120_plain_answer_2

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 33
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems'?

### Claim

I cannot answer the question about the datasets, benchmarks, or evaluation settings described in that paper.

### Evidence

```text
[1] SCAR: Semantic Continuity-Aware Retrieval for Efficient Context Expansion in RAG
Fixed-length chunking in Retrieval-Augmented Generation (RAG) often leads to boundary fragmentation, where critical evidence is split across segments, degrading retrieval recall. While static windowing and parent retrieval improve recall, they introduce significant token overhead. We propose SCAR (Semantic Continuity-Aware Retrieval), an adaptive retrieval policy that selectively expands neighboring chunks by weighing query-neighbor relevance against a structural continuity penalty. SCAR uses a relative expansion threshold tied to each retrieved chunk's own query-relevance, yielding an approximately scale-invariant decision rule that transfers across embedding models without recalibration. Across four diverse corpora (RFC, GDPR, a 10-K report, and a Merger agreement; N=320 queries; 160 boundary-fragmented), SCAR achieves 92.8% recall on boundary-fragmented queries with only 7.84 chunks, a 22.9% reduction compared to static windowing (10.16 chunks). Paired bootstrap tests (B=10,000) confirm the chunk reduction is highly significant (p<0.0001, Cohen's d=-1.49, large effect), with a small recall difference (Cohen's d=-0.33). The policy transfers across three embedding models (text-embedding-3-large, BGE-large-en-v1.5, zembed-1) using the same single hyperparameter setting, and downstream RAGAS evaluation on the 10-K corpus confirms SCAR preserves generation faithfulness while reducing context tokens by 27.1%.

[2] Charge as a Construct-Validity Factor in Chinese Legal Case Retrieval: A Cross-Benchmark Audit
Chinese Legal Case Retrieval (LCR) benchmarks grade a reference judgment relevant when its legal characterization matches the query, and strong systems now reach NDCG@10 of 0.85-0.88. Most of the BM25-to-best-trained gap is recoverable with no retrieval model: ranking candidates only by shared primary charge, broken by BM25, closes 99.2% of it on LeCaRDv2 -- with no detectable difference from the best-trained system. This reflects benchmark design: LeCaRDv2 defines top relevance via the crime's key constitutive elements, which encode the charge, so same-charge cases are relevant by construction (relevance lift 4.49; charge-to-relevance macro-AUC 0.871). Holding charge fixed, the trained reranker's advantage over BM25 collapses to a small within-charge residual (+0.026 NDCG@10, cluster-bootstrap CI excluding zero, about a quarter), the only non-definitional positive. The effect is not uniform: the same rule recovers 84.3% on LeCaRDv1 and is out of spec on CAIL2022, with the charge-to-relevance signal weakening in step (macro-AUC 0.871/0.759/0.728); a predicted-charge cascade reproduces 76.6% on LeCaRDv2 but does not transfer. The construct is also cashable at first stage: an exploratory zero-training charge-pool channel lifts LeCaRDv2 recall (R@100 +0.025, wrong-charge controls hurt), reported as a positive control for the confound, not a retrieval method or novelty claim. Charge is thus a high-leverage construct-validity factor at the benchmark level -- not auniform explanation of NDCG@10, and not evidence that any system relies on charge. We package established construct-validity and partial-input checks as a reusable charge-controlled protocol (CCE); on all three benchmarks its triggers come back null or descriptive, behaving as designed. We release the scripts, schema, and protocol so future benchmarks can be screened before their NDCG@10 is read as legal-reasoning ability.
```

---

## GHR0028 — gh_89_cited_answer_1

**FINAL_LABEL:**  `SUPPORTED`

**FINAL_NOTES:** 

### Metadata

- review_order: 34
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation'?

### Claim

The paper 'PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation' describes experiments on six QA (Question Answering) benchmarks .

### Evidence

```text
[1] PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation
Agentic GraphRAG trains language-model agents to iteratively retrieve and reason over graph-structured evidence, enabling more accurate and context-aware decision-making by efficiently navigating complex information networks. However, outcome-only reinforcement learning suffers from \textit{\textbf{answer-path reward aliasing}}, where correct answers may come from shortcuts rather than useful evidence paths. It also exhibits \textit{\textbf{search-update ambiguity}}, as scalar trajectory-level feedback does not indicate which retrieval actions to adjust. To mitigate these shortcomings, we present PathRouter, a path-aware training framework for agentic GraphRAG. PathRouter jointly evaluates each trajectory along answer correctness and evidence-path overlap, yielding four trajectory categories with differentiated GRPO advantage scaling that suppresses shortcut reinforcement while preserving evidence-seeking behavior. For evidence-poor trajectories, a frozen gold-evidence teacher provides token-level KL guidance on reasoning and search-query tokens, excluding answer tokens to avoid direct response imitation. Experiments on six QA benchmarks across three model sizes show that PathRouter consistently improves answer F1 and evidence-path overlap, achieving average F1 gains of 3.1 on 3B and 4.9 on 7B models compared to a strong baseline.
```

---

## GHR0012 — gh_154_plain_answer_2

**FINAL_LABEL:** `ABSTENTION`

**FINAL_NOTES:** 

### Metadata

- review_order: 35
- sampling_stratum: `drop_home_related::plain_answer`
- sampling_weight: `4.333333333333333`
- hard_policy: `drop_home_related`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'NEST: Narrative Event Structures in Time for Long Video Understanding', and what problem is it designed to address?

### Claim

I cannot answer the question based on the information in the sources.

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.

[2] Knowledge Graph Enhanced Memory-Augmented Retrieval for Long Context Modeling
Long-context language modeling requires not only extending context windows but maintaining coherent understanding of entity states and relationships across thousands of tokens -- a challenge that semantic similarity alone cannot address. KGERMAR addresses this by constructing dynamic, context-specific knowledge graphs from input text during inference, enabling domain-adaptive retrieval that leverages both semantic similarity and explicit entity relationships. The framework performs real-time entity and relation extraction to build contextual knowledge graphs, then integrates graph-structural embeddings with textual semantics through a multi-component memory architecture. Three memory banks -- contextual, semantic, and structural -- are maintained with retrieval signals fused via learned weights to capture both surface-level semantics and deeper relational patterns. Evaluated on SlimPajama (84.7K training examples), WikiText-103 (4,358 examples), PG-19 (100 examples), and Proof-pile (46.3K examples), KGERMAR achieves up to 8.5\% lower perplexity and 2--2.5x better memory efficiency than memory-augmented baselines across context lengths from 1K to 32K tokens, with superior in-context learning performance across five NLU tasks. The dynamic knowledge graph construction approach advances memory-augmented language modeling by enabling domain-specific knowledge representation that adapts to input contexts rather than relying on fixed knowledge bases.
```

---

## GHR0067 — gh_5_cited_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 36
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Compact Geometric Representations of Hierarchies'?

### Claim

Complementing these upper bounds, lower bounds are provided showing that dimension $Ω(n)$ is necessary for general DAGs and $Ω(t/\log(n/t))$ is required for graphs of treewidth $t$.

### Evidence

```text
[1] Compact Geometric Representations of Hierarchies
Computing geometric representations of data is a cornerstone of modern machine learning, typically achieved by training dual encoders which map queries and documents into a shared embedding space. Recent work of You et al. [NeurIPS '25] has extended this approach to hierarchical retrieval, where relevance is determined by the ancestor-descendant relationships in a Directed Acyclic Graph (DAG). While previous work has shown that valid embeddings exist when the number of descendants is small, these bounds degrade significantly for deep hierarchies, requiring dimensions as large as the total number of nodes. In this paper, we investigate compact reachability embeddings for more general graph classes and provide theoretical guarantees for representing hierarchies using embeddings whose dimension depends on structural graph parameters. We prove that for any directed tree, there exists a reachability embedding in constant dimension 3, independent of the tree's size or depth. We generalize this result to graphs characterized by treewidth $t$, constructing embeddings of dimension $O(t \log n)$, where $n$ is the number of nodes. Complementing these upper bounds, we provide matching or near-matching lower bounds, showing that dimension $Ω(n)$ is necessary for general DAGs and $Ω(t/\log(n/t))$ is required for graphs of treewidth $t$. We also obtain upper and lower bounds parameterized by the number of cross-edges in the DAG. We additionally show that our embeddings can be constructed on real world datasets, and that they give much smaller dimensions in high recall regimes compared to prior embeddings with theoretical guarantees.

[2] Querit-Reranker: Training Compact Multilingual Rerankers via Efficient Label-Free Distribution Adaptation
Deployable multilingual rerankers must generalize across languages, domains, and target ranking tasks while remaining efficient enough for second-stage reranking. However, adapting them to new target distributions typically requires extensive task-specific relevance annotations, which are costly to obtain. We present Querit-Reranker, a family of multilingual cross-encoder rerankers trained with a data-centric pipeline for label-efficient adaptation. We instantiate it as Querit-Reranker-A0.4B, initialized from an in-house MoE backbone with 0.4B activated parameters, and Querit-Reranker-4B, initialized from Qwen3-Embedding-4B. Our pipeline first learns general relevance modeling from large-scale ranking-oriented data, then adapts to target distributions through synthetic-query mining with teacher scores as continuous soft labels. To consolidate complementary task-adapted strengths, we further merge checkpoints via spherical linear interpolation, obtaining a single deployable model without runtime ensembling overhead. Using Qwen3-Embedding-0.6B as the shared first-stage retriever, Querit-Reranker-A0.4B improves average nDCG@10 from 54.11 to 59.28 on BEIR and from 59.87 to 67.70 on MIRACL. On MTEB Multilingual v2 Reranking, it also substantially outperforms larger embedding-based baselines, while Querit-Reranker-4B further achieves state-of-the-art performance among publicly available models. We release both models on Hugging Face.

[3] Non-negative Elastic Net Decoding for Information Retrieval
Dense retrieval has become the dominant paradigm in information retrieval, in which each document is scored against a query by the inner product of their vector embeddings, and the top-$k$ documents by score are retrieved for this query. However, since each document's score depends solely on the embedding of the query and itself, the retrieval process is oblivious to the content of the entire corpus. Therefore, dense retrieval cannot avoid selecting semantically similar documents from the corpus, which may result in a non-diverse, redundant set of retrieved documents. To this end, we approach retrieval as a joint decoding problem, in which documents are selected as a set with regard to the context of the rest of the corpus. To achieve this, we propose Non-Negative elastic Net (NNN) decoding, which selects documents whose embeddings jointly reconstruct the query embedding as a sparse non-negative linear combination. Our main theoretical result establishes a strict separation between dense retrieval and NNN decoding. For any corpus, every query correctly handled by dense retrieval is also handled by NNN decoding, while on corpora containing correlated documents, NNN decoding additionally handles queries that dense retrieval cannot. Experimental results indicate that applying NNN decoding to frozen embeddings trained for inner-product scoring yields consistent improvements across several benchmarks. Moreover, we introduce an end-to-end training procedure which optimizes the embeddings for NNN decoding, producing significant performance gains surpassing in all metrics and benchmarks compared to dense retrieval. Our work establishes a new paradigm fo

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0019 — gh_52_cited_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 37
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'NEST: Narrative Event Structures in Time for Long Video Understanding'?

### Claim

In contrast, Event Relation Extraction (ERE) is more tractable once events are given, reaching 35.45% F1 zero-shot and 44.42% F1 after fine-tuning.

### Evidence

```text
[1] NEST: Narrative Event Structures in Time for Long Video Understanding
Recent progress in vision-language models has enabled the processing of increasingly long video sequences, but the ability to handle extended token streams does not translate to understanding of narrative structure in long videos. Existing long video benchmarks focus on needle-in-a-haystack retrieval rather than evaluating how low-level actions form events, how events interact across time, and how narratives progress, for example, whether a model can connect an early setback, such as a job loss to a later relationship breakup, despite long gaps, intervening scenes, or flashbacks that reframe what occurred. We introduce NEST (Narrative Event Structures in Time for Long Video Understanding), a dataset of 1005 full-length movies (avg. 98 minutes), each annotated with 102 multimodal narrative events grounded in visual content, dialogue, and audio. NEST captures multimodal narrative events with structured annotations grounded in visual content, dialogue, and audio, and links them through relations that reflect narrative structure, including temporal ordering, hierarchical composition, and long-range dependencies. We introduce baselines for event trigger detection (ETD), event localization (EL), event argument extraction (EAE), and event relation extraction (ERE). The benchmark is highly challenging for grounded event discovery, with ETD below 8%, EL under 6%, and EAE below 11%. In contrast, ERE is more tractable once events are given, reaching 35.45% F1 zero-shot and 44.42% F1 after fine-tuning.
```

---

## GHR0130 — gh_107_cited_answer_1

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 38
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice', and what problem is it designed to address?

### Claim

The paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice' introduces a system for generating personalized reading content using Large Language Models (LLMs) combined with Retrieval-Augmented Generation (RAG) .

### Evidence

```text
[2] Combining Retrieval-Augmented Text Generation with LLMs for Reading Content Recommendations
This work presents the design, implementation, and evaluation of a system for generating personalized reading content using Large Language Models (LLMs) combined with Retrieval-Augmented Generation (RAG). The proposed architecture consists of four modules: Input, RAG, Generation, and Judging and enables users to specify both a question and a target reading content complexity. RAG is employed to retrieve relevant information from the Internet, enriching and grounding the content produced by three modern LLMs: Meta LLaMA 4 Scout, LLaMA 3.1 8B Instant, and Google Gemma2 9B. Reading materials are generated using three prompting strategies (Chain-of-Thought, zero-shot, and few-shot), and the LLM-as-a-Judge module automatically evaluates answer quality and alignment with the desired readability level. Experimental results show that RAG consistently improves system performance across all models and prompting techniques, increasing relevance and particularly groundedness by up to 26-35 percentage points. Overall, the findings demonstrate that the RAG-augmented architecture effectively produces reading content tailored to user queries and desired textual complexity.
```

---

## GHR0064 — gh_53_plain_answer_3

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 39
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese'?

### Claim

Ablations: The paper performs experiments to understand the impact of removing each of the three external oracles.

### Evidence

```text
[1] Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese
Byte-Pair Encoding tokenization is statistically efficient for vocabulary compression, but semantically blind to structured technical entities, fragmenting physical quantities, numbers, units, and symbolic expressions into lexically arbitrary subwords. We present TOTEN, a knowledge-based ontological tokenization framework that replaces statistical derivation with declarative classification grounded in a formal ontology of engineering entities (OEE). We formalize TOTEN as the triple <O, classify, {inst_tau}>: the ontology gathers types, structural principles, composition relations, and preservable invariants; the classification function maps raw text into typed regions; and the instantiator family yields a self-descriptive structured representation. Robustness derives from deterministic coupling with three external oracles: Pint (dimensional), Unicode Character Database (typographic), and RSLP (Portuguese morphology). Intrinsic evaluation covers four properties verifiable by construction -- ontological atomicity, dimensional equivalence, typographic robustness, and numerical reconstruction -- over an internal, physically validated benchmark (EngQuant, N=800) and four Brazilian Portuguese external corpora (N=1771 eligible cases). We also report detection recall, distinguishing coverage from conditional atomicity. Against eight state-of-the-art baselines, TOTEN achieves unit ontological atomicity in all contrasts and numerical reconstruction of 0.775-0.904 on external corpora, vs. 0.627-0.703 for the best baseline (Quantulum3); on EngQuant, 0.780 vs. 0.340. Differences are statistically significant (McNemar with Holm correction). Spearman correlation between internal and external rankings confirms concurrent validity of the control benchmark. Dimensional equivalence shows statistical parity with Pint, the oracle from which the system inherits dimensional authority.
```

---

## GHR0018 — gh_74_cited_answer_6

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 40
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents'?

### Claim

Comparison with baselines: The paper compares CoreMem with existing systems on the LOCOMO and LongMemEval-S benchmarks, demonstrating strong accuracy improvements .

### Evidence

```text
[1] CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents
Personalized dialogue agents require continuous long-term memory to maintain coherent interactions across multiple sessions. However, deploying these capabilities on consumer-grade hardware (e.g., 8 GB VRAM edge devices) introduces severe memory and compute bottlenecks. Existing systems typically rely on isotropic cosine similarity for retrieval and heuristic rules for context compression. These approaches lack a unified theoretical foundation, frequently suffering from the hubness problem in high-dimensional retrieval and syntactic fragmentation during compression. To overcome these limitations, we propose CoreMem, a resource-efficient edge-cloud memory architecture fundamentally unified by information geometry. First, Riemannian retrieval replaces cosine matching with a locally adaptive Fisher-Rao metric, effectively penalizing hub memories via Mahalanobis distance with O(Ndr) Woodbury acceleration for real-time search. Second, Fisher-guided discrete token distillation (FDTD) introduces a hierarchical sentence-to-token compression mechanism. It derives sensitivity scores from Fisher information traces, providing a principled compression-KL tradeoff augmented with explicit structural syntax protection. Evaluated on the LOCOMO and LongMemEval-S benchmarks, CoreMem achieves strong accuracy improvements, yielding substantial gains in Open-domain (+4.51 pp) and Temporal (+4.17 pp) reasoning. Extensive profiling confirms that CoreMem operates seamlessly within a strict 8 GB VRAM budget, successfully bridging the gap between resource-constrained edge devices and the demand for theoretically grounded, lifelong memory agents.
```

---

## GHR0039 — gh_52_plain_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 41
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'NEST: Narrative Event Structures in Time for Long Video Understanding'?

### Claim

Event Argument Extraction (EAE): The performance is below 11%.

### Evidence

```text
[1] NEST: Narrative Event Structures in Time for Long Video Understanding
Recent progress in vision-language models has enabled the processing of increasingly long video sequences, but the ability to handle extended token streams does not translate to understanding of narrative structure in long videos. Existing long video benchmarks focus on needle-in-a-haystack retrieval rather than evaluating how low-level actions form events, how events interact across time, and how narratives progress, for example, whether a model can connect an early setback, such as a job loss to a later relationship breakup, despite long gaps, intervening scenes, or flashbacks that reframe what occurred. We introduce NEST (Narrative Event Structures in Time for Long Video Understanding), a dataset of 1005 full-length movies (avg. 98 minutes), each annotated with 102 multimodal narrative events grounded in visual content, dialogue, and audio. NEST captures multimodal narrative events with structured annotations grounded in visual content, dialogue, and audio, and links them through relations that reflect narrative structure, including temporal ordering, hierarchical composition, and long-range dependencies. We introduce baselines for event trigger detection (ETD), event localization (EL), event argument extraction (EAE), and event relation extraction (ERE). The benchmark is highly challenging for grounded event discovery, with ETD below 8%, EL under 6%, and EAE below 11%. In contrast, ERE is more tractable once events are given, reaching 35.45% F1 zero-shot and 44.42% F1 after fine-tuning.
```

---

## GHR0148 — gh_133_plain_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 42
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'ScholarSum: Student-Teacher Abstractive Summarization via Knowledge Graph Reasoning and Reflective Refinement', and what problem is it designed to address?

### Claim

I cannot answer the question based on the information in the sources.

### Evidence

```text
[1] CQC-RAG: Robust Retrieval-Augmented Generation via Cross-Query Consistency
Retrieval-Augmented Generation (RAG) has become a common approach for improving the factuality of Large Language Models (LLMs), yet its reliability remains highly sensitive to how external evidence is retrieved and used. Semantically equivalent queries with different syntactic forms may lead to different retrieval results, while irrelevant or misleading documents can further induce hallucinated answers. Existing multi-path reasoning methods improve robustness by sampling multiple candidate answers and applying voting- or confidence-based selection, but they still face two limitations: diversity is often injected through uncontrollable decoding randomness, and answer evaluation is usually confined to a single query-induced evidence view. To address these limitations, we propose a Cross-Query Consistency Hypothesis: correct answers tend to maintain high confidence across semantically equivalent but syntactically diverse queries, whereas noise-induced hallucinations exhibit unstable confidence under such query variations. Based on this hypothesis, we introduce CQC-RAG, a framework that co-designs query-level diversity injection with cross-query consistency evaluation. CQC-RAG rewrites the original question into diverse but meaning-preserving queries, reranks a shared document pool to construct query-conditioned reasoning contexts, applies an evidence-grounded protocol to extract answer-evidence pairs and selects answers according to their confidence stability across these contexts. This design enables self-evaluation without external supervision and does not rely on expanded retrieval coverage. Experiments on four open-domain question answering benchmarks show that CQC-RAG outperforms the strongest previous multi-query baseline by +4.76 pp EM on TriviaQA and +9.12 pp EM on MuSiQue, validating the effectiveness of cross-query consistency for filtering noise-induced hallucinations.

[2] Zero-source LLM Hallucination Detection with Human-like Criteria Probing
Large language models (LLMs) often hallucinate by generating factually incorrect or unfaithful content, posing significant risks to their safe use. Detecting such hallucinations is particularly challenging under the zero-source constraint, where no model internals or external references are available, and detection must rely solely on the textual query-answer pair. In this paper, we propose Human-like Criteria Probing for Hallucination Detection (HCPD), a paradigm that emulates the multi-faceted reasoning of human evaluators. Its core is a Human-like Criteria Probing (HCP) mechanism, in which a LLM agent adaptively decomposes its judgment into a weighted set of interpretable criteria and aggregates criterion-specific scores into a final truthfulness measure. To achieve this adaptive capability, we introduce a reward-based alignment scheme using only weak supervision from semantic consistency. At inference, we employ a multi-sampling aggregation strategy to ensure robust decisions while preserving full interpretability. We further provide theoretical analysis supporting the reliability of our approach. Extensive experiments show that HCPD consistently outperforms state-of-the-art baselines, offering an effective and explainable solution for zero-source hallucination detection. Code is available at https://github.com/TRISKEL10N/HCPD.
```

---

## GHR0108 — gh_12_plain_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 43
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation'?

### Claim

To objectively evaluate the approach, a challenging subset called ModeVent was introduced, derived from the MultiVent dataset.

### Evidence

```text
[1] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.

[2] REVES: REvision and VErification--Augmented Training for Test-Time Scaling
Test-time scaling via sequential revision has emerged as a powerful paradigm for enhancing Large Language Model (LLM) reasoning. However, standard post-training methods primarily optimize single-shot objectives, creating a fundamental misalignment with multi-step inference dynamics. While recent work treats this as multi-turn reinforcement learning (RL), conventional approaches optimize over the multi-step trajectories directly, failing to further exploit the high-quality mistakes in intermediate steps that model can learn from correcting them. We propose a two-stage iterative framework that alternates between online data/prompt augmentation and policy optimization. By converting the intermediate steps (``near-miss'' answers) in the successful recovery trajectories into decoupled revision and verification prompts, our approach concentrates training on both effective answer transformation and error identification. This approach enables efficient off-policy data generation and reduces the computational overhead of long-horizon sampling compared to standard multi-turn RL. On LiveCodeBench, using publicly available test cases as feedback, we observe gains of +6.5 points over the RL baseline and +4.0 points over standard multi-turn training. Beyond coding, our approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems. Math results under ground-truth verification further confirm improved correction ability. It also generalizes to out-of-distribution constraint-satisfaction puzzles such as n\_queens and mini\_sudoku, where correctness is defined entirely by problem constraints. Code is available at https://github.com/yxliu02/REVES.git.

[3] Personal Care Utility: Health as Everyday Infrastructure
Healthcare is essential, expert, and episodic by design - built around the roughly one hour per year a person spends with a clinician. The 8,759 hours outside clinical settings, where eating, sleeping, movement, medication, and stress actually shape long-term health, have no comparable infrastructure. The bottleneck for personalized health is not raw data or reasoning capability; it is the absence of that infrastructure layer. This paper introduces the Personal Care Utility (PCU): a layered, event-driven architecture proposed as the missing utility for everyday health, in the way that payments, networks, and power are utilities for their domains. PCU organizes continuous personal signals into semantically meaningful life events through a Personicle, estimates dynamic health state against personal baselines, reasons about cause and context, and routes guidance through an orchestrator that separates clinical decision logic, behavioral strategy selection, and natural-language expression. This separation lets large language models support reasoning and communication while keeping safety-critical clinical decisions grounded in validated evidence. We instantiate PCU for Type 2 Diabetes - turning CGM, meal, activity, medication, sleep, stress, and clinical data into glycemic events, individualized state estimates, causal explanations, and knowledge-grounded interventions. A day-in-the-life scenario shows the same infrastructure producing real-time nudges, weekly summaries, medication check-ins, silence, or deterministic safety alerts depending on context and risk. We close with how PCU generalizes to other chronic conditions and the governance questions any always-on personal health utility must address. T

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0036 — gh_53_cited_answer_3

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 44
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese'?

### Claim

Additionally, the paper notes that TOTEN's performance may be impacted by the complexity and ambiguity of the text, as well as the presence of out-of-vocabulary entities.

### Evidence

```text
[1] Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese
Byte-Pair Encoding tokenization is statistically efficient for vocabulary compression, but semantically blind to structured technical entities, fragmenting physical quantities, numbers, units, and symbolic expressions into lexically arbitrary subwords. We present TOTEN, a knowledge-based ontological tokenization framework that replaces statistical derivation with declarative classification grounded in a formal ontology of engineering entities (OEE). We formalize TOTEN as the triple <O, classify, {inst_tau}>: the ontology gathers types, structural principles, composition relations, and preservable invariants; the classification function maps raw text into typed regions; and the instantiator family yields a self-descriptive structured representation. Robustness derives from deterministic coupling with three external oracles: Pint (dimensional), Unicode Character Database (typographic), and RSLP (Portuguese morphology). Intrinsic evaluation covers four properties verifiable by construction -- ontological atomicity, dimensional equivalence, typographic robustness, and numerical reconstruction -- over an internal, physically validated benchmark (EngQuant, N=800) and four Brazilian Portuguese external corpora (N=1771 eligible cases). We also report detection recall, distinguishing coverage from conditional atomicity. Against eight state-of-the-art baselines, TOTEN achieves unit ontological atomicity in all contrasts and numerical reconstruction of 0.775-0.904 on external corpora, vs. 0.627-0.703 for the best baseline (Quantulum3); on EngQuant, 0.780 vs. 0.340. Differences are statistically significant (McNemar with Holm correction). Spearman correlation between internal and external rankings confirms concurrent validity of the control benchmark. Dimensional equivalence shows statistical parity with Pint, the oracle from which the system inherits dimensional authority.
```

---

## GHR0068 — gh_9_cited_answer_6

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 45
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents'?

### Claim

The paper also proposes a unified trajectory construction paradigm for deep research agents and achieves state-of-the-art performance on various benchmarks .

### Evidence

```text
[2] S1-DeepResearch: Beyond Search, Toward Real-World Long-Horizon Research Agents
Deep research agents aim to solve complex knowledge-intensive tasks through long-horizon planning, evidence gathering, reasoning, and report generation. While recent progress in search agents has demonstrated strong capabilities in information retrieval and answer verification, most existing training datasets remain search-centric, focusing primarily on closed-ended question answering and information localization. As a result, they mainly train information-seeking behavior while providing limited coverage of key deep research capabilities, including evidence integration, knowledge synthesis, planning, file understanding, and structured report generation. In this work, we propose a unified trajectory construction paradigm for deep research agents that combines closed-ended QA and open-ended exploration. The proposed framework consists of graph-grounded task formulation, agentic trajectory rollout, and multi-dimensional trajectory verification, enabling scalable synthesis of high-quality agentic trajectories spanning long-chain complex reasoning, deep research instruction following, report writing, file understanding and generation, and skills usage. Compared with existing search-oriented datasets, our synthesized trajectories place greater emphasis on knowledge synthesis, complex reasoning, and planning. S1-DeepResearch-32B achieves state-of-the-art performance among open-source models of comparable scale across 20 benchmarks spanning five capability dimensions, including complex reasoning, instruction following, report generation, file understanding, and skills usage. On several challenging deep research benchmarks, it approaches the performance of leading proprietary frontier models. These results highlight the importance of jointly modeling information acquisition, knowledge synthesis, and planning-oriented agent behaviors for building effective deep research agents.
```

---

## GHR0122 — gh_4_plain_answer_6

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 46
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

The paper does not directly compare its results with the findings from the papers 'Optimal transport (OT) has been shown to detect hallucinations in neural machine translation (NMT)' and 'While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy', as these are separate studies focusing on different models and tasks.

### Evidence

```text
[1] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.

[2] Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization
Optimal transport (OT) has been shown to detect hallucinations in neural machine translation (NMT) by measuring the geometric distance between cross-attention distributions and a reference distribution, without any supervision. We extend this analysis to all six decoder layers of the Fairseq DE-EN model ($N=3{,}414$), showing that Wass-to-Unif and Wass-to-Data are complementary detectors specialised across hallucination types, that detection is concentrated in layers L1--L4 with L5 anti-predictive for subtler types, and that hallucinated translations lack the exploratory attention phase present in correct translations from the first decoding step. We further evaluate whether the geometric signal transfers to abstractive summarization faithfulness detection: our unsupervised OT detector on AggreFact ($N=1{,}116$) achieves $57.2\%$/$57.6\%$ balanced accuracy on CNN/XSum -- above chance but substantially below supervised MiniCheck-Flan-T5-L($69.9\%$/$74.3\%$). This gap is principled: unlike NMT hallucinations, unfaithful summaries can attend correctly to source tokens while misrepresenting their content, a failure mode invisible to concentration-based OT metrics by construction. Structural experiments on T5-base confirm consistent decoder organisation across depth, with Layer~3 showing peak concentration and Layer~12 being most critical for generation quality. Together, the results establish OT on cross-attention as a reliable detector when the failure mode is source disengagement, a principled interpretability tool regardless of task, and fundamentally limited when faithfulness failures occur downstream of attention.

[3] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.
```

---

## GHR0081 — gh_51_cited_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 47
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice', and what problem is it designed to address?

### Claim

HistoRAG aims to translate historiographical principles into concrete architectural interventions, addressing measurable deficiencies in standard RAG, such as era-specific vocabulary retrieval, temporal skew, weak correlation between vector similarity and LLM-assessed relevance, and disjoint source pools .

### Evidence

```text
[1] HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice
Retrieval-Augmented Generation (RAG) is the prevailing architecture for grounding language model outputs in external evidence, yet its dominant evaluation paradigms and default configurations remain oriented toward factual question-answering. For interpretive disciplines such as historical studies, RAG embeds assumptions that conflict with scholarly practice. We introduce HistoRAG, a framework that translates historiographical principles into concrete architectural interventions. Separated retrieval and generation decouples source discovery from interpretation, temporal windowing enforces balanced source representation across the research period as a methodological requirement of historical inquiry, and LLM-as-judge evaluation makes relevance judgments transparent and contestable. We evaluate these interventions using SPIEGELragged, applied to 102,189 articles from Der Spiegel (1950-1979). Each intervention addresses a measurable deficiency in standard RAG: era-specific vocabulary retrieves zero chunks from the 1950s when using 1970s terminology, evidence of the temporal skew that motivates windowing; vector similarity and LLM-assessed relevance correlate only weakly (Spearman rho = 0.275), motivating post-retrieval evaluation; and keyword-based and semantic retrieval surface largely disjoint source pools, motivating an architecture in which both operate as complementary retrieval layers under a shared LLM evaluation filter. We also introduce the concept of Zwischentexte (intermediate texts that function as interpretive proposals rather than findings) as a framework for responsible integration of LLM-generated text into scholarly practice. The architecture offers a model for how domain-specific epistemological commitments can be translated into RAG design decisions, and may transfer to other interpretive disciplines working with large corpora.
```

---

## GHR0033 — gh_54_cited_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 48
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models', and what problem is it designed to address?

### Claim

This method is designed to address the problem of hallucination detection in large language models (LLMs).

### Evidence

```text
[1] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.
```

---

## GHR0043 — gh_56_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 49
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'?

### Claim

These limitations include coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge.

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.
```

---

## GHR0118 — gh_50_plain_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 50
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio'?

### Claim

This suggests that current Language Model (LLM) agents fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance.

### Evidence

```text
[1] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.

[2] LAUKIN: A Multi-jurisdictional Common Law Contract Dataset
Multinational companies increasingly require cross-jurisdictional contract review, yet existing legal NLP datasets are largely restricted to a single jurisdiction. We introduce LAUKIN (Legal equivalence dataset of Australia, UK, and INdia), a dataset of clause pairs (AU-UK, UK-IN, IN-AU) labelled for boolean legal equivalence. We develop a novel multi-stage retrieval and reranking pipeline to construct the initial clause pair mapping, with a subset of clause pairs subsequently annotated by legal experts as Equivalent or Not Equivalent. The dataset comprises 14,727 clause pairs from 204 contracts across 8 agreement types, of which 3,000 are manually labelled: 900 train, 600 dev, and 1,500 test. We evaluate 12 models across 4 techniques, achieving a best macro-F1 of 65.11%, establishing LAUKIN as a challenging benchmark. Results reveal that, despite shared legal heritage, drafting conventions diverge significantly across jurisdictions, making cross-jurisdictional equivalence classification non-trivial. LAUKIN also includes 11,727 unlabelled training pairs to support future semi-supervised learning research in legal NLP.

[3] Query-aware Routing for Filtered Approximate Nearest Neighbors Search
Filtered ANN search, which combines vector similarity with attribute predicates, is a core primitive in modern vector databases and retrieval-augmented generation. We benchmark all major categorical filtered ANN methods across multiple datasets under three predicates and find that no single method dominates. Moreover, even within a single dataset and predicate type, the best method for a query can vary. Therefore, we propose a query-aware routing framework. A lightweight ML model predicts each candidate method's recall on the query, and the router consults an offline benchmark table that maps every method and parameter setting to its measured recall and QPS, then selects the method with the best recall--QPS trade-off. Our ablation study narrows 22 candidate features to a minimal set of three and we adopt regression rather than classification as the prediction target to sharpen accuracy. Our model is trained on six real-world datasets and applied to five unseen validation datasets. The final result shows that our router achieves state-of-the-art recall and QPS balance across all five validation datasets compared to existing filtered ANN baselines, while incurring negligible latency overhead.
```

---

## GHR0040 — gh_91_plain_answer_3

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 51
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'REVES: REvision and VErification--Augmented Training for Test-Time Scaling'?

### Claim

In coding tasks, the approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems.

### Evidence

```text
[1] REVES: REvision and VErification--Augmented Training for Test-Time Scaling
Test-time scaling via sequential revision has emerged as a powerful paradigm for enhancing Large Language Model (LLM) reasoning. However, standard post-training methods primarily optimize single-shot objectives, creating a fundamental misalignment with multi-step inference dynamics. While recent work treats this as multi-turn reinforcement learning (RL), conventional approaches optimize over the multi-step trajectories directly, failing to further exploit the high-quality mistakes in intermediate steps that model can learn from correcting them. We propose a two-stage iterative framework that alternates between online data/prompt augmentation and policy optimization. By converting the intermediate steps (``near-miss'' answers) in the successful recovery trajectories into decoupled revision and verification prompts, our approach concentrates training on both effective answer transformation and error identification. This approach enables efficient off-policy data generation and reduces the computational overhead of long-horizon sampling compared to standard multi-turn RL. On LiveCodeBench, using publicly available test cases as feedback, we observe gains of +6.5 points over the RL baseline and +4.0 points over standard multi-turn training. Beyond coding, our approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems. Math results under ground-truth verification further confirm improved correction ability. It also generalizes to out-of-distribution constraint-satisfaction puzzles such as n\_queens and mini\_sudoku, where correctness is defined entirely by problem constraints. Code is available at https://github.com/yxliu02/REVES.git.
```

---

## GHR0096 — gh_31_plain_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 52
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation', and what problem is it designed to address?

### Claim

The system uses Variational Free Energy (VFE) and internal attention states to dynamically gate interventions, reducing hallucination rates and logical fabrication, and improving the robustness of M-RAG systems.

### Evidence

```text
[1] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.

[2] When Global Gating Is Enough: Admission-Time Hubness Control in Anisotropic Vector Retrieval Systems
Vector hubness, where a few points become nearest neighbors of many queries, creates a poisoning risk in retrieval-augmented generation (RAG): one injected document can influence unrelated requests. Existing defenses use periodic reverse-kNN scans, leaving an exposure window and repeated corpus-wide work. We study admission-time control, scoring each candidate against sentinel queries and quarantining hub-like documents before insertion. Across two 100,000-document corpora, five encoders, and disjoint attacker and defender query sets, a global gate achieves recall 1.0 at the decisive embedding-space point (>=0.92 across the effective range) and 0.91 +/- 0.07 on HotFlip attacks, with 1% false positives on general documents. A per-topic gate provides no reliable benefit, consistent with anisotropy coupling local and global visibility. Thresholds are maintained incrementally, with corpus-size-independent insertion cost and amortized deletion cost. On HNSW, admission adds about 3.1% to ingestion latency, scoring remains flat to 10^6 vectors, and 1.2% of decisions flip under approximate indexing, none involving attacks. Provenance complements the gate for natural or tight-domain hubs.

[3] When Does Streaming Tool Use Help? Characterizing Tool-Intent Stabilization in Streaming Retrieval-Augmented Generation
Streaming Retrieval-Augmented Generation (Streaming RAG) reduces user-perceived latency by issuing tool queries in parallel with ongoing user input, before the utterance is complete. Reported gains are aggregate, yet the mechanism's benefit is fundamentally query-intrinsic: speculation can only help when the correct tool query becomes determinable before the user stops speaking or typing. We isolate and measure this property -- tool-intent stabilization, the point in the input stream at which a speculative query's retrieval converges to the answer-bearing result. On the CRAG benchmark (1371 validation questions) we (i) measure the distribution of stabilization, (ii) derive a model-agnostic bound H on the portion of tool latency that can be hidden behind the user's remaining input, as a function of tool latency L and input cadence δ, (iii) validate against a working streaming pipeline that realized savings meet or exceed this bound, and (iv) identify which query properties predict early versus late stabilization. The study requires no model training and runs on commodity CPU hardware. We find that at a realistic operating point (L=600ms, δ=3w/s, θ=0.8), 73.9% of queries across the full benchmark admit substantial latency hiding -- a blended figure that mixes sufficiency stabilization on the 21.3% of questions where gold evidence is verbatim-present and BM25-retrievable (95.2% streamable on this favorable slice) with a grounding-free top-1-settling fallback on the remainder. On the favorable slice, φ_suf is bracketed to [0.26, 0.281] by exact and relaxed grounding -- both early. Question type produces a significant but coarse early/late split (Kruskal-Wallis p=0.017, epsilon^2=0.04), directly informing when a learned speculative trigger is worth its cost.
```

---

## GHR0077 — gh_11_cited_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 53
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World'?

### Claim

The paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World' discusses several limitations, ablations, and analysis findings.

### Evidence

```text
[1] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3.2% for Claude Code (Sonnet 4.6) over no-evolution baselines, with a -9.5% cost reduction compared to the uniform-sampled baseline. These properties make VisualClaw a natural fit for edge applications, where the cascade reduces a 1-hour streaming session from ~3,600 API uploads down to only 5-20 calls and the self-evolution makes it a perfect personalized assistant.

[2] SAFE-Cascade: Cost-Adaptive Vision-Language Routing for Chart Question Answering
Vision-language models (VLMs) are powerful for chart question answering, but invoking a VLM for every query can be unnecessarily expensive when many questions are answerable from OCR text and lightweight language reasoning. We demonstrate SAFE-Cascade, an interactive system for cost-adaptive chart question answering. Given a chart image and a natural-language question, SAFE-Cascade first extracts chart text with OCR, obtains a provisional answer from a text-only language model, and then uses a learned router to decide whether to accept the text answer or escalate to a VLM. The demo exposes this decision process to users: OCR evidence, text-only answer, routing probability, escalation decision, final answer, estimated cost, and estimated latency are shown side by side. SAFE-Cascade is designed as a transparent interface for understanding when visual grounding is actually needed. Users can upload or select charts, ask questions, inspect the evidence used by each pathway, compare text-only and VLM answers, and adjust the escalation threshold to explore the accuracy-cost frontier. The system is implemented with Azure Document Intelligence for OCR, gpt-5-mini as the text-only model, gemini-2.5-flash-image as the VLM, and a Random Forest router trained on inference-time features. On a held-out ChartQA test split of 375 examples from a 2,500-example experiment, SAFE-Cascade achieves 69.1% unified accuracy with 73.1% VLM invocation, compared with 67.7% accuracy and 100% VLM invocation for the full-VLM baseline. The observed +1.4 percentage-point difference is statistically uncertain, so we interpret SAFE-Cascade as matching full-VLM performance while reducing VLM calls by 26.9% and estimated cost by 9.3%. The demonstration shows how selective modality routing can make multimodal knowledge systems more transparent, tunable, and cost-aware.

[3] AgentFinVQA: A Deployable Multi-Agent Pipeline for Auditable Financial Chart QA
Financial chart question answering in regulated settings demands more than accuracy: practitioners must know which answers to trust before acting on them, and many institutions cannot send client data to external model providers. Yet existing chart-QA agents are accuracy-focused and opaque, and most assume proprietary API access; to our knowledge, none combines auditability with on-premise deployability without significant accuracy compromise. We present AgentFinVQA, a multi-agent pipeline that decomposes each query into planning, OCR, legend grounding, visual inspection, and verification, recording every step in a traceable Model Evaluation Packet (MEP) per sample. On FinMME, AgentFinVQA improves $+7.68$ pp over a primary-backbone matched zero-shot baseline with a proprietary backbone (Gemini-3 Flash; 71.24% vs. 63.56%, McNemar $p \approx 1.1 \times 10^{-16}$), and $+4.84$ pp with open-weights Qwen3.6-27B-FP8 served locally. The verifier's verdict also serves a

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0099 — gh_35_plain_answer_9

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 54
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization'?

### Claim

in the fully unsupervised setting, an RMT-deviation score achieves a weaker mean AUROC of 0.71.

### Evidence

```text
[1] Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization
Optimal transport (OT) has been shown to detect hallucinations in neural machine translation (NMT) by measuring the geometric distance between cross-attention distributions and a reference distribution, without any supervision. We extend this analysis to all six decoder layers of the Fairseq DE-EN model ($N=3{,}414$), showing that Wass-to-Unif and Wass-to-Data are complementary detectors specialised across hallucination types, that detection is concentrated in layers L1--L4 with L5 anti-predictive for subtler types, and that hallucinated translations lack the exploratory attention phase present in correct translations from the first decoding step. We further evaluate whether the geometric signal transfers to abstractive summarization faithfulness detection: our unsupervised OT detector on AggreFact ($N=1{,}116$) achieves $57.2\%$/$57.6\%$ balanced accuracy on CNN/XSum -- above chance but substantially below supervised MiniCheck-Flan-T5-L($69.9\%$/$74.3\%$). This gap is principled: unlike NMT hallucinations, unfaithful summaries can attend correctly to source tokens while misrepresenting their content, a failure mode invisible to concentration-based OT metrics by construction. Structural experiments on T5-base confirm consistent decoder organisation across depth, with Layer~3 showing peak concentration and Layer~12 being most critical for generation quality. Together, the results establish OT on cross-attention as a reliable detector when the failure mode is source disengagement, a principled interpretability tool regardless of task, and fundamentally limited when faithfulness failures occur downstream of attention.

[2] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.

[3] Connecting Speech to Words through Images
How can we learn the mapping between written words and their spoken counterparts in the absence of explicit textual supervision? We present a visually grounded method for building a vocabulary of spoken words using only images and their spoken descriptions. First, image captioning systems are used to build a vocabulary of written words representing salient visual concepts in the images. For each word, we then find utterances whose image captions contain that word. Then we use an unsupervised word discovery technique to align these utterances to locate instances of the target word. The result is spoken word segments that are linked to written words -- all accomplished without any text supervision. In spoken word retrieval and keyword spotting experiments, the proposed approach outperforms a strong neural baseline while being more interpretable. These results demonstrate the feasibility of the approach in English and motivate future work on low-resource languages without transcripts.
```

---

## GHR0051 — gh_59_plain_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 55
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents', and what problem is it designed to address?

### Claim

DeepRubric aims to provide more reliable query--rubric supervision by first determining what an evidence-backed report should be evaluated on and then synthesizing aligned query--rubric pairs from those evaluation targets.

### Evidence

```text
[1] DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents
Deep research agents synthesize long-form reports by searching and reasoning over retrieved evidence. Reinforcement learning with rubric-based rewards improves these agents by optimizing them against checkable criteria that translate report quality into reward signals, but its efficiency depends on whether those criteria reliably capture the task scope and evidence needs. Most existing studies ask an LLM to generate rubrics for a given query, but when the model fails to infer the underlying information needs, the generated rubrics may be incomplete and reduce RL efficiency. To obtain more reliable query--rubric supervision, we introduce DeepRubric, a data construction framework that reverses this process: instead of inferring evaluation criteria for a given query, it first determines what an evidence-backed report should be evaluated on and then synthesizes aligned query--rubric pairs from those evaluation targets. Starting from a sampled seed topic, DeepRubric builds an evidence tree by recursively expanding evidence-backed sub-questions, whose leaves serve as atomic and verifiable evaluation targets. It then uses the evidence tree to synthesize the training query and rubrics, ensuring that the reward evaluates exactly the information requested by the query. Using DeepRubric, we construct 9K query--rubric supervision examples and train DeepRubric-8B with rubric-based GRPO, achieving comparable performance to prior open state-of-the-art deep research models across three benchmarks with roughly 13x fewer RL GPU-hours.
```

---

## GHR0104 — gh_31_plain_answer_1

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 56
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation', and what problem is it designed to address?

### Claim

The paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation' introduces a Multi-Agent system called MODE-RAG.

### Evidence

```text
[1] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.

[2] When Global Gating Is Enough: Admission-Time Hubness Control in Anisotropic Vector Retrieval Systems
Vector hubness, where a few points become nearest neighbors of many queries, creates a poisoning risk in retrieval-augmented generation (RAG): one injected document can influence unrelated requests. Existing defenses use periodic reverse-kNN scans, leaving an exposure window and repeated corpus-wide work. We study admission-time control, scoring each candidate against sentinel queries and quarantining hub-like documents before insertion. Across two 100,000-document corpora, five encoders, and disjoint attacker and defender query sets, a global gate achieves recall 1.0 at the decisive embedding-space point (>=0.92 across the effective range) and 0.91 +/- 0.07 on HotFlip attacks, with 1% false positives on general documents. A per-topic gate provides no reliable benefit, consistent with anisotropy coupling local and global visibility. Thresholds are maintained incrementally, with corpus-size-independent insertion cost and amortized deletion cost. On HNSW, admission adds about 3.1% to ingestion latency, scoring remains flat to 10^6 vectors, and 1.2% of decisions flip under approximate indexing, none involving attacks. Provenance complements the gate for natural or tight-domain hubs.

[3] When Does Streaming Tool Use Help? Characterizing Tool-Intent Stabilization in Streaming Retrieval-Augmented Generation
Streaming Retrieval-Augmented Generation (Streaming RAG) reduces user-perceived latency by issuing tool queries in parallel with ongoing user input, before the utterance is complete. Reported gains are aggregate, yet the mechanism's benefit is fundamentally query-intrinsic: speculation can only help when the correct tool query becomes determinable before the user stops speaking or typing. We isolate and measure this property -- tool-intent stabilization, the point in the input stream at which a speculative query's retrieval converges to the answer-bearing result. On the CRAG benchmark (1371 validation questions) we (i) measure the distribution of stabilization, (ii) derive a model-agnostic bound H on the portion of tool latency that can be hidden behind the user's remaining input, as a function of tool latency L and input cadence δ, (iii) validate against a working streaming pipeline that realized savings meet or exceed this bound, and (iv) identify which query properties predict early versus late stabilization. The study requires no model training and runs on commodity CPU hardware. We find that at a realistic operating point (L=600ms, δ=3w/s, θ=0.8), 73.9% of queries across the full benchmark admit substantial latency hiding -- a blended figure that mixes sufficiency stabilization on the 21.3% of questions where gold evidence is verbatim-present and BM25-retrievable (95.2% streamable on this favorable slice) with a grounding-free top-1-settling fallback on the remainder. On the favorable slice, φ_suf is bracketed to [0.26, 0.281] by exact and relaxed grounding -- both early. Question type produces a significant but coarse early/late split (Kruskal-Wallis p=0.017, epsilon^2=0.04), directly informing when a learned speculative trigger is worth its cost.
```

---

## GHR0107 — gh_3_plain_answer_5

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 57
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science'?

### Claim

utilizing full-text content faces challenges related to excessive length and information redundancy.

### Evidence

```text
[1] Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science
Research methods are essential carriers of knowledge contribution in academic papers. Automatic multi-label classification of research methods can support knowledge services such as method retrieval, review generation, and research intelligence analysis. While existing studies primarily rely on titles and abstracts, abstracts often provide only limited methodological information, whereas utilizing full-text content faces challenges related to excessive length and information redundancy. Therefore, this paper proposes a segment combination strategy by partitioning the full-text content according to its physical postion. Using an annotated corpus of 1,954 full-text articles from three representative journals in Library and Information Science (JASIST, LISR, and JDoc), we evaluate the classification performance of various segments and their combinations across multiple models. Experimental results indicate that methodological information is distributed unevenly within the full-text content, with the middle-to-late and final segments exhibiting greater discriminative power. Furthermore, integrating bibliographic metadata with cross-segment combination strategies effectively enhances classification performance.

[2] Focus When Necessary: Adaptive Routing and Collaborative Grounding for Training-Free Visual Grounding
While Multimodal Large Language Models (MLLMs) excel in cross-modal reasoning, they often struggle to perceive fine-grained details in complex high-resolution images. Recent training-free methods address this through image scaling and localized cropping. However, applying these manipulations indiscriminately introduces computational redundancy for simple queries and can degrade accuracy by truncating essential global context or introducing irrelevant background noise. To this end, we propose LazyMCoT, a dynamic and training-free framework that adaptively allocates visual grounding efforts based on sample difficulty. The framework features an Adaptive Routing mechanism that evaluates predictive uncertainty using first-token statistics from a single forward pass. This efficiently bypasses confident cases while ensuring the recall of difficult samples via conformal calibration. For these challenging cases, a Collaborative Grounding module integrates the inherent cross-modal attention of the model with an external visual expert through a two-stage refinement process. This refinement process generates a precise localized display to recover small or occluded targets. Extensive experiments across diverse benchmarks demonstrate that LazyMCoT rivals training-based approaches by simultaneously improving reasoning accuracy and reducing average inference latency. Our code is availble at https://github.com/TencentBAC/LazyMCoT.

[3] Analyzing and Encoding the Al-Mawrid Arabic-English Dictionary with the ISO Language Markup Framework and TEI Lex-0
This paper presents a robust methodology for the systematic digitization and encoding of the Al-Mawrid Arabic-English dictionary, transforming it from a legacy print resource into a standardized computational lexicon. Addressing a significant gap in Arabic lexical infrastructure, the study adopts a dual-standard framing that aligns the ISO Lexical Markup Framework (LMF) with the Text Encoding Initiative TEI Lex-0 guidelines. By applying an editorial view to the dictionary's macro- and microstructure, the research resolves the structural ambiguities and punctuation inconsistencies typical of 20th-century bilingual dictionaries. The methodology is grounded in an empirical analysis of the dictionary's lexical knowledge density. Drawing on a representative sample (the letter Ayn, comprising 4.6% of the total volume), the study provides scientific weight to the encoding process, demonstrating a structural parsing accuracy of 91%. Quantitative evaluation of the information extraction rules reveals high performance, with 85% precision and 98% recall for synonyms, and 88% precision for other morpho-semantic features. Beyond technical description, the paper provides a critical comparison with existing Arabic lexical resources and discusses the limitations of TEI Lex-0 when modelling specific Arabic phenomena, such as implicit "open set" semantic relations and scattered morphological cues. Furthermore, the study explores the potential for Linguistic Linked Open Data (LLOD) integration by establishing a scalable prefix-based referencing system that facilitates the resource's inclusion in the semantic web. The result is an interoperable, machine-tractable resource that provides a reproducible workflow for the retro-digitization of complex legacy bilingual lexicons within the Arabic NLP and Digital Humanities communities.
```

---

## GHR0141 — gh_112_plain_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 58
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science'?

### Claim

Evidence from Library and Information Science' is not among the sources provided.

### Evidence

```text
[1] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.

[2] LEDGER: A Long-Context Benchmark of Corporate Annual Reports for Grounded Financial Retrieval and Extraction
Finance reporting is a natural proving ground for large language models, and the very-long-context capabilities of recent models across all sizes make rigorous evaluation in this domain an increasingly pressing need. Yet most public financial resources reduce the task to plain-text SEC 10-K filings paired with a handful of question-answer items. We release LEDGER (Long-context Evaluation of Documents for Grounded Extraction and Retrieval), a corpus of 4,999 digitized corporate annual reports - full documents with figures, tables, and narrative, not just regulatory filings. Each report is labeled with 31 consolidated financial KPIs to be extracted and linked to the market's reaction at the earnings date. From this data we derive three evaluation benchmarks spanning the difficulty spectrum: a pure page-level KPI retrieval task with TREC-style relevance judgments over 118,048 questions in natural language, a conversational "needle-in-a-haystack" single-value lookup, and a full KPI extraction task, both from long, numerically dense reports. We additionally provide human OCR-quality annotations with inter-annotator agreement and the complete extraction, validation, and scoring toolchain. We further demonstrate the dataset's research utility with a case study linking CEO-letter rhetoric to post-publication market impact.
```

---

## GHR0086 — gh_22_cited_answer_8

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 59
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World'?

### Claim

For high-resource languages, the results on 8B-sized open-source models match those of closed-source models such as Deepseek2.5 and GPT-4o-mini.

### Evidence

```text
[1] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3.2% for Claude Code (Sonnet 4.6) over no-evolution baselines, with a -9.5% cost reduction compared to the uniform-sampled baseline. These properties make VisualClaw a natural fit for edge applications, where the cascade reduces a 1-hour streaming session from ~3,600 API uploads down to only 5-20 calls and the self-evolution makes it a perfect personalized assistant.

[2] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.

[3] Encode Errors: Representational Retrieval of In-Context Demonstrations for Multilingual Grammatical Error Correction
Grammatical Error Correction (GEC) involves detecting and correcting the wrong usage of grammar. While large language models (LLMs) with in-context learning (ICL) capabilities have shown significant progress on various natural language processing (NLP) tasks, their few-shot performance on GEC remains suboptimal. This is mainly due to the challenge of retrieving suitable in-context demonstrations that capture error patterns instead of semantic similarity. In this paper, we demonstrate that LLMs can inherently capture information related to grammatical errors through their internal states. From these states, we extract the Grammatical Error Representation (GER), an informative and semantically neutral encoding of grammatical errors. Our novel GER-based retrieval method significantly boosts performance in ICL settings on multilingual GEC datasets, improving the precision of correction. For high-resource languages, our results on 8B-sized open-source models match those of closed-source models such as Dee

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0100 — gh_13_plain_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 60
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'?

### Claim

The performance improvement of SAMA is underscored as a demonstration of its versatility, robustness, and effectiveness.

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.

[2] Stellar: Scalable Multimodal Document Retrieval for Natural Language Queries
Multimodal document retrieval--selecting the most relevant multimodal document from a large corpus to answer a natural language query--plays an essential role in Retrieval-Augmented Generation (RAG) systems. State-of-the-art methods represent each document and query with multiple token-level embeddings and use late interaction to achieve high effectiveness. However, such multi-vector representations incur substantial memory overhead during retrieval, leading to poor scalability and hindering real-world deployment. In this paper, we present Stellar, a scalable multimodal document retrieval framework that stores token-level document embeddings on disk and loads only a small set of candidate embeddings into memory for late interaction. Stellar comprises two key components: (i) Lexical Representation-based Filtering (LRF), which fine-tunes a Multimodal Large Language Model (MLLM) as a sparse encoder to produce high-quality lexical representations, enabling efficient and effective document filtering to significantly reduce the candidate set; (ii) Efficient Disk-backed Late Interaction (DLI), which designs an on-disk token embedding storage layout guided by a balanced clustering algorithm, and dynamically loads only the necessary token embeddings into memory using a simple yet effective cost model. Extensive experiments on four real-world benchmarks and a newly presented large-scale dataset demonstrate that Stellar reduces memory overhead and query latency by 1-2 orders of magnitude compared to existing methods without compromising retrieval effectiveness.

[3] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0095 — gh_49_plain_answer_4

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 61
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation'?

### Claim

For Dream and Passkey, the performance improves from 30.0 to 90.0 and 23.3 to 74.0, respectively.

### Evidence

```text
[1] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.

[2] Context Compression Is Not One Thing: Readable Symbolic Re-expression vs. Coherent Summary at Matched Budget
We study context compression for multi-hop question answering with small language models. We propose Telegraph English, a readable symbolic format that rewrites retrieved passages into structured entity-relation statements, preserving reasoning evidence at lower token cost. In controlled experiments on MuSiQue, TwoWiki, and HotpotQA, Telegraph English outperforms three matched-budget compression baselines (character-level deletion, truncation, and random sub-sampling) on every dataset, with gains of 13 to 20 F1 percentage point. It also outperforms a coherent prose summary produced by the same encoder on the hardest dataset. A pre-registered depth-interaction hypothesis is null: the advantage does not grow with reasoning depth within datasets. We interpret these results as evidence that readable symbolic re-expression preserves entity content more densely than either natural language or coherent summarization at matched token budget.

[3] Adaptive Multi-Resolution Procedural Knowledge Compression for Large Language Models
Large language models (LLMs) are widely used to tackle complex tasks with autonomous workflows. Recently, reusable natural language skills have emerged as a popular paradigm to inject procedural knowledge into LLM applications. Since popular skills are often invoked repeatedly, placing their full text in every context significantly increases prefill cost and latency. While text compression techniques have the potential to solve this problem, most existing methods are designed to compress factual knowledge in documents instead of procedural knowledge, making them insufficient for skill compression. In this paper, we argue that an effective skill compression method should: 1) preserve logical dependencies among workflows and tool protocols, 2) enable lightweight, offline compression for frequently updated community skills, and 3) be adaptable to varying complexities across skills. To address this, we present SKIM (SKIll coMpression), an adaptive multi-resolution soft token compression framework for procedural skills. Depending on the complexity of each skill, SKIM creates different numbers of soft tokens that not only improve the efficiency of LLM inference, but also preserve the effectiveness of skill usage. Experiments indicate that SKIM compresses skills to 30 to 60 percent of their original token length while preserving task performance better than existing compression methods.We have released our code at https://github.com/bebr2/SKIM .
```

---

## GHR0070 — gh_13_cited_answer_4

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 62
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'?

### Claim

The paper does not provide direct comparisons with other methods for multimodal document retrieval, as it focuses on the generation of synthetic data for multimodal information extraction .

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.
```

---

## GHR0074 — gh_48_cited_answer_6

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 63
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Understanding the Behaviors of Environment-aware Information Retrieval'?

### Claim

To facilitate learning over multi-retrieval-step trajectories, a branching-based rollout technique is introduced to improve training stability.

### Evidence

```text
[1] Understanding the Behaviors of Environment-aware Information Retrieval
Recent retrieval-augmented generation (RAG) approaches have demonstrated strong capability in handling complex queries, yet current research overlooks a critical challenge: different retrievers require fundamentally different query formulation strategies for optimal performance. In this work, we present the first systematic analysis of how LLMs can learn to adapt their query formulation strategies for different retrievers via reinforcement learning (RL). Our empirical study reveals that RL effectively teaches an LLM to tailor its queries to specific retriever characteristics. We discover that different retrievers exhibit surprisingly distinct optimal query styles (e.g., descriptive vs. question-like), suggesting strategies learned for one retriever ineffective for another. We further show that performance can be enhanced by incorporating retriever-specific human guidance and by scaling model size. To facilitate learning over multi-retrieval-step trajectories, we introduce a branching-based rollout technique that improves training stability. Our work provides the first empirical evidence and actionable insights for building truly retriever-aware RAG systems. Code and resources are available at https://github.com/LCO-Embedding/Envs-aware-Information-Retrieval.
```

---

## GHR0032 — gh_62_cited_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 64
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents'?

### Claim

The authors introduce DeepRubric, a data construction framework that synthesizes aligned query--rubric pairs from evidence-backed evaluation targets, aiming to obtain more reliable query--rubric supervision for deep research agents.

### Evidence

```text
[1] DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents
Deep research agents synthesize long-form reports by searching and reasoning over retrieved evidence. Reinforcement learning with rubric-based rewards improves these agents by optimizing them against checkable criteria that translate report quality into reward signals, but its efficiency depends on whether those criteria reliably capture the task scope and evidence needs. Most existing studies ask an LLM to generate rubrics for a given query, but when the model fails to infer the underlying information needs, the generated rubrics may be incomplete and reduce RL efficiency. To obtain more reliable query--rubric supervision, we introduce DeepRubric, a data construction framework that reverses this process: instead of inferring evaluation criteria for a given query, it first determines what an evidence-backed report should be evaluated on and then synthesizes aligned query--rubric pairs from those evaluation targets. Starting from a sampled seed topic, DeepRubric builds an evidence tree by recursively expanding evidence-backed sub-questions, whose leaves serve as atomic and verifiable evaluation targets. It then uses the evidence tree to synthesize the training query and rubrics, ensuring that the reward evaluates exactly the information requested by the query. Using DeepRubric, we construct 9K query--rubric supervision examples and train DeepRubric-8B with rubric-based GRPO, achieving comparable performance to prior open state-of-the-art deep research models across three benchmarks with roughly 13x fewer RL GPU-hours.
```

---

## GHR0002 — gh_148_cited_answer_4

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 65
- sampling_stratum: `drop_home_related::cited_answer`
- sampling_weight: `4.166666666666667`
- hard_policy: `drop_home_related`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

The paper discusses limitations of test-time scaling for agentic search, focusing on breadth scaling, and presents DivInit, a training-free intervention at the first turn to address the limitation of query redundancy at the first turn.

### Evidence

```text
[2] Beyond Parallel Sampling: Diverse Query Initialization for Agentic Search
Test-time scaling for agentic search typically increases depth (i.e., more turns and tokens per trajectory) or breadth (i.e., more parallel rollouts). Here we focus on breadth scaling, showing that standard parallel sampling yields diminishing returns, tracing this to query redundancy at the first turn. When models issue similar first queries across rollouts, the threads retrieve overlapping evidence, and subsequent turns are conditioned on this shared retrieval. We address this limitation with DivInit, a training-free intervention at the first turn. Rather than sampling k independent first queries, DivInit draws n candidates from a single call, picks k < n diverse seeds, and runs them as parallel trajectories. Across five open-weight models and eight benchmarks, DivInit consistently improves over standard parallel sampling, with average gains of five to seven points on multi-hop QA at matched compute. Code available at https://github.com/cxcscmu/diverse-query-initialization
```

---

## GHR0003 — gh_160_cited_answer_1

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 66
- sampling_stratum: `drop_home_related::cited_answer`
- sampling_weight: `4.166666666666667`
- hard_policy: `drop_home_related`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'?

### Claim

I'm sorry for any confusion, but the sources provided do not discuss the paper titled 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'.

### Evidence

```text
[1] Stellar: Scalable Multimodal Document Retrieval for Natural Language Queries
Multimodal document retrieval--selecting the most relevant multimodal document from a large corpus to answer a natural language query--plays an essential role in Retrieval-Augmented Generation (RAG) systems. State-of-the-art methods represent each document and query with multiple token-level embeddings and use late interaction to achieve high effectiveness. However, such multi-vector representations incur substantial memory overhead during retrieval, leading to poor scalability and hindering real-world deployment. In this paper, we present Stellar, a scalable multimodal document retrieval framework that stores token-level document embeddings on disk and loads only a small set of candidate embeddings into memory for late interaction. Stellar comprises two key components: (i) Lexical Representation-based Filtering (LRF), which fine-tunes a Multimodal Large Language Model (MLLM) as a sparse encoder to produce high-quality lexical representations, enabling efficient and effective document filtering to significantly reduce the candidate set; (ii) Efficient Disk-backed Late Interaction (DLI), which designs an on-disk token embedding storage layout guided by a balanced clustering algorithm, and dynamically loads only the necessary token embeddings into memory using a simple yet effective cost model. Extensive experiments on four real-world benchmarks and a newly presented large-scale dataset demonstrate that Stellar reduces memory overhead and query latency by 1-2 orders of magnitude compared to existing methods without compromising retrieval effectiveness.

[2] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3.2% for Claude Code (Sonnet 4.6) over no-evolution baselines, with a -9.5% cost reduction compared to the uniform-sampled baseline. These properties make VisualClaw a natural fit for edge applications, where the cascade reduces a 1-hour streaming session from ~3,600 API uploads down to only 5-20 calls and the self-evolution makes it a perfect personalized assistant.
```

---

## GHR0150 — gh_111_plain_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 67
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents'?

### Claim

I cannot answer the question about the experimental results or comparisons reported in that specific paper.

### Evidence

```text
[1] S1-DeepResearch: Beyond Search, Toward Real-World Long-Horizon Research Agents
Deep research agents aim to solve complex knowledge-intensive tasks through long-horizon planning, evidence gathering, reasoning, and report generation. While recent progress in search agents has demonstrated strong capabilities in information retrieval and answer verification, most existing training datasets remain search-centric, focusing primarily on closed-ended question answering and information localization. As a result, they mainly train information-seeking behavior while providing limited coverage of key deep research capabilities, including evidence integration, knowledge synthesis, planning, file understanding, and structured report generation. In this work, we propose a unified trajectory construction paradigm for deep research agents that combines closed-ended QA and open-ended exploration. The proposed framework consists of graph-grounded task formulation, agentic trajectory rollout, and multi-dimensional trajectory verification, enabling scalable synthesis of high-quality agentic trajectories spanning long-chain complex reasoning, deep research instruction following, report writing, file understanding and generation, and skills usage. Compared with existing search-oriented datasets, our synthesized trajectories place greater emphasis on knowledge synthesis, complex reasoning, and planning. S1-DeepResearch-32B achieves state-of-the-art performance among open-source models of comparable scale across 20 benchmarks spanning five capability dimensions, including complex reasoning, instruction following, report generation, file understanding, and skills usage. On several challenging deep research benchmarks, it approaches the performance of leading proprietary frontier models. These results highlight the importance of jointly modeling information acquisition, knowledge synthesis, and planning-oriented agent behaviors for building effective deep research agents.

[2] Long-Context Modeling via GSS-Transformer Hybrid Architecture with Learnable Mixing
Modeling long-range dependencies remains a central challenge in natural language processing. Transformer architectures achieve strong performance via self-attention but scale quadratically ($O(N^2)$) with sequence length, while State Space Models (SSMs) scale linearly ($O(N)$) but suffer from a selective recall bottleneck, struggling to retrieve precise information from compressed states. This creates a fundamental tradeoff between efficiency and perplexity. To tackle these challenges, we propose the \textit{Parallel Hybrid Architecture (PHA)}, which runs Gated State Spaces (GSS), Grouped Query Attention (GQA), and Feed-Forward Networks (FFNs) as independent parallel branches fused by a learnable mixing mechanism. Instead of forcing SSMs to approximate attention or serializing the two paradigms, PHA allows each branch to specialize: GSS captures global context, while attention performs selective retrieval, with FFN providing complementary processing. On WikiText-103, PHA achieves 16.51 PPL at 125M parameters, outperforming Hedgehog (16.70) and H3-125M (23.70). Scaling to 180M parameters yields 16.42 PPL, which gives comparable results with the pure attention baseline while delivering 24\% higher throughput and up to 40\% lower memory usage at long contexts. On OpenWebText, our 125M model achieves 19.72 PPL, outperforming standard Transformers (20.60) and GSS hybrid baselines (19.80). These results demonstrate that separating sequence modeling paradigms into parallel specialists enables Transformer-level perplexity with substantially improved efficiency for long-context language modeling.
```

---

## GHR0126 — gh_131_cited_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 68
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World', and what problem is it designed to address?

### Claim

I cannot answer the question using only the given sources.

### Evidence

```text
[1] ComAct: Reframing Professional Software Manipulation via COM-as-Action Paradigm
Existing computer-use agents remain fundamentally limited in professional software manipulation: GUI-based agents suffer from fragile visual grounding and long-horizon error accumulation, while API-basedapproaches struggle with heterogeneous protocols and inaccessible commercial interfaces. In this work,we identify the Component Object Model (COM) as a unified executable abstraction, proposing COM-as-Action: a new paradigm that reframes professional software interaction as deterministic program synthesisrather than sequential visual control. To validate this paradigm in the most demanding environments, weintroduce ComCADBench, the first benchmark for agents operating real industrial CAD software. Ourexperiments reveal a substantial paradigm gap: frontier proprietary models achieve near-zero successunder GUI-based interaction, whereas COM-based execution yields substantial immediate gains. Tobridge the remaining gap between syntactic correctness and geometric accuracy, we develop ComActor, aself-correcting agent trained through a progressive three-stage framework, alongside ComForge, a scalableplatform for large-scale training in Windows containers. Extensive experiments show that ComActorachieves state-of-the-art performance on ComCADBench, with strong resilience in long-horizon taskswhere baselines collapse, and generalizes to external CAD benchmark.

[2] PACMS: Submodular Context Selection as a Pluggable Engine for LLM Agents
Conversational and tool-using LLM agents operate over a context window that fills from several directions simultaneously. As a session proceeds, the agent accumulates user and assistant turns, entries drawn from a persistent memory store, and often largest of all, the verbatim outputs of tool calls such as file reads, search results, and API responses. Once the cumulative context exceeds the model's token budget, the framework must decide what to keep. The prevailing mechanism is recency truncation, sometimes paired with periodic summarization. This is topic-blind: a fact established early in a session is discarded simply because it is old, even when the current user query is about exactly that fact; conversely, verbose but irrelevant recent material is retained. Agents that must recall information across many turns, the defining case for memory, are precisely where recency truncation fails. Existing alternatives sit outside the agent's assembly step. Retrieval augmented generation fetches external documents into the prompt but does not arbitrate the agent's \emph{already-present} pooled context. Context-compression methods reduce token count by rewriting or pruning text, but operate query-blind and lossily. Neither treats memory entries, conversation turns, and tool outputs as a single candidate pool to be selected from by relevance at the moment the prompt is assembled.
```

---

## GHR0016 — gh_84_cited_answer_10

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 69
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems'?

### Claim

MonaVec targets on-device RAG, offline agents, and embedded retrieval, similar to the niche SQL

### Evidence

```text
[1] MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems
We present MonaVec, a deterministic, embedded vector-search kernel for edge and offline AI -- settings where server infrastructure, network connectivity, and training data are all unavailable. Existing vector-search systems assume a persistent server, gigabytes of RAM, or a training pass over the corpus; MonaVec instead targets the deployment profile of SQLite: one file, one function call, runs anywhere. Its quantization core is training-free by default and data-oblivious: a Randomized Hadamard Transform (RHDH) conditions any input distribution toward N(0,1), so precomputed Lloyd-Max tables quantize to 4 bits (8x smaller) with no learned codebook and no data pass. The index persists as a single .mvec file whose embedded ChaCha20 rotation seed makes results reproducible across architectures and byte-identical within a build -- a determinism guarantee that parallel-build graph libraries cannot offer. On semantic embeddings (AG News, 45K x 1024-dim BGE-M3, cosine), MonaVec 4-bit BruteForce reaches 0.960 Recall@10 in 27 MB -- leading float32 FAISS-IVF and 8-bit usearch on recall -- while trading peak throughput for byte-identical determinism. A single-pass global standardization (fit()) extends the same data-oblivious pipeline to magnitude-sensitive L2 data, and optional IvfFlat and HNSW backends carry it to million-vector corpora. MonaVec is implemented in pure Rust with Python bindings and runtime SIMD dispatch (AVX-512/AVX2/NEON/scalar). It targets on-device RAG, offline agents, and embedded retrieval -- the niche SQLite occupies for relational data: one file, one call, runs anywhere.
```

---

## GHR0092 — gh_34_cited_answer_3

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 70
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese'?

### Claim

The authors also mention that while TOTEN achieves unit ontological atomicity and numerical reconstruction, it may not perform as well in other linguistic contexts or for entities not covered by the ontology .

### Evidence

```text
[1] Toten: Knowledge-Based Ontological Tokenization Of Physical Quantities And Technical Notation In Brazilian Portuguese
Byte-Pair Encoding tokenization is statistically efficient for vocabulary compression, but semantically blind to structured technical entities, fragmenting physical quantities, numbers, units, and symbolic expressions into lexically arbitrary subwords. We present TOTEN, a knowledge-based ontological tokenization framework that replaces statistical derivation with declarative classification grounded in a formal ontology of engineering entities (OEE). We formalize TOTEN as the triple <O, classify, {inst_tau}>: the ontology gathers types, structural principles, composition relations, and preservable invariants; the classification function maps raw text into typed regions; and the instantiator family yields a self-descriptive structured representation. Robustness derives from deterministic coupling with three external oracles: Pint (dimensional), Unicode Character Database (typographic), and RSLP (Portuguese morphology). Intrinsic evaluation covers four properties verifiable by construction -- ontological atomicity, dimensional equivalence, typographic robustness, and numerical reconstruction -- over an internal, physically validated benchmark (EngQuant, N=800) and four Brazilian Portuguese external corpora (N=1771 eligible cases). We also report detection recall, distinguishing coverage from conditional atomicity. Against eight state-of-the-art baselines, TOTEN achieves unit ontological atomicity in all contrasts and numerical reconstruction of 0.775-0.904 on external corpora, vs. 0.627-0.703 for the best baseline (Quantulum3); on EngQuant, 0.780 vs. 0.340. Differences are statistically significant (McNemar with Holm correction). Spearman correlation between internal and external rankings confirms concurrent validity of the control benchmark. Dimensional equivalence shows statistical parity with Pint, the oracle from which the system inherits dimensional authority.
```

---

## GHR0020 — gh_79_cited_answer_8

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 71
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems'?

### Claim

It also provides examples of the types of failure modes detected by the sub-agents and the rationales they provide for their abstention.

### Evidence

```text
[1] EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems
In large-scale enterprise settings, centralized multi-agent systems (MAS) are increasingly adopted, in which a coordinator delegates user requests to lightweight, domain-specialized sub-agents. While this architecture improves modularity, scalability, and cost efficiency, its reliability depends not only on accurate routing but also on sub-agents' ability to calibrate their responses to capability constraints. In particular, sub-agents built on smaller fine-tuned models often struggle with such calibration, leading them to over-answer ambiguous, underspecified, misrouted, or unsupported requests and produce hallucinated outputs instead of actionable feedback. To address this challenge, we present EARS (Explanatory Abstention for Reliable Sub-Agent Modeling), a production-oriented framework that reframes sub-agent abstention as an inter-agent communication protocol: a sub-agent does not merely abstain, but exposes an actionable failure state to the coordinator. EARS curates human-agent interaction data using an ensemble of calibrated LLM-as-a-Judge models, producing structured abstention labels and rationales under a taxonomy of sub-agent failure modes. These data are used to fine-tune sub-agents to detect failure conditions and return rationales for coordinator-level clarification, rerouting, or fallback. We evaluate EARS in a large-scale production e-commerce assistant supporting enterprise business intelligence workflows. EARS improves the overall response pass rate from 68.5% to 78.9%, demonstrating that sub-agent-side explanatory abstention improves MAS reliability.
```

---

## GHR0061 — gh_88_plain_answer_1

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 72
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'?

### Claim

The paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction' describes experiments across benchmark datasets for Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE).

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.
```

---

## GHR0069 — gh_16_cited_answer_10

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 73
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'REVES: REvision and VErification--Augmented Training for Test-Time Scaling'?

### Claim

Scaling to 180M parameters, PHA achieves 16.42 PPL, which gives comparable results with the pure attention baseline while delivering 24\% higher throughput and up to

### Evidence

```text
[1] REVES: REvision and VErification--Augmented Training for Test-Time Scaling
Test-time scaling via sequential revision has emerged as a powerful paradigm for enhancing Large Language Model (LLM) reasoning. However, standard post-training methods primarily optimize single-shot objectives, creating a fundamental misalignment with multi-step inference dynamics. While recent work treats this as multi-turn reinforcement learning (RL), conventional approaches optimize over the multi-step trajectories directly, failing to further exploit the high-quality mistakes in intermediate steps that model can learn from correcting them. We propose a two-stage iterative framework that alternates between online data/prompt augmentation and policy optimization. By converting the intermediate steps (``near-miss'' answers) in the successful recovery trajectories into decoupled revision and verification prompts, our approach concentrates training on both effective answer transformation and error identification. This approach enables efficient off-policy data generation and reduces the computational overhead of long-horizon sampling compared to standard multi-turn RL. On LiveCodeBench, using publicly available test cases as feedback, we observe gains of +6.5 points over the RL baseline and +4.0 points over standard multi-turn training. Beyond coding, our approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems. Math results under ground-truth verification further confirm improved correction ability. It also generalizes to out-of-distribution constraint-satisfaction puzzles such as n\_queens and mini\_sudoku, where correctness is defined entirely by problem constraints. Code is available at https://github.com/yxliu02/REVES.git.

[2] Context-Aware RL for Agentic and Multimodal LLMs
Large language models (LLMs) often fail when answering requires identifying a small but decisive piece of evidence within a long or complex context, such as a single line in a tool trace or a subtle detail in an image. We propose ContextRL, a context-aware reinforcement learning (RL) method that improves long-horizon reasoning and multimodal performance through an \emph{indirect} auxiliary objective. Instead of supervising only the final answer, ContextRL presents the model with a query, an answer, and two highly similar contexts, and rewards it for selecting the context that supports the query--answer pair, thereby encouraging fine-grained grounding. We construct contrastive context data in two domains: for coding agents, trajectories serve as contexts, yielding 1k pairs built via condition filtering; for multimodal reasoning, images serve as contexts, yielding 7K pairs built via generative editing and similarity search. ContextRL achieves average gains of +2.2% over standard GRPO on 5 long-horizon benchmarks, and +1.8% across 12 diverse visual question answering benchmarks. To disentangle the effect of the proposed objective from that of additional data, we compare against data-augmentation baselines that repurpose the same contrastive contexts as standard query--context--answer examples. These baselines provide little to no improvement, showing that the gains arise from the proposed context-selection objective rather than from the contrastive data alone.

[3] Long-Context Modeling via GSS-Transformer Hybrid Architecture with Learnable Mixing
Modeling long-range dependencies remains a central challenge in natural language processing. Transformer architectures achieve strong performance via self-attention but scale quadratically ($O(N^2)$) with sequence length, while State Space Models (SSMs) scale linearly ($O(N)$) but suffer from a selective recall bottleneck, struggling to retrieve precise information from compressed states. This creates a fundamental tradeoff between efficiency and perplexity. To tackle these challenges, we propose the \textit{Parallel Hybrid Architecture (PHA)}, which runs Gated State Spaces (GSS), Grouped Query Attention (GQA), and Feed-Forward Networks (FFNs) as independent parallel branches fused by a learnable mixing mechanism. Instead of forcing SSMs to approximate attention or serializing the two paradigms, PHA allows each branch to specialize: GSS captures global context, while attention performs selective retrieval, with FFN providing complementary processing. On WikiText-103, PHA achieves 16.51 PPL at 125M parameters, outperforming Hedgehog (16.70) and H3-125M (23.70). Scaling to 180M parameters yields 16.42 PPL, which gives comparable results with the pure attention baseline while delivering 24\% higher throughput and up to 40\% lower memory usage at long contexts. On OpenWebText, our 125M model achieves 19.72 PPL, outperforming standard Transformers (20.60) and GSS hybrid baselines (19.80). These results demonstrate that separating sequence modeling paradigms into parallel specialists enables Tr

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0037 — gh_72_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 74
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval'?

### Claim

To make the evaluation more rigorous under densely crowded scene conditions, they introduce a challenging subset called Dense-Set, which is derived from COCO and Flickr30K.

### Evidence

```text
[1] LARE: Low-Attention Region Encoding for Text-Image Retrieval
Image retrieval in crowded scenes is particularly challenging due to the salience bias of conventional visual encoders, which tend to focus on dominant objects while neglecting low-attention regions that are often crucial for fine-grained retrieval. We propose LARE (Low-Attention Region Encoding), a framework that explicitly models these overlooked regions. LARE adopts a dual-encoding strategy that encodes low-attention regions of an image and the full image in parallel, leading to more diverse and informative image embeddings. To evaluate image retrieval performance in challenging crowded scenes, we introduce Dense-Set, a challenging subset derived from COCO and Flickr30K. In this subset, images are re-captioned to provide richer descriptions of low-attention or previously overlooked regions. This dataset highlights the limitations of existing retrieval models and enables a more rigorous evaluation under densely crowded scene conditions. Experimental results demonstrate that the proposed framework improves retrieval performance by preserving subtle, non-dominant visual cues within the shared latent space.
```

---

## GHR0065 — gh_27_cited_answer_5

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 75
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice'?

### Claim

The paper introduces the concept of Zwischentexte (intermediate texts that function as interpretive proposals rather than findings) as a framework for responsible integration of LLM-generated text into scholarly practice .

### Evidence

```text
[1] HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice
Retrieval-Augmented Generation (RAG) is the prevailing architecture for grounding language model outputs in external evidence, yet its dominant evaluation paradigms and default configurations remain oriented toward factual question-answering. For interpretive disciplines such as historical studies, RAG embeds assumptions that conflict with scholarly practice. We introduce HistoRAG, a framework that translates historiographical principles into concrete architectural interventions. Separated retrieval and generation decouples source discovery from interpretation, temporal windowing enforces balanced source representation across the research period as a methodological requirement of historical inquiry, and LLM-as-judge evaluation makes relevance judgments transparent and contestable. We evaluate these interventions using SPIEGELragged, applied to 102,189 articles from Der Spiegel (1950-1979). Each intervention addresses a measurable deficiency in standard RAG: era-specific vocabulary retrieves zero chunks from the 1950s when using 1970s terminology, evidence of the temporal skew that motivates windowing; vector similarity and LLM-assessed relevance correlate only weakly (Spearman rho = 0.275), motivating post-retrieval evaluation; and keyword-based and semantic retrieval surface largely disjoint source pools, motivating an architecture in which both operate as complementary retrieval layers under a shared LLM evaluation filter. We also introduce the concept of Zwischentexte (intermediate texts that function as interpretive proposals rather than findings) as a framework for responsible integration of LLM-generated text into scholarly practice. The architecture offers a model for how domain-specific epistemological commitments can be translated into RAG design decisions, and may transfer to other interpretive disciplines working with large corpora.
```

---

## GHR0007 — gh_148_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 76
- sampling_stratum: `drop_home_related::plain_answer`
- sampling_weight: `4.333333333333333`
- hard_policy: `drop_home_related`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

The sources provided are about Operad theory and test-time scaling for agentic search, not about hallucination detection in large language models.

### Evidence

```text
[1] Operadic consistency: a label-free signal for compositional reasoning failures in LLMs
Detecting LLM reasoning failures at inference time without ground-truth labels has motivated a wide range of confidence baselines, including self-consistency, semantic entropy, and P(True), built on within-question sampling and self-evaluation. Operad theory, the formalism for systems built by iterated substitution, suggests a complementary diagnostic: a model's direct answer to a compositional query should agree with the answer it produces by composing a stated decomposition of the same query. We instantiate this idea as operadic consistency (OC), a per-question signal. Across twelve instruction-tuned LLMs (4B to 671B parameters, open-weights and closed-source) on four multi-hop QA datasets, OC is strongly correlated with accuracy on every dataset (Pearson $r \in [0.86, 0.94]$, all $p \leq 0.0004$), and is the only signal we evaluate with $r \geq 0.85$ uniformly across all four datasets. Chain-of-thought self-consistency (CoT-SC; Wang et al., 2023) matches OC on HotpotQA and DROP ($r = 0.93, 0.87$) but drops to $r \approx 0.45$ on MuSiQue and StrategyQA. At the per-question level, OC contributes information beyond CoT-SC and semantic entropy on every dataset (cluster-robust $p \leq 10^{-16}$ for the OC coefficient), and the conclusion is robust to additionally controlling for constructed decomposition-aware baselines ($p \leq 10^{-13}$). The same signal yields selective-prediction improvements (accuracy at fixed coverage) over a tuned CoT-SC baseline at the equal-cost $K = 3$ budget (AUARC lifts of +0.086 to +0.096 and AUROC lifts of +0.092 to +0.164; 95% CIs exclude zero on every cell). On five frontier thinking models, where the decomposition is extracted from the model's own chain of thought, the same equal-cost comparison gives positive selective-prediction point-estimate lift on all 16 (dataset, budget, metric) cells tested, with 95% CIs excluding zero on 12 of the 16.

[2] Beyond Parallel Sampling: Diverse Query Initialization for Agentic Search
Test-time scaling for agentic search typically increases depth (i.e., more turns and tokens per trajectory) or breadth (i.e., more parallel rollouts). Here we focus on breadth scaling, showing that standard parallel sampling yields diminishing returns, tracing this to query redundancy at the first turn. When models issue similar first queries across rollouts, the threads retrieve overlapping evidence, and subsequent turns are conditioned on this shared retrieval. We address this limitation with DivInit, a training-free intervention at the first turn. Rather than sampling k independent first queries, DivInit draws n candidates from a single call, picks k < n diverse seeds, and runs them as parallel trajectories. Across five open-weight models and eight benchmarks, DivInit consistently improves over standard parallel sampling, with average gains of five to seven points on multi-hop QA at matched compute. Code available at https://github.com/cxcscmu/diverse-query-initialization
```

---

## GHR0120 — gh_41_plain_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 77
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation'?

### Claim

The paper also presents the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document.

### Evidence

```text
[1] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.

[2] Context Compression Is Not One Thing: Readable Symbolic Re-expression vs. Coherent Summary at Matched Budget
We study context compression for multi-hop question answering with small language models. We propose Telegraph English, a readable symbolic format that rewrites retrieved passages into structured entity-relation statements, preserving reasoning evidence at lower token cost. In controlled experiments on MuSiQue, TwoWiki, and HotpotQA, Telegraph English outperforms three matched-budget compression baselines (character-level deletion, truncation, and random sub-sampling) on every dataset, with gains of 13 to 20 F1 percentage point. It also outperforms a coherent prose summary produced by the same encoder on the hardest dataset. A pre-registered depth-interaction hypothesis is null: the advantage does not grow with reasoning depth within datasets. We interpret these results as evidence that readable symbolic re-expression preserves entity content more densely than either natural language or coherent summarization at matched token budget.

[3] Query-aware Routing for Filtered Approximate Nearest Neighbors Search
Filtered ANN search, which combines vector similarity with attribute predicates, is a core primitive in modern vector databases and retrieval-augmented generation. We benchmark all major categorical filtered ANN methods across multiple datasets under three predicates and find that no single method dominates. Moreover, even within a single dataset and predicate type, the best method for a query can vary. Therefore, we propose a query-aware routing framework. A lightweight ML model predicts each candidate method's recall on the query, and the router consults an offline benchmark table that maps every method and parameter setting to its measured recall and QPS, then selects the method with the best recall--QPS trade-off. Our ablation study narrows 22 candidate features to a minimal set of three and we adopt regression rather than classification as the prediction target to sharpen accuracy. Our model is trained on six real-world datasets and applied to five unseen validation datasets. The final result shows that our router achieves state-of-the-art recall and QPS balance across all five validation datasets compared to existing filtered ANN baselines, while incurring negligible latency overhead.
```

---

## GHR0041 — gh_78_plain_answer_1

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 78
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio'?

### Claim

The paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio' describes a dataset called MetaSyn.

### Evidence

```text
[1] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.
```

---

## GHR0123 — gh_129_cited_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 79
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation', and what problem is it designed to address?

### Claim

I cannot answer the question using only the given sources.

### Evidence

```text
[1] Context Compression Is Not One Thing: Readable Symbolic Re-expression vs. Coherent Summary at Matched Budget
We study context compression for multi-hop question answering with small language models. We propose Telegraph English, a readable symbolic format that rewrites retrieved passages into structured entity-relation statements, preserving reasoning evidence at lower token cost. In controlled experiments on MuSiQue, TwoWiki, and HotpotQA, Telegraph English outperforms three matched-budget compression baselines (character-level deletion, truncation, and random sub-sampling) on every dataset, with gains of 13 to 20 F1 percentage point. It also outperforms a coherent prose summary produced by the same encoder on the hardest dataset. A pre-registered depth-interaction hypothesis is null: the advantage does not grow with reasoning depth within datasets. We interpret these results as evidence that readable symbolic re-expression preserves entity content more densely than either natural language or coherent summarization at matched token budget.

[2] Adaptive Multi-Resolution Procedural Knowledge Compression for Large Language Models
Large language models (LLMs) are widely used to tackle complex tasks with autonomous workflows. Recently, reusable natural language skills have emerged as a popular paradigm to inject procedural knowledge into LLM applications. Since popular skills are often invoked repeatedly, placing their full text in every context significantly increases prefill cost and latency. While text compression techniques have the potential to solve this problem, most existing methods are designed to compress factual knowledge in documents instead of procedural knowledge, making them insufficient for skill compression. In this paper, we argue that an effective skill compression method should: 1) preserve logical dependencies among workflows and tool protocols, 2) enable lightweight, offline compression for frequently updated community skills, and 3) be adaptable to varying complexities across skills. To address this, we present SKIM (SKIll coMpression), an adaptive multi-resolution soft token compression framework for procedural skills. Depending on the complexity of each skill, SKIM creates different numbers of soft tokens that not only improve the efficiency of LLM inference, but also preserve the effectiveness of skill usage. Experiments indicate that SKIM compresses skills to 30 to 60 percent of their original token length while preserving task performance better than existing compression methods.We have released our code at https://github.com/bebr2/SKIM .
```

---

## GHR0119 — gh_36_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 80
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'ScholarSum: Student-Teacher Abstractive Summarization via Knowledge Graph Reasoning and Reflective Refinement'?

### Claim

it is implied that the performance of ScholarSum is evaluated against previous baselines in terms of both completeness and faithfulness.

### Evidence

```text
[1] ScholarSum: Student-Teacher Abstractive Summarization via Knowledge Graph Reasoning and Reflective Refinement
Abstractive summarization plays a crucial role in enabling efficient understanding of scientific literature, yet it inherently demands both linguistic fluency and factual faithfulness. Existing approaches often fail to reconcile these two requirements. Extractive methods rely on rigid sentence splicing that disrupts macro-level logical coherence, while large language model (LLM)-based generative approaches, despite mastering linguistic fluency, exhibit limited factual consistency. In this work, we propose ScholarSum, a hierarchical reflective graph-based framework that emulates a student-teacher writing process for fluent and faithful scientific summarization. ScholarSum first organizes the document into a hierarchical knowledge graph by segmenting it into semantically coherent units, whose multi-layered community structure captures global logic and macro-level themes. Guided by this global structure, the student generates an initial draft, which is subsequently refined through fine-grained evidence retrieval. To ensure factual consistency, a teacher-like reviewer then iteratively examines the draft, identifies unsupported content, and prompts targeted re-retrieval and rewriting until the summary meets rigorous quality standards. Extensive experiments demonstrate that ScholarSum significantly outperforms previous baselines in terms of both completeness and faithfulness. Our code is available at https://github.com/Xiaoyu-Tao/ScholarSum.

[2] CQC-RAG: Robust Retrieval-Augmented Generation via Cross-Query Consistency
Retrieval-Augmented Generation (RAG) has become a common approach for improving the factuality of Large Language Models (LLMs), yet its reliability remains highly sensitive to how external evidence is retrieved and used. Semantically equivalent queries with different syntactic forms may lead to different retrieval results, while irrelevant or misleading documents can further induce hallucinated answers. Existing multi-path reasoning methods improve robustness by sampling multiple candidate answers and applying voting- or confidence-based selection, but they still face two limitations: diversity is often injected through uncontrollable decoding randomness, and answer evaluation is usually confined to a single query-induced evidence view. To address these limitations, we propose a Cross-Query Consistency Hypothesis: correct answers tend to maintain high confidence across semantically equivalent but syntactically diverse queries, whereas noise-induced hallucinations exhibit unstable confidence under such query variations. Based on this hypothesis, we introduce CQC-RAG, a framework that co-designs query-level diversity injection with cross-query consistency evaluation. CQC-RAG rewrites the original question into diverse but meaning-preserving queries, reranks a shared document pool to construct query-conditioned reasoning contexts, applies an evidence-grounded protocol to extract answer-evidence pairs and selects answers according to their confidence stability across these contexts. This design enables self-evaluation without external supervision and does not rely on expanded retrieval coverage. Experiments on four open-domain question answering benchmarks show that CQC-RAG outperforms the strongest previous multi-query baseline by +4.76 pp EM on TriviaQA and +9.12 pp EM on MuSiQue, validating the effectiveness of cross-query consistency for filtering noise-induced hallucinations.

[3] Zero-source LLM Hallucination Detection with Human-like Criteria Probing
Large language models (LLMs) often hallucinate by generating factually incorrect or unfaithful content, posing significant risks to their safe use. Detecting such hallucinations is particularly challenging under the zero-source constraint, where no model internals or external references are available, and detection must rely solely on the textual query-answer pair. In this paper, we propose Human-like Criteria Probing for Hallucination Detection (HCPD), a paradigm that emulates the multi-faceted reasoning of human evaluators. Its core is a Human-like Criteria Probing (HCP) mechanism, in which a LLM agent adaptively decomposes its judgment into a weighted set of interpretable criteria and aggregates criterion-specific scores into a final truthfulness measure. To achieve this adaptive capability, we introduce a reward-based alignment scheme using only weak supervision from semantic consistency. At inference, we employ a multi-sampling aggregation strategy to ensure robust decisions while preserving full interpretability. We further provide theoretical analysis supporting the reliability of our approach. Extensive experiments show that HCPD consistently outperforms state-of-the-art baselines, offering an effective and explainable solution for zero-source hallucination detection. Code is available at https://github.com/TRISKEL10N/HCPD.
```

---

## GHR0094 — gh_48_plain_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 81
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Understanding the Behaviors of Environment-aware Information Retrieval'?

### Claim

The paper 'Understanding the Behaviors of Environment-aware Information Retrieval' discusses several limitations, ablations, and analysis findings.

### Evidence

```text
[1] Understanding the Behaviors of Environment-aware Information Retrieval
Recent retrieval-augmented generation (RAG) approaches have demonstrated strong capability in handling complex queries, yet current research overlooks a critical challenge: different retrievers require fundamentally different query formulation strategies for optimal performance. In this work, we present the first systematic analysis of how LLMs can learn to adapt their query formulation strategies for different retrievers via reinforcement learning (RL). Our empirical study reveals that RL effectively teaches an LLM to tailor its queries to specific retriever characteristics. We discover that different retrievers exhibit surprisingly distinct optimal query styles (e.g., descriptive vs. question-like), suggesting strategies learned for one retriever ineffective for another. We further show that performance can be enhanced by incorporating retriever-specific human guidance and by scaling model size. To facilitate learning over multi-retrieval-step trajectories, we introduce a branching-based rollout technique that improves training stability. Our work provides the first empirical evidence and actionable insights for building truly retriever-aware RAG systems. Code and resources are available at https://github.com/LCO-Embedding/Envs-aware-Information-Retrieval.

[2] When Does Mixing Help? Analyzing Query Embedding Interpolation in Multilingual Dense Retrieval
While mixed-language querying is ubiquitous in multilingual communities, the sensitivity of dense retrievers to such queries remains poorly understood. We present a ratio-controlled study on mMARCO that systematically evaluates retrieval performance by varying the mixing proportion of parallel query translations via embedding-level mixing -- constructing mixed queries as an interpolation of monolingual embeddings. Experiments with BGE-M3 demonstrate that an optimal mixing ratio outperforms the best monolingual endpoint in 88/105 cases. We uncover a distinct asymmetry driven by English dominance: mixing is uniformly beneficial when retrieving from non-English document indices, whereas indices containing English are best served by pure English queries. Furthermore, English acts as the strongest mixing partner for every non-English document language. Finally, when controlling for English dominance, mixing gains correlate negatively with typological distance. We conclude that language-mix sensitivity is structured and predictable, and we validate the robustness of these patterns across model families and scales.

[3] RL-Index: Reinforcement Learning for Retrieval Index Reasoning
Retrieving external knowledge is essential for solving real-world tasks, yet it remains challenging when the relationship between a query and its relevant knowledge involves implicit and complex reasoning beyond surface-level semantic or lexical matching (e.g., mathematical problems relying on the same theorem or coding requiring deep reasoning). Existing approaches primarily rely on query-side reasoning (e.g., query rewriting), which introduces significant online latency and underutilizes the opportunity to perform reasoning over the knowledge corpus itself (i.e., index-side reasoning). In this paper, we propose RL-Index, an agentic indexing framework that formulates retrieval index reasoning as a reinforcement learning problem. Instead of performing reasoning at query time, RL-Index shifts reasoning to the indexing stage by augmenting documents with LLM-generated rationales that explicitly encode the latent query-knowledge relationship. To optimize the quality of these rationales, we employ Group Relative Policy Optimization (GRPO) and use retrieval similarity as a verifiable reward signal, enabling direct optimization of indexing decisions for retrieval effectiveness. Extensive experiments on the BRIGHT benchmark demonstrate that RL-Index consistently improves both retrieval and downstream question-answering performance, while significantly reducing online inference latency. Moreover, the learned rationale augmentation generalizes across diverse retrievers and generators, highlighting its robustness as a plug-and-play indexing strategy across different retrieval systems.
```

---

## GHR0113 — gh_23_plain_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 82
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems', and what problem is it designed to address?

### Claim

MonaVec targets the deployment profile of SQLite, aiming for one file, one function call, and the ability to run anywhere.

### Evidence

```text
[1] MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems
We present MonaVec, a deterministic, embedded vector-search kernel for edge and offline AI -- settings where server infrastructure, network connectivity, and training data are all unavailable. Existing vector-search systems assume a persistent server, gigabytes of RAM, or a training pass over the corpus; MonaVec instead targets the deployment profile of SQLite: one file, one function call, runs anywhere. Its quantization core is training-free by default and data-oblivious: a Randomized Hadamard Transform (RHDH) conditions any input distribution toward N(0,1), so precomputed Lloyd-Max tables quantize to 4 bits (8x smaller) with no learned codebook and no data pass. The index persists as a single .mvec file whose embedded ChaCha20 rotation seed makes results reproducible across architectures and byte-identical within a build -- a determinism guarantee that parallel-build graph libraries cannot offer. On semantic embeddings (AG News, 45K x 1024-dim BGE-M3, cosine), MonaVec 4-bit BruteForce reaches 0.960 Recall@10 in 27 MB -- leading float32 FAISS-IVF and 8-bit usearch on recall -- while trading peak throughput for byte-identical determinism. A single-pass global standardization (fit()) extends the same data-oblivious pipeline to magnitude-sensitive L2 data, and optional IvfFlat and HNSW backends carry it to million-vector corpora. MonaVec is implemented in pure Rust with Python bindings and runtime SIMD dispatch (AVX-512/AVX2/NEON/scalar). It targets on-device RAG, offline agents, and embedded retrieval -- the niche SQLite occupies for relational data: one file, one call, runs anywhere.

[2] SCAR: Semantic Continuity-Aware Retrieval for Efficient Context Expansion in RAG
Fixed-length chunking in Retrieval-Augmented Generation (RAG) often leads to boundary fragmentation, where critical evidence is split across segments, degrading retrieval recall. While static windowing and parent retrieval improve recall, they introduce significant token overhead. We propose SCAR (Semantic Continuity-Aware Retrieval), an adaptive retrieval policy that selectively expands neighboring chunks by weighing query-neighbor relevance against a structural continuity penalty. SCAR uses a relative expansion threshold tied to each retrieved chunk's own query-relevance, yielding an approximately scale-invariant decision rule that transfers across embedding models without recalibration. Across four diverse corpora (RFC, GDPR, a 10-K report, and a Merger agreement; N=320 queries; 160 boundary-fragmented), SCAR achieves 92.8% recall on boundary-fragmented queries with only 7.84 chunks, a 22.9% reduction compared to static windowing (10.16 chunks). Paired bootstrap tests (B=10,000) confirm the chunk reduction is highly significant (p<0.0001, Cohen's d=-1.49, large effect), with a small recall difference (Cohen's d=-0.33). The policy transfers across three embedding models (text-embedding-3-large, BGE-large-en-v1.5, zembed-1) using the same single hyperparameter setting, and downstream RAGAS evaluation on the 10-K corpus confirms SCAR preserves generation faithfulness while reducing context tokens by 27.1%.

[3] Charge as a Construct-Validity Factor in Chinese Legal Case Retrieval: A Cross-Benchmark Audit
Chinese Legal Case Retrieval (LCR) benchmarks grade a reference judgment relevant when its legal characterization matches the query, and strong systems now reach NDCG@10 of 0.85-0.88. Most of the BM25-to-best-trained gap is recoverable with no retrieval model: ranking candidates only by shared primary charge, broken by BM25, closes 99.2% of it on LeCaRDv2 -- with no detectable difference from the best-trained system. This reflects benchmark design: LeCaRDv2 defines top relevance via the crime's key constitutive elements, which encode the charge, so same-charge cases are relevant by construction (relevance lift 4.49; charge-to-relevance macro-AUC 0.871). Holding charge fixed, the trained reranker's advantage over BM25 collapses to a small within-charge residual (+0.026 NDCG@10, cluster-bootstrap CI excluding zero, about a quarter), the only non-definitional positive. The effect is not uniform: the same rule recovers 84.3% on LeCaRDv1 and is out of spec on CAIL2022, with the charge-to-relevance signal weakening in step (macro-AUC 0.871/0.759/0.728); a predicted-charge cascade reproduces 76.6% on LeCaRDv2 but does not transfer. The construct is also cashable at first stage: an exploratory zero-training charge-pool channel lifts LeCaRDv2 recall (R@100 +0.025, wrong-charge controls hurt), reported as a positive control for the confound, not a retrieval method or novelty claim. Charge is thus a high-leverage construct-validity factor at the benchmark level -- not auniform explanation of NDCG@10, and not evidence that any system relies on charge. We package established construct-validity and partial-input checks as a reusable charge-controlled protocol (CCE); o

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0042 — gh_87_plain_answer_5

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 83
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation'?

### Claim

For evidence-poor trajectories, a frozen gold-evidence teacher provides token-level KL (Kullback-Leibler) guidance on reasoning and search-query tokens, excluding answer tokens to avoid direct response imitation.

### Evidence

```text
[1] PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation
Agentic GraphRAG trains language-model agents to iteratively retrieve and reason over graph-structured evidence, enabling more accurate and context-aware decision-making by efficiently navigating complex information networks. However, outcome-only reinforcement learning suffers from \textit{\textbf{answer-path reward aliasing}}, where correct answers may come from shortcuts rather than useful evidence paths. It also exhibits \textit{\textbf{search-update ambiguity}}, as scalar trajectory-level feedback does not indicate which retrieval actions to adjust. To mitigate these shortcomings, we present PathRouter, a path-aware training framework for agentic GraphRAG. PathRouter jointly evaluates each trajectory along answer correctness and evidence-path overlap, yielding four trajectory categories with differentiated GRPO advantage scaling that suppresses shortcut reinforcement while preserving evidence-seeking behavior. For evidence-poor trajectories, a frozen gold-evidence teacher provides token-level KL guidance on reasoning and search-query tokens, excluding answer tokens to avoid direct response imitation. Experiments on six QA benchmarks across three model sizes show that PathRouter consistently improves answer F1 and evidence-path overlap, achieving average F1 gains of 3.1 on 3B and 4.9 on 7B models compared to a strong baseline.
```

---

## GHR0058 — gh_97_plain_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 84
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science'?

### Claim

The evaluation settings involve examining the classification performance of various segments (different parts of the full-text content) and their combinations across multiple models.

### Evidence

```text
[1] Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science
Research methods are essential carriers of knowledge contribution in academic papers. Automatic multi-label classification of research methods can support knowledge services such as method retrieval, review generation, and research intelligence analysis. While existing studies primarily rely on titles and abstracts, abstracts often provide only limited methodological information, whereas utilizing full-text content faces challenges related to excessive length and information redundancy. Therefore, this paper proposes a segment combination strategy by partitioning the full-text content according to its physical postion. Using an annotated corpus of 1,954 full-text articles from three representative journals in Library and Information Science (JASIST, LISR, and JDoc), we evaluate the classification performance of various segments and their combinations across multiple models. Experimental results indicate that methodological information is distributed unevenly within the full-text content, with the middle-to-late and final segments exhibiting greater discriminative power. Furthermore, integrating bibliographic metadata with cross-segment combination strategies effectively enhances classification performance.
```

---

## GHR0087 — gh_16_cited_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 85
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'REVES: REvision and VErification--Augmented Training for Test-Time Scaling'?

### Claim

On LiveCodeBench, the proposed approach gains +6.5 points over the RL baseline and +4.0 points over standard multi-turn training .

### Evidence

```text
[1] REVES: REvision and VErification--Augmented Training for Test-Time Scaling
Test-time scaling via sequential revision has emerged as a powerful paradigm for enhancing Large Language Model (LLM) reasoning. However, standard post-training methods primarily optimize single-shot objectives, creating a fundamental misalignment with multi-step inference dynamics. While recent work treats this as multi-turn reinforcement learning (RL), conventional approaches optimize over the multi-step trajectories directly, failing to further exploit the high-quality mistakes in intermediate steps that model can learn from correcting them. We propose a two-stage iterative framework that alternates between online data/prompt augmentation and policy optimization. By converting the intermediate steps (``near-miss'' answers) in the successful recovery trajectories into decoupled revision and verification prompts, our approach concentrates training on both effective answer transformation and error identification. This approach enables efficient off-policy data generation and reduces the computational overhead of long-horizon sampling compared to standard multi-turn RL. On LiveCodeBench, using publicly available test cases as feedback, we observe gains of +6.5 points over the RL baseline and +4.0 points over standard multi-turn training. Beyond coding, our approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems. Math results under ground-truth verification further confirm improved correction ability. It also generalizes to out-of-distribution constraint-satisfaction puzzles such as n\_queens and mini\_sudoku, where correctness is defined entirely by problem constraints. Code is available at https://github.com/yxliu02/REVES.git.
```

---

## GHR0009 — gh_157_plain_answer_1

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 86
- sampling_stratum: `drop_home_related::plain_answer`
- sampling_weight: `4.333333333333333`
- hard_policy: `drop_home_related`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems'?

### Claim

The sources provided do not mention the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems'.

### Evidence

```text
[1] Scaling Enterprise Agent Routing: Degradation, Diagnosis, and Recovery
Production LLM assistants route user requests to growing libraries of specialized tools, but how does routing accuracy degrade as the catalog scales? We study single-step routing on a 110-agent, 584-tool catalog from a deployed enterprise productivity assistant, evaluating three frontier models from 10 to 110 agents. Routing F1 on under-specified requests drops 16--23 percentage points across models. An oracle analysis decomposes the degradation into a \emph{retrieval} gap (the model cannot surface the right tool) and a \emph{confusion} gap (even with perfect retrieval, the oracle ceiling drops 10pp). Embedding-based shortlisting recovers +10--11pp F1 at full scale across all three models and two providers. A production annotation study (1,435 human-labeled utterances, three annotators) confirms the recovery on real traffic at +10--17pp despite 10--15pp lower absolute performance.

[2] Shopping Reasoning Bench: An Expert-Authored Benchmark for Multi-Turn Conversational Shopping Assistants
Conversational shopping assistants now serve hundreds of millions of customers, yet no existing benchmark jointly evaluates the open-ended multi-turn reasoning, domain expertise, and criterion-level quality that real shopping conversations demand. Shopping reasoning is unique among language model applications. Unlike factual question answering or verifiable code generation, it requires balancing subjective preferences, budget constraints, and cross-product trade-offs across multi-turn dialogue, capabilities absent from previous e-commerce and general-purpose benchmarks. We introduce the Shopping Reasoning Bench, an expert-authored benchmark of 525 missions (232 single-turn, 293 multi-turn) with 10863 importance-weighted binary rubrics authored by retail domain experts. These criteria are organized under a taxonomy of five reasoning categories and fifteen subcategories covering diverse demands such as preference refinement, trade-off analysis, and compatibility assessment. An evaluation of nine models across three families (GPT, Claude, Gemini) shows that pass rates reach only 57--77% overall. On multi-turn missions, all models score 13--29 points lower on optional above-and-beyond criteria than on required ones, and performance degrades 4--18 points as conversations progress. These gaps show that current models handle basic shopping assistance but fall short of expert-level advice, making Shopping Reasoning Bench a challenging testbed for future shopping assistant development.
```

---

## GHR0125 — gh_133_cited_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 87
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'ScholarSum: Student-Teacher Abstractive Summarization via Knowledge Graph Reasoning and Reflective Refinement', and what problem is it designed to address?

### Claim

The problem it is designed to address is not specified in the given sources either. do not discuss abstractive summarization via knowledge graph reasoning and reflective refinement.

### Evidence

```text
[1] CQC-RAG: Robust Retrieval-Augmented Generation via Cross-Query Consistency
Retrieval-Augmented Generation (RAG) has become a common approach for improving the factuality of Large Language Models (LLMs), yet its reliability remains highly sensitive to how external evidence is retrieved and used. Semantically equivalent queries with different syntactic forms may lead to different retrieval results, while irrelevant or misleading documents can further induce hallucinated answers. Existing multi-path reasoning methods improve robustness by sampling multiple candidate answers and applying voting- or confidence-based selection, but they still face two limitations: diversity is often injected through uncontrollable decoding randomness, and answer evaluation is usually confined to a single query-induced evidence view. To address these limitations, we propose a Cross-Query Consistency Hypothesis: correct answers tend to maintain high confidence across semantically equivalent but syntactically diverse queries, whereas noise-induced hallucinations exhibit unstable confidence under such query variations. Based on this hypothesis, we introduce CQC-RAG, a framework that co-designs query-level diversity injection with cross-query consistency evaluation. CQC-RAG rewrites the original question into diverse but meaning-preserving queries, reranks a shared document pool to construct query-conditioned reasoning contexts, applies an evidence-grounded protocol to extract answer-evidence pairs and selects answers according to their confidence stability across these contexts. This design enables self-evaluation without external supervision and does not rely on expanded retrieval coverage. Experiments on four open-domain question answering benchmarks show that CQC-RAG outperforms the strongest previous multi-query baseline by +4.76 pp EM on TriviaQA and +9.12 pp EM on MuSiQue, validating the effectiveness of cross-query consistency for filtering noise-induced hallucinations.

[2] Zero-source LLM Hallucination Detection with Human-like Criteria Probing
Large language models (LLMs) often hallucinate by generating factually incorrect or unfaithful content, posing significant risks to their safe use. Detecting such hallucinations is particularly challenging under the zero-source constraint, where no model internals or external references are available, and detection must rely solely on the textual query-answer pair. In this paper, we propose Human-like Criteria Probing for Hallucination Detection (HCPD), a paradigm that emulates the multi-faceted reasoning of human evaluators. Its core is a Human-like Criteria Probing (HCP) mechanism, in which a LLM agent adaptively decomposes its judgment into a weighted set of interpretable criteria and aggregates criterion-specific scores into a final truthfulness measure. To achieve this adaptive capability, we introduce a reward-based alignment scheme using only weak supervision from semantic consistency. At inference, we employ a multi-sampling aggregation strategy to ensure robust decisions while preserving full interpretability. We further provide theoretical analysis supporting the reliability of our approach. Extensive experiments show that HCPD consistently outperforms state-of-the-art baselines, offering an effective and explainable solution for zero-source hallucination detection. Code is available at https://github.com/TRISKEL10N/HCPD.
```

---

## GHR0030 — gh_52_cited_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 88
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'NEST: Narrative Event Structures in Time for Long Video Understanding'?

### Claim

The benchmark is highly challenging for grounded event discovery, with Event Trigger Detection (ETD) below 8%, Event Localization (EL) under 6%, and Event Argument Extraction (EAE) below 11%.

### Evidence

```text
[1] NEST: Narrative Event Structures in Time for Long Video Understanding
Recent progress in vision-language models has enabled the processing of increasingly long video sequences, but the ability to handle extended token streams does not translate to understanding of narrative structure in long videos. Existing long video benchmarks focus on needle-in-a-haystack retrieval rather than evaluating how low-level actions form events, how events interact across time, and how narratives progress, for example, whether a model can connect an early setback, such as a job loss to a later relationship breakup, despite long gaps, intervening scenes, or flashbacks that reframe what occurred. We introduce NEST (Narrative Event Structures in Time for Long Video Understanding), a dataset of 1005 full-length movies (avg. 98 minutes), each annotated with 102 multimodal narrative events grounded in visual content, dialogue, and audio. NEST captures multimodal narrative events with structured annotations grounded in visual content, dialogue, and audio, and links them through relations that reflect narrative structure, including temporal ordering, hierarchical composition, and long-range dependencies. We introduce baselines for event trigger detection (ETD), event localization (EL), event argument extraction (EAE), and event relation extraction (ERE). The benchmark is highly challenging for grounded event discovery, with ETD below 8%, EL under 6%, and EAE below 11%. In contrast, ERE is more tractable once events are given, reaching 35.45% F1 zero-shot and 44.42% F1 after fine-tuning.
```

---

## GHR0110 — gh_35_plain_answer_11

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 89
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization'?

### Claim

the authors note that this approach has not been extensively tested on

### Evidence

```text
[1] Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization
Optimal transport (OT) has been shown to detect hallucinations in neural machine translation (NMT) by measuring the geometric distance between cross-attention distributions and a reference distribution, without any supervision. We extend this analysis to all six decoder layers of the Fairseq DE-EN model ($N=3{,}414$), showing that Wass-to-Unif and Wass-to-Data are complementary detectors specialised across hallucination types, that detection is concentrated in layers L1--L4 with L5 anti-predictive for subtler types, and that hallucinated translations lack the exploratory attention phase present in correct translations from the first decoding step. We further evaluate whether the geometric signal transfers to abstractive summarization faithfulness detection: our unsupervised OT detector on AggreFact ($N=1{,}116$) achieves $57.2\%$/$57.6\%$ balanced accuracy on CNN/XSum -- above chance but substantially below supervised MiniCheck-Flan-T5-L($69.9\%$/$74.3\%$). This gap is principled: unlike NMT hallucinations, unfaithful summaries can attend correctly to source tokens while misrepresenting their content, a failure mode invisible to concentration-based OT metrics by construction. Structural experiments on T5-base confirm consistent decoder organisation across depth, with Layer~3 showing peak concentration and Layer~12 being most critical for generation quality. Together, the results establish OT on cross-attention as a reliable detector when the failure mode is source disengagement, a principled interpretability tool regardless of task, and fundamentally limited when faithfulness failures occur downstream of attention.

[2] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.

[3] Connecting Speech to Words through Images
How can we learn the mapping between written words and their spoken counterparts in the absence of explicit textual supervision? We present a visually grounded method for building a vocabulary of spoken words using only images and their spoken descriptions. First, image captioning systems are used to build a vocabulary of written words representing salient visual concepts in the images. For each word, we then find utterances whose image captions contain that word. Then we use an unsupervised word discovery technique to align these utterances to locate instances of the target word. The result is spoken word segments that are linked to written words -- all accomplished without any text supervision. In spoken word retrieval and keyword spotting experiments, the proposed approach outperforms a strong neural baseline while being more interpretable. These results demonstrate the feasibility of the approach in English and motivate future work on low-resource languages without transcripts.
```

---

## GHR0079 — gh_6_cited_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 90
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents'?

### Claim

CoreMem operates seamlessly within a strict 8 GB VRAM budget, successfully bridging the gap between resource-constrained edge devices and the demand for theoretically grounded, lifelong memory agents .

### Evidence

```text
[1] CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents
Personalized dialogue agents require continuous long-term memory to maintain coherent interactions across multiple sessions. However, deploying these capabilities on consumer-grade hardware (e.g., 8 GB VRAM edge devices) introduces severe memory and compute bottlenecks. Existing systems typically rely on isotropic cosine similarity for retrieval and heuristic rules for context compression. These approaches lack a unified theoretical foundation, frequently suffering from the hubness problem in high-dimensional retrieval and syntactic fragmentation during compression. To overcome these limitations, we propose CoreMem, a resource-efficient edge-cloud memory architecture fundamentally unified by information geometry. First, Riemannian retrieval replaces cosine matching with a locally adaptive Fisher-Rao metric, effectively penalizing hub memories via Mahalanobis distance with O(Ndr) Woodbury acceleration for real-time search. Second, Fisher-guided discrete token distillation (FDTD) introduces a hierarchical sentence-to-token compression mechanism. It derives sensitivity scores from Fisher information traces, providing a principled compression-KL tradeoff augmented with explicit structural syntax protection. Evaluated on the LOCOMO and LongMemEval-S benchmarks, CoreMem achieves strong accuracy improvements, yielding substantial gains in Open-domain (+4.51 pp) and Temporal (+4.17 pp) reasoning. Extensive profiling confirms that CoreMem operates seamlessly within a strict 8 GB VRAM budget, successfully bridging the gap between resource-constrained edge devices and the demand for theoretically grounded, lifelong memory agents.
```

---

## GHR0038 — gh_64_plain_answer_8

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 91
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Understanding the Behaviors of Environment-aware Information Retrieval'?

### Claim

The paper provides the first empirical evidence and actionable insights for building truly retriever-aware RAG systems.

### Evidence

```text
[1] Understanding the Behaviors of Environment-aware Information Retrieval
Recent retrieval-augmented generation (RAG) approaches have demonstrated strong capability in handling complex queries, yet current research overlooks a critical challenge: different retrievers require fundamentally different query formulation strategies for optimal performance. In this work, we present the first systematic analysis of how LLMs can learn to adapt their query formulation strategies for different retrievers via reinforcement learning (RL). Our empirical study reveals that RL effectively teaches an LLM to tailor its queries to specific retriever characteristics. We discover that different retrievers exhibit surprisingly distinct optimal query styles (e.g., descriptive vs. question-like), suggesting strategies learned for one retriever ineffective for another. We further show that performance can be enhanced by incorporating retriever-specific human guidance and by scaling model size. To facilitate learning over multi-retrieval-step trajectories, we introduce a branching-based rollout technique that improves training stability. Our work provides the first empirical evidence and actionable insights for building truly retriever-aware RAG systems. Code and resources are available at https://github.com/LCO-Embedding/Envs-aware-Information-Retrieval.
```

---

## GHR0124 — gh_141_cited_answer_1

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 92
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'Compact Geometric Representations of Hierarchies'?

### Claim

The paper 'Compact Geometric Representations of Hierarchies' is not among the provided sources, so I cannot find the information about the datasets, benchmarks, or evaluation settings described in that paper.

### Evidence

```text
[1] Querit-Reranker: Training Compact Multilingual Rerankers via Efficient Label-Free Distribution Adaptation
Deployable multilingual rerankers must generalize across languages, domains, and target ranking tasks while remaining efficient enough for second-stage reranking. However, adapting them to new target distributions typically requires extensive task-specific relevance annotations, which are costly to obtain. We present Querit-Reranker, a family of multilingual cross-encoder rerankers trained with a data-centric pipeline for label-efficient adaptation. We instantiate it as Querit-Reranker-A0.4B, initialized from an in-house MoE backbone with 0.4B activated parameters, and Querit-Reranker-4B, initialized from Qwen3-Embedding-4B. Our pipeline first learns general relevance modeling from large-scale ranking-oriented data, then adapts to target distributions through synthetic-query mining with teacher scores as continuous soft labels. To consolidate complementary task-adapted strengths, we further merge checkpoints via spherical linear interpolation, obtaining a single deployable model without runtime ensembling overhead. Using Qwen3-Embedding-0.6B as the shared first-stage retriever, Querit-Reranker-A0.4B improves average nDCG@10 from 54.11 to 59.28 on BEIR and from 59.87 to 67.70 on MIRACL. On MTEB Multilingual v2 Reranking, it also substantially outperforms larger embedding-based baselines, while Querit-Reranker-4B further achieves state-of-the-art performance among publicly available models. We release both models on Hugging Face.

[2] Non-negative Elastic Net Decoding for Information Retrieval
Dense retrieval has become the dominant paradigm in information retrieval, in which each document is scored against a query by the inner product of their vector embeddings, and the top-$k$ documents by score are retrieved for this query. However, since each document's score depends solely on the embedding of the query and itself, the retrieval process is oblivious to the content of the entire corpus. Therefore, dense retrieval cannot avoid selecting semantically similar documents from the corpus, which may result in a non-diverse, redundant set of retrieved documents. To this end, we approach retrieval as a joint decoding problem, in which documents are selected as a set with regard to the context of the rest of the corpus. To achieve this, we propose Non-Negative elastic Net (NNN) decoding, which selects documents whose embeddings jointly reconstruct the query embedding as a sparse non-negative linear combination. Our main theoretical result establishes a strict separation between dense retrieval and NNN decoding. For any corpus, every query correctly handled by dense retrieval is also handled by NNN decoding, while on corpora containing correlated documents, NNN decoding additionally handles queries that dense retrieval cannot. Experimental results indicate that applying NNN decoding to frozen embeddings trained for inner-product scoring yields consistent improvements across several benchmarks. Moreover, we introduce an end-to-end training procedure which optimizes the embeddings for NNN decoding, producing significant performance gains surpassing in all metrics and benchmarks compared to dense retrieval. Our work establishes a new paradigm for leveraging dense embeddings in information retrieval, beyond the standard practice of inner-product scoring.
```

---

## GHR0137 — gh_102_plain_answer_3

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 93
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization'?

### Claim

In the paper 'Hallucination detection in large language models', the main experimental results or comparisons reported are as follows:

### Evidence

```text
[1] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.

[2] Connecting Speech to Words through Images
How can we learn the mapping between written words and their spoken counterparts in the absence of explicit textual supervision? We present a visually grounded method for building a vocabulary of spoken words using only images and their spoken descriptions. First, image captioning systems are used to build a vocabulary of written words representing salient visual concepts in the images. For each word, we then find utterances whose image captions contain that word. Then we use an unsupervised word discovery technique to align these utterances to locate instances of the target word. The result is spoken word segments that are linked to written words -- all accomplished without any text supervision. In spoken word retrieval and keyword spotting experiments, the proposed approach outperforms a strong neural baseline while being more interpretable. These results demonstrate the feasibility of the approach in English and motivate future work on low-resource languages without transcripts.
```

---

## GHR0098 — gh_11_plain_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 94
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World'?

### Claim

Hybrid encoding reduces deployment cost by filtering less informative streaming frames and compressing the text skill bank.

### Evidence

```text
[1] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3.2% for Claude Code (Sonnet 4.6) over no-evolution baselines, with a -9.5% cost reduction compared to the uniform-sampled baseline. These properties make VisualClaw a natural fit for edge applications, where the cascade reduces a 1-hour streaming session from ~3,600 API uploads down to only 5-20 calls and the self-evolution makes it a perfect personalized assistant.

[2] SAFE-Cascade: Cost-Adaptive Vision-Language Routing for Chart Question Answering
Vision-language models (VLMs) are powerful for chart question answering, but invoking a VLM for every query can be unnecessarily expensive when many questions are answerable from OCR text and lightweight language reasoning. We demonstrate SAFE-Cascade, an interactive system for cost-adaptive chart question answering. Given a chart image and a natural-language question, SAFE-Cascade first extracts chart text with OCR, obtains a provisional answer from a text-only language model, and then uses a learned router to decide whether to accept the text answer or escalate to a VLM. The demo exposes this decision process to users: OCR evidence, text-only answer, routing probability, escalation decision, final answer, estimated cost, and estimated latency are shown side by side. SAFE-Cascade is designed as a transparent interface for understanding when visual grounding is actually needed. Users can upload or select charts, ask questions, inspect the evidence used by each pathway, compare text-only and VLM answers, and adjust the escalation threshold to explore the accuracy-cost frontier. The system is implemented with Azure Document Intelligence for OCR, gpt-5-mini as the text-only model, gemini-2.5-flash-image as the VLM, and a Random Forest router trained on inference-time features. On a held-out ChartQA test split of 375 examples from a 2,500-example experiment, SAFE-Cascade achieves 69.1% unified accuracy with 73.1% VLM invocation, compared with 67.7% accuracy and 100% VLM invocation for the full-VLM baseline. The observed +1.4 percentage-point difference is statistically uncertain, so we interpret SAFE-Cascade as matching full-VLM performance while reducing VLM calls by 26.9% and estimated cost by 9.3%. The demonstration shows how selective modality routing can make multimodal knowledge systems more transparent, tunable, and cost-aware.

[3] AgentFinVQA: A Deployable Multi-Agent Pipeline for Auditable Financial Chart QA
Financial chart question answering in regulated settings demands more than accuracy: practitioners must know which answers to trust before acting on them, and many institutions cannot send client data to external model providers. Yet existing chart-QA agents are accuracy-focused and opaque, and most assume proprietary API access; to our knowledge, none combines auditability with on-premise deployability without significant accuracy compromise. We present AgentFinVQA, a multi-agent pipeline that decomposes each query into planning, OCR, legend grounding, visual inspection, and verification, recording every step in a traceable Model Evaluation Packet (MEP) per sample. On FinMME, AgentFinVQA improves $+7.68$ pp over a primary-backbone matched zero-shot baseline with a proprietary backbone (Gemini-3 Flash; 71.24% vs. 63.56%, McNemar $p \approx 1.1 \times 10^{-16}$), and $+4.84$ pp with open-weights Qwen3.6-27B-FP8 served locally. The verifier's verdict also serves a

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0066 — gh_18_cited_answer_5

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 95
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments'?

### Claim

The paper 'EvoBrowseComp: An Evolving Benchmark for Evaluating Search Agents' introduces a new benchmark of 800 complex questions synthesized via live-web traversal, requiring broad horizontal search and establishing a scalable paradigm for auto-updatable, high-difficulty benchmarking .

### Evidence

```text
[3] EvoBrowseComp: Benchmarking Search Agents on Evolving Knowledge
Search Agents -- large language models augmented with search tools -- have intensified the need for future-proof evaluation benchmarks. Existing benchmarks such as BrowseComp rely on static knowledge, making them vulnerable to test-set contamination and parametric memorization. Consequently, models can achieve high scores through fact recall rather than genuine retrieval, obscuring true browsing competence via reasoning shortcuts. In this paper, we introduce EvoBrowseComp, an evolving benchmark of 400 English and 400 Chinese contamination-free complex questions synthesized via live-web traversal. To collect these questions, we design a three-agent collaborative framework: (1) a QA synthesis agent that retrieves fresh knowledge from the live web to synthesize QA pairs; (2) an information filtering agent that filters retrieved knowledge in terms of credibility and popularity to block parametric shortcuts; and (3) a high-level guidance agent that formalizes questions into reasoning graphs to reduce logical redundancy and shortcuts in synthesized QA pairs. Because the framework supports fully automated synthesis, EvoBrowseComp can be regularly updated to prevent data contamination and maintain temporal freshness. Extensive experiments confirm its great difficulty, requiring broad horizontal search. It establishes a scalable paradigm for auto-updatable, high-difficulty benchmarking that keeps pace with both evolving world knowledge and advancing agent capabilities.
```

---

## GHR0106 — gh_11_plain_answer_7

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 96
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World'?

### Claim

Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings.

### Evidence

```text
[1] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3.2% for Claude Code (Sonnet 4.6) over no-evolution baselines, with a -9.5% cost reduction compared to the uniform-sampled baseline. These properties make VisualClaw a natural fit for edge applications, where the cascade reduces a 1-hour streaming session from ~3,600 API uploads down to only 5-20 calls and the self-evolution makes it a perfect personalized assistant.

[2] SAFE-Cascade: Cost-Adaptive Vision-Language Routing for Chart Question Answering
Vision-language models (VLMs) are powerful for chart question answering, but invoking a VLM for every query can be unnecessarily expensive when many questions are answerable from OCR text and lightweight language reasoning. We demonstrate SAFE-Cascade, an interactive system for cost-adaptive chart question answering. Given a chart image and a natural-language question, SAFE-Cascade first extracts chart text with OCR, obtains a provisional answer from a text-only language model, and then uses a learned router to decide whether to accept the text answer or escalate to a VLM. The demo exposes this decision process to users: OCR evidence, text-only answer, routing probability, escalation decision, final answer, estimated cost, and estimated latency are shown side by side. SAFE-Cascade is designed as a transparent interface for understanding when visual grounding is actually needed. Users can upload or select charts, ask questions, inspect the evidence used by each pathway, compare text-only and VLM answers, and adjust the escalation threshold to explore the accuracy-cost frontier. The system is implemented with Azure Document Intelligence for OCR, gpt-5-mini as the text-only model, gemini-2.5-flash-image as the VLM, and a Random Forest router trained on inference-time features. On a held-out ChartQA test split of 375 examples from a 2,500-example experiment, SAFE-Cascade achieves 69.1% unified accuracy with 73.1% VLM invocation, compared with 67.7% accuracy and 100% VLM invocation for the full-VLM baseline. The observed +1.4 percentage-point difference is statistically uncertain, so we interpret SAFE-Cascade as matching full-VLM performance while reducing VLM calls by 26.9% and estimated cost by 9.3%. The demonstration shows how selective modality routing can make multimodal knowledge systems more transparent, tunable, and cost-aware.

[3] AgentFinVQA: A Deployable Multi-Agent Pipeline for Auditable Financial Chart QA
Financial chart question answering in regulated settings demands more than accuracy: practitioners must know which answers to trust before acting on them, and many institutions cannot send client data to external model providers. Yet existing chart-QA agents are accuracy-focused and opaque, and most assume proprietary API access; to our knowledge, none combines auditability with on-premise deployability without significant accuracy compromise. We present AgentFinVQA, a multi-agent pipeline that decomposes each query into planning, OCR, legend grounding, visual inspection, and verification, recording every step in a traceable Model Evaluation Packet (MEP) per sample. On FinMME, AgentFinVQA improves $+7.68$ pp over a primary-backbone matched zero-shot baseline with a proprietary backbone (Gemini-3 Flash; 71.24% vs. 63.56%, McNemar $p \approx 1.1 \times 10^{-16}$), and $+4.84$ pp with open-weights Qwen3.6-27B-FP8 served locally. The verifier's verdict also serves a

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0053 — gh_52_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 97
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'NEST: Narrative Event Structures in Time for Long Video Understanding'?

### Claim

Event Trigger Detection (ETD): The performance is below 8%.

### Evidence

```text
[1] NEST: Narrative Event Structures in Time for Long Video Understanding
Recent progress in vision-language models has enabled the processing of increasingly long video sequences, but the ability to handle extended token streams does not translate to understanding of narrative structure in long videos. Existing long video benchmarks focus on needle-in-a-haystack retrieval rather than evaluating how low-level actions form events, how events interact across time, and how narratives progress, for example, whether a model can connect an early setback, such as a job loss to a later relationship breakup, despite long gaps, intervening scenes, or flashbacks that reframe what occurred. We introduce NEST (Narrative Event Structures in Time for Long Video Understanding), a dataset of 1005 full-length movies (avg. 98 minutes), each annotated with 102 multimodal narrative events grounded in visual content, dialogue, and audio. NEST captures multimodal narrative events with structured annotations grounded in visual content, dialogue, and audio, and links them through relations that reflect narrative structure, including temporal ordering, hierarchical composition, and long-range dependencies. We introduce baselines for event trigger detection (ETD), event localization (EL), event argument extraction (EAE), and event relation extraction (ERE). The benchmark is highly challenging for grounded event discovery, with ETD below 8%, EL under 6%, and EAE below 11%. In contrast, ERE is more tractable once events are given, reaching 35.45% F1 zero-shot and 44.42% F1 after fine-tuning.
```

---

## GHR0022 — gh_73_cited_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 98
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

Ablations: The paper compares the performance of their proposed Free-Energy Signatures (Fes) with other attention-spectral baselines such as LapEig and GoR-4.

### Evidence

```text
[1] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.
```

---

## GHR0071 — gh_49_cited_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 99
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation'?

### Claim

Across 12,779 filtered samples, DICE yields lower Evidence Dilution Index (EDI) than the single-vector baseline in 92.8% of cases.

### Evidence

```text
[1] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.

[2] Context Compression Is Not One Thing: Readable Symbolic Re-expression vs. Coherent Summary at Matched Budget
We study context compression for multi-hop question answering with small language models. We propose Telegraph English, a readable symbolic format that rewrites retrieved passages into structured entity-relation statements, preserving reasoning evidence at lower token cost. In controlled experiments on MuSiQue, TwoWiki, and HotpotQA, Telegraph English outperforms three matched-budget compression baselines (character-level deletion, truncation, and random sub-sampling) on every dataset, with gains of 13 to 20 F1 percentage point. It also outperforms a coherent prose summary produced by the same encoder on the hardest dataset. A pre-registered depth-interaction hypothesis is null: the advantage does not grow with reasoning depth within datasets. We interpret these results as evidence that readable symbolic re-expression preserves entity content more densely than either natural language or coherent summarization at matched token budget.

[3] Adaptive Multi-Resolution Procedural Knowledge Compression for Large Language Models
Large language models (LLMs) are widely used to tackle complex tasks with autonomous workflows. Recently, reusable natural language skills have emerged as a popular paradigm to inject procedural knowledge into LLM applications. Since popular skills are often invoked repeatedly, placing their full text in every context significantly increases prefill cost and latency. While text compression techniques have the potential to solve this problem, most existing methods are designed to compress factual knowledge in documents instead of procedural knowledge, making them insufficient for skill compression. In this paper, we argue that an effective skill compression method should: 1) preserve logical dependencies among workflows and tool protocols, 2) enable lightweight, offline compression for frequently updated community skills, and 3) be adaptable to varying complexities across skills. To address this, we present SKIM (SKIll coMpression), an adaptive multi-resolution soft token compression framework for procedural skills. Depending on the complexity of each skill, SKIM creates different numbers of soft tokens that not only improve the efficiency of LLM inference, but also preserve the effectiveness of skill usage. Experiments indicate that SKIM compresses skills to 30 to 60 percent of their original token length while preserving task performance better than existing compression methods.We have released our code at https://github.com/bebr2/SKIM .
```

---

## GHR0128 — gh_99_cited_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 100
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio'?

### Claim

The sources provided discuss limitations and findings related to legal case retrieval systems and agent memory pipelines, but not meta-analysis articles from Nature Portfolio.

### Evidence

```text
[1] Charge as a Construct-Validity Factor in Chinese Legal Case Retrieval: A Cross-Benchmark Audit
Chinese Legal Case Retrieval (LCR) benchmarks grade a reference judgment relevant when its legal characterization matches the query, and strong systems now reach NDCG@10 of 0.85-0.88. Most of the BM25-to-best-trained gap is recoverable with no retrieval model: ranking candidates only by shared primary charge, broken by BM25, closes 99.2% of it on LeCaRDv2 -- with no detectable difference from the best-trained system. This reflects benchmark design: LeCaRDv2 defines top relevance via the crime's key constitutive elements, which encode the charge, so same-charge cases are relevant by construction (relevance lift 4.49; charge-to-relevance macro-AUC 0.871). Holding charge fixed, the trained reranker's advantage over BM25 collapses to a small within-charge residual (+0.026 NDCG@10, cluster-bootstrap CI excluding zero, about a quarter), the only non-definitional positive. The effect is not uniform: the same rule recovers 84.3% on LeCaRDv1 and is out of spec on CAIL2022, with the charge-to-relevance signal weakening in step (macro-AUC 0.871/0.759/0.728); a predicted-charge cascade reproduces 76.6% on LeCaRDv2 but does not transfer. The construct is also cashable at first stage: an exploratory zero-training charge-pool channel lifts LeCaRDv2 recall (R@100 +0.025, wrong-charge controls hurt), reported as a positive control for the confound, not a retrieval method or novelty claim. Charge is thus a high-leverage construct-validity factor at the benchmark level -- not auniform explanation of NDCG@10, and not evidence that any system relies on charge. We package established construct-validity and partial-input checks as a reusable charge-controlled protocol (CCE); on all three benchmarks its triggers come back null or descriptive, behaving as designed. We release the scripts, schema, and protocol so future benchmarks can be screened before their NDCG@10 is read as legal-reasoning ability.

[2] Control-Plane Placement Shapes Forgetting: An Architectural Study of Agent Memory Across Thirteen System Configurations
Where an LLM sits in an agent memory pipeline -- between the recall plane that retrieves stored facts (extensively benchmarked) and the control plane that mutates them via supersede, release, purge (largely untested) -- shapes which forgetting failure modes the system recovers. Comparing thirteen system configurations on a 385-case adversarial surface, we observe three placement regimes with partly complementary coverage: deterministic primitives suffice for lexical/temporal categories but fail canonicalization (5% on identifier-obfuscation, 0% on cross-lingual); inscribe-time LLM recovers canonicalization (100%) but cannot help intent-aware deletion (0% on prefix-collision and compound-fact); a mutation-time hook recovers intent-aware deletion (78-85%) and brightens nearly all categories simultaneously (91.7-93.2% overall, $0.17 per 385-case run, 2.3s/case mutation latency vs. 64-191ms/case deterministic, recall path unchanged). We expose the trade-off via ForgetEval, a 1000-case templated suite plus a 385-case adversarial layer (132 hand-crafted + 253 LLM-drafted oracle-validated) scored by deterministic substring match, paired with a six-method Adapter Protocol with honest N/A scoring that lets heterogeneous memory stores enter in 130 lines. Admission is corroborated by 10-annotator IAA (Fleiss' kappa = 0.958) and a 77-case external-authored subset (four blind contributors) that replicates the canonicalization asymmetry and amplifies the joint-placement lift (+27.8 pt). Production failures are predominantly forgetting failures rather than recall failures, yet existing benchmarks measure only recall. ForgetEval and all adapters are released under MIT.
```

---

## GHR0140 — gh_122_plain_answer_1

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 101
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation'?

### Claim

The paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation' does not appear to be among the sources provided.

### Evidence

```text
[1] When Global Gating Is Enough: Admission-Time Hubness Control in Anisotropic Vector Retrieval Systems
Vector hubness, where a few points become nearest neighbors of many queries, creates a poisoning risk in retrieval-augmented generation (RAG): one injected document can influence unrelated requests. Existing defenses use periodic reverse-kNN scans, leaving an exposure window and repeated corpus-wide work. We study admission-time control, scoring each candidate against sentinel queries and quarantining hub-like documents before insertion. Across two 100,000-document corpora, five encoders, and disjoint attacker and defender query sets, a global gate achieves recall 1.0 at the decisive embedding-space point (>=0.92 across the effective range) and 0.91 +/- 0.07 on HotFlip attacks, with 1% false positives on general documents. A per-topic gate provides no reliable benefit, consistent with anisotropy coupling local and global visibility. Thresholds are maintained incrementally, with corpus-size-independent insertion cost and amortized deletion cost. On HNSW, admission adds about 3.1% to ingestion latency, scoring remains flat to 10^6 vectors, and 1.2% of decisions flip under approximate indexing, none involving attacks. Provenance complements the gate for natural or tight-domain hubs.

[2] When Does Streaming Tool Use Help? Characterizing Tool-Intent Stabilization in Streaming Retrieval-Augmented Generation
Streaming Retrieval-Augmented Generation (Streaming RAG) reduces user-perceived latency by issuing tool queries in parallel with ongoing user input, before the utterance is complete. Reported gains are aggregate, yet the mechanism's benefit is fundamentally query-intrinsic: speculation can only help when the correct tool query becomes determinable before the user stops speaking or typing. We isolate and measure this property -- tool-intent stabilization, the point in the input stream at which a speculative query's retrieval converges to the answer-bearing result. On the CRAG benchmark (1371 validation questions) we (i) measure the distribution of stabilization, (ii) derive a model-agnostic bound H on the portion of tool latency that can be hidden behind the user's remaining input, as a function of tool latency L and input cadence δ, (iii) validate against a working streaming pipeline that realized savings meet or exceed this bound, and (iv) identify which query properties predict early versus late stabilization. The study requires no model training and runs on commodity CPU hardware. We find that at a realistic operating point (L=600ms, δ=3w/s, θ=0.8), 73.9% of queries across the full benchmark admit substantial latency hiding -- a blended figure that mixes sufficiency stabilization on the 21.3% of questions where gold evidence is verbatim-present and BM25-retrievable (95.2% streamable on this favorable slice) with a grounding-free top-1-settling fallback on the remainder. On the favorable slice, φ_suf is bracketed to [0.26, 0.281] by exact and relaxed grounding -- both early. Question type produces a significant but coarse early/late split (Kruskal-Wallis p=0.017, epsilon^2=0.04), directly informing when a learned speculative trigger is worth its cost.
```

---

## GHR0129 — gh_105_cited_answer_1

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 102
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval', and what problem is it designed to address?

### Claim

The paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval' does not appear in the provided sources.

### Evidence

```text
[1] Beyond Parallel Sampling: Diverse Query Initialization for Agentic Search
Test-time scaling for agentic search typically increases depth (i.e., more turns and tokens per trajectory) or breadth (i.e., more parallel rollouts). Here we focus on breadth scaling, showing that standard parallel sampling yields diminishing returns, tracing this to query redundancy at the first turn. When models issue similar first queries across rollouts, the threads retrieve overlapping evidence, and subsequent turns are conditioned on this shared retrieval. We address this limitation with DivInit, a training-free intervention at the first turn. Rather than sampling k independent first queries, DivInit draws n candidates from a single call, picks k < n diverse seeds, and runs them as parallel trajectories. Across five open-weight models and eight benchmarks, DivInit consistently improves over standard parallel sampling, with average gains of five to seven points on multi-hop QA at matched compute. Code available at https://github.com/cxcscmu/diverse-query-initialization

[2] Looped World Models
Current world models face a fundamental tension: faithful long-horizon simulation demands deep computation, but deeper models are expensive to deploy and prone to compounding errors. We resolve this by introducing Looped World Models (LoopWM), which are the first looped architectures for world modelling. Our method iteratively refines latent environment states through a parameter-shared transformer block. This yield up to 100x parameter efficiency over conventional approaches with adaptive computation that automatically scales depth to match the complexity of each prediction step. Orthogonal to scaling model size and training data, LoopWM establishes iterative latent depth as a new scaling axis for world simulation, which might significantly push the community forward.
```

---

## GHR0136 — gh_113_cited_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 103
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World'?

### Claim

I cannot provide the main experimental results or comparisons reported in that paper using the given sources.

### Evidence

```text
[1] SAFE-Cascade: Cost-Adaptive Vision-Language Routing for Chart Question Answering
Vision-language models (VLMs) are powerful for chart question answering, but invoking a VLM for every query can be unnecessarily expensive when many questions are answerable from OCR text and lightweight language reasoning. We demonstrate SAFE-Cascade, an interactive system for cost-adaptive chart question answering. Given a chart image and a natural-language question, SAFE-Cascade first extracts chart text with OCR, obtains a provisional answer from a text-only language model, and then uses a learned router to decide whether to accept the text answer or escalate to a VLM. The demo exposes this decision process to users: OCR evidence, text-only answer, routing probability, escalation decision, final answer, estimated cost, and estimated latency are shown side by side. SAFE-Cascade is designed as a transparent interface for understanding when visual grounding is actually needed. Users can upload or select charts, ask questions, inspect the evidence used by each pathway, compare text-only and VLM answers, and adjust the escalation threshold to explore the accuracy-cost frontier. The system is implemented with Azure Document Intelligence for OCR, gpt-5-mini as the text-only model, gemini-2.5-flash-image as the VLM, and a Random Forest router trained on inference-time features. On a held-out ChartQA test split of 375 examples from a 2,500-example experiment, SAFE-Cascade achieves 69.1% unified accuracy with 73.1% VLM invocation, compared with 67.7% accuracy and 100% VLM invocation for the full-VLM baseline. The observed +1.4 percentage-point difference is statistically uncertain, so we interpret SAFE-Cascade as matching full-VLM performance while reducing VLM calls by 26.9% and estimated cost by 9.3%. The demonstration shows how selective modality routing can make multimodal knowledge systems more transparent, tunable, and cost-aware.

[2] AgentFinVQA: A Deployable Multi-Agent Pipeline for Auditable Financial Chart QA
Financial chart question answering in regulated settings demands more than accuracy: practitioners must know which answers to trust before acting on them, and many institutions cannot send client data to external model providers. Yet existing chart-QA agents are accuracy-focused and opaque, and most assume proprietary API access; to our knowledge, none combines auditability with on-premise deployability without significant accuracy compromise. We present AgentFinVQA, a multi-agent pipeline that decomposes each query into planning, OCR, legend grounding, visual inspection, and verification, recording every step in a traceable Model Evaluation Packet (MEP) per sample. On FinMME, AgentFinVQA improves $+7.68$ pp over a primary-backbone matched zero-shot baseline with a proprietary backbone (Gemini-3 Flash; 71.24% vs. 63.56%, McNemar $p \approx 1.1 \times 10^{-16}$), and $+4.84$ pp with open-weights Qwen3.6-27B-FP8 served locally. The verifier's verdict also serves as a useful confidence signal (68.2% vs. 55.6% exact accuracy on confirmed vs. revised answers), enabling human-in-the-loop review routing. Error analysis shows that question misunderstanding, legend confusion and extraction error account for nearly two-thirds of failures and are the categories least detected by the verifier, identifying clear directions for future work. Together these results show that auditable, on-premise financial chart QA is practical and that the open-weights system keeps most of the accuracy gains while enabling full data residency. We release our code to support reproducible evaluation.
```

---

## GHR0013 — gh_90_cited_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 104
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science'?

### Claim

The paper presents an evaluation of various segments and their combinations across multiple models using an annotated corpus of 1,954 full-text articles from three representative journals in Library and Information Science.

### Evidence

```text
[1] Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science
Research methods are essential carriers of knowledge contribution in academic papers. Automatic multi-label classification of research methods can support knowledge services such as method retrieval, review generation, and research intelligence analysis. While existing studies primarily rely on titles and abstracts, abstracts often provide only limited methodological information, whereas utilizing full-text content faces challenges related to excessive length and information redundancy. Therefore, this paper proposes a segment combination strategy by partitioning the full-text content according to its physical postion. Using an annotated corpus of 1,954 full-text articles from three representative journals in Library and Information Science (JASIST, LISR, and JDoc), we evaluate the classification performance of various segments and their combinations across multiple models. Experimental results indicate that methodological information is distributed unevenly within the full-text content, with the middle-to-late and final segments exhibiting greater discriminative power. Furthermore, integrating bibliographic metadata with cross-segment combination strategies effectively enhances classification performance.
```

---

## GHR0080 — gh_4_cited_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 105
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

The paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models' reports the following main experimental results and comparisons:

### Evidence

```text
[1] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.

[2] Layer-Resolved Optimal Transport for Hallucination Detection in NMT and Abstractive Summarization
Optimal transport (OT) has been shown to detect hallucinations in neural machine translation (NMT) by measuring the geometric distance between cross-attention distributions and a reference distribution, without any supervision. We extend this analysis to all six decoder layers of the Fairseq DE-EN model ($N=3{,}414$), showing that Wass-to-Unif and Wass-to-Data are complementary detectors specialised across hallucination types, that detection is concentrated in layers L1--L4 with L5 anti-predictive for subtler types, and that hallucinated translations lack the exploratory attention phase present in correct translations from the first decoding step. We further evaluate whether the geometric signal transfers to abstractive summarization faithfulness detection: our unsupervised OT detector on AggreFact ($N=1{,}116$) achieves $57.2\%$/$57.6\%$ balanced accuracy on CNN/XSum -- above chance but substantially below supervised MiniCheck-Flan-T5-L($69.9\%$/$74.3\%$). This gap is principled: unlike NMT hallucinations, unfaithful summaries can attend correctly to source tokens while misrepresenting their content, a failure mode invisible to concentration-based OT metrics by construction. Structural experiments on T5-base confirm consistent decoder organisation across depth, with Layer~3 showing peak concentration and Layer~12 being most critical for generation quality. Together, the results establish OT on cross-attention as a reliable detector when the failure mode is source disengagement, a principled interpretability tool regardless of task, and fundamentally limited when faithfulness failures occur downstream of attention.

[3] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.
```

---

## GHR0035 — gh_68_cited_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 106
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

The paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models' reports the following main experimental results and comparisons:

### Evidence

```text
[1] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.
```

---

## GHR0057 — gh_70_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 107
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation'?

### Claim

Specifically, it mentions that static rules tend to unnecessarily disrupt accurate generations, while leaving multi-modal reasoning unguided allows existing mismatches to cascade into severe logical fabrications.

### Evidence

```text
[1] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.
```

---

## GHR0027 — gh_91_cited_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 108
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'REVES: REvision and VErification--Augmented Training for Test-Time Scaling'?

### Claim

Math results under ground-truth verification further confirm improved correction ability.

### Evidence

```text
[1] REVES: REvision and VErification--Augmented Training for Test-Time Scaling
Test-time scaling via sequential revision has emerged as a powerful paradigm for enhancing Large Language Model (LLM) reasoning. However, standard post-training methods primarily optimize single-shot objectives, creating a fundamental misalignment with multi-step inference dynamics. While recent work treats this as multi-turn reinforcement learning (RL), conventional approaches optimize over the multi-step trajectories directly, failing to further exploit the high-quality mistakes in intermediate steps that model can learn from correcting them. We propose a two-stage iterative framework that alternates between online data/prompt augmentation and policy optimization. By converting the intermediate steps (``near-miss'' answers) in the successful recovery trajectories into decoupled revision and verification prompts, our approach concentrates training on both effective answer transformation and error identification. This approach enables efficient off-policy data generation and reduces the computational overhead of long-horizon sampling compared to standard multi-turn RL. On LiveCodeBench, using publicly available test cases as feedback, we observe gains of +6.5 points over the RL baseline and +4.0 points over standard multi-turn training. Beyond coding, our approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems. Math results under ground-truth verification further confirm improved correction ability. It also generalizes to out-of-distribution constraint-satisfaction puzzles such as n\_queens and mini\_sudoku, where correctness is defined entirely by problem constraints. Code is available at https://github.com/yxliu02/REVES.git.
```

---

## GHR0145 — gh_122_plain_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 109
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation'?

### Claim

I cannot find any information about the datasets, benchmarks, or evaluation settings described in that specific paper using the sources provided.

### Evidence

```text
[1] When Global Gating Is Enough: Admission-Time Hubness Control in Anisotropic Vector Retrieval Systems
Vector hubness, where a few points become nearest neighbors of many queries, creates a poisoning risk in retrieval-augmented generation (RAG): one injected document can influence unrelated requests. Existing defenses use periodic reverse-kNN scans, leaving an exposure window and repeated corpus-wide work. We study admission-time control, scoring each candidate against sentinel queries and quarantining hub-like documents before insertion. Across two 100,000-document corpora, five encoders, and disjoint attacker and defender query sets, a global gate achieves recall 1.0 at the decisive embedding-space point (>=0.92 across the effective range) and 0.91 +/- 0.07 on HotFlip attacks, with 1% false positives on general documents. A per-topic gate provides no reliable benefit, consistent with anisotropy coupling local and global visibility. Thresholds are maintained incrementally, with corpus-size-independent insertion cost and amortized deletion cost. On HNSW, admission adds about 3.1% to ingestion latency, scoring remains flat to 10^6 vectors, and 1.2% of decisions flip under approximate indexing, none involving attacks. Provenance complements the gate for natural or tight-domain hubs.

[2] When Does Streaming Tool Use Help? Characterizing Tool-Intent Stabilization in Streaming Retrieval-Augmented Generation
Streaming Retrieval-Augmented Generation (Streaming RAG) reduces user-perceived latency by issuing tool queries in parallel with ongoing user input, before the utterance is complete. Reported gains are aggregate, yet the mechanism's benefit is fundamentally query-intrinsic: speculation can only help when the correct tool query becomes determinable before the user stops speaking or typing. We isolate and measure this property -- tool-intent stabilization, the point in the input stream at which a speculative query's retrieval converges to the answer-bearing result. On the CRAG benchmark (1371 validation questions) we (i) measure the distribution of stabilization, (ii) derive a model-agnostic bound H on the portion of tool latency that can be hidden behind the user's remaining input, as a function of tool latency L and input cadence δ, (iii) validate against a working streaming pipeline that realized savings meet or exceed this bound, and (iv) identify which query properties predict early versus late stabilization. The study requires no model training and runs on commodity CPU hardware. We find that at a realistic operating point (L=600ms, δ=3w/s, θ=0.8), 73.9% of queries across the full benchmark admit substantial latency hiding -- a blended figure that mixes sufficiency stabilization on the 21.3% of questions where gold evidence is verbatim-present and BM25-retrievable (95.2% streamable on this favorable slice) with a grounding-free top-1-settling fallback on the remainder. On the favorable slice, φ_suf is bracketed to [0.26, 0.281] by exact and relaxed grounding -- both early. Question type produces a significant but coarse early/late split (Kruskal-Wallis p=0.017, epsilon^2=0.04), directly informing when a learned speculative trigger is worth its cost.
```

---

## GHR0063 — gh_75_plain_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 110
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice', and what problem is it designed to address?

### Claim

HistoRAG aims to translate historiographical principles into concrete architectural interventions, such as decoupling source discovery from interpretation, enforcing balanced source representation across the research period, and making relevance judgments transparent and contestable.

### Evidence

```text
[1] HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice
Retrieval-Augmented Generation (RAG) is the prevailing architecture for grounding language model outputs in external evidence, yet its dominant evaluation paradigms and default configurations remain oriented toward factual question-answering. For interpretive disciplines such as historical studies, RAG embeds assumptions that conflict with scholarly practice. We introduce HistoRAG, a framework that translates historiographical principles into concrete architectural interventions. Separated retrieval and generation decouples source discovery from interpretation, temporal windowing enforces balanced source representation across the research period as a methodological requirement of historical inquiry, and LLM-as-judge evaluation makes relevance judgments transparent and contestable. We evaluate these interventions using SPIEGELragged, applied to 102,189 articles from Der Spiegel (1950-1979). Each intervention addresses a measurable deficiency in standard RAG: era-specific vocabulary retrieves zero chunks from the 1950s when using 1970s terminology, evidence of the temporal skew that motivates windowing; vector similarity and LLM-assessed relevance correlate only weakly (Spearman rho = 0.275), motivating post-retrieval evaluation; and keyword-based and semantic retrieval surface largely disjoint source pools, motivating an architecture in which both operate as complementary retrieval layers under a shared LLM evaluation filter. We also introduce the concept of Zwischentexte (intermediate texts that function as interpretive proposals rather than findings) as a framework for responsible integration of LLM-generated text into scholarly practice. The architecture offers a model for how domain-specific epistemological commitments can be translated into RAG design decisions, and may transfer to other interpretive disciplines working with large corpora.
```

---

## GHR0056 — gh_61_plain_answer_6

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 111
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval'?

### Claim

specific ablations or analysis findings are not explicitly mentioned in the provided source.

### Evidence

```text
[1] LARE: Low-Attention Region Encoding for Text-Image Retrieval
Image retrieval in crowded scenes is particularly challenging due to the salience bias of conventional visual encoders, which tend to focus on dominant objects while neglecting low-attention regions that are often crucial for fine-grained retrieval. We propose LARE (Low-Attention Region Encoding), a framework that explicitly models these overlooked regions. LARE adopts a dual-encoding strategy that encodes low-attention regions of an image and the full image in parallel, leading to more diverse and informative image embeddings. To evaluate image retrieval performance in challenging crowded scenes, we introduce Dense-Set, a challenging subset derived from COCO and Flickr30K. In this subset, images are re-captioned to provide richer descriptions of low-attention or previously overlooked regions. This dataset highlights the limitations of existing retrieval models and enables a more rigorous evaluation under densely crowded scene conditions. Experimental results demonstrate that the proposed framework improves retrieval performance by preserving subtle, non-dominant visual cues within the shared latent space.
```

---

## GHR0025 — gh_61_cited_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 112
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval'?

### Claim

The experimental results demonstrate that the proposed framework improves retrieval performance by preserving subtle, non-dominant visual cues within the shared latent space .

### Evidence

```text
[1] LARE: Low-Attention Region Encoding for Text-Image Retrieval
Image retrieval in crowded scenes is particularly challenging due to the salience bias of conventional visual encoders, which tend to focus on dominant objects while neglecting low-attention regions that are often crucial for fine-grained retrieval. We propose LARE (Low-Attention Region Encoding), a framework that explicitly models these overlooked regions. LARE adopts a dual-encoding strategy that encodes low-attention regions of an image and the full image in parallel, leading to more diverse and informative image embeddings. To evaluate image retrieval performance in challenging crowded scenes, we introduce Dense-Set, a challenging subset derived from COCO and Flickr30K. In this subset, images are re-captioned to provide richer descriptions of low-attention or previously overlooked regions. This dataset highlights the limitations of existing retrieval models and enables a more rigorous evaluation under densely crowded scene conditions. Experimental results demonstrate that the proposed framework improves retrieval performance by preserving subtle, non-dominant visual cues within the shared latent space.
```

---

## GHR0050 — gh_63_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 113
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation', and what problem is it designed to address?

### Claim

It is designed to address the problem of cross-modal hallucinations, causal fabrications, and sycophancy in Large Vision-Language Models.

### Evidence

```text
[1] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.
```

---

## GHR0133 — gh_147_cited_answer_1

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 114
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents'?

### Claim

The paper 'CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents' is not among the provided sources, so I cannot provide the main experimental results or comparisons from that specific paper.

### Evidence

```text
[1] Learning to Reason by Analogy via Retrieval-Augmented Reinforcement Fine-Tuning
Retrieval-augmented generation (RAG) has become a standard mechanism for grounding language models in external knowledge, yet conventional retrieval based on lexical or semantic similarity is poorly suited for complex reasoning tasks: a semantically similar problem may demand an entirely different solution strategy, while a superficially different problem may share the same underlying reasoning pattern. We propose Retrieval-Augmented Reinforcement Fine-Tuning (RA-RFT), a post-training framework that teaches language models to reason by analogy. RA-RFT uses gold-relevance distillation to train a retriever that ranks contexts by expected reasoning benefit rather than semantic overlap, and then fine-tunes the policy model via reinforcement fine-tuning methods with retrieved analogous demonstrations, so the model learns to leverage reasoning traces under verifiable outcome rewards. We further analyze the diversity of retrieved contexts and find that reasoning-aware retrieval surfaces complementary solution strategies that provide distinct reasoning scaffolds for individual problems. Across challenging mathematical reasoning benchmarks, RA-RFT consistently outperforms standard reinforcement fine-tuning methods. For example, it improves AIME 2025 average@32 accuracy by 7.1 and 2.8 points over GRPO for Qwen3-1.7B and Qwen3-4B respectively -- suggesting that reasoning-aware retrieval is a complementary axis of improvement and orthogonal to advances in reward design or training curricula.

[2] MCompassRAG: Topic Metadata as a Semantic Compass for Paragraph-Level Retrieval
Retrieval-augmented generation (RAG) systems depend critically on how documents are chunked and searched. Fine-grained chunks can improve retrieval precision but expand the search space, increasing latency and cost; larger chunks reduce the number of candidates but make dense similarity less reliable, as the representation for each chunk mixes multiple topics and introduces more semantic noise. This trade-off becomes especially limiting in deep research tasks, where retrieval must be both fast and precise across large, heterogeneous corpora. We introduce MCompassRAG, a metadata-guided retrieval framework that uses topic-level signals as a semantic compass for selecting relevant evidence. Instead of relying only on cosine similarity between queries and noisy chunk embeddings, MCompassRAG enriches chunk representations with topic metadata in the same embedding space and trains a lightweight retriever through LLM-teacher distillation. At inference time, MCompassRAG performs topic-aware retrieval without additional LLM calls, improving both efficiency and evidence quality. Across six complex retrieval benchmarks, MCompassRAG improves information efficiency (IE) by 8.24% on average with over 5 times lower latency than the strongest efficient RAG baselines. Code is available on https://github.com/AmirAbaskohi/MCompassRAG.
```

---

## GHR0047 — gh_57_plain_answer_1

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 115
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems'?

### Claim

The main experimental result reported in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems' is an improvement in the overall response pass rate.

### Evidence

```text
[1] EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems
In large-scale enterprise settings, centralized multi-agent systems (MAS) are increasingly adopted, in which a coordinator delegates user requests to lightweight, domain-specialized sub-agents. While this architecture improves modularity, scalability, and cost efficiency, its reliability depends not only on accurate routing but also on sub-agents' ability to calibrate their responses to capability constraints. In particular, sub-agents built on smaller fine-tuned models often struggle with such calibration, leading them to over-answer ambiguous, underspecified, misrouted, or unsupported requests and produce hallucinated outputs instead of actionable feedback. To address this challenge, we present EARS (Explanatory Abstention for Reliable Sub-Agent Modeling), a production-oriented framework that reframes sub-agent abstention as an inter-agent communication protocol: a sub-agent does not merely abstain, but exposes an actionable failure state to the coordinator. EARS curates human-agent interaction data using an ensemble of calibrated LLM-as-a-Judge models, producing structured abstention labels and rationales under a taxonomy of sub-agent failure modes. These data are used to fine-tune sub-agents to detect failure conditions and return rationales for coordinator-level clarification, rerouting, or fallback. We evaluate EARS in a large-scale production e-commerce assistant supporting enterprise business intelligence workflows. EARS improves the overall response pass rate from 68.5% to 78.9%, demonstrating that sub-agent-side explanatory abstention improves MAS reliability.
```

---

## GHR0091 — gh_15_cited_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 116
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems'?

### Claim

To address this challenge, the paper presents EARS, a framework that reframes sub-agent abstention as an inter-agent communication protocol, allowing a sub-agent to expose an actionable failure state to the coordinator .

### Evidence

```text
[1] EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems
In large-scale enterprise settings, centralized multi-agent systems (MAS) are increasingly adopted, in which a coordinator delegates user requests to lightweight, domain-specialized sub-agents. While this architecture improves modularity, scalability, and cost efficiency, its reliability depends not only on accurate routing but also on sub-agents' ability to calibrate their responses to capability constraints. In particular, sub-agents built on smaller fine-tuned models often struggle with such calibration, leading them to over-answer ambiguous, underspecified, misrouted, or unsupported requests and produce hallucinated outputs instead of actionable feedback. To address this challenge, we present EARS (Explanatory Abstention for Reliable Sub-Agent Modeling), a production-oriented framework that reframes sub-agent abstention as an inter-agent communication protocol: a sub-agent does not merely abstain, but exposes an actionable failure state to the coordinator. EARS curates human-agent interaction data using an ensemble of calibrated LLM-as-a-Judge models, producing structured abstention labels and rationales under a taxonomy of sub-agent failure modes. These data are used to fine-tune sub-agents to detect failure conditions and return rationales for coordinator-level clarification, rerouting, or fallback. We evaluate EARS in a large-scale production e-commerce assistant supporting enterprise business intelligence workflows. EARS improves the overall response pass rate from 68.5% to 78.9%, demonstrating that sub-agent-side explanatory abstention improves MAS reliability.
```

---

## GHR0112 — gh_13_plain_answer_6

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 117
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'?

### Claim

SAMA's Anchor-Preserving Diffusion mechanism maintains critical semantic anchors while diversifying visual contexts for image synthesis.

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.

[2] Stellar: Scalable Multimodal Document Retrieval for Natural Language Queries
Multimodal document retrieval--selecting the most relevant multimodal document from a large corpus to answer a natural language query--plays an essential role in Retrieval-Augmented Generation (RAG) systems. State-of-the-art methods represent each document and query with multiple token-level embeddings and use late interaction to achieve high effectiveness. However, such multi-vector representations incur substantial memory overhead during retrieval, leading to poor scalability and hindering real-world deployment. In this paper, we present Stellar, a scalable multimodal document retrieval framework that stores token-level document embeddings on disk and loads only a small set of candidate embeddings into memory for late interaction. Stellar comprises two key components: (i) Lexical Representation-based Filtering (LRF), which fine-tunes a Multimodal Large Language Model (MLLM) as a sparse encoder to produce high-quality lexical representations, enabling efficient and effective document filtering to significantly reduce the candidate set; (ii) Efficient Disk-backed Late Interaction (DLI), which designs an on-disk token embedding storage layout guided by a balanced clustering algorithm, and dynamically loads only the necessary token embeddings into memory using a simple yet effective cost model. Extensive experiments on four real-world benchmarks and a newly presented large-scale dataset demonstrate that Stellar reduces memory overhead and query latency by 1-2 orders of magnitude compared to existing methods without compromising retrieval effectiveness.

[3] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0004 — gh_155_cited_answer_1

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 118
- sampling_stratum: `drop_home_related::cited_answer`
- sampling_weight: `4.166666666666667`
- hard_policy: `drop_home_related`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio', and what problem is it designed to address?

### Claim

The paper 'Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio' does not provide information on a method, system, or framework being introduced.

### Evidence

```text
[1] LAUKIN: A Multi-jurisdictional Common Law Contract Dataset
Multinational companies increasingly require cross-jurisdictional contract review, yet existing legal NLP datasets are largely restricted to a single jurisdiction. We introduce LAUKIN (Legal equivalence dataset of Australia, UK, and INdia), a dataset of clause pairs (AU-UK, UK-IN, IN-AU) labelled for boolean legal equivalence. We develop a novel multi-stage retrieval and reranking pipeline to construct the initial clause pair mapping, with a subset of clause pairs subsequently annotated by legal experts as Equivalent or Not Equivalent. The dataset comprises 14,727 clause pairs from 204 contracts across 8 agreement types, of which 3,000 are manually labelled: 900 train, 600 dev, and 1,500 test. We evaluate 12 models across 4 techniques, achieving a best macro-F1 of 65.11%, establishing LAUKIN as a challenging benchmark. Results reveal that, despite shared legal heritage, drafting conventions diverge significantly across jurisdictions, making cross-jurisdictional equivalence classification non-trivial. LAUKIN also includes 11,727 unlabelled training pairs to support future semi-supervised learning research in legal NLP.

[2] Query-aware Routing for Filtered Approximate Nearest Neighbors Search
Filtered ANN search, which combines vector similarity with attribute predicates, is a core primitive in modern vector databases and retrieval-augmented generation. We benchmark all major categorical filtered ANN methods across multiple datasets under three predicates and find that no single method dominates. Moreover, even within a single dataset and predicate type, the best method for a query can vary. Therefore, we propose a query-aware routing framework. A lightweight ML model predicts each candidate method's recall on the query, and the router consults an offline benchmark table that maps every method and parameter setting to its measured recall and QPS, then selects the method with the best recall--QPS trade-off. Our ablation study narrows 22 candidate features to a minimal set of three and we adopt regression rather than classification as the prediction target to sharpen accuracy. Our model is trained on six real-world datasets and applied to five unseen validation datasets. The final result shows that our router achieves state-of-the-art recall and QPS balance across all five validation datasets compared to existing filtered ANN baselines, while incurring negligible latency overhead.
```

---

## GHR0054 — gh_56_plain_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 119
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'?

### Claim

It presents findings from extensive experiments across benchmark datasets for Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE), demonstrating that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings.

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.
```

---

## GHR0045 — gh_70_plain_answer_6

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 120
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation'?

### Claim

The evaluation of the system is based on extensive experiments that indicate that the proposed system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.

### Evidence

```text
[1] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.
```

---

## GHR0131 — gh_135_cited_answer_3

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 121
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science'?

### Claim

They do not cover the paper titled 'Which Sections of a Research Paper Best Reveal Its Research Methods?

### Evidence

```text
[1] How Fine-Grained Should a RAG Benchmark Be? A Hierarchical Framework for Synthetic Question Generation
Evaluating retrieval-augmented generation (RAG) systems requires benchmarks that capture diverse question characteristics, yet practitioners lack empirical guidance on which dimensions to vary and at what granularity. We present HieraRAG, a hierarchical framework for studying granularity in RAG benchmark construction, defining optimal granularity as the level that maximizes discriminative power (the standard deviation of generation quality across categories) within a given RAG configuration. As a case study, we generate 5,872 synthetic question-answer (QA) pairs from FineWeb-10BT across 3 dimensions (Question Complexity, Answer Type, Linguistic Variation) at 3 granularity levels (2, 4, and 8 categories). With a BM25+Falcon-3-10B pipeline, optimal granularity varies by dimension: complexity benefits from fine-grained distinctions (discriminative power: 0.053) while answer type and linguistic variation peak at medium granularity. We introduce a Coherence Ratio metric to quantify whether fine-grained splits cleanly subdivide parent categories, revealing structural differences across dimensions (Question Complexity: 0.40 vs. Answer Type: 1.44). Human evaluation of 110 stratified QA pairs confirms synthetic quality. While these specific findings reflect a single configuration, HieraRAG provides a portable procedure and validation metric for practitioners to determine evaluation granularity within their own RAG settings.

[2] LectūraAgents: A Multi-Agent Framework for Adaptive Personalized AI-Assisted Learning and Embodied Teaching
Effective personalized AI-assisted learning demands systems that can not only generate accurate learner-specific educational materials, but also dynamically adapt their instruction to diverse learners. However, existing educational agents have primarily focused on lecture content automation and simulations, which often fall short of modelling multimodal and embodied instructional methods tailored for the individual learner. To this end, we propose LectūraAgents - a multi-agent framework that enables personalized learning through end-to-end adaptive embodied teaching. At its core, LectūraAgents mirrors a professor-student relationship, in which a ProfessorAgent leads a collaborative team of specialized subordinate agents through research, planning, review, and embodied delivery of lecture contents that adapt to a learner's needs. The framework offers three main contributions: (1) a hierarchical multi-agent architecture for end-to-end personalized learning; (2) an adaptive embodied teaching mechanism, wherein the ProfessorAgent executes visible and pedagogically motivated teaching actions (e.g., handwrite, highlight, underline, etc.) over contents in a teaching environment; and (3) a Teaching Action-Speech Alignment (TASA) algorithm that employs salience-based heuristics and temporal semantic segmentation to generate coherent teaching action sequences aligned with learner profiles. We evaluate LectūraAgents on diverse courses at high school, undergraduate, and graduate levels using sample-specific rubric-based analysis; with generated lecture materials and teaching actions assessed and validated by expert educators. Experimental results show consistent gains in lecture content quality, embodied teaching quality, assessment, and personalization over existing approaches, positioning LectūraAgents as a pedagogically well-grounded framework for personalized learning at scale.
```

---

## GHR0010 — gh_149_plain_answer_1

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 122
- sampling_stratum: `drop_home_related::plain_answer`
- sampling_weight: `4.333333333333333`
- hard_policy: `drop_home_related`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents'?

### Claim

The paper 'CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents' is not among the sources provided.

### Evidence

```text
[1] Learning to Reason by Analogy via Retrieval-Augmented Reinforcement Fine-Tuning
Retrieval-augmented generation (RAG) has become a standard mechanism for grounding language models in external knowledge, yet conventional retrieval based on lexical or semantic similarity is poorly suited for complex reasoning tasks: a semantically similar problem may demand an entirely different solution strategy, while a superficially different problem may share the same underlying reasoning pattern. We propose Retrieval-Augmented Reinforcement Fine-Tuning (RA-RFT), a post-training framework that teaches language models to reason by analogy. RA-RFT uses gold-relevance distillation to train a retriever that ranks contexts by expected reasoning benefit rather than semantic overlap, and then fine-tunes the policy model via reinforcement fine-tuning methods with retrieved analogous demonstrations, so the model learns to leverage reasoning traces under verifiable outcome rewards. We further analyze the diversity of retrieved contexts and find that reasoning-aware retrieval surfaces complementary solution strategies that provide distinct reasoning scaffolds for individual problems. Across challenging mathematical reasoning benchmarks, RA-RFT consistently outperforms standard reinforcement fine-tuning methods. For example, it improves AIME 2025 average@32 accuracy by 7.1 and 2.8 points over GRPO for Qwen3-1.7B and Qwen3-4B respectively -- suggesting that reasoning-aware retrieval is a complementary axis of improvement and orthogonal to advances in reward design or training curricula.

[2] MCompassRAG: Topic Metadata as a Semantic Compass for Paragraph-Level Retrieval
Retrieval-augmented generation (RAG) systems depend critically on how documents are chunked and searched. Fine-grained chunks can improve retrieval precision but expand the search space, increasing latency and cost; larger chunks reduce the number of candidates but make dense similarity less reliable, as the representation for each chunk mixes multiple topics and introduces more semantic noise. This trade-off becomes especially limiting in deep research tasks, where retrieval must be both fast and precise across large, heterogeneous corpora. We introduce MCompassRAG, a metadata-guided retrieval framework that uses topic-level signals as a semantic compass for selecting relevant evidence. Instead of relying only on cosine similarity between queries and noisy chunk embeddings, MCompassRAG enriches chunk representations with topic metadata in the same embedding space and trains a lightweight retriever through LLM-teacher distillation. At inference time, MCompassRAG performs topic-aware retrieval without additional LLM calls, improving both efficiency and evidence quality. Across six complex retrieval benchmarks, MCompassRAG improves information efficiency (IE) by 8.24% on average with over 5 times lower latency than the strongest efficient RAG baselines. Code is available on https://github.com/AmirAbaskohi/MCompassRAG.
```

---

## GHR0049 — gh_81_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 123
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice'?

### Claim

The paper also introduces the concept of LLM-as-judge evaluation for making relevance judgments transparent and contestable.

### Evidence

```text
[1] HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice
Retrieval-Augmented Generation (RAG) is the prevailing architecture for grounding language model outputs in external evidence, yet its dominant evaluation paradigms and default configurations remain oriented toward factual question-answering. For interpretive disciplines such as historical studies, RAG embeds assumptions that conflict with scholarly practice. We introduce HistoRAG, a framework that translates historiographical principles into concrete architectural interventions. Separated retrieval and generation decouples source discovery from interpretation, temporal windowing enforces balanced source representation across the research period as a methodological requirement of historical inquiry, and LLM-as-judge evaluation makes relevance judgments transparent and contestable. We evaluate these interventions using SPIEGELragged, applied to 102,189 articles from Der Spiegel (1950-1979). Each intervention addresses a measurable deficiency in standard RAG: era-specific vocabulary retrieves zero chunks from the 1950s when using 1970s terminology, evidence of the temporal skew that motivates windowing; vector similarity and LLM-assessed relevance correlate only weakly (Spearman rho = 0.275), motivating post-retrieval evaluation; and keyword-based and semantic retrieval surface largely disjoint source pools, motivating an architecture in which both operate as complementary retrieval layers under a shared LLM evaluation filter. We also introduce the concept of Zwischentexte (intermediate texts that function as interpretive proposals rather than findings) as a framework for responsible integration of LLM-generated text into scholarly practice. The architecture offers a model for how domain-specific epistemological commitments can be translated into RAG design decisions, and may transfer to other interpretive disciplines working with large corpora.
```

---

## GHR0062 — gh_62_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 124
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents'?

### Claim

The authors introduce DeepRubric, a data construction framework that aims to provide more reliable query--rubric supervision for deep research agents.

### Evidence

```text
[1] DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents
Deep research agents synthesize long-form reports by searching and reasoning over retrieved evidence. Reinforcement learning with rubric-based rewards improves these agents by optimizing them against checkable criteria that translate report quality into reward signals, but its efficiency depends on whether those criteria reliably capture the task scope and evidence needs. Most existing studies ask an LLM to generate rubrics for a given query, but when the model fails to infer the underlying information needs, the generated rubrics may be incomplete and reduce RL efficiency. To obtain more reliable query--rubric supervision, we introduce DeepRubric, a data construction framework that reverses this process: instead of inferring evaluation criteria for a given query, it first determines what an evidence-backed report should be evaluated on and then synthesizes aligned query--rubric pairs from those evaluation targets. Starting from a sampled seed topic, DeepRubric builds an evidence tree by recursively expanding evidence-backed sub-questions, whose leaves serve as atomic and verifiable evaluation targets. It then uses the evidence tree to synthesize the training query and rubrics, ensuring that the reward evaluates exactly the information requested by the query. Using DeepRubric, we construct 9K query--rubric supervision examples and train DeepRubric-8B with rubric-based GRPO, achieving comparable performance to prior open state-of-the-art deep research models across three benchmarks with roughly 13x fewer RL GPU-hours.
```

---

## GHR0031 — gh_77_cited_answer_4

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 125
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments'?

### Claim

Analysis Findings: The benchmark provides multi-dimensional evaluation signals for academic paper search agents, including search efficiency, intent-level robustness, and failure cases .

### Evidence

```text
[1] ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments
Academic paper search is a core step in scientific research, and LLM-based search agents are emerging as a promising paradigm for iterative, intent-driven literature exploration. However, existing benchmarks are insufficient for systematically evaluating agentic academic search under realistic open literature environments. We propose ScholarQuest, a large-scale, taxonomy-guided benchmark for agentic academic paper search. ScholarQuest is constructed from over 1,000 computer science topics and four representative research intents, including method-oriented, setting-anchored, comparison-based, and scope-controlled queries. It further provides scalable answer construction and a shared retrieval backend ScholarBase for reproducible evaluation. Benchmarking results show that agentic methods outperform single-shot retrieval baselines, yet the best-performing agent only achieves 0.314 Recall@100 and 0.355 Recall@All, indicating substantial room for improvement. In addition, analyses of search efficiency, intent-level robustness, and failure cases further highlight the benchmark's ability to provide multi-dimensional evaluation signals for academic paper search agents.
```

---

## GHR0023 — gh_88_cited_answer_1

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 126
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction'?

### Claim

The paper 'SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction' describes experiments across benchmark datasets for Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE) .

### Evidence

```text
[1] SAMA: Semantic Anchor-aligned Augmentation for Unified Low-Resource Multimodal Information Extraction
Multimodal Information Extraction (MIE)-covering tasks such as Multimodal Named Entity Recognition (MNER), Relation Extraction (MRE), and Event Extraction (MEE)-is essential for understanding multimedia content but remains constrained by severe data scarcity. Although data augmentation is a promising remedy, existing approaches are impeded by coarse cross-modal alignment and fragmented, task-specific designs that fail to exploit shared semantic knowledge. To overcome these limitations, we introduce Semantic Anchor-aligned Multimodal Augmentation (SAMA), a unified framework for generating high-fidelity, task-aware synthetic data. SAMA constructs structured semantic anchors from ground-truth labels to guide a Collaborative Multi-Experts Multimodal Large Language Model (CME-MLLM), which integrates a Universal Adapter for shared semantics with Task-Specific Adapters to produce diverse yet constraint-compliant textual samples. For image synthesis, SAMA employs an Anchor-Preserving Diffusion mechanism that uses anchor-weighted prompts and latent conditioning to maintain critical semantic anchors while diversifying visual contexts. To eliminate the need for manual verification, SAMA further introduces a Dual-Constraint Filtering module that selects synthetic samples based on both cross-modal consistency and anchor fidelity. Extensive experiments across benchmark datasets for MNER, MRE, and MEE demonstrate that SAMA consistently outperforms state-of-the-art augmentation baselines under both fully supervised and low-resource settings, underscoring its versatility, robustness, and effectiveness.
```

---

## GHR0109 — gh_23_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 127
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems', and what problem is it designed to address?

### Claim

This system is designed to address the problem of vector-search in edge and offline AI settings where server infrastructure, network connectivity, and training data are unavailable.

### Evidence

```text
[1] MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems
We present MonaVec, a deterministic, embedded vector-search kernel for edge and offline AI -- settings where server infrastructure, network connectivity, and training data are all unavailable. Existing vector-search systems assume a persistent server, gigabytes of RAM, or a training pass over the corpus; MonaVec instead targets the deployment profile of SQLite: one file, one function call, runs anywhere. Its quantization core is training-free by default and data-oblivious: a Randomized Hadamard Transform (RHDH) conditions any input distribution toward N(0,1), so precomputed Lloyd-Max tables quantize to 4 bits (8x smaller) with no learned codebook and no data pass. The index persists as a single .mvec file whose embedded ChaCha20 rotation seed makes results reproducible across architectures and byte-identical within a build -- a determinism guarantee that parallel-build graph libraries cannot offer. On semantic embeddings (AG News, 45K x 1024-dim BGE-M3, cosine), MonaVec 4-bit BruteForce reaches 0.960 Recall@10 in 27 MB -- leading float32 FAISS-IVF and 8-bit usearch on recall -- while trading peak throughput for byte-identical determinism. A single-pass global standardization (fit()) extends the same data-oblivious pipeline to magnitude-sensitive L2 data, and optional IvfFlat and HNSW backends carry it to million-vector corpora. MonaVec is implemented in pure Rust with Python bindings and runtime SIMD dispatch (AVX-512/AVX2/NEON/scalar). It targets on-device RAG, offline agents, and embedded retrieval -- the niche SQLite occupies for relational data: one file, one call, runs anywhere.

[2] SCAR: Semantic Continuity-Aware Retrieval for Efficient Context Expansion in RAG
Fixed-length chunking in Retrieval-Augmented Generation (RAG) often leads to boundary fragmentation, where critical evidence is split across segments, degrading retrieval recall. While static windowing and parent retrieval improve recall, they introduce significant token overhead. We propose SCAR (Semantic Continuity-Aware Retrieval), an adaptive retrieval policy that selectively expands neighboring chunks by weighing query-neighbor relevance against a structural continuity penalty. SCAR uses a relative expansion threshold tied to each retrieved chunk's own query-relevance, yielding an approximately scale-invariant decision rule that transfers across embedding models without recalibration. Across four diverse corpora (RFC, GDPR, a 10-K report, and a Merger agreement; N=320 queries; 160 boundary-fragmented), SCAR achieves 92.8% recall on boundary-fragmented queries with only 7.84 chunks, a 22.9% reduction compared to static windowing (10.16 chunks). Paired bootstrap tests (B=10,000) confirm the chunk reduction is highly significant (p<0.0001, Cohen's d=-1.49, large effect), with a small recall difference (Cohen's d=-0.33). The policy transfers across three embedding models (text-embedding-3-large, BGE-large-en-v1.5, zembed-1) using the same single hyperparameter setting, and downstream RAGAS evaluation on the 10-K corpus confirms SCAR preserves generation faithfulness while reducing context tokens by 27.1%.

[3] Charge as a Construct-Validity Factor in Chinese Legal Case Retrieval: A Cross-Benchmark Audit
Chinese Legal Case Retrieval (LCR) benchmarks grade a reference judgment relevant when its legal characterization matches the query, and strong systems now reach NDCG@10 of 0.85-0.88. Most of the BM25-to-best-trained gap is recoverable with no retrieval model: ranking candidates only by shared primary charge, broken by BM25, closes 99.2% of it on LeCaRDv2 -- with no detectable difference from the best-trained system. This reflects benchmark design: LeCaRDv2 defines top relevance via the crime's key constitutive elements, which encode the charge, so same-charge cases are relevant by construction (relevance lift 4.49; charge-to-relevance macro-AUC 0.871). Holding charge fixed, the trained reranker's advantage over BM25 collapses to a small within-charge residual (+0.026 NDCG@10, cluster-bootstrap CI excluding zero, about a quarter), the only non-definitional positive. The effect is not uniform: the same rule recovers 84.3% on LeCaRDv1 and is out of spec on CAIL2022, with the charge-to-relevance signal weakening in step (macro-AUC 0.871/0.759/0.728); a predicted-charge cascade reproduces 76.6% on LeCaRDv2 but does not transfer. The construct is also cashable at first stage: an exploratory zero-training charge-pool channel lifts LeCaRDv2 recall (R@100 +0.025, wrong-charge controls hurt), reported as a positive control for the confound, not a retrieval method or novelty claim. Charge is thus a high-leverage construct-validity factor at the benchmark level -- not auniform explanation of NDCG@10, and not evidence that any system relies on charge. We package established construct-validity and partial-input checks as a reusable charge-controlled protocol (CCE); o

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0046 — gh_73_plain_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 128
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

The paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models' discusses several limitations, ablations, and analysis findings.

### Evidence

```text
[1] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.
```

---

## GHR0029 — gh_79_cited_answer_3

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 129
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems'?

### Claim

It also mentions that the current implementation of EARS is specific to the e-commerce assistant supporting enterprise business intelligence workflows, and its applicability to other domains may require adaptation.

### Evidence

```text
[1] EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems
In large-scale enterprise settings, centralized multi-agent systems (MAS) are increasingly adopted, in which a coordinator delegates user requests to lightweight, domain-specialized sub-agents. While this architecture improves modularity, scalability, and cost efficiency, its reliability depends not only on accurate routing but also on sub-agents' ability to calibrate their responses to capability constraints. In particular, sub-agents built on smaller fine-tuned models often struggle with such calibration, leading them to over-answer ambiguous, underspecified, misrouted, or unsupported requests and produce hallucinated outputs instead of actionable feedback. To address this challenge, we present EARS (Explanatory Abstention for Reliable Sub-Agent Modeling), a production-oriented framework that reframes sub-agent abstention as an inter-agent communication protocol: a sub-agent does not merely abstain, but exposes an actionable failure state to the coordinator. EARS curates human-agent interaction data using an ensemble of calibrated LLM-as-a-Judge models, producing structured abstention labels and rationales under a taxonomy of sub-agent failure modes. These data are used to fine-tune sub-agents to detect failure conditions and return rationales for coordinator-level clarification, rerouting, or fallback. We evaluate EARS in a large-scale production e-commerce assistant supporting enterprise business intelligence workflows. EARS improves the overall response pass rate from 68.5% to 78.9%, demonstrating that sub-agent-side explanatory abstention improves MAS reliability.
```

---

## GHR0005 — gh_148_cited_answer_5

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 130
- sampling_stratum: `drop_home_related::cited_answer`
- sampling_weight: `4.166666666666667`
- hard_policy: `drop_home_related`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

The paper presents the results of experiments on five open-weight models and eight benchmarks, showing that DivInit consistently improves over standard parallel sampling.

### Evidence

```text
[1] Operadic consistency: a label-free signal for compositional reasoning failures in LLMs
Detecting LLM reasoning failures at inference time without ground-truth labels has motivated a wide range of confidence baselines, including self-consistency, semantic entropy, and P(True), built on within-question sampling and self-evaluation. Operad theory, the formalism for systems built by iterated substitution, suggests a complementary diagnostic: a model's direct answer to a compositional query should agree with the answer it produces by composing a stated decomposition of the same query. We instantiate this idea as operadic consistency (OC), a per-question signal. Across twelve instruction-tuned LLMs (4B to 671B parameters, open-weights and closed-source) on four multi-hop QA datasets, OC is strongly correlated with accuracy on every dataset (Pearson $r \in [0.86, 0.94]$, all $p \leq 0.0004$), and is the only signal we evaluate with $r \geq 0.85$ uniformly across all four datasets. Chain-of-thought self-consistency (CoT-SC; Wang et al., 2023) matches OC on HotpotQA and DROP ($r = 0.93, 0.87$) but drops to $r \approx 0.45$ on MuSiQue and StrategyQA. At the per-question level, OC contributes information beyond CoT-SC and semantic entropy on every dataset (cluster-robust $p \leq 10^{-16}$ for the OC coefficient), and the conclusion is robust to additionally controlling for constructed decomposition-aware baselines ($p \leq 10^{-13}$). The same signal yields selective-prediction improvements (accuracy at fixed coverage) over a tuned CoT-SC baseline at the equal-cost $K = 3$ budget (AUARC lifts of +0.086 to +0.096 and AUROC lifts of +0.092 to +0.164; 95% CIs exclude zero on every cell). On five frontier thinking models, where the decomposition is extracted from the model's own chain of thought, the same equal-cost comparison gives positive selective-prediction point-estimate lift on all 16 (dataset, budget, metric) cells tested, with 95% CIs excluding zero on 12 of the 16.

[2] Beyond Parallel Sampling: Diverse Query Initialization for Agentic Search
Test-time scaling for agentic search typically increases depth (i.e., more turns and tokens per trajectory) or breadth (i.e., more parallel rollouts). Here we focus on breadth scaling, showing that standard parallel sampling yields diminishing returns, tracing this to query redundancy at the first turn. When models issue similar first queries across rollouts, the threads retrieve overlapping evidence, and subsequent turns are conditioned on this shared retrieval. We address this limitation with DivInit, a training-free intervention at the first turn. Rather than sampling k independent first queries, DivInit draws n candidates from a single call, picks k < n diverse seeds, and runs them as parallel trajectories. Across five open-weight models and eight benchmarks, DivInit consistently improves over standard parallel sampling, with average gains of five to seven points on multi-hop QA at matched compute. Code available at https://github.com/cxcscmu/diverse-query-initialization
```

---

## GHR0111 — gh_15_plain_answer_6

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 131
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems'?

### Claim

This degradation is decomposed into a retrieval gap and a confusion gap.

### Evidence

```text
[1] EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems
In large-scale enterprise settings, centralized multi-agent systems (MAS) are increasingly adopted, in which a coordinator delegates user requests to lightweight, domain-specialized sub-agents. While this architecture improves modularity, scalability, and cost efficiency, its reliability depends not only on accurate routing but also on sub-agents' ability to calibrate their responses to capability constraints. In particular, sub-agents built on smaller fine-tuned models often struggle with such calibration, leading them to over-answer ambiguous, underspecified, misrouted, or unsupported requests and produce hallucinated outputs instead of actionable feedback. To address this challenge, we present EARS (Explanatory Abstention for Reliable Sub-Agent Modeling), a production-oriented framework that reframes sub-agent abstention as an inter-agent communication protocol: a sub-agent does not merely abstain, but exposes an actionable failure state to the coordinator. EARS curates human-agent interaction data using an ensemble of calibrated LLM-as-a-Judge models, producing structured abstention labels and rationales under a taxonomy of sub-agent failure modes. These data are used to fine-tune sub-agents to detect failure conditions and return rationales for coordinator-level clarification, rerouting, or fallback. We evaluate EARS in a large-scale production e-commerce assistant supporting enterprise business intelligence workflows. EARS improves the overall response pass rate from 68.5% to 78.9%, demonstrating that sub-agent-side explanatory abstention improves MAS reliability.

[2] Scaling Enterprise Agent Routing: Degradation, Diagnosis, and Recovery
Production LLM assistants route user requests to growing libraries of specialized tools, but how does routing accuracy degrade as the catalog scales? We study single-step routing on a 110-agent, 584-tool catalog from a deployed enterprise productivity assistant, evaluating three frontier models from 10 to 110 agents. Routing F1 on under-specified requests drops 16--23 percentage points across models. An oracle analysis decomposes the degradation into a \emph{retrieval} gap (the model cannot surface the right tool) and a \emph{confusion} gap (even with perfect retrieval, the oracle ceiling drops 10pp). Embedding-based shortlisting recovers +10--11pp F1 at full scale across all three models and two providers. A production annotation study (1,435 human-labeled utterances, three annotators) confirms the recovery on real traffic at +10--17pp despite 10--15pp lower absolute performance.

[3] Shopping Reasoning Bench: An Expert-Authored Benchmark for Multi-Turn Conversational Shopping Assistants
Conversational shopping assistants now serve hundreds of millions of customers, yet no existing benchmark jointly evaluates the open-ended multi-turn reasoning, domain expertise, and criterion-level quality that real shopping conversations demand. Shopping reasoning is unique among language model applications. Unlike factual question answering or verifiable code generation, it requires balancing subjective preferences, budget constraints, and cross-product trade-offs across multi-turn dialogue, capabilities absent from previous e-commerce and general-purpose benchmarks. We introduce the Shopping Reasoning Bench, an expert-authored benchmark of 525 missions (232 single-turn, 293 multi-turn) with 10863 importance-weighted binary rubrics authored by retail domain experts. These criteria are organized under a taxonomy of five reasoning categories and fifteen subcategories covering diverse demands such as preference refinement, trade-off analysis, and compatibility assessment. An evaluation of nine models across three families (GPT, Claude, Gemini) shows that pass rates reach only 57--77% overall. On multi-turn missions, all models score 13--29 points lower on optional above-and-beyond criteria than on required ones, and performance degrades 4--18 points as conversations progress. These gaps show that current models handle basic shopping assistance but fall short of expert-level advice, making Shopping Reasoning Bench a challenging testbed for future shopping assistant development.
```

---

## GHR0127 — gh_100_cited_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 132
- sampling_stratum: `remove_strongest::cited_answer`
- sampling_weight: `8.5`
- hard_policy: `remove_strongest`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems'?

### Claim

I can provide the main experimental results and comparisons from the other two sources: The main experimental result reported in the paper describing Drop-by-Drop is that it significantly reduces storage and memory overhead by allowing a single checkpoint to serve multiple bitwidths, while maintaining competitive perplexity and accuracy across major architectures such as Qwen, LLaMA, Gemma, and Mistral. In the paper discussing DICE (Document Inference via Chunk Evidence), the main experimental results are:

### Evidence

```text
[1] Multi-Bitwidth Quantization for LLMs Using Additive Codebooks
As large language models (LLMs) are increasingly deployed across heterogeneous hardware with varying resource constraints, the ability to adaptively manage the trade-off between performance and efficiency without retraining is critical. We propose Drop-by-Drop, a novel multi-bitwidth post-training quantization framework that enables inference-time precision control over LLM weights from a single trained model. Our method is theoretically grounded in information theory and successive refinement. We establish that LLM weights, which commonly follow a Gaussian distribution, can be optimally reconstructed with increasing fidelity as additional bits are incorporated, under a weighted mean squared error distortion motivated by LLM loss functions. To realize this in practice, Drop-by-Drop incorporates Matryoshka-style supervision into the loss function, exploiting the structure of additive codebooks. Drop-by-Drop produces a single model where ordered subsets of codebooks yield accurate partial reconstructions at each precision level. This approach significantly reduces storage and memory overhead by allowing a single checkpoint to serve multiple bitwidths, while maintaining competitive perplexity and accuracy across major architectures, such as Qwen, LLaMA, Gemma, and Mistral.

[2] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.
```

---

## GHR0052 — gh_84_plain_answer_9

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 133
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems'?

### Claim

The paper also notes that optional IvfFlat and HNSW backends can carry MonaVec to million-vector corpora.

### Evidence

```text
[1] MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems
We present MonaVec, a deterministic, embedded vector-search kernel for edge and offline AI -- settings where server infrastructure, network connectivity, and training data are all unavailable. Existing vector-search systems assume a persistent server, gigabytes of RAM, or a training pass over the corpus; MonaVec instead targets the deployment profile of SQLite: one file, one function call, runs anywhere. Its quantization core is training-free by default and data-oblivious: a Randomized Hadamard Transform (RHDH) conditions any input distribution toward N(0,1), so precomputed Lloyd-Max tables quantize to 4 bits (8x smaller) with no learned codebook and no data pass. The index persists as a single .mvec file whose embedded ChaCha20 rotation seed makes results reproducible across architectures and byte-identical within a build -- a determinism guarantee that parallel-build graph libraries cannot offer. On semantic embeddings (AG News, 45K x 1024-dim BGE-M3, cosine), MonaVec 4-bit BruteForce reaches 0.960 Recall@10 in 27 MB -- leading float32 FAISS-IVF and 8-bit usearch on recall -- while trading peak throughput for byte-identical determinism. A single-pass global standardization (fit()) extends the same data-oblivious pipeline to magnitude-sensitive L2 data, and optional IvfFlat and HNSW backends carry it to million-vector corpora. MonaVec is implemented in pure Rust with Python bindings and runtime SIMD dispatch (AVX-512/AVX2/NEON/scalar). It targets on-device RAG, offline agents, and embedded retrieval -- the niche SQLite occupies for relational data: one file, one call, runs anywhere.
```

---

## GHR0083 — gh_17_cited_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 134
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science'?

### Claim

The paper 'Which Sections of a Research Paper Best Reveal Its Research Methods?

### Evidence

```text
[1] Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science
Research methods are essential carriers of knowledge contribution in academic papers. Automatic multi-label classification of research methods can support knowledge services such as method retrieval, review generation, and research intelligence analysis. While existing studies primarily rely on titles and abstracts, abstracts often provide only limited methodological information, whereas utilizing full-text content faces challenges related to excessive length and information redundancy. Therefore, this paper proposes a segment combination strategy by partitioning the full-text content according to its physical postion. Using an annotated corpus of 1,954 full-text articles from three representative journals in Library and Information Science (JASIST, LISR, and JDoc), we evaluate the classification performance of various segments and their combinations across multiple models. Experimental results indicate that methodological information is distributed unevenly within the full-text content, with the middle-to-late and final segments exhibiting greater discriminative power. Furthermore, integrating bibliographic metadata with cross-segment combination strategies effectively enhances classification performance.

[2] Benchmarking LLM Agents on Meta-Analysis Articles from Nature Portfolio
Meta-analysis is a demanding form of evidence synthesis that combines literature retrieval, PI/ECO-guided study selection, and statistical aggregation. Its structured, verifiable workflow makes it an ideal substrate for evaluating systematic scientific reasoning, yet existing benchmarks lack ground truth across the full retrieval-screening-synthesis pipeline. We introduce MetaSyn, a dataset of 442 expert-curated meta-analyses from Nature Portfolio journals. Each entry pairs a research question with PI/ECO criteria, a retrieval corpus of 140k PubMed articles, verified positive studies, hard negatives that are topically similar but PI/ECO-ineligible, and complete search strategies and date bounds. Benchmarking twelve pipeline configurations (nine RAG variants and a protocol-driven agent) reveals a critical screening bottleneck: despite a retrieval ceiling of 90.9% recall at K=200, no system recovers more than 52.7% of ground-truth included literature. Current LLMs fail to reliably separate eligible studies from PI/ECO-failing distractors in pools of comparable topical relevance. Stage-attributed metrics capture where systems succeed and fail; a single end-to-end score does not.

[3] LEDGER: A Long-Context Benchmark of Corporate Annual Reports for Grounded Financial Retrieval and Extraction
Finance reporting is a natural proving ground for large language models, and the very-long-context capabilities of recent models across all sizes make rigorous evaluation in this domain an increasingly pressing need. Yet most public financial resources reduce the task to plain-text SEC 10-K filings paired with a handful of question-answer items. We release LEDGER (Long-context Evaluation of Documents for Grounded Extraction and Retrieval), a corpus of 4,999 digitized corporate annual reports - full documents with figures, tables, and narrative, not just regulatory filings. Each report is labeled with 31 consolidated financial KPIs to be extracted and linked to the market's reaction at the earnings date. From this data we derive three evaluation benchmarks spanning the difficulty spectrum: a pure page-level KPI retrieval task with TREC-style relevance judgments over 118,048 questions in natural language, a conversational "needle-in-a-haystack" single-value lookup, and a full KPI extraction task, both from long, numerically dense reports. We additionally provide human OCR-quality annotations with inter-annotator agreement and the complete extraction, validation, and scoring toolchain. We further demonstrate the dataset's research utility with a case study linking CEO-letter rhetoric to post-publication market impact.
```

---

## GHR0149 — gh_105_plain_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 135
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `method_scope`

### Question

What method, system, or framework is introduced in the paper 'LARE: Low-Attention Region Encoding for Text-Image Retrieval', and what problem is it designed to address?

### Claim

I cannot answer the question based on the information in the sources.

### Evidence

```text
[1] Beyond Parallel Sampling: Diverse Query Initialization for Agentic Search
Test-time scaling for agentic search typically increases depth (i.e., more turns and tokens per trajectory) or breadth (i.e., more parallel rollouts). Here we focus on breadth scaling, showing that standard parallel sampling yields diminishing returns, tracing this to query redundancy at the first turn. When models issue similar first queries across rollouts, the threads retrieve overlapping evidence, and subsequent turns are conditioned on this shared retrieval. We address this limitation with DivInit, a training-free intervention at the first turn. Rather than sampling k independent first queries, DivInit draws n candidates from a single call, picks k < n diverse seeds, and runs them as parallel trajectories. Across five open-weight models and eight benchmarks, DivInit consistently improves over standard parallel sampling, with average gains of five to seven points on multi-hop QA at matched compute. Code available at https://github.com/cxcscmu/diverse-query-initialization

[2] Looped World Models
Current world models face a fundamental tension: faithful long-horizon simulation demands deep computation, but deeper models are expensive to deploy and prone to compounding errors. We resolve this by introducing Looped World Models (LoopWM), which are the first looped architectures for world modelling. Our method iteratively refines latent environment states through a parameter-shared transformer block. This yield up to 100x parameter efficiency over conventional approaches with adaptive computation that automatically scales depth to match the complexity of each prediction step. Orthogonal to scaling model size and training data, LoopWM establishes iterative latent depth as a new scaling axis for world simulation, which might significantly push the community forward.
```

---

## GHR0048 — gh_84_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 136
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems'?

### Claim

Limitations: The paper mentions that MonaVec is designed for edge and offline AI settings where server infrastructure, network connectivity, and training data are unavailable.

### Evidence

```text
[1] MonaVec: A Training-Free Embedded Vector Search Kernel for Edge and Offline AI Systems
We present MonaVec, a deterministic, embedded vector-search kernel for edge and offline AI -- settings where server infrastructure, network connectivity, and training data are all unavailable. Existing vector-search systems assume a persistent server, gigabytes of RAM, or a training pass over the corpus; MonaVec instead targets the deployment profile of SQLite: one file, one function call, runs anywhere. Its quantization core is training-free by default and data-oblivious: a Randomized Hadamard Transform (RHDH) conditions any input distribution toward N(0,1), so precomputed Lloyd-Max tables quantize to 4 bits (8x smaller) with no learned codebook and no data pass. The index persists as a single .mvec file whose embedded ChaCha20 rotation seed makes results reproducible across architectures and byte-identical within a build -- a determinism guarantee that parallel-build graph libraries cannot offer. On semantic embeddings (AG News, 45K x 1024-dim BGE-M3, cosine), MonaVec 4-bit BruteForce reaches 0.960 Recall@10 in 27 MB -- leading float32 FAISS-IVF and 8-bit usearch on recall -- while trading peak throughput for byte-identical determinism. A single-pass global standardization (fit()) extends the same data-oblivious pipeline to magnitude-sensitive L2 data, and optional IvfFlat and HNSW backends carry it to million-vector corpora. MonaVec is implemented in pure Rust with Python bindings and runtime SIMD dispatch (AVX-512/AVX2/NEON/scalar). It targets on-device RAG, offline agents, and embedded retrieval -- the niche SQLite occupies for relational data: one file, one call, runs anywhere.
```

---

## GHR0090 — gh_12_cited_answer_1

**FINAL_LABEL:** INVALID_EXTRACTION

**FINAL_NOTES:** 

### Metadata

- review_order: 137
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation'?

### Claim

The paper 'MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation' reports the following main experimental results and comparisons:

### Evidence

```text
[1] MODE-RAG: Manifold Outlier Diagnosis and Energy-based Retrieval-Augmented Generation Evaluation
While Multimodal Retrieval-Augmented Generation (M-RAG) enhances Large Vision-Language Models, it remains highly susceptible to cross-modal hallucinations, causal fabrications, and sycophancy. Furthermore, existing mitigation pipelines often face an intervention paradox: static rules tend to unnecessarily disrupt accurate generations, whereas leaving the multi-modal reasoning completely unguided allows existing mismatches to cascade into severe logical fabrications. To quantify and mitigate these hallucinations, we propose a Multi-Agent system, MODE-RAG, driven by Variational Free Energy (VFE) and internal attention states to dynamically gate interventions. High-risk queries are routed to five stage-specific agents, integrating Monte Carlo Tree Search (MCTS) for rigorous causal derivation and logit perturbations to penalize sycophancy. Dedicated Correction and Overseer agents ensure formatting stability and perform post-hoc factual verification. To objectively evaluate our approach, we introduce ModeVent, a challenging subset derived from the MultiVent dataset. Extensive experiments indicate that our system effectively reduces hallucination rates and logical fabrication, significantly improving the robustness of M-RAG systems.

[2] REVES: REvision and VErification--Augmented Training for Test-Time Scaling
Test-time scaling via sequential revision has emerged as a powerful paradigm for enhancing Large Language Model (LLM) reasoning. However, standard post-training methods primarily optimize single-shot objectives, creating a fundamental misalignment with multi-step inference dynamics. While recent work treats this as multi-turn reinforcement learning (RL), conventional approaches optimize over the multi-step trajectories directly, failing to further exploit the high-quality mistakes in intermediate steps that model can learn from correcting them. We propose a two-stage iterative framework that alternates between online data/prompt augmentation and policy optimization. By converting the intermediate steps (``near-miss'' answers) in the successful recovery trajectories into decoupled revision and verification prompts, our approach concentrates training on both effective answer transformation and error identification. This approach enables efficient off-policy data generation and reduces the computational overhead of long-horizon sampling compared to standard multi-turn RL. On LiveCodeBench, using publicly available test cases as feedback, we observe gains of +6.5 points over the RL baseline and +4.0 points over standard multi-turn training. Beyond coding, our approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems. Math results under ground-truth verification further confirm improved correction ability. It also generalizes to out-of-distribution constraint-satisfaction puzzles such as n\_queens and mini\_sudoku, where correctness is defined entirely by problem constraints. Code is available at https://github.com/yxliu02/REVES.git.

[3] Personal Care Utility: Health as Everyday Infrastructure
Healthcare is essential, expert, and episodic by design - built around the roughly one hour per year a person spends with a clinician. The 8,759 hours outside clinical settings, where eating, sleeping, movement, medication, and stress actually shape long-term health, have no comparable infrastructure. The bottleneck for personalized health is not raw data or reasoning capability; it is the absence of that infrastructure layer. This paper introduces the Personal Care Utility (PCU): a layered, event-driven architecture proposed as the missing utility for everyday health, in the way that payments, networks, and power are utilities for their domains. PCU organizes continuous personal signals into semantically meaningful life events through a Personicle, estimates dynamic health state against personal baselines, reasons about cause and context, and routes guidance through an orchestrator that separates clinical decision logic, behavioral strategy selection, and natural-language expression. This separation lets large language models support reasoning and communication while keeping safety-critical clinical decisions grounded in validated evidence. We instantiate PCU for Type 2 Diabetes - turning CGM, meal, activity, medication, sleep, stress, and clinical data into glycemic events, individualized state estimates, causal explanations, and knowledge-grounded interventions. A day-in-the-life scenario shows the same infrastructure producing real-time nudges, weekly summaries, medication check-ins, silence, or deterministic safety alerts depending on context and risk. We close with how PCU generalizes to other chronic conditions and the governance questions any always-on personal health utility must address. T

[TRUNCATED FOR REVIEW FILE]
```

---

## GHR0014 — gh_79_cited_answer_2

**FINAL_LABEL:** UNSUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 138
- sampling_stratum: `home_weak_1::cited_answer`
- sampling_weight: `8.625`
- hard_policy: `home_weak_1`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems'?

### Claim

Limitations: The paper acknowledges that the effectiveness of EARS may depend on the quality and quantity of the human-agent interaction data used for training the LLM-as-a-Judge models.

### Evidence

```text
[1] EARS: Explanatory Abstention for Reliable Sub-Agent Modeling in Large-scale Multi-Agent Systems
In large-scale enterprise settings, centralized multi-agent systems (MAS) are increasingly adopted, in which a coordinator delegates user requests to lightweight, domain-specialized sub-agents. While this architecture improves modularity, scalability, and cost efficiency, its reliability depends not only on accurate routing but also on sub-agents' ability to calibrate their responses to capability constraints. In particular, sub-agents built on smaller fine-tuned models often struggle with such calibration, leading them to over-answer ambiguous, underspecified, misrouted, or unsupported requests and produce hallucinated outputs instead of actionable feedback. To address this challenge, we present EARS (Explanatory Abstention for Reliable Sub-Agent Modeling), a production-oriented framework that reframes sub-agent abstention as an inter-agent communication protocol: a sub-agent does not merely abstain, but exposes an actionable failure state to the coordinator. EARS curates human-agent interaction data using an ensemble of calibrated LLM-as-a-Judge models, producing structured abstention labels and rationales under a taxonomy of sub-agent failure modes. These data are used to fine-tune sub-agents to detect failure conditions and return rationales for coordinator-level clarification, rerouting, or fallback. We evaluate EARS in a large-scale production e-commerce assistant supporting enterprise business intelligence workflows. EARS improves the overall response pass rate from 68.5% to 78.9%, demonstrating that sub-agent-side explanatory abstention improves MAS reliability.
```

---

## GHR0059 — gh_74_plain_answer_7

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 139
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents'?

### Claim

the paper does not explicitly discuss any specific ablations or analysis findings beyond the comparison of CoreMem's performance to existing systems and its ability to operate within resource constraints.

### Evidence

```text
[1] CoreMem: Riemannian Retrieval and Fisher-Guided Distillation for Long-Term Memory in Dialogue Agents
Personalized dialogue agents require continuous long-term memory to maintain coherent interactions across multiple sessions. However, deploying these capabilities on consumer-grade hardware (e.g., 8 GB VRAM edge devices) introduces severe memory and compute bottlenecks. Existing systems typically rely on isotropic cosine similarity for retrieval and heuristic rules for context compression. These approaches lack a unified theoretical foundation, frequently suffering from the hubness problem in high-dimensional retrieval and syntactic fragmentation during compression. To overcome these limitations, we propose CoreMem, a resource-efficient edge-cloud memory architecture fundamentally unified by information geometry. First, Riemannian retrieval replaces cosine matching with a locally adaptive Fisher-Rao metric, effectively penalizing hub memories via Mahalanobis distance with O(Ndr) Woodbury acceleration for real-time search. Second, Fisher-guided discrete token distillation (FDTD) introduces a hierarchical sentence-to-token compression mechanism. It derives sensitivity scores from Fisher information traces, providing a principled compression-KL tradeoff augmented with explicit structural syntax protection. Evaluated on the LOCOMO and LongMemEval-S benchmarks, CoreMem achieves strong accuracy improvements, yielding substantial gains in Open-domain (+4.51 pp) and Temporal (+4.17 pp) reasoning. Extensive profiling confirms that CoreMem operates seamlessly within a strict 8 GB VRAM budget, successfully bridging the gap between resource-constrained edge devices and the demand for theoretically grounded, lifelong memory agents.
```

---

## GHR0088 — gh_20_cited_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 140
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation'?

### Claim

The specific benchmarks are not explicitly mentioned in the source, but it is stated that the experiments were conducted across three model sizes.

### Evidence

```text
[1] PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation
Agentic GraphRAG trains language-model agents to iteratively retrieve and reason over graph-structured evidence, enabling more accurate and context-aware decision-making by efficiently navigating complex information networks. However, outcome-only reinforcement learning suffers from \textit{\textbf{answer-path reward aliasing}}, where correct answers may come from shortcuts rather than useful evidence paths. It also exhibits \textit{\textbf{search-update ambiguity}}, as scalar trajectory-level feedback does not indicate which retrieval actions to adjust. To mitigate these shortcomings, we present PathRouter, a path-aware training framework for agentic GraphRAG. PathRouter jointly evaluates each trajectory along answer correctness and evidence-path overlap, yielding four trajectory categories with differentiated GRPO advantage scaling that suppresses shortcut reinforcement while preserving evidence-seeking behavior. For evidence-poor trajectories, a frozen gold-evidence teacher provides token-level KL guidance on reasoning and search-query tokens, excluding answer tokens to avoid direct response imitation. Experiments on six QA benchmarks across three model sizes show that PathRouter consistently improves answer F1 and evidence-path overlap, achieving average F1 gains of 3.1 on 3B and 4.9 on 7B models compared to a strong baseline.

[2] REVES: REvision and VErification--Augmented Training for Test-Time Scaling
Test-time scaling via sequential revision has emerged as a powerful paradigm for enhancing Large Language Model (LLM) reasoning. However, standard post-training methods primarily optimize single-shot objectives, creating a fundamental misalignment with multi-step inference dynamics. While recent work treats this as multi-turn reinforcement learning (RL), conventional approaches optimize over the multi-step trajectories directly, failing to further exploit the high-quality mistakes in intermediate steps that model can learn from correcting them. We propose a two-stage iterative framework that alternates between online data/prompt augmentation and policy optimization. By converting the intermediate steps (``near-miss'' answers) in the successful recovery trajectories into decoupled revision and verification prompts, our approach concentrates training on both effective answer transformation and error identification. This approach enables efficient off-policy data generation and reduces the computational overhead of long-horizon sampling compared to standard multi-turn RL. On LiveCodeBench, using publicly available test cases as feedback, we observe gains of +6.5 points over the RL baseline and +4.0 points over standard multi-turn training. Beyond coding, our approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems. Math results under ground-truth verification further confirm improved correction ability. It also generalizes to out-of-distribution constraint-satisfaction puzzles such as n\_queens and mini\_sudoku, where correctness is defined entirely by problem constraints. Code is available at https://github.com/yxliu02/REVES.git.

[3] CORA: Analyzing and bridging thinking-answer gap in Multimodal RLVR via Consistency-Oriented Reasoning Alignment
Reinforcement learning with verifiable rewards (RLVR) has successfully elicited the reasoning capabilities of large language models, motivating its extension to multimodal scenarios. Existing methods primarily focus on improving the visual coverage of reasoning traces and mitigating visual hallucinations, but underestimate the semantic inconsistency between the reasoning process and the final answer. In this paper, we delve into thinking-answer inconsistency in RLVR for large vision-language models (LVLMs), showing thorough analyses of rollouts collected throughout Group Relative Policy Optimization (GRPO) training process and post-RLVR evaluation outputs that this issue persists during training and remains present during inference. Motivated by the analysis, we propose Consistency-Oriented Reasoning Alignment (CORA), which introduces thinking-answer semantic consistency into RLVR through a lightweight plug-and-play consistency reward model, and further incorporates Hybrid Reward Advantage Splitting (HRAS) to stably coordinate task and consistency optimization. Extensive experiments across representative multimodal reasoning benchmarks and mainstream LVLMs show that CORA improves task performance while effectively mitigating thinking-answer inconsistency, leading to more faithful reasoning traces.
```

---

## GHR0072 — gh_29_cited_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 141
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'REVES: REvision and VErification--Augmented Training for Test-Time Scaling'?

### Claim

Beyond coding, the approach is also tested on circle packing, where it matches the SOTA result .

### Evidence

```text
[1] REVES: REvision and VErification--Augmented Training for Test-Time Scaling
Test-time scaling via sequential revision has emerged as a powerful paradigm for enhancing Large Language Model (LLM) reasoning. However, standard post-training methods primarily optimize single-shot objectives, creating a fundamental misalignment with multi-step inference dynamics. While recent work treats this as multi-turn reinforcement learning (RL), conventional approaches optimize over the multi-step trajectories directly, failing to further exploit the high-quality mistakes in intermediate steps that model can learn from correcting them. We propose a two-stage iterative framework that alternates between online data/prompt augmentation and policy optimization. By converting the intermediate steps (``near-miss'' answers) in the successful recovery trajectories into decoupled revision and verification prompts, our approach concentrates training on both effective answer transformation and error identification. This approach enables efficient off-policy data generation and reduces the computational overhead of long-horizon sampling compared to standard multi-turn RL. On LiveCodeBench, using publicly available test cases as feedback, we observe gains of +6.5 points over the RL baseline and +4.0 points over standard multi-turn training. Beyond coding, our approach matches the previously reported SOTA result on circle packing while using the smallest base model (4B) and far fewer rollouts than the much larger evolutionary search systems. Math results under ground-truth verification further confirm improved correction ability. It also generalizes to out-of-distribution constraint-satisfaction puzzles such as n\_queens and mini\_sudoku, where correctness is defined entirely by problem constraints. Code is available at https://github.com/yxliu02/REVES.git.
```

---

## GHR0117 — gh_3_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 142
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science'?

### Claim

Evidence from Library and Information Science' discusses the limitations and analysis findings related to the distribution of methodological information within full-text research articles.

### Evidence

```text
[1] Which Sections of a Research Paper Best Reveal Its Research Methods? Evidence from Library and Information Science
Research methods are essential carriers of knowledge contribution in academic papers. Automatic multi-label classification of research methods can support knowledge services such as method retrieval, review generation, and research intelligence analysis. While existing studies primarily rely on titles and abstracts, abstracts often provide only limited methodological information, whereas utilizing full-text content faces challenges related to excessive length and information redundancy. Therefore, this paper proposes a segment combination strategy by partitioning the full-text content according to its physical postion. Using an annotated corpus of 1,954 full-text articles from three representative journals in Library and Information Science (JASIST, LISR, and JDoc), we evaluate the classification performance of various segments and their combinations across multiple models. Experimental results indicate that methodological information is distributed unevenly within the full-text content, with the middle-to-late and final segments exhibiting greater discriminative power. Furthermore, integrating bibliographic metadata with cross-segment combination strategies effectively enhances classification performance.

[2] Focus When Necessary: Adaptive Routing and Collaborative Grounding for Training-Free Visual Grounding
While Multimodal Large Language Models (MLLMs) excel in cross-modal reasoning, they often struggle to perceive fine-grained details in complex high-resolution images. Recent training-free methods address this through image scaling and localized cropping. However, applying these manipulations indiscriminately introduces computational redundancy for simple queries and can degrade accuracy by truncating essential global context or introducing irrelevant background noise. To this end, we propose LazyMCoT, a dynamic and training-free framework that adaptively allocates visual grounding efforts based on sample difficulty. The framework features an Adaptive Routing mechanism that evaluates predictive uncertainty using first-token statistics from a single forward pass. This efficiently bypasses confident cases while ensuring the recall of difficult samples via conformal calibration. For these challenging cases, a Collaborative Grounding module integrates the inherent cross-modal attention of the model with an external visual expert through a two-stage refinement process. This refinement process generates a precise localized display to recover small or occluded targets. Extensive experiments across diverse benchmarks demonstrate that LazyMCoT rivals training-based approaches by simultaneously improving reasoning accuracy and reducing average inference latency. Our code is availble at https://github.com/TencentBAC/LazyMCoT.

[3] Analyzing and Encoding the Al-Mawrid Arabic-English Dictionary with the ISO Language Markup Framework and TEI Lex-0
This paper presents a robust methodology for the systematic digitization and encoding of the Al-Mawrid Arabic-English dictionary, transforming it from a legacy print resource into a standardized computational lexicon. Addressing a significant gap in Arabic lexical infrastructure, the study adopts a dual-standard framing that aligns the ISO Lexical Markup Framework (LMF) with the Text Encoding Initiative TEI Lex-0 guidelines. By applying an editorial view to the dictionary's macro- and microstructure, the research resolves the structural ambiguities and punctuation inconsistencies typical of 20th-century bilingual dictionaries. The methodology is grounded in an empirical analysis of the dictionary's lexical knowledge density. Drawing on a representative sample (the letter Ayn, comprising 4.6% of the total volume), the study provides scientific weight to the encoding process, demonstrating a structural parsing accuracy of 91%. Quantitative evaluation of the information extraction rules reveals high performance, with 85% precision and 98% recall for synonyms, and 88% precision for other morpho-semantic features. Beyond technical description, the paper provides a critical comparison with existing Arabic lexical resources and discusses the limitations of TEI Lex-0 when modelling specific Arabic phenomena, such as implicit "open set" semantic relations and scattered morphological cues. Furthermore, the study explores the potential for Linguistic Linked Open Data (LLOD) integration by establishing a scalable prefix-based referencing system that facilitates the resource's inclusion in the semantic web. The result is an interoperable, machine-tractable resource that provides a reproducible workflow for the retro-digitization of complex legacy bilingual lexicons within the Arabic NLP and Digital Humanities communities.
```

---

## GHR0089 — gh_18_cited_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 143
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `cited_evidence`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments'?

### Claim

Agentic methods outperform single-shot retrieval baselines, but the best-performing agent only achieves 0.314 Recall@100 and 0.355 Recall@All, indicating substantial room for improvement .

### Evidence

```text
[1] ScholarQuest: A Taxonomy-Guided Benchmark for Agentic Academic Paper Search in Open Literature Environments
Academic paper search is a core step in scientific research, and LLM-based search agents are emerging as a promising paradigm for iterative, intent-driven literature exploration. However, existing benchmarks are insufficient for systematically evaluating agentic academic search under realistic open literature environments. We propose ScholarQuest, a large-scale, taxonomy-guided benchmark for agentic academic paper search. ScholarQuest is constructed from over 1,000 computer science topics and four representative research intents, including method-oriented, setting-anchored, comparison-based, and scope-controlled queries. It further provides scalable answer construction and a shared retrieval backend ScholarBase for reproducible evaluation. Benchmarking results show that agentic methods outperform single-shot retrieval baselines, yet the best-performing agent only achieves 0.314 Recall@100 and 0.355 Recall@All, indicating substantial room for improvement. In addition, analyses of search efficiency, intent-level robustness, and failure cases further highlight the benchmark's ability to provide multi-dimensional evaluation signals for academic paper search agents.
```

---

## GHR0097 — gh_48_plain_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 144
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Understanding the Behaviors of Environment-aware Information Retrieval'?

### Claim

The study reveals that reinforcement learning (RL) effectively teaches an LLM to tailor its queries to specific retriever characteristics.

### Evidence

```text
[1] Understanding the Behaviors of Environment-aware Information Retrieval
Recent retrieval-augmented generation (RAG) approaches have demonstrated strong capability in handling complex queries, yet current research overlooks a critical challenge: different retrievers require fundamentally different query formulation strategies for optimal performance. In this work, we present the first systematic analysis of how LLMs can learn to adapt their query formulation strategies for different retrievers via reinforcement learning (RL). Our empirical study reveals that RL effectively teaches an LLM to tailor its queries to specific retriever characteristics. We discover that different retrievers exhibit surprisingly distinct optimal query styles (e.g., descriptive vs. question-like), suggesting strategies learned for one retriever ineffective for another. We further show that performance can be enhanced by incorporating retriever-specific human guidance and by scaling model size. To facilitate learning over multi-retrieval-step trajectories, we introduce a branching-based rollout technique that improves training stability. Our work provides the first empirical evidence and actionable insights for building truly retriever-aware RAG systems. Code and resources are available at https://github.com/LCO-Embedding/Envs-aware-Information-Retrieval.

[2] When Does Mixing Help? Analyzing Query Embedding Interpolation in Multilingual Dense Retrieval
While mixed-language querying is ubiquitous in multilingual communities, the sensitivity of dense retrievers to such queries remains poorly understood. We present a ratio-controlled study on mMARCO that systematically evaluates retrieval performance by varying the mixing proportion of parallel query translations via embedding-level mixing -- constructing mixed queries as an interpolation of monolingual embeddings. Experiments with BGE-M3 demonstrate that an optimal mixing ratio outperforms the best monolingual endpoint in 88/105 cases. We uncover a distinct asymmetry driven by English dominance: mixing is uniformly beneficial when retrieving from non-English document indices, whereas indices containing English are best served by pure English queries. Furthermore, English acts as the strongest mixing partner for every non-English document language. Finally, when controlling for English dominance, mixing gains correlate negatively with typological distance. We conclude that language-mix sensitivity is structured and predictable, and we validate the robustness of these patterns across model families and scales.

[3] RL-Index: Reinforcement Learning for Retrieval Index Reasoning
Retrieving external knowledge is essential for solving real-world tasks, yet it remains challenging when the relationship between a query and its relevant knowledge involves implicit and complex reasoning beyond surface-level semantic or lexical matching (e.g., mathematical problems relying on the same theorem or coding requiring deep reasoning). Existing approaches primarily rely on query-side reasoning (e.g., query rewriting), which introduces significant online latency and underutilizes the opportunity to perform reasoning over the knowledge corpus itself (i.e., index-side reasoning). In this paper, we propose RL-Index, an agentic indexing framework that formulates retrieval index reasoning as a reinforcement learning problem. Instead of performing reasoning at query time, RL-Index shifts reasoning to the indexing stage by augmenting documents with LLM-generated rationales that explicitly encode the latent query-knowledge relationship. To optimize the quality of these rationales, we employ Group Relative Policy Optimization (GRPO) and use retrieval similarity as a verifiable reward signal, enabling direct optimization of indexing decisions for retrieval effectiveness. Extensive experiments on the BRIGHT benchmark demonstrate that RL-Index consistently improves both retrieval and downstream question-answering performance, while significantly reducing online inference latency. Moreover, the learned rationale augmentation generalizes across diverse retrievers and generators, highlighting its robustness as a plug-and-play indexing strategy across different retrieval systems.
```

---

## GHR0146 — gh_139_plain_answer_1

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 145
- sampling_stratum: `remove_strongest::plain_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `remove_strongest`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `results_comparison`

### Question

What main experimental results or comparisons are reported in the paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice'?

### Claim

The paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice' is not among the sources provided.

### Evidence

```text
[1] OpenMedReason: Scientific Reasoning Supervision for Medical Vision-Language Models
High-stakes clinical use of large vision-language models (LVLMs) requires reasoning that is grounded in visual evidence and clinical knowledge, not just correct final answers. We introduce OpenMedReason, a large-scale, open multimodal medical reasoning corpus comprising approximately 450K image-question-answer instances whose reasoning traces are primarily derived from curated biomedical, human-authored scientific articles. OpenMedReason provides high-fidelity supervision beyond synthetic chains of thought, covering diverse medical domain vision modalities such as radiological scans, microscopic images, visible light photographs, charts, and others. We complement it with OpenMedReason-Bench, a held-out benchmark that allows fine-grained evaluation of LVLMs along three complementary axes of capability, including perception, medical knowledge, and rationale, enabling diagnostic evaluation beyond final-answer accuracy. OpenMedReason is a rich training resource that exhibits its effectiveness in both supervised fine-tuning (SFT) and reinforcement-based alignment. Training with OpenMedReason yields a 20% average improvement in VQA accuracy over the base model and achieves performance within 4.2% of the strongest comparable-scale medical LVLMs. Fine-grained performance analysis confirms that the gains are not concentrated in any single axis: OpenMedReason improves perception, medical knowledge, and rationale jointly, and its reasoning traces are preferred over those of the base model in 86.1% of pairwise comparisons. We release the code and dataset at huggingface.co/datasets/neginb/OpenMedReason.

[2] LEDGER: A Long-Context Benchmark of Corporate Annual Reports for Grounded Financial Retrieval and Extraction
Finance reporting is a natural proving ground for large language models, and the very-long-context capabilities of recent models across all sizes make rigorous evaluation in this domain an increasingly pressing need. Yet most public financial resources reduce the task to plain-text SEC 10-K filings paired with a handful of question-answer items. We release LEDGER (Long-context Evaluation of Documents for Grounded Extraction and Retrieval), a corpus of 4,999 digitized corporate annual reports - full documents with figures, tables, and narrative, not just regulatory filings. Each report is labeled with 31 consolidated financial KPIs to be extracted and linked to the market's reaction at the earnings date. From this data we derive three evaluation benchmarks spanning the difficulty spectrum: a pure page-level KPI retrieval task with TREC-style relevance judgments over 118,048 questions in natural language, a conversational "needle-in-a-haystack" single-value lookup, and a full KPI extraction task, both from long, numerically dense reports. We additionally provide human OCR-quality annotations with inter-annotator agreement and the complete extraction, validation, and scoring toolchain. We further demonstrate the dataset's research utility with a case study linking CEO-letter rhetoric to post-publication market impact.
```

---

## GHR0116 — gh_10_plain_answer_2

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 146
- sampling_stratum: `home_weak_plus_distractors::plain_answer`
- sampling_weight: `8.7`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `dataset_benchmark`

### Question

What datasets, benchmarks, or evaluation settings are described in the paper 'NEST: Narrative Event Structures in Time for Long Video Understanding'?

### Claim

This dataset consists of 1005 full-length movies, each annotated with 102 multimodal narrative events grounded in visual content, dialogue, and audio.

### Evidence

```text
[1] NEST: Narrative Event Structures in Time for Long Video Understanding
Recent progress in vision-language models has enabled the processing of increasingly long video sequences, but the ability to handle extended token streams does not translate to understanding of narrative structure in long videos. Existing long video benchmarks focus on needle-in-a-haystack retrieval rather than evaluating how low-level actions form events, how events interact across time, and how narratives progress, for example, whether a model can connect an early setback, such as a job loss to a later relationship breakup, despite long gaps, intervening scenes, or flashbacks that reframe what occurred. We introduce NEST (Narrative Event Structures in Time for Long Video Understanding), a dataset of 1005 full-length movies (avg. 98 minutes), each annotated with 102 multimodal narrative events grounded in visual content, dialogue, and audio. NEST captures multimodal narrative events with structured annotations grounded in visual content, dialogue, and audio, and links them through relations that reflect narrative structure, including temporal ordering, hierarchical composition, and long-range dependencies. We introduce baselines for event trigger detection (ETD), event localization (EL), event argument extraction (EAE), and event relation extraction (ERE). The benchmark is highly challenging for grounded event discovery, with ETD below 8%, EL under 6%, and EAE below 11%. In contrast, ERE is more tractable once events are given, reaching 35.45% F1 zero-shot and 44.42% F1 after fine-tuning.

[2] LAUKIN: A Multi-jurisdictional Common Law Contract Dataset
Multinational companies increasingly require cross-jurisdictional contract review, yet existing legal NLP datasets are largely restricted to a single jurisdiction. We introduce LAUKIN (Legal equivalence dataset of Australia, UK, and INdia), a dataset of clause pairs (AU-UK, UK-IN, IN-AU) labelled for boolean legal equivalence. We develop a novel multi-stage retrieval and reranking pipeline to construct the initial clause pair mapping, with a subset of clause pairs subsequently annotated by legal experts as Equivalent or Not Equivalent. The dataset comprises 14,727 clause pairs from 204 contracts across 8 agreement types, of which 3,000 are manually labelled: 900 train, 600 dev, and 1,500 test. We evaluate 12 models across 4 techniques, achieving a best macro-F1 of 65.11%, establishing LAUKIN as a challenging benchmark. Results reveal that, despite shared legal heritage, drafting conventions diverge significantly across jurisdictions, making cross-jurisdictional equivalence classification non-trivial. LAUKIN also includes 11,727 unlabelled training pairs to support future semi-supervised learning research in legal NLP.

[3] A Large-Scale Multi-Dimensional Empirical Study of LLMs for Conversation Summarization
Despite the significant advancement of LLMs in conversation summarization, their evaluation remains limited by insufficient scenarios, input lengths, and sample sizes. Furthermore, existing benchmarks often omit frontier reasoning systems and efficient small models, or lack fine-grained, multi-dimensional assessments. To bridge these gaps, we propose OmniCSEval, a unified benchmark comprising 1,800 diverse conversations across six real-world scenarios, featuring context lengths ranging from 128 to 32k tokens. For fine-grained evaluation, we employ a bidirectional fact-checking framework that integrates key fact matching to assess completeness and conciseness, alongside summary fact verification to evaluate faithfulness. To ensure reliable assessment, we establish a human-LLM collaborative pipeline for key fact extraction and a multi-LLM consensus verifier for summary fact decomposition. Leveraging this framework, we evaluate 28 LLMs across four distinct categories grouped by reasoning capability and model scale. Our extensive empirical study reveals critical insights regarding the cross-scenario challenges current LLMs continue to face, the impacts of reasoning and scale, and the efficiency and adaptability of reasoning models. We also provide guidance for system selection in real-world deployments.
```

---

## GHR0001 — gh_150_cited_answer_2

**FINAL_LABEL:** ABSTENTION

**FINAL_NOTES:** 

### Metadata

- review_order: 147
- sampling_stratum: `drop_home_related::cited_answer`
- sampling_weight: `4.166666666666667`
- hard_policy: `drop_home_related`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'HistoRAG: Embedding Historical Methodology in Retrieval-Augmented Generation Through Critical Technical Practice'?

### Claim

I'm unable to discuss any limitations, ablations, or analysis findings from that specific paper.

### Evidence

```text
[1] OpenMedReason: Scientific Reasoning Supervision for Medical Vision-Language Models
High-stakes clinical use of large vision-language models (LVLMs) requires reasoning that is grounded in visual evidence and clinical knowledge, not just correct final answers. We introduce OpenMedReason, a large-scale, open multimodal medical reasoning corpus comprising approximately 450K image-question-answer instances whose reasoning traces are primarily derived from curated biomedical, human-authored scientific articles. OpenMedReason provides high-fidelity supervision beyond synthetic chains of thought, covering diverse medical domain vision modalities such as radiological scans, microscopic images, visible light photographs, charts, and others. We complement it with OpenMedReason-Bench, a held-out benchmark that allows fine-grained evaluation of LVLMs along three complementary axes of capability, including perception, medical knowledge, and rationale, enabling diagnostic evaluation beyond final-answer accuracy. OpenMedReason is a rich training resource that exhibits its effectiveness in both supervised fine-tuning (SFT) and reinforcement-based alignment. Training with OpenMedReason yields a 20% average improvement in VQA accuracy over the base model and achieves performance within 4.2% of the strongest comparable-scale medical LVLMs. Fine-grained performance analysis confirms that the gains are not concentrated in any single axis: OpenMedReason improves perception, medical knowledge, and rationale jointly, and its reasoning traces are preferred over those of the base model in 86.1% of pairwise comparisons. We release the code and dataset at huggingface.co/datasets/neginb/OpenMedReason.

[2] LEDGER: A Long-Context Benchmark of Corporate Annual Reports for Grounded Financial Retrieval and Extraction
Finance reporting is a natural proving ground for large language models, and the very-long-context capabilities of recent models across all sizes make rigorous evaluation in this domain an increasingly pressing need. Yet most public financial resources reduce the task to plain-text SEC 10-K filings paired with a handful of question-answer items. We release LEDGER (Long-context Evaluation of Documents for Grounded Extraction and Retrieval), a corpus of 4,999 digitized corporate annual reports - full documents with figures, tables, and narrative, not just regulatory filings. Each report is labeled with 31 consolidated financial KPIs to be extracted and linked to the market's reaction at the earnings date. From this data we derive three evaluation benchmarks spanning the difficulty spectrum: a pure page-level KPI retrieval task with TREC-style relevance judgments over 118,048 questions in natural language, a conversational "needle-in-a-haystack" single-value lookup, and a full KPI extraction task, both from long, numerically dense reports. We additionally provide human OCR-quality annotations with inter-annotator agreement and the complete extraction, validation, and scoring toolchain. We further demonstrate the dataset's research utility with a case study linking CEO-letter rhetoric to post-publication market impact.
```

---

## GHR0044 — gh_73_plain_answer_8

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 148
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models'?

### Claim

A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics.

### Evidence

```text
[1] Thermodynamic Signatures of Reasoning: Free-Energy and Spectral-Form-Factor Diagnostics for Hallucination Detection in Large Language Models
Hallucination detection in large language models (LLMs) is deployment-critical, and recent work shows that the spectrum of attention-derived graph Laplacians carries strong signal about reasoning quality. Prior spectral diagnostics, however, summarize the Laplacian spectrum by a handful of eigenvalues or hand-picked scalars, leaving most of its structure unused. We propose Free-Energy Signatures (Fes), a spectral descriptor that treats each layer's attention Laplacian as a Hamiltonian and extracts its thermodynamic potentials partition function, free energy, spectral entropy, heat capacity together with the random-matrix-theory (RMT) spectral form factor. We prove three results: (i)~Lipschitz stability of Fes under attention perturbation; (ii)~an expressiveness result showing that Fes enriches finite spectral summaries and approximates moment-derived spectral functionals under explicit regularity and grid-resolution assumptions; and (iii)~a finite-sample PAC bound on the AUROC of a training-free detector built from Fes. Empirically, across six open-weight LLMs and six benchmarks, a lightweight probe on Fes descriptors achieves the strongest aggregate AUROC among attention-spectral baselines, improving over LapEig by $+6.5$ AUROC points and over GoR-4 by $+2.4$ points on average, while requiring no update to the underlying LLM. In the fully unsupervised setting, an RMT-deviation score achieves mean AUROC $0.71$, providing a label-free but weaker detector. A complementary RMT analysis shows that correct generations exhibit more Wigner-Dyson like spectral statistics, whereas hallucinations exhibit more Poisson-like statistics. The anonymized code and config are provided in the supplementary material.
```

---

## GHR0060 — gh_58_plain_answer_3

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 149
- sampling_stratum: `home_weak_1::plain_answer`
- sampling_weight: `8.607142857142858`
- hard_policy: `home_weak_1`
- answer_variant: `plain_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation'?

### Claim

The paper also introduces the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document.

### Evidence

```text
[1] Lost in a Single Vector: Improving Long-Document Retrieval with Chunk Evidence Aggregation
Dense retrieval ranks one query vector against one document vector. On long documents, this interface can fail when a short but decisive span is weakened during document encoding before ranking. We study this failure mode as document-side early compression and introduce the Evidence Dilution Index (EDI) to measure how far a document-level representation falls below the strongest chunk-level evidence within the same gold document. Guided by this view, we propose DICE (Document Inference via Chunk Evidence), a training-free document-side strategy that splits documents into chunks, encodes them independently with a frozen model, and aggregates them back into a single vector while preserving the standard one-query-one-document interface. On LongEmbed, DICE improves retrieval across four backbones, with the largest gains on slices beyond 4k tokens: for Dream, Passkey >4k rises from 30.0 to 90.0 and Needle >4k from 23.3 to 74.0. Across 12,779 filtered samples, DICE yields lower EDI than the single-vector baseline in 92.8% of cases. These results establish document-level encoding as a practical and underexplored lever for long-document retrieval.
```

---

## GHR0084 — gh_11_cited_answer_9

**FINAL_LABEL:** SUPPORTED

**FINAL_NOTES:** 

### Metadata

- review_order: 150
- sampling_stratum: `home_weak_plus_distractors::cited_answer`
- sampling_weight: `8.714285714285714`
- hard_policy: `home_weak_plus_distractors`
- answer_variant: `cited_answer`
- evidence_scope: `all_retrieved_evidence_uncited_claim`
- question_template: `limitations_ablation`

### Question

What limitations, ablations, or analysis findings are discussed in the paper 'VisualClaw: A Real-Time, Personalized Agent for the Physical World'?

### Claim

On FinMME, AgentFinVQA improves over a primary-backbone matched zero-shot baseline with a proprietary backbone (Gemini-3 Flash) and an open-weights system (Qwen3.6

### Evidence

```text
[1] VisualClaw: A Real-Time, Personalized Agent for the Physical World
Vision language models are serving as general-purpose interfaces for complex multimodal tasks. However, deployment still faces three gaps: VLMs typically incur high latency and cost when processing dense video frames and long prompts, the agent scaffold remains static after deployment, and standard video-QA benchmarks do not test whether agents can use visual evidence inside tool-using workspaces. We present VisualClaw, a self-evolving multimodal agent built around two principles. First, hybrid encoding reduces deployment cost by filtering less informative streaming frames with a cascaded gate and compressing the text skill bank through hot/cold top-k injection. Second, skill evolution lets the agent learn from failures: retrieved memories condition an evolver as direct concatenated context or as guided evidence, producing skill-bank updates that help future questions. Across 4 video-QA benchmarks with 2 VLMs, VisualClaw cuts per-question API cost by an average -98% versus full-frame upload and by -25.9% over the offline uniform 8 frame baseline, while boosting accuracy in most settings, e.g., an average +3.85% and a peak +15.80% on EgoSchema with Gemini 3 Flash. To address the gap, we curate VisualClawArena, a 200-scenario multimodal agentic benchmark built through a strict five-stage pipeline; models must use video evidence, documents, dynamic updates, and executable checks inside a workspace. On VisualClawArena, the same framework with computer-use agent backends improves macro accuracy by +2.9% for Codex (GPT-5.5) and +3.2% for Claude Code (Sonnet 4.6) over no-evolution baselines, with a -9.5% cost reduction compared to the uniform-sampled baseline. These properties make VisualClaw a natural fit for edge applications, where the cascade reduces a 1-hour streaming session from ~3,600 API uploads down to only 5-20 calls and the self-evolution makes it a perfect personalized assistant.

[2] SAFE-Cascade: Cost-Adaptive Vision-Language Routing for Chart Question Answering
Vision-language models (VLMs) are powerful for chart question answering, but invoking a VLM for every query can be unnecessarily expensive when many questions are answerable from OCR text and lightweight language reasoning. We demonstrate SAFE-Cascade, an interactive system for cost-adaptive chart question answering. Given a chart image and a natural-language question, SAFE-Cascade first extracts chart text with OCR, obtains a provisional answer from a text-only language model, and then uses a learned router to decide whether to accept the text answer or escalate to a VLM. The demo exposes this decision process to users: OCR evidence, text-only answer, routing probability, escalation decision, final answer, estimated cost, and estimated latency are shown side by side. SAFE-Cascade is designed as a transparent interface for understanding when visual grounding is actually needed. Users can upload or select charts, ask questions, inspect the evidence used by each pathway, compare text-only and VLM answers, and adjust the escalation threshold to explore the accuracy-cost frontier. The system is implemented with Azure Document Intelligence for OCR, gpt-5-mini as the text-only model, gemini-2.5-flash-image as the VLM, and a Random Forest router trained on inference-time features. On a held-out ChartQA test split of 375 examples from a 2,500-example experiment, SAFE-Cascade achieves 69.1% unified accuracy with 73.1% VLM invocation, compared with 67.7% accuracy and 100% VLM invocation for the full-VLM baseline. The observed +1.4 percentage-point difference is statistically uncertain, so we interpret SAFE-Cascade as matching full-VLM performance while reducing VLM calls by 26.9% and estimated cost by 9.3%. The demonstration shows how selective modality routing can make multimodal knowledge systems more transparent, tunable, and cost-aware.

[3] AgentFinVQA: A Deployable Multi-Agent Pipeline for Auditable Financial Chart QA
Financial chart question answering in regulated settings demands more than accuracy: practitioners must know which answers to trust before acting on them, and many institutions cannot send client data to external model providers. Yet existing chart-QA agents are accuracy-focused and opaque, and most assume proprietary API access; to our knowledge, none combines auditability with on-premise deployability without significant accuracy compromise. We present AgentFinVQA, a multi-agent pipeline that decomposes each query into planning, OCR, legend grounding, visual inspection, and verification, recording every step in a traceable Model Evaluation Packet (MEP) per sample. On FinMME, AgentFinVQA improves $+7.68$ pp over a primary-backbone matched zero-shot baseline with a proprietary backbone (Gemini-3 Flash; 71.24% vs. 63.56%, McNemar $p \approx 1.1 \times 10^{-16}$), and $+4.84$ pp with open-weights Qwen3.6-27B-FP8 served locally. The verifier's verdict also serves a

[TRUNCATED FOR REVIEW FILE]
```

---
