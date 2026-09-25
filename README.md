# PorSurffi

The trip brain for **PorSurffi**, the surf trip of PoRa / Prodeko at Aalto University.

This repo is the shared memory. Decisions, numbers, drafts and research live here as files so
they survive the organizer team turning over each year — which it does, every year.

**Current status:** planning PorSurffi 2027. Destination **undecided**; see
[`state/trip.yml`](state/trip.yml).

## Start here

| File | What it is |
| --- | --- |
| [`state/trip.yml`](state/trip.yml) | Single source of truth. Dates, headcount, budget, who owns what. |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | How the agent system is wired and why. |
| [`docs/2026-baseline.md`](docs/2026-baseline.md) | What the 2026 trip actually cost and where it went wrong. |
| [`docs/channels.md`](docs/channels.md) | The four Telegram channels and what belongs in each. |
| [`decisions/`](decisions/) | One file per real decision, including why the alternatives lost. |
| [`site/`](site/) | The porsurf.com countdown page. Static, deploy the folder as-is. |

## The agents

Seven definitions in [`.claude/agents/`](.claude/agents/). One orchestrator (`trip-brain`) and
six specialists: `scout`, `planner`, `comms`, `marketing`, `dispatch`, `safety`.

If you use **Claude Code**, they load automatically in this repo. If you use **ChatGPT** or
anything else, open the file and paste the body below the frontmatter as a system prompt — they
are deliberately plain markdown so this works.

One rule runs through all of them: **agents draft, people send.** Nothing reaches a participant
channel without a human approving it.

## Working in this repo

```bash
# Pull the Telegram history into a readable digest
python scripts/ingest_telegram.py data/telegram/<export>.json

# Strip secrets out of anything before sharing it
python scripts/redact.py <file> --write
```

Conventions: prices in EUR, dates as `YYYY-MM-DD`, and **every number carries a source** — a
chat date, a document, a quote, or the explicit word `assumption`.

## What is deliberately not here

The raw Telegram exports are gitignored. They contain a personal IBAN, a door code and 25
participants' full names. Keep them local.

**Nothing that names a participant belongs in this repo.**

## Trip principles and organizer workflow

- [Trip DNA](docs/trip-dna.md) - the core promise, experience pillars, and decision filter for future trips.
- [Organizer workflow](docs/organizer-workflow.md) - a reusable phase-by-phase playbook from defining the trip through post-trip closeout.
