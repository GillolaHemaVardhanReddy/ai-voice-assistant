# Master AI Engineer — Project Roadmap 🗺️

> **STATUS: PARKING LOT, NOT A CONTRACT.** Nothing below P1 is decided. Protocol: before each project/phase we hold a short **discussion gate** — Acharya presents options + recommendation, the student decides, THEN it gets planned in detail. Tools/atoms are chosen only when we arrive, based on what's best and production-current at that time. This doc just keeps ideas from getting lost.

The portfolio path (hemavardhanreddy.vercel.app): **4 projects**, each build-while-learn, each shipped as a portfolio card. Together they cover the full AI/ML landscape — LLM engineering (Track B) AND classical ML / data science (Track A) — with zero dry theory courses.

**Rule carried over from P1:** every phase of every project ends with a **ship-it atom** — README + demo GIF + "what's under the hood" write-up → portfolio card.

**Atomization rule:** the CURRENT project is fully atomized; future projects stay module-level living drafts, atomized when we arrive (same as P1's far phases).

---

## 🏛️ DECIDED 13 Aug 2026 (S20, his call) — **the voice agent splits off as its own project**

**His words:** *"the voice agent will be my new project itself but at one point i want to give my rag the voice and ears too."*

- **Spidy stays the RAG product** — text today, and later grows ears + a mouth so a recruiter can *talk* to it.
- **The real-time voice loop becomes its own repo/project** — Phases 3–5 are built there, properly, not bolted onto Spidy.
- **The seam:** the voice project exposes reusable `listen()` / `say()` modules; **Spidy becomes their first consumer** — exactly the API-first shape Phase 9 already commits to. No throwaway work either way.
- ⇒ Phases 3–5 stop being "a detour from Spidy" and become a product in their own right. Update the syllabus framing when we arrive at 3.0.

## 💰 DECIDED 13 Aug 2026 (S20) — **local models are for LEARNING, so they run on his Mac. Hosting stays ₹0.**

**His answers:** goal for local models = *"just i want to see how they work"* · budget = **₹800/month total, OpenRouter included.**

**The rule that keeps it free: no model weights ever enter the production container.** That is the whole reason 63 MB fits Render's 512 MB.

| | where it runs | cost |
|---|---|---|
| React widget | Vercel | ₹0 |
| FastAPI + `index.npz` | Render free (63 MB RSS, zero models) | ₹0 |
| Embeddings + LLM | OpenRouter | **~₹45/mo** at current traffic |
| **Whisper · Piper · Ollama** | **his MacBook**, exposed on demand via **Cloudflare Tunnel** | ₹0 |

- **Three weight classes, not one problem** — sorting them is what made ₹0 possible. **Reranker** ~90 MB → **~25 MB quantized ONNX** = the *only* candidate that could ever ship (the `fastembed`/`onnxruntime` road he already walked at P1.6, minus the sympy bloat he diagnosed). **Whisper** 150 MB–1.5 GB and **local LLM** 2–8 GB = never on a free tier; Mac only. **Piper** ~60 MB — revisit at Phase 4.
- **If a local model ever earns production, it crosses as a quantized ONNX file, not as PyTorch.**
- ⚠️ **The risk is a runaway, not the monthly bill.** A hammered public endpoint turns ₹45 into ₹4,500. Defenses already built (CORS, per-IP rate limit, spend cap) — **keep the cap set below ₹800.**
- **Rejected, and why:** Oracle Always Free (24 GB, but ARM + capacity roulette) · Hetzner ~€4/mo · Fly.io ~$6–11/mo · Cloud Run pay-per-request. All real options, none needed *while the goal is learning*. Revisit only if a local model must be always-on.
- **Image techniques still unused when we need them:** multi-stage build · ONNX int8 quantization · weights on a volume · distroless base. ⚠️ Verify Render/OpenRouter pricing before relying on any figure above.
- 🗺️ **Drawn:** `docs/pipeline-map.html` — the pipeline as data flow + build-vs-run + the ₹0 plan.

---

## P1 — AI Voice Assistant *(CURRENT — in progress)*
**The product:** API-first voice assistant (STT → LLM → TTS), sold cheap. **Business use:** the sellable product itself.

Covers (= `foundations-map.md` F1–F17): Python, softmax & probability ✅, embeddings/RAG, vector math, Whisper/TTS, real-time streaming, agents & tool-calling, **backprop by hand → PyTorch → attention/transformers → train a mini-LLM**, **Hugging Face fine-tuning + LoRA (production-grade, real-time serving — the student's explicit priority)**, React/Node product, evals/guardrails/cost engineering, deploy.

Status: Phase 1 ✅ → syllabus in `docs/syllabus/`, progress in `docs/progress.md`.

---

## P1.5 — Recruiter Bot *(rides along with P1 — student's call, 26 Jul 2026)*
**The product:** a chatbot on hemavardhanreddy.vercel.app that knows the student end-to-end and answers recruiter questions from his real documents (resume, project READMEs, story). Later: replies to recruiter emails.

**Not a side-track** — it *is* P1 Phase 2 (RAG) pointed at the student's own data instead of toy text. Ships in 3 gated versions:

| Ver | Gate | Adds | Why that gate |
|-----|------|------|---------------|
| **v1** | after **Phase 2** (+2–3 sessions) | RAG over his docs + React widget + Express endpoint, deployed | Phase 2 is the engine; the MERN half is the student's existing strength, so it's cheap to pull forward |
| **v2** | after **Phase 6** | reads + drafts email replies | Email replying = agent with tools. Before Phase 6 it's a hack. |
| **v3** | after **Phase 10** | voice (recruiters *talk* to it), evals, cost caps | needs the full loop + guardrails |

**Timing rationale:** the student has an active job search — a live bot in ~3 weeks beats a perfect one in 6 months.

**What makes it postworthy (aim Phase 2 atoms at these):**
1. **Says "I don't know"** instead of inventing experience — *hard honesty requirement*, this bot represents a real person to people who may hire him. Must never fabricate credentials.
2. **Cites its source** ("from his 2024 project README")
3. **Published retrieval eval** — 20 real recruiter questions, hit-rate measured and stated in the README
4. **Cost + rate limiting** — recruiters can't run up the API bill; cost/conversation in the README
5. **Write-up of chunking decisions** — why the resume was split that way, what broke first

Items 1–3 & 5 are free byproducts of Phase 2. Item 4 is an afternoon of Express middleware.

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
