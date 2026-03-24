#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///

import json
import subprocess

with open("timeline_events.json") as f:
    events = json.load(f)

# Build typst document with a grid of cards
lines = []
lines.append("""
#set page(margin: 0.25in)
#set text(size: 6.5pt)

#grid(
  columns: 5,
  gutter: 0pt,
  ..{(
""")

for ev in events:
    text = ev["event"].replace('"', '\\"')
    lines.append(f"""    box(
      width: 100%,
      height: 0.4in,
      stroke: 0.5pt + luma(180),
      inset: 3pt,
      align(horizon, text("{text}"))
    ),""")

lines.append("""  )}
)
""")

typst_src = "\n".join(lines)

with open("cards.typ", "w") as f:
    f.write(typst_src)

subprocess.run(["typst", "compile", "cards.typ", "cards.pdf"], check=True)
print("Generated cards.pdf")
