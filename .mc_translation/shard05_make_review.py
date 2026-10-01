#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produce a compact review listing of extracted strings."""
import json

with open(r"E:\编程\项目\Paper-main\.mc_translation\shard05_extracted.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

lines = []
for rel, items in data.items():
    if not isinstance(items, list) or not items:
        continue
    lines.append(f"\n===== {rel} ({len(items)} strings) =====")
    for it in items:
        orig = it['original'].replace('\n', '\\n')
        ctx = it['context'].replace('\n', ' ')
        lines.append(f"  L{it['line']}: {orig!r}")
        lines.append(f"      ctx: {ctx[:180]}")

out = '\n'.join(lines)
with open(r"E:\编程\项目\Paper-main\.mc_translation\shard05_review.txt", 'w', encoding='utf-8') as f:
    f.write(out)
print(f"Wrote {len(lines)} lines")
