from fastapi import APIRouter
from pydantic import BaseModel
from rag.chat import answer_query

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    reply = answer_query(payload.message)
    return ChatResponse(reply=reply)


