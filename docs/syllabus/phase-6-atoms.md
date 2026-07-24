# Phase 6 — TOOLS & AGENTS (it acts, not just talks)

Goal: let your assistant *do* things — check the time, do math, call an API, search — by giving it tools. This is a huge modern AI-engineer skill. 🔧 = open-the-hood atom.

| Atom | Idea you'll learn | What you'll do | You'll end up with |
|------|-------------------|----------------|--------------------|
| **6.0** | Why tools: LLMs can't act alone | See it fail at "what time is it?" | The motivation |
| **6.1 🔧** | Function calling — the model *asks* to run a function | Read how a tool-call request looks | The mechanism |
| **6.2** | Define your first tool | Write a `get_time` / calculator function | A callable tool |
| **6.3** | The tool-call loop | Wire model → tool → result → model | It uses your tool |
| **6.4** | A genuinely useful tool | Add a real API (e.g. search/weather) | A capable assistant |
| **6.5 🔧** | The **agent loop**: think → act → observe → repeat | Trace a multi-step task | The agent pattern |
| **6.6** | Multi-step tasks | Let it chain tools to finish a job | An agent that plans |
| **6.7** | Guardrails on tools | Add limits/safety to tool use | Safe actions |
| **6.8** | Wrap it up | Assistant that takes actions | **A tool-using agent** |
