import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 8, 12])

print(a)
print(b)

print(a / np.linalg.norm(a))

print(b / np.linalg.norm(b))

