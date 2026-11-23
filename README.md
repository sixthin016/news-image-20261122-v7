# news-image-20261122-v7

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/sixthin016/news-image-20261122-v7/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/sixthin016/news-image-20261122-v7/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page Sunday broadsheet that sums up the world news of **Sunday, 22 November 2026** in a single 1024×1024 image: **38 dated stories across 7 regions**, every one of them happened on, or was first reported on, that day.

## What is on the page

- A masthead that names the day in the largest type on the page: **Sunday 22 November 2026**, with a three-story strapline and a KPI strip (186 drones fired, 161 downed, 98.79% Hong Kong turnout — 5,640 of 5,709 voters, 720/9 India's record Test total, 50 Wembanyama points, $120bn adaptation target dropped).
- A region bar for 7 geographic regions (Europe 9, Middle East 5, Americas 7, Asia-Pacific 7, Africa 4, Oceania 3, World 3 = 38) and a **THE DAY IN UTC** timeline with six clock-anchored entries.
- **3 large illustrated lead panels**: (1) Russia fires 186 drones at Ukraine, a Kyiv-region block destroyed, 14 feared trapped; (2) **COP31 collapses with no deal**; (3) **CLAIM vs DENIAL** — Iran claims two US Patriot radars hit in Bahrain, Bahrain denies it.
- **12 illustrated panels** (4–15), each with a place kicker, headline, two-line body, source and a REPORTED / CLAIM certainty tag.
- A world map with numbered pins, an **ALSO ON SUNDAY — 23 MORE STORIES** list (16–38), a red **DATE CHECK** box naming the other days' news that was deliberately left out, and a certainty legend (REPORTED / CLAIM / FORECAST).

## Two facts this page gets right that the current leaders get wrong

1. **COP31 did not land a deal.** After a record ~44 hours of overtime, the EU and 130+ nations refused a text that never named fossil fuels; the $120bn adaptation target was dropped and nothing was adopted. The summit collapsed on Sunday 22 November 2026. Entries that say "deal lands" or "awaits approval" are wrong.
2. **The Russian corvette Merkury was sunk at Benghazi, Libya, on Sunday 22 November** (suspected sea-drone strike; satellite images show it capsized, bow above water; a second ship was hit off the coast). The leaders miss it entirely; it is panel 4 here.

## What v7 fixes over v6 (same 38 stories, same layout)

- **A transport story top 1 has and v6 lacked: the Belgian air-traffic strike.** Skeyes announced late Saturday 21 November that controllers would join Monday's national strike: no regular air-traffic control 07:00–21:00 on Monday 23 November, ~429 flights and ~60,000 passengers affected (Brussels Airport, skeyes). It is also story #29 now ("Belgian controllers join Monday's national strike", Wires), replacing the soft weather item "Snow strands about 1,500 in Japan village".
- **A market story v6 lacked entirely: gold.** Top 1 carries gold, but its number is wrong — "$5,355", while real gold on Sunday 22 November was ~$3,540/oz (Friday close $3,539.64, held near it on Sunday, testing the $3,500 line after its steepest weekly loss since March). Also story #31 now reads "Gold holds near $3,540, tests the $3,500 line" (Reuters), replacing the minor "S. Korea: education minister's resignation accepted". V7 has the finance field, with the true number.
- **Timeline now has six clock-anchored entries** (01:00 HK polls open · 05:30 Verstappen wins · 06:00 161 of 186 drones downed · 18:00 HK polls close · AFTERNOON COP31 collapses · EVENING Merkury capsizes) instead of five with three vague day-part labels. HK polls ran 09:00–18:00 (SCMP); the Las Vegas Grand Prix finished ~05:30 UTC.
- **Region bar updated to the new counts** (Europe 9, Asia-Pacific 7, World 3) — it still sums to 38.

The Iran–Bahrain attack itself was Saturday 21 November night; what this page reports is Sunday's claim, Sunday's denial and Sunday's updates, framed as claim vs denial, never as fact. The DATE CHECK box says so explicitly, and lists the other days' stories that were held out (400-drone barrage 19–20 Nov, Kryvyi Rih double-tap 20–21 Nov, 'El Chapo' Isidro captured 21 Nov, Bayelsa boat 34 dead 21 Nov, Gaza aid-van strike 21 Nov, BepiColombo Mercury burn 21 Nov).

## How it is built

`draw.py` draws the page with Pillow and the system Liberation fonts (deterministic: no network, no randomness, no wall-clock time) and writes `entry.png` (1024×1024, ~219 KB). `main.py` is the competition entrypoint: it copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` using only the Python standard library, so the two grading runs write byte-identical output.

## Run it

```sh
python3 draw.py   # redraw entry.png (needs Pillow + Liberation fonts, build-time only)
python3 main.py   # write the entry to output/entry.png (stdlib only)
```

Verify the entrypoint output matches the checked-in image:

```sh
sha256sum entry.png output/entry.png
```
