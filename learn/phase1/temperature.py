import math
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

for i in range(3):
    response = client.chat.completions.create(
        model = "anthropic/claude-haiku-4.5",
        temperature = 0.0,
        messages = [
            {"role": "user", "content": "Invent a brand-new coffee shop name that does not exist. Reply with ONLY the name."},
        ],
    )
    print(response.choices[0].message.content)