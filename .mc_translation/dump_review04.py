#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os
D = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(D, "shard04_collected.json"), encoding="utf-8") as f:
    data = json.load(f)
ws = data["with_strings"]
lines = []
for rel, items in ws.items():
    lines.append(f"### FILE: {rel}  ({len(items)})")
    for it in items:
        lines.append(f"  L{it['line']}{'[TB]' if it['tb'] else ''}: {it['orig']!r}")
        lines.append(f"      ctx: {it['ctx']}")
    lines.append("")
with open(os.path.join(D, "shard04_review.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("files:", len(ws), "lines written:", len(lines))
