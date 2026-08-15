#!/usr/bin/env python3
"""Stdlib Markdown → HTML for a local preview. No Rust, no Dataview runtime."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

VAULT = Path("/root/obsidian-vault")
OUT = Path("/var/www/obsidian")
SKIP_DIRS = {
    ".git",
    ".obsidian",
    ".trash",
    "Logs",
    "node_modules",
}
SKIP_FILES = {
    "sessions.md",  # live C2 session table — not for HTTP
}


def collect_notes(root: Path) -> dict[str, Path]:
    by_stem: dict[str, Path] = {}
    for path in root.rglob("*.md"):
        if any(p in SKIP_DIRS for p in path.relative_to(root).parts):
            continue
        if path.name in SKIP_FILES:
            continue
        by_stem.setdefault(path.stem, path)
    return by_stem


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return text


def wiki_href(target: str, src: Path, notes: dict[str, Path], vault: Path) -> str:
    name = target.split("|", 1)[0].strip().removesuffix(".md")
    dest = notes.get(Path(name).name) or notes.get(name)
    if dest is None:
        rel = Path(name)
        if not rel.suffix:
            rel = rel.with_suffix(".md")
        candidate = (vault / rel).resolve()
        if candidate.is_file():
            dest = candidate
    if dest is None:
        return ""
    html_rel = dest.relative_to(vault).with_suffix(".html")
    src_dir = src.parent
    try:
        return Path(html_rel).as_posix() if src_dir == vault else Path(
            "../" * len(src.relative_to(vault).parent.parts)
        ).joinpath(html_rel).as_posix()
    except ValueError:
        return html_rel.as_posix()


def convert(md: str, src: Path, notes: dict[str, Path], vault: Path) -> str:
    md = strip_frontmatter(md)
    lines = md.splitlines()
    out: list[str] = []
    in_code = False
    in_table = False

    def close_table() -> None:
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            close_table()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                lang = html.escape(line[3:].strip())
                out.append(f'<pre><code class="lang-{lang}">')
                in_code = True
            i += 1
            continue
        if in_code:
            out.append(html.escape(line))
            i += 1
            continue

        if re.match(r"^\|", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
                i += 1
                continue
            if not in_table:
                out.append("<table><thead><tr>")
                out.append("".join(f"<th>{inline(c, src, notes, vault)}</th>" for c in cells))
                out.append("</tr></thead><tbody>")
                in_table = True
            else:
                out.append("<tr>" + "".join(f"<td>{inline(c, src, notes, vault)}</td>" for c in cells) + "</tr>")
            i += 1
            continue
        close_table()

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2), src, notes, vault)}</h{level}>")
            i += 1
            continue
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append("<li>" + inline(re.sub(r"^[-*]\s+", "", lines[i]), src, notes, vault) + "</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append("<li>" + inline(re.sub(r"^\d+\.\s+", "", lines[i]), src, notes, vault) + "</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        if not line.strip():
            i += 1
            continue
        out.append("<p>" + inline(line, src, notes, vault) + "</p>")
        i += 1
    close_table()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def inline(text: str, src: Path, notes: dict[str, Path], vault: Path) -> str:
    def wiki(match: re.Match[str]) -> str:
        raw = match.group(1)
        label = raw.split("|", 1)[1] if "|" in raw else raw
        href = wiki_href(raw, src, notes, vault)
        if not href:
            return f"<span class='missing'>[[{html.escape(raw)}]]</span>"
        return f'<a href="{html.escape(href)}">{html.escape(label)}</a>'

    text = re.sub(r"\[\[([^\]]+)\]\]", wiki, text)
    text = html.escape(text, quote=False)
    # restore the anchors we just built (they were escaped)
    # re-run wiki on unescaped? already mixed. Simpler path: apply wiki after escape using placeholders.
    return text


def inline_fixed(text: str, src: Path, notes: dict[str, Path], vault: Path) -> str:
    parts: list[str] = []
    last = 0
    for match in re.finditer(r"\[\[([^\]]+)\]\]|`([^`]+)`|\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(html.escape(text[last : match.start()]))
        if match.group(1) is not None:
            raw = match.group(1)
            label = raw.split("|", 1)[1] if "|" in raw else raw
            href = wiki_href(raw, src, notes, vault)
            if href:
                parts.append(f'<a href="{html.escape(href)}">{html.escape(label)}</a>')
            else:
                parts.append(f"<span class='missing'>[[{html.escape(raw)}]]</span>")
        elif match.group(2) is not None:
            parts.append(f"<code>{html.escape(match.group(2))}</code>")
        elif match.group(3) is not None:
            parts.append(f"<strong>{html.escape(match.group(3))}</strong>")
        else:
            parts.append(f'<a href="{html.escape(match.group(5))}">{html.escape(match.group(4))}</a>')
        last = match.end()
    parts.append(html.escape(text[last:]))
    return "".join(parts)


# use the fixed inline everywhere
inline = inline_fixed  # type: ignore[misc]


PAGE = """<!doctype html>
<html lang="pl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body{{font:16px/1.5 system-ui,sans-serif;max-width:920px;margin:2rem auto;padding:0 1rem;color:#e8eaed;background:#12141a}}
a{{color:#8ab4f8}} .missing{{color:#f28b82}}
pre{{background:#1e222b;padding:1rem;overflow:auto;border-radius:8px}}
code{{font-family:ui-monospace,monospace;font-size:.9em}}
table{{border-collapse:collapse;width:100%;margin:1rem 0}}
th,td{{border:1px solid #3c4043;padding:.4rem .6rem;text-align:left}}
th{{background:#1e222b}}
nav{{font-size:.9rem;margin-bottom:1.5rem;color:#9aa0a6}}
.note{{background:#1e222b;padding:.75rem 1rem;border-radius:8px;margin:1rem 0;color:#9aa0a6}}
</style></head>
<body>
<nav><a href="/index.html">indeks</a> · {rel}</nav>
<p class="note">Podgląd statyczny (bez Dataview/Tasks). Sesje Sliver i logi nie są publikowane. Tylko localhost:8081.</p>
{body}
</body></html>
"""


def write_index(out: Path, notes: list[Path], vault: Path) -> None:
    items = []
    for path in sorted(notes, key=lambda p: str(p.relative_to(vault)).lower()):
        rel = path.relative_to(vault)
        href = rel.with_suffix(".html").as_posix()
        items.append(f'<li><a href="{html.escape(href)}">{html.escape(rel.as_posix())}</a></li>')
    body = "<h1>Obsidian vault (podgląd)</h1><ul>" + "\n".join(items) + "</ul>"
    (out / "index.html").write_text(
        PAGE.format(title="Vault", rel="index", body=body),
        encoding="utf-8",
    )


def main() -> int:
    vault = Path(sys.argv[1]) if len(sys.argv) > 1 else VAULT
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT
    notes = collect_notes(vault)
    out.mkdir(parents=True, exist_ok=True)
    written = 0
    for path in notes.values():
        rel = path.relative_to(vault)
        dest = out / rel.with_suffix(".html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        body = convert(path.read_text(encoding="utf-8", errors="replace"), path, notes, vault)
        dest.write_text(
            PAGE.format(title=html.escape(path.stem), rel=html.escape(rel.as_posix()), body=body),
            encoding="utf-8",
        )
        written += 1
    write_index(out, list(notes.values()), vault)
    print(f"exported {written} notes → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
