"""
BOOST training teacher flyer — single-page A4 PDF.
Modern layout inspired by reference: hero+photo split, service grid,
dark trainers panel, contact strip footer.
Borosil-orange palette.
Output: C:\\Users\\Devastotra Poddar\\Downloads\\BOOST_Training_Flyer_Teachers.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepInFrame,
)
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame

REPO = r"C:\Users\Devastotra Poddar\Downloads\boost-training-reg"
HERO_IMG = os.path.join(REPO, "assets", "nutrition-banner.jpg")
LOGO_IMG = os.path.join(REPO, "assets", "belda_logo.png")
INST_KJ_RAW = os.path.join(REPO, "assets", "kjeldahl.jpg")
INST_FAT_RAW = os.path.join(REPO, "assets", "fat-analyser.png")
INST_FIB_RAW = os.path.join(REPO, "assets", "fibre-analyser.jpg")
OUT = r"C:\Users\Devastotra Poddar\Downloads\BOOST_Training_Flyer_Alumni.pdf"

# ---------- pre-process instrument photos to identical canvas ----------
def normalize_photo(src_path, dst_path, canvas_w=600, canvas_h=420, bg=(255,255,255)):
    """Letterbox-fit src into canvas_w x canvas_h white canvas."""
    try:
        from PIL import Image as PILImage
    except ImportError:
        return src_path  # fallback, no normalization
    if not os.path.exists(src_path):
        return None
    img = PILImage.open(src_path).convert("RGB")
    iw, ih = img.size
    scale = min(canvas_w / iw, canvas_h / ih)
    new_w, new_h = int(iw * scale), int(ih * scale)
    img = img.resize((new_w, new_h), PILImage.LANCZOS)
    canvas_img = PILImage.new("RGB", (canvas_w, canvas_h), bg)
    canvas_img.paste(img, ((canvas_w - new_w) // 2, (canvas_h - new_h) // 2))
    canvas_img.save(dst_path, "JPEG", quality=90)
    return dst_path

INST_KJ = normalize_photo(INST_KJ_RAW, os.path.join(REPO, "assets", "_inst_kj.jpg"))
INST_FAT = normalize_photo(INST_FAT_RAW, os.path.join(REPO, "assets", "_inst_fat.jpg"))
INST_FIB = normalize_photo(INST_FIB_RAW, os.path.join(REPO, "assets", "_inst_fib.jpg"))

# Palette
ORANGE = colors.HexColor("#B8732A")
ORANGE_DARK = colors.HexColor("#8A4F15")
ORANGE_LIGHT = colors.HexColor("#F4D8B6")
CREAM = colors.HexColor("#FAF2E7")
INK = colors.HexColor("#1F1A14")
INK_DIM = colors.HexColor("#5C4F3E")
DARK_PANEL = colors.HexColor("#1F2A22")  # deep green-black for "trainers" panel
LINE = colors.HexColor("#E5D5BA")
WHITE = colors.white

PAGE_W, PAGE_H = A4
MX = 0  # full-bleed layout: padding handled inside cells

# ---------- background ----------
def draw_background(canv, doc):
    canv.saveState()
    canv.setFillColor(WHITE)
    canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canv.restoreState()

# ---------- styles ----------
ss = getSampleStyleSheet()

s_logo = ParagraphStyle(
    "logo", fontName="Helvetica-Bold", fontSize=12, leading=14,
    textColor=ORANGE_DARK,
)
s_logo_sub = ParagraphStyle(
    "logo_sub", fontName="Helvetica", fontSize=7.5, leading=10,
    textColor=INK_DIM,
)

s_hero_h = ParagraphStyle(
    "hero_h", fontName="Times-Bold", fontSize=21, leading=24,
    textColor=WHITE, spaceAfter=5,
)
s_hero_h_em = ParagraphStyle(
    "hero_h_em", fontName="Times-BoldItalic", fontSize=21, leading=24,
    textColor=ORANGE_LIGHT,
)
s_hero_body = ParagraphStyle(
    "hero_body", fontName="Helvetica", fontSize=7.8, leading=10.2,
    textColor=WHITE, spaceAfter=2, alignment=4,
)

s_section_label = ParagraphStyle(
    "sec_label", fontName="Helvetica-Bold", fontSize=10, leading=12,
    textColor=ORANGE_DARK, spaceAfter=2,
)
s_section_h = ParagraphStyle(
    "sec_h", fontName="Times-Bold", fontSize=18, leading=22,
    textColor=INK, spaceAfter=10,
)

s_svc_title = ParagraphStyle(
    "svc_title", fontName="Helvetica-Bold", fontSize=9.8, leading=12,
    textColor=INK, spaceAfter=2,
)
s_svc_title_accent = ParagraphStyle(
    "svc_title_accent", fontName="Helvetica-Bold", fontSize=9.8, leading=12,
    textColor=ORANGE_DARK,
)
s_svc_body = ParagraphStyle(
    "svc_body", fontName="Helvetica", fontSize=7.4, leading=9.4,
    textColor=INK_DIM, alignment=4,
)

s_panel_label = ParagraphStyle(
    "panel_label", fontName="Helvetica-Bold", fontSize=8.8, leading=10.5,
    textColor=ORANGE_LIGHT, spaceAfter=3,
)
s_panel_h = ParagraphStyle(
    "panel_h", fontName="Times-Bold", fontSize=16, leading=19,
    textColor=WHITE, spaceAfter=5,
)
s_panel_body = ParagraphStyle(
    "panel_body", fontName="Helvetica", fontSize=7.4, leading=9.8,
    textColor=colors.HexColor("#D8D2C5"), alignment=4, spaceAfter=3,
)
s_panel_name = ParagraphStyle(
    "panel_name", fontName="Times-Bold", fontSize=10, leading=12,
    textColor=WHITE, spaceAfter=1,
)
s_panel_role = ParagraphStyle(
    "panel_role", fontName="Helvetica-Bold", fontSize=7.4, leading=9.2,
    textColor=ORANGE_LIGHT, spaceAfter=3,
)

s_call_meta = ParagraphStyle(
    "call_meta", fontName="Helvetica-Bold", fontSize=8.2, leading=11,
    textColor=ORANGE_LIGHT, spaceAfter=2,
)
s_call_big = ParagraphStyle(
    "call_big", fontName="Helvetica-Bold", fontSize=14, leading=17,
    textColor=WHITE,
)

s_strip_label = ParagraphStyle(
    "strip_label", fontName="Helvetica-Bold", fontSize=8, leading=10,
    textColor=ORANGE_LIGHT,
)
s_strip_val = ParagraphStyle(
    "strip_val", fontName="Helvetica", fontSize=7.8, leading=10,
    textColor=WHITE,
)

s_quote = ParagraphStyle(
    "quote", fontName="Times-Italic", fontSize=7.2, leading=9,
    textColor=INK_DIM, alignment=1, spaceBefore=2,
)

# ---------- icon helpers (drawn vector boxes with letter glyphs) ----------
def icon_cell(letter, color=ORANGE):
    """Small colored square with a serif letter, used as service icon."""
    p = Paragraph(
        f'<font color="white"><b>{letter}</b></font>',
        ParagraphStyle("ic", fontName="Times-Bold", fontSize=14, leading=16,
                       alignment=1, textColor=WHITE)
    )
    t = Table([[p]], colWidths=[10 * mm], rowHeights=[10 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t

# ---------- build ----------
def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
        title="BOOST Training Flyer for Belda College Alumni - Learning Reunion",
        author="Department of Nutrition, Belda College",
    )
    frame = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0, showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="flyer", frames=[frame], onPage=draw_background)])

    flow = []

    # ============= TOP STRIP =============
    # Real Belda College logo (downloaded from beldacollege.ac.in)
    if os.path.exists(LOGO_IMG):
        try:
            logo_img = RLImage(LOGO_IMG, width=14 * mm, height=14 * mm, kind="proportional")
        except Exception:
            logo_img = icon_cell("B", ORANGE)
    else:
        logo_img = icon_cell("B", ORANGE)

    logo_cell = Table([
        [logo_img, [
            Paragraph("BELDA COLLEGE", s_logo),
            Paragraph("Department of Nutrition", s_logo_sub),
        ]]
    ], colWidths=[16 * mm, None])
    logo_cell.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    top_meta = Paragraph(
        '<font color="#8A4F15"><b>WBDSTBT BOOST PROGRAMME</b></font>'
        '<br/><font size=8 color="#5C4F3E">in collaboration with Borosil Scientific</font>',
        ParagraphStyle("topm", fontName="Helvetica", fontSize=9.5, leading=12,
                       alignment=2)
    )
    top_strip = Table(
        [[logo_cell, top_meta]],
        colWidths=[PAGE_W * 0.55, PAGE_W * 0.45],
    )
    top_strip.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    flow.append(top_strip)

    # ============= HERO ROW (orange text panel | photo) =============
    hero_text = [
        Paragraph(
            'Come Back to <i><font color="#F4D8B6">Learn.</font></i> '
            'Stay to <i><font color="#F4D8B6">Reconnect.</font></i>',
            s_hero_h
        ),
        Spacer(1, 4),
        Paragraph(
            "A two-day Learning &amp; Reunion get-together for Belda College alumni. "
            "Hands-on training on Kjeldahl protein, Soxhlet fat extraction and dietary "
            "fibre estimation, on the new BOOST instruments your seniors never had.",
            s_hero_body
        ),
    ]
    hero_text_fit = KeepInFrame(
        PAGE_W * 0.5 - 32,
        58 * mm - 22,
        hero_text,
        mode="shrink",
        vAlign="MIDDLE",
    )
    hero_text_tbl = Table([[hero_text_fit]], colWidths=[PAGE_W * 0.5], rowHeights=[58 * mm])
    hero_text_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ORANGE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))

    # Hero image (right) — fall back to solid orange-tinted block if missing
    if os.path.exists(HERO_IMG):
        try:
            img = RLImage(HERO_IMG, width=PAGE_W * 0.5, height=58 * mm, kind="proportional")
            img.hAlign = "CENTER"
            hero_img_cell = img
        except Exception:
            hero_img_cell = Paragraph("", s_hero_body)
    else:
        hero_img_cell = Paragraph("", s_hero_body)

    hero_row = Table(
        [[hero_text_tbl, hero_img_cell]],
        colWidths=[PAGE_W * 0.5, PAGE_W * 0.5],
        rowHeights=[58 * mm],
    )
    hero_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("BACKGROUND", (1, 0), (1, 0), ORANGE_LIGHT),
    ]))
    flow.append(hero_row)

    # ============= DATE BAND =============
    date_band = Table(
        [[Paragraph(
            '<font color="white"><b>&#128197; 19-20 May 2026</b> &#160;&#160; '
            '&#128338; 10:00 to 17:00 IST &#160;&#160; '
            '&#128205; Belda College, Paschim Medinipur &#160;&#160; '
            '&#127891; 30 alumni seats &#160;&#160; '
            '&#128176; Rs 200</font>',
            ParagraphStyle("db", fontName="Helvetica", fontSize=10, leading=13,
                           alignment=1)
        )]],
        colWidths=[PAGE_W],
    )
    date_band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ORANGE_DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    flow.append(date_band)

    # ============= ID REQUIREMENT BAND (cream, prominent) =============
    id_band = Table(
        [[Paragraph(
            '<font color="#8A4F15"><b>&#128737; BRING ON DAY 1</b></font> &#160;&#8212;&#160; '
            '<font color="#1F1A14">Alumni ID card &#160;<b>OR</b>&#160; UG / PG passing certificate &#160;<b>OR</b>&#160; '
            'final-year mark sheet, for verification at the Department of Nutrition gate.</font>',
            ParagraphStyle("idb", fontName="Helvetica", fontSize=8.6, leading=11,
                           alignment=1)
        )]],
        colWidths=[PAGE_W],
    )
    id_band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ORANGE_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.6, ORANGE),
    ]))
    flow.append(id_band)

    # ============= MIDDLE: WHAT YOU GAIN  +  WHO TEACHES =============
    # Left: 3 student deliverables
    svc_rows = []
    items = [
        ("1", "Bench skills for", "your current role",
         "Whether you teach, do PG / PhD, work in food industry, FSSAI / NABL labs, NGOs or are preparing for NET-JRF, GATE, FCI and FSSAI exams - two days on the bench fixes the methods permanently."),
        ("2", "Reunion with", "your Department",
         "Same corridor, same teachers, same lab-coat smell. Catch up with batchmates over chai, walk through the renovated lab, see what the Department has become."),
        ("3", "Certificate from", "Borosil Scientific",
         "An industry-issued credential for your CV, your appraisal file, your PG / PhD application, or your audit-floor wall - not just a college token."),
    ]
    for num, t1, t2, body in items:
        ic = icon_cell(num, ORANGE)
        text = [
            Paragraph(f"{t1} <font color='#B8732A'>{t2}</font>", s_svc_title),
            Paragraph(body, s_svc_body),
        ]
        row = Table([[ic, text]], colWidths=[12 * mm, None])
        row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LINEBELOW", (1, 0), (1, 0), 0.3, LINE),
        ]))
        svc_rows.append([row])

    services_block = [
        Paragraph("OUR <font color='#B8732A'>PROGRAMME</font>", ParagraphStyle(
            "svh", fontName="Helvetica-Bold", fontSize=12, leading=14,
            textColor=INK, spaceAfter=2,
        )),
        Table([[None]], colWidths=[40 * mm], rowHeights=[2],
              style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), ORANGE)])),
        Spacer(1, 5),
    ]
    for r in svc_rows:
        services_block.extend(r)

    # (instrument cards now live in a full-width strip below the middle row)

    inst_name_style = ParagraphStyle(
        "inst_name", fontName="Times-Bold", fontSize=11, leading=13,
        textColor=WHITE, alignment=1, spaceAfter=2,
    )
    inst_tag_style = ParagraphStyle(
        "inst_tag", fontName="Helvetica-Bold", fontSize=7.2, leading=9.5,
        textColor=ORANGE_LIGHT, alignment=1, spaceAfter=4,
    )
    inst_body_style = ParagraphStyle(
        "inst_body", fontName="Helvetica", fontSize=7.6, leading=10,
        textColor=WHITE, alignment=1,
    )

    # Full-width strip BELOW middle row → 3 wide cards
    INST_AVAIL_W = PAGE_W - 28              # global left/right padding
    CARD_W = INST_AVAIL_W / 3
    PHOTO_W = CARD_W - 14
    PHOTO_H = PHOTO_W * 0.42                # shallow enough to keep footer on page 1

    def inst_card(img_path, name, role, body):
        if img_path and os.path.exists(img_path):
            try:
                img = RLImage(img_path, width=PHOTO_W, height=PHOTO_H)
                img.hAlign = "CENTER"
            except Exception:
                img = Paragraph("", inst_body_style)
        else:
            img = Paragraph("", inst_body_style)
        return [
            img,
            Spacer(1, 4),
            Paragraph(name, ParagraphStyle(
                "ipn", fontName="Times-Bold", fontSize=10, leading=12,
                textColor=INK, alignment=1, spaceAfter=1
            )),
            Paragraph(role, ParagraphStyle(
                "ipt", fontName="Helvetica-Bold", fontSize=7.2, leading=9.5,
                textColor=ORANGE_DARK, alignment=1, spaceAfter=3
            )),
            Paragraph(body, ParagraphStyle(
                "ipb", fontName="Helvetica", fontSize=7.4, leading=10,
                textColor=INK_DIM, alignment=1
            )),
        ]

    cards = [[
        inst_card(INST_KJ, "Kjeldahl Magnus", "DAY 1 &middot; PROTEIN NITROGEN",
                  "Smart, in-built application library. Touchscreen, auto steam generation and titration."),
        inst_card(INST_FAT, "Fat Analyser, Randall", "DAY 2 &middot; FAT EXTRACTION",
                  "Six-station automated extraction. Boil, rinse, recover solvent. Reproducible &plusmn;0.1% RSD."),
        inst_card(INST_FIB, "Rapid Fibre Analyser", "DAY 2 &middot; DIETARY FIBRE",
                  "Fibre Bag protocol, no filtration losses. AOAC 991.43 compatible. Six-position digestion."),
    ]]
    cards_tbl = Table(cards, colWidths=[CARD_W, CARD_W, CARD_W])
    cards_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("BOX", (0, 0), (0, 0), 0.6, LINE),
        ("BOX", (1, 0), (1, 0), 0.6, LINE),
        ("BOX", (2, 0), (2, 0), 0.6, LINE),
        ("LINEBELOW", (0, 0), (0, 0), 2.5, ORANGE),
        ("LINEBELOW", (1, 0), (1, 0), 2.5, colors.HexColor("#6c8c5c")),
        ("LINEBELOW", (2, 0), (2, 0), 2.5, ORANGE_DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    # Wrap the strip in a paddable table so it has page side-padding
    inst_strip = Table(
        [[Paragraph("THREE INSTRUMENTS YOU WILL <font color='#B8732A'>RUN</font>",
                    ParagraphStyle("inst_h", fontName="Helvetica-Bold", fontSize=10, leading=12,
                                   textColor=INK, alignment=0, spaceAfter=4))],
         [cards_tbl]],
        colWidths=[PAGE_W - 28],
    )
    inst_strip.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (0, 0), 3),
        ("BOTTOMPADDING", (0, 0), (0, 0), 2),
        ("TOPPADDING", (0, 1), (0, 1), 0),
        ("BOTTOMPADDING", (0, 1), (0, 1), 0),
    ]))
    inst_strip_wrap = Table([[inst_strip]], colWidths=[PAGE_W])
    inst_strip_wrap.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
    ]))

    # Right: dark "WHO TEACHES" panel with trainer profiles
    panel_inner = [
        Paragraph("WHO <font color='#F4D8B6'>TEACHES YOU</font>", s_panel_label),
        Paragraph("Industry experts, not slides", s_panel_h),
        Paragraph(
            "Belda College alumni go on to teach, audit, research and run labs across India. These are the two people you would most want standing next to you when you finally run a Kjeldahl or a dietary fibre cycle yourself.",
            s_panel_body
        ),
        Spacer(1, 6),
        Paragraph("Mr Sanjay Bhalke", s_panel_name),
        Paragraph("National Sales Manager (Instrumentation), Borosil Scientific", s_panel_role),
        Paragraph(
            "More than two decades commissioning, validating and troubleshooting Kjeldahl, Soxhlet and dietary fibre platforms across academic, regulatory and industry laboratories. Will show you the interview questions food companies actually ask about these methods.",
            s_panel_body
        ),
        Spacer(1, 8),
        Paragraph("Mr Vaithilingam", s_panel_name),
        Paragraph("Senior Product Manager, Borosil Scientific", s_panel_role),
        Paragraph(
            "Technical authority behind Magnus, Soxtron and DFA-50 lines. Method development, AOAC compliance audits, liaison with Indian and international standards bodies. Will answer 'why this exact temperature ramp' from the chemistry up, the way it would land in a viva.",
            s_panel_body
        ),
        Spacer(1, 10),
        # bottom CTA strip inside dark panel — fills lower whitespace + reinforces the offer
        Table(
            [[Paragraph(
                "<font color='#F4D8B6'><b>SAME DEPARTMENT.</b></font> "
                "<font color='white'>NEW BENCHES.</font> "
                "<font color='#F4D8B6'><b>BOROSIL CERTIFICATE.</b></font>",
                ParagraphStyle("panel_cta", fontName="Helvetica-Bold", fontSize=9, leading=12,
                               textColor=WHITE, alignment=1)
            )]],
            colWidths=[None],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#2A3A30")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEABOVE", (0, 0), (-1, -1), 0.6, ORANGE),
                ("LINEBELOW", (0, 0), (-1, -1), 0.6, ORANGE),
            ]),
        ),
    ]
    panel_tbl = Table([[panel_inner]], colWidths=[None])
    panel_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_PANEL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    middle_row = Table(
        [[services_block, panel_tbl]],
        colWidths=[PAGE_W * 0.55, PAGE_W * 0.45],
    )
    middle_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 18),
        ("RIGHTPADDING", (0, 0), (0, 0), 8),
        ("TOPPADDING", (0, 0), (0, 0), 9),
        ("BOTTOMPADDING", (0, 0), (0, 0), 9),
        ("LEFTPADDING", (1, 0), (1, 0), 0),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (1, 0), (1, 0), 0),
        ("BOTTOMPADDING", (1, 0), (1, 0), 0),
        # extend dark colour across the whole right cell so no white gap below the trainer panel
        ("BACKGROUND", (1, 0), (1, 0), DARK_PANEL),
    ]))
    flow.append(middle_row)

    # ============= INSTRUMENT CARDS STRIP (full-width) =============
    flow.append(inst_strip_wrap)

    # ============= CONTACT STRIP =============
    s_strip_val_link = ParagraphStyle(
        "strip_val_link", parent=s_strip_val,
        fontName="Helvetica-Bold", textColor=WHITE,
        underlineWidth=0.6, underlineOffset=-2,
    )
    contact_left = [
        Paragraph(
            "&#128231; &#160; <b>EMAIL</b>",
            ParagraphStyle("cl", fontName="Helvetica-Bold", fontSize=7.8, leading=10,
                           textColor=ORANGE_LIGHT)
        ),
        Paragraph(
            '<link href="mailto:devastotrapoddar@beldacollege.ac.in" color="white"><u>devastotrapoddar@beldacollege.ac.in</u></link>',
            s_strip_val_link
        ),
    ]
    contact_mid = [
        Paragraph(
            "&#128241; &#160; <b>PHONE</b>",
            ParagraphStyle("cm", fontName="Helvetica-Bold", fontSize=7.8, leading=10,
                           textColor=ORANGE_LIGHT)
        ),
        Paragraph(
            '<link href="tel:+918337054946" color="white"><u>+91 83370 54946</u></link>',
            s_strip_val_link
        ),
    ]
    contact_right = [
        Paragraph(
            "&#128279; &#160; <b>REGISTER ONLINE</b>",
            ParagraphStyle("cr", fontName="Helvetica-Bold", fontSize=7.8, leading=10,
                           textColor=ORANGE_LIGHT)
        ),
        Paragraph(
            '<link href="https://devastotra-stack.github.io/boost-training-reg-alumni/" color="white"><u>devastotra-stack.github.io/boost-training-reg-alumni/</u></link>',
            s_strip_val_link
        ),
    ]
    contact = Table(
        [[contact_left, contact_mid, contact_right]],
        colWidths=[PAGE_W / 3] * 3,
    )
    contact.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ORANGE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEAFTER", (0, 0), (1, 0), 0.5, ORANGE_LIGHT),
    ]))
    flow.append(contact)

    # ============= FOOTER QUOTE STRIP =============
    quote = Table(
        [[Paragraph(
            '"You leave the same Department you walked out of years ago - but this time, with bench skills '
            'your seniors never had, and a Borosil-issued certificate in hand." &#160;&#160;'
            '<font color="#B8732A">&#8226;</font>&#160;&#160; Carry your alumni ID, passing certificate or final-year mark sheet on Day 1 &#160;&#160;'
            '<font color="#B8732A">&#8226;</font>&#160;&#160; Certificate issued by Borosil Scientific',
            s_quote)]],
        colWidths=[PAGE_W],
    )
    quote.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    flow.append(quote)

    doc.build(flow)
    print(f"Wrote: {OUT}")

if __name__ == "__main__":
    build()
