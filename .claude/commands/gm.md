---
description: "Good morning — comprehensive daily briefing: calendar, tasks, active projects, priorities"
---

**Before starting:** Read `CLAUDE.md` → find `## Vault Map` → parse the YAML. Use those paths for every folder reference below. If no Vault Map exists, use the default paths shown in parentheses.

Morning briefing. Pull everything needed to start the day with full context. Be concise — this is a briefing, not a report.

---

## Step 0: Journal gap check

Before pulling calendar, check for skipped days. Find the most recent journal file under `{journals}` (default: `📓 Journals/`):

```bash
LATEST=$(find "📓 Journals" -type f -name "*.md" 2>/dev/null \
  | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' \
  | sort -u | tail -1)
TODAY=$(date +%Y-%m-%d)
if [ -n "$LATEST" ]; then
  GAP=$(( ( $(date -j -f "%Y-%m-%d" "$TODAY" +%s) - $(date -j -f "%Y-%m-%d" "$LATEST" +%s) ) / 86400 ))
  echo "Last journal: $LATEST | Today: $TODAY | Gap: $GAP days"
fi
```

Apply [[Journal Gap Protocol]] (lives in `{brain}/Journal Gap Protocol.md`):
- **Gap 0-1:** continue normally to Step 1.
- **Gap 2-3:** ask the user: "You missed [list days]. Stub them as gap-marker files, or fold context into today?" Default to **stub** if no answer.
- **Gap 4+:** auto-stub each missed day silently, then proceed.

For each gap day, create a stub at `{journals}/YYYY/MM MMM/YYYY-MM-DD • ddd.md` per the stub format in the protocol. **Do NOT** run reflection or cascades on stub days. Skip silently if no prior journal exists (first-time user).

---

## Step 1: Pull today's calendar

```bash
lark-cli calendar +agenda
```

List today's events in a clean table: time, title, organizer. Flag any that look like they need prep (pitches, client meetings, key decisions).

---

## Step 2: Pull open Lark tasks

```bash
lark-cli task +my-tasks --due-mode today 2>/dev/null || lark-cli task +my-tasks --limit 20
```

Surface any tasks due today or overdue. Group by project if possible.

---

## Step 3: Read vault context

Read these three files:
- `{brain}/Memory.md` (default: `🧠 Brain/Memory.md`) — active projects and strategic context
- `{todo}` (default: `📥 Inbox/To-Do.md`) — open action items (focus on 🔴 This Week section)
- `{brain}/North Star.md` (default: `🧠 Brain/North Star.md`) — current goals and priorities

---

## Step 4: Synthesize the briefing

Output a structured morning brief with these sections:

**📅 Today's Calendar**
List meetings with time + one-line context if relevant (e.g. "pitch", "internal", "client checkpoint"). Flag any that need immediate prep.

**✅ Tasks Due Today**
From Lark tasks + To-Do.md. Only what needs action today or is overdue.

**🔥 Active Projects — Key Watch Items**
From Memory.md — 3–5 bullet points on the most important active threads. What's moving, what's blocked, what needs a decision.

**🎯 Suggested Top 3 for Today**
Based on calendar + tasks + active projects — what are the 3 highest-leverage things to focus on? Keep it sharp, not a laundry list.

**⚠️ Flags**
Anything urgent, overdue, or at risk of slipping that deserves attention before anything else.

---

## Notes

- Be concise. The user is starting their day — don't overwhelm.
- If calendar or tasks fail to pull, note it and continue with vault context.
- Don't re-read yesterday's journal unless something in the active context specifically requires it.
