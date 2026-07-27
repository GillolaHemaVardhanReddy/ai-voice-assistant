# Math Map 🧮 — where the math lives, and where we go deep

> Requested by the student (26 Jul 2026): *"analyse where we get maths and update curriculum where we learn in depth what topics."*

> **Update (27 Jul 2026):** *"don't throw LA resources at me — get the data from them and integrate the teachings into our learn-by-doing way. Any time we get a mathematical term, automatically analyse the topic in maths and teach it as a sub-atom, cleanly."*

**The principle: just-in-time, never upfront.** We do NOT stop and take a linear-algebra course. Every math topic below is introduced at the exact atom where the code needs it, worked by hand with small numbers first, then confirmed in NumPy. Same ATOM rules apply.

## How a math sub-atom is taught (the 4 beats)

Every 🧮 sub-atom runs in this order. **The order IS the lesson** — jumping to beat 3 is what breaks.

| # | Beat | Rule |
|---|---|---|
| 1 | 🖼️ **Picture** | Arrows, shapes, plots. **Zero symbols.** He must be able to *guess* the answer from the picture. |
| 2 | 🔢 **Small numbers** | 2D, single digits, by hand. Numbers he can verify mentally. |
| 3 | ✏️ **Formula** | Only now. Read aloud as an English sentence; name every symbol. |
| 4 | 💻 **Code** | NumPy confirms what he already believes. Predict-before-run. |

Then always: **connect it back to text/product** — *"…and this is why two sentences count as similar."* A math sub-atom that ends in geometry-land is unfinished.

**No external links as a substitute for teaching.** Sources (3Blue1Brown, Immersive Math, Strang) are *mined* for their best intuition and rebuilt here as atoms. A link may be offered as optional dessert **after** a concept has landed — never instead of it.

**Three depth levels:**
- 🟢 **Dose** — 2–5 min inline in the atom that needs it. No extra atoms.
- 🟡 **Block** — a small group of dedicated math sub-atoms, because the code is unbuildable without it.
- 🔵 **Deferred** — genuinely needed, but for **P2 Insight Engine**, not this project.

---

## The three deep blocks (🟡)

### M-Block A — Vector algebra  ·  *Phase 2.2–2.7 (NOW)*
The whole of RAG is one geometry idea: similar meaning = arrows pointing the same way.

| Topic | Atom | Worked by hand as | Status |
|---|---|---|---|
| Vector = list of numbers = an arrow | 2.2 | `[1,2,3]` | ✅ |
| **Dot product** | 2.2 | `1·4 + 2·5 + 3·6 = 32` | ✅ |
| **Magnitude / norm** (length via `a·a`) | 2.2a | `√14 ≈ 3.74` | ✅ |
| **Unit vector** (normalizing = dividing out length) | 2.2b | `[1,2,3] / 3.74` | ✅ |
| **Cosine similarity** = dot of the unit vectors | 2.4 | 2D "dogs vs money" → `0.998` / `0.165` | ✅ |
| 🧮 **Dot product = an AND-gate agreement score** | 2.4 | `a[i]*b[i]` summed = a JS `for` loop | ✅ |
| 🧮 **Text → arrow bridge** (a feature score list *is* a coordinate) | 2.4 | 2-feature toy space, drawn | ✅ |
| 🧮 **2.5a — Features are directions; a vector is a recipe** *(span & basis, rebuilt)* | 2.5 | 2 basis arrows → mix to reach any point | ⬜ |
| 🧮 **2.5b — Projection: the dot product is a shadow** *(duality, rebuilt)* | 2.5 | shine a light, measure the shadow of `b` on `a` | ⬜ |
| 🧮 **2.6a — Why 384-D is fine (and unpicturable)** | 2.6 | random high-D vectors are ~always near-perpendicular | ⬜ |
| 🧮 **2.7a — Search = ONE matrix × vector multiply** | 2.7 | stack 5 chunk-vectors → `(5×384)·(384,)` → 5 scores | ⬜ |

*Why a block:* without normalization, long documents beat relevant ones. This is the #1 real RAG bug and it's pure algebra. And **2.7a is where matrices genuinely arrive** — not as theory, but because searching 10,000 chunks one-at-a-time in a Python loop is too slow. That makes M-Block B feel earned rather than imposed.

#### What we take from a standard LA course — and what we skip

Mined from 3Blue1Brown *Essence of Linear Algebra* + Immersive Math, rebuilt as our own atoms:

| Standard LA topic | Our home | Verdict |
|---|---|---|
| Vectors, coordinates | 2.2 | ✅ taken |
| Linear combinations, **span**, **basis** | 2.5a | ✅ taken — *"each dimension is a direction; a text mixes them"* |
| **Dot product & duality** (projection) | 2.4, 2.5b | ✅ taken — the shadow picture |
| High-dimensional geometry | 2.6a | ✅ taken — reassurance + near-orthogonality |
| Linear transformations = **matrices** | 2.7a (intro), 7.0 (full) | ✅ taken, in two passes |
| **Matrix multiplication** as composition | 7.0, 7.3 | ✅ taken |
| **Transpose** | 7.9 (`Q·Kᵀ`) | ✅ taken |
| **Rank / low-rank factorization** | 8.6 (LoRA) | ✅ taken |
| Determinant | — | ❌ skipped — never used in this stack |
| Cross product | — | ❌ skipped — 3D-graphics tool, not ML |
| Inverse, null space, Gaussian elimination | — | ❌ skipped — we never solve linear systems |
| **Eigenvalues / eigenvectors → PCA** | P2.5 | 🔵 deferred — clustering/insight project, not RAG |

Skips are listed **on purpose**: the completeness promise means naming what we don't teach and why, never quietly omitting it.

### M-Block B — Matrices  ·  *start of Phase 7 (before 7.0)*
A neural network layer **is** a matrix multiply. Attention is three of them.

| Topic | Needed by | Worked by hand as |
|---|---|---|
| Matrix = stack of vectors; **shapes** `(rows, cols)` | 7.0 | 2×3 by hand |
| **Matrix × vector** = many dot products at once | 7.0 | one neuron → one layer |
| **Matmul** + why inner dimensions must match | 7.0, 7.3 | `(2×3)(3×2)` |
| **Transpose** | 7.9 | why `Q·Kᵀ` |
| Broadcasting (NumPy/PyTorch shape rules) | 7.3, 7.5 | shape-error decoding |

*Why a block:* 90% of PyTorch errors a beginner hits are shape errors. Understanding shapes = debugging superpower.

### M-Block C — Calculus for backprop  ·  *Phase 7.2–7.3*
The one genuinely new branch of math in this project — and the payoff is understanding how *all* learning works.

| Topic | Needed by | Worked by hand as |
|---|---|---|
| **Derivative = slope** | 7.2 | `f(x)=x²` at x=3 → 6 |
| **Gradient descent** = step downhill | 7.2 | 3 iterations on paper |
| **Learning rate** (too big overshoots) | 7.2 | same function, 2 rates |
| **Chain rule** | 7.3 | nested function, 2 layers |
| **Partial derivatives / gradient vector** | 7.3 | one weight at a time |
| **Cross-entropy loss** ↔ log-probability | 7.1 | reconnects to softmax (1.3 ✅) |

*Why a block:* backprop IS the chain rule. Everything else in Phase 7 is bookkeeping around it.

---

## The doses (🟢) — inline, no extra atoms

| Math | Where | What we do |
|---|---|---|
| Probability, **softmax**, temperature | 1.3–1.4 ✅ **done** | Worked by hand incl. negative scores |
| Log-probs, top-k / top-p sampling, entropy | 7.13 | Why sampling ≠ argmax |
| **Sampling rate, amplitude** (audio as numbers) | 3.0 | Read raw `.wav` values |
| **Frequency / mel spectrogram** intuition (Fourier, no proofs) | 3.2 | Visual reference only |
| **√dₖ scaling** in attention (why divide) | 7.9 | Variance intuition, small numbers |
| **sin/cos positional encoding** | 7.11 | Plot two positions |
| **Masking with −∞** (why not 0) | 7.10 | Trace through softmax |
| **Matrix rank / low-rank factorization** → LoRA | 8.6 | Why `A·B` ≪ full weights |
| **Eval statistics** — accuracy/precision/recall, small-sample caution | 10.4 | Score a 20-question eval set |
| **Unit economics** — cost/conversation, margin at N users | 10.0, 10.8 | Real arithmetic on real bills |

---

## Deferred to P2 — Insight Engine (🔵)

Real math, genuinely not needed here — and forcing it in would be theory-for-theory's-sake:

| Topic | Lands in |
|---|---|
| Distributions, hypothesis testing, A/B tests | P2.1 |
| Regression math, loss/regularization (L1/L2) | P2.2 |
| Information gain / entropy in trees, boosting math | P2.3 |
| **Eigenvalues & eigenvectors → PCA**, k-means objective | P2.5 |
| TF-IDF / BM25 scoring math | P2.6 |
| Time-series math (ARIMA-lite), RNN/LSTM gates | P2.7 |

**Combined promise:** P1 (this project) + P2 = the full applied-math stack for AI/ML — linear algebra, calculus, probability, statistics, optimization, information theory — every piece implemented by hand in a shipped project, none of it as a dry course.

---

## Curriculum changes this map introduces

1. **Phase 2 gained 2 sub-atoms (26 Jul):** `2.2a` norm/magnitude, `2.2b` unit vectors — inserted before 2.3. ✅ done
2. **Phase 7 gains a pre-block:** `7.-1` matrices & shapes, before the first neuron.
3. **Phase 2 gains 4 more 🧮 sub-atoms (27 Jul, LA integration):** `2.5a` span/basis as "features are directions", `2.5b` projection/duality as "the shadow", `2.6a` high-dimensional intuition, `2.7a` search as one matrix multiply. These replace the idea of sending him to an external LA course.
4. **Standing rule added to `.claude/CLAUDE.md`:** every mathematical term auto-becomes a 🧮 sub-atom with the 4 beats (picture → numbers → formula → code). Links are dessert, never the meal.
5. Everything else stays as-is; math arrives as doses at the listed atoms.
