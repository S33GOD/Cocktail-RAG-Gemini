from fastapi import FastAPI, HTTPException
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from RAG import ReasoningLoopQueryEngine
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
chatModel = ReasoningLoopQueryEngine()

class ChatRequest(BaseModel):
    user_input: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck")
def healthcheck():
    return {"message": "it works"}

@app.options("/chat")
async def options():
    return JSONResponse(status_code=200, content={})

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received user input: {request.user_input}")
        response = chatModel.query(request.user_input)
        logger.info(f"Generated response: {response}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Critical error")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")