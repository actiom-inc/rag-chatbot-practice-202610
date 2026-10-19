"""ローカルChromaによるTXT資料の登録・検索。"""
import hashlib
import chromadb
from practice import settings
from practice.embeddings import embed_passages, embed_queries

CHUNK_SIZE = 250
CHUNK_OVERLAP = 40
COLLECTION = "rag_handson_e5_small"


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("chunk_sizeは正、overlapは0以上chunk_size未満で指定してください")
    clean = text.strip()
    if not clean:
        return []
    step = chunk_size - overlap
    return [clean[start:start + chunk_size] for start in range(0, len(clean), step) if clean[start:start + chunk_size]]


def get_collection():
    settings.CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(settings.CHROMA_PATH))
    return client.get_or_create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})


def index_document(filename: str, text: str) -> int:
    if not filename.lower().endswith(".txt"):
        raise ValueError("TXTファイルのみ対応しています")
    if not text.strip():
        raise ValueError("ファイルが空です")
    chunks = split_text(text)
    collection = get_collection()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    file_hash = hashlib.sha256(filename.encode("utf-8")).hexdigest()[:12]
    ids = [f"{file_hash}:{digest}:{i}" for i in range(len(chunks))]
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embed_passages(chunks),
        metadatas=[{"source": filename, "chunk": i + 1} for i in range(len(chunks))],
    )
    return len(chunks)


def document_count() -> int:
    return get_collection().count()


def search_documents(query: str, top_k: int = 3) -> list[dict]:
    if not query.strip() or top_k < 1:
        return []
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return []
    response = collection.query(
        query_embeddings=embed_queries([query]),
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "text": doc,
            "source": meta.get("source", "不明"),
            "chunk": meta.get("chunk", 0),
            "distance": distance,
        }
        for doc, meta, distance in zip(
            response["documents"][0],
            response["metadatas"][0],
            response["distances"][0],
        )
    ]


def build_rag_system_prompt(matches: list[dict], strict: bool = True) -> str:
    """STEP 3から実装します。"""
    raise NotImplementedError("STEP 3で実装します")
