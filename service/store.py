import numpy as np
from pathlib import Path
from .embedder import encode
from .reranker import rerank, RELEVANCE_CUTOFF

_data = np.load(Path(__file__).parent / "index.npz", allow_pickle=False)
vecs = _data["vecs"]
chunks = _data["chunks"]
sources = _data["sources"]

def search(query, k=2):
    q = encode(query)
    scores = vecs @ q
    top = np.argsort(scores)[::-1][:k]
    return [(scores[i], chunks[i], sources[i]) for i in top]



def search_reranked(query, k_wide=20, keep=3):
    result = search(query, k_wide)
    docs = [q for _, q, _ in result]
    srcs = [s for _, _, s in result]
    ranks = rerank(query, docs, len(docs))
    final_ans = [(r, d, s) for r, d, s in zip(ranks, docs, srcs)]
    final_ans.sort(key=lambda t: t[0], reverse=True)
    final_ans = [t for t in final_ans if t[0] >= RELEVANCE_CUTOFF]
    return final_ans[:keep]


if(__name__=="__main__"):
    queries = [
        "what car does he drive?",
        "is he married?",
        "what was his 12th standard percentage?",
        "does he have a US visa?",
    ]
    for q in queries:
        hits = search_reranked(q)
        print(f"\n=== {q}  ->  {len(hits)} kept")
        for score, chunk, src in hits:
            print("query: ", q, "source: ", src , "\nscore: " , f"{score:.3f}  |  {chunk}")
            print("\n")