---
name: lark-minutes-debrief
description: Use when the user shares one or more Lark or Feishu meeting minutes URLs containing `/minutes/`, OR when the user says "lark minutes debrief", "debrief today's meetings", "debrief my meetings", or similar without providing URLs — in that case auto-discover today's meetings from the Lark meeting bot chat.
---

# Lark Minutes Debrief

Process one or more Lark meeting minutes end-to-end: fetch → analyze → classify → write notes → update people.

Two modes:
- **Manual** — user pastes one or more `/minutes/` URLs → skip to Step 1
- **Auto** — user says "lark minutes debrief" with no URLs → run Step 0 first to discover today's meetings

---

## Configuration

Auto-discovery (Step 0) requires the Lark meeting bot chat ID. Set it in `🧠 Brain/User.md` under a `lark_meeting_bot_chat_id` field, or hardcode it below.

**Current value:** `YOUR_MEETING_BOT_CHAT_ID`

> **How to find your chat ID:** In Lark, open the chat where the meeting recording bot posts notifications (usually named something like "Meeting Recordings" or "Lark VC Bot"). Ask Claudian: *"what is the chat ID for this Lark group?"* — or run `lark-cli im +chat-search --keyword "meeting"` to find it.
>
> Once you have it, replace `YOUR_MEETING_BOT_CHAT_ID` above, or set `lark_meeting_bot_chat_id: oc_xxx` in `🧠 Brain/User.md`. Until configured, Step 0 will ask you to paste the URL manually.

---

## When to Use
- User shares URLs containing `/minutes/` on any Lark or Feishu tenant
- User says "lark minutes debrief", "debrief today's meetings", "debrief my meetings" (no URL needed — uses auto-discovery if chat ID is configured)
- Multiple URLs at once → batch-fetch, then process individually
- URL may be preceded by context ("process this:", "can you debrief:", etc.)

## When NOT to Use
- `/docs/` URLs — use the `lark-doc` skill or workflow
- `/base/` URLs — use `lark-base`
- `/im/` or chat URLs — not a minute
- Future-scheduled events with no transcript yet — tell the user to run after the meeting ends
- Generic meeting notes not sourced from Lark — use the Meeting Note Template directly

---

## Quick Reference

| Step | Action |
|---|---|
| 0 | **Auto mode only** — discover today's minutes URLs from meeting bot chat |
| 1 | Extract token from URL |
| 2 | `lark-cli vc +notes --minute-tokens ...` (batch) + browser fallback if needed |
| 3 | Extract metadata + calendar lookup for attendees |
| 4 | Classify to existing `🚀 Projects/` folder |
| 5 | Determine file path (per project's subfolder convention) |
| 6 | Write meeting note (English) |
| 7 | Update `👤 People/` interaction logs |
| 8 | Cascade to Memory.md, To-Do.md, project notes |
| 9 | Delete `artifact-*` folders from vault root |

---

## Step 0 — Auto-Discovery (skip if user provided URLs)

First, resolve the meeting bot chat ID:
1. Check `🧠 Brain/User.md` for a `lark_meeting_bot_chat_id` field
2. If not set, check the `YOUR_MEETING_BOT_CHAT_ID` placeholder in the Configuration section above
3. If still not configured → tell the user auto-discovery isn't set up yet and ask them to paste the URL manually. Point them to the Configuration section in this skill file.

If a chat ID is found, read today's messages and extract all `/minutes/` URLs:

```bash
lark-cli --profile org-lark-cli im +chat-messages-list \
  --chat-id <CHAT_ID> \
  --start "$(python3 -c "from datetime import datetime, timezone; t=datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0); print(t.strftime('%Y-%m-%dT%H:%M:%SZ'))")" \
  --sort asc --format json | python3 -c "
import sys, re, json
data = json.load(sys.stdin)
seen = set()
results = []
for msg in data.get('data', {}).get('messages', []):
    content = msg.get('content', '')
    for token in re.findall(r'larksuite\.com/minutes/([a-z0-9]+)', content):
        if token not in seen:
            seen.add(token)
            title_match = re.search(r'主题[：:]\s*(.+)', content)
            title = title_match.group(1).strip() if title_match else token
            results.append({'token': token, 'title': title, 'time': msg.get('create_time','')})
for r in results:
    print(f\"{r['time']} | {r['title']} | {r['token']}\")
"
```

**Present the list to the user before proceeding:**

> Found N meeting(s) today:
> 1. HH:MM — [Meeting Title] (`token`)
> 2. HH:MM — [Meeting Title] (`token`)
>
> Process all? Or pick specific ones?

Wait for confirmation. If the user says "all" or gives no objection, proceed with all tokens. If they pick specific ones, use only those.

**If no meetings found:** tell the user the bot chat returned no minutes for today and ask them to paste the URL manually.

---

## Step 1 — Extract Tokens

From each URL like `https://<tenant>.larksuite.com/minutes/obsg5p9d9367d1w3qhn49978`, extract the token (last path segment, ignore `?` query params).

Supported tenant patterns:
- `*.larksuite.com/minutes/<token>`
- `*.feishu.cn/minutes/<token>`
- Any other Lark/Feishu host using the same `/minutes/<token>` convention

---

## Step 2 — Fetch Content

Run all tokens in one batch:

```bash
lark-cli --profile org-lark-cli vc +notes --minute-tokens <token1>,<token2>,...
```

This downloads transcripts to `artifact-<title>-<token>/transcript.txt` in the vault root.

**For each token:**
- If `artifacts.transcript_file` is present → Read the file with the Read tool
- If download failed (HTTP 403, no artifacts) → **fall back to browser**

### Browser Fallback (403 or no transcript)

```
1. Use mcp__claude-in-chrome__tabs_context_mcp (createIfEmpty: true)
2. Navigate to the minutes URL
3. Take a screenshot to see the page layout
4. Click the "Transcript" tab if not already active
5. Read transcript via read_page (ref_id of scrollable content area)
   OR scroll + screenshot to capture content
6. Read enough to identify: title, speakers, key topics, decisions
```

> Note: AI Notes may show "monthly limit reached" — that's fine, use the Transcript tab instead.

### If both CLI and browser fail

Stop. Report to the user which token(s) couldn't be fetched, show the error, and ask whether to skip or retry. **Do not create a meeting note from an empty or failed fetch.**

---

## Step 3 — Identify Meeting Metadata

From the content, extract:
- **Title** — from minutes page or transcript header
- **Date** — from timestamp in transcript (convert to YYYY-MM-DD in the user's local timezone)
- **Duration** — from page header or timestamp range
- **Organizer** — from minutes metadata (`owner_id`) or calendar

### Step 3A — Calendar Lookup (always run this)

Pull the relevant day's agenda once, then match each meeting by title/time:

```bash
lark-cli --profile org-lark-cli calendar +agenda
```

For each matched event, get the authoritative attendee list:

```bash
lark-cli --profile org-lark-cli calendar event.attendees list \
  --params '{"calendar_id": "primary", "event_id": "<event_id>", "user_id_type": "open_id"}'
```

**Use the calendar attendee list as the source of truth** for who was in the meeting — not just named speakers in the transcript (speakers may be a subset, and transcripts may mention people who weren't actually present).

Filter attendees by `rsvp_status`:
- `accept` → confirmed present
- `needs_action` → invited but unconfirmed — only include if they appear as a speaker in the transcript
- `decline` → exclude

If the meeting date is not today, adjust the `+agenda` call with `--date YYYY-MM-DD`.

### If no calendar match found

Fall back to speakers named in the transcript. Flag the uncertainty in the note's frontmatter:

```yaml
attendees_source: transcript  # not calendar-confirmed
```

---

## Step 4 — Classify Project

**The primary home for a meeting note is the related project folder in `🚀 Projects/`.** The orphan bucket `🤝 Meetings/` is a fallback, not a default.

1. List current project folders: `ls "🚀 Projects/"`
2. For each candidate folder, infer its topic from the folder name (and project README if present).
3. Match meeting content against those topics. Build an in-session keyword map, e.g.:

| Keywords / context | Project folder |
|---|---|
| design system, design tokens, component library | `<Design System Project>` |
| LMS, training, curriculum | `<Learning Project>` |
| P&L, financial review, budget | `<Finance Project>` |

4. **Three outcomes:**
   - **Clear match** → file under that project folder (Step 5)
   - **Ambiguous** (2+ plausible matches) → **ask the user** before creating
   - **No match** (no related project exists) → file under `🤝 Meetings/` as orphan (Step 5)
   - Never guess silently

> The sample keywords above are illustrative. The active projects in each user's vault will differ — build the keyword map fresh per session from the current `🚀 Projects/` directory.

---

## Step 5 — Determine File Path

### Path A — clear project match (primary)

**Always file into `🚀 Projects/<ProjectName>/Meetings/`.** Create the `Meetings/` subfolder if it doesn't exist yet.

```bash
mkdir -p "🚀 Projects/<ProjectName>/Meetings"
```

- File path: `🚀 Projects/<ProjectName>/Meetings/YYYY-MM-DD <Meeting Title>.md`
- File name: no em dashes (`—`)
- This applies to all projects regardless of how many meetings they currently have. Consistent structure across all projects.

### Path B — orphan (fallback)

If no project match, file directly in `🤝 Meetings/<Topic> - YYYY-MM-DD.md`. Use this only when the meeting genuinely doesn't belong to an existing project (ad-hoc 1:1, exploratory conversation, cross-cutting discussion).

---

## Step 6 — Create Meeting Note

**Before writing, resolve attendee profiles** (see Step 7 lookup rules below). For each attendee, determine the wikilink if a profile exists, or note them as plain text if not.

**Also resolve company tags:** Identify which `💼 Company/` entities are involved (the project owner + any client/partner counterparties). Add their slug as a tag in frontmatter and link them in `Related`.

**Company page resolution — use the bash snippet, don't eyeball it:**

The `💼 Company/` folder accumulates two layouts as it grows (per vault CLAUDE.md):
- **Flat file:** `💼 Company/<Name>.md` — the default starting point
- **Folder + overview file:** `💼 Company/<Name>/<Name>.md` — once an entity accumulates multiple notes (financials, contracts, etc.) it gets promoted to its own subfolder, with the overview file inside
- **Folder, no overview file:** `💼 Company/<Name>/` with sub-files but no `<Name>.md` — a partial promotion (overview file was never created)

**Empty-stub trap:** when a flat file gets promoted to a folder, the original `💼 Company/<Name>.md` may be left as an empty 0–1-line stub. Obsidian's resolver picks the root file first, rendering the wikilink blank even though the real content lives at `💼 Company/<Name>/<Name>.md`. Always size-check before linking.

**Resolution snippet — run for each involved company before writing the meeting note:**

```bash
resolve_company() {
  local name="$1"
  local folder_overview="💼 Company/$name/$name.md"
  local flat="💼 Company/$name.md"
  local folder="💼 Company/$name"

  # 1. Folder overview file with real content → use short wikilink (Obsidian resolves)
  if [ -s "$folder_overview" ] && [ "$(wc -c < "$folder_overview")" -gt 100 ]; then
    # If a flat shadow exists at root, force explicit path to avoid Obsidian picking the empty file
    if [ -f "$flat" ] && [ "$(wc -c < "$flat")" -lt 100 ]; then
      echo "SHADOW:$flat"  # tell user to delete the empty stub
    fi
    echo "[[$name]]"
    return
  fi
  # 2. Flat file with real content → short wikilink
  if [ -s "$flat" ] && [ "$(wc -c < "$flat")" -gt 100 ]; then
    echo "[[$name]]"
    return
  fi
  # 3. Folder exists but no overview — flag, don't fabricate
  if [ -d "$folder" ]; then
    echo "FOLDER_ONLY:$folder"
    return
  fi
  # 4. Nothing found
  echo "MISSING:$name"
}
```

**Decision rules:**
- `[[Name]]` returned → use as-is in `Related`
- `SHADOW:...` → tell the user an empty stub is shadowing the real page; recommend deleting it. Continue with the link
- `FOLDER_ONLY:...` → tell the user the company has no overview file and ask whether to (a) link the most relevant sub-file, (b) create a stub overview, or (c) skip the link
- `MISSING:...` → flag to user, don't fabricate

> The 100-byte threshold is a sanity floor — real overview files are always 200+ bytes. Anything smaller is almost certainly an empty stub.

**Aliases (future-proofing):** if a company page has an `aliases:` frontmatter field (e.g. `aliases: [Acme Corp, AC]`), the skill should also resolve those when an attendee or speaker uses the alias. Flag to the user to backfill aliases when a misalignment first appears.

Use this format (matching vault conventions):

```markdown
---
type: meeting
date: YYYY-MM-DD
attendees: [Name 1, Name 2, ...]
source: <lark-minutes-url>
tags: [meeting, <project-tag>, <company-slug-1>, <company-slug-2>]
project: <Project Name>
---
# <Meeting Title>

**Date:** YYYY-MM-DD (Day), HH:MM — duration
**Attendees:** [[Person With Profile]], [[Another Person]], Plain Name (no profile)
**Context:** One-line description of why this meeting happened

---

## Summary
[3-5 sentence narrative of what was discussed and decided]

---

## Key Signals
- [Observations, patterns, or notable dynamics]

---

## Key Decisions
- [Concrete decisions made with owner if applicable]

---

## Action Items
- [ ] **Owner:** Task description ← deadline if mentioned

---

## Next Steps
- [What needs to happen next]

---

## Related
- [[OwnerCompany]]            <!-- always link the owner company -->
- [[CounterpartyCompany]]     <!-- if client/partner involved -->
- [[link to project note]]
- [[link to related meeting or doc]]
```

**Frontmatter rules:**
- `attendees`: plain names, no wikilinks (YAML rendering is fragile)
- `tags`: always include `meeting` + project tag + each involved company slug
- Body `**Attendees:**` line: wikilink each person who has a `👤 People/` profile using **short wikilinks** (`[[Name]]`) per vault CLAUDE.md convention. Only use full path with alias if a name collision exists in the vault

Write in **English** regardless of the language of the transcript.

---

## Step 7 — Resolve & Update People

For each named attendee in the meeting, perform fuzzy-tolerant lookup (the same lookup the Step 6 attendee wikilinking depends on):

### Lookup rules (in order)

1. **Exact match:** `Glob "👤 People/**/<Full Name>.md"`
2. **First-name match:** if no exact, glob for `👤 People/**/*<FirstName>*.md` and inspect frontmatter `aliases:` for the full name. Common: people use nicknames or shortened names
3. **Spacing-tolerant match:** strip all whitespace from the candidate name and from each filename, then compare. Catches "Jane Doe Smith" ↔ "Jane DoeSmith", differences in compound surnames, etc.
4. **Aliases scan:** if still unmatched, grep `aliases:` lines across `👤 People/**/*.md` for the candidate name or first-name token
5. **Last resort:** ask the user before declaring "no profile exists" — never create a profile without approval

> When multiple candidates match, ask the user which one. Don't guess.

### Update each matched profile

Read it, then add a row to the **Interaction Log** table:

```markdown
| YYYY-MM-DD | Meeting | <1-line summary of what happened / their role in meeting> | [[path/to/meeting/note]] |
```

### Feed back to Step 6

Return the resolved profile name (or "no profile") for each attendee so Step 6 can wikilink them in the meeting note's `**Attendees:**` line. **Resolve all attendees before writing the meeting note** — don't write first and then come back.

### Unmatched attendees

Flag to the user with a clear list at the end of the run:

> **No `👤 People/` profile yet:**
> - Name 1 (org)
> - Name 2 (org)
>
> Want me to create any of these?

---

## Step 8 — Cascade Updates

- **Memory.md** (`🧠 Brain/Memory.md`) — if strategic decisions, new context, or project status changes surfaced
- **To-Do.md** (`📥 Inbox/To-Do.md`) — if action items surfaced that are not already tracked
- **Project note** — if the meeting significantly changes project status

---

## Step 9 — Clean Up

After processing, delete downloaded artifact folders from the vault root using `find -delete` (run from the vault root — `rm -rf` is typically blocked in sandboxed environments):

```bash
find . -maxdepth 2 -name "transcript.txt" -path "*/artifact-*" -delete
find . -maxdepth 1 -type d -name "artifact-*" -delete
```

Only delete artifact folders created during this session. Do not delete unrelated files.

### If cleanup fails

Log the paths that couldn't be deleted and tell the user — don't leave orphan `artifact-*` folders silently cluttering the vault.

---

## Quality Rules

- Meeting notes in **English only**
- No em dashes (`—`) in file names
- Never start a file with a blank line after frontmatter
- Link to the Lark minutes URL in the `source` frontmatter field
- Interaction log entries: brief, one-line, link to the meeting note
- If a person appears in multiple meetings in the same session, batch their interaction log updates
- **Always wikilink attendees in the body** (`**Attendees:**` line) using short wikilinks (`[[Name]]`) whenever a profile exists
- **Always tag involved companies** in frontmatter (e.g. `tags: [meeting, kickoff, acme, beta-corp]`) and link them in `## Related` (e.g. `[[Acme]]`, `[[Beta Corp]]`)

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Created a new `👤 People/` profile because one didn't exist | Never create — flag to user for approval |
| First keyword match → wrong project folder | Apply tie-break rules: most-specific wins, else ask |
| Wrote note in transcript's original language (e.g. Indonesian, Mandarin) | Always translate to English |
| Created note from empty/failed fetch | Stop on fetch failure, report to user, do not fabricate |
| Used calendar attendees even though the meeting wasn't on the calendar | Fall back to transcript speakers, flag `attendees_source: transcript` |
| Left `artifact-*` folders after a failed run | Always run Step 9 even on partial failure, log any leftovers |
| Triggered on a `/docs/` or `/base/` URL | Check the URL path segment — only `/minutes/<token>` belongs to this skill |
| Exact-match `Glob` missed a profile (e.g. spacing variants) | Use the Step 7 fuzzy lookup chain: exact → first-name + alias → spacing-tolerant → alias grep — before declaring "no profile" |
| Wrote meeting note with plain-text attendees only | Resolve all profiles in Step 7 *before* Step 6, then wikilink in the body's `**Attendees:**` line |
| Filed under a project folder but didn't tag/link the involved companies | Add company slugs to `tags`; add `[[CompanyName]]` to `Related` |
| Company wikilink resolves to an empty page | Run the `resolve_company` bash snippet from Step 6 — never eyeball. The flat-vs-folder layouts and empty-stub shadows are real failure modes |
| Linked a company that turned out to be a folder with no overview file | Resolution snippet returns `FOLDER_ONLY:` — ask user how to handle, don't silently link to a non-existent overview |
