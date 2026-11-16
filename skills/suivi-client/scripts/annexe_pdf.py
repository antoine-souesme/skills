"""Génère le PDF d'une annexe de devis ou d'un contrat à partir de sa source markdown.

Usage :
  Annexe :  python annexe_pdf.py ANNEXE.md Annexe.pdf --client "Nom du client" --adresse "Adresse du client" --pied "Annexe au devis n°X · Projet"
  Contrat : python annexe_pdf.py CONTRAT.md Contrat.pdf --pied "Contrat de prestation de service · Projet"

Markdown reconnu : # titre, ## sections, tableaux à 2 colonnes, listes - et 1., **gras**, <br/> dans une cellule.
Avec --client, le bloc émetteur / client est inséré avant la première section ##.
Sans --client (contrat), les parties sont écrites dans le markdown lui-même.
Un tableau dont la première cellule commence par « Le Prestataire » est rendu en deux colonnes égales (bloc de signatures).
Nécessite reportlab (Python 3.10+, ou reportlab==4.2.5 en Python 3.9).
"""
import sys, argparse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether

ap = argparse.ArgumentParser()
ap.add_argument("md"); ap.add_argument("out")
ap.add_argument("--client", default=""); ap.add_argument("--adresse", default="")
ap.add_argument("--pied", default="Annexe au devis")
args = ap.parse_args()
out = args.out
INK = colors.HexColor("#1F2328")
MUTED = colors.HexColor("#555B63")
HEAD = colors.HexColor("#ECEEF2")
LINE = colors.HexColor("#D9DCE1")

base = ParagraphStyle("base", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=INK)
small = ParagraphStyle("small", parent=base, fontSize=8.5, leading=12, textColor=MUTED)
bold = ParagraphStyle("bold", parent=base, fontName="Helvetica-Bold")
title = ParagraphStyle("title", parent=base, fontName="Helvetica-Bold", fontSize=15, leading=19)
h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=12, leading=16, spaceBefore=14, spaceAfter=6)
right = ParagraphStyle("right", parent=base, alignment=2)
rightb = ParagraphStyle("rightb", parent=bold, alignment=2)

W = A4[0] - 36 * mm - 12


def table(rows, widths, header=True):
    data = [[Paragraph(c, bold if (header and i == 0) else base) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


md_path = args.md
import re as _re, html as _html


def inline(t):
    t = _html.escape(t, quote=False)
    t = t.replace("&lt;br/&gt;", "<br/>")
    return _re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


parties = Table([
    [Paragraph("<b>Antoine Souesme (EI)</b>", base), Paragraph(f"<b>{args.client}</b>", right)],
    [Paragraph("33 Impasse des Noisetiers 22800 Le Fœil, FR", base), Paragraph(args.adresse, right)],
    [Paragraph("<b>SIREN :</b> 942 574 567", base), Paragraph("", base)],
], colWidths=[W / 2, W / 2])
parties.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))

story = []
lines = open(md_path, encoding="utf-8").read().splitlines()
i = 0
parties_done = False
pending = []  # heading kept with next block
li_style = ParagraphStyle("li", parent=base, leftIndent=10, spaceAfter=3)
step_style = ParagraphStyle("step", parent=base, spaceAfter=5)


def add(flow):
    global pending
    if pending:
        story.append(KeepTogether(pending + [flow]))
        pending = []
    else:
        story.append(flow)


while i < len(lines):
    l = lines[i].rstrip()
    if not l:
        i += 1
        continue
    if l.startswith("# "):
        story.append(Paragraph(inline(l[2:]), title))
        story.append(Spacer(1, 4))
    elif l.startswith("## "):
        if args.client and not parties_done:
            story += [Spacer(1, 8), HRFlowable(width="100%", thickness=0.5, color=LINE), Spacer(1, 8), parties, Spacer(1, 4)]
            parties_done = True
        pending = [Paragraph(inline(l[3:]), h2)]
    elif l.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(_re.fullmatch(r":?-+:?", c) for c in cells):
                rows.append([inline(c) for c in cells])
            i += 1
        if rows[0][0].startswith("Le Prestataire"):
            # bloc de signatures : jamais coupé entre deux pages
            add(KeepTogether([table(rows, [W * 0.5, W * 0.5])]))
        else:
            add(table(rows, [W * 0.42, W * 0.58]))
        story.append(Spacer(1, 6))
        continue
    elif _re.match(r"\d+\. ", l):
        add(Paragraph(inline(l), step_style))
    elif l.startswith("- "):
        add(Paragraph(inline(l[2:]), li_style, bulletText="•"))
    else:
        add(Paragraph(inline(l), base))
        story.append(Spacer(1, 4))
    i += 1


def footer(c, d):
    c.saveState()
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(18 * mm, 12 * mm, args.pied)
    c.drawRightString(A4[0] - 18 * mm, 12 * mm, f"Page {d.page}")
    c.restoreState()


doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=20 * mm,
                        title=args.pied, author="Antoine Souesme")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("ok")
