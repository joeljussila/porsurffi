# Getting the Telegram chat in here

There is no Telegram connector for Claude — checked the registry, nothing exists.
The export is manual, one-time, and takes about five minutes.

## Telegram **Desktop** only

The phone apps cannot export. Install Telegram Desktop and log in.

1. Open the PorSurffi group.
2. Top-right **⋮** → **Export chat history**.
3. Uncheck photos, video, voice, files — **text only**. (Media balloons this to gigabytes
   and adds little planning signal. If a specific screenshot matters, send that one file.)
4. Format: **Machine-readable JSON**. *Not* HTML.
5. Date range: from the group's start through today.
6. Export → it writes a folder containing `result.json`.

Drop `result.json` into this directory, then:

```
python scripts/ingest_telegram.py data/telegram/result.json --chat "PorSurffi"
```

## Notes

- Telegram may impose a ~24h security delay before a first export unlocks. Per-chat exports
  usually start immediately; account-wide ones are the ones that wait.
- Multiple groups (2026 trip + 2027 planning)? Export each, or do one account-wide export
  and select with `--chat`.
