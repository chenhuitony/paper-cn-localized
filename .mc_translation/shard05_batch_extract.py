#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch extract all translatable strings from shard files, group by file."""
import sys, os, json, subprocess

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
LIST = r"E:\编程\项目\Paper-main\.mc_translation\shard_05_network_ca_commands.txt"
TRANSLATOR = r"E:\编程\项目\Paper-main\.mc_translation\file_translator.py"
OUT = r"E:\编程\项目\Paper-main\.mc_translation\shard05_extracted.json"

files = []
with open(LIST, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            files.append(line)

all_results = {}
for rel in files:
    abs_path = os.path.join(BASE, rel.replace('/', os.sep))
    if not os.path.isfile(abs_path):
        all_results[rel] = {"error": "NOT FOUND"}
        continue
    try:
        proc = subprocess.run(
            [sys.executable, TRANSLATOR, "extract", abs_path],
            capture_output=True, text=True, encoding='utf-8', timeout=60
        )
        if proc.returncode != 0:
            all_results[rel] = {"error": proc.stderr.strip()[:500]}
            continue
        data = json.loads(proc.stdout)
        if data:
            all_results[rel] = data
    except Exception as e:
        all_results[rel] = {"error": str(e)[:500]}

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

# Summary
total_strings = 0
files_with_strings = 0
for rel, data in all_results.items():
    if isinstance(data, list) and data:
        files_with_strings += 1
        total_strings += len(data)

print(f"Total files listed: {len(files)}")
print(f"Files with translatable strings: {files_with_strings}")
print(f"Total translatable strings: {total_strings}")
print(f"Output: {OUT}")
