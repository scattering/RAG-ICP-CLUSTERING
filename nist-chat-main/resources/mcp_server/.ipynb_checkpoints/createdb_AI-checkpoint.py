import os
import time
from datetime import datetime
from typing import List
import requests

from dotenv import load_dotenv
from fastmcp import FastMCP
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

mcp = FastMCP(name="ChromaBuilderAndSearcher")
EMBEDDING_SERVER_URL = "http://localhost:8888/embeddings"

DEFAULT_DATA_PATH = "/storage/anp27/REMOTE_ENDPOINT/nist-chat-main/resources/MCPDOC"
DEFAULT_OUTPUT_BASE = "chroma_outputs"


def get_latest_chroma_path(base_path=DEFAULT_OUTPUT_BASE):
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


@mcp.tool(name="build_chroma_store")
async def build_chroma_store(data_path: str = DEFAULT_DATA_PATH, output_base: str = DEFAULT_OUTPUT_BASE) -> str:
    """
    Loads .txt, .md, and .pdf files from a folder, splits into chunks,
    and stores the chunks persistently in a Chroma DB collection with metadata.
    """
    start = time.time()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    chroma_path = os.path.join(output_base, f"chroma_{timestamp}")
    os.makedirs(chroma_path, exist_ok=True)

    try:
        documents = []

        # Load all supported document types
        txt_loader = DirectoryLoader(data_path, glob="*.txt", loader_cls=TextLoader)
        md_loader = DirectoryLoader(data_path, glob="*.md", loader_cls=TextLoader)
        pdf_loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls=PyPDFLoader)

        documents.extend(txt_loader.load())
        documents.extend(md_loader.load())
        documents.extend(pdf_loader.load())

        if not documents:
            return f"⚠ No documents found in '{data_path}'."

        # Split documents into chunks with overlap
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=500,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)

        # Enrich chunk metadata with filename/title and chunk index
        for i, chunk in enumerate(chunks):
            filename = os.path.basename(chunk.metadata.get('source', 'unknown'))
            title = os.path.splitext(filename)[0]
            chunk.metadata['chunk_index'] = i
            chunk.metadata['title'] = title

        # Use your preferred embedding method here:
        # Example using HuggingFace embeddings
        embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

        # Or to use your local embedding endpoint uncomment:
        # embeddings = LocalEmbedding(endpoint_url=EMBEDDING_SERVER_URL)

        # Create Chroma vector store and persist to disk
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=chroma_path
        )
        db.persist()

        end = time.time()
        return (
            f"✅ Indexed {len(documents)} documents → {len(chunks)} chunks → "
            f"saved to '{chroma_path}' in {round(end - start)} seconds."
        )

    except Exception as e:
        return f"❌ Failed to build Chroma DB: {e}"


if __name__ == "__main__":
    mcp.run()
