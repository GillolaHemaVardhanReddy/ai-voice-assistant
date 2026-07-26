import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

messages=[
    {"role": "system", "content": "You are a friendly voice assistant. Answers will be spoken aloud, so keep them under 2 sentences, conversational, no bullet points or code blocks."},
    {"role": "user", "content": "What is Node.js?"},
]

for i in range(2):
    response = client.chat.completions.create(
        model = "anthropic/claude-haiku-4.5",
        temperature = 1.0,
        messages=messages,
    )
    print(response.choices[0].message.content)

