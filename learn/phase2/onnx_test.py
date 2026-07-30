from fastembed import TextEmbedding
import numpy as np

model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")

vecs = list(model.embed(["He works with MySQL, ClickHouse and Redis."]))

assert np.isclose(np.linalg.norm(vecs[0]), 1.0), "embedder returned a non-unit vector"


print(vecs[0].shape, vecs[0][:3])

print("norm:", np.linalg.norm(vecs[0]))

print("gap:", 1.0 - np.linalg.norm(vecs[0]))
print("is it 1?", np.isclose(np.linalg.norm(vecs[0]), 1.0))