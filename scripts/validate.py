#!/usr/bin/env python3
"""Validate the skill set in this repository.

Usage: python scripts/validate.py [repo_root]        (default: parent of this script's folder)

Checks per skill folder (any top-level folder containing SKILL.md):
  - frontmatter has exactly `name` and `description`; name == folder name, kebab-case
  - description: starts with a capitalised third-person verb (ends with "s"), <= 900 characters,
    contains "Do NOT use", contains Vietnamese keywords (diacritics) and no duplicated trigger phrases
    across skills
  - every .md file outside evals/ is < 250 lines; code fences balanced
  - only `references/`, `scripts/` (one level deep) and `evals/` (may nest) sub folders
  - every `references/x.md` or `scripts/x.py` mentioned in SKILL.md exists
  - a skill may reach a sibling only as `../<skill-name>/` where that folder exists
  - .py files compile without SyntaxWarning (use raw strings r'...' for regex and backslashes)
Exit code 1 when any check fails.
"""
import os, re, sys, warnings

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
skills = sorted(d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, 'SKILL.md')))
errors, triggers = [], {}


def fence_ok(path):
    stack = None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^\s*(`{3,})(.*)$', line.rstrip('\n'))
        if not m:
            continue
        n, info = len(m.group(1)), m.group(2).strip()
        if stack is None:
            stack = n
        elif n >= stack and info == '':
            stack = None
    return stack is None


for s in skills:
    d = os.path.join(root, s)
    f = os.path.join(d, 'SKILL.md')
    t = open(f, encoding='utf-8').read()
    e = []
    m = re.match(r'^---\nname: (.+)\ndescription: (.+)\n---\n', t)
    if not m:
        e.append('frontmatter must be exactly name + description between --- lines')
    else:
        name, desc = m.group(1).strip(), m.group(2).strip()
        if name != s:
            e.append(f'name "{name}" != folder')
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', name):
            e.append('name not kebab-case')
        w = desc.split()[0]
        if not (w[0].isupper() and w.endswith('s')):
            e.append(f'description starts with "{w}" (needs a third-person verb)')
        if len(desc) > 900:
            e.append(f'description is {len(desc)} chars (> 900)')
        if 'Do NOT use' not in desc:
            e.append('description lacks "Do NOT use"')
        if not re.search(r'[À-ỹ]', desc):
            e.append('description lacks Vietnamese trigger keywords')
        for q in set(re.findall(r'"([^"]+)"', desc.split('Do NOT use')[0])):
            triggers.setdefault(q.lower(), []).append(s)
    for dp, dn, fn in os.walk(d):
        rel = os.path.relpath(dp, d)
        top = rel.split(os.sep)[0]
        if top not in ('.', 'references', 'scripts', 'evals'):
            e.append(f'unexpected folder {rel}')
        if top in ('references', 'scripts') and rel != top:
            e.append(f'{rel} is nested too deep')
        for x in fn:
            p = os.path.join(dp, x)
            if x.endswith('.md') and top != 'evals':
                n = open(p, encoding='utf-8').read().count('\n') + 1
                if n >= 250:
                    e.append(f'{os.path.relpath(p, root)} has {n} lines (>= 250)')
                if not fence_ok(p):
                    e.append(f'unbalanced code fence in {os.path.relpath(p, root)}')
            if x.endswith('.py'):
                with open(p, encoding='utf-8') as fh:
                    src = fh.read()
                with warnings.catch_warnings():
                    warnings.simplefilter('error')  # SyntaxWarning counts as failure
                    try:
                        compile(src, p, 'exec')
                    except (SyntaxError, Warning) as ex:
                        e.append(f'{os.path.relpath(p, root)} does not compile cleanly: {ex}')
    for ref in set(re.findall(r'`((?:references|scripts)/[\w\-./]+\.(?:md|py))`', t)):
        if not os.path.exists(os.path.join(d, ref)):
            e.append(f'mentioned file missing: {ref}')
    for sib in re.findall(r'\.\./([\w<>\-]+)/', t):
        if '<' not in sib and sib not in skills:
            e.append(f'"../{sib}/" points to a skill that does not exist')
    print(f'{"FAIL" if e else "ok  "} {s}')
    for x in e:
        print('     -', x)
    errors += [f'{s}: {x}' for x in e]

dups = {k: v for k, v in triggers.items() if len(v) > 1}
if dups:
    errors.append(f'duplicate trigger phrases: {dups}')
    print('FAIL duplicate trigger phrases:', dups)
print(f'\n{len(skills)} skills checked, {len(errors)} problem(s).')
sys.exit(1 if errors else 0)
