"""Generates the three supporting attachments from the shared data model.

House rules enforced here, from the project's poor-quality-artifact guidance:
no "AI blue" palette, no italic subheadings or footers, no confidentiality
notices, no mention of the project, and no input file that names another input
file. Filename conventions deliberately differ between files, because in a real
network they are produced by four different systems.
"""
import csv
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle)
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side

from model import SPEC, otdr_events, ont_rows

BLACK = colors.black
GREY = colors.HexColor("#4a4a4a")
BAND = colors.HexColor("#e6e6e6")
RULE = colors.HexColor("#8c8c8c")

# ======================================================= 1. loss budget standard
doc = SimpleDocTemplate("attachments/OSP-207_RevD_Optical_Loss_Budget.pdf",
                        pagesize=LETTER, topMargin=0.8*inch, bottomMargin=0.8*inch,
                        leftMargin=0.9*inch, rightMargin=0.9*inch,
                        title="OSP-207 Rev D — Optical Loss Budget Standard",
                        author="Outside Plant Engineering")
ss = getSampleStyleSheet()
title = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold",
                       fontSize=15, textColor=BLACK, spaceAfter=2, leading=19)
docline = ParagraphStyle("d", parent=ss["Normal"], fontName="Helvetica",
                         fontSize=9.5, textColor=GREY, spaceAfter=14)
h2 = ParagraphStyle("h2", parent=ss["Normal"], fontName="Helvetica-Bold",
                    fontSize=11, textColor=BLACK, spaceBefore=15, spaceAfter=6)
body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica",
                      fontSize=9.8, leading=14, textColor=BLACK)

def tbl(data, widths):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BAND),
        ("TEXTCOLOR", (0, 0), (-1, -1), BLACK),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.2),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t

S = [
    Paragraph("OPTICAL LOSS BUDGET STANDARD", title),
    Paragraph("Standard OSP-207&nbsp;&nbsp;|&nbsp;&nbsp;Revision D&nbsp;&nbsp;|&nbsp;&nbsp;"
              "Effective 2 March 2026&nbsp;&nbsp;|&nbsp;&nbsp;Owner: Outside Plant Engineering&nbsp;&nbsp;|&nbsp;&nbsp;"
              "Supersedes Revision C", docline),

    Paragraph("1. Scope", h2),
    Paragraph("This standard sets the component loss values and the received-power "
              "acceptance thresholds used to verify Gigabit Passive Optical Network (GPON) "
              "distribution plant. It applies at the 1490 nm downstream wavelength. All "
              "fibre in the access plant is ITU-T G.652.D single mode. Revision D restates "
              "the mechanical splice allowance, which was previously quoted as a range.", body),

    Paragraph("2. Component loss values", h2),
    Paragraph("These are design values. A component whose measured loss exceeds its design "
              "value is out of specification and shall be recorded as such.", body),
    Spacer(1, 7),
    tbl([
        ["Component", "Design loss", "Unit"],
        ["Single-mode fibre attenuation at 1490 nm", f"{SPEC['fiber_db_per_km']:.2f}", "dB per km"],
        ["Fusion splice", f"{SPEC['fusion_splice_db']:.2f}", "dB each"],
        ["Mechanical splice", f"{SPEC['mechanical_splice_db']:.2f}", "dB each"],
        ["Mated connector pair", f"{SPEC['connector_pair_db']:.2f}", "dB each"],
        ["1:8 optical splitter, insertion loss", f"{SPEC['splitter_1x8_db']:.2f}", "dB"],
        ["1:4 optical splitter, insertion loss", f"{SPEC['splitter_1x4_db']:.2f}", "dB"],
    ], [3.5*inch, 1.15*inch, 1.15*inch]),

    Paragraph("3. Transmit reference", h2),
    Paragraph(f"Optical line terminal (OLT) transmit power at the passive optical network "
              f"(PON) port is commissioned and held at <b>{SPEC['olt_tx_dbm']:+.2f} dBm</b>. "
              "End-to-end path loss is the difference between that transmit power and the "
              "power received at the optical network terminal (ONT).", body),

    Paragraph("4. Received-power acceptance thresholds", h2),
    Paragraph("Every in-service ONT is classified from its measured received power as set out "
              "below. Boundaries are inclusive as written.", body),
    Spacer(1, 7),
    tbl([
        ["Classification", "Measured ONT received power"],
        ["PASS", f"greater than or equal to {SPEC['pass_min_dbm']:.2f} dBm"],
        ["MARGINAL", f"below {SPEC['pass_min_dbm']:.2f} dBm and greater than or equal to "
                     f"{SPEC['fail_below_dbm']:.2f} dBm"],
        ["FAIL", f"below {SPEC['fail_below_dbm']:.2f} dBm"],
    ], [1.5*inch, 4.3*inch]),

    Paragraph("5. Measurement tolerance", h2),
    Paragraph(f"Power meters and optical time-domain reflectometers (OTDRs) in field service "
              f"carry a combined uncertainty of plus or minus {SPEC['tolerance_db']:.2f} dB. A "
              f"difference between measured loss and design loss of {SPEC['tolerance_db']:.2f} dB "
              "or less is therefore within tolerance and shall not be raised as a fault. A "
              f"difference greater than {SPEC['tolerance_db']:.2f} dB indicates excess loss that "
              "is physically present in the plant and shall be investigated.", body),

    Paragraph("6. OTDR test method for distribution legs", h2),
    Paragraph("A distribution leg is tested by shooting an OTDR from the fibre distribution hub "
              "(FDH) output port toward the multiport service terminal (MST). The trace datum, "
              "0.00 km, is the FDH output port. Because the MST houses a splitter, the trace "
              "terminates at the MST input connector: <b>it cannot see any fibre, connector or "
              "splice downstream of the MST, and that includes all subscriber drop cable.</b> "
              "Excess loss downstream of an MST is therefore invisible to this test and must be "
              "isolated from received-power measurements taken at the subscriber terminal.", body),

    Paragraph("7. Recording", h2),
    Paragraph("An event recorded by an OTDR is reported by its distance from the trace datum. "
              "The trace does not identify whether a splice is fusion or mechanical; that is "
              "established from the plant record for the leg concerned, and the design value "
              "appropriate to the splice type is the one that applies.", body),
]
doc.build(S)
print("wrote attachments/OSP-207_RevD_Optical_Loss_Budget.pdf")

# ============================================================== 2. OTDR export
with open("attachments/otdr_export_fdh14_20260302.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["trace_id", "leg", "event_no", "distance_from_fdh_km",
                "event_type", "measured_loss_db", "reflectance_db"])
    for e in otdr_events():
        w.writerow([f"FDH14-{e['leg']}", e["leg"], e["event"],
                    f"{e['distance_km']:.2f}", e["type"],
                    f"{e['loss_db']:.2f}", e["reflectance_db"]])
print("wrote attachments/otdr_export_fdh14_20260302.csv")

# ============================================================ 3. ONT power survey
wb = Workbook()
ws = wb.active
ws.title = "Power Survey"

thin = Side(style="thin", color="8C8C8C")
bd = Border(left=thin, right=thin, top=thin, bottom=thin)

ws["A1"] = "ONT Power Survey — FDH-14"
ws["A1"].font = Font(bold=True, size=13, color="000000")
ws["A2"] = "Downstream 1490 nm. Survey window 24 February to 2 March 2026."
ws["A2"].font = Font(size=10, color="4A4A4A")
ws["A3"] = "Received power measured at the ONT optical port with a calibrated power meter."
ws["A3"].font = Font(size=10, color="4A4A4A")

headers = ["ONT ID", "Leg", "Served From", "Drop Length (m)",
           "Measured Received Power (dBm)", "Service Tier"]
TIERS = {"A": "Residential 1G", "B": "Residential 1G", "C": "Residential 1G",
         "D": "Business 2G", "E": "Residential 1G"}
BUSINESS = {"ONT-C-03": "Business 2G", "ONT-B-02": "Business 2G"}

for c, h in enumerate(headers, start=1):
    cell = ws.cell(row=5, column=c, value=h)
    cell.font = Font(bold=True, size=10, color="000000")
    cell.border = bd
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

for i, r in enumerate(ont_rows(), start=6):
    vals = [r["ont"], r["leg"], r["mst"], r["drop_m"], r["measured_rx"],
            BUSINESS.get(r["ont"], TIERS[r["leg"]])]
    for c, v in enumerate(vals, start=1):
        cell = ws.cell(row=i, column=c, value=v)
        cell.font = Font(size=10)
        cell.border = bd
        if c in (4, 5):
            cell.alignment = Alignment(horizontal="right")
            if c == 5:
                cell.number_format = "0.00"
        else:
            cell.alignment = Alignment(horizontal="left")

for col, wdt in zip("ABCDEF", [13, 8, 14, 16, 30, 16]):
    ws.column_dimensions[col].width = wdt
ws.row_dimensions[5].height = 32
ws.freeze_panes = "A6"

wb.save("attachments/ONT_Power_Survey_FDH14.xlsx")
print("wrote attachments/ONT_Power_Survey_FDH14.xlsx")
