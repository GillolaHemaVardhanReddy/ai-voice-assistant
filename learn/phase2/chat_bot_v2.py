import os
from openai import OpenAI
from dotenv import load_dotenv
from memory_class import Memory

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

m = Memory("You are Hemavardhan's personal assistant on his portfolio website. Recruiters chat with you to learn about him. Be helpful, specific and confident.")

while(1):
    user_input = input("You: ")
    if(user_input.lower() == 'exit'):
        break
    m.add("user", user_input)
    stream = ""
    try:
        response = client.chat.completions.create(
            model = "anthropic/claude-haiku-4.5",
            messages=m.history,
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
        m.add("assistant", stream)
    except Exception as e:
        print(f"Error: {e}")
        m.pop()
        continue

