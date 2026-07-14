---
name: rose-artifact-check
description: Vet a planned or uploaded set of Project Rose attachments (input files + Structured Visual Artifact) against the project's sourcing and quality rules before the user commits to them. Use when the user asks whether a file/image/source is allowed, where to get artifacts, or wants their attachment set reviewed.
---

# Rose Artifact Check — attachment and SVA vetting

Given the user's description of their files (or the files themselves — ask them to drop copies in this directory,
or inspect the task's Attachments section via Chrome MCP on port 9222), grade each item against these gates and
report pass/fail per gate with a fix.

## Set-level gates

1. ≥3 files total; exactly one primary output type will be requested; file formats are varied (.pdf/.xlsx/.docx/.csv/image).
2. Exactly one file qualifies as the Structured Visual Artifact (SVA) — or more, but at least one.
3. No file reused from any previous task or project (hard rule).
4. If the task name carries a token requirement, total input tokens reach it (use the RLS token count tool).
5. Native formats only: spreadsheet as .xlsx/.csv (never embedded in a PDF), image as .jpg/.png. Check against the
   allowed-types sheet: https://docs.google.com/spreadsheets/d/1gwsVKFZVNYVYej4xi6sV3bvmF4QX4_9v9p9kH1UIsx8
6. Filenames: spaces are allowed; the prompt must reference exact filenames.

## Per-file source gates

- **Sanitized own document:** PII stripped, org names anonymized, figures/dates/identifiers changed, proprietary pages
  removed. The 4 confidentiality checkboxes must be truthful.
- **Web-sourced:** credible source, no paywall, passes URL Checker, and NOT easily searchable — test by googling the key
  figures/conclusions the rubric will grade; verbatim hit on a top result = fail. Record file_url + containing page URL.
- **Self-made (tasker-generated):** professional caliber; no screenshots-of-screens, no rotated/blurry photos, no
  handwriting unless professionally realistic.
- **Gemini Deep Research output:** the ONLY allowed AI source; net-new document, no PII, user verified every claim.
  Any other AI-generated content — especially images — is an automatic fail.

## SVA-specific gates

- Requires synthesis: not solvable by reading/transcribing/counting/identifying alone; must be integrated with the
  other files or across its own parts.
- Not perception-gated: legible, measurable data points, labeled axes/elements, clear color demarcation; difficulty
  comes from reasoning, not eyesight.
- Realistic to Telecom/Network professional work (topology diagrams, rack/port maps, RF coverage plots, SLA dashboards,
  alarm/event tables, circuit layout records…). Too simple gets sent back (a Canva legacy-topology diagram in this
  domain was returned for insufficient complexity).
- Reminder: the SVA must be posted with a 1–2 sentence use-case note in **#rose-telecom-and-network-b78** for approval
  by [EXP] Mark B BEFORE the task is built around it. Offer to draft that Slack post (process text is fine).

## Output

A table: file → source category → gates passed → gates failed → concrete fix. End with an overall verdict:
ready to upload / fix first / rethink the set. Do not fabricate or generate replacement artifacts yourself.
