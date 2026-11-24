import re
import argparse
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup

DEFAULT_TYP_PATH = Path("../sections/00-glossary.typ")
DEFAULT_HTML_IN_PATH = Path("cache/atlas.html")
DEFAULT_HTML_OUT_PATH = Path("cache/temp_1_glossary.html")

GLOSSARY_HEADER_TEXT = "Глоссарий"
BIBLIOGRAPHY_ROLE = "doc-bibliography"

REGEX_ENTRIES_BLOCK = r"#let entries = \((.*?)\n\)"
REGEX_ENTRY_SPLIT = r"\n  \("
REGEX_FIELD_TEMPLATE = r'{field}:\s*"((?:[^"\\]|\\.)*)"'
REGEX_DESCRIPTION = r"description:\s*\[(.*?)\]"
REGEX_CITATION = r"@(\w+)"
REGEX_TYPST_ESCAPE = r"\\(u\{[0-9a-fA-F]+\}|.)"

CITATION_HTML_TEMPLATE = r'<a href="#ref-\1" class="cite">[\1]</a>'

ESCAPE_MAP = {
    "n": "\n",
    "r": "\r",
    "t": "\t",
    '"': '"',
    "\\": "\\",
}


def unescape_typst_string(s: str) -> str:
    def replacer(m):
        esc = m.group(1)
        if esc.startswith("u{") and esc.endswith("}"):
            return chr(int(esc[2:-1], 16))
        return ESCAPE_MAP.get(esc, "\\" + esc)

    return re.sub(REGEX_TYPST_ESCAPE, replacer, s)


def parse_typst_glossary(typ_path: Path) -> list[dict]:
    content = typ_path.read_text(encoding="utf-8")

    entries_match = re.search(REGEX_ENTRIES_BLOCK, content, re.DOTALL)
    if not entries_match:
        raise ValueError(f"Не удалось найти блок '#let entries = (...)' в {typ_path}")

    raw_entries_text = entries_match.group(1)
    raw_entries = re.split(REGEX_ENTRY_SPLIT, raw_entries_text)

    entries = []
    for raw in raw_entries:
        if not raw.strip():
            continue

        entry = {}

        for field in ["key", "short", "long", "group"]:
            match = re.search(REGEX_FIELD_TEMPLATE.format(field=field), raw)
            if match:
                entry[field] = unescape_typst_string(match.group(1))

        desc_match = re.search(REGEX_DESCRIPTION, raw, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
            desc = unescape_typst_string(desc)
            desc = re.sub(REGEX_CITATION, CITATION_HTML_TEMPLATE, desc)
            entry["description"] = desc

        if "key" in entry and "short" in entry:
            entries.append(entry)

    return entries


def generate_glossary_html(entries: list[dict]) -> str:
    grouped = defaultdict(list)
    for entry in entries:
        group = entry.get("group", "Разное")
        grouped[group].append(entry)

    html_parts = []

    for group_name, group_entries in grouped.items():
        html_parts.append(f"<h3>{group_name}</h3>")
        html_parts.append("<dl>")

        for entry in group_entries:
            short = entry.get("short", "")
            long_desc = entry.get("long", "")
            desc = entry.get("description", "")
            key = entry.get("key", "")

            anchor = f'<span id="{key}"></span>'
            if long_desc:
                dt = f"<dt>{anchor}<strong>{short}</strong> – {long_desc}</dt>"
            else:
                dt = f"<dt>{anchor}<strong>{short}</strong></dt>"

            dd = f"<dd>{desc}</dd>"

            html_parts.append(dt)
            html_parts.append(dd)

        html_parts.append("</dl>")

    return "\n".join(html_parts)


def inject_into_html(html_in_path: Path, glossary_html: str, html_out_path: Path):
    soup = BeautifulSoup(html_in_path.read_text(encoding="utf-8"), "lxml")

    for nav in soup.find_all("nav", attrs={"role": "doc-toc"}):
        nav.decompose()

    glossary_header = None
    for h2 in soup.find_all("h2"):
        if GLOSSARY_HEADER_TEXT in h2.get_text():
            glossary_header = h2
            break

    if not glossary_header:
        raise ValueError(f"Не удалось найти заголовок '{GLOSSARY_HEADER_TEXT}' в HTML")

    next_section = None
    for sibling in glossary_header.find_next_siblings():
        if sibling.name == "section" and sibling.get("role") == BIBLIOGRAPHY_ROLE:
            next_section = sibling
            break

    if not next_section:
        next_section = soup.find("body")

    elements_to_remove = []
    current = glossary_header.find_next_sibling()
    while current and current != next_section:
        elements_to_remove.append(current)
        current = current.find_next_sibling()

    for el in elements_to_remove:
        el.decompose()

    new_glossary_soup = BeautifulSoup(glossary_html, "html.parser")

    for element in reversed(new_glossary_soup.contents):
        glossary_header.insert_after(element)

    html_out_path.parent.mkdir(parents=True, exist_ok=True)
    html_out_path.write_text(str(soup), encoding="utf-8")
    print(f"Глоссарий успешно внедрен в {html_out_path}")


def main():
    parser = argparse.ArgumentParser(description="Генератор глоссария для 'Атлас'")
    parser.add_argument(
        "--typ", type=Path, default=DEFAULT_TYP_PATH, help="Путь к .typ файлу глоссария"
    )
    parser.add_argument(
        "--html",
        type=Path,
        default=DEFAULT_HTML_IN_PATH,
        help="Путь к исходному HTML файлу",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_HTML_OUT_PATH,
        help="Путь для сохранения результата",
    )
    args = parser.parse_args()

    print(f"1. Парсинг {args.typ}...")
    entries = parse_typst_glossary(args.typ)
    print(f"   Найдено записей: {len(entries)}")

    print("2. Генерация HTML-глоссария...")
    glossary_html = generate_glossary_html(entries)

    print(f"3. Внедрение в {args.html}...")
    inject_into_html(args.html, glossary_html, args.out)

    print("Готово!")


if __name__ == "__main__":
    main()
