from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from transformers import pipeline, set_seed # type: ignore[reportPrivateImportUsage]
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Load embedding model
try:
    embed_model = SentenceTransformer("BAAI/bge-large-en-v1.5")
except Exception as e:
    print(f"Failed to load embedding model: {e}")
    raise e

# Load text generation model
try:
    # You can swap "gpt2" with another model if you want
    gen_pipeline = pipeline("text-generation", model="BAAI/bge-large-en-v1.5")
    set_seed(42)  # for reproducibility
except Exception as e:
    print(f"Failed to load generation model: {e}")
    raise e

class EmbeddingRequest(BaseModel):
    input: List[str]
    model: Optional[str] = None

class CompletionRequest(BaseModel):
    model: Optional[str] = None
    messages: List[dict]  # list of {"role": "...", "content": "..."}
    temperature: Optional[float] = .15
    max_tokens: Optional[int] = 512

@app.post("/embeddings")
async def create_embeddings(request: EmbeddingRequest):
    if not all(isinstance(x, str) for x in request.input):
        raise HTTPException(status_code=422, detail="All inputs must be strings")

    vectors = embed_model.encode(request.input, show_progress_bar=False)
    return {
        "data": [{"embedding": vector.tolist(), "index": idx} for idx, vector in enumerate(vectors)],
        "object": "list",
        "model": request.model or "gpt2"
    }

@app.post("/chat/completions")
async def create_completion(request: CompletionRequest):
    # Extract last user message content
    user_message = next((msg["content"] for msg in reversed(request.messages) if msg["role"] == "user"), "")
    if not user_message:
        raise HTTPException(status_code=422, detail="No user message found")

    # Generate text with HuggingFace pipeline
    outputs = gen_pipeline(
        user_message,
        max_new_tokens=request.max_tokens or 256,
        temperature=request.temperature or 0.15,
        num_return_sequences=1,
        pad_token_id=50256
)
    completion_text = outputs[0]["generated_text"][len(user_message):].strip()

    return {
        "id": "model2",
        "object": "chat.completion",
        "created": 1234567890,
        "model": request.model or "gpt2",
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
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
