---
description: "Good night — vault execution: journal, meeting notes, cascades, Memory and Brain updates"
---

**Before starting:** Read `CLAUDE.md` → find `## Vault Map` → parse the YAML. Use those paths for every folder reference below. If no Vault Map exists, use the default paths shown in parentheses.

End-of-day **execution**. Takes all context from the current session and locks it into the vault.

> **This is not the interview.** Run `/eod` first to gather context from your calendar, meetings, and Lark chats. `/gn` just writes.

If you skipped `/eod`, that's fine — run `/gn` with whatever was discussed in this session and it will work from that context.

---

## Step 0: Journal gap check (run BEFORE writing today's journal)

Check for skipped days so context from missed dates does not get lumped into today's file:

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
- **Gap 0-1:** proceed to Step 1 normally.
- **Gap 2-3:** ask the user: "You missed [list days]. Stub them as gap files, or fold context into today?" Default to **stub** if no answer.
- **Gap 4+:** auto-stub each missed day silently.

For each gap day, create a stub at `{journals}/YYYY/MM MMM/YYYY-MM-DD • ddd.md` with `status: gap` frontmatter per the protocol. **Do NOT** run the reflection interview, People cascades, or Memory updates on stub days. Cascades only run for today. Skip silently if no prior journal exists.

---

## Step 1: Update today's daily journal

Path: `{journals}/YYYY/{journals_format}.md` (default: `📓 Journals/YYYY/MM MMM/YYYY-MM-DD • ddd.md`)

```bash
mkdir -p "{journals}/YYYY/MM MMM"   # substitute actual values at runtime
```

- **If journal exists:** fill in any empty sections. Merge session context into Notes, Highlights, Challenges, Reflection.
- **If journal doesn't exist:** create it using the Journal Template:
  `Check-in → 📝 Notes → Highlights → Challenges → Lessons Learned → Reflection`
- **📝 Notes section:** detailed daily context — meetings attended, decisions made, ideas explored, things learned. Tag with relevant hashtags for your projects and areas (e.g. #work, #personal, #ideas).
- **Language rule:** all vault content in English, even if the conversation happened in another language.

---

## Step 2: Create meeting notes for uncaptured meetings

For each meeting discussed in this session that doesn't have a vault note yet:
- **Project meeting** → `{projects}/<path>/Meetings/YYYY-MM-DD <Title>.md` (default: `🚀 Projects/`)
- **Pitch meeting** → update or create the pitch Brief under `{projects}/<Client>/Pitches/<Name>/`
- **Orphan meeting** (no clear project home) → `{meetings_orphan}/YYYY-MM-DD <Title>.md` (default: `🤝 Meetings/`)

---

## Step 3: Cascading updates

Update all notes touched or referenced today:
- `{people}/` profiles (default: `👤 People/`) — add to Interaction Log for anyone mentioned
- `{projects}/` notes (default: `🚀 Projects/`) — update status and log for any project discussed
- `{todo}` (default: `📥 Inbox/To-Do.md`) — mark completed items, add new action items
- `{brain}/Memory.md` (default: `🧠 Brain/Memory.md`) — update active project context and status

---

## Step 4: Update 🧠 Brain/ if applicable

- `{brain}/Decisions.md` — log any decisions made today
- `{brain}/Patterns.md` — record any new patterns or principles surfaced
- `{brain}/Gotchas.md` — note any mistakes or pitfalls learned
