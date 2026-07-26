import math

scores = [2.0, 1.0, -1]

exps = [math.exp(s) for s in scores]

total = sum(exps)

probs = [e/total for e in exps]

print("probs: ", probs)

print("sum: " , sum(probs))