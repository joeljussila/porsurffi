# Telegram bot — specification

Not built yet. This is the design to build against.

## What it is for

A travel assistant that handles the repetitive half of running a 30-person trip: reminders,
deadline chasing, FAQ answers, the daily dispatch during the trip itself.

## What it cannot do

**A bot cannot read chat history from before it joined a group.** This is a hard Telegram
limitation, not a configuration problem. The bot is for everything *going forward*; historical
context reaches the repo through the Desktop JSON export instead
(`data/telegram/HOW-TO-EXPORT.md`).

Bots also only see messages addressed to them unless privacy mode is disabled, which is worth
leaving on for the participant channels.

## Architecture

```
Telegram  ──►  bot  ──►  reads state/trip.yml, docs/, decisions/
                 │
                 ├─ answers FAQs directly (read-only, safe)
                 ├─ posts scheduled reminders (pre-approved content only)
                 └─ drafts anything new into the ADMIN channel for a human to forward
```

The bot is a **reader of this repo**, not a second source of truth. If it needs a fact, the fact
belongs in `state/trip.yml` first.

## Command surface

| Command | Who | Behaviour |
| --- | --- | --- |
| `/status` | anyone | Trip dates, destination, next deadline — straight from `state/trip.yml`. |
| `/pay` | anyone | Next payment amount, account, reference, deadline. |
| `/checklist` | anyone | What this person still has to do (visa, payment, form). |
| `/surf` | anyone | Today's surf report, during the trip. |
| `/schedule` | anyone | Today and tomorrow. |
| `/remind <who> <what> <when>` | organizers | Schedules a reminder. Drafts, does not send. |
| `/draft <channel> <brief>` | organizers | Calls `comms`, returns a draft to the admin channel. |

## Reminders — the part that actually saves time

2026's real pain was chasing people: ETA visa applications needed repeated reminders and Oona
tracked approvals by hand, and shirt sizes came in through a Forms round with missing responses
right up to the order deadline.

So the bot tracks **per-person completion state** for a small set of items — payment
installments, visa, forms, insurance — and DMs only the people who are outstanding. Never
blanket-spam the whole channel for something 80% of people already did.

That per-person state is **personal data**. It lives in a local store that is gitignored, not in
this repo.

## Build notes

- Python, `python-telegram-bot`. Token from BotFather, in an env var, never committed.
- The bot token belongs to whoever runs it — it is not a shared secret to paste in chat.
- Deploy somewhere with persistent state; a scheduler is needed for reminders.
- Start read-only (`/status`, `/pay`, `/checklist`). Add sending later, behind approval.
