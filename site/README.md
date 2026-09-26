# porsurf.com

Home page from Claude Design: "The countdown has begun." types once, is erased, then a live
countdown types in over an animated surf image. No build step, no dependencies. Everything is
in this folder. The countdown currently targets 2026-10-06 at 12:00 Helsinki time, inherited
from the original countdown page (`ee19d09`). Current planning notes leave the launch date
unconfirmed and mention a different opening time; confirm with organizers before publishing.

| File | What |
| --- | --- |
| `index.html` | The page. Darkness over the background: `--dim` in `:root` (0 = none, 0.6 = very dark). |
| `assets/hero-animation.webp` | 32 s looping animated WebP at 720 × 540 and 24 fps, converted from the source video. |
| `assets/hero.mp4` | Original graded source video retained for future edits; not used on the page. |
| `assets/poster.jpg` | Static background fallback, including when reduced motion is enabled. |
| `favicon.png` | 64 × 64 wave-and-surfboard favicon in the Cyanotype palette. |

## Preview locally

```bash
cd site && python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy to porsurf.com (Vercel)

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
