from fastmcp import FastMCP
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from typing import List
import requests
import os

mcp = FastMCP(name="ChunkSearch")
EMBEDDING_SERVER_URL = "http://localhost:8888/embeddings"  # remote endpoint
def get_latest_chroma_path(base_path="chroma_outputs"):
    subdirs = [
        os.path.join(base_path, d)
        for d in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, d)) and d.startswith("chroma_")
    ]
    return max(subdirs, key=os.path.getmtime) if subdirs else base_path




class LocalEmbedding(Embeddings):
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = requests.post(self.endpoint_url, json={"input": texts})
        response.raise_for_status()
        data = response.json()
        return [d["embedding"] for d in data["data"]]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

@mcp.tool(name="search_database")
async def search_database(question: str, k: int = 3) -> str:
    CHROMA_PATH = get_latest_chroma_path()
    """
    You are an expert scientific assistant. Answer the question below **only** using the context provided.
    Be detailed, explain step by step, and cite document titles or page numbers if relevant.
    If the answer is not in the context, say 'Not found in the documents'.
    """
    try:
        # Init embedding
        embedding_fn = LocalEmbedding(EMBEDDING_SERVER_URL)

        # Load Chroma with embedding
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_fn
        )

        # Embed query
        query_embedding = embedding_fn.embed_query(question)

        # Search
        results = db.similarity_search_by_vector_with_relevance_scores(
            query_embedding, k=k
        )

        if not results:
            return "⚠️ No relevant chunks found."

        # Format output
        chunks = []
        for doc, score in results:
            chunks.append(f"Score: {score:.3f}\nContent: {doc.page_content}")

        return "\n\n---\n\n".join(chunks)

    except Exception as e:
        return f"❌ Search failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()
