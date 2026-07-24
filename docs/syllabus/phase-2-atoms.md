# Phase 2 — MEMORY & RAG (answers from your data)

Goal: your assistant answers from *your own documents* — what people really mean by "train it on my data." 🔧 = open-the-hood atom.

| Atom | Idea you'll learn | What you'll do | You'll end up with |
|------|-------------------|----------------|--------------------|
| **2.0** | Clean conversation memory | Store turns in a list properly | Reliable chat memory |
| **2.1** | Why it can't know your data (+ context limits) | Ask about a private note, watch it fail | The problem, felt |
| **2.2 🔧** | NumPy + what a **vector** is (dot product) | Implement a dot product in NumPy | Comfort with vectors |
| **2.3** | Embedding = text → vector | Embed a sentence, print vector + size | A real vector |
| **2.4 🔧** | **Cosine similarity** = closeness of vectors | Compute it by hand on tiny 2D vectors | The math, unscary |
| **2.5** | Similarity in code | Compare cat / kitten / car | Meaning as numbers |
| **2.6** | Chunk → embed → store = a vector store | Split a doc, embed chunks, keep them | A tiny knowledge base |
| **2.7** | Retrieval = nearest chunks to a question | Query it, get the right chunks | Search by meaning |
| **2.8** | RAG = paste chunks into the prompt | Answer a question from your data | Grounded answers |
| **2.9** | Wrap it up | Point it at a folder of your notes | **Assistant that knows your stuff** |

> Framework: `sentence-transformers` (free, local embeddings). Cost note vs paid embedding APIs included.
