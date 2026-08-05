from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from .rag import answer
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Literal
from .rag_v2 import answer as answer_v2

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

class Turn(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class AskV2Request(BaseModel):
    question: str
    history: list[Turn] = []

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


@app.post("/v2/ask")
@limiter.limit("20/minute")
def ask_v2(request: Request, body: AskV2Request):
    history = [t.model_dump() for t in body.history]
    try:
        result = answer_v2(body.question, history)
    except Exception:
        raise HTTPException(status_code=502, detail="Upstream model unavailable. Try again.")
    return {"answer": result, "version": "v2"}