from sentence_transformers import SentenceTransformer
from cosine import cosine
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


text = open("learn/phase2/about.txt", "r").read()

chunks = []
embed_texts = []
section = ""
for block in text.split("\n\n"):
    block = block.strip()
    if not block:
        continue
    if block.startswith("#"):
        section = block.lstrip("# ").strip()
    else:
        chunks.append(block)
        embed_texts.append(f"{section}: {block}")

vecs = model.encode(embed_texts)
def search(query, k=2):
    q = model.encode(query)
    scores = vecs @ q
    top = np.argsort(scores)[::-1][:k]
    return [(scores[i], chunks[i]) for i in top]


if(__name__=="__main__"):
    queries = [
        "how does he approach building features?",
        "has he handled payments at scale?",
        "what is he learning right now?",
        "does he know databases?",
    ]
    for q in queries:
        for score, chunk in search(q, k=3):
            print("query: ", q, "\nscore: " , f"{score:.3f}  |  {chunk}")
            print("\n")