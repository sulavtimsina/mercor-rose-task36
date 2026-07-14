"""Single source of truth for Telecom/Network_36_TEXT.

Every published number in every attachment is derived from this module, so the
attachments cannot drift out of agreement with each other or with the golden
response.

v2. Gemini 3.5 Flash solved v1 at ~100% by writing Python and computing the
whole thing deterministically, so arithmetic volume is not difficulty. v2 moves
the difficulty into *deciding what to compute*, via three independent traps:

  1. A field change notice reroutes Leg C after the as-built survey closed. The
     as-built drawing is superseded for that leg. Miss it and all four Leg C
     subscribers get the wrong design loss, and three healthy ones get falsely
     reported as faults.
  2. The 1:8 primary splitter is certified per port, not nominal. Each leg is
     fed from a specific port with its own insertion loss. Plug in a single
     nominal constant and every one of the 16 rows is wrong.
  3. Remediation ranks on SLA credit exposure, not subscriber headcount. One
     Business 10G Priority subscriber outweighs a whole leg of Residential, so
     counting subscribers produces the wrong order.
"""

# ---------------------------------------------------------------- spec (Rev E)
SPEC = {
    "wavelength_nm": 1490,
    "fiber_db_per_km": 0.25,
    "fusion_splice_db": 0.10,
    "mechanical_splice_db": 0.30,
    "connector_pair_db": 0.50,
    "splitter_1x4_db": 7.20,     # MST splitters remain a flat design value
    "olt_tx_dbm": 2.50,
    "pass_min_dbm": -25.00,      # Rx >= -25.00            -> PASS
    "fail_below_dbm": -27.00,    # -27.00 <= Rx < -25.00   -> MARGINAL
                                 # Rx < -27.00             -> FAIL
    "tolerance_db": 1.00,        # |discrepancy| <= 1.00   -> within tolerance
}

# TRAP 2. The 1:8 primary splitter at FDH-14 is individually certified. There is
# no nominal value to fall back on: the standard directs the reader to the
# per-port figures in the plant record.
SPLITTER_PORT_LOSS_DB = {
    1: 10.62, 2: 10.28, 3: 10.35, 4: 10.81,
    5: 10.44, 6: 10.19, 7: 10.55, 8: 10.73,
}

# Which FDH-14 output port feeds each leg. Deliberately not in leg order.
LEG_PORT = {"A": 3, "B": 1, "C": 5, "D": 4, "E": 2}

# Connector complement on every subscriber path: 2 feeder + 2 distribution +
# 2 drop = 6 mated pairs.
CONNECTORS = {"feeder": 2, "distribution": 2, "drop": 2}

# ---------------------------------------------------------------------- feeder
FEEDER = {
    "from": "Ardwick Exchange (ARD-01) — OLT-3, PON port 1/1/4",
    "to": "FDH-14",
    "length_km": 12.40,
    "fusion": 5,
    "mechanical": 0,
}

# ------------------------------------------------- distribution legs (from FDH)
# As recorded on the as-built drawing ODN-FDH14-R3, survey closed 12 Jan 2026.
# splices: (distance_km_from_FDH, type)
LEGS_AS_BUILT = {
    "A": {"mst": "MST-A", "length_km": 2.80, "splices": [(1.10, "fusion"), (2.35, "fusion")]},
    "B": {"mst": "MST-B", "length_km": 5.60, "splices": [(1.60, "fusion"), (3.20, "mechanical"),
                                                         (4.05, "fusion"), (5.20, "fusion")]},
    "C": {"mst": "MST-C", "length_km": 4.10, "splices": [(1.25, "fusion"), (3.40, "fusion")]},
    "D": {"mst": "MST-D", "length_km": 7.30, "splices": [(2.10, "fusion"), (3.55, "mechanical"),
                                                         (4.35, "fusion"), (5.90, "fusion"),
                                                         (6.80, "fusion")]},
    "E": {"mst": "MST-E", "length_km": 3.50, "splices": [(1.30, "fusion"), (2.75, "fusion")]},
}

# TRAP 1. Field Change Notice FCN-2291, issued 18 February 2026 — after the
# as-built survey closed, and before the 2 March OTDR survey. Leg C was rerouted
# around a carriageway widening scheme. The as-built record for Leg C is
# superseded; every other leg is unaffected.
FIELD_CHANGE = {
    "ref": "FCN-2291",
    "issued": "18 February 2026",
    "leg": "C",
    "reason": "Carriageway widening on Ardwick Lane required the Leg C duct to be "
              "abandoned between chainage 0.90 km and 3.70 km. Leg C has been "
              "rediverted along the Bank Street footway.",
    "new_length_km": 8.20,
    "new_splices": [(1.40, "fusion"), (3.05, "mechanical"), (4.60, "fusion"),
                    (6.15, "fusion"), (7.70, "fusion")],
}


def legs():
    """The plant as it actually stands: as-built, with the change notice applied."""
    out = {k: dict(v) for k, v in LEGS_AS_BUILT.items()}
    lg = FIELD_CHANGE["leg"]
    out[lg] = {
        "mst": LEGS_AS_BUILT[lg]["mst"],
        "length_km": FIELD_CHANGE["new_length_km"],
        "splices": list(FIELD_CHANGE["new_splices"]),
    }
    return out


LEGS = legs()

# --------------------------------------------------------------- subscriber ONTs
# TRAP 3. Service tier drives SLA credit exposure, which drives remediation order.
TIER_WEIGHT = {
    "Residential 1G": 1,
    "Business 2G": 3,
    "Business 10G Priority": 6,
}

# (ont_id, leg, drop_length_m, tier, measurement_noise_db, extra_fault_db)
ONTS = [
    ("ONT-A-01", "A", 120, "Residential 1G",        +0.08, 0.00),
    ("ONT-A-02", "A", 185, "Residential 1G",        -0.11, 0.00),
    ("ONT-A-03", "A", 240, "Residential 1G",        +0.04, 0.00),

    ("ONT-B-01", "B",  95, "Residential 1G",        +0.06, 0.00),
    ("ONT-B-02", "B", 160, "Residential 1G",        -0.05, 0.00),
    ("ONT-B-03", "B", 225, "Residential 1G",        +0.09, 0.00),
    ("ONT-B-04", "B", 310, "Residential 1G",        -0.02, 0.00),

    ("ONT-C-01", "C", 140, "Residential 1G",        +0.06, 0.00),
    ("ONT-C-02", "C", 205, "Residential 1G",        -0.07, 0.00),
    ("ONT-C-03", "C",  95, "Business 10G Priority", -0.03, 3.20),  # dirty drop connector
    ("ONT-C-04", "C", 270, "Residential 1G",        +0.05, 0.00),

    ("ONT-D-01", "D", 110, "Business 2G",           +0.07, 0.00),
    ("ONT-D-02", "D", 175, "Residential 1G",        -0.04, 0.00),
    ("ONT-D-03", "D", 250, "Residential 1G",        +0.02, 0.00),

    ("ONT-E-01", "E", 130, "Residential 1G",        +0.06, 0.00),
    ("ONT-E-02", "E", 195, "Residential 1G",        -0.08, 0.00),
]

# ------------------------------------------------------------- injected faults
# Excess loss present in the live plant but NOT in the design.
LEG_FAULTS = {
    ("B", 3.20): 1.90,   # mechanical splice degraded: 2.20 dB measured vs 0.30 design
    ("D", 5.90): 2.80,   # fusion splice degraded:     2.90 dB measured vs 0.10 design
}

MST_CONNECTOR = {"A": (0.48, -45.2), "B": (0.52, -44.8), "C": (0.49, -45.6),
                 "D": (0.51, -45.0), "E": (0.47, -45.9)}


# ------------------------------------------------------------------ derivations
def feeder_loss_db():
    return (FEEDER["length_km"] * SPEC["fiber_db_per_km"]
            + FEEDER["fusion"] * SPEC["fusion_splice_db"]
            + FEEDER["mechanical"] * SPEC["mechanical_splice_db"]
            + CONNECTORS["feeder"] * SPEC["connector_pair_db"])


def leg_loss_db(leg):
    """Distribution fibre + splices only (connectors counted separately)."""
    L = LEGS[leg]
    loss = L["length_km"] * SPEC["fiber_db_per_km"]
    for _, kind in L["splices"]:
        loss += SPEC["fusion_splice_db"] if kind == "fusion" else SPEC["mechanical_splice_db"]
    return loss


def splitter_loss_db(leg):
    return SPLITTER_PORT_LOSS_DB[LEG_PORT[leg]]


def leg_excess_db(leg):
    return sum(v for (lg, _), v in LEG_FAULTS.items() if lg == leg)


def ont_rows():
    fixed = (feeder_loss_db()
             + CONNECTORS["distribution"] * SPEC["connector_pair_db"]
             + SPEC["splitter_1x4_db"]
             + CONNECTORS["drop"] * SPEC["connector_pair_db"])

    rows = []
    for ont, leg, drop_m, tier, noise, extra in ONTS:
        drop_loss = (drop_m / 1000.0) * SPEC["fiber_db_per_km"]
        design_loss = fixed + splitter_loss_db(leg) + leg_loss_db(leg) + drop_loss
        design_rx = SPEC["olt_tx_dbm"] - design_loss

        measured_rx = round(design_rx - leg_excess_db(leg) - extra + noise, 2)
        measured_loss = SPEC["olt_tx_dbm"] - measured_rx
        discrepancy = measured_loss - design_loss

        if measured_rx >= SPEC["pass_min_dbm"]:
            status = "PASS"
        elif measured_rx >= SPEC["fail_below_dbm"]:
            status = "MARGINAL"
        else:
            status = "FAIL"

        rows.append({
            "ont": ont, "leg": leg, "mst": LEGS[leg]["mst"], "port": LEG_PORT[leg],
            "drop_m": drop_m, "tier": tier, "weight": TIER_WEIGHT[tier],
            "design_loss": design_loss, "design_rx": design_rx,
            "measured_rx": measured_rx, "measured_loss": measured_loss,
            "discrepancy": discrepancy, "status": status,
            "anomalous": abs(discrepancy) > SPEC["tolerance_db"],
        })
    return rows


def otdr_events():
    """OTDR shot from the FDH-14 output port toward each MST on 2 March 2026 —
    i.e. after the Leg C reroute, so Leg C events follow the new route."""
    events = []
    for leg, L in LEGS.items():
        n = 0
        for dist, kind in L["splices"]:
            n += 1
            expected = SPEC["fusion_splice_db"] if kind == "fusion" else SPEC["mechanical_splice_db"]
            excess = LEG_FAULTS.get((leg, dist), 0.0)
            jitter = 0.01
            measured = expected + excess + (jitter if (n % 2 == 0) else -jitter)
            events.append({"leg": leg, "event": n, "distance_km": dist, "type": "Splice",
                           "loss_db": round(measured, 2), "reflectance_db": ""})
        n += 1
        loss, refl = MST_CONNECTOR[leg]
        events.append({"leg": leg, "event": n, "distance_km": L["length_km"],
                       "type": "Connector", "loss_db": loss, "reflectance_db": refl})
    return events


def faults():
    """The three faults, ranked: severity (FAIL first), then SLA credit exposure
    descending, then lowest measured received power."""
    rows = ont_rows()
    groups = []

    for (lg, dist), _ in sorted(LEG_FAULTS.items()):
        affected = [r for r in rows if r["leg"] == lg]
        kind = dict(LEGS[lg]["splices"])[dist]
        design = SPEC["fusion_splice_db"] if kind == "fusion" else SPEC["mechanical_splice_db"]
        measured = next(e["loss_db"] for e in otdr_events()
                        if e["leg"] == lg and e["distance_km"] == dist)
        groups.append({
            "what": f"Leg {lg} {kind} splice at {dist:.2f} km",
            "location": "shared distribution plant",
            "measured_db": measured, "design_db": design,
            "subscribers": len(affected),
            "exposure": sum(r["weight"] for r in affected),
            "severity": "FAIL" if any(r["status"] == "FAIL" for r in affected) else "MARGINAL",
            "worst_rx": min(r["measured_rx"] for r in affected),
        })

    for r in rows:
        if r["anomalous"] and leg_excess_db(r["leg"]) == 0.0:
            groups.append({
                "what": f"{r['ont']} drop-side excess loss",
                "location": f"downstream of {r['mst']}, invisible to the OTDR",
                "measured_db": None, "design_db": None,
                "subscribers": 1, "exposure": r["weight"],
                "severity": r["status"], "worst_rx": r["measured_rx"],
            })

    sev = {"FAIL": 0, "MARGINAL": 1}
    groups.sort(key=lambda g: (sev[g["severity"]], -g["exposure"], g["worst_rx"]))
    for i, g in enumerate(groups, start=1):
        g["id"] = f"FLT-{i:02d}"
    return groups


if __name__ == "__main__":
    print(f"feeder {feeder_loss_db():.3f} dB")
    for lg in LEGS:
        print(f"  leg {lg}: port {LEG_PORT[lg]} splitter {splitter_loss_db(lg):.2f} dB, "
              f"fibre+splice {leg_loss_db(lg):.3f} dB, excess {leg_excess_db(lg):.2f} dB")
    print()
    print(f"{'ONT':<10}{'dRx':>8}{'mRx':>8}{'disc':>7}  {'status':<9}{'tier':<24}{'anom'}")
    for r in ont_rows():
        print(f"{r['ont']:<10}{r['design_rx']:>8.2f}{r['measured_rx']:>8.2f}"
              f"{r['discrepancy']:>7.2f}  {r['status']:<9}{r['tier']:<24}"
              f"{'YES' if r['anomalous'] else ''}")
    print()
    for g in faults():
        print(f"{g['id']}  {g['what']:<40} {g['severity']:<9} "
              f"{g['subscribers']} sub  exposure {g['exposure']}  worst {g['worst_rx']:.2f} dBm")
