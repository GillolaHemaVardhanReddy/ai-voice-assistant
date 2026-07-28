import os
import numpy as np
from openai import OpenAI
from store import search
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)


SYSTEM="""You answer questions about Hemavardhan on his behalf, for recruiters.
Answer ONLY using the CONTEXT below.
If the CONTEXT does not contain the answer, say you don't have that information.
Never guess or invent details. Keep answers to 2-3 sentences."""

def answer(question, k = 5):
    hits = search(question, k)
    context = "\n\n".join(chunk for score, chunk in hits)
    r = client.chat.completions.create(
        model = "anthropic/claude-haiku-4.5",
        stream = True,
        messages=[
             {"role": "system", "content": SYSTEM},
             {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"}
        ]
    )
    s = ""
    for chunk in r:
        if chunk.choices[0].finish_reason is not None:
                break
        delta = chunk.choices[0].delta.content
        if delta:
            s += delta
            print(delta, end="", flush=True)
    print("\n\n")

if __name__ == "__main__":
    for q in ["what does he do at his current job?",
              "has he published anything open source?",
              "what is his salary expectation?"]:
        print("\nQ:", q)
        answer(q)