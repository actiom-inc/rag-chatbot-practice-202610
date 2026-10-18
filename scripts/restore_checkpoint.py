"""チェックポイントの完成版をバックアップ付きで復元する。"""
import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = {"step1", "step2", "step3", "step4"}


def restore(step: str, root: Path = ROOT) -> Path:
    if step not in STEPS:
        raise ValueError(f"不明なSTEP: {step}")
    source = root / "checkpoints" / step
    paths = [(source / "app.py", root / "app.py")]
    if step != "step1":
        paths.append((source / "rag.py", root / "practice" / "rag.py"))
    for src, _ in paths:
        if not src.is_file():
            raise FileNotFoundError(f"完成版が見つかりません: {src}")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_dir = root / ".data" / "backups" / f"{stamp}-{step}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    for src, dest in paths:
        if dest.exists():
            relative = dest.relative_to(root)
            backup = backup_dir / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest, backup)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"復元: {dest.relative_to(root)}")
    print(f"退避: {backup_dir}")
    return backup_dir


def main():
    parser = argparse.ArgumentParser(description="STEP完成版を復元する")
    parser.add_argument("step", choices=sorted(STEPS))
    args = parser.parse_args()
    restore(args.step)


if __name__ == "__main__":
    main()
