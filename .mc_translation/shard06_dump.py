#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "shard06_aggregated.json"), encoding="utf-8") as f:
    d = json.load(f)
lines = []
for i, s in enumerate(d["strings"]):
    lines.append(f'[{i}] (x{s["count"]},{s["nfiles"]}f) {s["original"]!r}')
with open(os.path.join(HERE, "shard06_originals.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(len(lines))
