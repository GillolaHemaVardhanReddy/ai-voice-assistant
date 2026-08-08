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

## Session 14 — a name is a sticky label; the decorator took the object

💡 **Idea:** two `def ask()` in one file — the second **does** clobber the name. FastAPI doesn't care, because `@app.post(...)` ran at **import time** and filed away the **function object**, never the name. *Missed three sessions running (S12, S13, S14) — so this time he ran it.*

💻 **The proof he typed (no FastAPI, plain Python):**
```python
phonebook = []

def ask():
    return "v1"

phonebook.append(ask)      # stores the OBJECT

def ask():
    return "v2"            # the NAME now points elsewhere

print("name says:", ask())          # v2
print("phonebook says:", phonebook[0]())   # v1  ← still alive
```
He predicted **v2 / v1** correctly. Bridge: `@app.post("/v2/ask")` ≡ `ask = app.post("/v2/ask")(ask)` — **`app.post(...)(...)` IS the `phonebook.append`.**

⚠️ **Gotchas:**
- Same import-time fact as `bag=[]` in S12: **`def` builds an object once; the name is just a label on it.**
- The real cost isn't a crash, it's **blindness** — every log line and traceback frame from *either* route says `ask`. Rename `ask_v2` before v2 ships.

<details>
<summary>❓ self-test</summary>

1. Two `def ask()` in one file, both decorated with different routes. Which one does `ask()` call? Which one does `/ask` serve?
2. When does `@app.post("/x")` actually run — at import, or on the first request?
3. Rewrite `@app.post("/x")\ndef f(): ...` without the `@` syntax.
</details>

---

## Warm-up scoreboard

| Session | Q1 (last) | Q2 (~3 back) | Q3 (old repo) | Score |
|---|---|---|---|---|
| 11 | two kinds of "not 1" ✅ | per-attempt timeout ✗ | `with` / context managers ✗ → taught | 1/3 |
| 12 | two `ask` handlers ✗ *(had the FastAPI half, missed names-vs-objects)* | Pydantic ✗ **backwards** — said missing fields are dropped; it's **422 at the door** | `with` + exception ✅ **both halves** — S11's park closed | 1.5/3 |
| 13 | Pydantic **half** — has the bouncer now, posted him at the wrong door (said *both* bodies 422; extra fields are silently dropped, only the missing one bounces) | index staleness — **outcome ✅, mechanism ✗** (didn't have *`store.py` loads `index.npz`, never the `.txt`*) | **NumPy ✗** — had the types (`list`/`array`), not the values → taught as a sub-atom, `@` landed | 1/3 |
| 14 | two `ask` handlers ✗ **3rd miss** — *"routes are namespaces like C++"*. Fixed with a **6-line phonebook proof he ran himself** (see card below) | Pydantic ✗ **3rd session wrong, same half** — said extras are rejected; **extras are silently dropped**. Stop asking it and make him *watch* a 422 instead | `with` + exception ✅✅ crisp, unprompted | 2/3 |
