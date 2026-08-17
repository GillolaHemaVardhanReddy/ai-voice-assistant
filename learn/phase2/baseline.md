# Retrieval baseline — BEFORE reranking (Atom 2.10.3, 14 Aug 2026)

Run: `python -m learn.phase2.score` from the repo root.
Corpus: 6 notes files → 127 chunks. Retriever: bi-encoder cosine, `vecs @ q`, no rerank.

| k | score (hit-rate) | top1 | MRR |
|---|---|---|---|
| 5 | 7 / 7 | 6 / 7 | **0.93** |
| 3 | 7 / 7 | 6 / 7 | **0.93** |
| 1 | 4 / 7 | 6 / 7 | **0.86** |

**These are the numbers 2.11 (reranking) has to beat.**

## What each metric is sensitive to

| metric | asks | changes with k? |
|---|---|---|
| score (hit-rate) | is a correct file **anywhere** in the top k? | **very** — 7/7 → 4/7 at k=1 |
| MRR | **how high** is the best correct file? | only when the best rank falls off the end |
| top1 | is the **rank-1** result correct? | **never** — position 1 is position 1 at any k |

## Reading the baseline

- **The only imperfect row is row 2**, `"what projects did he do till now?"` — `projects.txt` sits at rank 2 while `faq.txt` takes rank 1. That single row is the entire gap between 0.93 and 1.00.
- **Headroom is therefore +0.07 at most.** Not a flaw in the harness — the corpus is 6 files on clearly distinct topics. Reranking earns its reputation on large, confusable corpora (hundreds of similar-sounding chunks), so a small gain here is the expected result, not a failure.
- **A reranker does not change hit-rate** — same candidates, reordered. It moves **MRR and top1**. Those two did not exist before this atom.
- At k=1 the `"all"` rows collapse (`k >= N` rule): a 2-file `"all"` row cannot pass when only one file can come back.
