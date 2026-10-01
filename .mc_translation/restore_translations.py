# -*- coding: utf-8 -*-
"""
restore_translations.py — 从 .mc_translation/ 的 apply 脚本中提取文件级翻译映射，
对 paper-server/src/minecraft/java 重新应用（按英文原文匹配，幂等，UTF-8 写回，带语法校验）。
本脚本不含任何 git 操作、不删除任何文件。
"""
import os, io, sys, re, ast, json

T_DIR = r"E:\编程\项目\Paper-main\.mc_translation"
BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
sys.path.insert(0, T_DIR)
import file_translator as ft

def extract_T_dict(src):
    """Locate 'T = {' ... matching '}' (string/comment-aware brace matching) and eval it."""
    m = re.search(r'^\s*T\s*=\s*\{', src, re.M)
    if not m:
        return None
    start = m.start()
    i = src.index('{', start)
    n = len(src)
    depth = 0
    in_s = in_c = in_lc = in_bc = False
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ''
        if in_lc:
            if c == '\n':
                in_lc = False
            i += 1
            continue
        if in_bc:
            if c == '*' and nxt == '/':
                in_bc = False
                i += 2
                continue
            i += 1
            continue
        if in_s:
            if c == '\\':
                i += 2
                continue
            if c == '"':
                in_s = False
            i += 1
            continue
        if in_c:
            if c == '\\':
                i += 2
                continue
            if c == "'":
                in_c = False
            i += 1
            continue
        if c == '"':
            in_s = True
            i += 1
            continue
        if c == "'":
            in_c = True
            i += 1
            continue
        if c == '/' and nxt == '/':
            in_lc = True
            i += 2
            continue
        if c == '/' and nxt == '*':
            in_bc = True
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1
    else:
        return None
    block = src[start:i + 1]
    expr = block[block.index('=') + 1:].strip()
    try:
        return ast.literal_eval(expr)
    except Exception:
        ns = {}
        try:
            exec(compile(block, '<T>', 'exec'), ns)
            return ns.get('T')
        except Exception as e2:
            print('  exec fallback failed: %s' % e2, file=sys.stderr)
            return None

def collect_mappings():
    merged = {}  # relpath -> {original: translated}
    scripts = ['apply_shard02.py', 'apply_shard04.py', 'batch_apply_03.py', 'shard05_apply.py',
               os.path.join('shard01_work', 'apply_translations.py')]
    for rel in scripts:
        p = os.path.join(T_DIR, rel)
        if not os.path.exists(p):
            print('missing script: %s' % p)
            continue
        with io.open(p, encoding='utf-8') as f:
            src = f.read()
        T = extract_T_dict(src)
        if T is None:
            print('no T in %s' % rel)
            continue
        n_keys = 0
        for fp, mp in T.items():
            if not isinstance(mp, dict):
                continue
            d = merged.setdefault(fp, {})
            for k, v in mp.items():
                if k not in d:
                    d[k] = v
                    n_keys += 1
        print('extracted %s: %d files, %d pairs (merged total now %d pairs)' % (
            rel, len(T), n_keys, sum(len(x) for x in merged.values())))
    return merged

def apply_to_file(relpath, mapping):
    fp = os.path.join(BASE, relpath.replace('/', os.sep))
    if not os.path.isfile(fp):
        return 'missing', 0
    with io.open(fp, encoding='utf-8') as f:
        content = f.read()
    strings = ft.find_strings_with_positions(content)
    replacements = []
    for start, end, str_content, is_tb in strings:
        if str_content in mapping:
            trans = mapping[str_content]
            if trans is not None and trans != str_content:
                replacements.append((start, end, str_content, trans, is_tb))
    if not replacements:
        return 'no-match', 0
    replacements.sort(key=lambda x: x[0], reverse=True)
    modified = content
    applied = 0
    skipped = 0
    for start, end, orig, trans, is_tb in replacements:
        actual = modified[start + 1:end - 1] if not is_tb else modified[start + 3:end - 3]
        if actual != orig:
            skipped += 1
            continue
        if is_tb:
            modified = modified[:start + 3] + trans + modified[end - 3:]
        else:
            modified = modified[:start + 1] + trans + modified[end - 1:]
        applied += 1
    issues = ft.verify_file(modified)
    if issues:
        return 'verify-fail:' + ';'.join(issues), applied
    with io.open(fp, 'w', encoding='utf-8') as f:
        f.write(modified)
    return 'ok', applied

def main():
    merged = collect_mappings()
    print('TOTAL: %d files in mapping, %d pairs' % (len(merged), sum(len(x) for x in merged.values())))
    n_files_ok = n_apply = n_missing = n_verify_fail = 0
    detail = []
    for relpath, mapping in merged.items():
        status, applied = apply_to_file(relpath, mapping)
        if status == 'ok':
            n_files_ok += 1
            n_apply += applied
        elif status == 'missing':
            n_missing += 1
        elif status.startswith('verify-fail'):
            n_verify_fail += 1
            detail.append(relpath + ' :: ' + status)
        # no-match: silently ignore
    print('files_ok=%d, total_replacements=%d, missing=%d, verify_fail=%d' % (
        n_files_ok, n_apply, n_missing, n_verify_fail))
    for d in detail[:30]:
        print('  VERIFY-FAIL: ' + d)
    # persist detail for later reading
    with io.open(os.path.join(T_DIR, 'restore_report.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(['files_ok=%d total_replacements=%d missing=%d verify_fail=%d' % (
            n_files_ok, n_apply, n_missing, n_verify_fail)] + detail))

if __name__ == '__main__':
    main()
