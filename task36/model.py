"""Single source of truth for Telecom/Network_36_TEXT.

Every published number in every attachment is derived from this module, so the
attachments cannot drift out of agreement with each other or with the golden
response.
"""

# ---------------------------------------------------------------- spec (Rev D)
SPEC = {
    "wavelength_nm": 1490,
    "fiber_db_per_km": 0.25,
    "fusion_splice_db": 0.10,
    "mechanical_splice_db": 0.30,
    "connector_pair_db": 0.50,
    "splitter_1x8_db": 10.50,
    "splitter_1x4_db": 7.20,
    "olt_tx_dbm": 2.50,
    "pass_min_dbm": -25.00,      # Rx >= -25.00            -> PASS
    "fail_below_dbm": -27.00,    # -27.00 <= Rx < -25.00   -> MARGINAL
                                 # Rx < -27.00             -> FAIL
    "tolerance_db": 1.00,        # |discrepancy| <= 1.00   -> within tolerance
}

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
# splices: (distance_km_from_FDH, type)
LEGS = {
    "A": {"mst": "MST-A", "length_km": 2.80, "splices": [(1.10, "fusion"), (2.35, "fusion")]},
    "B": {"mst": "MST-B", "length_km": 5.60, "splices": [(1.60, "fusion"), (3.20, "mechanical"),
                                                         (4.05, "fusion"), (5.20, "fusion")]},
    "C": {"mst": "MST-C", "length_km": 4.10, "splices": [(1.25, "fusion"), (3.40, "fusion")]},
    "D": {"mst": "MST-D", "length_km": 7.30, "splices": [(2.10, "fusion"), (3.55, "mechanical"),
                                                         (4.35, "fusion"), (5.90, "fusion"),
                                                         (6.80, "fusion")]},
    "E": {"mst": "MST-E", "length_km": 3.50, "splices": [(1.30, "fusion"), (2.75, "fusion")]},
}

# --------------------------------------------------------------- subscriber ONTs
# (ont_id, leg, drop_length_m, measurement_noise_db, extra_fault_db)
ONTS = [
    ("ONT-A-01", "A", 120, +0.08, 0.00),
    ("ONT-A-02", "A", 185, -0.11, 0.00),
    ("ONT-A-03", "A", 240, +0.04, 0.00),

    ("ONT-B-01", "B",  95, +0.06, 0.00),
    ("ONT-B-02", "B", 160, -0.05, 0.00),
    ("ONT-B-03", "B", 225, +0.09, 0.00),
    ("ONT-B-04", "B", 310, -0.02, 0.00),

    ("ONT-C-01", "C", 140, +0.06, 0.00),
    ("ONT-C-02", "C", 205, -0.07, 0.00),
    ("ONT-C-03", "C",  95, -0.03, 3.20),   # dirty drop connector — this ONT only
    ("ONT-C-04", "C", 270, +0.05, 0.00),

    ("ONT-D-01", "D", 110, +0.07, 0.00),
    ("ONT-D-02", "D", 175, -0.04, 0.00),
    ("ONT-D-03", "D", 250, +0.02, 0.00),

    ("ONT-E-01", "E", 130, +0.06, 0.00),
    ("ONT-E-02", "E", 195, -0.08, 0.00),
]

# ------------------------------------------------------------- injected faults
# Excess loss present in the live plant but NOT in the as-built design.
# Keyed by (leg, distance_km) matching a splice in LEGS.
LEG_FAULTS = {
    ("B", 3.20): 1.90,   # mechanical splice degraded: 2.20 dB measured vs 0.30 expected
    ("D", 5.90): 2.80,   # fusion splice degraded:     2.90 dB measured vs 0.10 expected
}

# OTDR reflectance readings at each MST input connector (cosmetic realism).
MST_CONNECTOR = {"A": (0.48, -45.2), "B": (0.52, -44.8), "C": (0.49, -45.6),
                 "D": (0.51, -45.0), "E": (0.47, -45.9)}


# ------------------------------------------------------------------ derivations
def feeder_loss_db():
    """Feeder fibre + splices + its 2 mated connector pairs."""
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


def leg_excess_db(leg):
    """Total un-designed excess loss sitting in this distribution leg."""
    return sum(v for (lg, _), v in LEG_FAULTS.items() if lg == leg)


def ont_rows():
    """Design loss, design Rx, measured Rx and classification for every ONT."""
    fixed = (feeder_loss_db()
             + SPEC["splitter_1x8_db"]
             + CONNECTORS["distribution"] * SPEC["connector_pair_db"]
             + SPEC["splitter_1x4_db"]
             + CONNECTORS["drop"] * SPEC["connector_pair_db"])

    rows = []
    for ont, leg, drop_m, noise, extra in ONTS:
        drop_loss = (drop_m / 1000.0) * SPEC["fiber_db_per_km"]
        design_loss = fixed + leg_loss_db(leg) + drop_loss
        design_rx = SPEC["olt_tx_dbm"] - design_loss

        measured_rx = design_rx - leg_excess_db(leg) - extra + noise
        measured_rx = round(measured_rx, 2)

        measured_loss = SPEC["olt_tx_dbm"] - measured_rx
        discrepancy = measured_loss - design_loss

        if measured_rx >= SPEC["pass_min_dbm"]:
            status = "PASS"
        elif measured_rx >= SPEC["fail_below_dbm"]:
            status = "MARGINAL"
        else:
            status = "FAIL"

        rows.append({
            "ont": ont, "leg": leg, "mst": LEGS[leg]["mst"], "drop_m": drop_m,
            "drop_loss": drop_loss, "design_loss": design_loss, "design_rx": design_rx,
            "measured_rx": measured_rx, "measured_loss": measured_loss,
            "discrepancy": discrepancy, "status": status,
            "anomalous": abs(discrepancy) > SPEC["tolerance_db"],
        })
    return rows


def otdr_events():
    """Events as an OTDR shot from the FDH-14 output port toward each MST."""
    events = []
    for leg, L in LEGS.items():
        n = 0
        for dist, kind in L["splices"]:
            n += 1
            expected = SPEC["fusion_splice_db"] if kind == "fusion" else SPEC["mechanical_splice_db"]
            excess = LEG_FAULTS.get((leg, dist), 0.0)
            # Healthy splices read very close to their spec value.
            jitter = {0.10: 0.01, 0.30: 0.01}.get(expected, 0.0)
            measured = expected + excess + (jitter if (n % 2 == 0) else -jitter)
            events.append({
                "leg": leg, "event": n, "distance_km": dist, "type": "Splice",
                "loss_db": round(measured, 2), "reflectance_db": "",
            })
        n += 1
        loss, refl = MST_CONNECTOR[leg]
        events.append({
            "leg": leg, "event": n, "distance_km": L["length_km"], "type": "Connector",
            "loss_db": loss, "reflectance_db": refl,
        })
    return events


if __name__ == "__main__":
    print(f"feeder loss      : {feeder_loss_db():.3f} dB")
    for leg in LEGS:
        print(f"leg {leg} fibre+splice: {leg_loss_db(leg):.3f} dB   excess {leg_excess_db(leg):.2f} dB")
    print()
    hdr = f"{'ONT':<10}{'design Rx':>10}{'meas Rx':>9}{'disc':>7}  {'status':<9}{'anom'}"
    print(hdr)
    for r in ont_rows():
        print(f"{r['ont']:<10}{r['design_rx']:>10.2f}{r['measured_rx']:>9.2f}"
              f"{r['discrepancy']:>7.2f}  {r['status']:<9}{'YES' if r['anomalous'] else ''}")
