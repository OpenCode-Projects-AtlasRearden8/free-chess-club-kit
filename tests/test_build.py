"""Tests for the Free Pop-Up Chess Club Kit build.

Every sheet must render to a valid, one-page, US Letter PDF whose text
matches the sheet it came from. Run with:  python3 -m pytest tests/ -v
"""

from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

import pytest
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build as build_mod  # noqa: E402

LETTER_WIDTH_PT = 612.0  # 8.5 inches
LETTER_HEIGHT_PT = 792.0  # 11 inches

# sheet name -> words that must appear in the extracted PDF text
EXPECTED_TEXT = {
    "welcome-and-etiquette": ["Welcome to the Board", "Touch move, gently", "one idea per game"],
    "teaching-ladder": ["Eight-Game Teaching Ladder", "Pawn", "castle", "stalemate"],
    "pairing-grid": ["Hand-Run Pairing Grid", "Round 4", "bye earns"],
    "tournament-tally": ["Club Night Tally Sheet", "Time control", "Scoring, the friendly version"],
    "progress-passport": ["My Chess Passport", "Throne Gap", "full chess"],
    "bring-a-friend": ["Bring a Friend", "No pieces", "No signups"],
}

# The printables are supposed to be unbranded: nothing about us, our
# tooling, or any player's personal data may sneak into the PDFs.
FORBIDDEN_TEXT = (
    "asdale",
    "dynamics",
    "LLC",
    "opencode",
    "glm",
    "dylan",
    "dylanasdale",
)


@pytest.fixture(scope="module")
def pdfs(tmp_path_factory):
    """Build every sheet once into a module-shared temp dir."""
    out_dir = tmp_path_factory.mktemp("printables")
    return {p.name: p for p in build_mod.build(out_dir=out_dir)}


def reader_for(path: Path) -> PdfReader:
    return PdfReader(BytesIO(path.read_bytes()))


class TestBuildCompleteness:
    def test_builds_every_sheet(self, pdfs):
        assert set(pdfs) == {f"{name}.pdf" for name in build_mod.SHEETS}

    def test_each_pdf_is_nonempty(self, pdfs):
        for name, path in pdfs.items():
            assert path.stat().st_size > 5_000, f"{name} looks too small for a real PDF"


class TestPdfValidity:
    def test_header_bytes(self, pdfs):
        for name, path in pdfs.items():
            data = path.read_bytes()
            assert data[:5] == b"%PDF-", f"{name} lacks %PDF magic header"

    def test_exactly_one_page_each(self, pdfs):
        for name, path in pdfs.items():
            reader = reader_for(path)
            assert len(reader.pages) == 1, f"{name} spilled onto {len(reader.pages)} pages"

    def test_us_letter_page_size(self, pdfs):
        for name, path in pdfs.items():
            box = reader_for(path).pages[0].mediabox
            width, height = float(box.width), float(box.height)
            assert (width, height) == (LETTER_WIDTH_PT, LETTER_HEIGHT_PT), f"{name} is not US Letter"

    def test_renders_expected_text(self, pdfs):
        for name, needles in EXPECTED_TEXT.items():
            text = reader_for(pdfs[f"{name}.pdf"]).pages[0].extract_text() or ""
            # Letter-spaced kickers extract with spaces inside words; collapse
            # all whitespace so the match stays robust.
            compact = "".join(text.lower().split())
            for needle in needles:
                assert "".join(needle.lower().split()) in compact, (
                    f"{name}: {needle!r} missing from PDF text"
                )

    def test_ladder_has_eight_games(self, pdfs):
        text = reader_for(pdfs["teaching-ladder.pdf"]).pages[0].extract_text() or ""
        compact = "".join(text.lower().split())
        for numbered in ("2addthetwokings", "6addbothqueens", "8realchess"):
            assert numbered in compact, f"teaching-ladder: game {numbered!r} missing"


class TestUnbranded:
    def test_no_branding_or_secrets_in_pdf_text(self, pdfs):
        for name, path in pdfs.items():
            text = reader_for(path).pages[0].extract_text().lower()
            for bad in FORBIDDEN_TEXT:
                assert bad not in text, f"{name} contains forbidden token {bad!r}"

    def test_no_branding_in_html_sources(self):
        for name in build_mod.SHEETS:
            html_text = (build_mod.SRC / f"{name}.html").read_text(encoding="utf-8").lower()
            for bad in ("asdale", "dynamics", "llc", "opencode", "dylan"):
                assert bad not in html_text, f"{name}.html contains forbidden token {bad!r}"

    def test_css_sources_have_no_external_urls(self):
        css = (build_mod.SRC / "shared.css").read_text(encoding="utf-8")
        assert "http://" not in css and "https://" not in css, "CSS must stay fully local"
        for name in build_mod.SHEETS:
            html = (build_mod.SRC / f"{name}.html").read_text(encoding="utf-8")
            assert "http://" not in html and "https://" not in html, f"{name}.html is not fully local"


class TestBuildScript:
    def test_unknown_sheet_name_rejected(self, tmp_path):
        with pytest.raises(SystemExit):
            build_mod.build(out_dir=tmp_path, only=("does-not-exist",))

    def test_build_is_idempotent(self, tmp_path):
        first = build_mod.build(out_dir=tmp_path)
        second = build_mod.build(out_dir=tmp_path)
        assert [(p.name, p.stat().st_size) for p in first] == [
            (p.name, p.stat().st_size) for p in second
        ]
