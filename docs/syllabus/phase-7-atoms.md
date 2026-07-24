# Phase 7 — UNDER THE HOOD ★ (the deep dive)

Goal: you asked to *understand any AI deeply* — this is it. Build a neural network, then a transformer, **from scratch**, by hand. By the end you can explain and code what's inside an LLM. Everything is hands-on. 🔧 = core theory+implementation.

Because it's the big one, it's grouped into three runs. Still one atom per turn.

### Run A — Neural networks from scratch
| Atom | Idea | You implement |
|------|------|---------------|
| **7.0 🔧** | A neuron = weighted sum + activation | Code one neuron (NumPy) |
| **7.1 🔧** | Loss = how wrong we are | Code a loss function |
| **7.2 🔧** | **Gradient descent** — nudge weights downhill | Minimize a 1-variable function |
| **7.3 🔧** | **Backpropagation** — the chain rule that trains nets | A tiny 2-layer net, pure NumPy |
| **7.4** | Training works | Train it, watch loss drop | A net that learns |

### Run B — PyTorch (the pro tool)
| Atom | Idea | You implement |
|------|------|---------------|
| **7.5 🔧** | Tensors + **autograd** (gradients for free) | Play with tensors |
| **7.6** | `nn.Module` + training loop | Rebuild your net in PyTorch |

### Run C — Transformers from scratch
| Atom | Idea | You implement |
|------|------|---------------|
| **7.7** | Embeddings = a lookup table | Build one |
| **7.8 🔧** | **Attention** intuition — who looks at whom | Trace it on a 4-word sentence |
| **7.9 🔧** | Self-attention math (**Q·K·V**) | Work one head by hand, small numbers |
| **7.10 🔧** | **Causal masking** — no peeking ahead | Add the mask, see why |
| **7.11 🔧** | Multi-head + positional encoding | Extend the head |
| **7.12** | The transformer block | Assemble one block in code |
| **7.13** | Train a tiny char-level **mini-LLM** | Train it, generate text |
| **7.14** | Wrap it up | Explain the whole thing in your words | **You understand LLMs, for real** |
