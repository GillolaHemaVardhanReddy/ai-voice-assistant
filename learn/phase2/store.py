from sentence_transformers import SentenceTransformer
from cosine import cosine
import numpy as np
import glob


model = SentenceTransformer("all-MiniLM-L6-v2")

files = sorted(glob.glob("learn/phase2/notes/*.txt"))


chunks = []
embed_texts = []
sources=[]
for file in files:
    text = open(file, "r").read()
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
            sources.append(file.split("/")[-1])

assert len(chunks) == len(embed_texts) == len(sources)
print(len(files), "files →", len(chunks), "chunks")

vecs = model.encode(embed_texts)
def search(query, k=2):
    q = model.encode(query)
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