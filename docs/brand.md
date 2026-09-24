# Brand — PorSurffi vol. 2

The visual reference for the organization and the 2027 trip. Everything visual (posters, promo
video graphics, Telegram banners, merch) follows this board and palette.

## Mood board

**Pinterest: "porsurffi vol. 2"** — <https://pin.it/6QuhEFheb> (16 pins as of 2026-09-23)

Cyanotype and risograph prints, blue-washed photography, a few warm orange sunset prints. Blue
dominates the board; orange is the accent, not an equal partner.

## Palette — "Cyanotype"

Chosen 2026-09-23. Every hex is sampled directly from a pin on the board (k-means cluster
centres per pin, no rounding), except Black, which replaced the board's warm ink `#231615` by
choice.

| Role | Name | Hex | Use |
| --- | --- | --- | --- |
| Primary | Deep navy | `#062A67` | Main dark background, headlines on light |
| Blue | Tide blue | `#205C96` | Secondary surfaces, subheads |
| Blue | Cyan blue | `#448BBD` | Illustration, lighter blue areas |
| Blue | Ice | `#C2E0E8` | Soft backgrounds, secondary text on navy |
| Accent | Hot orange | `#D3462B` | Buttons, prices, key highlights |
| Accent | Coral | `#DC7854` | Orange accents on navy, tags, illustration |
| Neutral | Cool white | `#F2FAFD` | Light background, text on navy |
| Neutral | Black | `#000000` | Text, strong contrast elements |

Rejected alternatives (same session): a "Riso pop" palette built on cobalt `#0A3ACE`, a "Sunset
print" palette on cream `#EDE0C6`, and an off-board "Signal orange" `#FF7A1A`.

## Usage rules

Contrast ratios are WCAG 2 values computed 2026-09-23. 4.5:1 is the minimum for body text, 3:1
for large text and shapes.

| Pairing | Ratio | Verdict |
| --- | --- | --- |
| Coral on Deep navy | 4.47:1 | Orange on navy — use Coral |
| Hot orange on Deep navy | 3.05:1 | Large headlines and shapes only |
| Hot orange on Cool white | 4.24:1 | Fine for headlines and buttons |
| White text on Hot orange | 4.49:1 | Button labels OK |
| Black text on Hot orange | 4.68:1 | Button labels OK |
| Any orange on Tide blue | 1.5–3.5:1 | Avoid |

- Navy background → Coral for orange text, Hot orange only for buttons and big shapes.
- Light background → Hot orange for accents, navy for headlines.
- Never put orange on Tide blue.
