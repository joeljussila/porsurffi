# porsurf.com - countdown site

A single static page: a countdown to registration opening, over the surf video on a loop. No
build step, no dependencies. Everything is in this folder.

| File | What |
| --- | --- |
| `index.html` | The page. Styles and the countdown script are inline. |
| `assets/hero.mp4` | Background video, already graded (see below). 32 s loop, no audio, 1.9 MB. |
| `assets/poster.jpg` | Still frame shown before the video loads and for reduced-motion users. |

## Countdown target

`2026-10-06 12:00` Helsinki time (`+03:00`), from the Meet 1 notes (2026-09-24): "Countdown
nollassa kun ilmo alkaa, eli 6.10 klo 12". Change `OPENS` in `index.html` if the date moves.
When it hits zero the page shows "Ilmo on auki." - add the registration link there once it
exists.

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

The graded video is baked in with ffmpeg, so every browser shows the same result:

```bash
ffmpeg -i source.mp4 -an -vf "fps=24,eq=brightness=-0.03:contrast=0.82:saturation=0.6,\
curves=r='0/0.12 0.5/0.50 1/0.86':g='0/0.09 0.5/0.44 1/0.80':b='0/0.07 0.5/0.38 1/0.70',\
rgbashift=rh=2:bh=-2,gblur=sigma=0.7,noise=alls=14:allf=t+u,vignette=angle=PI/5,format=yuv420p" \
  -c:v libx264 -preset slow -crf 27 -movflags +faststart assets/hero.mp4
```

What each step does: 24 fps for film cadence, darker and flatter contrast, desaturated, lifted
warm blacks and dulled highlights (the faded tape look), a 2 px red/blue colour fringe, slight
softness, moving grain and a vignette. On top of that, the page adds scanlines, a flicker, film
grain and a small gate weave in CSS, plus a navy wash so the text stays readable.

To make the video darker or lighter, change `brightness` (e.g. `-0.08` for darker) and re-run.
