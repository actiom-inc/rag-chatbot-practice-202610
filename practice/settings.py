"""研修共通の設定。APIキーは必ず.envで扱う。"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "openai").strip().lower()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
CHROMA_PATH = Path(os.getenv("CHROMA_PATH", ".data/chroma"))


def check_api_settings() -> str | None:
    """問題なければNone、問題があれば表示用メッセージを返す。"""
    if PROVIDER == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            return "OPENAI_API_KEYが設定されていません。 .env を確認してください。"
    elif PROVIDER == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            return "ANTHROPIC_API_KEYが設定されていません。 .env を確認してください。"
    else:
        return "LLM_PROVIDERにはopenaiまたはanthropicを指定してください。"
    return None


def active_model() -> str:
    return OPENAI_MODEL if PROVIDER == "openai" else ANTHROPIC_MODEL
