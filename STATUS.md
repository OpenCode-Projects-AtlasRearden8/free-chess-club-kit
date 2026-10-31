# STATUS — Free Pop-Up Chess Club Kit

Last updated: 2026-10-31

## What was built

A complete printable kit for running a tiny pop-up chess club at a library,
coffee shop, or kitchen table. Six HTML/CSS sheets in `src/` build into six
unbranded US Letter PDFs in `printables/` via one local build script. No
signups, no network calls, no secrets, no personal data. It complements
**chess-beginner-comeback-guide** and **chess-puzzle-drills** (and the
**free-chess-scoresheet-pack**) by running the *club itself* rather than
repeating their player-facing content; the siblings are referenced by name
only.

| Sheet (PDF) | Purpose |
| --- | --- |
| `welcome-and-etiquette.pdf` | Prop-up poster: what the club is, seven gentle house rules, quick answers for the shy, ladder teaser |
| `teaching-ladder.pdf` | Eight-game beginner ladder, one idea per game (pawn march → throne gap → rook highway → bishop's color → knight leap → queen safety → castling → full chess), with host scripts and "done when" gates |
| `pairing-grid.pdf` | Hand-run pairing grid: 4 rounds × up to 6 boards, write-in slots, bye rules, Swiss-the-easy-way cheat box |
| `tournament-tally.pdf` | Clipboard tally: event header, 12 player rows, round columns, totals, "new idea learned" column, scoring ritual notes |
| `progress-passport.pdf` | Take-home passport: 8 ladder stamp boxes + 6 bonus stamps (first win, clean handshake, taught a friend…) |
| `bring-a-friend.pdf` | Two cut-out flyer cards per page with where/when blanks |

Supporting files: `build.py` (build script), `tests/test_build.py`
(12-test suite), `README.md`, `LICENSE` (MIT, copyright
`Copyright (c) 2026 Asdale Dynamics, LLC` as credited in the README),
`.gitignore`.

## How to run it

```bash
pip install weasyprint          # local renderer only (no accounts/keys)
python3 build.py                # builds all 6 PDFs into printables/
python3 build.py --only teaching-ladder   # subset build
python3 -m pytest tests/ -v     # verify every sheet builds a valid PDF
```

Print the PDFs at 100% scale ("Actual size") on US Letter.

## Verification results

- `python3 build.py` — builds all 6 sheets successfully (sizes 20.7–180.4 KB).
- `python3 -m pytest tests/` — **12 passed** (in ~6s). The suite verifies:
  - every sheet builds and produces a nonempty PDF with a `%PDF-` header
  - each sheet is exactly **1 page** and exactly **US Letter size (612×792 pt)**
  - expected per-sheet text is present in the extracted PDF text
  - the teaching ladder really contains all eight games
  - PDFs are unbranded: no company, tooling, or personal-data tokens
    (asdale / dynamics / LLC / opencode / glm / dylan / dylanasdale)
  - HTML/CSS sources are unbranded and contain no external URLs (fully local)
  - build rejects unknown sheet names and is idempotent
- Visual QA: all 6 PDFs rasterized with `pdftoppm` at 60–120 dpi and
  inspected — poster columns balance, the ladder table and pairing grid fit
  their page with footer, tally rows and passport stamp boxes align, and
  the 2-up flyer cuts cleanly along the dashed border.
- Fix loop that was caught and resolved by the tests: initial ladder and
  pairing-grid layouts spilled to 2 pages; tightened cell padding,
  line-height, and copy until every sheet was exactly one page again.

## Design notes

- Sheet design: US Letter, 0.5in margins, local system fonts only
  (Fraunces for headings, Karla for body; Georgia/Arial fallbacks) — the
  build works offline with zero font downloads.
- Chess-flavored palette: felt green, walnut brown, gold accents; the
  passport wears a full felt-green cover band.
- The tally page is larger (~180 KB) purely because of its many dotted
  rules; everything stays text-only, no images.

## Known gaps / ideas for later

- No A4 page-size variant (sources are Letter; one CSS change plus test
  update would add it — the tests pin Letter size).
- The pairing grid tops out at 4 rounds / 6 boards per round; a second page
  for bigger crowd nights (16–24 players) would be a new sheet, not an edit.
- Stamp sheet of pre-cut printable "stamps" (for hosts without a stamp pad)
  would be a fun seventh sheet.
- No editable/interactive form-field PDFs; sheets are designed for
  handwriting after printing, by design.
- WeasyPrint version differences (v70 used here to verify) may shift
  text-flow slightly on other versions; the 1-page test will catch overflow.
