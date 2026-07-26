import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

response = client.chat.completions.create(
    model="anthropic/claude-haiku-4.5",
    messages=[{"role": "system", "content": "you are my humble servent who adresses me as 'boss'."},{"role": "user", "content": "Write a haiku about the ocean in one sentence."}],
    stream=True,
)

for chunk in response:
    delta = chunk.choices[0].delta.content
    if(delta):
        print(chunk.choices[0].delta.content, end="", flush=True)
print()