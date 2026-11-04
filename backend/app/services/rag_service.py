from typing import List

from pathlib import Path

from openai import OpenAI

from app.rag.chunker import split_text
from app.rag.embedding import EmbeddingService
from app.rag.vector_store import VectorStore
from app.core.config import settings


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS_DIR = (
    PROJECT_ROOT / "backend" / "app" / "rag" / "documents"
)


class RAGService:

    def __init__(self):

        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.LLM_TIMEOUT_SECONDS
        )

    def ingest_documents(self):

        files = list(DOCUMENTS_DIR.glob("*.txt"))

        if not files:
            raise FileNotFoundError(
                "No .txt documents found."
            )

        total_chunks = 0
        sources = []

        for file_path in files:

            text = file_path.read_text(
                encoding="utf-8"
            )

            chunks = split_text(
                text,
                chunk_size=120,
                overlap=30
            )

            embeddings = (
                self.embedding_service.embed_documents(chunks)
            )

            self.vector_store.add_documents(
                chunks=chunks,
                embeddings=embeddings,
                source=file_path.name
            )

            total_chunks += len(chunks)
            sources.append(file_path.name)

        return {
            "documents_processed": len(files),
            "chunks_created": total_chunks,
            "sources": sources
        }

    def retrieve(
        self,
        question: str,
        top_k: int = 3
    ):

        query_embedding = (
            self.embedding_service.embed_query(question)
        )

        contexts = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return contexts

    def generate_answer(
        self,
        question: str,
        contexts: List[str]
    ):

        if not contexts:
            return (
                "I could not find relevant information "
                "in the available documents."
            )

        context_text = "\n\n".join(contexts)

        response = self.client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=(
                "You are a document question-answering assistant. "
                "Answer using only the supplied context. "
                "Do not invent information. "
                "If the answer is not present in the context, "
                "say that the documents do not contain the answer."
            ),
            input=(
                f"Context:\n{context_text}\n\n"
                f"Question:\n{question}"
            )
        )

        return response.output_text

    def ask(
        self,
        question: str,
        top_k: int = 3
    ):

        contexts = self.retrieve(
            question=question,
            top_k=top_k
        )

        answer = self.generate_answer(
            question=question,
            contexts=contexts
        )

        return {
            "question": question,
            "answer": answer,
            "retrieved_context": contexts,
            "retrieved_chunks": len(contexts)
        }