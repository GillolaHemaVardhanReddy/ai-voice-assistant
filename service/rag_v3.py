from .rag import SYSTEM, client
from .store import search_reranked
from .rewrite import rewrite
from .timing import timed

@timed
def answer(question, history=None, k=5):
    history = history or []
    messages = [{"role": "system", "content": SYSTEM}]
    messages += history
    hits = search_reranked(rewrite(question, history))
    if(not len(hits)):
        return ("I don't have that in my notes. For anything not covered here, "
                "it's best to ask Hemavardhan directly at gillolahemavardhanreddy@gmail.com.")
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