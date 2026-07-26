# Math Map 🧮 — where the math lives, and where we go deep

> Requested by the student (26 Jul 2026): *"analyse where we get maths and update curriculum where we learn in depth what topics."*

**The principle: just-in-time, never upfront.** We do NOT stop and take a linear-algebra course. Every math topic below is introduced at the exact atom where the code needs it, worked by hand with small numbers first, then confirmed in NumPy. Same ATOM rules apply.

**Three depth levels:**
- 🟢 **Dose** — 2–5 min inline in the atom that needs it. No extra atoms.
- 🟡 **Block** — a small group of dedicated math sub-atoms, because the code is unbuildable without it.
- 🔵 **Deferred** — genuinely needed, but for **P2 Insight Engine**, not this project.

---

## The three deep blocks (🟡)

### M-Block A — Vector algebra  ·  *Phase 2.2–2.5 (NOW)*
The whole of RAG is one geometry idea: similar meaning = arrows pointing the same way.

| Topic | Atom | Worked by hand as |
|---|---|---|
| Vector = list of numbers = an arrow | 2.2 ✅ | `[1,2,3]` |
| **Dot product** | 2.2 ✅ | `1·4 + 2·5 + 3·6 = 32` |
| **Magnitude / norm** (length via `a·a`) | 2.2a | `√14 ≈ 3.74` |
| **Unit vector** (normalizing = dividing out length) | 2.2b | `[1,2,3] / 3.74` |
| **Cosine similarity** = dot of the unit vectors | 2.4 | 2D vectors, angle by hand |
| Why high dimensions are fine (and unpicturable) | 2.4 | 384-D reassurance |

*Why a block:* without normalization, long documents beat relevant ones. This is the #1 real RAG bug and it's pure algebra.

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

1. **Phase 2 gains 2 sub-atoms now:** `2.2a` norm/magnitude, `2.2b` unit vectors — inserted before 2.3.
2. **Phase 7 gains a pre-block:** `7.-1` matrices & shapes, before the first neuron.
3. Everything else stays as-is; math arrives as doses at the listed atoms.
