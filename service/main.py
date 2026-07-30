from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from .rag import answer
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://hemavardhanreddy.vercel.app"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
@limiter.limit("20/minute")
def ask(request: Request, body: AskRequest):
    result = answer(body.question)
    if result is None:
            raise HTTPException(status_code=502, detail="Upstream model unavailable. Try again.")
    return {"answer": result}