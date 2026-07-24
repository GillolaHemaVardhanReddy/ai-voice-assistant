# Phase 9 — The PRODUCT: API-first + SDK (your MERN turf)  *(living draft)*

Goal: package the assistant as a **clean API any app can integrate** — like an SDK — then build your own web app as its *first consumer*. This is the shape sellable AI products take: others embed your assistant, not just use your site. 🔧 = open-the-hood atom.

| Atom | Idea you'll learn | What you'll do | You'll end up with |
|------|-------------------|----------------|--------------------|
| **9.0** | API-first architecture: core as a service | Sketch: core API ↔ any client (web/mobile/3rd-party) | The product shape |
| **9.1** | The brain endpoint | Express route: text in → reply out | An AI API you own |
| **9.2** | Voice endpoints | STT + TTS + full-pipeline routes | The whole assistant as HTTP |
| **9.3** | Streaming over HTTP | SSE / WebSocket live replies | Real-time API |
| **9.4** | Auth & API keys | Issue keys, protect routes | Integratable by others |
| **9.5 🔧** | How the browser captures audio | `MediaRecorder` / WebAudio | Browser records you |
| **9.6** | Your first consumer: the React app | Chat UI + hold-to-talk calling YOUR api | The web product |
| **9.7** | Persistence | Conversations/users in MongoDB | A real app |
| **9.8** | SDK packaging | A tiny npm client (`assistant.chat()`, `assistant.speak()`) + docs | **A drop-in SDK** |
| **9.9** | Wrap it up | Second consumer demo (few lines, new app) | **Proof it integrates anywhere** |

> Far-phase draft: exact shape refined once the loop exists.
