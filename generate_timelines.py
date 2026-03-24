#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///

import json
import subprocess

with open("timeline_events.json") as f:
    events = json.load(f)

# Define the 6 timeline tiers
tiers = [
    {"start": -4600000000, "end": -500000000, "label": "4.6 Bya – 500 Mya"},
    {"start": -500000000, "end": -66000000, "label": "500 Mya – 66 Mya"},
    {"start": -66000000, "end": -10000, "label": "66 Mya – 10,000 BC"},
    {"start": -10000, "end": -500, "label": "10,000 BC – 500 BC"},
    {"start": -500, "end": 1800, "label": "500 BC – 1800"},
    {"start": 1800, "end": 2030, "label": "1800 – Present"},
]


def format_year(y):
    if y <= -1000000000:
        return f"{y / -1000000000:.1f} Bya"
    if y <= -1000000:
        return f"{y / -1000000:.0f} Mya"
    if y <= -10000:
        return f"{y / -1000:.0f}K ya"
    if y < 0:
        return f"{-y} BC"
    return str(y)


def make_tick_years(start, end):
    """Generate sensible tick marks for a given range."""
    span = end - start
    # Pick a step that gives roughly 10-20 ticks
    candidates = [
        1000000000, 500000000, 100000000, 50000000, 10000000, 5000000,
        1000000, 500000, 100000, 50000, 10000, 5000, 2000, 1000, 500,
        200, 100, 50, 20, 10,
    ]
    step = candidates[0]
    for c in candidates:
        if span / c >= 8:
            step = c
            break
    ticks = []
    # Start from a round number
    first = ((start // step) + 1) * step
    y = first
    while y <= end:
        ticks.append(y)
        y += step
    return ticks


lines = []
lines.append("""
#set page(margin: 0.5in, flipped: true)
#set text(size: 9pt)
""")

for tier in tiers:
    start = tier["start"]
    end = tier["end"]
    span = end - start
    label = tier["label"]

    ticks = make_tick_years(start, end)

    # Split each tier into 3 strips on one page
    # Each strip covers 1/3 of the time range, stacked vertically
    strip_height = 2.1  # inches per strip
    strips = 3

    lines.append(f"""
#page[
  #align(center, text(14pt, strong("{label}")))
  #v(4pt)
  #layout(size => {{
    let w = size.width
    block(width: w, height: {strip_height * strips}in)[
""")

    for s in range(strips):
        strip_start = start + s * span / strips
        strip_end = start + (s + 1) * span / strips
        strip_span = strip_end - strip_start
        y_offset = s * strip_height * 72  # convert inches to pt
        timeline_y = y_offset + 40

        # Timeline line for this strip
        lines.append(f"""      #place(line(start: (0pt, {timeline_y}pt), end: (w, {timeline_y}pt), stroke: 1.5pt))""")

        # Ticks in this strip's range
        for t in ticks:
            if strip_start <= t <= strip_end:
                frac = (t - strip_start) / strip_span
                yr_label = format_year(t).replace('"', '\\"')
                lines.append(f"""      #place(dx: {frac} * w, dy: {timeline_y - 6}pt, line(start: (0pt, 0pt), end: (0pt, 12pt), stroke: 0.75pt))
      #place(dx: {frac} * w - 30pt, dy: {timeline_y + 10}pt, box(width: 60pt, align(center, text(12pt, "{yr_label}"))))""")

        # Strip range label at left
        range_start = format_year(int(strip_start)).replace('"', '\\"')
        range_end = format_year(int(strip_end)).replace('"', '\\"')
        lines.append(f"""      #place(dx: 0pt, dy: {y_offset + 4}pt, text(11pt, luma(120), "{range_start} — {range_end}"))""")

    lines.append("""    ]
  })
]
""")

typst_src = "\n".join(lines)

with open("timelines.typ", "w") as f:
    f.write(typst_src)

subprocess.run(["typst", "compile", "timelines.typ", "timelines.pdf"], check=True)
print("Generated timelines.pdf")
