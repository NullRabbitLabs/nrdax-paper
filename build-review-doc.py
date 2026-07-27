#!/usr/bin/env python3
"""Concatenate the paper into one file for review in Google Docs or similar.

The sections in `sections/` remain the source of truth. This is a generated
read-and-comment artefact: deterministic, so re-running produces the same bytes
and a returned copy can be diffed against it.

Usage:  python3 build-review-doc.py            -> review/paper-full.md
        python3 build-review-doc.py --html     -> review/paper-full.html
"""
from __future__ import annotations
import pathlib, re, sys, html

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "review"


def body() -> str:
    head = (ROOT / "paper.md").read_text()
    # Keep title, authors, status and abstract; drop the contents list and the
    # repo-navigation footer, which mean nothing in a linear document.
    head = head.split("## Contents")[0].rstrip()
    parts = [head, "\n\n---\n"]
    for f in sorted((ROOT / "sections").glob("*.md")):
        t = f.read_text().strip()
        # A figure is a repo-relative SVG that Google Docs cannot render. Leave a
        # labelled marker so the reviewer knows one belongs there.
        t = re.sub(r"!\[(.*?)\]\(\.\./figures/(.*?)\)",
                   r"> **[FIGURE: \1]** — see `figures/\2` in the repository.", t)
        parts.append(t)
        parts.append("\n\n---\n")
    return "\n".join(parts).rstrip() + "\n"


def to_html(md: str) -> str:
    """Minimal markdown->HTML: enough for Google Docs to import headings, tables,
    lists, blockquotes and inline code with structure intact."""
    out, in_table, in_code = [], False, False
    for line in md.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            out.append("<pre>" if in_code else "</pre>")
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            if not in_table:
                out.append("<table border='1' cellpadding='4' cellspacing='0'>")
                in_table = True
            tag = "th" if len(out) and out[-1].startswith("<table") else "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
            continue
        if in_table:
            out.append("</table>")
            in_table = False
        m = re.match(r"^(#{1,4}) (.*)$", line)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
        elif re.match(r"^[-*] ", line):
            out.append(f"<li>{inline(line[2:])}</li>")
        elif re.match(r"^\d+\. ", line):
            out.append(f"<li>{inline(re.sub(r'^\d+\. ', '', line))}</li>")
        elif line.startswith(">"):
            out.append(f"<blockquote>{inline(line.lstrip('> '))}</blockquote>")
        elif line.strip() == "---":
            out.append("<hr>")
        elif not line.strip():
            out.append("")
        else:
            out.append(f"<p>{inline(line)}</p>")
    if in_table:
        out.append("</table>")
    return ("<html><head><meta charset='utf-8'><title>NRDAX taxonomy paper</title></head>"
            "<body style=\"font-family:Georgia,serif;max-width:46em\">\n"
            + "\n".join(out) + "\n</body></html>\n")


def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def main() -> None:
    OUT.mkdir(exist_ok=True)
    md = body()
    if "--html" in sys.argv:
        p = OUT / "paper-full.html"
        p.write_text(to_html(md))
    else:
        p = OUT / "paper-full.md"
        p.write_text(md)
    words = len(md.split())
    print(f"{p.relative_to(ROOT)}  {words} words, {len(md)} bytes")


if __name__ == "__main__":
    main()
