# Telecom/Network_36_TEXT — Project Rose

Working repo for one Mercor Project Rose task. Everything that has to be typed into RL Studio is
reproduced below so it can be copied straight off a phone.

**Studio task:** https://studio.mercor.com/annotator/tasks/task_7290b7c2659f417cafd0871eef0b0d8e/

---

## Status

Version 1 was **too easy**: Gemini 3.5 Flash scored roughly 100% on trajectory 6. It wrote Python,
computed every value correctly, and even nailed the drop-side fault that was meant to defeat it.
Against a model with a code interpreter, arithmetic volume is not difficulty.

Version 2 moves the difficulty into *deciding what to compute*. See "The three traps" below.

| Step | State |
|---|---|
| SVA approved by Mark B (as PDF) | done — but the drawing has since changed, so re-post it |
| Input files uploaded to Studio | **stale — v1 files are in Studio, 5 new files must replace them** |
| Prompt entered in Studio | **stale — must be replaced with the v2 prompt below** |
| Economic rationale | entered |
| File Input Source (now 5 items) | 1 of 5 done |
| Confidentiality checkboxes | ticked |
| Auto QCs | not run |
| 3 trajectories | **v1 runs are void — rerun after the files and prompt are replaced** |
| Model Failure Justification | not written |
| Submit for Prompt Review | not done |

Studio's editor silently drops pasted text. **After pasting, hit Save Changes, reload, and confirm
it stuck.** The "Add Files" button does nothing in a remote-debugging Chrome — drag and drop the
files onto the Input Files area instead, or use an ordinary Chrome window.

---

## The three traps (why the model should now fail)

1. **Field change notice.** `FCN-2291` reroutes Leg C after the as-built survey closed: 4.10 km
   becomes 8.20 km, with a different splice schedule. The as-built drawing still shows the old
   route, and says so. A model that ignores the notice understates Leg C design loss by 1.53 dB and
   **falsely reports three healthy subscribers (C-01, C-02, C-04) as faults**.
2. **Certified splitter ports.** The 1:8 primary splitter has no nominal loss. Each port is
   certified separately (10.19–10.81 dB) and each leg is fed from a specific port. Plug in a
   nominal 10.50 dB and **all 16 rows are wrong**.
3. **SLA credit exposure.** Remediation ranks on severity, then SLA credit exposure, then lowest
   received power — not on subscriber headcount. One Business 10G Priority subscriber (weight 6)
   outranks a whole leg of Residential. **FLT-01 is a single subscriber, ahead of a leg of three.**

---

## The prompt (paste into the User message box)

> Analyze the five attached plant records for fibre distribution hub FDH-14 on a Gigabit Passive Optical Network (GPON) access network and produce an optical fault remediation memo as plain text in your response. Conduct your analysis as of 2 March 2026.
>
> The attached files are ODN-FDH14-R3.pdf (as-built plant record: network schematic, certified splitter port insertion losses, segment record, and splice schedule), OSP-207_RevE_Optical_Loss_Budget.pdf (component loss values, acceptance thresholds, measurement tolerance, OTDR test method, remediation priority rules, and change control), FCN-2291 Leg C Rediversion.docx (a field change notice affecting the distribution plant), otdr_export_fdh14_20260302.csv (optical time-domain reflectometer (OTDR) events for each distribution leg), and ONT_Power_Survey_FDH14.xlsx (drop lengths, measured received power, and service tier for each optical network terminal (ONT)).
>
> Carry out the following analysis. Apply the plant records that are in force as of the analysis date, and price every component using the standard.
>
> Calculate, for every ONT in the power survey, the design end-to-end path loss from the optical line terminal (OLT) to that ONT. A complete path comprises the feeder segment, the primary splitter at the FDH, the distribution leg serving that subscriber, the 1:4 splitter at the multiport service terminal (MST), the subscriber drop, and every fusion splice, mechanical splice, and mated connector pair on that path. Derive the design received power at each ONT from the commissioned OLT transmit power.
>
> Classify each ONT against the acceptance thresholds in the standard using its measured received power.
>
> Compute, for each ONT, the discrepancy between its measured path loss and its design path loss, and identify which ONTs exceed the measurement tolerance defined in the standard.
>
> Reconcile the OTDR events against the splice schedule in force to identify every plant component whose measured loss exceeds its design value by more than the measurement tolerance. Report each such component by distribution leg, distance from the FDH, component type, measured loss, and design loss.
>
> Determine, for each group of affected subscribers, whether the excess loss sits in shared distribution plant or downstream of an MST, and state the evidence that establishes this.
>
> Rank the faults for remediation using the priority rules in the standard, and state the SLA credit exposure you calculated for each fault.
>
> Express every optical loss in decibels (dB) and every optical power in decibel-milliwatts (dBm), each to two decimal places. Drop lengths are recorded in metres and must be converted before being combined with per-kilometre attenuation.
>
> Structure the memo to these requirements. Use exactly four sections, with these headings, in this order and this wording: "1. FAULT SUMMARY", "2. PER-SUBSCRIBER OPTICAL BUDGET", "3. FAULT LOCALISATION", "4. REMEDIATION ORDER". Render section 2 as a pipe-delimited plain-text table whose columns are, in order: ONT ID | Design Loss (dB) | Design Rx (dBm) | Measured Rx (dBm) | Discrepancy (dB) | Classification. Render section 4 as a numbered list with one fault per line, each line beginning with a fault identifier of the form FLT-01, FLT-02, and so on in rank order, and each line stating the severity, the number of subscribers affected, and the SLA credit exposure. Use no bullet points and no bold or italic markup anywhere in the memo. Keep the memo under 900 words.

Plain text: [`task36/prompt.txt`](task36/prompt.txt) — 3488 characters (limit 500–4,500).

---

## Economic rationale

> Reconciling as-built plant records, OTDR traces and per-subscriber power readings across a
PON hub is a 4-to-6 hour manual job for a field engineer, and mis-localising a single degraded
splice dispatches a splice crew to the wrong access point at roughly $1,800 per truck roll;
automating this reconciliation removes that engineering time and prevents the wasted dispatch
while three subscribers are already below the service threshold and accruing SLA credits.

---

## Input files — all five are **Tasker-generated**, leave both URL boxes empty

1. `ODN-FDH14-R3.pdf` — the SVA (as-built drawing)
2. `OSP-207_RevE_Optical_Loss_Budget.pdf` — the standard
3. `FCN-2291 Leg C Rediversion.docx` — the field change notice
4. `otdr_export_fdh14_20260302.csv` — OTDR events
5. `ONT_Power_Survey_FDH14.xlsx` — subscriber power readings

All confidentiality checkboxes are honestly true: the network is invented, there is no real or
personal data, no employer work product, nothing requiring anonymisation.

---

## The answer (for grading trajectories yourself)

Run `python3 task36/reference_answer.py`. It prints every correct value **and** exactly what a model
that falls into each trap will produce — which is what the Model Failure Justification is written
from.

- 16 ONTs: **8 PASS, 4 MARGINAL, 4 FAIL**. 8 exceed the 1.00 dB tolerance.
- **FLT-01** — ONT-C-03, drop-side excess loss. FAIL, 1 subscriber, SLA exposure 6.
- **FLT-02** — Leg D, fusion splice at 5.90 km (2.91 dB vs 0.10 dB). FAIL, 3 subscribers, exposure 5.
- **FLT-03** — Leg B, mechanical splice at 3.20 km (2.21 dB vs 0.30 dB). MARGINAL, 4 subs, exposure 4.

Target band: **10–60% correct**. Above 60% and the task is still too easy.

---

## Rebuilding the input files

One source of truth, so the five attachments can never disagree with each other or with the answer.

```bash
cd task36
python3 make_sva.py        # -> attachments/ODN-FDH14-R3.pdf   (the SVA)
python3 make_files.py      # -> standard, change notice, OTDR export, power survey
python3 lint_artifacts.py  # checks for the tells that get artifacts rejected
python3 reference_answer.py
```

Change a number in `task36/model.py` and rerun — every file updates together.

`lint_artifacts.py` enforces the project's rejection catalogue: no "AI blue" palette, no input file
naming another input file, no AI-default entity names, no banned phrases, no future dates, no
markdown in the prompt.

**If the prompt or any file changes, all three trajectories must be rerun.**
