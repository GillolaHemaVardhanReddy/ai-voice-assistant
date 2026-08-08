from service.store import search

response1 = search("Does he have experiance in MongoDB?", k = 5)


response2 = search("Does he have experiance in MongoDB? so he knows it?" ,k = 5)

print("chunks for question 1: Does he have experiance in MongoDB?\n")
for i in response1:
    print(i, "\n")
print("chunks for question 2: Does he have experiance in MongoDB? so he knows it?\n")
for i in response2:
    print(i, "\n")