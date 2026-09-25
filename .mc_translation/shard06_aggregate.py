#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggregate translatable candidate strings across all files in the shard list."""
import sys, os, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ft", os.path.join(HERE, "file_translator.py"))
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
LIST = os.path.join(HERE, "shard_06_level_rest_core_etc.txt")

def main():
    with open(LIST, encoding="utf-8") as f:
        rels = [l.strip() for l in f if l.strip()]

    # unique original -> {count, files:[], contexts:[]}
    agg = {}
    files_with_strings = []
    missing = []
    for rel in rels:
        fp = os.path.join(BASE, rel.replace("/", os.sep))
        if not os.path.isfile(fp):
            missing.append(rel)
            continue
        with open(fp, encoding="utf-8") as f:
            content = f.read()
        strings = ft.find_strings_with_positions(content)
        got = []
        for start, end, sc, is_tb in strings:
            if not ft.is_likely_translatable(sc):
                continue
            got.append(sc)
            ctx = ft.get_context_line(content, start)
            e = agg.setdefault(sc, {"count": 0, "files": set(), "contexts": []})
            e["count"] += 1
            e["files"].add(rel)
            if len(e["contexts"]) < 3:
                e["contexts"].append(rel + " :: " + ctx[:160])
        if got:
            files_with_strings.append((rel, len(got)))

    out = []
    for sc, e in agg.items():
        out.append({
            "original": sc,
            "count": e["count"],
            "nfiles": len(e["files"]),
            "contexts": e["contexts"],
        })
    out.sort(key=lambda x: (-x["count"], x["original"]))

    result = {
        "total_files": len(rels),
        "missing": missing,
        "files_with_strings": len(files_with_strings),
        "unique_strings": len(out),
        "strings": out,
    }
    with open(os.path.join(HERE, "shard06_aggregated.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"total={len(rels)} missing={len(missing)} files_with_strings={len(files_with_strings)} unique={len(out)}")

if __name__ == "__main__":
    main()
