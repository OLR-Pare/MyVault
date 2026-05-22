---
type: protocol
date: 2026-05-17
description: Rules for handling skipped journal days in /gm and /gn. Detects gap between today and the last journal, then either prompts the user (2-3 day gap) or auto-stubs missed days (4+ days). Preserves the one-file-per-day timeline.
tags: [protocol, journals, gm, gn]
---
# Journal Gap Protocol

How [[gm]] and [[gn]] handle skipped days so the journal stays a clean one-file-per-day record. Related: [[Closed Loops]], [[North Star]].

## Detection

At the top of every `/gm` and `/gn` run, find the most recent journal file under `{journals}` (default: `📓 Journals/`):

```bash
LATEST=$(find "📓 Journals" -type f -name "*.md" 2>/dev/null \
  | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' \
  | sort -u | tail -1)
TODAY=$(date +%Y-%m-%d)
GAP_DAYS=$(( ( $(date -j -f "%Y-%m-%d" "$TODAY" +%s) - $(date -j -f "%Y-%m-%d" "$LATEST" +%s) ) / 86400 ))
```

`GAP_DAYS` = days between last journal and today. (Substitute the actual `{journals}` path from your Vault Map.)

## Decision table

| Gap | `/gm` behavior | `/gn` behavior |
|---|---|---|
| 0 | Already wrote today, append or refresh | Already exists, fill empty sections |
| 1 | Normal (yesterday was journaled, today is fresh) | Normal, write today's journal |
| 2-3 | **Ask the user**: "You missed [Mon, Tue]. Stub them as gap-marker files, or fold context into today?" | Same prompt. Default to **stub** if no answer. |
| 4+ | **Auto-stub** missed days (no interview), then proceed with today | **Auto-stub** missed days, then write full journal for today |

## Stub file format

For each gap day, create `{journals}/YYYY/MM MMM/YYYY-MM-DD • ddd.md`:

```markdown
---
date: YYYY-MM-DD
status: gap
type: journal
---
# YYYY-MM-DD • ddd

> Gap day, no journal written. Stub auto-created on YYYY-MM-DD by /gm or /gn.

## 📅 Calendar (retroactive)

[If a calendar source is available (e.g. `lark-cli calendar +agenda --date YYYY-MM-DD`), include the output. Otherwise: "Not pulled."]

## 📝 Notes

(none, gap day)
```

**Rules for stubs:**
- Always create the file even if calendar pull fails. An empty stub is better than a missing date.
- Never run the reflection interview on stub days.
- `status: gap` frontmatter lets Dataview queries exclude them from "consecutive day" streaks.
- If the user later wants to backfill a stub, they just edit the file. The protocol does not touch existing files with non-gap status.

## Cascading updates on gap days

- **Do not** scan chat or email retroactively for context. Too noisy, low signal-to-noise.
- **Do** preserve any calendar events as a record, useful for "what was I doing that week?" recall.
- **Do not** update `Memory.md` or People profiles retroactively from stub days. Those updates only flow from real journaled days.

## Why this design

- One file per day preserves search and date-based recall.
- Folding 3 missed days into "today's" note breaks the journal-as-timeline contract.
- Stubs are cheap (4 lines) but mark the date as "intentionally empty" instead of "lost".
- Gap markers plus the `status` field let future reviews (weekly, monthly) see streak breaks without manual tracking.

## /gn specific note

After auto-stubbing, run all normal cascades (People, To-Do, Memory, Brain) against **today's** context only, not retroactively.
