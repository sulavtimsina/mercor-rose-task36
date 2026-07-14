---
name: rose-next-step
description: Figure out where the user's Project Rose task currently stands and tell them the exact next step, flagging anything they skipped. Use when the user asks "what's next", "did I miss anything", "what do I do now", or wants a status check on their task.
---

# Rose Next Step — pipeline position and missed-step audit

## 1. Determine the live state

Use Chrome MCP on port 9222. Open the Studio tasks page
(https://studio.mercor.com/annotator/tasks/?world_id=world_da784f3a95e34a4faed4ad20ec98d590), find the user's task
(Created By = their [EXP] name), and read its **Task Status**. If they have a task open in a tab, prefer that tab.
Open the task page itself to check section-level state (attachments count, QC badges, trajectory runs, review card).

## 2. Map status → required actions

- **Seed Status (none claimed yet):** claim ONE task (first task must be approved before a second). Then SVA approval
  in the domain channel BEFORE building.
- **Prompt Writing:** in order — SVA posted+approved in #rose-telecom-and-network-b78 → ≥3 attachments uploaded, native
  formats, one is the SVA → source info per file → URL Checker passing → prompt written (checklist in CLAUDE.md §Step 1
  item 5) → economic rationale → Prompt Auto QC green (rerun 2–3×) → 3 trajectories with Gemini 3.5 Flash → self-graded
  failure in 10–60% band with ≥1 content criterion met in ≥1 run → Model Failure Justification → Submit for Prompt Review.
- **In Prompt Review / Awaiting Prompt Review:** nothing to do; do NOT start another task.
- **Prompt Needs Edits:** read Review card + right-sidebar reviewer checklist → revise → if prompt/files changed, RERUN
  all 3 trajectories → rerun affected Auto QCs → reply in Writer Comment Box → Submit for Prompt Review again.
- **Rubric Writing (prompt approved):** golden response (verify every claim) → GR Auto QC → 40+ T/F rubric criteria
  (~75/25 correctness/design) → Rubric Auto QC → judge grading with Gemini 3.1 Pro on all 3 trajectories (avg ≤60%) →
  Noisy Rubric Check (<10% criteria flipping) → all 6 Auto QCs green → Submit for Task Review.
- **In Revision:** same as Prompt Needs Edits but also rerun judge grading + noisy rubric check → Send for re-review.
- **Approved:** done — review reviewer edits, then claim the next task (max 2 in progress from now on).

## 3. Missed-step audit (run every time)

Check and call out explicitly, pass/fail:
- Insightful timer running while they work? (Writers must log all time.)
- SVA posted to the domain channel for approval before deep work?
- Source info filled for EVERY attachment + URL Checker run on web files?
- Any file reused from a previous task/project? (Forbidden.)
- AI-generated image anywhere in inputs? (Forbidden; only Gemini Deep Research docs allowed.)
- Trajectories rerun after any prompt/file change?
- Auto QCs rerun 2–3× after the last edit?
- Task status stagnant close to 24h? (Automated warnings → removal risk.)
- Anything unclear in reviewer feedback → Writer Comment Box / DM the reviewer, not silence.

## 4. Output format

Tell them: current status → the single next action → then the ordered remaining steps → any missed-step flags.
