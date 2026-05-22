# CLAUDE.md

This file provides guidance to Claude (claude.ai/code) when working in this vault.

## About the Owner

**Rayva Andira** — Automation Engineer (Lark Workspace) / Data Engineer at ALVA, Jakarta.

**Communication style:** Prefers concise, actionable output with code examples and structured summaries.

**Current focus:** Building internal systems for ALVA (payment requests, invoicing, automation).

Full profile: [[🧠 Brain/User.md]]

---

## What This Is

Personal second brain in Obsidian — work + personal, notes + projects + journals + people.

---

## Vault Structure

```
vault/
├── CLAUDE.md            ← you are here
├── 🧠 Brain/            ← durable knowledge & goals
│   ├── User.md          ← owner profile
│   ├── Memory.md        ← session log + active context (update each session)
│   ├── North Star.md    ← goals, focus, anti-goals
│   ├── Decisions.md     ← decision log with links to records
│   ├── Patterns.md      ← recurring conventions & lessons
│   └── Gotchas.md       ← known pitfalls to avoid
├── 💼 Company/          ← entities you have an ongoing relationship with (own/work at/partner with)
├── 📥 Inbox/            ← quick capture, TODO.md
├── 📓 Journals/         ← daily journals (YYYY/MM MMM/YYYY-MM-DD • ddd.md)
├── 💡 Ideas/            ← idea seeds
├── 🚀 Projects/         ← active projects
├── 📚 Learnings/        ← structured course notes (Domestika, Coursera, etc.)
├── 🤝 Meetings/         ← meeting notes
├── 👤 People/           ← personal CRM (private — see People conventions below)
├── 🧩 Templates/        ← Obsidian templates (do not add notes here)
└── 📎 Attachments/      ← images, files
```

### Templates Available
- `Daily Journal` — 📓 Journals/
- `Meeting Note` — 🤝 Meetings/
- `Idea` — 💡 Ideas/
- `Project` — 🚀 Projects/
- `Person` — 👤 People/
- `Learning Note` — 📚 Learnings/
- `Company Overview` — 💼 Company/[Entity].md

---

## Vault Map

All slash commands read paths from here at runtime. Do not hardcode paths in commands — always resolve from this map.

```yaml
brain: "🧠 Brain"
journals: "📓 Journals"
journals_format: "YYYY/MM MMM/YYYY-MM-DD • ddd"
journals_template: "🧩 Templates/Daily Journal Template"
people: "👤 People"
projects: "🚀 Projects"
meetings_orphan: "🤝 Meetings"
inbox: "📥 Inbox"
todo: "📥 Inbox/To-Do.md"
templates: "🧩 Templates"
company: "💼 Company"
ideas: "💡 Ideas"
learnings: "📚 Learnings"
```

---

## Language

**Default: notes are written in English.** Override per-user preference (set in `🧠 Brain/User.md`) — if the user prefers another language, write notes in that language. Conversation replies in chat always match whatever language the user uses.

---

## Formatting Rules

- **No em dashes (`—`) in file names, folder names, or headings.** Use a hyphen or space instead. (Em dashes can break sync, search, and link resolution.)
- **Never start a file with an empty line.** Content must begin immediately after the closing `---` of the frontmatter — no blank line in between
- **Folder names use title case.** e.g. `Cards`, `Mockups`, `Resources` — not `cards`, `mockups`, `resources`
- **Lark Docs sync:** When pushing a vault note to Lark Docs, add the resulting Lark doc URL as a `source` field in the vault file's frontmatter. This keeps a two-way reference between vault and Lark.

---

## Conventions

### Frontmatter
All notes require at minimum:

| Field | Required | Description |
|-------|----------|-------------|
| `type` | All | journal, meeting, idea, project, person, decision, note |
| `date` | All | YYYY-MM-DD |
| `tags` | All | Array of tags |
| `description` | All except journals | ~150 chars, what this note is about |
| `status` | For projects, decisions | active, completed, archived, proposed, accepted, deprecated |
| `project` | When relevant | Links note to a project |
| `people` | For meetings | Array of wikilinks to 👤 People/ |

### Wikilinks & Graph
- Use **short wikilinks** (filename only, no path): `[[My Note]]` not `[[🚀 Projects/My Note]]`
- Obsidian resolves by filename across the vault — short links survive file moves
- **Notes without links are bugs** — every note must link to at least one other note

### File Naming
- Journals: `📓 Journals/YYYY/MM MMM/YYYY-MM-DD • ddd.md` (e.g. `📓 Journals/2026/04 Apr/2026-04-06 • Mon.md`)
- People: `[Full Name].md` (e.g. `Jane Smith.md`)
- Meetings: `YYYY-MM-DD <Title>.md` (e.g. `2026-05-04 Kickoff.md`) — date first, no em dash

### People System (Personal CRM)
- One file per person in `👤 People/` — named by their full name
- Structure: Identity → Context → Interaction Log → Key Insights → Active Items
- **Rule:** When any note mentions a person who has a `👤 People/` file → link to their profile AND add a row to their Interaction Log
- Meeting notes include a `people:` frontmatter field linking to person notes
- Over time, person notes compound into a full relationship profile
- **Optional subfolders by relationship type or company** as the folder grows: `👤 People/Antikode/`, `👤 People/Partners/`, `👤 People/Clients/`, `👤 People/Family/`, etc. Start flat — only subfolder when you have 10+ people in a category.

**Privacy:** This folder is your **private personal CRM** — not for team sharing. Treat it like a private notebook. For team-wide people data (org charts, employee directories, contact lists), use a shared system like a Lark Base or HRIS, not this folder.

### Company Folder (`💼 Company/`)
The `💼 Company/` folder holds notes about entities you have an ongoing relationship with — companies you work at, partner with, own, sit on the board of, or advise.

**The pattern:** one note per entity, named after the entity (e.g. `Antikode.md`). Use the **Company Overview** template. If an entity accumulates multiple notes (financials, strategy, contracts), promote it to its own subfolder when that happens.

**Hard rules:**
- Never put individual people files in the Company folder. Profiles live exclusively in `👤 People/`.
- Financial positions (loans, investments, deals) belong in your finance tracking system, not in `💼 Company/`. Test: *"Is this a legal entity I have a recurring relationship with?"* → Company. *"Is this a financial position?"* → not here.

### 🧠 Brain/ — Durable Knowledge
The `🧠 Brain/` folder holds long-lived context that persists across sessions:
- **North Star.md** — current goals, focus areas, anti-goals, and shifts log
- **Decisions.md** — index of key decisions with links to decision record notes
- **Patterns.md** — recurring conventions, things that work well
- **Gotchas.md** — known pitfalls, mistakes to avoid repeating

### 📥 Inbox/To-Do.md — Centralized Tasks
All action items from meetings, daily notes, and conversations get consolidated into `📥 Inbox/To-Do.md`. Organized by urgency (This Week / This Month / Personal / Pending). Update as items surface or complete.

---

## Daily Journal Workflow

Journals live in `📓 Journals/YYYY/MM MMM/YYYY-MM-DD • ddd.md` (e.g. `📓 Journals/2026/04 Apr/2026-04-06 • Mon.md`).

Hybrid format (uses Daily Journal Template):
- **Check-in** — Energy / Focus / Grateful for
- **📝 Notes** — detailed daily context: meetings, decisions, ideas, things learned. Tagged with relevant hashtags
- **Highlights** — what went well
- **Challenges** — blockers or difficulties
- **Lessons Learned** — takeaways worth remembering
- **Reflection** — What went well / What could improve / Tomorrow's priority

Claude extracts intent from free-form input and categorizes into the right sections automatically. The owner never needs to manually label which section something belongs to — Claude figures it out from context.

End-of-day flow: run `/eod` first to gather context from the calendar, meetings, and Lark chats, then `/gn` to lock everything into the vault.

---

## Technical Work Separation

**Technical project work (coding, debugging, API integration, pipeline building) happens in dedicated dev environments (e.g. Antigravity, VS Code), not in this vault.**

Daily journal entries should capture **outcomes and decisions**, not implementation details:
- ✅ "Shipped the new WFO logic — red or green only, no yellow tier. Team leads find it clearer."
- ✅ "Decided to defer leave deduction — source data is unreliable, patching on top creates worse bugs."
- ✗ "Fixed `build_note()` to recompute `card_state` internally using actual metric values"
- ✗ "RLS was enabled by default — `ALTER TABLE ... DISABLE ROW LEVEL SECURITY`"

**Rule of thumb:** If it reads like a commit log or debug session, it belongs in the dev environment. If it reads like something you'd tell a trusted colleague over coffee, it belongs in the journal.

**After a dev session**, write a 3-5 line summary in the daily note:
- What was built / shipped
- Any decisions made and why
- Blockers or next steps
- Lessons learned (strategic, not code-level)

Technical learnings (API gotchas, platform quirks, architecture patterns) belong in the project's own docs or the dev environment's CLAUDE.md — not in daily journals.

---

## Structured Course Notes

When the owner shares a **structured course** (Domestika, Coursera, Codecademy, etc. — anything with distinct modules/sections):
1. Create a **Learning doc** in `📚 Learnings/` with format `Learning [Course Title] ([Instructor]).md`
2. Put the course URL in the doc's `source:` frontmatter field
3. Add a section per module — the owner adds notes as each module finishes

This applies to any course with multiple sections, not one-off videos.

---

## Project Organization

Project notes live in `🚀 Projects/`. Create a subfolder when a project has multiple files (briefs, mockups, agreements). Otherwise a single `Project - [name].md` file is fine.

---

## Meeting Notes

**Primary home: `🚀 Projects/<Project>/Meetings/`.** A meeting about Project X belongs in `🚀 Projects/Project X/Meetings/2026-05-04 Kickoff.md`. The project folder is the home; the `Meetings/` subfolder keeps meeting notes organized alongside other project artifacts (briefs, mockups, agreements, etc.).

**Fallback: `🤝 Meetings/`** — only for orphan meetings without a clear project home (ad-hoc 1:1s, cross-cutting discussions, exploratory conversations that haven't crystallized into a project yet).

**Why:** project context compounds when everything related to a project lives together. Scattering meetings across `🤝 Meetings/` breaks that and makes the project folder feel hollow. The `Meetings/` subfolder pattern keeps things tidy as a project grows.

The `lark-minutes-debrief` skill applies this rule automatically: it classifies the meeting into the right project, creates the `Meetings/` subfolder if needed, and only falls back to `🤝 Meetings/` when the meeting is truly orphan.

> **Hard rule:** Never place a meeting note directly in a project folder root. Always use the `Meetings/` subfolder. Run `mkdir -p` before writing the file — even if this is the project's first meeting. This applies to `/gn`, `/eod`, `/dump`, and `lark-minutes-debrief` equally.

---

## Auto-Update Rules

Three persistent files Claude must keep current:

- **CLAUDE.md** — vault rules, formatting, workflow instructions. Update when the owner sets a new rule or convention.
- **🧠 Brain/User.md** — identity, roles, key people, preferences, working style. Update when new personal context or preferences surface.
- **🧠 Brain/Memory.md** — running strategic context, active decisions, pending items. Update when:
  - A strategic decision is made (add to Decisions Log)
  - Active project context changes (update the relevant section)
  - A new pending item surfaces (add to Pending Items)
  - A pending item is resolved (remove or move to Decisions Log)

**When to update:** proactively, as new information surfaces during conversation. Don't wait to be asked. Keep entries concise. Most recent at top.

---

## Auto-Behaviors (skill triggers)

Skills live in `.claude/skills/`. Each one self-declares when to fire via its `description:` frontmatter ("Use when..."). When a user message matches a skill's trigger condition, **invoke that skill before doing anything else — even before asking clarifying questions.** The skill's own SKILL.md tells you what to do once invoked.

This is auto-discovery, not a hardcoded list. New skills added under `.claude/skills/` activate as soon as their folder is in place — no edits to this file required. Run `/setup` to see what's currently installed.

---

## Behavior Rules

- Always read a file before editing it
- Translate voice notes to English when journaling
- Keep notes concise and scannable — headers, bullets, checkboxes
- Use short wikilinks only
- Notes without links are bugs — every note links to at least one other
- Update `🧠 Brain/Memory.md` when asked or at end of significant sessions

### Cascading Updates (IMPORTANT)
When creating or editing any note, always check for related content that should also be updated:

1. **People**: Any person mentioned → update their `👤 People/` profile (Interaction Log + Active Items)
2. **Projects**: If a note relates to an active project → update the project note's status/log
3. **To-Do**: If a task is completed or new action items emerge → update `📥 Inbox/To-Do.md`
4. **🧠 Brain/Memory.md**: If project status or active context changes → update the relevant section
5. **Linked notes**: If a note references other notes via wikilinks → check if those notes need updating too
6. **🧠 Brain/**: If a decision is made → log in Decisions.md. If a pattern emerges → log in Patterns.md. If a mistake is made → log in Gotchas.md

> Rule of thumb: one input (journal, meeting, idea) should ripple through all related files — people, projects, todos, memory, brain. Don't leave related notes stale.

---

## Lark CLI

Always use profile **`org-lark-cli`** for all Lark operations — Sheets, Base, Docs, IM, Calendar, Wiki, etc. The App ID + Secret for this profile come from the distributor (see `_Pre-Install Setup.md`).

- Never switch to or create other `lark-cli` profiles without explicit approval from the owner
- Never remove this profile
- If a command fails with permission error `99991679`, the scope may need to be added in the Lark Developer Console for this app — surface this to the owner rather than silently switching profiles
- Quick check: `lark-cli profile list` should show `org-lark-cli` as active
