"""A deliberately tiny markdown subset renderer: headings, paragraphs, lists,
pipe tables, bold/italic, inline code and links. No third-party dependency, and
it escapes HTML so generated pages cannot inject markup from the source file."""

import html
import re


def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", "", t)                      # drop images
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1 ↗</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def to_html(md):
    out, i = [], 0
    lines = md.split("\n")
    n = len(lines)
    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        # table: header row, separator, body rows
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append('<div class="tablewrap"><table class="data"><thead><tr>'
                       + "".join("<th>%s</th>" % _inline(h) for h in header)
                       + "</tr></thead><tbody>")
            for r in rows:
                out.append("<tr>" + "".join("<td>%s</td>" % _inline(c) for c in r) + "</tr>")
            out.append("</tbody></table></div>")
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = max(2, len(m.group(1)))
            out.append("<h%d>%s</h%d>" % (lvl, _inline(m.group(2)), lvl))
            i += 1
            continue

        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % _inline(x) for x in items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join("<li>%s</li>" % _inline(x) for x in items) + "</ol>")
            continue

        para = []
        while i < n and lines[i].strip() and not re.match(r"^(#{1,6}\s|\s*[-*]\s|\s*\d+\.\s|\|)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % _inline(" ".join(para)))

    return "\n".join(out)
