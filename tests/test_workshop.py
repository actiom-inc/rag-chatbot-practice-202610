import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.restore_checkpoint import restore


class RestoreTests(unittest.TestCase):
    def test_recovery_preserves_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "checkpoints/step1").mkdir(parents=True)
            (root / "checkpoints/step1/app.py").write_text("new", encoding="utf-8")
            (root / "app.py").write_text("old", encoding="utf-8")
            backup = restore("step1", root)
            self.assertEqual((root / "app.py").read_text(), "new")
            self.assertEqual((backup / "app.py").read_text(), "old")

    def test_unknown_step_rejected(self):
        with self.assertRaises(ValueError):
            restore("step9")


class CheckpointTests(unittest.TestCase):
    def test_all_checkpoint_files_exist(self):
        for step in ("step1", "step2", "step3", "step4"):
            self.assertTrue((ROOT / "checkpoints" / step / "app.py").is_file())
            if step != "step1":
                self.assertTrue((ROOT / "checkpoints" / step / "rag.py").is_file())

    def test_chunking(self):
        import ast
        source = (ROOT / "checkpoints/step4/rag.py").read_text(encoding="utf-8")
        compile(source, "rag.py", "exec")
        chunk_fn = next(x for x in ast.parse(source).body if isinstance(x, ast.FunctionDef) and x.name == "split_text")
        self.assertIsNotNone(chunk_fn)
        for n in range(1, 5):
            app_source = (ROOT / "checkpoints" / f"step{n}" / "app.py").read_text(encoding="utf-8")
            compile(app_source, f"step{n}/app.py", "exec")


if __name__ == "__main__":
    unittest.main()
