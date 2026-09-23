"""Build the single public CV and publication record.

Run from the repository root with Python and ReportLab installed:
    python scripts/build_cv.py

The conference list is maintained in cv/conferences.txt. Professional contact
details only: the supplied private home address and mobile number are omitted.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "Katrin-Merfeld-CV-and-Publications.pdf"
PAPER = colors.HexColor("#FAF9F5")
INK = colors.HexColor("#20201E")
MUTED = colors.HexColor("#60605C")
RULE = colors.HexColor("#CFCFC9")
YELLOW = colors.HexColor("#FFCD00")
W, H = A4

FONT_DIR = Path("C:/Windows/Fonts")
if all((FONT_DIR / name).exists() for name in ("georgia.ttf", "georgiab.ttf", "arial.ttf", "arialbd.ttf")):
    font_files = (FONT_DIR / "georgia.ttf", FONT_DIR / "georgiab.ttf", FONT_DIR / "arial.ttf", FONT_DIR / "arialbd.ttf")
else:
    # ReportLab's bundled Vera font keeps the build portable after a fork.
    fallback = Path(rl_config.__file__).parent / "fonts"
    font_files = (fallback / "Vera.ttf", fallback / "VeraBd.ttf", fallback / "Vera.ttf", fallback / "VeraBd.ttf")
for font_name, font_file in zip(("Georgia", "Georgia-Bold", "Arial", "Arial-Bold"), font_files):
    pdfmetrics.registerFont(TTFont(font_name, str(font_file)))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")

styles = {
    "eyebrow": ParagraphStyle("eyebrow", fontName="Arial-Bold", fontSize=8.5, leading=12, textColor=MUTED, spaceAfter=10, tracking=1.5),
    "title": ParagraphStyle("title", fontName="Georgia", fontSize=38, leading=43, textColor=INK, spaceAfter=5),
    "subtitle": ParagraphStyle("subtitle", fontName="Arial", fontSize=12.2, leading=17, textColor=MUTED, spaceAfter=21),
    "section": ParagraphStyle("section", fontName="Georgia", fontSize=18, leading=23, textColor=INK, spaceBefore=20, spaceAfter=9),
    "subsection": ParagraphStyle("subsection", fontName="Arial-Bold", fontSize=9.7, leading=13, textColor=INK, spaceBefore=14, spaceAfter=6, keepWithNext=1),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=9.4, leading=14, textColor=INK, spaceAfter=7),
    "small": ParagraphStyle("small", fontName="Arial", fontSize=8.7, leading=12.5, textColor=INK, spaceAfter=5),
    "muted": ParagraphStyle("muted", fontName="Arial", fontSize=8.2, leading=12, textColor=MUTED, spaceAfter=7),
    "date": ParagraphStyle("date", fontName="Arial-Bold", fontSize=8.5, leading=12, textColor=MUTED),
    "pub": ParagraphStyle("pub", fontName="Arial", fontSize=9, leading=13.2, textColor=INK, leftIndent=12, firstLineIndent=-12, spaceAfter=8),
    "conference": ParagraphStyle("conference", fontName="Arial", fontSize=8.2, leading=10.8, textColor=INK, leftIndent=11, firstLineIndent=-11, spaceAfter=1.2),
}


def p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, styles[style])


def plain(text: str, style: str = "body") -> Paragraph:
    return p(escape(text), style)


def section(title: str):
    return [p(escape(title), "section"), HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=12)]


def timeline(items):
    rows = [[p(escape(date), "date"), p(escape(description), "small")] for date, description in items]
    table = Table(rows, colWidths=[87, 404], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 12),
        ("RIGHTPADDING", (1, 0), (1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(YELLOW)
    canvas.rect(0, H - 9, W, 9, fill=1, stroke=0)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(52, 48, W - 52, 48)
    canvas.setFont("Arial-Bold", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(52, 34, "KATRIN MERFELD  /  ACADEMIC CV & PUBLICATIONS")
    canvas.drawRightString(W - 52, 34, f"{doc.page:02d}")
    canvas.restoreState()


JOURNAL = [
    (2025, "Merfeld, K., Klein, J. F., de Regt, A., Baltin (née Riegger), A. S., & Henkel, S. In-store technology personalization: A typology and research agenda based on type of automation and data collection. Journal of Business Research, 191, 115236."),
    (2025, "Benoit, S., Merfeld, K., Tunn, V. S. C., Schaefers, T., & Andreassen, T. W. The B2B sharing economy: Framework, implications, and future research. Journal of Business Research, 191, 115244."),
    (2025, "Schwarzmann, V., Merfeld, K., & Kreutzer, K. Navigating age diversity in volunteer teams: Barriers and enablers of teamwork. Nonprofit and Voluntary Sector Quarterly, 54(3), 547-582."),
    (2025, "Oetken, K. J., Hennig, K., Henkel, S., & Merfeld, K. A psychoanalytical approach in urban design: Exploring dynamics of co-creation through theme-centred interaction. Journal of Urban Design, 30(4), 445-472."),
    (2024, "Perera, C., Toxopeus, H., Klein, S., & Merfeld, K. Enabling justice for nature-based solutions in real estate development. Nature-Based Solutions, 6, 100148."),
    (2024, "Fitschen, P., Merfeld, K., Klein, J. F., & Henkel, S. Understanding the urban mobility challenge: Why shared mobility providers fail to attract car drivers. Transport Policy, 158, 104-111."),
    (2024, "Terpoorten, C., Klein, J. F., & Merfeld, K. Understanding B2B customer journeys for complex digital services: The case of cloud computing. Industrial Marketing Management, 119, 178-192."),
    (2024, "de Jong, J. P. J., Mulhuijzen, M., Merfeld, K., Rigtering, C., van Balen, T., & Boënne, M. Industrial product development with lead users as a source of Schumpeterian opportunity. Journal of Product Innovation Management, 41(6), 1165-1183."),
    (2024, "Großmann, C., Merfeld, K., Klein, J. F., Föller, F., & Henkel, S. Onto the light side of sharing: Using the force of blockchain. Journal of Business Research, 175, 114507."),
    (2023, "Timmer, S., Merfeld, K., & Henkel, S. Exploring motivations for multimodal commuting: A hierarchical means-end chain analysis. Transportation Research Part A: Policy and Practice, 176, 103831."),
    (2022, "Riegger, A. S., Merfeld, K., Klein, J. F., & Henkel, S. Technology-enabled personalization: Impact of smart technology choice on consumer shopping behavior. Technological Forecasting and Social Change, 181, 121752."),
    (2022, "Klein, J. F., Merfeld, K., Wilhelms, M. P., Falk, T., & Henkel, S. Buying to share: How prosumption promotes purchases in peer-to-peer asset sharing. Journal of Business Research, 143, 171-183."),
    (2021, "Riegger, A. S., Klein, J. F., Merfeld, K., & Henkel, S. Technology-enabled personalization in retail stores: Understanding drivers and barriers. Journal of Business Research, 123, 140-155."),
    (2020, "Lehr, A., Buettgen, M., Benoit, S., & Merfeld, K. Spillover effects from unintended trials on attitude and behavior: Promoting new products through access-based services. Psychology & Marketing, 37(5), 705-723."),
    (2019, "Merfeld, K., Wilhelms, M. P., & Henkel, S. Being driven autonomously: A qualitative study to elicit consumers' overarching motivational structures. Transportation Research Part C: Emerging Technologies, 107, 229-247."),
    (2019, "Merfeld, K., Wilhelms, M. P., Henkel, S., & Kreutzer, K. Carsharing with shared autonomous vehicles: Uncovering drivers, barriers and future developments - A four-stage Delphi study. Technological Forecasting and Social Change, 144, 66-81."),
    (2017, "Wilhelms, M. P., Merfeld, K., & Henkel, S. Yours, mine, and ours: A user-centric analysis of opportunities and challenges in peer-to-peer asset sharing. Business Horizons, 60(6), 771-781."),
]

OTHER_WORK = [
    "Bulkeley, H., Lacambra, C., Barnwal, A., Blackwatters, J. J., Callenberg, M., Demonsant, C., Fransen, A., Jeong, J., Kinniburgh, F., Lillquist, J., Maia, S., Merfeld, K., & Toxopeus, H. (2026). Integration, Financing and Just Transition for Urban Sustainability. The British Academy. Research report.",
    "Toxopeus, H., & Merfeld, K. (2023). Exploring business models for sustainability with nature as a key resource: A case study of urban nature-based solutions. SSRN working paper.",
    "Merfeld, K. (2018). Shared and autonomous: A market perspective on contemporary mobility. Doctoral dissertation.",
    "Wilhelms, M. P., Henkel, S., & Merfeld, K. (2017). You are what you share: Understanding participation motives in peer-to-peer carsharing. In Disrupting Mobility: Impacts of Sharing Economy and Innovative Transportation on Cities (pp. 105-119). Springer.",
]


def build():
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=52, rightMargin=52,
        topMargin=51, bottomMargin=67, title="Katrin Merfeld | Academic CV and Publications",
        author="Katrin Merfeld", subject="Academic curriculum vitae and publications",
    )
    story = []
    story += [p("ACADEMIC CV  /  SEPTEMBER 2026", "eyebrow"), p("Katrin Merfeld", "title"), p("Associate Professor · Utrecht University School of Economics", "subtitle")]
    story += [HRFlowable(width="100%", thickness=2, color=INK, spaceAfter=13)]
    story += [p("<b>Research:</b> Sustainability marketing · nature-based solutions · sharing economies · consumer behaviour", "small")]
    story += [p('<b>Contact:</b> <link href="mailto:k.merfeld@uu.nl" color="#20201E">k.merfeld@uu.nl</link> · <link href="https://www.uu.nl/staff/KMerfeld" color="#20201E">uu.nl/staff/KMerfeld</link> · Utrecht, The Netherlands', "small")]

    story += section("Appointments")
    story += [timeline([
        ("2025-present", "Associate Professor, Marketing & Business Development, Utrecht University School of Economics"),
        ("2020-2025", "Assistant Professor, Marketing & Business Development, Utrecht University School of Economics"),
        ("2018-2020", "Postdoctoral Researcher, EBS University"),
        ("2015-2018", "Research Assistant, EBS University"),
    ])]
    story += section("Education")
    story += [timeline([
        ("Since 2023", "Habilitation research, EBS University, Wiesbaden"),
        ("2015-2018", "Dr. rer. pol., summa cum laude, EBS University; dissertation in consumer behaviour"),
        ("2014-2016", "Diplôme du Programme Grande École, KEDGE Business School, Bordeaux"),
        ("2013-2015", "MSc Marketing, EBS University"),
        ("2010-2013", "BSc Business Administration, University of Mannheim"),
    ])]
    story += section("Research and teaching")
    story += [plain("Research spans sustainability marketing, the value and communication of urban nature, sharing and mobility, technology-enabled services, and alternative modes of consumption. Current European projects include NATURESCAPES and ClimEx-PE.")]
    story += [plain("Programme coordinator for the MSc Business and Social Impact. Master's teaching includes Sustainability Marketing and Platform Economy & Business.")]

    story += section("Funding and recognition")
    story += [p("<b>Major collaborative grants</b>", "subsection")]
    story += [plain("Principal investigator, NWO Water4All / ClimEx-PE (approximately EUR 270,000 to USE). Work package co-lead, Horizon Europe / NATURESCAPES (approximately EUR 6.5 million total; EUR 560,000 to USE).", "small")]
    story += [p("<b>Additional grants</b>", "subsection")]
    story += [timeline([
        ("2023", "REBO USE Teaching Innovation Grant, Sustainability Marketing Challenge; REBO USO Teaching Innovation Grant, Alumni Network"),
        ("2022", "EWUU Alliance Grant, Circular and Socially Inclusive Real Estate; Pathways to Sustainability funding for NATURICITY and Sharing Paradoxes"),
        ("2021", "REBO USO grants for Workboost and the BSI Challenge; EWUU Alliance Grant for platforms for urban nature-based solutions"),
    ])]
    story += [plain("EBS Upcoming Scholar Award (2020); SRH Social Impact Thesis Award (2018).", "small")]

    story += section("Academic service and supervision")
    story += [plain("Editorial board member, Humanities & Social Sciences Communications. Reviewer for Journal of Business Research, Journal of Service Research, Journal of Retailing and Consumer Services, Organization & Environment, Psychology & Marketing, Technological Forecasting and Social Change, and Transportation Research Parts A and C, among others.", "small")]
    story += [plain("PhD supervision: Anne-Sophie Riegger, Christopher Großmann, Max Mulhuijzen, Philip Fitschen, Vera Schwarzmann, Fahim Schaffi, Jihwan Ryu, and Madeleine Neumann. Postdoctoral mentoring: Charlotte Demosant and Jessica Lillquist.", "small")]
    story += [p("<b>Languages:</b> German (native), English (C2), Dutch (B2), French (A2), Spanish (A1), Latin (Latinum).", "small")]

    story += section("Seminars and knowledge exchange")
    story += [timeline([
        ("2025", "Urban NBS Day on law and nature-based solutions; presentation on business models for nature-based solutions at the Presencing Institute; collaboration with the German World Shops"),
        ("2024", "Urban NBS Day on health and nature-based solutions; NATURESCAPES fieldwork and stakeholder workshops; NATURESCAPES Collaboratory meetings"),
        ("2023", "Urban NBS Day on inclusivity in real estate, Dutch Design Week exhibition, and presentations on nature-based solutions and sustainable business models"),
        ("2022", "Workshops with UNICEF Germany and German World Shops; Urban NBS Day on co-financing and digitalisation for nature-based solutions"),
        ("2021", "Research seminars at EBS University, Utrecht University, and the University of Surrey; presentation to the Global Alliance for Banking on Values / MIT Community Innovators Lab"),
    ])]

    story += [PageBreak(), p("PUBLICATION RECORD  /  JOURNAL ARTICLES", "eyebrow"), p("Publications", "title"), p("Peer-reviewed articles and other scholarly work", "subtitle")]
    story += [HRFlowable(width="100%", thickness=2, color=INK, spaceAfter=15)]
    current_year = None
    for year, citation in JOURNAL:
        if year != current_year:
            current_year = year
            story.append(p(str(year), "subsection"))
        story.append(plain(citation, "pub"))

    story += section("Reports, books and working papers")
    story += [plain(citation, "pub") for citation in OTHER_WORK]

    story += section("Conference presentations")
    conference_text = (ROOT / "cv" / "conferences.txt").read_text(encoding="utf-8")
    conference_entries = [x.strip() for x in conference_text.split("\n\n") if x.strip()]
    for item in conference_entries:
        story.append(plain(item, "conference"))

    OUTPUT.parent.mkdir(exist_ok=True)
    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    print(f"Created {OUTPUT}")
    print(f"Journal articles: {len(JOURNAL)}; conference presentations: {len(conference_entries)}")


if __name__ == "__main__":
    build()
