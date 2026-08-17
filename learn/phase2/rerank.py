import os, requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("OPENROUTER_API_KEY")
print("key loaded:", bool(KEY))

query = "can he start immediately?"

doc_a = """# Notice period, availability and when he can start 
"His notice period is 2 months. That is how long it will take him to join after accepting an offer."""

doc_b = """
# What he has instead, in the same areas

Instead of Kubernetes, he has real production operations experience: AWS, CloudFront CDN with automated cache invalidation, PM2 clustering, CI/CD pipelines, and deploy-order safety gates for coordinated multi-database migrations.
"""


r = requests.post(
    "https://openrouter.ai/api/v1/rerank",
    headers={"Authorization": f"Bearer {KEY}"},
    json={
        "model": "cohere/rerank-v3.5",
        "query": query,
        "documents": [doc_a, doc_b],
        "top_n": 2,
    },
)
print(r.status_code)
print(r.json())