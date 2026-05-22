---
description: "Quick capture — route a brain dump, voice note, or raw input to the right vault location"
---

**Before starting:** Read `CLAUDE.md` → find `## Vault Map` → parse the YAML. Use those paths for every folder reference in the routing table below. If no Vault Map exists, use the default paths shown.

Quick capture and route. Use this when you have a batch of things to log — a voice memo, a stream of thoughts, meeting notes from memory, or anything you want classified and saved without going through the full `/eod` flow.

**When to use `/dump` vs. just chatting:**
- `/dump` = deliberate batch capture. You're about to share a lot and want all of it structured and saved.
- Normal chat = conversational, selective. I'll capture things as they come up naturally.

---

## What to do

Take the user's raw input (voice dump, quick thought, paste, or `$ARGUMENTS`) and:

### 1. Parse — identify what type of content this is

- Journal entry (personal reflection, day recap, mood/energy)
- Meeting notes (who, what decided, action items)
- Idea (new business, product, process improvement)
- Task / action item (something to do)
- Person info (new contact, update on someone)
- Project update (status change, decision, blocker)
- Learning (something understood or discovered)
- Mixed (multiple types in one dump — split and route each)

### 2. Route — save to the correct location

| Type | Location |
|------|----------|
| Journal content | `{journals}/YYYY/...` (default: `📓 Journals/YYYY/MM MMM/YYYY-MM-DD • ddd.md`) |
| Meeting notes | `{projects}/<path>/Meetings/` or `{meetings_orphan}/` (defaults: `🚀 Projects/`, `🤝 Meetings/`) |
| Idea | `{ideas}/<title>.md` (default: `💡 Ideas/`) |
| Task / action item | `{todo}` (default: `📥 Inbox/To-Do.md`) |
| Person info | `{people}/<company>/<name>.md` (default: `👤 People/`) |
| Project update | `{projects}/<path>/` relevant file (default: `🚀 Projects/`) |
| Learning | `{learnings}/` or relevant project doc (default: `📚 Learnings/`) |

### 3. Format — apply the right template and conventions

- Use appropriate frontmatter (type, date, tags)
- English only, regardless of input language
- Follow vault formatting rules (no em dashes in filenames, no leading blank lines after frontmatter)

### 4. Cascade — update related files

After saving, check and update:
- `{people}/` profiles (default: `👤 People/`) for anyone mentioned (Interaction Log)
- `{projects}/` notes (default: `🚀 Projects/`) for any project referenced
- `{todo}` (default: `📥 Inbox/To-Do.md`) for any action items surfaced
- `{brain}/Memory.md` (default: `🧠 Brain/Memory.md`) if project status or active context changes
- `{brain}/Decisions.md` (default: `🧠 Brain/Decisions.md`) if a decision was made

---

## Notes

- If the dump is large and mixed, split it — create multiple files rather than one messy note.
- If content is ambiguous, make a judgment call and note what you did. Don't ask questions unless something is truly unclear.
- Language rule: translate to English before writing to any vault file.
