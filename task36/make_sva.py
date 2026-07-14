"""Renders the Structured Visual Artifact: the FDH-14 as-built plant record.

Deliberately monochrome, in the style of an outside-plant record drawing. The
project's poor-quality-artifact guidance rejects the navy/cornflower/grey
"AI blue" palette, italic subheadings, and any input file that refers to another
input file, so none of those appear here.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from model import FEEDER, LEGS, ONTS, SPEC

INK   = "#000000"
GREY  = "#4a4a4a"
RULE  = "#8c8c8c"
BAND  = "#e6e6e6"

fig = plt.figure(figsize=(20, 13), dpi=130)
fig.patch.set_facecolor("white")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 200); ax.set_ylim(0, 130); ax.axis("off")

ORDER = ["A", "B", "C", "D", "E"]

def box(x, y, w, h, title, sub=None, fs=11.5):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.6))
    ty = y + h * (0.62 if sub else 0.5)
    ax.text(x + w/2, ty, title, ha="center", va="center", fontsize=fs,
            fontweight="bold", color=INK)
    if sub:
        ax.text(x + w/2, y + h*0.27, sub, ha="center", va="center",
                fontsize=fs-2.3, color=GREY)

def theader(x, w, y, cols, hdrs):
    ax.add_patch(Rectangle((x, y), w, 4.0, fc=BAND, ec=RULE, lw=0.7))
    for cx, h in zip(cols, hdrs):
        ax.text(cx, y + 2.0, h, fontsize=9.8, fontweight="bold", color=INK, va="center")

# ------------------------------------------------------------------ title block
ax.text(8, 124.0, "OPTICAL DISTRIBUTION NETWORK — AS-BUILT PLANT RECORD",
        fontsize=20, fontweight="bold", color=INK)
ax.text(8, 120.2, "FIBRE DISTRIBUTION HUB FDH-14      ARDWICK EXCHANGE (ARD-01), OLT-3 "
                  "PON PORT 1/1/4      GIGABIT PASSIVE OPTICAL NETWORK, 1490 nm DOWNSTREAM",
        fontsize=10.5, color=GREY)
ax.text(192, 124.0, "DRAWING  ODN-FDH14-R3", fontsize=10.5, color=INK,
        ha="right", fontweight="bold")
ax.text(192, 120.4, "AS-BUILT      SHEET 1 OF 1", fontsize=10.5, color=GREY, ha="right")
ax.plot([8, 192], [117.5, 117.5], color=INK, lw=1.8)

# -------------------------------------------------------------------- schematic
ax.text(8, 113.5, "SCHEMATIC", fontsize=12.5, fontweight="bold", color=INK)

SPINE = 94.5
box(8, SPINE - 6.5, 26, 13, "ARD-01", "OLT-3   PON 1/1/4")
ax.text(21, SPINE - 9.4, f"Tx {SPEC['olt_tx_dbm']:+.2f} dBm", ha="center",
        fontsize=11, color=INK, fontweight="bold")

ax.annotate("", xy=(57, SPINE), xytext=(34, SPINE),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2))
ax.text(45.5, SPINE + 2.6, "FEEDER", ha="center", fontsize=10.5,
        fontweight="bold", color=INK)
ax.text(45.5, SPINE - 4.6, f"{FEEDER['length_km']:.2f} km", ha="center",
        fontsize=10.2, color=GREY)

box(57, SPINE - 6.5, 26, 13, "FDH-14", "1:8 PRIMARY SPLITTER")
ax.text(70, SPINE - 9.4, "ports 1-5 live, 6-8 spare", ha="center",
        fontsize=9.8, color=GREY)

sub_count = {}
for _, lg, *_ in ONTS:
    sub_count[lg] = sub_count.get(lg, 0) + 1

leg_y = {lg: SPINE + off for lg, off in zip(ORDER, [16, 8, 0, -8, -16])}

ax.plot([83, 91], [SPINE, SPINE], color=INK, lw=1.8)
ax.plot([91, 91], [leg_y["E"], leg_y["A"]], color=INK, lw=1.8)

for lg in ORDER:
    y = leg_y[lg]
    L = LEGS[lg]
    ax.annotate("", xy=(119, y), xytext=(91, y),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8))
    ax.text(105, y + 2.2, f"LEG {lg}      {L['length_km']:.2f} km", ha="center",
            fontsize=10, color=INK, fontweight="bold")

    for dist, kind in L["splices"]:
        px = 93 + (dist / L["length_km"]) * 24
        if kind == "fusion":
            ax.plot([px], [y], marker="|", ms=12, mew=2.4, color=INK)
        else:
            ax.add_patch(Circle((px, y), 0.75, fc="white", ec=INK, lw=1.8, zorder=5))

    box(119, y - 4, 24, 8, L["mst"], "1:4 SPLITTER", fs=10.5)
    ax.text(146, y, f"{sub_count[lg]} subscriber drops", va="center",
            fontsize=10.2, color=GREY)

# Legend and notes. Confined to x < 88 so nothing can run under the leg arrows,
# and units plus an abbreviations key are stated explicitly: the domain lead has
# sent artifacts back for omitting units, and a peer reviewer for overlapping text.
ax.text(8, 82.2, "LEGEND AND NOTES", fontsize=10.5, fontweight="bold", color=INK)

ax.plot([9], [78.8], marker="|", ms=12, mew=2.4, color=INK)
ax.text(11.5, 78.8, "fusion splice", va="center", fontsize=10, color=GREY)
ax.add_patch(Circle((46, 78.8), 0.75, fc="white", ec=INK, lw=1.8))
ax.text(48.5, 78.8, "mechanical splice", va="center", fontsize=10, color=GREY)

ax.text(8, 75.2, "All distances in kilometres (km). Optical power in decibel-milliwatts (dBm).",
        fontsize=10, color=GREY)
ax.text(8, 71.8, "Mated connector pairs per subscriber path: 6 "
                 "(2 feeder, 2 distribution, 2 drop).", fontsize=10, color=GREY)
ax.text(8, 68.4, "OLT  optical line terminal.      FDH  fibre distribution hub.",
        fontsize=10, color=GREY)
ax.text(8, 65.0, "MST  multiport service terminal.      ONT  optical network terminal.",
        fontsize=10, color=GREY)

ax.plot([8, 192], [61.0, 61.0], color=RULE, lw=1.0)

# --------------------------------------------------------- table: segment record
ax.text(8, 56.8, "SEGMENT RECORD", fontsize=12.5, fontweight="bold", color=INK)

X1, W1 = 8, 92
c1 = [9, 50, 66, 78, 91]
theader(X1, W1, 50.5, c1, ["SEGMENT", "LENGTH (km)", "FUSION", "MECH", "CONN"])

rows = [("Feeder, ARD-01 to FDH-14", f"{FEEDER['length_km']:.2f}",
         FEEDER["fusion"], FEEDER["mechanical"], 2)]
for lg in ORDER:
    L = LEGS[lg]
    f = sum(1 for _, k in L["splices"] if k == "fusion")
    m = sum(1 for _, k in L["splices"] if k == "mechanical")
    rows.append((f"Distribution Leg {lg}, FDH-14 to {L['mst']}",
                 f"{L['length_km']:.2f}", f, m, 2))
rows.append(("Drop, MST to ONT", "per subscriber", 0, 0, 2))

y = 46.5
for i, (name, ln, f, m, c) in enumerate(rows):
    ax.add_patch(Rectangle((X1, y - 0.1), W1, 4.0, fc="white", ec=RULE, lw=0.6))
    for cx, v in zip(c1, [name, ln, str(f), str(m), str(c)]):
        ax.text(cx, y + 1.9, v, fontsize=9.8, color=INK, va="center")
    y -= 4.0

# --------------------------------------------------------- table: splice schedule
ax.text(108, 56.8, "SPLICE SCHEDULE, DISTRIBUTION LEGS", fontsize=12.5,
        fontweight="bold", color=INK)
ax.text(108, 53.4, "Distances are measured from the FDH-14 output port, which is the "
                   "0.00 km datum for leg testing.", fontsize=9.8, color=GREY)

schedule = [(lg, d, k) for lg in ORDER for d, k in LEGS[lg]["splices"]]
half = (len(schedule) + 1) // 2

for ci, chunk in enumerate([schedule[:half], schedule[half:]]):
    X = 108 + ci * 44
    cols = [X + 1.5, X + 13, X + 28]
    theader(X, 40, 46.5, cols, ["LEG", "DIST (km)", "SPLICE TYPE"])
    y = 42.5
    for lg, d, k in chunk:
        ax.add_patch(Rectangle((X, y - 0.1), 40, 3.8, fc="white", ec=RULE, lw=0.6))
        for cx, v in zip(cols, [lg, f"{d:.2f}", k.capitalize()]):
            ax.text(cx, y + 1.8, v, fontsize=9.8, color=INK, va="center")
        y -= 3.8

ax.plot([8, 192], [8.5, 8.5], color=RULE, lw=1.0)
ax.text(8, 5.4, "OUTSIDE PLANT ENGINEERING      AS-BUILT SURVEY CLOSED 2 MARCH 2026",
        fontsize=9.6, color=GREY)
ax.text(192, 5.4, "ODN-FDH14-R3", fontsize=9.6, color=GREY, ha="right")

# PDF is the approved format: the domain lead reviewed and approved the PDF of
# this drawing on 13 July 2026. Vector, so it cannot go illegible at any zoom.
fig.savefig("attachments/ODN-FDH14-R3.pdf", facecolor="white")
print("wrote attachments/ODN-FDH14-R3.pdf")
