# Telecom/Network_36_TEXT — Project Rose

Working repo for one Mercor Project Rose task. Everything that has to be typed into RL Studio is
reproduced below so it can be copied straight off a phone.

**Studio task:** https://studio.mercor.com/annotator/tasks/task_7290b7c2659f417cafd0871eef0b0d8e/

---

## Status

| Step | State |
|---|---|
| SVA approved by Mark B (as PDF) | done |
| 4 input files uploaded to Studio | done |
| Prompt entered in Studio | **not saved — retype it** |
| Economic rationale entered | **not saved — retype it** |
| File Input Source (4 items) | 1 of 4 done |
| Confidentiality checkboxes (4) | not ticked |
| Auto QCs (Prompt, Attachments, Framing) | not run |
| URL Checker | not run |
| 3 trajectories (Gemini 3.5 Flash) | not run |
| Model Failure Justification | not written |
| Submit for Prompt Review | not done |

Studio's editor silently drops pasted text. **After pasting anything, hit Save Changes, reload the
page, and check it is still there.**

---

## The prompt (paste into the User message box)

> Analyze the four attached plant records for fibre distribution hub FDH-14 on a Gigabit Passive Optical Network (GPON) access network and produce an optical fault remediation memo as plain text in your response. Conduct your analysis as of 2 March 2026.
>
> The attached files are ODN-FDH14-R3.pdf (as-built plant record: network schematic, segment record, and splice schedule), OSP-207_RevD_Optical_Loss_Budget.pdf (component loss values, acceptance thresholds, measurement tolerance, and the OTDR test method), otdr_export_fdh14_20260302.csv (optical time-domain reflectometer (OTDR) events for each distribution leg), and ONT_Power_Survey_FDH14.xlsx (drop lengths and measured received power for each optical network terminal (ONT)).
>
> Carry out the following analysis.
>
> Calculate, for every ONT in the readings file, the design end-to-end path loss from the optical line terminal (OLT) to that ONT. Build the path from the as-built record and price each element using the loss values in the standard. A complete path comprises the feeder segment, the 1:8 primary splitter at the FDH, the distribution leg serving that subscriber, the 1:4 splitter at the multiport service terminal (MST), the subscriber drop, and every fusion splice, mechanical splice, and mated connector pair on that path. Derive the design received power at each ONT from the commissioned OLT transmit power.
>
> Classify each ONT against the acceptance thresholds in the standard using its measured received power.
>
> Compute, for each ONT, the discrepancy between its measured path loss and its design path loss, and identify which ONTs exceed the measurement tolerance defined in the standard.
>
> Reconcile the OTDR events against the splice schedule to identify every plant component whose measured loss exceeds its design value. Report each such component by distribution leg, distance from the FDH, component type, measured loss, and design loss.
>
> Determine, for each group of affected subscribers, whether the excess loss sits in shared distribution plant or downstream of an MST, and state the evidence that establishes this.
>
> Rank the faults for remediation. Order by severity first, placing FAIL ahead of MARGINAL; then by the number of subscribers affected, in descending order; then by the lowest measured received power.
>
> Express every optical loss in decibels (dB) and every optical power in decibel-milliwatts (dBm), each to two decimal places. Drop lengths are recorded in metres and must be converted before being combined with per-kilometre attenuation.
>
> Structure the memo to these requirements. Use exactly four sections, with these headings, in this order and this wording: "1. FAULT SUMMARY", "2. PER-SUBSCRIBER OPTICAL BUDGET", "3. FAULT LOCALISATION", "4. REMEDIATION ORDER". Render section 2 as a pipe-delimited plain-text table whose columns are, in order: ONT ID | Design Loss (dB) | Design Rx (dBm) | Measured Rx (dBm) | Discrepancy (dB) | Classification. Render section 4 as a numbered list with one fault per line, each line beginning with a fault identifier of the form FLT-01, FLT-02, and so on in rank order. Use no bullet points and no bold or italic markup anywhere in the memo. Keep the memo under 900 words.

Plain-text copy: [`task36/prompt.txt`](task36/prompt.txt) — 3,207 characters (limit is 500–4,500).

---

## Economic rationale (paste into its box)

> Reconciling as-built plant records, OTDR traces and per-subscriber power readings across a PON hub is a 4-to-6 hour manual job for a field engineer, and mis-localising a single degraded splice dispatches a splice crew to the wrong access point at roughly $1,800 per truck roll; automating this reconciliation removes that engineering time and prevents the wasted dispatch while three subscribers are already below the service threshold and accruing SLA credits.

---

## File Input Source — all four are **Tasker-generated**, leave both URL boxes empty

1. `ODN-FDH14-R3.pdf`
2. `OSP-207_RevD_Optical_Loss_Budget.pdf`
3. `otdr_export_fdh14_20260302.csv`
4. `ONT_Power_Survey_FDH14.xlsx`

All four confidentiality checkboxes are honestly true: the network is invented, there is no real or
personal data, no employer work product, nothing requiring anonymisation.

---

## The answer (for grading trajectories yourself)

`python3 task36/reference_answer.py` prints every correct value. Summary:

- 16 ONTs: **8 PASS, 5 MARGINAL, 3 FAIL**. 8 exceed the 1.00 dB tolerance.
- **FLT-01** — Leg D, fusion splice at 5.90 km. 2.91 dB measured vs 0.10 dB design. FAIL, 3 subscribers.
- **FLT-02** — Leg B, mechanical splice at 3.20 km. 2.21 dB vs 0.30 dB design. MARGINAL, 4 subscribers.
- **FLT-03** — ONT-C-03, excess loss on the drop side. MARGINAL, 1 subscriber.

Target band for the model: **10–60% correct**. The expected miss is **FLT-03** — Leg C's OTDR trace is
clean, so the fault has to be downstream of MST-C, where the OTDR cannot see. A model that reasons
only from the OTDR will not find it.

Two traps guard against lucky guesses: Leg D's fault is a *fusion* splice sitting next to a healthy
*mechanical* one, while Leg B's fault *is* its mechanical splice — so neither "mechanical splices are
the weak ones" nor its opposite survives both legs.

---

## Rebuilding the input files

Everything is generated from one source of truth, so the four attachments can never disagree with
each other or with the answer above.

```bash
cd task36
python3 make_sva.py        # -> attachments/ODN-FDH14-R3.pdf   (the approved SVA)
python3 make_files.py      # -> the standard, the OTDR export, the power survey
python3 lint_artifacts.py  # checks for the tells that get artifacts rejected
python3 reference_answer.py
```

Change a number in `task36/model.py` and rerun — every file updates together.

`lint_artifacts.py` enforces the project's rejection catalogue: no "AI blue" palette, no input file
naming another input file, no AI-default entity names, no banned phrases, no future dates, no
markdown in the prompt.

**If the prompt or files change, all three trajectories must be rerun.**
