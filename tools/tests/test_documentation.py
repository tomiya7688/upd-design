"""Documentation language-pair and relative-link regression tests."""
from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]

PAIRS = {
    "README.md": "en/README.md",
    "docs/users/README.md": "docs/users/en/README.md",
    "docs/users/メリット.md": "docs/users/en/benefits.md",
    "docs/users/具体例.md": "docs/users/en/examples.md",
    "docs/developers/README.md": "docs/developers/en/README.md",
    "docs/developers/境界.md": "docs/developers/en/boundaries.md",
    "docs/developers/実装.md": "docs/developers/en/implementation.md",
    "docs/developers/レビュー.md": "docs/developers/en/review-checklist.md",
    "docs/developers/検査ツール.md": "docs/developers/en/checker.md",
    "tools/README.md": "tools/en/README.md",
}

LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
JAPANESE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


class DocumentationTests(unittest.TestCase):
    def test_all_pages_have_language_pairs(self):
        for japanese, english in PAIRS.items():
            with self.subTest(japanese=japanese, english=english):
                self.assertTrue((ROOT / japanese).is_file())
                self.assertTrue((ROOT / english).is_file())

    def test_language_matched_filenames(self):
        for japanese, english in PAIRS.items():
            with self.subTest(japanese=japanese):
                self.assertTrue(japanese.endswith("README.md") or JAPANESE.search(Path(japanese).stem))
                self.assertFalse(JAPANESE.search(Path(english).name))

    def test_language_switch_links(self):
        for japanese, english in PAIRS.items():
            with self.subTest(page=japanese):
                text = (ROOT / japanese).read_text(encoding="utf-8")
                self.assertIn("[English](", text)
                self.assertTrue(any(
                    (ROOT / japanese).parent.joinpath(unquote(link)).resolve() == (ROOT / english).resolve()
                    for link in LINK.findall(text)
                ))
            with self.subTest(page=english):
                text = (ROOT / english).read_text(encoding="utf-8")
                self.assertIn("[日本語](", text)
                self.assertTrue(any(
                    (ROOT / english).parent.joinpath(unquote(link)).resolve() == (ROOT / japanese).resolve()
                    for link in LINK.findall(text)
                ))

    def test_english_prose_has_no_japanese_characters(self):
        for english in PAIRS.values():
            with self.subTest(english=english):
                text = (ROOT / english).read_text(encoding="utf-8")
                text = re.sub(r"\[日本語\]\([^)]*\)", "", text)
                self.assertFalse(JAPANESE.search(text), "English page contains Japanese text")

    def test_relative_markdown_links_exist(self):
        for name in (*PAIRS, *PAIRS.values()):
            path = ROOT / name
            for link in LINK.findall(path.read_text(encoding="utf-8")):
                if link.startswith(("https://", "http://", "mailto:", "#")):
                    continue
                target = unquote(link.split("#", 1)[0].split("?", 1)[0])
                if not target:
                    continue
                with self.subTest(page=name, target=target):
                    self.assertTrue((path.parent / target).exists(), f"{name}: {target}")


if __name__ == "__main__":
    unittest.main()
