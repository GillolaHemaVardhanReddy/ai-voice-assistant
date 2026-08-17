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
MRR = 0
top1 = 0
for q in questions:
    print(f"Question: ",q["question"])
    results = [str(i[2]) for i in search(q["question"], k=1)]
    print("got:", results)
    print("expected:", q["file"])
    check = [f in results for f in q["file"]]
    ranks = {}
    for f in q["file"]:
        ranks[f] = results.index(f)+1 if f in results else None
    if 1 in ranks.values():
        top1 += 1
    u = [i for i in ranks.values() if i is not None]
    if(len(u) > 0):
        MRR += (1/min(u))
    print(ranks)
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
print("score is:", ans, "/" , len(questions), "\ntop1 of the expected set is: ", top1, "\n MRR (mean reciprocal rank) is: ", round(MRR / len(questions),2))