import numpy as np
from pathlib import Path
from .embedder import encode

_data = np.load(Path(__file__).parent / "index.npz", allow_pickle=False)
vecs = _data["vecs"]
chunks = _data["chunks"]
sources = _data["sources"]

def search(query, k=2):
    q = encode(query)
    scores = vecs @ q
    top = np.argsort(scores)[::-1][:k]
    return [(scores[i], chunks[i], sources[i]) for i in top]


if(__name__=="__main__"):
    queries = [
        "how does he approach building features?",
        "has he handled payments at scale?",
        "what is he learning right now?",
        "does he know databases?",
    ]
    for q in queries:
        for score, chunk, src in search(q, k=3):
            print("query: ", q, "source: ", src , "\nscore: " , f"{score:.3f}  |  {chunk}")
            print("\n")