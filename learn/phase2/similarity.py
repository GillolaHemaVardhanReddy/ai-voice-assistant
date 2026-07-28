from sentence_transformers import SentenceTransformer
from cosine import cosine



model = SentenceTransformer("all-MiniLM-L6-v2")
words = ["cat", "car", "banana", "democracy", "hydrogen"]
vecs = model.encode(words)
mean_vec = vecs.mean(axis=0)
final_vec = vecs - mean_vec
sims = []

for i in range(len(words)):
    for j in range(i + 1, len(words)):
        s = cosine(final_vec[i], final_vec[j])
        sims.append(s)
        print(f"{words[i]:10} vs {words[j]:10} : {s:.3f}")
print("\n\n")
print("average is: ",sum(sims) / len(sims))