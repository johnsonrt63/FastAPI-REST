# app.py  9/17
import os
import secrets
from typing import Optional

from fastapi import FastAPI, HTTPException, Header, Depends, status
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

app = FastAPI(title="LLM Relay API", version="1.1.0")

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is required")

if not SERVICE_API_KEY:
    raise RuntimeError("SERVICE_API_KEY environment variable is required")

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0.2,
    api_key=OPENAI_API_KEY,
)

class ChatIn(BaseModel):
  session_id: str
  message: str
  options: dict | None = None

class LLMRequest(BaseModel):
    message: str = Field(..., description="Message to send to the LLM")
    system_prompt: Optional[str] = Field(
        default="You are a helpful assistant.",
        description="Optional system prompt",
    )

class LLMResponse(BaseModel):
    response: str


def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    if not secrets.compare_digest(x_api_key, SERVICE_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return True


@app.get("/health")
async def health():
    return {"status": "ok"}

#@app.post("/chat", response_model=LLMResponse, dependencies=[Depends(verify_api_key)])
#async def chat(payload: LLMRequest):
@app.post("/chat")
async def chat(body: ChatIn):
    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=body.message),
        ]

        result = llm.invoke(messages)
        print(f"Answer is: {result.content}")
        return LLMResponse(response=result.content)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        reply = f"Echo: {body.message}"
        return {"id": "abc123", "session_id": body.session_id, "reply": {"text": result.content}}  # Response Path: reply.text
    