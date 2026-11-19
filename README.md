[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/b19bay/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/b19bay/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# news-image-20261118 — Wednesday 18 November 2026

"Sum up 18 November's world news in one image" — a code-rendered front page
for Wednesday, 18 November 2026: **38 stories, all of which happened or
were first reported that day**. Eleven hero stories carry flat code-drawn
illustrations (Xi greets Trump in Shenzhen, the Gulf strikes, Voyager 1 one
light-day out, 141 drones over Ukraine, the Fed minutes, Cyclone Akvan,
Amnesty's El Obeid report, the EU's €45bn Ukraine loan, UK inflation at
3.6%, Israeli tanks in central Gaza, Jeffries' 251–11 Speaker nod); 27 more
stories run as a numbered list below. A dotted world map pins the heroes, a
day-in-numbers strip runs the big figures, and a DATE CHECK box names the
big stories deliberately left out because they were first reported on
17 November (Peltola's Senate win, Nvidia's quarter, OpenAI's GPT-6.2).

## Entry

- `entry.png` — the finished image, 1024x1024, rendered in code (Python/PIL,
  DejaVu/Liberation fonts). No AI-generated imagery, no garbled text.
- `main.py` — the program: Python 3 stdlib only, copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`). It checks the
  image against the competition gate (1024x1024, 1 MiB) before writing and
  verifies the copy's sha256 afterwards.
- `render.py` — the script that drew the image (kept for transparency).
- `SOURCES.md` — the verification record for all 38 stories.

## How it was built

1. Researched 18 November 2026 from wire reports (AP, Reuters, AFP, BBC,
   NYT, WSJ, ONS, the Fed, IMD, NASA, WHO, Amnesty, UN News); every printed
   fact was checked against at least two independent reports, and every story
   was dated — anything first reported on 16–17 November was cut and named
   in the DATE CHECK box instead of printed as the day's news.
2. Rendered three front-page variants (map on top; map at the bottom with a
   3-column list; map at the bottom with a 2-column list) and scored each
   against the five published judging criteria.
3. Picked the winner at ~300 px, the size the judge reads: map at the
   bottom, 3-column list — masthead, date, hero headlines, map and numbers
   strip all stay legible at small size. The map-on-top variant wasted the
   top of the page and its bottom band ran past the footer; the 2-column
   list ran off the page.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
