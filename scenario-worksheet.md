# Scenario Design Worksheet — Telecom/Network_36_TEXT

Output type is TEXT: the deliverable is a structured plain-text remediation memo, not a file.
All build artifacts live in `task36/`. Every number in every attachment is generated from
`task36/model.py`, so the files cannot disagree with each other or with the golden response.

## 1. The real workflow (Realistic Workflow Test)
Post-construction acceptance / fault localisation on a GPON access hub. An outside-plant engineer
receives the as-built record, the OTDR traces shot by the splicing crew, and the ONT power readings
pulled from the OLT, and must decide which subscribers are out of spec, where the excess loss
physically is, and which crew goes where first. The "customer" of the deliverable is the field
dispatch desk and the NOC.

## 2. Economic value (Economic Rationale)
Reconciling as-built records, OTDR traces and per-subscriber power readings across a PON hub is a
4-to-6 hour manual job for a field engineer, and mis-localising a single degraded splice dispatches
a splice crew to the wrong access point at roughly $1,800 per truck roll; automating this
reconciliation removes that engineering time and prevents the wasted dispatch while three
subscribers are already below the service threshold and accruing SLA credits.

## 3. The Structured Visual Artifact
`ODN-FDH14-R3.png` — the as-built plant record for hub FDH-14: ODN schematic (CO/OLT → 12.40 km
feeder → FDH-14 1:8 splitter → five distribution legs → MST-A…E 1:4 splitters → 16 subscriber drops),
plus a segment record table (length / fusion / mechanical / connectors per segment) and a splice
schedule (per-leg splice distances and types, referenced to the OTDR datum).

- Synthesis required: the SVA alone answers nothing. It supplies topology and the splice schedule;
  loss values come from the standard, event losses from the OTDR log, and received power from the
  readings. The answer only exists at the intersection of all four.
- Not perception-gated: every quantity is in a labelled table. No counting symbols, no tiny text,
  no colour discrimination, no object identification.
- Complexity: five legs, two splice types with different design losses, and an OTDR datum that has
  to be mapped back onto the schedule to type each event.

## 4. The distinct units of work (6, and NOT all chained)
1. Build each subscriber's design path loss from the as-built record priced with the standard.
2. Classify all 16 ONTs PASS / MARGINAL / FAIL from measured Rx. (Independent of #1 — reads
   straight from the readings file against the standard's thresholds.)
3. Compute measured-vs-design discrepancy per ONT and flag those over the 1.00 dB tolerance.
4. Reconcile OTDR events against the splice schedule to type each event and find components whose
   measured loss exceeds design. (Independent path to the same conclusion — corroborates #3.)
5. Separate shared-plant faults (whole leg affected, OTDR-visible) from drop-side faults
   (single ONT, OTDR-blind because the trace stops at the MST splitter).
6. Rank remediation: severity, then subscribers affected, then lowest measured Rx.

No single point of failure: #2 and #4 do not depend on #1, so a model that botches the budget
arithmetic can still earn the classification and localisation criteria.

## 5. Objectivity lockdown
- Every component loss, the OLT Tx power, the three classification thresholds and the ±1.00 dB
  tolerance are stated numerically in the standard.
- Rounding fixed at 2 decimals; units fixed (dB for loss, dBm for power); drop lengths in metres
  must be converted to km.
- Ranking ties fully broken: severity → subscribers affected (desc) → lowest measured Rx.
- Healthy subscribers sit within 0.11 dB of design; every real fault is ≥1.81 dB. The 1.00 dB
  tolerance line falls in a wide empty gap, so no ONT is a borderline judgment call.
- Classification uses measured Rx, which is *given*, so it cannot be knocked off by an arithmetic
  slip upstream.

## 6. Dependency + searchability
- Without the files: impossible. Every figure is invented plant data.
- Googling any figure returns nothing — no real network, no published document.

## 7. Input files (all Tasker-generated)
| # | File (native format) | Source category | SVA? |
|---|---|---|---|
| 1 | ODN-FDH14-R3.png (image) | Tasker-generated | yes |
| 2 | OSP-207_RevD_Optical_Loss_Budget.pdf | Tasker-generated | |
| 3 | otdr_export_fdh14_20260302.csv | Tasker-generated | |
| 4 | ONT_Power_Survey_FDH14.xlsx | Tasker-generated | |

## 8. The three traps (why a model should land in the 10–60% band)
- Leg D's fault is a *fusion* splice while a healthy *mechanical* splice sits on the same leg —
  punishes the "mechanical splices are the weak ones" heuristic.
- Leg B's fault *is* the mechanical splice — so the opposite heuristic fails too.
- ONT-C-03 is low with a clean OTDR trace on its leg. The standard says the trace stops at the MST
  splitter, so the fault must be drop-side. A model reasoning only from the OTDR misses it entirely.
- The OTDR log types every event as "Splice" with no fusion/mechanical distinction; that must be
  recovered from the SVA splice schedule before any event can be judged in or out of spec.

## 9. Reference answer (from task36/reference_answer.py)
16 ONTs: 8 PASS, 5 MARGINAL, 3 FAIL; 8 exceed tolerance.
FLT-01 Leg D fusion splice @ 5.90 km (FAIL, 3 subs) → FLT-02 Leg B mechanical splice @ 3.20 km
(MARGINAL, 4 subs) → FLT-03 ONT-C-03 drop-side loss (MARGINAL, 1 sub).

## 9b. Compliance pass against the "AI / Poor Image Quality Examples" guidance
Fixed after reading the guidance doc and Kandace M's 12 Jul channel post:
- Dropped the navy/cornflower/grey "AI blue" palette for monochrome line work.
- Removed every reference from one input file to another (the guidance flags this repeatedly).
- Removed all italic subheadings and footers.
- Varied the filename conventions across the four files (uniform naming is cited as evidence
  of an AI-generated fileset).
- Renamed the exchange off "Riverbend" (too close to the flagged AI default "Riverside").
- No confidentiality notice, no mention of the project, no "synthetic"/"simulated" wording.
- Added OSP-207 section 7: the OTDR does not report splice type, so the type must be taken
  from the plant record. Closes the last objectivity gap.
`task36/lint_artifacts.py` re-checks all of this automatically; run it before any upload.

## 10. Next gate
Post the SVA + 1–2 sentence use case in #rose-telecom-and-network-b78, tag [EXP] Mark B.
NOT YET DONE — this must happen before anything is uploaded to Studio.
