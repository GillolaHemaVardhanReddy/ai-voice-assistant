from .golden import questions
from service.store import search


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