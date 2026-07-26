import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

messages = [
    {"role": "system", "content": "you are my assistant and will talk to me with humble and sweet tone and address me as boss"},
    {"role": "user", "content": "Hello, my name is hemavardhan, please remember that"},
]

r1 = client.chat.completions.create(
    model="anthropic/claude-haiku-4.5",
    temperature=0.7,
    messages=messages,
)

print(r1.choices[0].message.content)

messages.append({"role": "assistant", "content": r1.choices[0].message.content})
messages.append({"role": "user", "content": "what is my name?"})

r2 = client.chat.completions.create(
    model="anthropic/claude-haiku-4.5",
    temperature=0.7,
    messages=messages,
)


print(r2.choices[0].message.content)