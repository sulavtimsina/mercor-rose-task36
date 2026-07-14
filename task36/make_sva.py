"""Renders the Structured Visual Artifact: the FDH-14 as-built plant record.

Monochrome, in the style of an outside-plant record drawing. The project's
poor-quality-artifact guidance rejects the navy/cornflower/grey "AI blue"
palette, italic subheadings, and any input file that refers to another input
file, so none of those appear here.

This drawing shows the plant AS BUILT on 12 January 2026. Leg C was later
rerouted under a field change notice, so the Leg C geometry here is superseded.
That is deliberate: it draws from LEGS_AS_BUILT, not from the live LEGS.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from model import FEEDER, LEGS_AS_BUILT, LEG_PORT, SPLITTER_PORT_LOSS_DB, ONTS, SPEC

INK, GREY, RULE, BAND = "#000000", "#4a4a4a", "#8c8c8c", "#e6e6e6"
ORDER = ["A", "B", "C", "D", "E"]

fig = plt.figure(figsize=(20, 15), dpi=130)
fig.patch.set_facecolor("white")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 200); ax.set_ylim(0, 145); ax.axis("off")


def box(x, y, w, h, title, sub=None, fs=11.5):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.6))
    ax.text(x + w/2, y + h * (0.62 if sub else 0.5), title, ha="center", va="center",
            fontsize=fs, fontweight="bold", color=INK)
    if sub:
        ax.text(x + w/2, y + h*0.27, sub, ha="center", va="center",
                fontsize=fs-2.3, color=GREY)


def theader(x, w, y, cols, hdrs, h=4.0):
    ax.add_patch(Rectangle((x, y), w, h, fc=BAND, ec=RULE, lw=0.7))
    for cx, t in zip(cols, hdrs):
        ax.text(cx, y + h/2, t, fontsize=9.8, fontweight="bold", color=INK, va="center")


# ------------------------------------------------------------------ title block
ax.text(8, 139.0, "OPTICAL DISTRIBUTION NETWORK — AS-BUILT PLANT RECORD",
        fontsize=20, fontweight="bold", color=INK)
ax.text(8, 135.2, "FIBRE DISTRIBUTION HUB FDH-14      ARDWICK EXCHANGE (ARD-01), OLT-3 "
                  "PON PORT 1/1/4      GIGABIT PASSIVE OPTICAL NETWORK, 1490 nm DOWNSTREAM",
        fontsize=10.5, color=GREY)
ax.text(192, 139.0, "DRAWING  ODN-FDH14-R3", fontsize=10.5, color=INK, ha="right",
        fontweight="bold")
ax.text(192, 135.4, "AS-BUILT      SHEET 1 OF 1", fontsize=10.5, color=GREY, ha="right")
ax.plot([8, 192], [132.5, 132.5], color=INK, lw=1.8)

# -------------------------------------------------------------------- schematic
ax.text(8, 128.5, "SCHEMATIC", fontsize=12.5, fontweight="bold", color=INK)

SPINE = 109.5
box(8, SPINE - 6.5, 26, 13, "ARD-01", "OLT-3   PON 1/1/4")
ax.text(21, SPINE - 9.4, f"Tx {SPEC['olt_tx_dbm']:+.2f} dBm", ha="center", fontsize=11,
        color=INK, fontweight="bold")

ax.annotate("", xy=(57, SPINE), xytext=(34, SPINE),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2))
ax.text(45.5, SPINE + 2.6, "FEEDER", ha="center", fontsize=10.5, fontweight="bold", color=INK)
ax.text(45.5, SPINE - 4.6, f"{FEEDER['length_km']:.2f} km", ha="center", fontsize=10.2, color=GREY)

box(57, SPINE - 6.5, 26, 13, "FDH-14", "1:8 PRIMARY SPLITTER")
ax.text(70, SPINE - 9.4, "ports 1-5 live, 6-8 spare", ha="center", fontsize=9.8, color=GREY)

sub_count = {}
for _, lg, *_ in ONTS:
    sub_count[lg] = sub_count.get(lg, 0) + 1

leg_y = {lg: SPINE + off for lg, off in zip(ORDER, [16, 8, 0, -8, -16])}
ax.plot([83, 91], [SPINE, SPINE], color=INK, lw=1.8)
ax.plot([91, 91], [leg_y["E"], leg_y["A"]], color=INK, lw=1.8)

for lg in ORDER:
    y, L = leg_y[lg], LEGS_AS_BUILT[lg]
    ax.annotate("", xy=(119, y), xytext=(91, y),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8))
    ax.text(105, y + 2.2, f"LEG {lg}   PORT {LEG_PORT[lg]}   {L['length_km']:.2f} km",
            ha="center", fontsize=9.8, color=INK, fontweight="bold")
    for dist, kind in L["splices"]:
        px = 93 + (dist / L["length_km"]) * 24
        if kind == "fusion":
            ax.plot([px], [y], marker="|", ms=12, mew=2.4, color=INK)
        else:
            ax.add_patch(Circle((px, y), 0.75, fc="white", ec=INK, lw=1.8, zorder=5))
    box(119, y - 4, 24, 8, L["mst"], "1:4 SPLITTER", fs=10.5)
    ax.text(146, y, f"{sub_count[lg]} subscriber drops", va="center", fontsize=10.2, color=GREY)

# legend and notes — kept left of x=88 so nothing runs under the leg arrows
ax.text(8, 97.2, "LEGEND AND NOTES", fontsize=10.5, fontweight="bold", color=INK)
ax.plot([9], [93.8], marker="|", ms=12, mew=2.4, color=INK)
ax.text(11.5, 93.8, "fusion splice", va="center", fontsize=10, color=GREY)
ax.add_patch(Circle((46, 93.8), 0.75, fc="white", ec=INK, lw=1.8))
ax.text(48.5, 93.8, "mechanical splice", va="center", fontsize=10, color=GREY)
ax.text(8, 90.2, "All distances in kilometres (km). Optical power in decibel-milliwatts (dBm). "
                 "Loss in decibels (dB).", fontsize=10, color=GREY)
ax.text(8, 86.8, "Mated connector pairs per subscriber path: 6 (2 feeder, 2 distribution, 2 drop).",
        fontsize=10, color=GREY)
ax.text(8, 83.4, "OLT  optical line terminal.      FDH  fibre distribution hub.      "
                 "MST  multiport service terminal.      ONT  optical network terminal.",
        fontsize=10, color=GREY)

ax.plot([8, 192], [80.0, 80.0], color=RULE, lw=1.0)

# ------------------------------------------- certified splitter port insertion loss
ax.text(8, 76.0, "FDH-14 PRIMARY SPLITTER — CERTIFIED PORT INSERTION LOSS",
        fontsize=12.5, fontweight="bold", color=INK)
ax.text(8, 72.6, "This 1:8 splitter is individually certified. The insertion loss of the port "
                 "feeding a leg is the value that applies to that leg.", fontsize=9.8, color=GREY)

ports = sorted(SPLITTER_PORT_LOSS_DB)
pcols = [10 + i * 23 for i in range(len(ports))]
theader(8, 184, 65.0, pcols, [f"PORT {p}" for p in ports])
ax.add_patch(Rectangle((8, 61.0), 184, 4.0, fc="white", ec=RULE, lw=0.6))
for cx, p in zip(pcols, ports):
    ax.text(cx, 63.0, f"{SPLITTER_PORT_LOSS_DB[p]:.2f} dB", fontsize=9.8, color=INK, va="center")

ax.plot([8, 192], [57.5, 57.5], color=RULE, lw=1.0)

# --------------------------------------------------------- table: segment record
ax.text(8, 53.5, "SEGMENT RECORD", fontsize=12.5, fontweight="bold", color=INK)
X1, W1 = 8, 96
c1 = [9, 47, 60, 74, 84, 93]
theader(X1, W1, 47.0, c1, ["SEGMENT", "FDH PORT", "LENGTH (km)", "FUSION", "MECH", "CONN"])

rows = [("Feeder, ARD-01 to FDH-14", "—", f"{FEEDER['length_km']:.2f}",
         FEEDER["fusion"], FEEDER["mechanical"], 2)]
for lg in ORDER:
    L = LEGS_AS_BUILT[lg]
    f = sum(1 for _, k in L["splices"] if k == "fusion")
    m = sum(1 for _, k in L["splices"] if k == "mechanical")
    rows.append((f"Distribution Leg {lg}, FDH-14 to {L['mst']}", str(LEG_PORT[lg]),
                 f"{L['length_km']:.2f}", f, m, 2))
rows.append(("Drop, MST to ONT", "—", "per subscriber", 0, 0, 2))

y = 43.0
for name, port, ln, f, m, c in rows:
    ax.add_patch(Rectangle((X1, y - 0.1), W1, 4.0, fc="white", ec=RULE, lw=0.6))
    for cx, v in zip(c1, [name, port, ln, str(f), str(m), str(c)]):
        ax.text(cx, y + 1.9, v, fontsize=9.8, color=INK, va="center")
    y -= 4.0

# --------------------------------------------------------- table: splice schedule
ax.text(108, 53.5, "SPLICE SCHEDULE, DISTRIBUTION LEGS", fontsize=12.5,
        fontweight="bold", color=INK)
ax.text(108, 50.2, "Distances are measured from the FDH-14 output port, the 0.00 km datum.",
        fontsize=9.8, color=GREY)

schedule = [(lg, d, k) for lg in ORDER for d, k in LEGS_AS_BUILT[lg]["splices"]]
half = (len(schedule) + 1) // 2
for ci, chunk in enumerate([schedule[:half], schedule[half:]]):
    X = 108 + ci * 44
    cols = [X + 1.5, X + 13, X + 28]
    theader(X, 40, 43.0, cols, ["LEG", "DIST (km)", "SPLICE TYPE"], h=3.8)
    y = 39.2
    for lg, d, k in chunk:
        ax.add_patch(Rectangle((X, y - 0.1), 40, 3.8, fc="white", ec=RULE, lw=0.6))
        for cx, v in zip(cols, [lg, f"{d:.2f}", k.capitalize()]):
            ax.text(cx, y + 1.8, v, fontsize=9.8, color=INK, va="center")
        y -= 3.8

ax.plot([8, 192], [8.5, 8.5], color=RULE, lw=1.0)
ax.text(8, 5.4, "OUTSIDE PLANT ENGINEERING      AS-BUILT SURVEY CLOSED 12 JANUARY 2026",
        fontsize=9.6, color=GREY)
ax.text(192, 5.4, "ODN-FDH14-R3", fontsize=9.6, color=GREY, ha="right")

fig.savefig("attachments/ODN-FDH14-R3.pdf", facecolor="white")
fig.savefig("sva_preview.png", dpi=100, facecolor="white")
print("wrote attachments/ODN-FDH14-R3.pdf (+ sva_preview.png)")
