# Website countdown and reveal timing

- Status: confirmed
- Decision date: 2026-10-06
- Source: Viljami's organizer Codex request on 2026-10-06 to combine the old countdown with
  Joel's `reveal` branch, followed by the clarification "no, 12 pm, midday".
- Implementation owner: Viljami / Codex
- Deadline: 2026-10-06 12:00 Europe/Helsinki (EEST, UTC+3)

Keep the existing video/countdown design until noon, then automatically open Joel's reveal
design. New visitors after the deadline see the reveal immediately. The deadline check must
work independently of the typewriter loop and recheck when a suspended tab becomes visible.

Alternatives not chosen:

- Midnight: the first request said "12 am", but Viljami explicitly corrected it to midday.
- Fixed winter EET (UTC+2): Viljami specified Finnish Helsinki local time; Helsinki is on
  summer time on this date. The implementation uses the explicit UTC+3 instant.
- Replacing the countdown immediately with Joel's page: this loses the requested countdown.

Scope: website presentation and timing only. Joel's artwork says "El Salvador", while
`state/trip.yml` still records the destination as undecided. This request is not evidence of
an organizer destination decision, supplier acceptance, or booking; those remain unchanged.
