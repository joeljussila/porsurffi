# Architecture

Two layers, one rule.

**GitHub is the memory.** Every decision, number, contact and draft lives here as a file.
It is the thing that survives the organizer team turning over each year.

**Telegram is the interface.** Four channels, each with one job. Nothing is *decided* in
Telegram; decisions land in `decisions/` and state lands in `state/trip.yml`.

**The rule: no agent sends anything to a human without a human approving it first.**
Agents draft. People send. This is not a trust issue — it is that a bot posting to 25
students' announcement channel at 3am is unrecoverable, and a wrong price in that post
costs real money.

```
                     ┌──────────────────┐
                     │   trip-brain     │  orchestrator — owns the plan,
                     │  (orchestrator)  │  delegates, keeps state/ true
                     └────────┬─────────┘
          ┌────────────┬──────┴──────┬────────────┬───────────┐
          ▼            ▼             ▼            ▼           ▼
       scout       planner         comms      marketing    dispatch
   destinations   budget +      drafts for    brand +     weather, surf,
   flights,       timeline,     the 4          promo,     wildlife, history
   surf camps,    logistics     channels      recruiting  for the fun channel
   group deals
          │
          ▼
       safety
   advisories, health,
   insurance, "is this
   actually a good idea"
```

## Why an orchestrator at all

Six agents that each talk to you directly is six things to remember. `trip-brain` exists so
there is **one** place to ask "what's the state of the trip" and one thing that notices when
the flight agent's answer invalidates the budget agent's model. It reads `state/trip.yml`,
decides which sub-agent to call, and writes the result back.

## The agents

| Agent | Owns | Never does |
| --- | --- | --- |
| **trip-brain** | The plan. Delegation. Keeping `state/trip.yml` true. | Research anything itself. |
| **scout** | Destinations, flights, surf camps, group deals, niche local finds. | Book. Quote a price without a source and a date. |
| **planner** | Budget model, payment schedule, timeline, rooming, logistics. | Invent numbers `scout` hasn't sourced. |
| **comms** | Drafts for all four channels, in the right voice per channel. | Send. Ever. |
| **marketing** | Brand, promo copy, the October recruitment push. | Promise anything not in `state/trip.yml`. |
| **dispatch** | Daily content for the fun channel — surf report, wildlife, history. | Give safety guidance. That's `safety`. |
| **safety** | Travel advisories, health, vaccines, insurance, risk calls. | Soften a finding to keep a destination alive. |

Definitions live in `.claude/agents/`. They are plain markdown — if a teammate uses ChatGPT
instead of Claude Code, the body of the file is a system prompt they can paste.

## State and decisions

- **`state/trip.yml`** — the single source of truth. Dates, headcount, budget, destination,
  status of each workstream. If an agent and this file disagree, this file wins.
- **`decisions/`** — one file per real decision, in the format `NNNN-slug.md`. Records what was
  decided, what the alternatives were, and **why the losers lost**. This is the part that makes
  next year's team fast instead of starting over.
- **`docs/`** — durable reference. The 2026 baseline, the channel playbook.

## Why this is reusable

Strip `state/trip.yml` and `decisions/`, keep everything else, and this runs any large group
trip. The genuinely transferable assets are the **2026 baseline** (what a 25-person student
surf trip actually costs and where it goes wrong), the **channel playbook**, and the **agent
definitions**. That is the sellable core — not the Sri Lanka specifics.

## The privacy boundary

The raw Telegram exports contain a **personal IBAN**, a door code, and **25 students' full
names**. They are gitignored and must stay that way. `scripts/redact.py` strips secrets from
anything you intend to share; it deliberately does **not** anonymize names, because a
half-anonymized roster is more dangerous than an obviously private file.

Rule of thumb: if a file names a participant, it does not go in this repo.
