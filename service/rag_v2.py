from .rag import SYSTEM, client
from .store import search
from .rewrite import rewrite
from .timing import timed

@timed
def answer(question, history=None, k=5):
    history = history or []
    messages = [{"role": "system", "content": SYSTEM}]
    messages += history
    hits = search(rewrite(question, history), k)
    context = "\n\n".join(f"[{src}] {chunk}" for score, chunk, src in hits)
    messages.append({
        "role": "user",
        "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
    })
    r = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        temperature=0.2,
        messages=messages,
    )
    return r.choices[0].message.content