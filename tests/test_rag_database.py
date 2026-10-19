"""実API・モデルダウンロードなしでChromaの登録/検索を確認する。"""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_rag_checkpoint():
    file_path = ROOT / "checkpoints" / "step4" / "rag.py"
    spec = importlib.util.spec_from_file_location("rag_checkpoint_integration", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fake_embed(texts):
    # テスト対象はDBの永続化・メタデータ・類似検索の接続。
    # Embeddingの品質テストではないので固定ベクトルを使う。
    return [[1.0, 0.0, 0.0] for _ in texts]


class RagDatabaseTests(unittest.TestCase):
    def test_chroma_index_search_and_persistence(self):
        rag = load_rag_checkpoint()
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "chroma"
            with (
                patch.object(rag.settings, "CHROMA_PATH", db_path),
                patch.object(rag, "embed_passages", fake_embed),
                patch.object(rag, "embed_queries", fake_embed),
            ):
                text = "一般社員の国内宿泊費は12,000円です。上限超過は部門長の承認が必要です。"
                count = rag.index_document("travel.txt", text)
                self.assertGreaterEqual(count, 1)
                self.assertEqual(rag.document_count(), count)

                # 同じ資料を登録しても重複を増やさない。
                rag.index_document("travel.txt", text)
                self.assertEqual(rag.document_count(), count)

                matches = rag.search_documents("宿泊費の上限は？")
                self.assertTrue(matches)
                self.assertEqual(matches[0]["source"], "travel.txt")
                self.assertIn("12,000円", matches[0]["text"])
                self.assertIsInstance(matches[0]["chunk"], int)

                # PersistentClientを再度開いても登録結果が残る。
                self.assertEqual(rag.get_collection().count(), count)

    def test_strict_prompt_mentions_sources_and_unknowns(self):
        rag = load_rag_checkpoint()
        result = rag.build_rag_system_prompt([
            {"text": "上限は12,000円です。", "source": "travel.txt", "chunk": 1}
        ])
        self.assertIn("travel.txt", result)
        self.assertIn("資料からは確認できません", result)
        self.assertIn("12,000円", result)


if __name__ == "__main__":
    unittest.main()
