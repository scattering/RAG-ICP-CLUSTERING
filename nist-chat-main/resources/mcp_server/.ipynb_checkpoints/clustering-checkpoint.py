import os
import shutil
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain_community.vectorstores import Chroma
from fastmcp import FastMCP

mcp = FastMCP("Clustering")

@mcp.tool()
async def cluster_documents_from_chroma(
    chroma_base_path: str = "chroma_outputs",
    output_folder: str = "clustered_docs",
    n_clusters: int = 5
) -> str:
    """
    Load most recent Chroma vector DB, cluster its documents, and output top keywords per cluster.

    Args:
        chroma_base_path: Base folder with timestamped Chroma folders.
        output_folder: Where clustered folders will be created.
        n_clusters: Number of semantic clusters.

    Returns:
        Path to the output folder containing clustered documents.
    """
    # Remove previous clustering results if they exist
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    # Get most recent Chroma folder
    folders = [os.path.join(chroma_base_path, f) for f in os.listdir(chroma_base_path)]
    folders = [f for f in folders if os.path.isdir(f)]
    if not folders:
        raise FileNotFoundError("No folders found in chroma_outputs.")
    latest_folder = max(folders, key=os.path.getmtime)

    # Load vector store
    db = Chroma(persist_directory=latest_folder)

    # Get documents and embeddings
    docs = db.get(include=["embeddings", "metadatas", "documents"])
    vectors = np.array(docs["embeddings"])
    metadatas = docs["metadatas"]
    documents = docs["documents"]

    if len(vectors) < n_clusters:
        raise ValueError("Not enough documents to form the requested number of clusters.")

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(vectors)

    clusters = {i: [] for i in range(n_clusters)}  # For keyword extraction

    for i, label in enumerate(labels):
        cluster_path = os.path.join(output_folder, f"cluster_{label}")
        os.makedirs(cluster_path, exist_ok=True)

        # Extract filename
        meta = metadatas[i] or {}
        original_path = meta.get("source") or f"doc_{i}.txt"
        file_path = os.path.join(cluster_path, os.path.basename(original_path))

        # Save document
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(documents[i])

        clusters[label].append(documents[i])

    # Extract top keywords per cluster using TF-IDF
    for label, docs in clusters.items():
        if not docs:
            continue
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(docs)
        tfidf_scores = np.asarray(X.mean(axis=0)).flatten()
        top_indices = tfidf_scores.argsort()[-5:][::-1]
        keywords = [vectorizer.get_feature_names_out()[i] for i in top_indices]

        keyword_path = os.path.join(output_folder, f"cluster_{label}", "keywords.txt")
        with open(keyword_path, "w", encoding="utf-8") as f:
            f.write("\n".join(keywords))

    return f"Clustered {len(documents)} documents from '{latest_folder}' into {n_clusters} folders in '{output_folder}', with top keywords per cluster."

if __name__ == "__main__":
    mcp.run()
