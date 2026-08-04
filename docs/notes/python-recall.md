# 🔁 Python Recall — dragging the old repo back into reach

Standing order (student's call, 4 Aug 2026): *"keep recalls at every new session start so slowly by the time passes we can catch up all the forgotten learnings i did in that repo."*

Source material = his own repos, mainly `GillolaHemaVardhanReddy/python`. **Revise from his code, never re-teach from zero.**
Warm-up question 3 each session comes from the sweep list below.

---

## 🗺️ Sweep tracker — one old-repo topic per session

| Topic | Where it lives in his repo | Status |
|---|---|---|
| `week1` basics (types, loops, f-strings) | `week1/` | ⬜ not swept |
| OOP — class / `__init__` / `self` | `week2/4.class_objects`, `5.inheritance`, `6.oops` | ✅ swept (Atom 2.0a–e, Session 3) |
| Iterators & generators | `week2/7.itergendecorator` | ✅ swept (Session 10 — `list(g)` one-shot) |
| Decorators (incl. factories) | `week2/7.itergendecorator` | ✅ swept (Atom 2.10a S8, factory recalled clean S9) |
| **Context managers — `with`** | `week2/7.itergendecorator` (`@open_file`) | 🟡 **half swept (S11 — the guarantee ✅; `__enter__`/`__exit__` PARKED → next session)** |
| NumPy / Pandas | `week3/1.numpypandas`, repo `datascience` | ⬜ not swept |
| SQLite module | `week3/2.Module_SQLite3` | ⬜ not swept |
| Flask routes | `flask SELFLEARN/app.py` | 🟡 partly used as the FastAPI bridge (S8) |
| PyTorch tensors / autograd / NNs | `pytorch_selflearn/0–5` | ⬜ not swept — **check depth before Phase 7** |

---

## Session 11 — `with` = a door that closes itself behind you

💡 **Idea:** `open()` leaves the file hanging open if your code crashes before `close()`. `with` guarantees the close — trip or not, the door shuts behind you.

💻 **The line that matters:**
```python
with open("note.txt", "w") as f:
    f.write("hello")

print("closed?", f.closed)   # True
```
Without `with`, the same print gives `False` — he ran both, saw `False` → `True`.

⚠️ **Gotchas:**
- `f` still exists *after* the block — **only the door closed, not the variable.**
- `python: command not found` on Ubuntu — the system only ships `python3`. The bare `python` comes from the **venv's own `bin/`**, so `source venv/bin/activate` first.

<details>
<summary>❓ self-test</summary>

1. After a `with open(...) as f:` block ends, is `f` gone? What *is* different about it?
2. Your code raises inside the `with` body. Does the file still get closed? Does the exception still crash the program?
3. Which two methods does an object need before Python will let it sit after `with`? *(parked — next session)*
</details>

---

## Warm-up scoreboard

| Session | Q1 (last) | Q2 (~3 back) | Q3 (old repo) | Score |
|---|---|---|---|---|
| 11 | two kinds of "not 1" ✅ | per-attempt timeout ✗ | `with` / context managers ✗ → taught | 1/3 |
