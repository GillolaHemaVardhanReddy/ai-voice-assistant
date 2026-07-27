from sentence_transformers import SentenceTransformer
from cosine import cosine



model = SentenceTransformer("all-MiniLM-L6-v2")
words = ["cat", "car", "banana", "democracy", "hydrogen"]
vecs = model.encode(words)

for i in range(len(words)):
    for j in range(i + 1, len(words)):
        print(f"{words[i]:10} vs {words[j]:10} : {cosine(vecs[i], vecs[j]):.3f}")
