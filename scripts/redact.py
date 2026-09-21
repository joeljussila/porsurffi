#!/usr/bin/env python3
"""
Strip secrets out of a text/markdown/jsonl file before it is shared or committed.

    python scripts/redact.py out/foo.digest.md              # report only
    python scripts/redact.py out/foo.digest.md --write      # rewrite in place
    python scripts/redact.py out/foo.digest.md -o clean.md  # write elsewhere

Handles: IBANs, card fragments, door/PIN codes, phone numbers, email addresses.

It does NOT anonymize personal names — there is no reliable way to do that automatically
and a half-anonymized roster is worse than an obviously private one. Keep files that name
participants out of the repo entirely (see .gitignore).
"""
import argparse, re, sys

RULES = [
    # Trailing group may be shorter than 4 (a Finnish IBAN ends in a 2-char group).
    ("IBAN",      re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4})+(?:[ ]?[A-Z0-9]{1,3})?\b"),
                  "[IBAN REDACTED]"),
    ("card tail", re.compile(r"((?:kortin|card)\D{0,20}?)\d{4}\b", re.I),          r"\1[REDACTED]"),
    ("door code", re.compile(r"((?:koodi|code|pin)\D{0,6}?)\d{4,8}#?", re.I),      r"\1[REDACTED]"),
    # Use [ -] not \s: \s spans newlines and swallows the following line.
    ("phone",     re.compile(r"\+358[ \d-]{6,15}|\b0\d{2}[ -]?\d{3}[ -]?\d{3,4}\b"), "[PHONE REDACTED]"),
    ("email",     re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b"),                   "[EMAIL REDACTED]"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("-o", "--out")
    ap.add_argument("--write", action="store_true", help="rewrite the input file in place")
    a = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    with open(a.path, encoding="utf-8") as fh:
        text = fh.read()

    total = 0
    for label, rx, sub in RULES:
        text, n = rx.subn(sub, text)
        total += n
        print(f"  {label:10} {n:3} redacted")

    dest = a.out or (a.path if a.write else None)
    if dest:
        with open(dest, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"[ok] {total} redactions -> {dest}")
    else:
        print(f"[dry run] {total} redactions found; pass --write or -o to apply")
    return 1 if total and not dest else 0


if __name__ == "__main__":
    sys.exit(main())
