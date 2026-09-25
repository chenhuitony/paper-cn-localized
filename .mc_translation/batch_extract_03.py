#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch extract translatable strings from all files in the shard list."""
import sys, os, json, subprocess

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
LIST = r"E:\编程\项目\Paper-main\.mc_translation\shard_03_world_item_server_adv.txt"
SCRIPT = r"E:\编程\项目\Paper-main\.mc_translation\file_translator.py"
OUT = r"E:\编程\项目\Paper-main\.mc_translation\shard03_extracted.json"

def main():
    with open(LIST, 'r', encoding='utf-8') as f:
        files = [l.strip() for l in f if l.strip()]
    
    all_results = {}
    skipped_no_file = []
    total_strings = 0
    
    for i, rel in enumerate(files):
        fpath = os.path.join(BASE, rel.replace('/', os.sep))
        if not os.path.isfile(fpath):
            skipped_no_file.append(rel)
            continue
        try:
            proc = subprocess.run(
                [sys.executable, SCRIPT, "extract", fpath],
                capture_output=True, text=True, encoding='utf-8', timeout=30
            )
            if proc.returncode != 0:
                all_results[rel] = {"error": proc.stderr.strip(), "strings": []}
                continue
            data = json.loads(proc.stdout)
            if data:
                all_results[rel] = {"strings": data}
                total_strings += len(data)
        except Exception as e:
            all_results[rel] = {"error": str(e), "strings": []}
        
        if (i+1) % 100 == 0:
            print(f"Processed {i+1}/{len(files)}, strings so far: {total_strings}", flush=True)
    
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    files_with_strings = sum(1 for v in all_results.values() if v.get("strings"))
    print(f"\nDone. Files processed: {len(files)}")
    print(f"Files with translatable strings: {files_with_strings}")
    print(f"Total translatable strings: {total_strings}")
    print(f"Files not found: {len(skipped_no_file)}")
    if skipped_no_file:
        for s in skipped_no_file[:20]:
            print(f"  MISSING: {s}")
    print(f"Output: {OUT}")

if __name__ == '__main__':
    main()
