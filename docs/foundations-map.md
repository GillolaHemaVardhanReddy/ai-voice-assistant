# Foundations Coverage Map 🎓

**The promise:** by the end of this project, every foundation an AI engineer needs is learned **and implemented by you**. This table is the guarantee — each foundation maps to the exact atoms where you build it. If something were missing, it would show here as a hole.

| # | Foundation | Where you implement it | Status |
|---|------------|------------------------|--------|
| F1 | Python + NumPy for AI | venv/packages 1.0 · NumPy & vectors 2.2 · used everywhere after | ⬜ |
| F2 | Math: probability & **softmax** | 1.3 (code softmax) · 1.4 (temperature) | ✅ |
| F3 | Math: linear algebra (vectors, dot product, matmul) | 2.2, 2.4 (cosine by hand) · 7.9 (Q·K·V matmul) | ⬜ |
| F4 | Embeddings & similarity | 2.3–2.7 (embed, cosine, vector store, retrieval) · 7.7 | ⬜ |
| F5 | RAG | 2.6–2.9 | ⬜ |
| F6 | Audio & speech models (STT/TTS) | 3.0–3.6 · 4.0–4.6 | ⬜ |
| F7 | Real-time AI systems (streaming, latency, VAD) | 1.7 · 5.0–5.6 | ⬜ |
| F8 | Tool use & **agents** | 6.0–6.8 | ⬜ |
| F9 | Math: gradients & calculus-for-learning | 7.2 (gradient descent from scratch) | ⬜ |
| F10 | Neural nets: neuron, loss, **backpropagation** | 7.0–7.4 (2-layer net, pure NumPy) | ⬜ |
| F11 | **PyTorch** (tensors, autograd, training loop) | 7.5–7.6 | ⬜ |
| F12 | **Transformers**: attention, **causal masking**, multi-head, positional encoding | 7.7–7.12 | ⬜ |
| F13 | Training a language model end-to-end | 7.13 (train a mini-LLM) | ⬜ |
| F14 | **Hugging Face** ecosystem | 8.2–8.3 | ⬜ |
| F15 | Fine-tuning + **LoRA/PEFT** | 8.4–8.6 | ⬜ |
| F16 | **Evaluation** & guardrails | 8.7 · 10.4–10.6 | ⬜ |
| F17 | AI product engineering (APIs, prompting, cost, deploy) | 1.x · 9.x · 10.x | ⬜ |
| **F18** | **Production retrieval engineering** — reranking, hybrid search, chunking strategy, ANN & vector DBs, retrieval evals | 2.10–2.14 | ⬜ |
| **F19** | **Tokenization** — BPE, vocabulary, why cost/multilingual/spelling behave as they do | 7.6a | ⬜ |
| **F20** | **Inference optimisation & local serving** — quantization, KV cache, batching, runtimes | 10.1a–10.1c | ⬜ |

Tick each ⬜ → ✅ as its atoms complete. All 20 checked = **you have the working foundations of an AI engineer, proven by things you built.**

---

## 🔍 Audit — 8 Aug 2026 (he asked: *"i dont trust you that you didnt keep all the topics in the plan"*)

He was right. A grep of every file in `docs/` found three foundations with **no atom anywhere in the syllabus**. They are now **F18–F20** above.

| Topic | Occurrences in `docs/` before this audit | Verdict |
|---|---|---|
| vector DB / FAISS / pgvector / Qdrant / Pinecone | **1** — a one-line aside in a notes file | ❌ no atom → **F18** |
| reranking | **1** — the parenthetical *"(later: reranking)"* | ❌ no atom → **F18** |
| BM25 / hybrid search | parked in a **different future project** (`project-roadmap.md` P2) | ❌ not this project → **F18** |
| chunking strategy (overlap, parent-doc) | 2.6 says *"split a doc"* and stops | ❌ no atom → **F18** |
| tokenization / BPE | **2** — one reference *link*, one *"tour `tokenizers`"* inside 8.2 | ❌ never built → **F19** |
| quantization / GGUF / int8 | **2** — both about float rounding, unrelated | ❌ no atom → **F20** |
| KV cache / batching | **0** | ❌ no atom → **F20** |

**Why F18 mattered most:** F5 (RAG) was scoped to atoms 2.6–2.9 — which is *stage 1* of an eight-rung ladder. Stages 3–6 (retrieval quality, self-correction, evaluation, production economics) had no home.

**Why F19 mattered:** Phase 1 taught tokens as a *cost unit*, and Phase 7 trains a mini-LLM — which needs a tokenizer. It was assumed, never built.

**Why F20 mattered:** atom 10.1 says *"local Whisper + Piper + open LLM (Ollama)"* — but nothing anywhere says how to make a local model **fast enough to use**. That's the whole difficulty of going open-source, and it was a blank.

**Deliberate exclusions (not gaps — decided, documented):** classical ML, MLOps, computer vision and n8n live in future projects P2–P4 (`project-roadmap.md`). PCA / dimensionality reduction deferred to P2 (`math-map.md`).
