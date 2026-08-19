# GOLDEN QUESTION SET — the test suite for search().
# Each row is one recruiter question + the file(s) that actually hold the answer.
# The answer key was VERIFIED by reading the notes (grep + judgement), not remembered.
# Score = how many rows pass. Change the retriever, re-run, compare the number.
#
# "match" — how to judge a row:
#   "all" — every listed file must come back (the answer is split across them)
#   "any" — at least one listed file is enough (the same fact is stored in several)
#
# ⚠️ An "all" row listing N files needs k >= N. At k=1 only one file can come back,
#    so a 2-file "all" row scores 0 no matter how good the retriever is. (S21, measured)
#
# PREDICTION (before ever running the scorer, k=5):  5 / 5 pass, because ...

questions = [
    {"question":"does he know kubernetes?", "file": ["boundaries.txt"], "match": "any"},
    {"question":"what projects did he do till now?", "file": ["projects.txt"], "match": "any"},
    {"question": "what does he do at his current job?", "file": ["about.txt"], "match": "any"},
    {"question": "what is his salary expectations?", "file": ["preferences.txt", "faq.txt"], "match": "any"},
    {"question": "what is his notice period?", "file": ["preferences.txt","faq.txt"], "match": "all"},
    {"question": "what databases has he worked with?", "file": ["skills.txt", "boundaries.txt"], "match": "all"},
    # vocabulary mismatch: the word "immediately" appears in NONE of the notes (grepped).
    # The answer is "notice period: 2 months". Pure test of meaning-over-spelling. Passes at k=1.
    {"question": "can he start immediately?", "file": ["faq.txt", "preferences.txt"], "match": "any"},
    # HARVESTED FROM A LIVE FAILURE (19 Aug 2026, S22) — the deployed v1/v2 answered
    # "I don't have that information" although Way2News is in the notes 5 times.
    # Cosine matched the word "company" to "company stages" / "product company" in
    # preferences.txt. Fails on plain search, passes on search_reranked.
    {"question": "which company does he work for right now?", "file": ["about.txt", "faq.txt"], "match": "any"},
]