# -*- coding: utf-8 -*-
"""
restore_translations2.py — 从 .mc_translation/ 的 apply 脚本中提取翻译映射（文件级 + 全局级），
对 paper-server/src/minecraft/java 全部 .java 重新应用（按英文原文匹配，幂等，UTF-8 写回，带语法校验）。
本脚本不含任何 git 操作、不删除任何文件。
"""
import os, io, sys, re, ast

T_DIR = r"E:\编程\项目\Paper-main\.mc_translation"
BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
sys.path.insert(0, T_DIR)
import file_translator as ft

def extract_T_dict(src):
    m = re.search(r'^\s*T\s*=\s*\{', src, re.M)
    if not m:
        return None
    i = src.index('{', m.start())
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
                block = src[m.start():i + 1]
                expr = block[block.index('=') + 1:].strip()
                try:
                    return ast.literal_eval(expr)
                except Exception:
                    ns = {}
                    exec(compile(block, '<T>', 'exec'), ns)
                    return ns.get('T')
        i += 1
    return None

def collect():
    file_level = {}
    global_level = {}
    scripts = ['apply_shard02.py', 'apply_shard04.py', 'batch_apply_03.py', 'shard05_apply.py',
               os.path.join('shard01_work', 'apply_translations.py')]
    for rel in scripts:
        p = os.path.join(T_DIR, rel)
        if not os.path.exists(p):
            continue
        with io.open(p, encoding='utf-8') as f:
            src = f.read()
        T = extract_T_dict(src)
        if not T:
            print('no T in %s' % rel)
            continue
        sample = next(iter(T.values()))
        if isinstance(sample, dict):
            n = 0
            for fp, mp in T.items():
                d = file_level.setdefault(fp, {})
                for k, v in mp.items():
                    d.setdefault(k, v)
                    n += 1
            print('file-level %s: %d files, %d pairs' % (rel, len(T), n))
        else:
            n = 0
            for k, v in T.items():
                global_level.setdefault(k, v)
                n += 1
            print('global %s: %d pairs' % (rel, n))
    return file_level, global_level

def apply_file(relpath, mapping):
    fp = os.path.join(BASE, relpath.replace('/', os.sep))
    if not os.path.isfile(fp):
        return 'missing', 0
    with io.open(fp, encoding='utf-8') as f:
        content = f.read()
    if not mapping:
        return 'no-map', 0
    strings = ft.find_strings_with_positions(content)
    reps = []
    for start, end, sc, is_tb in strings:
        if sc in mapping:
            tr = mapping[sc]
            if tr is not None and tr != sc:
                reps.append((start, end, sc, tr, is_tb))
    if not reps:
        return 'no-match', 0
    reps.sort(key=lambda x: x[0], reverse=True)
    modified = content
    applied = 0
    for start, end, orig, trans, is_tb in reps:
        actual = modified[start + 1:end - 1] if not is_tb else modified[start + 3:end - 3]
        if actual != orig:
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
    file_level, global_level = collect()
    print('TOTAL file-level: %d files, %d pairs; global: %d pairs' % (
        len(file_level), sum(len(x) for x in file_level.values()), len(global_level)))
    n_ok = n_apply = n_missing = n_vfail = 0
    fails = []
    # walk all java files
    for dp, _, fns in os.walk(BASE):
        for fn in fns:
            if not fn.endswith('.java'):
                continue
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, BASE).replace(os.sep, '/')
            mapping = dict(global_level)
            if rel in file_level:
                mapping.update(file_level[rel])
            status, applied = apply_file(rel, mapping)
            if status == 'ok':
                n_ok += 1
                n_apply += applied
            elif status == 'missing':
                n_missing += 1
            elif status.startswith('verify-fail'):
                n_vfail += 1
                fails.append(rel + ' :: ' + status)
    print('files_ok=%d replacements=%d missing=%d verify_fail=%d' % (n_ok, n_apply, n_missing, n_vfail))
    for f in fails[:40]:
        print('  VERIFY-FAIL: ' + f)
    with io.open(os.path.join(T_DIR, 'restore_report2.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(['files_ok=%d replacements=%d missing=%d verify_fail=%d' % (
            n_ok, n_apply, n_missing, n_vfail)] + fails))

if __name__ == '__main__':
    main()
