"""Derives the reference answer straight from the model, so the golden response
can be checked against it rather than hand-computed.

Also reports what a model that falls into each of the three traps would produce,
which is what the Model Failure Justification is written from.
"""
from model import (SPEC, LEGS, LEGS_AS_BUILT, LEG_PORT, SPLITTER_PORT_LOSS_DB,
                   FIELD_CHANGE, ont_rows, otdr_events, faults, leg_loss_db,
                   feeder_loss_db, CONNECTORS)

rows = ont_rows()

print("SECTION 2 — PER-SUBSCRIBER OPTICAL BUDGET")
print("ONT ID     | Design Loss | Design Rx | Measured Rx | Discrepancy | Class")
for r in rows:
    print(f"{r['ont']:<10} | {r['design_loss']:>11.2f} | {r['design_rx']:>9.2f} | "
          f"{r['measured_rx']:>11.2f} | {r['discrepancy']:>+11.2f} | {r['status']}")

n = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "MARGINAL", "FAIL")}
print(f"\nTotals: {len(rows)} ONTs — {n['PASS']} PASS, {n['MARGINAL']} MARGINAL, {n['FAIL']} FAIL; "
      f"{sum(1 for r in rows if r['anomalous'])} exceed the {SPEC['tolerance_db']:.2f} dB tolerance.")

print("\nSECTION 3 — COMPONENTS OUT OF SPEC BY MORE THAN TOLERANCE")
schedule = {(lg, d): k for lg in LEGS for d, k in LEGS[lg]["splices"]}
for e in otdr_events():
    if e["type"] != "Splice":
        continue
    kind = schedule[(e["leg"], e["distance_km"])]
    expected = SPEC["fusion_splice_db"] if kind == "fusion" else SPEC["mechanical_splice_db"]
    if e["loss_db"] - expected > SPEC["tolerance_db"]:
        print(f"  Leg {e['leg']} @ {e['distance_km']:.2f} km — {kind} splice — "
              f"measured {e['loss_db']:.2f} dB vs design {expected:.2f} dB "
              f"(excess {e['loss_db'] - expected:+.2f} dB)")
print("  Leg C — OTDR trace clean end to end. ONT-C-03 alone is anomalous, so its excess loss "
      "lies downstream of MST-C (drop side), where the OTDR cannot see.")

print("\nSECTION 4 — REMEDIATION ORDER")
for g in faults():
    print(f"  {g['id']}  {g['what']:<40} {g['severity']:<9} "
          f"{g['subscribers']} subscriber(s)  SLA exposure {g['exposure']}  "
          f"worst Rx {g['worst_rx']:.2f} dBm")

# ------------------------------------------------------------------ trap payoffs
print("\n" + "=" * 78)
print("WHAT EACH TRAP COSTS A MODEL THAT MISSES IT")
print("=" * 78)

lg = FIELD_CHANGE["leg"]
old = (LEGS_AS_BUILT[lg]["length_km"] * SPEC["fiber_db_per_km"]
       + sum(SPEC["fusion_splice_db"] if k == "fusion" else SPEC["mechanical_splice_db"]
             for _, k in LEGS_AS_BUILT[lg]["splices"]))
new = leg_loss_db(lg)
print(f"\nTRAP 1 — ignoring field change notice {FIELD_CHANGE['ref']} (Leg {lg} reroute)")
print(f"  Leg {lg} design loss: superseded {old:.3f} dB vs in-force {new:.3f} dB "
       f"(understated by {new - old:.3f} dB)")
print(f"  Every Leg {lg} discrepancy is inflated by {new - old:.2f} dB:")
for r in rows:
    if r["leg"] != lg:
        continue
    wrong = r["discrepancy"] + (new - old)
    flag = "flagged as a fault" if abs(wrong) > SPEC["tolerance_db"] else "within tolerance"
    truth = "IS a fault" if r["anomalous"] else "is healthy"
    verdict = "  <-- FALSE POSITIVE" if (abs(wrong) > SPEC["tolerance_db"]) and not r["anomalous"] else ""
    print(f"    {r['ont']}: true {r['discrepancy']:+.2f} dB ({truth}) -> "
          f"reports {wrong:+.2f} dB, {flag}{verdict}")

print("\nTRAP 2 — using a nominal 10.50 dB for the 1:8 splitter instead of the certified port")
for lgx in sorted(LEG_PORT):
    cert = SPLITTER_PORT_LOSS_DB[LEG_PORT[lgx]]
    print(f"    Leg {lgx} (port {LEG_PORT[lgx]}): certified {cert:.2f} dB, "
          f"nominal error {10.50 - cert:+.2f} dB on every row of that leg")
print("    -> all 16 design-loss, design-Rx and discrepancy values wrong.")

print("\nTRAP 3 — ranking by subscriber headcount instead of SLA credit exposure")
by_count = sorted(faults(), key=lambda g: ({"FAIL": 0, "MARGINAL": 1}[g["severity"]],
                                           -g["subscribers"], g["worst_rx"]))
print("    correct order:", " -> ".join(g["what"].split(" drop-side")[0].split(" splice")[0]
                                        for g in faults()))
print("    headcount order:", " -> ".join(g["what"].split(" drop-side")[0].split(" splice")[0]
                                          for g in by_count))
