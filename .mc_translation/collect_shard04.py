#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch-collect candidate translatable strings across shard files."""
import sys, os, json, importlib.util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ft", os.path.join(SCRIPT_DIR, "file_translator.py"))
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
LIST = os.path.join(SCRIPT_DIR, "shard_04_util_data.txt")

def main():
    files = []
    with open(LIST, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                # format: "1\tnet/minecraft/..."  (numbered)
                if "\t" in line:
                    line = line.split("\t", 1)[1]
                files.append(line)

    out = {}
    empty = []
    missing = []
    for rel in files:
        path = os.path.join(BASE, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            missing.append(rel)
            continue
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        strings = ft.find_strings_with_positions(content)
        cands = []
        for idx, (start, end, sc, is_tb) in enumerate(strings):
            if not ft.is_likely_translatable(sc):
                continue
            line = content[:start].count("\n") + 1
            ctx = ft.get_context_line(content, start)
            cands.append({"line": line, "tb": is_tb, "orig": sc, "ctx": ctx[:160]})
        if cands:
            out[rel] = cands
        else:
            empty.append(rel)

    result = {"with_strings": out, "empty": empty, "missing": missing}
    with open(os.path.join(SCRIPT_DIR, "shard04_collected.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)

    total_cands = sum(len(v) for v in out.values())
    print(f"total files listed: {len(files)}")
    print(f"files with candidate strings: {len(out)}")
    print(f"files empty/skipped: {len(empty)}")
    print(f"files missing on disk: {len(missing)}")
    print(f"total candidate strings: {total_cands}")

if __name__ == "__main__":
    main()
