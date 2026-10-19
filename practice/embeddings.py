"""EmbeddingはAPI課金なし。非対称検索のE5プレフィックスを使う。"""
from functools import lru_cache

from practice import settings


@lru_cache(maxsize=1)
def _load_model():
    from sentence_transformers import SentenceTransformer

    # 研修の再現性と端末互換性を優先してCPUで動かす
    return SentenceTransformer(settings.EMBEDDING_MODEL, device="cpu")


def embed_passages(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = _load_model().encode(
        ["passage: " + text for text in texts],
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.tolist()


def embed_queries(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = _load_model().encode(
        ["query: " + text for text in texts],
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.tolist()
