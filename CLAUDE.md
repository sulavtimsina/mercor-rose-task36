# Project Rose (Mercor) — Working Knowledge Base

The user is a **task writer** on Mercor's Project Rose, domain **Telecom/Network**, working in RL Studio
(https://studio.mercor.com, world `world_da784f3a95e34a4faed4ad20ec98d590`). Access is provisioned via Okta.
A Chrome debug profile with all logins lives on port 9222 (launch command in memory: chrome-9222-mercor-debug-profile).

Full instructions doc: [EXP] Project Rose - Instructions
https://docs.google.com/document/d/1zN-0wCzCKtJeyCNlWQIYC9ylUKfjOvdDKGAnuDDGs48
A local text dump is at `rose-instructions.txt` in this directory — grep it for details before answering guideline questions.

## What a task is

Prompt + ≥3 input files + economic rationale + proven model failure (Step 1), then golden response + 40+ criteria
true/false rubric (Step 2). Tasks are pre-seeded; the user CLAIMS one (never creates from scratch). Task names follow
`Industry_TaskNumber_OutputType` (e.g. `Telecom/Network_36_TEXT`); the prompt MUST explicitly request the output type
in the name. Average total effort ~15 hours per task.

**Limits:** only 1 task until the first is fully Approved (mandatory quality check on task #1); max 2 in progress after
that. Task status must move at least every 24h. Log ALL writing time in Insightful (pay is per-task, timer still required;
reviewers must NOT run the timer while writing).

## Pipeline (Step 1 — Prompt Writing)

1. Claim a `Seed Status` task in the Telecom/Network world ("Claim Task for Prompt Writing").
2. Design the scenario. It must pass three tests: Realistic Workflow (a real telecom professional would hand this
   exact prompt + files to an AI), Economic Value (saves hours of paid skilled work / drives a decision), Objectivity
   (99 of 100 domain experts reach the identical answer). ≥5 distinct units of work, NOT all chained.
3. **Post the Structured Visual Artifact (SVA) to #rose-telecom-and-network-b78 for approval BEFORE building the task**,
   with 1–2 sentences on the use case. Required step — skipping it risks a send-back.
4. Upload ≥3 attachments (one = the SVA), varied native formats (.pdf, .xlsx, .docx, .csv, images). Fill in
   Task Input File Source for every file (Tasker-generated / Web not modified / Web modified + file_url and page URL),
   run the **URL Checker** on web-sourced files.
5. Write the prompt: 500–4,500 chars, action-oriented, references files by exact filename, defines jargon on first use
   ("full phrase (ACRONYM)"), timeless ("as of <date>", never "today"), exactly ONE output type, no URLs, no persona or
   scene-setting. Write the 1-sentence economic rationale (monetary/time savings).
6. Run **Prompt Auto QC**, resolve flags, rerun 2–3× (LLM-based, noisy). Disagree with a flag → thumbs-down + explain.
7. Run **3 trajectories** with Gemini 3.5 Flash (run 1 first to sanity-check failure, then the other 2). Grade the
   output YOURSELF — there is no auto-score at this stage; a 0% grading readout is meaningless. File outputs are in the
   "Diff" card. Target: model averages **10–60% correct** across the 3 runs, with ≥1 content criterion met in ≥1 run.
   Model too good → add real-world complexity. All 3 runs exhaust 100 steps → flag to Mark B, then Molly Meehl.
   Changed the prompt or files → rerun all trajectories.
8. Write the Model Failure Justification: tie it to specific verifiable errors in the runs; must show a genuine miss in
   the 10–60% band, not a near-correct answer.
9. Submit for Prompt Review (button unlocks only when Prompt QC + Attachments QC are green).

## Pipeline (Step 2 — after prompt approval; task auto-moves to Rubric Writing)

1. Golden response in the Golden Response section: verify EVERY claim against the attachments (you may start from a
   model draft in RLS but must correct everything). Run GR Auto QC, resolve, rerun.
2. Rubric: 40+ true/false criteria, ~75% correctness / ~25% design, every prompt request covered by ≥1 criterion.
   Spreadsheet view is easiest. Google Sheets import exists but export the template FIRST — hand-built sheets with wrong
   headers/tags/brackets break the import. Run Rubric Auto QC, resolve, rerun.
3. Judge grading: each trajectory → New Grading Run → Gemini 3.1 Pro → Run. All 3. Average must stay ≤60% or the task
   is too easy (add complexity, update GR + rubric).
4. Noisy Rubric Check: 3 grading runs; if ≥10% of criteria flip pass/fail between runs, tighten wording and rerun.
5. All Auto QCs green (Prompt, Attachments, Golden Response, Rubric, Task Metadata, Submission Foundations) →
   Submit for Task Review.

**Revisions:** feedback is in the Review card at the bottom + reviewer checklist in the right sidebar. Respond in the
Writer Comment Box. Prompt changed → rerun trajectories; always rerun all Auto QCs, judge grading, noisy rubric check,
then "Send for re-review". **Approved = done** — QC stages after that need no writer action.

## Attachment / artifact rules (most send-backs happen here)

Allowed sources:
- Own professional documents, SANITIZED: strip PII, anonymize org names, change figures/dates/identifiers, drop
  proprietary pages. 4 confidentiality checkboxes must be honest.
- Public web documents from credible sources (vendor spec sheets, equipment manuals, standards excerpts, FCC/OSHA/USPTO
  filings) — must pass the URL Checker and must NOT be easily searchable (if googling the rubric's key figure finds the
  answer verbatim on a top result, disqualified).
- Self-made files: diagrams you drew (Canva OK), photos of worksheets, spreadsheets you built → "Tasker-generated".
- **Gemini Deep Research is the ONLY allowed AI source** — for net-new closed-source input documents (memos, reports,
  synthetic non-visual data with no PII). Verify contents yourself.

Never allowed: AI-generated images; screenshots of computer screens; rotated/illegible photos; spreadsheets embedded in
PDFs (native formats only); reusing files from any previous task/project; real brand logos; handwriting on inputs unless
professionally realistic. Allowed file types list:
https://docs.google.com/spreadsheets/d/1gwsVKFZVNYVYej4xi6sV3bvmF4QX4_9v9p9kH1UIsx8

SVA requirements: synthesis required (not solvable by reading/transcribing/counting/identifying alone), realistic to the
domain, not perception-gated (no tiny text, near-identical colors, counting, reverse-image identification).

## Inspiration policy
(Task Scenario Ideas sheet is for inspiration only: https://docs.google.com/spreadsheets/d/1E1yOi7QCWKhDCbeBTComzQ7np54eXfpw7nYBmOT77jU)

## Who to contact / where to post

| Question | Where / who |
|---|---|
| Task ideas, SVA approval, domain judgment calls | #rose-telecom-and-network-b78, tag **[EXP] Mark B** (Domain Lead — always first contact) |
| General guidelines, best practices | #rose-questions, tag **@Maven** (AI bot, answers with citations) first |
| Studio access/bugs, Okta, Insightful tech issues | #rose-tech-help; escalation: Arnesh Issar or Ashish Chavan (TPMs) |
| Reviewer process, review quality | [EXP] Gina B (Reviewer TL) |
| Onboarding/enablement | [EXP] Kandace M (Enablement TL) |
| Project-level decisions, escalations (e.g. 100-step failures after DL confirms) | Molly Meehl (Project Coordinator) |
| Payment, Insightful tracking, tax | support@mercor.com |
| Personal commitments, project concerns | Harwinder Singh / Viktor Dombrovskiy (SPLs) |

Post in public channels (tag the person) rather than DM; include the task link when asking about a task.
Away >3 days → tell the project team.

## Pay

First task: fixed price per approved task. After a quality first task: option to convert to hourly, or stay per-task.
Bonuses: $150 onboarding (after first task approved), prompt one-shot and rubric one-shot bonuses (approved on first
review). Payments process Wednesdays via Stripe.

## When helping the user

- Before answering a guideline question, check `rose-instructions.txt` here, then Slack (@Maven answers are citable).
- To look at their live task, use the Chrome MCP tools on port 9222 (Studio, Slack, Gmail, Okta are logged in).
- Today's date matters: verify against announcements in #rose-announcements for policy changes (doc changelog updates often).
