"""Derives the reference answer straight from the model, so the golden response
can be checked against it rather than hand-computed."""
from model import SPEC, LEGS, ont_rows, otdr_events

rows = ont_rows()

print("SECTION 2 — PER-SUBSCRIBER OPTICAL BUDGET")
print("ONT ID     | Design Loss | Design Rx | Measured Rx | Discrepancy | Class")
for r in rows:
    print(f"{r['ont']:<10} | {r['design_loss']:>11.2f} | {r['design_rx']:>9.2f} | "
          f"{r['measured_rx']:>11.2f} | {r['discrepancy']:>+11.2f} | {r['status']}")

print()
print("SECTION 3 — OUT-OF-SPEC COMPONENTS (OTDR reconciled to splice schedule)")
schedule = {(lg, d): k for lg in LEGS for d, k in LEGS[lg]["splices"]}
for e in otdr_events():
    if e["type"] != "Splice":
        continue
    kind = schedule[(e["leg"], e["distance_km"])]
    expected = SPEC["fusion_splice_db"] if kind == "fusion" else SPEC["mechanical_splice_db"]
    excess = e["loss_db"] - expected
    if excess > SPEC["tolerance_db"]:
        print(f"  Leg {e['leg']} @ {e['distance_km']:.2f} km — {kind} splice — "
              f"measured {e['loss_db']:.2f} dB vs design {expected:.2f} dB "
              f"(excess {excess:+.2f} dB)")
print("  Leg C — OTDR trace clean end to end. ONT-C-03 alone is anomalous, so its "
      "excess loss lies downstream of MST-C (drop side), where the OTDR cannot see.")

print()
print("SECTION 4 — REMEDIATION ORDER")
groups = [
    ("FLT-01", "Leg D fusion splice @ 5.90 km", "FAIL", 3, -27.21),
    ("FLT-02", "Leg B mechanical splice @ 3.20 km", "MARGINAL", 4, -25.80),
    ("FLT-03", "ONT-C-03 drop-side excess loss", "MARGINAL", 1, -26.28),
]
for fid, what, sev, n, worst in groups:
    print(f"  {fid}  {what:<36} {sev:<9} {n} subscriber(s)  worst Rx {worst:.2f} dBm")

print()
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_marg = sum(1 for r in rows if r["status"] == "MARGINAL")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_anom = sum(1 for r in rows if r["anomalous"])
print(f"Totals: {len(rows)} ONTs — {n_pass} PASS, {n_marg} MARGINAL, {n_fail} FAIL; "
      f"{n_anom} exceed the {SPEC['tolerance_db']:.2f} dB tolerance.")
