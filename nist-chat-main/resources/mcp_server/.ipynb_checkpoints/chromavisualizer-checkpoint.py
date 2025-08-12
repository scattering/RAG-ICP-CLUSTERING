import chromadb
from chromadb.config import Settings
from chromaviz import visualize_collection

persist_dir = "REMOTE_ENDPOINT/nist-chat-main/resources/mcp_server/chroma_outputs/chroma_20250728-172801"

client = chromadb.Client(Settings(persist_directory=persist_dir, anonymized_telemetry=False))

collections = client.list_collections()
print("Collections found:", [c.name for c in collections])

# Pick a collection (usually first if only one)
collection = client.get_collection(collections[0].name)

# Visualize
visualize_collection(collection, "output_visualization.png")
print("Saved visualization to output_visualization.png")
