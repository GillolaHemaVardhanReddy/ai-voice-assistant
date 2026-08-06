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
| **Context managers — `with`** | `week2/7.itergendecorator` (`@open_file`) | ✅ **swept (S11 the guarantee; S12 recalled clean — closes AND still raises).** `__enter__`/`__exit__` still untaught — teach only when we *write* one. |
| **Default arguments / mutability** | (new — not from the old repo) | ✅ swept S12 — `bag=[]` leaks across calls; see the card below |
| NumPy / Pandas | `week3/1.numpypandas`, repo `datascience` | 🟡 **half swept (S13)** — `list*2` vs `array*2`, `*` is `__mul__` on the type, `@` = dot product (`140`), `vecs @ q` → 127 scores. **Pandas untouched**, and NumPy indexing/slicing/`argsort`/broadcasting-with-shapes still owed. |
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

## Session 12 — mutable default arguments: the bag is nailed to the function

💡 **Idea:** a default value is created **once, when `def` runs** (import time), and stapled to the function object. Every call reaches for that same object. `k=5` is safe — you can't mutate `5`. `bag=[]` is not.

💻 **The line that matters:**
```python
def add(item, bag=[]):
    bag.append(item)
    return bag

print(add("a"))   # ['a']
print(add("b"))   # ['a', 'b']   ← the SAME bag, not a new one
```
The fix, and the reason `rag_v2.py` reads the way it does:
```python
def answer(question, history=None, k=5):
    history = history or []     # the [] now runs per CALL, not per import
```

⚠️ **Gotchas:**
- On a **public endpoint** this is a data leak, not a curiosity: recruiter A's history splices into recruiter B's prompt, silently, until the container restarts.
- **`history: list[Turn] = []` in a Pydantic model is SAFE** — Pydantic deep-copies field defaults per instance. Same syntax, opposite behaviour, because a different machine is building the object.
- Same import-time fact as P1.7.0's decorator: **`def` builds an object; a name is just a sticky label on it.**

<details>
<summary>❓ self-test</summary>

1. When is the `[]` in `def add(item, bag=[])` created — at import, or on each call?
2. Why is `k=5` immune to the same bug?
3. `history = history or []` — what does the `or` actually do here, and what does it treat the same as `None`?
4. Pydantic's `history: list[Turn] = []` looks identical and is safe. Why?
</details>

---

## Warm-up scoreboard

| Session | Q1 (last) | Q2 (~3 back) | Q3 (old repo) | Score |
|---|---|---|---|---|
| 11 | two kinds of "not 1" ✅ | per-attempt timeout ✗ | `with` / context managers ✗ → taught | 1/3 |
| 12 | two `ask` handlers ✗ *(had the FastAPI half, missed names-vs-objects)* | Pydantic ✗ **backwards** — said missing fields are dropped; it's **422 at the door** | `with` + exception ✅ **both halves** — S11's park closed | 1.5/3 |
| 13 | Pydantic **half** — has the bouncer now, posted him at the wrong door (said *both* bodies 422; extra fields are silently dropped, only the missing one bounces) | index staleness — **outcome ✅, mechanism ✗** (didn't have *`store.py` loads `index.npz`, never the `.txt`*) | **NumPy ✗** — had the types (`list`/`array`), not the values → taught as a sub-atom, `@` landed | 1/3 |
