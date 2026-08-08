from service.rag_v2 import answer
from service.rewrite import rewrite

# print("ARM A 1: ", answer("Does he have experiance in MongoDB?"), "\n\n")

# print("ARM A 2: ", answer("so he knows it?"), "\n\n")


response = answer("Does he have experiance in MongoDB?" , [])

print("ARM B 1: ", response, "\n\n")

history = [{"role": "user", "content": "Does he have experiance in MongoDB?"}, {"role": "assistant", "content": response}]
print("REWRITTEN: ", rewrite("so he knows it?", history))

# print("ARM B 2: ", answer("so he knows it?", history), "\n\n")
