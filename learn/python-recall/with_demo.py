with open("note.txt", "w") as f:
    f.write("hello")

print("closed?", f.closed)