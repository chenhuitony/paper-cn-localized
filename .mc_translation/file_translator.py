#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-file Java string translator helper.
Usage:
  # Extract translatable strings from a file
  python file_translator.py extract <file_path>
  
  # Apply translations to a file (reads translations from stdin as JSON: {original: translated})
  python file_translator.py apply <file_path> < translations.json
  
  # Verify a file is well-formed
  python file_translator.py verify <file_path>
"""
import sys, os, re, json

CHINESE_RE = re.compile(r'[\u4e00-\u9fff]')
ENGLISH_RE = re.compile(r'[A-Za-z]{2,}')

def find_strings_with_positions(content):
    """Find all string literals with positions. Handles regular strings and text blocks.
    Returns list of (start, end, content_between_quotes, is_text_block)."""
    results = []
    i = 0
    n = len(content)
    in_string = False
    in_char = False
    in_line_comment = False
    in_block_comment = False
    string_start = -1
    is_text_block = False
    
    while i < n:
        c = content[i]
        
        if in_line_comment:
            if c == '\n':
                in_line_comment = False
            i += 1
            continue
        
        if in_block_comment:
            if c == '*' and i + 1 < n and content[i+1] == '/':
                in_block_comment = False
                i += 2
                continue
            i += 1
            continue
        
        if in_string:
            if c == '\\' and i + 1 < n:
                i += 2
                continue
            if c == '"':
                # Check if this is the end of a text block (""")
                if is_text_block:
                    # Need three consecutive quotes to end
                    if i + 2 < n and content[i+1] == '"' and content[i+2] == '"':
                        str_content = content[string_start+3:i]
                        results.append((string_start, i + 3, str_content, True))
                        in_string = False
                        is_text_block = False
                        i += 3
                        continue
                    # Single or double quote inside text block - just continue
                    i += 1
                    continue
                else:
                    # Regular string end
                    str_content = content[string_start+1:i]
                    results.append((string_start, i + 1, str_content, False))
                    in_string = False
                    i += 1
                    continue
            i += 1
            continue
        
        if in_char:
            if c == '\\' and i + 1 < n:
                i += 2
                continue
            if c == "'":
                in_char = False
            i += 1
            continue
        
        # Not in special state
        if c == '"':
            # Check if text block (""")
            if i + 2 < n and content[i+1] == '"' and content[i+2] == '"':
                in_string = True
                is_text_block = True
                string_start = i
                i += 3
                continue
            else:
                in_string = True
                is_text_block = False
                string_start = i
                i += 1
                continue
        if c == "'":
            in_char = True
            i += 1
            continue
        if c == '/' and i + 1 < n:
            if content[i+1] == '/':
                in_line_comment = True
                i += 2
                continue
            if content[i+1] == '*':
                in_block_comment = True
                i += 2
                continue
        i += 1
    
    return results

def is_likely_translatable(s, context=""):
    """Heuristic to determine if a string is user-facing text that should be translated."""
    stripped = s.strip()
    if not stripped:
        return False
    if not ENGLISH_RE.search(stripped):
        return False
    # Skip contract expressions
    if '->' in stripped:
        cleaned = re.sub(r'[_,\s]', '', stripped).replace('->', '').replace('!null', '').replace('null', '').replace('true', '').replace('false', '').replace('new', '').replace('this', '').replace('param', '')
        cleaned = re.sub(r'\d+', '', cleaned)
        if cleaned == '':
            return False
    # Skip resource keys
    if re.match(r'^[a-z0-9_.-]+:[a-z0-9_./-]+$', stripped):
        return False
    # Skip translation keys (dotted lowercase with no spaces, e.g. "multiplayer.player.joined")
    if re.match(r'^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$', stripped) and ' ' not in stripped:
        return False
    # Skip identifiers
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', stripped):
        return False
    # Skip pure numbers/hex
    if re.match(r'^[0-9a-fA-FxX]+$', stripped):
        return False
    # Skip paths/URLs
    if re.match(r'^[/\\]', stripped) or re.match(r'^[a-zA-Z]:[\\/]', stripped):
        return False
    if re.match(r'^https?://', stripped):
        return False
    # Skip version strings
    if re.match(r'^v?\d+(\.\d+)*', stripped):
        return False
    # Skip format-only
    if re.match(r'^[%{}\d\s.,;:!?\-+*/=<>()\[\]&|^~`@#$]+$', stripped):
        return False
    # Skip regex-like (metacharacters without spaces)
    if re.search(r'[\\\[\]{}()|^$*+?]', stripped) and ' ' not in stripped and not re.search(r'[A-Za-z]{3,}', stripped):
        return False
    # If it has spaces and English, likely translatable
    if ' ' in stripped:
        return True
    # Single capitalized word that looks like a message
    if re.match(r'^[A-Z][a-z]+$', stripped) and stripped not in (
        'Paper','Spigot','Bukkit','Minecraft','Java','Windows','Linux','Mac'):
        return True
    return False

def get_context_line(content, pos):
    ls = content.rfind('\n', 0, pos) + 1
    le = content.find('\n', pos)
    if le == -1:
        le = len(content)
    return content[ls:le].strip()

def verify_file(content):
    """Verify Java file is well-formed: balanced quotes, no unterminated strings, balanced braces/parens."""
    issues = []
    
    # Check string literals
    strings = find_strings_with_positions(content)
    # The state machine itself detects unterminated strings (if in_string at end)
    # But find_strings_with_positions doesn't report that. Let's do a separate check.
    
    # Simple check: count braces and parens (rough)
    # This is approximate because strings/comments can contain them, but good for a sanity check
    in_s = in_c = in_lc = in_bc = False
    brace = paren = bracket = 0
    i = 0
    n = len(content)
    while i < n:
        c = content[i]
        if in_lc:
            if c == '\n': in_lc = False
            i += 1; continue
        if in_bc:
            if c == '*' and i+1 < n and content[i+1] == '/': in_bc = False; i += 2; continue
            i += 1; continue
        if in_s:
            if c == '\\' and i+1 < n: i += 2; continue
            if c == '"': in_s = False
            i += 1; continue
        if in_c:
            if c == '\\' and i+1 < n: i += 2; continue
            if c == "'": in_c = False
            i += 1; continue
        if c == '"':
            # Check text block
            if i+2 < n and content[i+1] == '"' and content[i+2] == '"':
                in_s = True; i += 3; continue
            in_s = True; i += 1; continue
        if c == "'": in_c = True; i += 1; continue
        if c == '/' and i+1 < n:
            if content[i+1] == '/': in_lc = True; i += 2; continue
            if content[i+1] == '*': in_bc = True; i += 2; continue
        if c == '{': brace += 1
        elif c == '}': brace -= 1
        elif c == '(': paren += 1
        elif c == ')': paren -= 1
        elif c == '[': bracket += 1
        elif c == ']': bracket -= 1
        i += 1
    
    if in_s:
        issues.append("Unterminated string literal")
    if in_bc:
        issues.append("Unterminated block comment")
    if brace != 0:
        issues.append(f"Unbalanced braces: {brace}")
    if paren != 0:
        issues.append(f"Unbalanced parentheses: {paren}")
    if bracket != 0:
        issues.append(f"Unbalanced brackets: {bracket}")
    
    return issues

def cmd_extract(filepath):
    """Extract translatable strings from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    strings = find_strings_with_positions(content)
    results = []
    for idx, (start, end, str_content, is_tb) in enumerate(strings):
        if not is_likely_translatable(str_content):
            continue
        line = content[:start].count('\n') + 1
        ctx = get_context_line(content, start)
        results.append({
            "index": idx,
            "line": line,
            "start": start,
            "end": end,
            "is_text_block": is_tb,
            "original": str_content,
            "context": ctx[:200],
        })
    
    print(json.dumps(results, ensure_ascii=False, indent=2))

def cmd_apply(filepath):
    """Apply translations from stdin JSON (mapping original -> translated)."""
    translations = json.load(sys.stdin)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    strings = find_strings_with_positions(content)
    
    # Build mapping: we need to match by original content
    # Process from end to start to preserve positions
    replacements = []
    for start, end, str_content, is_tb in strings:
        if str_content in translations:
            trans = translations[str_content]
            if trans is not None and trans != str_content:
                replacements.append((start, end, str_content, trans, is_tb))
    
    # Sort by start descending
    replacements.sort(key=lambda x: x[0], reverse=True)
    
    modified = content
    applied = 0
    for start, end, orig, trans, is_tb in replacements:
        # Verify the content at this position still matches
        actual = modified[start+1:end-1] if not is_tb else modified[start+3:end-3]
        if actual != orig:
            print(f"WARNING: content mismatch at position {start}, skipping", file=sys.stderr)
            continue
        
        if is_tb:
            modified = modified[:start+3] + trans + modified[end-3:]
        else:
            modified = modified[:start+1] + trans + modified[end-1:]
        applied += 1
    
    # Verify
    issues = verify_file(modified)
    if issues:
        print(f"VERIFICATION FAILED for {filepath}:", file=sys.stderr)
        for iss in issues:
            print(f"  - {iss}", file=sys.stderr)
        print("File NOT written.", file=sys.stderr)
        sys.exit(1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(modified)
    
    print(f"Applied {applied} translations to {filepath}")

def cmd_verify(filepath):
    """Verify a file is well-formed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    issues = verify_file(content)
    if issues:
        print(f"ISSUES in {filepath}:")
        for iss in issues:
            print(f"  - {iss}")
        sys.exit(1)
    else:
        print(f"OK: {filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python file_translator.py <extract|apply|verify> <file_path>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    filepath = sys.argv[2]
    
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    
    if cmd == 'extract':
        cmd_extract(filepath)
    elif cmd == 'apply':
        cmd_apply(filepath)
    elif cmd == 'verify':
        cmd_verify(filepath)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
