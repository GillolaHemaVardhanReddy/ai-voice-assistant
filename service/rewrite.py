from .rag import client
from .timing import timed

SYSTEM = """
you are a helpful assistant that rewrites questions to be self-contained and clear,
and do not answer any question, your role is just to rewrite the question in conversation history at the end if its not self contained and depend on history,
and you have to only return the rewritten question, no extra text in response.
if the question is already self-contained, return the question as is.
note: do not change the meaning of the question user asked or add any extra information, just rewrite it to be self-contained and clear.
"""
@timed
def rewrite(question, history = None):
    final_question = ""
    if history:
        for i in history:
            final_question = final_question + " " + i['role'] + ": " + i['content']
    else:
        return question
    final_question = f"HISTORY:\n{final_question}\n\nQUESTION:\n{question}"
    r = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": final_question}
        ]
    )
    return r.choices[0].message.content