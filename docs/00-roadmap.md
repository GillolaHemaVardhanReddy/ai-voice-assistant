# Roadmap — Build-While-Learn, Point 0 → AI Engineer

**Method:** we build the voice assistant and *open the hood on each concept exactly when we use it.* No long upfront theory — theory is always attached to a real build need. You reach a working (even sellable) assistant fast, and still cover the deep internals end to end.

Each phase ends with **working code**. One atom per turn. Nothing moves on until it runs and makes sense.

| Phase | You build | You open the hood on |
|-------|-----------|----------------------|
| **1 · The Brain** | a text chatbot | tokens, probability, **softmax**, temperature |
| **2 · Memory & RAG** | answers from your data | NumPy, vectors, **cosine similarity**, embeddings |
| **3 · The Ears** | speech → text (Whisper) | audio as numbers, spectrograms, *a transformer, live* |
| **4 · The Mouth** | text → voice | how neural TTS makes sound |
| **5 · The Loop** | hands-free conversation | streaming, latency, voice-activity detection |
| **6 · Tools & Agents** | an assistant that *acts* | function calling, the agent loop |
| **7 · Under the Hood ★** | *(the deep dive)* a tiny LLM | neurons → **backprop** → PyTorch → **attention & masking** → train a mini-LLM |
| **8 · Fine-tuning** | your own customized model | Hugging Face, datasets, **LoRA/PEFT**, evaluation |
| **9 · The Product: API + SDK** | the assistant as an integratable API/SDK, then the browser app as its first consumer | API design, auth/keys, React + Node + Mongo, mic capture, streaming UI |
| **10 · Cheap & Sellable** | a deployable product | cost modeling, open models, **evals**, guardrails, deploy |

**Milestones along the way:**
- After **Phase 2** → a smart assistant that knows your data.
- After **Phase 5** → it *talks* with you, hands-free.
- After **Phase 7** → you *understand LLMs for real* (math included).
- After **Phase 9/10** → a real, sellable web product.

> Phase 0 (your teacher, repo, and this syllabus) is done ✅. Near phases are stable; far phases (7–10) are a living draft we refine as we approach them.
