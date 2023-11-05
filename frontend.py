import os
from typing import List, Literal, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Source(BaseModel):
    source: str
    title: str


class Message(BaseModel):
    role: Literal["DOCTOR", "PATIENT", "AI"]
    content: str
    sources: Optional[List[Source]] = None


class Transcript(BaseModel):
    transcript: List[Message]


class Query(BaseModel):
    transcript: List[Message]
    chat_history: List[Message]


@app.post("/query")
async def query_agent(query: Query):
    transcript = query.transcript
    chat_history = query.chat_history

    if len(transcript) == 0:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")

    if len(chat_history) == 0:
        # Initial request
        chat_history.append(Message(role="AI", content="Investigating..."))
    else:
        chat_history.append(Message(role="AI", content="I'm still thinking..."))

    return {"response": {"chat_history": chat_history}}


app.mount("/", StaticFiles(directory="DiagLLMFrontend/build", html=True), name="static")

if __name__ == "__main__":
    USE_NGROK = os.environ.get("USE_NGROK", False)

    if USE_NGROK:
        import nest_asyncio
        from pyngrok import ngrok

        port = 5000
        public_url = ngrok.connect(port).public_url
        nest_asyncio.apply()

        print(f"Running on {public_url}")

    uvicorn.run("frontend:app", host="0.0.0.0", port=5000, reload=True)
