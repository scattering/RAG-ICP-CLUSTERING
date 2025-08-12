from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from transformers.pipelines import pipeline
from transformers.trainer_utils import set_seed

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Remote Embedding + Completion API")

# Load embedding model
try:
    logger.info("Loading embedding model...")
    embed_model = SentenceTransformer("BAAI/bge-large-en-v1.5")
except Exception as e:
    logger.error(f"Failed to load embedding model: {e}")
    raise e

# Load text generation model
try:
    logger.info("Loading generation model...")
    gen_pipeline = pipeline("text-generation", model="facebook/opt-1.3b")
    set_seed(42)
except Exception as e:
    logger.error(f"Failed to load generation model: {e}")
    raise e

# Request/response models
class EmbeddingRequest(BaseModel):
    input: List[str]
    model: Optional[str] = None

class CompletionRequest(BaseModel):
    model: Optional[str] = None
    messages: List[dict]  # Each dict: {"role": "...", "content": "..."}
    temperature: Optional[float] = 0.15
    max_tokens: Optional[int] = 512

@app.post("/embeddings")
async def create_embeddings(request: EmbeddingRequest):
    if not all(isinstance(x, str) for x in request.input):
        raise HTTPException(status_code=422, detail="All inputs must be strings")

    try:
        vectors = embed_model.encode(request.input, show_progress_bar=False)
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise HTTPException(status_code=500, detail="Embedding generation failed")

    return {
        "data": [{"embedding": vector.tolist(), "index": idx} for idx, vector in enumerate(vectors)],
        "object": "list",
        "model": request.model or "all-MiniLM-L12-v2"
    }

@app.post("/chat/completions")
async def create_completion(request: CompletionRequest):
    user_message = next((msg["content"] for msg in reversed(request.messages) if msg["role"] == "user"), "")
    if not user_message:
        raise HTTPException(status_code=422, detail="No user message found")

    try:
        outputs = gen_pipeline(
            user_message,
            max_new_tokens=request.max_tokens or 256,
            temperature=request.temperature or 0.15,
            num_return_sequences=1,
            pad_token_id=50256
        )
        completion_text = outputs[0]["generated_text"][len(user_message):].strip()
    except Exception as e:
        logger.error(f"Text generation failed: {e}")
        raise HTTPException(status_code=500, detail="Text generation failed")

    return {
        "id": "opt-1.3b-completion",
        "object": "chat.completion",
        "created": 1234567890,
        "model": request.model or "facebook/opt-1.3b",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": completion_text},
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(user_message.split()),
            "completion_tokens": len(completion_text.split()),
            "total_tokens": len(user_message.split()) + len(completion_text.split())
        }
    }

# Optional: Local development entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("BAAI_LARGE:app", host="0.0.0.0", port=8888, reload=True)
