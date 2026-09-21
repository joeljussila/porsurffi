#!/usr/bin/env python3
"""
Ingest a Telegram Desktop JSON export into a normalized, queryable digest.

Usage:
    python scripts/ingest_telegram.py data/telegram/result.json
    python scripts/ingest_telegram.py data/telegram/result.json --chat "PorSurffi"

Handles both:
  * single-chat export   -> {"name":..., "messages":[...]}
  * full-account export  -> {"chats":{"list":[{...},...]}}

Writes to out/:
  messages.jsonl   one flattened message per line
  digest.md        stats, participants, per-topic extracts
"""
import argparse, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out")

# Bilingual FI/EN buckets - a Finnish group chat mixes both freely.
TOPICS = {
    "money": r"\b(€|eur|euro[sa]?|price|cost|paid|pay|deposit|refund|budget|invoice|split|"
             r"hinta|hinnat|maksu|maksoi|maksaa|lasku|budjetti|talletus|varausmaksu|kustannu)\w*",
    "flights": r"\b(flight|fly|airline|airport|layover|baggage|check-in|boarding|"
               r"lento|lennot|lentokent|matkalaukku|kone|välilasku)\w*",
    "lodging": r"\b(villa|hotel|hostel|guesthouse|accommodation|booking|airbnb|room|check-?out|"
               r"majoitus|hotelli|huone|varaus|talo)\w*",
    "surf": r"\b(surf|wave|swell|board|lineup|reef|beach break|point break|lesson|instructor|"
            r"aalto|aallot|lauta|laudat|surffi|surffa|tunti)\w*",
    "transport": r"\b(tuk|tuk-tuk|bus|van|driver|transfer|train|scooter|taxi|pickup|"
                 r"bussi|kuljetus|kuski|juna|mopo|skootteri)\w*",
    "food": r"\b(food|restaurant|breakfast|dinner|lunch|vegan|vegetarian|allerg|"
            r"ruoka|ravintola|aamiainen|illallinen|kasvis|allergi)\w*",
    "admin": r"\b(visa|insurance|passport|vaccin|eta|form|sign ?up|deadline|"
             r"viisumi|vakuutus|passi|rokot|lomake|ilmoittaudu|deadline|määräaika)\w*",
    "problems": r"(problem|issue|broke|broken|sick|injur|lost|late|delay|cancel|complain|"
                r"sucked|disaster|mistake|wrong|annoying|queue|scam|overprice|refus|"
                r"ongelma|rikki|sairas|loukkaan|myöhäs|myohas|peruut|valitus|pieleen|harmi|"
                r"katastrofi|sekais|sotku|huono|jono|ei toiminut|ei toimi|karmea|surkea)",
}
COMPILED = {k: re.compile(v, re.I) for k, v in TOPICS.items()}
URL_RE = re.compile(r"https?://\S+")


def flatten(text):
    """Telegram 'text' is str, or a list of str / {type,text} fragments."""
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        parts = []
        for f in text:
            if isinstance(f, str):
                parts.append(f)
            elif isinstance(f, dict):
                parts.append(f.get("text", ""))
        return "".join(parts)
    return ""


def pick_chat(data, wanted):
    if "messages" in data:
        return data.get("name") or "(unnamed)", data["messages"]
    chats = (data.get("chats") or {}).get("list") or []
    if not chats:
        sys.exit("No chats found. Is this a Telegram Desktop JSON export?")
    if wanted:
        hits = [c for c in chats if wanted.lower() in (c.get("name") or "").lower()]
        if not hits:
            names = "\n".join(f"  - {c.get('name')} ({len(c.get('messages', []))} msgs)" for c in chats)
            sys.exit(f"No chat matching {wanted!r}. Available:\n{names}")
        c = max(hits, key=lambda c: len(c.get("messages", [])))
        return c.get("name"), c.get("messages", [])
    c = max(chats, key=lambda c: len(c.get("messages", [])))
    print(f"[i] No --chat given; using largest: {c.get('name')!r}", file=sys.stderr)
    return c.get("name"), c.get("messages", [])


def main():
    # Windows consoles default to cp1252 and die on emoji in chat names.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--chat", help="substring of the chat name to select")
    ap.add_argument("--max-per-topic", type=int, default=120)
    a = ap.parse_args()

    with open(a.path, encoding="utf-8") as fh:
        data = json.load(fh)

    name, raw = pick_chat(data, a.chat)
    os.makedirs(OUT, exist_ok=True)
    # Derive output names from the input file so multiple exports never clobber each other.
    stem = os.path.splitext(os.path.basename(a.path))[0]
    jsonl_name, digest_name = f"{stem}.messages.jsonl", f"{stem}.digest.md"

    msgs, senders, media = [], Counter(), Counter()
    buckets = defaultdict(list)
    links, first, last = [], None, None

    for m in raw:
        if m.get("type") == "service":
            continue
        txt = flatten(m.get("text")).strip()
        mt = m.get("media_type") or ("photo" if m.get("photo") else None) or ("file" if m.get("file") else None)
        if mt:
            media[mt] += 1
        if not txt:
            continue
        who = m.get("from") or "(unknown)"
        when = m.get("date", "")
        senders[who] += 1
        first = min(first, when) if first else when
        last = max(last, when) if last else when

        rec = {"id": m.get("id"), "date": when, "from": who, "text": txt,
               "reply_to": m.get("reply_to_message_id")}
        msgs.append(rec)
        for u in URL_RE.findall(txt):
            links.append((when, who, u))
        for topic, rx in COMPILED.items():
            if rx.search(txt):
                buckets[topic].append(rec)

    with open(os.path.join(OUT, jsonl_name), "w", encoding="utf-8") as fh:
        for r in msgs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    L = []
    w = L.append
    w(f"# Telegram digest - {name}\n")
    w(f"- Messages with text: **{len(msgs):,}**")
    w(f"- Date range: **{first[:10] if first else '?'} -> {last[:10] if last else '?'}**")
    w(f"- Participants: **{len(senders)}**")
    if media:
        w(f"- Media: " + ", ".join(f"{k} x{v}" for k, v in media.most_common()))
    w("\n## Who talked\n")
    w("| Person | Messages |")
    w("| --- | ---: |")
    for who, n in senders.most_common():
        w(f"| {who} | {n} |")

    w("\n## Topic hits\n")
    w("| Topic | Messages |")
    w("| --- | ---: |")
    for t in TOPICS:
        w(f"| {t} | {len(buckets[t])} |")

    if links:
        w(f"\n## Links shared ({len(links)})\n")
        seen = set()
        for when, who, u in links:
            if u in seen:
                continue
            seen.add(u)
            w(f"- `{when[:10]}` **{who}**: {u}")

    for t in TOPICS:
        rows = buckets[t]
        if not rows:
            continue
        w(f"\n## {t} ({len(rows)} messages)\n")
        shown = rows[: a.max_per_topic]
        for r in shown:
            line = " ".join(r["text"].split())
            if len(line) > 400:
                line = line[:400] + " ..."
            w(f"- `{r['date'][:10]}` **{r['from']}**: {line}")
        if len(rows) > len(shown):
            w(f"\n_... {len(rows) - len(shown)} more; see messages.jsonl_")

    with open(os.path.join(OUT, digest_name), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print(f"[ok] {name}: {len(msgs):,} messages -> out/{jsonl_name} + out/{digest_name}")


if __name__ == "__main__":
    main()
