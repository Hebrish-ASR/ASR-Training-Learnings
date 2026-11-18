#!/usr/bin/env python3
"""Build learnings.json and the index table in README.md from learnings/*.md (front matter + body). Stdlib only.

    python3 scripts/build_index.py          # rewrite learnings.json and the README block between the index markers
    python3 scripts/build_index.py --check  # exit 1 if an entry is missing a field or the outputs are stale

Front matter (between --- lines, one `key: value` per line; lists as [a, b]):
  title, date (YYYY-MM-DD), models (base model ids), lines (fine-tune lines affected), topic, status.
The body has three sections: what was seen / question, why / finding, and "What changed in the training".
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ = ("title", "date", "models", "lines", "topic", "status")
BEGIN, END = "<!-- index:begin -->", "<!-- index:end -->"


def parse(path):
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise SystemExit(f"{path.name}: no front matter")
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        v = v.strip()
        meta[k.strip()] = [x.strip() for x in v[1:-1].split(",") if x.strip()] if v.startswith("[") else v
    missing = [k for k in REQ if not meta.get(k)]
    if missing:
        raise SystemExit(f"{path.name}: missing {missing}")
    body = m.group(2).strip()
    eff = re.search(r"## What changed in the training\n+(.*?)(?=\n## |\Z)", body, re.S)
    return {"id": path.stem, **meta, "file": f"learnings/{path.name}", "strategy_effect": eff.group(1).strip() if eff else "",
            "body_md": body}


def build():
    rows = sorted((parse(p) for p in (ROOT / "learnings").glob("*.md")), key=lambda r: (r["date"], r["id"]), reverse=True)
    table = "| Date | Learning | Models | Topic | Status |\n|---|---|---|---|---|\n" + "\n".join(
        f"| {r['date']} | [{r['title']}]({r['file']}) | {', '.join(r['models'])} | {r['topic']} | {r['status']} |" for r in rows)
    return rows, table


def main():
    rows, table = build()
    js = json.dumps({"learnings": rows}, indent=1, ensure_ascii=False) + "\n"
    readme = (ROOT / "README.md").read_text()
    new = readme[: readme.index(BEGIN) + len(BEGIN)] + "\n" + table + "\n" + readme[readme.index(END):]
    if "--check" in sys.argv:
        stale = (ROOT / "learnings.json").read_text() != js or readme != new
        sys.exit(f"stale: run scripts/build_index.py" if stale else 0)
    (ROOT / "learnings.json").write_text(js)
    (ROOT / "README.md").write_text(new)
    print(f"{len(rows)} learnings")


if __name__ == "__main__":
    main()
