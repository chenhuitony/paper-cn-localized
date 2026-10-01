#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Summarize extracted strings: list files with strings, and dump all strings compactly."""
import json, os

IN = r"E:\编程\项目\Paper-main\.mc_translation\shard03_extracted.json"

with open(IN, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Print summary
print("=== FILES WITH STRINGS ===")
for rel, info in sorted(data.items()):
    strs = info.get("strings", [])
    if strs:
        print(f"\n### {rel} ({len(strs)} strings)")
        for s in strs:
            orig = s["original"].replace("\n", "\\n").replace("\t", "\\t")
            ctx = s["context"].replace("\n", " ")[:120]
            print(f"  L{s['line']}: [{orig}]")
            print(f"    ctx: {ctx}")
