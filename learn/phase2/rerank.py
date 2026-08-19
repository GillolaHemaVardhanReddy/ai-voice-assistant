import os, requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("OPENROUTER_API_KEY")
print("key loaded:", bool(KEY))
RELEVANCE_CUTOFF = 0.05

query = "can he start immediately?"

good_1 = """# Notice period, availability and when he can start 
"His notice period is 2 months. That is how long it will take him to join after accepting an offer."""

good_2 = """
# Chances of notice period buyout
He cant buy out the notice period currently meaning he must serve his 2 months or 60 days at the current working company.
"""

mid_1 = """
# Vedamandir — the live production platform he works on

Vedamandir (vedamandir.com) is a live consumer platform for booking temple poojas and rituals online, serving daily bookings across India. It is the production system behind almost all of his payments, customer-recovery, analytics and multi-tenant work.
"""

mid_2 = """
# Cloud, DevOps and operations skills

He is strong with AWS, particularly S3 and CloudFront for CDN delivery, page caching and automated cache invalidation.
"""

bad_1 = """
cat is actually sitting on the mat
"""

bad_2 = """
The hero is running on the train.
"""

r = requests.post(
    "https://openrouter.ai/api/v1/rerank",
    headers={"Authorization": f"Bearer {KEY}"},
    json={
        "model": "cohere/rerank-v3.5",
        "query": query,
        "documents": [good_1, good_2, mid_1, mid_2, bad_1, bad_2],
        "top_n": 6,
    },
)
res = r.json()

ranks = res["results"]

for i in ranks:
    score = i["relevance_score"]
    text = i["document"]["text"]
    print(text, "has score of: ", score,  "\n\n")