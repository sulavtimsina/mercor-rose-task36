---
name: rose-help
description: Answer any Project Rose question — what a rule is, whom to ask, or where to post. Use whenever the user asks "can I…", "who do I ask about…", "where do I post…", "what's the rule for…", or anything about Project Rose guidelines, pay, contacts, attachments, prompts, rubrics, or reviews.
---

# Rose Help — rules, routing, and contacts

Answer from project sources in this order; cite which source you used.

1. **CLAUDE.md** in this directory — condensed rules, pipeline, contact table.
2. **rose-instructions.txt** in this directory — full instructions doc dump. Grep it for the specific topic
   (e.g. `grep -n -i "searchable" rose-instructions.txt`). This is the authoritative text.
3. **Live sources via Chrome MCP (port 9222)** when the question concerns something recent or ambiguous:
   - #rose-announcements for policy changes (the doc changelog lags Slack sometimes).
   - #rose-questions: search whether @Maven already answered it; Maven's answers cite the guidelines.
   - The instructions doc itself may have been updated — reload
     https://docs.google.com/document/d/1zN-0wCzCKtJeyCNlWQIYC9ylUKfjOvdDKGAnuDDGs48/mobilebasic and re-dump
     to rose-instructions.txt if its "Last updated" date is newer.

## Routing answers ("whom should I ask / where should I post")

Use the contact table in CLAUDE.md. Defaults:
- Domain/task judgment or SVA approval → post in **#rose-telecom-and-network-b78** and tag **[EXP] Mark B**.
- Generic guideline question → post in **#rose-questions** and tag **@Maven** (the AI bot) first; humans follow up.
- Tool broken / access issue → **#rose-tech-help**.
- Always: public channel over DM, include the task link, one question per message thread.

If the user asks you to draft the actual Slack message, that's fine (process communication, not task content).

## Hard boundaries

If the answer isn't in the sources, say so and tell them exactly where to post the question (usually @Maven in
#rose-questions) rather than guessing.
