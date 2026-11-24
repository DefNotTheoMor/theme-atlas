import argparse
import subprocess
from pathlib import Path

from build_glossary import (
    parse_typst_glossary,
    generate_glossary_html,
    inject_into_html,
)
from build_culture import process_culture
from build_cover import build_cover
from build_assets import build_assets

DEFAULT_TYP_PATH = Path("../sections/00-glossary.typ")
DEFAULT_BOOK_TYP_PATH = Path("../Атлас.typ")
DEFAULT_SVG_DIR = Path("../assets/images")
DEFAULT_CACHE_DIR = Path("cache")
DEFAULT_BUILD_DIR = Path("build")

CACHE_HTML_PATH = DEFAULT_CACHE_DIR / "atlas.html"
TEMP_GLOSSARY_PATH = DEFAULT_CACHE_DIR / "temp_1_glossary.html"
FINAL_HTML_PATH = DEFAULT_CACHE_DIR / "final.html"

EPUB_NAME = "atlas.epub"
FB2_NAME = "atlas.fb2"
RTF_NAME = "atlas.rtf"


def is_cache_fresh(book_typ_path: Path, target: Path) -> bool:
    if not target.exists() or not book_typ_path.exists():
        return False
    target_mtime = target.stat().st_mtime
    for typ_file in book_typ_path.parent.rglob("*.typ"):
        if typ_file.stat().st_mtime > target_mtime:
            return False
    return True


def build_html(book_typ_path: Path, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    html_out = cache_dir / "atlas.html"

    if is_cache_fresh(book_typ_path, html_out):
        print(f"0. HTML из Typst: [skip] {html_out}")
        return html_out

    print(f"0. Экспорт HTML из {book_typ_path}...")
    base_cmd = [
        "typst",
        "compile",
        str(book_typ_path.resolve()),
        str(html_out.resolve()),
        "--format",
        "html",
        "--root",
        str(book_typ_path.resolve().parent),
    ]

    for extra in (["--features", "html"], []):
        try:
            subprocess.run(base_cmd + extra, check=True, capture_output=True)
            print(f"=== HTML: {html_out} ===")
            return html_out
        except subprocess.CalledProcessError:
            continue

    raise RuntimeError(
        "Typst HTML export failed. Если ваша версия Typst требует флаг, "
        "добавьте --features html в вызов вручную."
    )


def build_pipeline(
    typ_path: Path, html_in_path: Path, svg_dir: Path, cache_dir: Path
) -> Path:
    print("=== СТАРТ СБОРКИ HTML ===")

    build_assets(svg_dir, cache_dir)

    print("2. Обработка глоссария...")
    entries = parse_typst_glossary(typ_path)
    glossary_html = generate_glossary_html(entries)
    inject_into_html(html_in_path, glossary_html, TEMP_GLOSSARY_PATH)

    print("3. Обработка культуры (PNG)...")
    process_culture(TEMP_GLOSSARY_PATH, FINAL_HTML_PATH, cache_dir)

    TEMP_GLOSSARY_PATH.unlink(missing_ok=True)
    print(f"=== HTML готов: {FINAL_HTML_PATH} ===")
    return FINAL_HTML_PATH


def build_epub(html_path: Path, cover_path: Path, cache_dir: Path, out_path: Path):
    print("5. Сборка EPUB...")
    subprocess.run(
        [
            "pandoc",
            str(html_path),
            "-o",
            str(out_path),
            "-t",
            "epub3",
            f"--epub-cover-image={cover_path}",
            f"--resource-path=.:{cache_dir}",
        ],
        check=True,
    )
    print(f"=== EPUB: {out_path} ===")


def build_fb2(html_path: Path, cover_path: Path, cache_dir: Path, out_path: Path):
    print("6. Сборка FB2...")
    subprocess.run(
        [
            "pandoc",
            str(html_path),
            "-o",
            str(out_path),
            f"--metadata=cover-image:{cover_path}",
            f"--resource-path=.:{cache_dir}",
        ],
        check=True,
    )
    print(f"=== FB2: {out_path} ===")


def build_rtf(html_path: Path, cache_dir: Path, out_path: Path):
    print("7. Сборка RTF...")
    subprocess.run(
        [
            "pandoc",
            str(html_path),
            "-o",
            str(out_path),
            f"--resource-path=.:{cache_dir}",
        ],
        check=True,
    )
    print(f"=== RTF: {out_path} ===")


def main():
    parser = argparse.ArgumentParser(description="Главный сборщик книги 'Атлас'")
    parser.add_argument("--typ", type=Path, default=DEFAULT_TYP_PATH)
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK_TYP_PATH)
    parser.add_argument(
        "--html",
        type=Path,
        default=None,
        help="Переопределить HTML-источник (по умолчанию cache/atlas.html)",
    )
    parser.add_argument("--svg-dir", type=Path, default=DEFAULT_SVG_DIR)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--build-dir", type=Path, default=DEFAULT_BUILD_DIR)
    args = parser.parse_args()

    args.cache_dir.mkdir(parents=True, exist_ok=True)
    args.build_dir.mkdir(parents=True, exist_ok=True)

    if args.html is not None:
        html_source = args.html
        print(f"=== Использую внешний HTML: {html_source} ===")
    else:
        html_source = build_html(args.book, args.cache_dir)

    final_html = build_pipeline(args.typ, html_source, args.svg_dir, args.cache_dir)
    cover_path = build_cover(args.book, args.cache_dir)

    build_epub(final_html, cover_path, args.cache_dir, args.build_dir / EPUB_NAME)
    build_fb2(final_html, cover_path, args.cache_dir, args.build_dir / FB2_NAME)
    build_rtf(final_html, args.cache_dir, args.build_dir / RTF_NAME)

    final_html.unlink(missing_ok=True)
    print("=== ВСЁ ГОТОВО ===")


if __name__ == "__main__":
    main()
