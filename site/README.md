# porsurf.com

Reveal page, live from 2026-10-06 12:00 Helsinki time. "PorSurffi 2027" and "El Salvador" are
typed, deleted and retyped over five pictures. Every 7 seconds the next picture dissolves in on
top of the previous one (2 s dissolve, 5 s hold). The countdown page this replaces is in git
history (`7a6b4f3`). No build step, no dependencies. Everything is in this folder.

| File | What |
| --- | --- |
| `index.html` | The page. Texts: `texts` in the script. Darkness over the pictures: `--dim` in `:root`. |
| `assets/pic-1.jpg` ... `pic-5.jpg` | The pictures, already graded to the 1970s look (see below). To change what stays in view when a screen crops one, edit its `object-position` in `index.html`. |
| `assets/hero.mp4`, `assets/poster.jpg` | Countdown page video and still. Not used by the reveal page. |
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
