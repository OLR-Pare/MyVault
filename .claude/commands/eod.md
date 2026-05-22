---
description: "End of day — interview, Lark calendar review, and chat scan to surface missed context before /gn"
---

**Before starting:** Read `CLAUDE.md` → find `## Vault Map` → parse the YAML. Use those paths for every folder reference below. If no Vault Map exists, use the default paths shown in parentheses.

End-of-day **gathering**. Surface everything that happened today that isn't already in the vault. Run `/gn` afterward to execute the journal update and cascades.

---

## Step 1: Pull today's Lark calendar

```bash
lark-cli calendar +agenda
```

Present today's events in a clean table: time, title, organizer. This is the scaffold for Steps 2 and 3.

---

## Step 2: Auto-process all recorded meetings

Invoke `lark-minutes-debrief` in auto-discovery mode — it reads the Lark meeting bot chat, finds all `/minutes/` URLs from today, and processes each one end-to-end (transcript → meeting note → people interaction logs → cascades).

```
Skill: lark-minutes-debrief
(auto mode — no URLs needed)
```

After it runs, cross-reference the results against the calendar:
- Mark meetings that were **processed** (recording found + note created)
- Mark meetings that are **unrecorded** (on the calendar but no transcript)

---

## Step 3: Interview unrecorded meetings only

For each meeting the debrief couldn't cover, ask conversationally. **One meeting at a time.**

Extract per meeting:
- Who was there?
- What was the main topic / what got decided?
- Any action items? (who, what, by when)

After going through all unrecorded meetings, ask:
> "Anything else today not on the calendar — quick calls, chat decisions, ideas, anything notable?"

---

## Step 4: Scan Lark chats (last 24h)

Find relevant chats using **two signals** — no manual labeling required.

### Signal A: Project name matching

1. Collect active project and pitch names from the vault:
   - Recursively list all subfolder names under `{projects}/` (default: `🚀 Projects/`) — these are the project and client names
   - Also pull active project names from `{brain}/Memory.md` (default: `🧠 Brain/Memory.md`) (the Active Strategic Context section)
   - Deduplicate and use each name as a search keyword

2. Search Lark for matching chats:
   ```bash
   lark-cli im +chat-search --keyword "<project name>" --page-size 5
   ```

3. Also collect any `lark-chats:` IDs already in project Brief/Charter frontmatter.

### Signal B: User's own activity today

Find chats where the user personally sent messages today — look up your Lark open ID from `{brain}/User.md` (default: `🧠 Brain/User.md`):
```bash
lark-cli im +messages-search \
  --sender-id "<your-lark-open-id>" \
  --start-time "<today 00:00 ISO>" \
  --page-size 50
```

### Scan and filter

For each unique chat ID found:
```bash
lark-cli im +chat-messages-list --chat-id <id> \
  --start "<today 00:00 ISO>" --sort asc --page-size 50
```

Skip chats with no messages today. Skip chats for meetings already processed in Step 2.

**Surface only:**
- Decisions: "deal", "confirmed", "go ahead", "let's do", "approved" — add your team's local language equivalents
- Action items: "please", "follow up", assigned to someone — add local language equivalents
- Client signals: updates from client-side contacts, pricing, timeline changes
- @mentions of the user
- Status changes on active projects

Group by project. Summarize in English. No raw message dumps, no logistics/small talk.

---

## Step 5: General check-in

After calendar + chats are covered, ask:
> "Any challenges or blockers worth logging?"
> "Any decisions we haven't captured yet?"
> "Anything that shifted your priorities for tomorrow?"

Keep it light — one sentence answers are fine.

---

## Step 6: Confirm and hand off

Summarize what was gathered:
- Meetings auto-processed via Lark transcript
- Unrecorded meetings covered via interview
- Lark chats scanned + notable signals found
- New action items surfaced

Then prompt:
> "Run `/gn` to lock everything into the vault."

---

## Notes

- **Language rule:** All vault content in English. Translate if the conversation happened in another language.
- **Don't create vault files in this step** — that's `/gn`'s job. Lark minutes debrief is the exception: it writes its own notes as part of its skill.
- **If a Lark minutes URL is shared** at any point → invoke `lark-minutes-debrief` on it immediately before continuing.
- **Chat scan scope:** 5–10 most relevant chats. Focused, not exhaustive.
