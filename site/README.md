# porsurf.com

Two-stage site: the original countdown and surf video run until **2026-10-06 at 12:00 noon
Helsinki time**, then automatically open Joel's reveal page. The deadline was confirmed by
Viljami in the organizer's Codex chat on 2026-10-06 and is configured once in `reveal-gate.js`:
`2026-10-06T12:00:00+03:00` (09:00 UTC; Helsinki is on EEST, not winter EET).

Before the deadline, "The countdown has begun." and the live countdown alternate in the
original typewriter loop. The poster is the fallback if video autoplay is blocked. After the
deadline, "PorSurffi 2027" and "El Salvador" are typed, deleted and retyped over Joel's five
pictures. Every 7 seconds the next picture dissolves in (2 s dissolve, 5 s hold). Returning to
an inactive tab rechecks the deadline; new visitors after noon go straight to the reveal.
Reduced-motion visitors see a static countdown/poster, then a static reveal photo and title.
No build step, no dependencies. Everything is in this folder.

This is a client-clock-based presentation gate, not a secret-content access control: visitors
can open `reveal.html` directly. The reveal artwork is from Joel's `reveal` branch (`8881a00`);
its destination text does not independently confirm a supplier booking or trip-state decision.

| File | What |
| --- | --- |
| `index.html` | Original countdown page and looping surf video. |
| `reveal-gate.js` | Shared deadline and automatic transition, independent of the typing loop. |
| `reveal.html` | Joel's reveal. Texts: `texts` in the script. Darkness: `--dim` in `:root`. |
| `assets/pic-1.jpg` ... `pic-5.jpg` | Joel's graded pictures. Cropping: `object-position` in `reveal.html`. |
| `assets/hero.mp4`, `assets/poster.jpg` | Countdown video and poster fallback. |
| `favicon.png` | 64 x 64 wave-and-surfboard favicon in the Cyanotype palette. |

## Grading the pictures

Same look as the video, with more colour kept:

```bash
ffmpeg -i source.jpg -vf "scale='if(gt(iw,ih),min(1800,iw*2),-2)':'if(gt(iw,ih),-2,min(1800,ih*2))':flags=lanczos,\
eq=brightness=-0.02:contrast=0.9:saturation=0.85,\
curves=r='0/0.08 0.5/0.52 1/0.93':g='0/0.06 0.5/0.48 1/0.88':b='0/0.05 0.5/0.43 1/0.80',\
rgbashift=rh=2:bh=-2,gblur=sigma=0.6,noise=alls=12:allf=u,vignette=angle=PI/5" -q:v 4 assets/pic-N.jpg
```

## Preview locally

```bash
cd site && python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy to porsurf.com (Vercel)

Run the dependency-free timing tests from the repository root: `node --test site/tests/*.test.cjs`.
They cover the exact boundary, different visitor timezones, inactive-tab return, and nested hosting paths.

1. Vercel -> Add New -> Project -> import `joeljussila/porsurffi`.
2. Framework preset: **Other**. Root directory: **`site`**. No build command, no output
   directory.
3. Deploy, then Project -> Settings -> Domains -> add `porsurf.com` and `www.porsurf.com`.
4. At the registrar, set the DNS records Vercel shows (an `A` record for the apex, a `CNAME`
   for `www`), or point the nameservers to Vercel.

Any static host works the same way (Netlify, Cloudflare Pages, GitHub Pages): publish the
`site/` folder as-is.

## The 1970s look

The graded source video is baked in with ffmpeg, so every browser shows the same result:

```bash
ffmpeg -i source.mp4 -an -vf "fps=24,eq=brightness=-0.03:contrast=0.82:saturation=0.6,\
curves=r='0/0.12 0.5/0.50 1/0.86':g='0/0.09 0.5/0.44 1/0.80':b='0/0.07 0.5/0.38 1/0.70',\
rgbashift=rh=2:bh=-2,gblur=sigma=0.7,noise=alls=14:allf=t+u,vignette=angle=PI/5,\
fade=t=in:st=0:d=1.2,fade=t=out:st=30.9:d=1.4,format=yuv420p" -t 32.3 \
  -c:v libx264 -preset slow -crf 27 -movflags +faststart assets/hero.mp4
```

What each step does: 24 fps for film cadence, darker and flatter contrast, desaturated, lifted
warm blacks and dulled highlights (the faded tape look), a 2 px red/blue colour fringe, slight
softness, moving grain and a vignette. The fade in and fade out make the loop seamless: each
pass ends on black and the next starts from black, so there is no hard cut.

To make the video darker or lighter, change `brightness` (e.g. `-0.08` for darker) and re-run.
