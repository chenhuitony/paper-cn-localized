#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect candidate translatable strings across all files in shard 02."""
import sys, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import file_translator as ft

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
LIST = os.path.join(HERE, "shard_02_world_entity_misc.txt")
OUT = os.path.join(HERE, "shard02_candidates.json")

def main():
    with open(LIST, 'r', encoding='utf-8') as f:
        rels = [ln.strip() for ln in f if ln.strip()]

    report = {}
    no_candidates = []
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
            ctx = ft.get_context_line(content, start)
            cands.append({
                "idx": idx,
                "line": line,
                "original": str_content,
                "context": ctx[:200],
                "is_tb": is_tb,
            })
        if cands:
            report[rel] = cands
        else:
            no_candidates.append(rel)

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    print(f"total files listed: {len(rels)}")
    print(f"missing files: {len(missing)}")
    print(f"files with candidates: {len(report)}")
    print(f"files with no candidates: {len(no_candidates)}")
    total_cands = sum(len(v) for v in report.values())
    print(f"total candidate strings: {total_cands}")
    if missing:
        print("MISSING EXAMPLES:")
        for m in missing[:20]:
            print("  ", m)

if __name__ == '__main__':
    main()
