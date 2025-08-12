import os
from pathlib import Path
from datetime import datetime
import requests
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from fastmcp import FastMCP

# Initialize MCP
mcp = FastMCP(name="DocAsOneChunk")

# Constants
EMBEDDING_SERVER_URL = "http://localhost:8888/embeddings"
DEFAULT_OUTPUT_BASE = "chroma_outputs"

# === Function: Load and Chunk Documents ===
def load_files_as_whole_chunks(folder_path: str) -> list[Document]:
    docs = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".txt") or filename.endswith(".md"):
            loader = TextLoader(file_path, encoding="utf-8")
            documents = loader.load()
            combined_text = "\n".join(doc.page_content for doc in documents)
            docs.append(Document(page_content=combined_text, metadata={"source": filename}))
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            combined_text = "\n".join(doc.page_content for doc in documents)
            docs.append(Document(page_content=combined_text, metadata={"source": filename}))
    return docs

# === Class: Remote Embeddings ===
class RemoteEmbeddings(Embeddings):
    def embed_documents(self, texts):
        response = requests.post(EMBEDDING_SERVER_URL, json={"input": texts})
        response.raise_for_status()
        data = response.json()
        return [item["embedding"] for item in data["data"]]

    def embed_query(self, text):
        return self.embed_documents([text])[0]

# === MCP Tool: Build Chroma from Folder ===
@mcp.tool(name="build_chroma_store")
async def build_chroma_from_folder(folder_path: str, output_base: str = DEFAULT_OUTPUT_BASE) -> str:
    """
    Builds a Chroma DB from the given folder as single-chunk-per-doc.
    Always creates a timestamped directory under chroma_outputs/.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    chroma_path = os.path.join(output_base, f"chroma_{timestamp}")
    os.makedirs(chroma_path, exist_ok=True)

    docs = load_files_as_whole_chunks(folder_path)
    if not docs:
        raise ValueError(f"No valid documents found in {folder_path}")

    embeddings = RemoteEmbeddings()
    db = Chroma.from_documents(docs, embedding=embeddings, persist_directory=chroma_path)
    db.persist()
    print(f"✅ Vector store created at: {chroma_path}")
    return chroma_path

# === Utility: Get Latest Chroma Folder ===
@mcp.tool(name="get_latest_chroma_path")
def get_latest_chroma_tool() -> str:
    """Returns the latest Chroma folder path under chroma_outputs/"""
    subdirs = [
        os.path.join(DEFAULT_OUTPUT_BASE, d)
        for d in os.listdir(DEFAULT_OUTPUT_BASE)
        if os.path.isdir(os.path.join(DEFAULT_OUTPUT_BASE, d)) and d.startswith("chroma_")
    ]
    return max(subdirs, key=os.path.getmtime) if subdirs else DEFAULT_OUTPUT_BASE

# === Main ===
if __name__ == "__main__":
    mcp.run()
