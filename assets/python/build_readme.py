#!/usr/bin/env python3
"""Generate the repository READMEs from the bilingual content sources."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README_FILES = {
    "pt-br.md": ("README.md", "🇧🇷 Português | [English](README.en.md)"),
    "en.md": ("README.en.md", "🇺🇸 English | [Português](README.md)"),
}


def main() -> None:
    for source_name, (output_name, language_links) in README_FILES.items():
        source = ROOT / "content" / source_name
        output = ROOT / output_name
        content = source.read_text(encoding="utf-8").strip()
        output.write_text(
            f"<!-- Generated from content/{source_name}; edit the source file. -->\n\n"
            f"{language_links}\n\n{content}\n",
            encoding="utf-8",
        )
        print(f"README gerado: {output_name}")


if __name__ == "__main__":
    main()
