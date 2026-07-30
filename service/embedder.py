from fastembed import TextEmbedding
import numpy as np

_model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")

def encode(texts):
    single = isinstance(texts, str)
    vecs = np.array(list(_model.embed([texts] if single else texts)))
    return vecs[0] if single else vecs

if __name__ == "__main__":
    print(encode("hello").shape, encode(["hello", "world"]).shape)