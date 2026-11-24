import argparse
from pathlib import Path
from bs4 import BeautifulSoup

DEFAULT_HTML_IN_PATH = Path("../Атлас.html")
DEFAULT_CACHE_DIR = Path("cache")
DEFAULT_HTML_OUT_PATH = DEFAULT_CACHE_DIR / "final.html"

FIGURE_CAPTION_MARKER = "Жюстина"
TARGET_HEIGHT_PX = 120

IMAGES = [
    ("sade_cross.png", "Логотип: крест с зарубками, маркиз де Сад", "«Жюстина»"),
    (
        "venus.png",
        "Логотип: куб с геральдическим щитом, Захер-Мазох",
        "«Венера в мехах»",
    ),
    ("mark.png", "Логотип: буква О с точкой, Полин Реаж", "«История О»"),
]


def process_culture(html_in_path: Path, html_out_path: Path, cache_dir: Path):
    soup = BeautifulSoup(html_in_path.read_text(encoding="utf-8"), "lxml")

    target_figure = None
    for fig in soup.find_all("figure"):
        caption = fig.find("figcaption")
        if caption and FIGURE_CAPTION_MARKER in caption.get_text():
            target_figure = fig
            break

    if not target_figure:
        raise ValueError("Не найдена фигура с тремя логотипами")

    wrapper = soup.new_tag(
        "div",
        style=(
            "display: flex; flex-wrap: wrap; "
            "justify-content: center; align-items: flex-end; "
            "gap: 2em; margin: 2em 0;"
        ),
    )

    for filename, alt, caption_text in IMAGES:
        png_path = cache_dir / filename
        if not png_path.exists():
            raise FileNotFoundError(f"Файл не найден: {png_path}")

        fig = soup.new_tag(
            "figure",
            style="text-align: center; margin: 0; flex: 0 0 auto;",
        )

        img = soup.new_tag("img")
        img["src"] = png_path.as_posix()
        img["alt"] = alt
        img["height"] = str(TARGET_HEIGHT_PX)
        img["style"] = (
            "height: auto; max-height: 120px; display: block; margin: 0 auto;"
        )
        fig.append(img)

        cap = soup.new_tag("figcaption", style="font-size: 0.9em; margin-top: 0.5em;")
        cap.string = caption_text
        fig.append(cap)

        wrapper.append(fig)

    target_figure.replace_with(wrapper)
    html_out_path.parent.mkdir(parents=True, exist_ok=True)
    html_out_path.write_text(str(soup), encoding="utf-8")
    print(f"Культура успешно обработана в {html_out_path}")


def main():
    parser = argparse.ArgumentParser(description="Обработчик культуры для 'Атлас'")
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML_IN_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_HTML_OUT_PATH)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    args = parser.parse_args()
    process_culture(args.html, args.out, args.cache_dir)


if __name__ == "__main__":
    main()
