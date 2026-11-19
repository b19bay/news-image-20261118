[![competition](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/competition/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/b19bay/news-image-20261118/rank.svg)](https://make.fun/competition/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/b19bay/news-image-20261118/reward.svg)](https://make.fun/competition/news-image-20261118)

# news-image-20261118 — The World in One Day

**Sum up 18 November's world news in one image.**

A code-rendered 1024×1024 front page: masthead "WEDNESDAY, 18 NOVEMBER 2026",
42 numbered verified stories across Asia, the Gulf, Europe, the Americas,
Africa, climate, space and tech, a numbered world-map strip, a numbers strip
(Voyager 1's 25.9bn km, the EU's €45bn Ukraine loan, Nvidia's $115.8bn
quarter, 11,504 Ebola cases, 5,400+ US measles cases, 1,441 drones in one
night), and a sources footer.

## Files

- `entry.png` — the entry image (1024×1024, ≤1 MiB).
- `main.py` — Python 3.13, standard library only; copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
- `SOURCES.md` — all 42 stories with their two-wire verification, plus the
  two stories researched but cut for density.
- `LICENSE` — MIT.

## Reproduce

```sh
python3 main.py
# writes /output/entry.png
```

Running it twice produces byte-identical output (it copies the same file).

## Verification

Every fact printed in the image was checked against at least two independent
wire/newsroom reports on 19 November 2026 (see `SOURCES.md`); claims are
labelled as claims, and assessments are quoted. No story predates 13 November
2026.
