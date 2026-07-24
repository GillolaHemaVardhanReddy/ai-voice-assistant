# Phase 1 — The BRAIN (text chat)

Goal: a terminal chatbot you type to and understand line by line. 🔧 = open-the-hood atom.

| Atom | Idea you'll learn | What you'll do | You'll end up with |
|------|-------------------|----------------|--------------------|
| **1.0** | Isolated Python env + packages | Make a venv, install `anthropic`, put key in `.env` | A ready workspace |
| **1.1** | An LLM call = a REST call | Run ~5 lines: "say hi in 5 words" | Your first AI reply |
| **1.2** | Tokens = what you pay for | Print `usage` from the response | Cost in real numbers |
| **1.3 🔧** | How the model picks the next word: probability + **softmax** | Code softmax on 3 small numbers by hand | The core mechanism |
| **1.4** | Temperature = the softmax knob | Run one prompt at temp 0 vs 1 | Feeling randomness live |
| **1.5** | System prompt = personality/rules | Add a system prompt, watch behavior change | A character you control |
| **1.6** | The model is *stateless* → memory = resending history | Send a 2-turn conversation | Real conversation memory |
| **1.7** | Streaming = tokens arriving live | Switch to streaming output | The "typing" effect |
| **1.8** | Wrap it in a loop | Build a `while` chat loop | **A working chatbot** |
