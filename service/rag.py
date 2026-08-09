import os
import numpy as np
from openai import OpenAI
from .store import search
from dotenv import load_dotenv
from .timing import timed

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY"),
    timeout = 30.0,
    max_retries=2,
)


SYSTEM="""You are Spidy, Hemavardhan's assistant on his portfolio site.
You are NOT Hemavardhan — always refer to him in the third person, never as "I".
If asked who or what you are, say you're Spidy, an assistant that answers questions
about Hemavardhan's work from his own notes, then return to the question.
Answer ONLY using the CONTEXT below.
If the CONTEXT does not contain the answer, say you don't have that information.
Each context block starts with its source file in square brackets. End your answer with the sources you used, like: [about.txt, boundaries.txt]
Never guess or invent details. Keep answers to 2-3 sentences."""

@timed
def answer(question, k = 5):
    try:
        hits = search(question, k)
        context = "\n\n".join(f"[{src}] {chunk}" for score, chunk, src in hits)
        r = client.chat.completions.create(
            model = "anthropic/claude-haiku-4.5",
            temperature = 0.2,
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
        return s
    except Exception as e:
         print("FAILED:", type(e).__name__, e)

if __name__ == "__main__":
    for q in ["what is his salary expectation?",
              "what does he do at his current job?",
              "does he know Kubernetes?"]:
        print("\nQ:", q)
        answer(q)