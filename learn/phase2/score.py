from pathlib import Path

from .golden import questions
from service.store import search

# --- guard: every filename in the key must be a real file on disk ---
# A typo'd filename ("project.txt", no s) never matches — silently, forever.
# The row fails every run and the retriever takes the blame. Fail loudly instead.
NOTES = Path(__file__).resolve().parents[2] / "service" / "notes"
on_disk = {p.name for p in NOTES.glob("*.txt")}
for q in questions:
    for name in q["file"]:
        if name not in on_disk:
            raise FileNotFoundError(f"key names {name}, which is not in {NOTES} — fix the key")

ans = 0
for q in questions:
    print(f"Question: ",q["question"])
    results = [str(i[2]) for i in search(q["question"], k=5)]
    print("got:", results)
    print("expected:", q["file"])
    check = [f in results for f in q["file"]]
    if(q["match"]=="all"):
        if(all(check)):
            print("PASS")
            ans+=1
        else:
            print("FAIL")
    else:
        if(any(check)):
            print("PASS")
            ans+=1
        else:
            print("FAIL")
print("score is:", ans, "/" , len(questions))