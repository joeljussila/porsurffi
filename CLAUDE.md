# PorSurffi: Claude's starting instructions

Read [`AGENTS.md`](AGENTS.md) first and follow it for every task, including tasks delegated to a specialist in `.claude/agents/`. It is the shared policy for Claude, Codex, and other AI helpers. This file is a quick entry point, not a separate set of rules.

## Why this workspace exists

PorSurffi is the PoRa / Prodeko surf trip at Aalto University. This repo is the organizers' shared memory across people and years: confirmed facts, decisions and their reasoning, sourced research, and reusable plans. The 2026 Sri Lanka trip is a baseline, not an instruction to repeat it. GitHub is the memory; Telegram is the conversation. See [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`docs/trip-dna.md`](docs/trip-dna.md) for the bigger picture.

Some collaborators will not be comfortable with Git or technical file formats. Guide them in plain language, make reasonable progress on their behalf, explain what is confirmed versus proposed, and ask for human decisions only when needed.

## Starting a task

1. Run `git status --short --branch` and `git remote -v`, then `git pull --ff-only` on the current tracking branch **before making changes**. The shared remote is `origin` (`joeljussila/porsurffi`), normally tracking `master`. If it cannot update safely, preserve local work and explain the blocker.
2. Read [`state/trip.yml`](state/trip.yml) for current confirmed facts and [`decisions/`](decisions/) for actual decisions. Read the relevant material in [`docs/`](docs/) before researching or drafting. Check old deadlines and changing external facts again; do not treat an old plan as a new decision.
3. Use `.claude/agents/` for specialist work when useful. Their prompts add domain context but do not override `AGENTS.md` or human approval requirements.

## Where to put the result

- Confirmed trip state and workstream status: `state/trip.yml`, with evidence.
- Organizer decisions and rejected alternatives: one entry in `decisions/`.
- Research, context, plans, and reusable drafts: the relevant file in `docs/`.
- Telegram bot behavior: `bot/`; scripts and generated digests: see `AGENTS.md`.

Every consequential figure needs a dated source or an explicit `assumption`. Use EUR and `YYYY-MM-DD`. Keep participant identities, raw chat exports, account details, door codes, and secrets out of Git. `scripts/redact.py` does **not** anonymize names. Only a person approves and sends participant-facing messages; agents do not book, pay, or contact people on their own.

## Completing a task

Check the work, stage only this task's files, review the staged diff, commit, and push all delivered work to the shared remote. Fetch and safely reconcile any remote changes before pushing; never force-push or sweep up untracked files. In particular, the root `ChatExport_.../` folder may contain private raw data and is not covered by the current ignore rule. If the push fails, say so explicitly. End with a brief, non-technical summary and the human decision or next action, if any.
