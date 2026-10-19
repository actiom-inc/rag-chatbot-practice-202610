"""研修前の事前確認（APIリクエストは送らない）。"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from practice import settings  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download-model", action="store_true", help="埋め込みモデルを事前ダウンロード")
    args = parser.parse_args()

    print("Python:", sys.version.split()[0])
    print("Provider:", settings.PROVIDER)
    print("Model:", settings.active_model())
    problem = settings.check_api_settings()
    if problem:
        print("API設定: 要確認 -", problem)
    else:
        print("API設定: キーの存在を確認（通信テストはしません）")
    if args.download_model:
        from practice.embeddings import embed_passages, embed_queries

        print("Embeddingモデルの準備中（初回はダウンロードが必要）...")
        print("登録ベクトル次元:", len(embed_passages(["研修の案内"])[0]))
        print("質問ベクトル次元:", len(embed_queries(["申込期限は？"])[0]))
        print("モデル準備: OK")
    else:
        print("Embeddingモデル: 未確認。--download-model で事前準備できます。")
    if problem:
        return 1
    print("準備完了（APIへの実リクエストは研修本番で実施します）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
