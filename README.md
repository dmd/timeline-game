# Timeline Game

A history trivia game where you place events on a timeline spanning from the formation of the solar system (4.6 billion years ago) to the present day.

## Play Online

Open `index.html` in a browser. You'll get 10 random events — pick the right era, click where you think each event belongs on the timeline, and try to minimize your score (lower is better).

The timeline is divided into six tiers that zoom in progressively:

| Tier | Range |
|------|-------|
| Deep Time | 4.6 Bya – 500 Mya |
| Mesozoic | 500 Mya – 66 Mya |
| Cenozoic | 66 Mya – 10,000 BC |
| Ancient | 10,000 BC – 500 BC |
| Medieval+ | 500 BC – 1800 |
| Modern | 1800 – Present |

## Print & Play

There's also a printable card game version. The Python scripts generate PDFs using [Typst](https://typst.app/):

- `generate_cards.py` — event cards to cut out
- `generate_timelines.py` — printed timeline boards
- `generate_answer_key.py` — answer key with all events and dates

Run any script directly (requires [uv](https://github.com/astral-sh/uv) and Typst):

```
./generate_cards.py
```

## Data

All events live in `timeline_events.json` — each entry has an event name, year, and category.
