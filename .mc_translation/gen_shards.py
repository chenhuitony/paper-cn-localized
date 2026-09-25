#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate balanced shard file lists for minecraft source translation."""
import os, json

ROOT = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
OUT = r"E:\编程\项目\Paper-main\.mc_translation"

def get_files(*prefixes):
    """Get all .java files under the given prefixes (relative to ROOT)."""
    result = []
    for prefix in prefixes:
        full = os.path.join(ROOT, prefix)
        if not os.path.isdir(full):
            continue
        for dirpath, dirnames, filenames in os.walk(full):
            for fn in filenames:
                if fn.endswith('.java'):
                    rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace('\\', '/')
                    result.append(rel)
    return sorted(result)

# Define shards by directory prefixes
shards = {
    "shard_01_world_block_levelgen": [
        "net/minecraft/world/level/block",
        "net/minecraft/world/level/levelgen",
    ],
    "shard_02_world_entity_misc": [
        "net/minecraft/world/entity",
        "net/minecraft/world/inventory",
        "net/minecraft/world/attribute",
        "net/minecraft/world/phys",
        "net/minecraft/world/effect",
        "net/minecraft/world/scores",
        "net/minecraft/world/ticks",
        "net/minecraft/world/damagesource",
        "net/minecraft/world/clock",
        "net/minecraft/world/waypoints",
        "net/minecraft/world/flag",
        "net/minecraft/world/food",
        "net/minecraft/world/timeline",
    ],
    "shard_03_world_item_server_adv": [
        "net/minecraft/world/item",
        "net/minecraft/server",
        "net/minecraft/advancements",
    ],
    "shard_04_util_data": [
        "net/minecraft/util",
        "net/minecraft/data",
    ],
    "shard_05_network_ca_commands": [
        "net/minecraft/network",
        "net/minecraft/commands",
        "ca",
    ],
    "shard_06_level_rest_core_etc": [
        "net/minecraft/world/level/storage",
        "net/minecraft/world/level/chunk",
        "net/minecraft/world/level/biome",
        "net/minecraft/world/level/entity",
        "net/minecraft/world/level/lighting",
        "net/minecraft/world/level/pathfinder",
        "net/minecraft/world/level/gameevent",
        "net/minecraft/world/level/saveddata",
        "net/minecraft/world/level/material",
        "net/minecraft/world/level/redstone",
        "net/minecraft/world/level/dimension",
        "net/minecraft/world/level/gamerules",
        "net/minecraft/world/level/timers",
        "net/minecraft/world/level/validation",
        "net/minecraft/world/level/portal",
        "net/minecraft/world/level/border",
        "net/minecraft/core",
        "net/minecraft/gametest",
        "net/minecraft/nbt",
        "net/minecraft/tags",
        "net/minecraft/gizmos",
        "net/minecraft/resources",
        "net/minecraft/stats",
        "net/minecraft/sounds",
        "net/minecraft/references",
        "net/minecraft/recipebook",
        "net/minecraft/locale",
        "alternate",
        "com",
        "io",
        "org",
    ],
}

total = 0
for name, prefixes in shards.items():
    files = get_files(*prefixes)
    total += len(files)
    outfile = os.path.join(OUT, f"{name}.txt")
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write('\n'.join(files))
    print(f"{name}: {len(files)} files -> {outfile}")

print(f"\nTotal: {total} files")
