# Free Pop-Up Chess Club Kit

Free printables for running a tiny pop-up chess club at a library table, a
coffee shop, or a kitchen table — nothing to install at the venue, no
signups, no apps, no chess clock required. Print the sheets at 100% scale on
US Letter, bring a board (or three), and you have a club: a welcome poster,
a one-idea-per-game teaching ladder, a hand-run pairing grid, a tally sheet,
a take-home stamp passport, and a bring-a-friend flyer. The PDFs are
unbranded — share them, stack them on the counter, staple them to the
community board.

Made the way we like everything at **Asdale Dynamics, LLC** — plain English,
warm tone, local-first, and printed pages that don't judge anyone's
openings. Everything builds from plain HTML/CSS with one local script.

## What's in the kit

| Sheet | What it's for |
| --- | --- |
| Welcome & etiquette poster | Prop-up page answering the two questions every new face asks — *what is this?* and *how do I behave?* — with seven gentle house rules |
| Eight-game teaching ladder | Beginner ladder, one chess idea per game, from pawns-only to a full real game, with scripts the host can actually say out loud |
| Hand-run pairing grid | Four rounds, up to 12 boards, write-in pair slots, bye rules, and a Swiss-the-easy-way cheat box |
| Club night tally sheet | Clipboard scoreboard: one row per player, round columns, totals, and a "new idea learned" column worth more than the score |
| Progress passport | Take-home sheet players stamp each visit — eight ladder stamps plus bonus stamps for brave moments |
| Bring-a-friend cards | Two cut-out cards per page with a where/when blank to fill in before stapling |

## How the club fits together

The teaching ladder and the club night share one rhythm: beginners play
ladder games and collect ladder stamps; graduates of Game 8 join the main
pairing grid. Pair on the grid, mark the tally, stamp passports, announce
nobody is ranked. The welcome poster does the explaining so you don't have
to.

## Build it yourself

Requirements: **Python 3.10+** and **WeasyPrint** —

```bash
pip install weasyprint
python3 build.py
```

That renders every sheet in `src/` into `printables/` as six separate
US Letter PDFs. Nothing touches the network; fonts come from your own
system (Georgia/serif and Arial/sans fallbacks are fine too).

```bash
python3 build.py --only teaching-ladder pairing-grid   # just these two
python3 build.py --out /tmp/mine                        # different output folder
```

## Tests

Every sheet is verified to build — valid PDF, exactly one page, correct US
Letter size, expected text present, no branding, no personal data, no
external URLs, and the ladder really has all eight games:

```bash
pip install weasyprint pypdf pytest
python3 -m pytest tests/ -v
```

## Make it yours

The sources are plain HTML + one shared stylesheet. Edit the text in
`src/*.html`, restyle in `src/shared.css`, re-run `python3 build.py`.
Renaming the club night, changing the bye rules, or adding a ninth ladder
game is a five-minute edit and one re-print.

## Friends of the kit

This kit runs the *club*; these siblings feed the players:

- **chess-beginner-comeback-guide** — a warm manual for lapsed grown-up
  beginners, from rules refresher to ten-game starter plan
- **chess-puzzle-drills** — a local puzzle-drill site for daily practice
- **free-chess-scoresheet-pack** — printable scoresheets, post-game
  reflection sheets, and a puzzle-drill booklet

Kit, guide, drills, and scoresheets each live in their own folder/repo and
are referenced by name on the welcome poster and passport — name only, so
nothing repeats and nothing links away from the table.

## Credits

Built and maintained by **Asdale Dynamics, LLC** as part of its
beginner-friendly, plain-English tools collection. Free to print at your
library, your coffee shop, and everywhere the pawns live. Licensed under
the MIT License (see `LICENSE`).
