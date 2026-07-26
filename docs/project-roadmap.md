# Master AI Engineer — Project Roadmap 🗺️

> **STATUS: PARKING LOT, NOT A CONTRACT.** Nothing below P1 is decided. Protocol: before each project/phase we hold a short **discussion gate** — Acharya presents options + recommendation, the student decides, THEN it gets planned in detail. Tools/atoms are chosen only when we arrive, based on what's best and production-current at that time. This doc just keeps ideas from getting lost.

The portfolio path (hemavardhanreddy.vercel.app): **4 projects**, each build-while-learn, each shipped as a portfolio card. Together they cover the full AI/ML landscape — LLM engineering (Track B) AND classical ML / data science (Track A) — with zero dry theory courses.

**Rule carried over from P1:** every phase of every project ends with a **ship-it atom** — README + demo GIF + "what's under the hood" write-up → portfolio card.

**Atomization rule:** the CURRENT project is fully atomized; future projects stay module-level living drafts, atomized when we arrive (same as P1's far phases).

---

## P1 — AI Voice Assistant *(CURRENT — in progress)*
**The product:** API-first voice assistant (STT → LLM → TTS), sold cheap. **Business use:** the sellable product itself.

Covers (= `foundations-map.md` F1–F17): Python, softmax & probability ✅, embeddings/RAG, vector math, Whisper/TTS, real-time streaming, agents & tool-calling, **backprop by hand → PyTorch → attention/transformers → train a mini-LLM**, **Hugging Face fine-tuning + LoRA (production-grade, real-time serving — the student's explicit priority)**, React/Node product, evals/guardrails/cost engineering, deploy.

Status: Phase 1 ✅ → syllabus in `docs/syllabus/`, progress in `docs/progress.md`.

---

## P2 — Insight Engine *(next after P1)*
**The product:** an ML analytics & intelligence platform that eats **P1's real usage data** (users, conversations, costs) and makes business decisions from it. Portfolio story: *"I built an AI product, then built the ML platform that runs its business."* The two feed each other — Insight Engine's models get deployed back INTO the assistant (e.g., the cost router).

**Business use:** churn prevention, cost optimization, product analytics — the exact ML that companies pay for.

Modules (living draft — atomized when we start):
1. **Data & stats foundations** — pandas, distributions, hypothesis testing, A/B tests on real product data
2. **Regression track** — linear → logistic (predict user churn); loss/regularization for real
3. **Tree track** — decision tree → random forest → **XGBoost / gradient boosting** (churn + intent classification); feature importance
4. **The cost router** 🔁 — classify message difficulty, route Haiku vs big model; **deployed back into P1** = classical ML in production
5. **Unsupervised track** — **k-means** (user/topic segmentation), hierarchical, DBSCAN, **PCA/t-SNE** visual dashboards
6. **Classical NLP track** — TF-IDF + BM25 search, word2vec; benchmark vs P1's embeddings
7. **Time-series track** — forecast API usage/cost: classical (moving avg/ARIMA-lite) vs **RNN/LSTM** (finally meet the pre-transformer world hands-on)
8. **Recommender mini-module** — suggest features/content to users (collaborative filtering)
9. **Full MLOps** — MLflow/W&B experiment tracking, model registry, **scheduled retraining pipeline, drift monitoring** — production-grade
10. **Dashboard product** — React analytics UI (portfolio centerpiece)

Covers the classical syllabus: math/stats ✓, ML algorithms ✓, gradient boosting ✓, optimization ✓, clustering ✓, RNN/LSTM ✓, classical NLP ✓, MLOps ✓, scikit-learn stack ✓.

---

## P3 — Eyes *(after P2)*
**The product:** give the assistant **vision** — a multimodal upgrade (screenshot understanding, "what am I looking at?", image search) — plus the deep CV fundamentals under it.

Modules (living draft): CNNs from scratch (convolutions by hand → PyTorch) → data augmentation & transfer learning → object detection → **CLIP embeddings** (image search that reuses P1's RAG math!) → vision transformers → multimodal LLM calls in production.

Covers: computer vision, CNNs, ViT, multimodal — the last big deep-learning pillar.

---

## P4 — Automation Studio *(weekend-scale, after P2)*
**The product:** n8n + custom-code workflows that sell P1 as automations (voice bot answering business FAQs, call summaries → CRM, etc.). Small project, big freelance value.

Covers: n8n, webhooks at scale, integration engineering — the "boxes" we already built the engine for in P1 Phase 6.

---

## Future foundations ledger (beyond P1's F1–F17)
| # | Foundation | Project |
|---|-----------|---------|
| F18 | Stats & experimentation (A/B, hypothesis testing) | P2.1 |
| F19 | Classical supervised ML (regression → trees → boosting) | P2.2–2.4 |
| F20 | Unsupervised ML (clustering, PCA) | P2.5 |
| F21 | Classical NLP + RNN/LSTM lineage | P2.6–2.7 |
| F22 | Production MLOps (tracking, registry, retraining, drift) | P2.9 |
| F23 | Computer vision (CNN → ViT → CLIP, multimodal) | P3 |
| F24 | Integration/automation engineering | P4 |

**The promise, extended:** P1–P4 complete = every topic on the standard AI/ML syllabus implemented in a shipped, business-usable project. Master-AI-engineer map with no holes.
