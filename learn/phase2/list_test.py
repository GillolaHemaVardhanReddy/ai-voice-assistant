import numpy as np
v = np.array([1.0, 2.0, 3.0])
v = v / np.linalg.norm(v)
r = np.round(v, 2)
print(r, np.linalg.norm(r))
