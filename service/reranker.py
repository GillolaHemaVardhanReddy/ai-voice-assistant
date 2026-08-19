import os, httpx
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("OPENROUTER_API_KEY")
# Calibrated 19 Aug 2026 on the real corpus, cohere/rerank-v3.5.
#   highest junk score  0.158  ("is he married?" -> "He is currently open to opportunities.")
#   lowest real answer  0.204  ("can he start immediately?" -> faq.txt)
# Line sits in the gap between them. Re-derive if the model or the notes change.
RELEVANCE_CUTOFF = 0.18

def rerank(query, docs, top_n = None):
    if top_n is None:
        top_n = len(docs)
    r = httpx.post(
        "https://openrouter.ai/api/v1/rerank",
        headers={"Authorization": f"Bearer {KEY}"},
        json={
            "model": "cohere/rerank-v3.5",
            "query": query,
            "documents": docs,
            "top_n": top_n,
        },
        timeout=20.0,
    )
    res = r.json()
    ranks = res["results"]
    finalAns = [0 for i in docs]
    for i in ranks:
        finalAns[i["index"]] = i["relevance_score"]
    return finalAns



if __name__ == "__main__":
    # Three docs. Slot 1 is the only real answer.
    # Slots 0 and 2 are byte-identical on purpose.
    query = "when can he join?"
    docs = [
        "The sky is blue and the clouds are white.",
        "His notice period is 2 months before he can join a new company.",
        "The sky is blue and the clouds are white.",
    ]

    scores = rerank(query, docs, top_n=len(docs))
    for i, (s, d) in enumerate(zip(scores, docs)):
        print(f"  slot {i}  {s:.4f}  {d[:45]}")

    # 1. one score per doc, no more, no less
    assert len(scores) == len(docs), \
        f"got {len(scores)} scores for {len(docs)} docs — docs were lost"

    # 2. the score landed in the ORIGINAL slot, not the reranker's order
    best = max(range(len(scores)), key=lambda i: scores[i])
    assert best == 1, f"answer is doc 1, but the top score is in slot {best}"

    # 3. identical text must score identically, in both its slots
    assert scores[0] == scores[2], \
        f"same text scored {scores[0]} in slot 0 and {scores[2]} in slot 2"

    print("ordering OK")
