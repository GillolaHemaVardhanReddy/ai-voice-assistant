from sentence_transformers import SentenceTransformer
import numpy as np


def cosine(a, b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

model = SentenceTransformer("all-MiniLM-L6-v2")


vec = model.encode("I know React and Node.js")


print(type(vec))
print(vec.shape)
print(np.linalg.norm(vec))
print(vec[:5])