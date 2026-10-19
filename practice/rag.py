"""ハンズオンで実装する領域。STEP 2から編集してください。"""

CHUNK_SIZE = 250
CHUNK_OVERLAP = 40


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """STEP 2: 長文を分割する。"""
    raise NotImplementedError("STEP 2で実装します")


def index_document(filename: str, text: str) -> int:
    """STEP 2: Chromaに保存し、登録チャンク数を返す。"""
    raise NotImplementedError("STEP 2で実装します")


def document_count() -> int:
    """STEP 2: 保存済みチャンク数を返す。"""
    raise NotImplementedError("STEP 2で実装します")


def search_documents(query: str, top_k: int = 3) -> list[dict]:
    """STEP 2: 類似文章を検索する。"""
    raise NotImplementedError("STEP 2で実装します")


def build_rag_system_prompt(matches: list[dict], strict: bool = True) -> str:
    """STEP 3: 検索結果をLLMへ渡すための指示を組み立てる。"""
    raise NotImplementedError("STEP 3で実装します")
