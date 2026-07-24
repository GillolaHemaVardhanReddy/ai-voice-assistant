# Phase 5 — The LOOP (real-time conversation)

Goal: wire ears → brain → mouth into a live, hands-free back-and-forth. It becomes a real voice assistant. 🔧 = open-the-hood atom.

| Atom | Idea you'll learn | What you'll do | You'll end up with |
|------|-------------------|----------------|--------------------|
| **5.0** | The pipeline in code | `listen() → think() → say()` | The whole loop on paper |
| **5.1** | One full spoken turn | Chain the three functions once | Speak once, spoken reply |
| **5.2** | Knowing when you stopped talking (VAD) | Add voice-activity detection | Hands-free turns |
| **5.3 🔧** | Latency budget — where seconds go | Measure each step's time | Know your bottlenecks |
| **5.4** | Streaming to feel instant | Start TTS before the LLM finishes | A snappy reply |
| **5.5** | Barge-in (interrupt) — *optional* | Let the user cut in | Natural feel |
| **5.6** | Wrap it up | A continuous conversation loop | **A talking assistant** |
