import subprocess
import shutil
import argparse
from pathlib import Path

DEFAULT_SVG_DIR = Path("../assets/images")
DEFAULT_CACHE_DIR = Path("cache")

TARGET_HEIGHT_PX = 480
TYPST_PPI = 288
PAGE_FILL = "white"

SVGS = [
    "sade_cross.svg",
    "venus.svg",
    "mark.svg",
]

TYPST_HEIGHT_PT = round(TARGET_HEIGHT_PX * 72 / TYPST_PPI, 2)

TYPST_TEMPLATE = """#set page(width: auto, height: auto, margin: 0pt, fill: {fill})
#image("svgs/{svg_name}", height: {height_pt}pt)
"""


def convert_svg_to_png(svg_path: Path, png_path: Path, cache_dir: Path) -> bool:
    svg_cache = cache_dir / "svgs"
    svg_cache.mkdir(parents=True, exist_ok=True)

    tmp_svg = svg_cache / svg_path.name
    shutil.copy2(svg_path, tmp_svg)

    typ_path = cache_dir / (svg_path.stem + ".typ")
    typ_path.write_text(
        TYPST_TEMPLATE.format(
            fill=PAGE_FILL,
            svg_name=svg_path.name,
            height_pt=TYPST_HEIGHT_PT,
        ),
        encoding="utf-8",
    )

    try:
        subprocess.run(
            [
                "typst",
                "compile",
                typ_path.name,
                png_path.name,
                "--format",
                "png",
                "--ppi",
                str(TYPST_PPI),
            ],
            check=True,
            capture_output=True,
            cwd=cache_dir,
        )
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors="replace") if e.stderr else str(e)
        print(f"  [fail] typst: {err}")
        return False
    finally:
        typ_path.unlink(missing_ok=True)
        tmp_svg.unlink(missing_ok=True)

    return True


def build_assets(svg_dir: Path, cache_dir: Path):
    print("=== КОНВЕРТАЦИЯ SVG → PNG (typst) ===")
    cache_dir.mkdir(parents=True, exist_ok=True)

    for filename in SVGS:
        svg_path = svg_dir / filename
        if not svg_path.exists():
            print(f"  [miss] {svg_path}")
            continue

        png_path = cache_dir / filename.replace(".svg", ".png")

        if png_path.exists() and png_path.stat().st_mtime >= svg_path.stat().st_mtime:
            print(f"  [skip] {png_path.name}")
            continue

        if convert_svg_to_png(svg_path, png_path, cache_dir):
            size_kb = png_path.stat().st_size // 1024
            print(f"  [ok]   {png_path.name} ({size_kb} KB)")

    print("=== ГОТОВО ===")


def main():
    parser = argparse.ArgumentParser(description="Конвертация SVG → PNG через Typst")
    parser.add_argument("--svg-dir", type=Path, default=DEFAULT_SVG_DIR)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    args = parser.parse_args()
    build_assets(args.svg_dir, args.cache_dir)


if __name__ == "__main__":
    main()
