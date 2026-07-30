import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "openai/text-embedding-3-small"

def encode(texts):
    single = isinstance(texts, str)
    r = client.embeddings.create(model=MODEL, input=[texts] if single else texts)
    vecs = np.array([d.embedding for d in r.data])
    vecs = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs[0] if single else vecs

if __name__ == "__main__":
    v = encode("hello")
    print(v.shape, np.linalg.norm(v))
    print("unit?", np.allclose(np.linalg.norm(v), 1.0))