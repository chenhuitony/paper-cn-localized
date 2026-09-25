import os, glob

ROOT = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
OUT = r"E:\编程\项目\Paper-main\.mc_translation"

# Get all files
all_files = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if fn.endswith('.java'):
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace('\\', '/')
            all_files.add(rel)

# Get files in all shards
shard_files = set()
for shard_file in glob.glob(os.path.join(OUT, "shard_*.txt")):
    with open(shard_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                shard_files.add(line.strip())

missing = sorted(all_files - shard_files)
print(f"Missing files: {len(missing)}")
for m in missing[:30]:
    print(f"  {m}")
if len(missing) > 30:
    print(f"  ... and {len(missing)-30} more")

# Append to shard_06
shard06 = os.path.join(OUT, "shard_06_level_rest_core_etc.txt")
with open(shard06, 'a', encoding='utf-8') as f:
    for m in missing:
        f.write('\n' + m)

# Re-count
with open(shard06, 'r', encoding='utf-8') as f:
    count = sum(1 for line in f if line.strip())
print(f"\nshard_06 now has {count} files")

# Verify total
total = 0
for shard_file in sorted(glob.glob(os.path.join(OUT, "shard_*.txt"))):
    with open(shard_file, 'r', encoding='utf-8') as f:
        c = sum(1 for line in f if line.strip())
    total += c
    print(f"  {os.path.basename(shard_file)}: {c}")
print(f"Total: {total}")
