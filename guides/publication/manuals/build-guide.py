#!/usr/bin/env python3
"""Build the English MyScoutee engineering guide from its Markdown chapters."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, CondPageBreak, Frame, Image, LongTable, NextPageTemplate, PageBreak, PageTemplate, Paragraph, Preformatted, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
OUTPUT = ROOT / "MyScoutee_Engineering_Deep_Dive_EN.pdf"
PATTERN_OUTPUT = REPO.parent / "myscoutee-backend" / "guides" / "learning" / "MyScoutee_Patterns_Data_Structures_and_Algorithms_EN.pdf"
TMP = REPO / "tmp" / "pdfs"
ASSET = ROOT / "assets" / "heart.png"
CHAPTERS = [
    REPO / "guides/development/architecture/01-context.md",
    REPO / "guides/development/architecture/02-application-and-data.md",
    REPO / "guides/development/architecture/03-deployment-and-operations.md",
    REPO / "guides/development/architecture/04-security-and-integrations.md",
    REPO / "guides/development/architecture/05-evidence-and-decisions.md",
    REPO / "guides/development/architecture/06-frameworks-applied.md",
    REPO / "guides/development/architecture/07-firebase-configuration.md",
    REPO / "guides/development/methods/rup-to-agile.md",
    REPO / "guides/development/decisions/marketing.md",
    REPO / "guides/development/decisions/cost.md",
    REPO / "guides/development/decisions/netcup-cloudflare-cloud.md",
    REPO / "guides/development/decisions/cloud-provider-stacks-and-billing.md",
    REPO / "guides/development/decisions/technology-trials.md",
]
PATTERN_CHAPTERS = [
    REPO / "guides/development/engineering/patterns-data-structures-and-algorithms.md",
    REPO / "guides/development/engineering/laboratory-map.md",
]

for name, filename in (
    ("Guide", "DejaVuSans.ttf"),
    ("GuideBold", "DejaVuSans-Bold.ttf"),
    ("GuideMono", "DejaVuSansMono.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, "/usr/share/fonts/truetype/dejavu/" + filename))

NAVY = colors.HexColor("#17324d")
TEAL = colors.HexColor("#176b87")
INK = colors.HexColor("#1c2633")
MUTED = colors.HexColor("#586675")
SOFT = colors.HexColor("#f3f6f8")
LINE = colors.HexColor("#d9e1e8")
PAGE_WIDTH, PAGE_HEIGHT = A4
CONTENT_WIDTH = PAGE_WIDTH - 92
LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT = landscape(A4)
LANDSCAPE_CONTENT_WIDTH = LANDSCAPE_WIDTH - 92
LANDSCAPE_CHAPTERS = {"06-frameworks-applied", "rup-to-agile", "marketing", "netcup-cloudflare-cloud", "cloud-provider-stacks-and-billing"}
NEW_PAGE_CHAPTERS = {"07-firebase-configuration"}
styles = getSampleStyleSheet()
styles.add(ParagraphStyle("BodyGuide", fontName="Guide", fontSize=8.6, leading=12.4, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle("TitleGuide", fontName="GuideBold", fontSize=24, leading=30, textColor=NAVY, spaceAfter=16))
styles.add(ParagraphStyle("ChapterGuide", fontName="GuideBold", fontSize=17, leading=22, textColor=NAVY, spaceAfter=13))
styles.add(ParagraphStyle("SectionGuide", fontName="GuideBold", fontSize=12, leading=16, textColor=NAVY, spaceBefore=11, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle("SubsectionGuide", fontName="GuideBold", fontSize=9.5, leading=13, textColor=TEAL, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle("KickerGuide", fontName="GuideBold", fontSize=8, leading=12, textColor=TEAL, spaceAfter=9))
styles.add(ParagraphStyle("SmallGuide", parent=styles["BodyGuide"], fontSize=7.6, leading=10.6, textColor=MUTED))
styles.add(ParagraphStyle("CellGuide", parent=styles["BodyGuide"], fontSize=7.3, leading=10.3, spaceAfter=0))
styles.add(ParagraphStyle("WideCellGuide", parent=styles["CellGuide"], fontSize=7.6, leading=10.7))
styles.add(ParagraphStyle("WideHeaderGuide", parent=styles["WideCellGuide"], fontName="GuideBold", textColor=NAVY))
styles.add(ParagraphStyle("CardGuide", parent=styles["BodyGuide"], fontSize=7.7, leading=10.8, spaceAfter=2))
styles.add(ParagraphStyle("CodeGuide", fontName="GuideMono", fontSize=7.2, leading=10.2, textColor=NAVY, backColor=SOFT, borderPadding=9, spaceBefore=3, spaceAfter=9))

TOKEN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|`([^`]+)`")


def markup(value: str) -> str:
    parts = []
    last = 0
    for match in TOKEN.finditer(value):
        parts.append(escape(value[last:match.start()]))
        if match.group(1) is not None:
            label, url = match.group(1), match.group(2)
            parts.append(f'<link href="{escape(url)}" color="#176b87">{escape(label)}</link>')
        elif match.group(3) is not None:
            parts.append(f'<b>{escape(match.group(3))}</b>')
        else:
            parts.append(f'<font name="GuideMono">{escape(match.group(4))}</font>')
        last = match.end()
    parts.append(escape(value[last:]))
    return "".join(parts)


def para(value: str, style: str = "BodyGuide") -> Paragraph:
    return Paragraph(markup(value), styles[style])


def table(lines: list[str], content_width: float = CONTENT_WIDTH) -> list:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    rows = [row for row in rows if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in row)]
    if not rows:
        return []
    count = len(rows[0])
    if count > 3 and content_width == CONTENT_WIDTH:
        result = []
        for row in rows[1:]:
            title = row[0]
            body = "<br/>".join(f"<b>{escape(rows[0][i])}:</b> {markup(row[i])}" for i in range(1, count))
            card = Table([[para(title, "CardGuide")], [Paragraph(body, styles["CardGuide"])]], colWidths=[CONTENT_WIDTH])
            card.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.35, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            result.extend([card, Spacer(1, 5)])
        return result
    if count > 3:
        first_fraction = 0.14 if count == 6 else 0.15
        widths = [content_width * first_fraction] + [content_width * (1 - first_fraction) / (count - 1)] * (count - 1)
        cells = [[para(cell, "WideHeaderGuide" if row_index == 0 else "WideCellGuide") for cell in row] for row_index, row in enumerate(rows)]
        item = LongTable(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
        item.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (-1, 0), SOFT),
            ("BACKGROUND", (0, 1), (0, -1), SOFT),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return [item, Spacer(1, 9)]
    fractions = {2: [0.32, 0.68], 3: [0.23, 0.385, 0.385]}.get(count, [1])
    widths = [content_width * value for value in fractions]
    cells = [[para(cell, "CellGuide") for cell in row] for row in rows]
    item = LongTable(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    item.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), SOFT),
        ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return [item, Spacer(1, 9)]


# These simple figures mirror the Markdown Mermaid views without requiring a
# browser or a Mermaid runtime during PDF generation.
DOT = {
    "01-context": 'digraph G {rankdir=LR; people[label="People and operators"]; product[label="MyScoutee product"]; systems[label="Firebase / payments / email"]; stores[label="Mongo / Redis / objects"]; registry[label="Independent Registry\n(opt-in)"]; people->product; product->systems; product->stores; product->registry[style=dashed];}',
    "02-application-and-data": 'digraph G {rankdir=LR; browser[label="Angular browser"]; gate[label="nginx"]; java[label="Java domains"]; mongo[label="MongoDB\nREAL / DEMO"]; worker[label="Affinity worker"]; browser->gate->java->mongo; mongo->worker[label="change stream"]; worker->mongo[label="projection"];}',
    "03-deployment-and-operations": 'digraph G {rankdir=LR; gate[label="nginx + Angular"]; api[label="Java API"]; mcp[label="MCP"]; db[label="Mongo / Redis / MinIO"]; demo[label="Explore Registry\n+ simulator"]; gate->api; gate->mcp->api; api->db; api->demo;}',
    "04-security-and-integrations": 'digraph G {rankdir=LR; client[label="Browser / external client"]; gate[label="Public edge"]; auth[label="Java auth + domain policy"]; product[label="Product data"]; registry[label="Independent Registry"]; client->gate->auth->product; auth->registry[style=dashed,label="operator consent + host egress"];}',
    "06-frameworks-applied": 'digraph G {rankdir=LR; people[label="Members / operators"]; ui[label="Angular UI\n(browser)"]; client[label="External client"]; gate[label="nginx"]; api[label="Java API"]; mcp[label="MCP gateway"]; stores[label="Mongo / Redis / MinIO"]; registry[label="Independent Registry"]; people->ui->gate->api->stores; client->gate; gate->mcp->api; api->registry[style=dashed,label="operator opt-in"];} ',
    "laboratory-map": 'digraph G {rankdir=LR; product[label="Installed Compose product"]; kvm[label="KVM/K3s lab"]; big[label="Big Data lab"]; elastic[label="Elastic lab"]; factor[label="2FA lab"]; infra[label="Infra lab"]; ci[label="CI lab"]; product->kvm[style=dotted,label="same source, separate runtime"]; big->product[style=dashed,dir=none,label="no data feed"]; elastic->product[style=dashed,dir=none,label="no telemetry feed"]; factor->product[style=dashed,dir=none,label="no login link"]; infra->product[style=dashed,dir=none,label="no provisioning"]; ci->product[style=dotted,label="candidate builds"];} ',
    "rup-to-agile": 'digraph G {rankdir=LR; rup[label="RUP\nrisk-driven iterations"]; one[label="1. Tailored RUP\nsmall tested slices"]; two[label="2. Lean UP\nOpenUP / AUP ideas"]; agile[label="Agile delivery\nempirical product decisions"]; rup->one->two->agile;}',
}


def figure(name: str) -> list:
    if name not in DOT:
        return []
    TMP.mkdir(parents=True, exist_ok=True)
    path = TMP / f"{name}.png"
    source = DOT[name].replace("digraph G {", 'digraph G {graph [bgcolor="transparent", pad="0.15", nodesep="0.25", ranksep="0.45"]; node [shape=box, style="rounded,filled", fillcolor="#eef5f8", color="#176b87", fontname="DejaVu Sans", fontsize=10, margin="0.16,0.12"]; edge [color="#176b87", fontname="DejaVu Sans", fontsize=8];')
    subprocess.run(["dot", "-Tpng", "-o", str(path)], input=source.encode(), check=True)
    with PILImage.open(path) as picture:
        width, height = picture.size
    scale = min(CONTENT_WIDTH / width, 135 / height)
    return [Image(str(path), width=width * scale, height=height * scale, hAlign="CENTER"), Spacer(1, 12)]


def parse_chapter(path: Path, content_width: float = CONTENT_WIDTH) -> list:
    story = [CondPageBreak(190)]
    lines = path.read_text(encoding="utf-8").splitlines()
    paragraph = []
    i = 0
    seen_figure = False

    def flush() -> None:
        if paragraph:
            story.append(para(" ".join(paragraph)))
            paragraph.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            language = line[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            if language == "mermaid":
                if not seen_figure:
                    story.extend(figure(path.stem))
                    seen_figure = True
            elif block:
                story.append(Preformatted("\n".join(block), styles["CodeGuide"]))
        elif line.startswith("|"):
            flush()
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            story.extend(table(block, content_width))
            continue
        elif line.startswith("# "):
            flush()
            story.append(para(line[2:], "ChapterGuide"))
        elif line.startswith("## "):
            flush()
            if path.stem == "cloud-provider-stacks-and-billing" and line[3:] == "Where the bill changes":
                story.append(CondPageBreak(410))
            elif path.stem == "cloud-provider-stacks-and-billing" and line[3:].startswith("Egress-only example"):
                story.append(CondPageBreak(190))
            story.append(para(line[3:], "SectionGuide"))
        elif line.startswith("### "):
            flush()
            story.append(para(line[4:], "SubsectionGuide"))
        elif re.match(r"^(?:- |\d+\. )", line):
            flush()
            marker, body = line.split(" ", 1)
            story.append(Paragraph(markup(body), styles["BodyGuide"], bulletText="•" if marker == "-" else marker))
        elif not line.strip():
            flush()
        else:
            paragraph.append(line.strip())
        i += 1
    flush()
    return story


def frame(canvas, doc) -> None:
    page_width, page_height = canvas._pagesize
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(46, page_height - 39, page_width - 46, page_height - 39)
    canvas.setFillColor(NAVY)
    canvas.setFont("GuideBold", 9)
    label = "LEARNING" if Path(doc.filename).name == PATTERN_OUTPUT.name else "ENGINEERING"
    canvas.drawString(46, page_height - 31, f"MYSCOUTEE  /  {label}")
    canvas.setFillColor(MUTED)
    canvas.setFont("Guide", 7.5)
    canvas.drawString(46, 27, "MyScoutee architecture and learning guides")
    canvas.drawRightString(page_width - 46, 27, str(doc.page))
    canvas.restoreState()


def build() -> None:
    for path in CHAPTERS:
        if not path.exists():
            raise FileNotFoundError(path)
    doc = BaseDocTemplate(str(OUTPUT), pagesize=A4, title="MyScoutee Engineering Deep Dive", author="MyScoutee")
    doc.addPageTemplates([
        PageTemplate(id="portrait", frames=[Frame(46, 46, CONTENT_WIDTH, PAGE_HEIGHT - 101, 0, 0, 0, 0)], pagesize=A4, onPage=frame),
        PageTemplate(id="landscape", frames=[Frame(46, 46, LANDSCAPE_CONTENT_WIDTH, LANDSCAPE_HEIGHT - 101, 0, 0, 0, 0)], pagesize=landscape(A4), onPage=frame),
    ])
    story = [Spacer(1, 90), Image(str(ASSET), width=76, height=76, hAlign="LEFT"), Spacer(1, 25), para("MyScoutee Engineering Deep Dive", "TitleGuide"), para("Architecture  /  delivery methods  /  decisions", "KickerGuide"), para("A cross-repository guide to the MyScoutee architecture, including Firebase configuration, delivery methods and technology choices."), Spacer(1, 28), para("Contents", "SectionGuide")]
    for chapter in CHAPTERS:
        first = chapter.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
        story.append(para(first, "BodyGuide"))
    story.append(PageBreak())
    current_template = "portrait"
    for chapter in CHAPTERS:
        target_template = "landscape" if chapter.stem in LANDSCAPE_CHAPTERS else "portrait"
        if target_template != current_template or target_template == "landscape" or chapter.stem in NEW_PAGE_CHAPTERS:
            story.extend([NextPageTemplate(target_template), PageBreak()])
        content_width = LANDSCAPE_CONTENT_WIDTH if target_template == "landscape" else CONTENT_WIDTH
        story.extend(parse_chapter(chapter, content_width))
        current_template = target_template
    doc.build(story)
    print(f"Wrote {OUTPUT}")


def build_patterns() -> None:
    for path in PATTERN_CHAPTERS:
        if not path.exists():
            raise FileNotFoundError(path)
    doc = BaseDocTemplate(str(PATTERN_OUTPUT), pagesize=A4, title="MyScoutee Patterns, Data Structures and Algorithms", author="MyScoutee")
    doc.addPageTemplates([
        PageTemplate(id="portrait", frames=[Frame(46, 46, CONTENT_WIDTH, PAGE_HEIGHT - 101, 0, 0, 0, 0)], pagesize=A4, onPage=frame),
    ])
    story = [Spacer(1, 90), Image(str(ASSET), width=76, height=76, hAlign="LEFT"), Spacer(1, 25), para("MyScoutee Patterns, Data Structures and Algorithms", "TitleGuide"), para("Application  /  laboratories", "KickerGuide"), para("An illustrated map of the implemented design patterns, data structures and algorithms in the MyScoutee application and its adjacent laboratories."), Spacer(1, 28), para("Contents", "SectionGuide")]
    for chapter in PATTERN_CHAPTERS:
        first = chapter.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
        story.append(para(first, "BodyGuide"))
    story.append(PageBreak())
    for index, chapter in enumerate(PATTERN_CHAPTERS):
        story.extend(parse_chapter(chapter))
        if index + 1 < len(PATTERN_CHAPTERS):
            story.append(PageBreak())
    doc.build(story)
    print(f"Wrote {PATTERN_OUTPUT}")


if __name__ == "__main__":
    build()
    build_patterns()
