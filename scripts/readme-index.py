#!/usr/bin/env python3
"""Generate the skill index of README.md from the SKILL.md frontmatter, so counts and names cannot drift.

Usage:
  python scripts/readme-index.py            # rewrite the block between the markers (insert it if missing)
  python scripts/readme-index.py --check    # exit 1 if the block is missing or out of date

The block sits between these markers in README.md:
  <!-- skills:start -->  ...  <!-- skills:end -->
Skills are the top-level folders that contain SKILL.md. The text of each row is the first sentence of
the skill description (everything before " Use "), shortened to 170 characters.
Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- skills:start -->", "<!-- skills:end -->"
MAXLEN = 170


def frontmatter(text: str):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
            if k:
                v = k.group(2).strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                out[k.group(1)] = v
    return out


def summary(desc: str) -> str:
    first = desc.split(" Use ", 1)[0].strip().rstrip(".")
    first = first.replace("|", "/")
    if len(first) > MAXLEN:
        first = first[:MAXLEN].rsplit(" ", 1)[0].rstrip(",;:- ") + "..."
    return first


def build_block() -> str:
    rows = []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").exists()):
        fm = frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
        rows.append(f"| [`{d.name}`]({d.name}/SKILL.md) | {summary(fm.get('description', ''))} |")
    head = (f"{START}\n**{len(rows)} skills.** This index is generated from each `SKILL.md`; "
            "run `python scripts/readme-index.py` to refresh it.\n\n| Skill | What it does |\n|---|---|")
    return "\n".join([head, *rows, END])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    text = text.replace("\r\n", "\n")
    block = build_block()

    if START in text and END in text:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _m: block, text, count=1, flags=re.S)
    else:
        if args.check:
            print("README.md has no skill index block (run python scripts/readme-index.py)")
            return 1
        m = re.search(r"\n## ", text)
        pos = m.start() + 1 if m else len(text)
        new = text[:pos] + "## Skill index\n\n" + block + "\n\n" + text[pos:]

    if args.check:
        if new != text:
            print("README.md skill index is out of date (run python scripts/readme-index.py)")
            return 1
        print("README.md skill index is up to date")
        return 0
    if new != text:
        readme.write_text(new.replace("\n", nl), encoding="utf-8", newline="")
        print("README.md skill index updated")
    else:
        print("README.md skill index already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
