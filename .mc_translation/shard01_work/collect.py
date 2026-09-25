#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect candidate translatable strings across all shard files. Read-only."""
import sys, os, json

sys.path.insert(0, r"E:\编程\项目\Paper-main\.mc_translation")
import file_translator as ft

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
LIST = r"E:\编程\项目\Paper-main\.mc_translation\shard_01_world_block_levelgen.txt"
OUT = r"E:\编程\项目\Paper-main\.mc_translation\shard01_work\candidates.json"

with open(LIST, 'r', encoding='utf-8') as f:
    rels = [ln.strip() for ln in f if ln.strip()]

summary = {}
total_candidates = 0
files_with = 0
missing = []

for rel in rels:
    fp = os.path.join(BASE, rel.replace('/', os.sep))
    if not os.path.isfile(fp):
        missing.append(rel)
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    strings = ft.find_strings_with_positions(content)
    cands = []
    for idx, (start, end, str_content, is_tb) in enumerate(strings):
        if not ft.is_likely_translatable(str_content):
            continue
        line = content[:start].count('\n') + 1
        ctx = ft.get_context_line(content, start)[:240]
        cands.append({
            "line": line,
            "is_tb": is_tb,
            "original": str_content,
            "context": ctx,
        })
    if cands:
        files_with += 1
        total_candidates += len(cands)
        summary[rel] = cands

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=1)

print(f"total_files_listed={len(rels)}")
print(f"missing={len(missing)}")
print(f"files_with_candidates={files_with}")
print(f"total_candidates={total_candidates}")
if missing:
    for m in missing[:20]:
        print("MISSING:", m)
