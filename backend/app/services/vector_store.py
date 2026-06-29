import chromadb
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.providers import get_embeddings
from app.core.config import get_settings


class VectorStoreService:
    def __init__(self):
        self._client = chromadb.EphemeralClient()
        self._store: Chroma | None = None
        self._settings = get_settings()

    def index(self, text: str, vendor_name: str) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._settings.chunk_size,
            chunk_overlap=self._settings.chunk_overlap,
            separators=["\n\n", "\n", ". ", " "],
        )
        chunks = splitter.split_text(text)
        self._client = chromadb.EphemeralClient()
        self._store = Chroma(
            client=self._client,
            collection_name=f"proposal_{vendor_name[:20].replace(' ', '_')}",
            embedding_function=get_embeddings(),
        )
        self._store.add_texts(
            texts=chunks,
            metadatas=[{"chunk_idx": i} for i in range(len(chunks))],
        )
        return chunks

    def retrieve(self, query: str, k: int | None = None) -> list[str]:
        if not self._store:
            return []
        k = k or self._settings.retrieval_top_k
        docs = self._store.similarity_search(query, k=k)
        return [d.page_content for d in docs]
