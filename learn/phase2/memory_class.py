class Memory:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.history = [{"role": "system", "content": system_prompt}]
    def add(self,role, text):
        self.history.append({"role": role, "content": text})
    def pop(self):
        if len(self.history) > 1:
            self.history.pop()


if __name__ == "__main__":
    m = Memory("You are a pirate.")
    m.add("user", "hi")

    other = Memory()
    print(m.history)
    print(other.history)