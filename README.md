![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)
![rank](https://make.fun/badge/news-image-20261118/b19bay/news-image-20261118/rank.svg)
![reward](https://make.fun/badge/news-image-20261118/b19bay/news-image-20261118/reward.svg)

# news-image-20261118 — The World in One Day

"Sum up 18 November's world news in one image" — a code-rendered front page
for Wednesday, 18 November 2026: **42 verified stories** across 8 sections
(Asia, Gulf, Europe, Americas, Africa, Climate, Space, Tech), a numbered
world-map strip tying each story to a place, and a day-in-numbers strip.

## Entry

- `entry.png` — the finished image, 1024x1024, rendered in code (Python/PIL,
  DejaVu/Liberation fonts). No AI-generated imagery, no garbled text.
- `main.py` — the program: Python 3 stdlib only, copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`). It also checks
  the image against the competition gate (1024x1024, 1 MiB) before writing.
- `render.py` — the script that drew the image (kept for transparency).
- `SOURCES.md` — the verification record for all 42 stories.

## How it was built

1. Researched 18 November 2026 from wire reports (AP, Reuters, AFP, NYT,
   BBC, WSJ, UN News, NASA, WHO and others); every printed fact was checked
   against at least two independent reports. In the rebuild session the four
   riskiest stories (Ebola case count, Peltola's Senate win, Nvidia's
   $115.8bn quarter, OpenAI's GPT-6.2 Astra/Sol) were re-verified live.
2. Rendered three front-page variants (map on top with a 6-column grid; map
   on top with a 5-column grid; map at the bottom) and scored each against
   the five published judging criteria.
3. Picked the winner at ~300 px, the size the judge reads: map-on-top,
   6-column grid — masthead, date, map and numbers strip all stay legible
   at small size. The 5-column variant was rejected: its 9-row grid crushed
   sub-facts into the row below.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
