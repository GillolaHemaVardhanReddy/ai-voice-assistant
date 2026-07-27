import numpy as np


def cosine(a, b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))



a = np.array([0.9, 0.1])    # "puppy playing"
b = np.array([0.95, 0.05])  # "golden retriever"
c = np.array([0.05, 0.9])   # "stock market crash"

print("puppy vs retriever:", cosine(a, b))
print("puppy vs stocks   :", cosine(a, c))