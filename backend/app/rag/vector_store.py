from typing import List

import chromadb

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

CHROMA_PATH = PROJECT_ROOT / "backend" / "chroma_db"


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        self.collection = self.client.get_or_create_collection(
            name="ai_testlab_documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        source: str
    ):

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Chunks and embeddings must have equal lengths."
            )

        if not chunks:
            return

        ids = [
            f"{source}_{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {"source": source}
            for _ in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 3
    ):

        if self.collection.count() == 0:
            return []

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count())
        )

        documents = result.get("documents") or [[]]

        return documents[0]