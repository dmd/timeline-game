#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///

import json
import subprocess

with open("timeline_events.json") as f:
    events = json.load(f)


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


lines = []
lines.append("""
#set page(margin: 0.5in)
#set text(size: 11pt)

= Answer Key

#grid(
  columns: 1,
  gutter: 4pt,
  ..{(
""")

for i, ev in enumerate(events):
    text = ev["event"].replace('"', '\\"')
    year = format_year(ev["year"])
    lines.append(f"""    grid(
      columns: (1in, 1fr),
      gutter: 8pt,
      align(right, strong("{year}")),
      text("{text}"),
    ),""")

lines.append("""  )}
)
""")

typst_src = "\n".join(lines)

with open("answer_key.typ", "w") as f:
    f.write(typst_src)

subprocess.run(["typst", "compile", "answer_key.typ", "answer_key.pdf"], check=True)
print("Generated answer_key.pdf")
