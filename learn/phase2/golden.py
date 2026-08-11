# GOLDEN QUESTION SET — the test suite for search().
# Each row is one recruiter question + the file(s) that actually hold the answer.
# The answer key was VERIFIED by reading the notes (grep + judgement), not remembered.
# Score = how many rows pass. Change the retriever, re-run, compare the number.
#
# "match" — how to judge a row:
#   "all" — every listed file must come back (the answer is split across them)
#   "any" — at least one listed file is enough (the same fact is stored in several)
#
# PREDICTION (before ever running the scorer, k=5):  __ / 5 pass, because ...

questions = [
    {"question":"does he know kubernetes?", "file": ["boundaries.txt"], "match": "any"},
    {"question":"what projects did he do till now?", "file": ["projects.txt"], "match": "any"},
    {"question": "what does he do at his current job?", "file": ["about.txt"], "match": "any"},
    {"question": "what is his salary expectations?", "file": ["preferences.txt", "faq.txt"], "match": "any"},
    {"question": "what is his notice period?", "file": ["preferences.txt","faq.txt"], "match": "any"},
]