import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

messages = [
    {"role": "system", "content": "You are a friendly voice assistant. Answers will be spoken aloud, so keep them under 2 sentences, conversational, no bullet points or code blocks."},
]

while(1):
    user_input = input("You: ")
    if(user_input.lower() == 'exit'):
        break
    messages.append({"role": "user", "content": user_input})
    stream = ""
    try:
        response = client.chat.completions.create(
            model = "anthropic/claude-haiku-4.5",
            messages=messages,
            stream=True,
            temperature=1.0
        )
        print("Assistant: ", end="", flush=True)
        for chunk in response:
            if chunk.choices[0].finish_reason is not None:
                break
            delta = chunk.choices[0].delta.content
            if(delta):
                stream += delta
                print(delta, end="", flush=True)
        print()
        messages.append({"role": "assistant", "content": stream})
    except Exception as e:
        print(f"Error: {e}")
        messages.pop()
        continue

