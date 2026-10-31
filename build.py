#!/usr/bin/env python3
"""Build the Free Pop-Up Chess Club Kit printables.

Renders every HTML sheet in src/ into an unbranded US Letter PDF inside
printables/. Local-only: no network calls, no accounts, just WeasyPrint.

Usage:
    python3 build.py              # build every sheet
    python3 build.py --only welcome-and-etiquette pairing-grid
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

SHEETS = (
    "welcome-and-etiquette",
    "teaching-ladder",
    "pairing-grid",
    "tournament-tally",
    "progress-passport",
    "bring-a-friend",
)


def build(out_dir: Path = ROOT / "printables", only: tuple[str, ...] = ()) -> list[Path]:
    """Render each sheet to a PDF. Returns the list of files written."""
    wanted = only if only else SHEETS
    unknown = [s for s in wanted if s not in SHEETS]
    if unknown:
        raise SystemExit(
            f"Unknown sheet(s): {', '.join(unknown)}\nKnown sheets: {', '.join(SHEETS)}\n"
        )

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    built: list[Path] = []
    for name in wanted:
        src_path = SRC / f"{name}.html"
        out_path = out_dir / f"{name}.pdf"
        HTML(filename=src_path).write_pdf(out_path)
        size_kb = out_path.stat().st_size / 1024
        try:
            shown = out_path.relative_to(ROOT)
        except ValueError:
            shown = out_path.resolve()
        print(f"  {name:<24} -> {shown}  ({size_kb:,.1f} KB)")
        built.append(out_path)
    return built


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Free Pop-Up Chess Club Kit PDFs.")
    parser.add_argument(
        "--only",
        nargs="*",
        default=(),
        metavar="SHEET",
        help=f"build only these sheets: {', '.join(SHEETS)}",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "printables",
        help="output directory (default: printables/)",
    )
    args = parser.parse_args()

    print("Building the Free Pop-Up Chess Club Kit printables...\n")
    built = build(out_dir=args.out, only=args.only)
    print(f"\nDone: {len(built)} sheet(s) in {Path(args.out).resolve()}")
    print("Print at 100% scale ('Actual size'), US Letter. Unbranded — share freely.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
