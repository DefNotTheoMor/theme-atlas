import subprocess
import argparse
from pathlib import Path

DEFAULT_BOOK_TYP_PATH = Path("../Атлас.typ")
DEFAULT_CACHE_DIR = Path("cache")

COVER_PPI = 300
COVER_NAME = "cover.png"


def is_cover_fresh(book_typ_path: Path, cover_path: Path) -> bool:
    if not cover_path.exists() or not book_typ_path.exists():
        return False
    cover_mtime = cover_path.stat().st_mtime
    newest_source = book_typ_path.stat().st_mtime
    for typ_file in book_typ_path.parent.rglob("*.typ"):
        newest_source = max(newest_source, typ_file.stat().st_mtime)
    return cover_mtime >= newest_source


def build_cover(book_typ_path: Path, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cover_path = cache_dir / COVER_NAME

    if is_cover_fresh(book_typ_path, cover_path):
        print(f"1. Обложка: [skip] {cover_path}")
        return cover_path

    print(f"1. Экспорт обложки из {book_typ_path}...")
    try:
        subprocess.run(
            [
                "typst",
                "compile",
                str(book_typ_path.resolve()),
                str(cover_path.resolve()),
                "--root",
                str(book_typ_path.resolve().parent),
                "--format",
                "png",
                "--pages",
                "1",
                "--ppi",
                str(COVER_PPI),
            ],
            check=True,
        )
        print(f"=== Обложка сохранена: {cover_path} ===")
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors="replace") if e.stderr else str(e)
        print(f"Ошибка при экспорте обложки: {err}")

    return cover_path


def main():
    parser = argparse.ArgumentParser(description="Экспорт обложки из Typst в PNG")
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK_TYP_PATH)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    args = parser.parse_args()
    build_cover(args.book, args.cache_dir)


if __name__ == "__main__":
    main()
