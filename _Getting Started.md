# Welcome to Your Second Brain

You're in. This vault is **pre-configured** — Claudian (in-vault AI), Periodic Notes, Obsidian Terminal, slash commands, and folder structure are all already wired. You just need a couple minutes of personalization pass and you're running.

> [!tip] How this vault works
> **Don't fill files in by hand. Talk to Claudian — Claudian writes the files.**
>
> The folder structure and templates are a guide to *what's worth telling Claudian about*. When you see an empty folder (like `💼 Company/`) or a Brain file (like `🧠 Brain/User.md`), that's a prompt to have a conversation. Claudian populates the vault from your context.

> **Already past this?** Skip to **[Daily workflow](#daily-workflow)** at the bottom.

---

## First-run vault setup

Four steps, in order. Steps 1–3 take ~30 seconds each. Step 4 is the big one — about 10–15 minutes to seed your vault with personal context. Total: ~15 minutes.

### 1. Restart Obsidian

Quit Obsidian fully (`Cmd+Q`) and reopen. This forces a clean plugin scan — without the restart, the bundled plugins (Claudian, Periodic Notes, Obsidian Terminal) may show as enabled but not actually run.

### 2. Confirm Claudian is signed in

The Claudian panel is already open on the right. If you're signed in to Claude Code, Claudian uses the same session — you should already be authenticated.

If the panel prompts you to sign in: click sign-in and use your **Claude subscription** (Pro, Max, or Team plan). No API key needed.

### 3. Run a health check

In Claudian, type:

> run /setup

`/setup` does four things:

- **Installs required Claude Code plugins** — automatically installs three plugins if they're not already on your machine (see below)
- **Verifies** plugin configs, folders, slash commands, and required files
- **Reports** anything missing with the exact command/action to fix it
- **Enables in-Obsidian editing** — creates `🧠 Brain/Commands/` and `🧠 Brain/Skills/` so you can browse and edit slash commands and skills directly inside Obsidian's file tree

**Plugins `/setup` installs automatically:**

| Plugin                   | What it does                                                                                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Superpowers**          | The engine behind every slash command in this vault — `/gm`, `/gn`, `/eod`, `/dump`, `/weekly-review`, and more. Without it, none of the daily workflow commands work.                        |
| **claude-md-management** | Keeps your `CLAUDE.md` up to date as you set new rules and preferences. When you tell Claudian "always do X", this makes sure it sticks across sessions.                                      |
| **context7**             | Pulls live documentation for any library or framework mid-conversation. Useful when you're asking Claudian about code or tools — it fetches current docs instead of relying on training data. |

**Bundled Obsidian plugins (pre-installed):**

| Plugin | What it does |
|---|---|
| **Claudian** | Embeds Claude Code in Obsidian — the chat panel on the right. |
| **BRAT** | Auto-updates Claudian whenever a new version ships. No manual downloads. |
| **Terminal** | Shell access inside Obsidian (`Cmd+P` → "Terminal: Open Terminal"). Run Claude Code and Lark CLI without leaving the app. |

If everything's healthy, you'll see a list of ✅ checks and a "Vault healthy. You're good to go" line.

### 4. Tell Claudian who you are

This is the step that makes the vault feel *yours* on day one instead of empty for a month. We combine **two sources**: your existing AI's memory of you (subjective context — "what you've told ChatGPT about your life") and your real Lark activity (objective signal — "what's actually happening day-to-day"). Claudian uses both to populate five layers of your vault, in this order:

1. **About you** → `🧠 Brain/User.md` + `CLAUDE.md`
2. **North Star** → `🧠 Brain/North Star.md` (goals, focus, anti-goals)
3. **Company entities** → `💼 Company/<Entity>.md` (entities you have an ongoing relationship with)
4. **People** → `👤 People/<Name>.md` (your personal CRM)
5. **Active projects** → `🚀 Projects/<Project>.md` (work threads you're running now)

Each sub-step from 4b onward follows the same loop: **paste a prompt to your AI chat → edit the response → hand it to Claudian → Claudian writes your file AND cross-checks with Lark → confirm or amend the suggestions Claudian surfaces**. ~15–20 minutes total.

The Lark cross-check is the quality gate. Heuristics narrow candidates; you confirm what's a real project / real person / real entity / real focus area. Without that gate, false positives end up in your vault forever.

> ✏️ **Edit each AI response before pasting it to Claudian.** AI outputs often contain placeholders like `[fill in: name]` or `[Former role]` for things it doesn't know. Replace placeholders with actual info, delete sections that don't apply, add anything important the AI missed. Cleaner input = cleaner vault. (Any text editor works — even the AI chat itself, just edit before copying.)

> 💡 **You don't need to know `lark-cli` commands.** Claudian auto-routes to the right Lark skill — `lark-contact`, `lark-vc`, `lark-doc`, `lark-wiki`, `lark-im`, `lark-calendar` — based on what the Claudian prompt asks for. If a skill is missing, Claudian will surface the exact install command (see `_Pre-Install Setup.md`).

#### 4a. About you

**Paste to your AI chat:**

```
I'm setting up an Obsidian "second brain" vault that uses AI to help me
organize my notes, journals, meetings, and projects. I need a personal
context briefing I can paste into the vault so the AI assistant there
understands who I am from day one.

Based on everything you know about me from our past conversations, write
a structured profile in plain Markdown covering:

- Identity: full name, role, company, location, languages I use
- Work context: what I do day-to-day, businesses or projects I'm involved
  in, key responsibilities
- Key people: people I work with closely — manager, teammates, collaborators,
  partners, co-founders, etc. (names + how we work together)
- Communication preferences: how I like AI to talk to me (concise vs
  verbose, what to challenge, what to skip)
- Working principles: values, frameworks, approaches I follow
- Output preferences: formatting style I like for notes, code, summaries

Don't make things up. If you're not sure about something, leave a
placeholder like `[fill in: ...]` so I can edit it later. Output as
plain Markdown.
```

> [!example] Paste to Claudian
> Here's my personal context. Use it to fill in `🧠 Brain/User.md` and the "About the Owner" section at the top of `CLAUDE.md`.
>
> [paste the edited response]

#### 4b. North Star (goals, focus, anti-goals)

**Paste to your AI chat:**

```
Based on what you know about me, write out my current North Star — the
direction I'm pointed at. Cover:

- 1–3 year goals: what I'm trying to build or become
- Current focus areas: the 2–3 things getting most of my attention right now
- Anti-goals: things I'm explicitly NOT pursuing right now, even if they
  look attractive — to protect focus
- Recent shifts: anything in the goals or focus that's changed lately

Be honest about what you actually know vs what you're inferring. If
anything's unclear, leave a `[fill in: ...]` placeholder.

Output as Markdown with clear section headers.
```

> [!example] Paste to Claudian
> Here's my North Star draft. Use it to fill in `🧠 Brain/North Star.md`.
>
> [paste the edited response]
>
> Then cross-reference with Lark:
>
> - Use the `lark-doc` skill: scan my docs from the last 30 days, especially strategic ones (planning, OKR, vision, roadmap). Identify recurring themes I'm actively engaging with.
> - Use the `lark-im` skill: scan my recent messages for strategic keywords I bring up frequently.
>
> Surface a structured summary in this format:
>
> - **Wrote** — summary of what you put in `North Star.md` from my paste
> - **Add candidates (strong signal)** — themes appearing across multiple recent docs/messages, likely real focus areas
> - **Add candidates (weak signal)** — themes mentioned occasionally, uncertain
> - **Possibly stale** — focus areas in my paste with zero recent Lark signal
>
> Wait for my confirmation before adding any amendments.

#### 4c. Company entities

**Paste to your AI chat:**

```
Based on what you know about me, list the companies / entities I have an
ongoing relationship with — companies I work at, partner with, own, sit on
the board of, or advise. For each one:

- Name
- My position at this entity (e.g. my title — employee/manager/partner/
  founder/advisor, plus team or division if relevant)
- 1–2 sentence overview of what the entity does
- What I'm currently focused on at this entity, if you know

Output as a Markdown list, one section per entity. Skip ones I'm only
loosely affiliated with — focus on entities where I have real ongoing
involvement.
```

> [!example] Paste to Claudian
> Here are my work entities. For each one, create a note in `💼 Company/` named after the entity (e.g. `💼 Company/Antikode.md`) using `🧩 Templates/Company Overview Template.md`.
>
> [paste the edited response]
>
> Then cross-reference with Lark:
>
> - Use the `lark-im` skill: list active group chats whose name matches an entity I listed. Note message frequency.
> - Use the `lark-doc` and `lark-wiki` skills: find recent docs / wiki pages tagged or about each entity. List the most relevant URLs as references on each entity note.
> - For Lark groups or shared spaces I'm in but didn't list as an entity: surface as add candidates if the group has 5+ members and recent activity.
>
> Surface a structured summary:
>
> - **Wrote** — entities created from my paste
> - **Add candidates (strong signal)** — entities suggested by Lark with multiple supporting signals (active group + recent docs)
> - **Add candidates (weak signal)** — uncertain entities (one signal only)
> - **Possibly stale** — entities in my paste with no Lark signal at all
>
> Wait for my confirmation before adding new entities or marking anything stale.

#### 4d. People (your personal CRM)

**Paste to your AI chat:**

```
Based on what you know about me from our past conversations, list the most
important people in my professional and personal life. For each person, write
a short Markdown profile with:

- Name
- Relationship to me (manager, teammate, collaborator, partner, client,
  co-founder, friend, family, etc.)
- Their role / what they do
- How we work together OR how I know them
- Any context that would help an AI assistant understand our relationship
  (length of relationship, frequency of contact, decision-making weight, etc.)

Output as a Markdown list, one section per person. Limit to the top 10–20
most relevant people — don't include everyone you've ever mentioned.
```

> [!example] Paste to Claudian
> Here are the most important people in my life. Create one note per person in `👤 People/` using the structure from `🧩 Templates/Person Template.md`. Use each person's full name as the filename.
>
> [paste the edited response]
>
> Then cross-reference with Lark:
>
> - Use the `lark-contact` skill: look up Lark identity (email, role, department) for everyone in my paste. Add to their profiles.
> - Use the `lark-im` skill: list people I've messaged most frequently in the last 90 days.
> - Use the `lark-vc` skill: list people I've met with most frequently (recurring meetings, recent calls).
> - Cross-reference: people frequently in chat or meetings but NOT in my paste = add candidates. Roles or companies in my paste contradicted by current Lark data = potentially stale.
>
> Surface a structured summary:
>
> - **Wrote** — people from my paste
> - **Add candidates (strong signal)** — people I interact with weekly+ but didn't list
> - **Add candidates (weak signal)** — people with occasional interaction (monthly-ish)
> - **Possibly stale** — people in my paste with no recent Lark interaction or contradicted role/company info
>
> Wait for my confirmation before adding new profiles or amending stale info.

#### 4e. Active projects

**Paste to your AI chat:**

```
Based on what you know about me, list my currently active work projects,
business initiatives, and major personal projects. For each one:

- Name (short, scannable)
- Type (internal company project, client work, personal, side project, etc.)
- Status (active, paused, just-launched, winding-down)
- 1–3 sentence description of what it is and why it matters to me
- Current focus or open questions, if you know them

Output as a Markdown list, one section per project. Skip anything finished
or that I've clearly moved on from.
```

> [!example] Paste to Claudian
> Here are my active projects. For each one, create a folder + project note in `🚀 Projects/` following `🧩 Templates/Project Template.md`. Use the project name for the folder.
>
> [paste the edited response]
>
> Then cross-reference with Lark:
>
> - Use the `lark-im` skill: list group chats with messages in the last 30 days, 3–15 members, and names suggesting projects (client name, product name, codewords like "pitch" / "campaign" / "build" / "revamp"). External members = strong project signal.
> - Use the `lark-calendar` skill: list recurring meetings (weekly+) from the last 30 days. Cross-ref with the group chats.
> - Use the `lark-wiki` and `lark-doc` skills: for each project in my paste, search for related planning, briefs, or status docs. Add the most relevant URLs as references on the project note.
> - For projects in my paste with zero Lark signal (no chat, no recurring meeting, no recent docs) → flag as possibly stale.
>
> Surface a structured summary:
>
> - **Wrote** — projects created from my paste
> - **Add candidates (strong signal)** — groups/meetings matching multiple project heuristics (recent activity + external members + project-like name + recurring meeting)
> - **Add candidates (weak signal)** — ambiguous groups or meetings (one signal only)
> - **Possibly stale** — projects in my paste with no Lark signal
>
> Wait for my confirmation before creating new projects or marking anything stale.

#### Keep going

> 💬 **Don't stop here.** You don't have to do all the sub-steps in one sitting, and you don't have to use these exact prompts. **Just keep talking to Claudian.** Some examples of what to feed it over time:
>
> - **Daily moments** — a colleague joined your team, a project hit a milestone, you made a strategic decision, a book worth remembering. Tell Claudian; it writes the right note in the right place.
> - **Refresh yourself** — when your role evolves, your working style shifts, or you discover a new principle worth tracking, say *"update my `User.md`, I've changed X"* and Claudian rewrites it. Same for `North Star.md` when your focus shifts.
> - **Digest external sources** — drop a PDF, website URL, annual report, article, or competitor brief into Claudian. It summarizes and updates the right entity (`👤 People/`, `💼 Company/`, `🚀 Projects/`). Especially useful for company research and long docs you'd otherwise skip.
> - **Periodic refresh** — every few months, ask Claudian to re-run the Lark cross-check on People / Projects / Company / North Star. Real-world signal (meetings, docs, contacts) evolves; the vault should track it.
>
> The vault gets smarter the more you feed it.

---

## Daily workflow

Four slash commands carry 90% of the value. Three of them form a loop that repeats every day — one for mornings, two for evenings. The fourth is for ad-hoc capture throughout the day.

---

### `/gm` — Good morning briefing

**When:** First thing in the morning, before your first meeting.

**What it does:** Pulls three sources of context together and gives you a single, scannable briefing to start the day:

1. **Today's Lark calendar** — every event, who organized it, and a flag on anything that needs prep (a pitch, a client meeting, a key decision)
2. **Open tasks** — Lark tasks due today or overdue, plus the 🔴 This Week section of your To-Do
3. **Active project context** — the 3–5 most important threads from Memory.md: what's moving, what's blocked, what needs a call

The output synthesizes all three into a **Top 3 for today** (the highest-leverage things to do) and a **Flags** section (anything urgent or at risk of slipping).

**Why it matters:** Without this, you start the day reactive — answering whatever hits you first. `/gm` gives you a 60-second orientation so you enter the day with intent.

---

### `/eod` — End of day gathering

**When:** End of day, before running `/gn`. Think of it as the interview before the write-up.

**What it does:** Surfaces everything that happened today that isn't already in the vault — through three passes:

1. **Calendar cross-reference** — pulls today's Lark calendar and compares against what's already captured in the vault. Shows you a clear split: captured vs. needs context.
2. **Meeting interview** — for each uncaptured meeting, asks you a few questions *one meeting at a time*: who was there, what got decided, any action items. If a meeting was recorded on Lark, you can share the minutes URL and it processes the transcript automatically.
3. **Lark chat scan** — scans the last 24h of Lark messages across your active projects. Finds relevant chats two ways: by matching project names from the vault against Lark groups, and by finding chats where *you personally sent messages today*. No manual labeling needed. Surfaces only what matters: decisions, action items, @mentions, client signals.

After gathering, it prompts you to run `/gn`.

**Why it matters:** Memory is lossy. By end of day, you've forgotten 30–40% of what actually happened. `/eod` acts as a structured retrieval — the calendar scaffold means you don't have to remember what to remember. The Lark chat scan catches decisions that were made informally over chat and never made it into a meeting.

> **Tip:** You don't have to answer every question in detail. Even one-sentence answers give the vault meaningful signal. The point is to capture, not to journal beautifully.

---

### `/gn` — Good night execution

**When:** After `/eod` (or directly, if you skipped the interview).

**What it does:** Takes everything discussed in the current session and writes it to the vault in one pass:

1. **Today's journal** — creates or fills in `📓 Journals/YYYY/MM MMM/YYYY-MM-DD • Day.md`. Populates Check-in, Notes, Highlights, Challenges, Lessons Learned, and Reflection from the session context. You never write these sections manually — it infers them.
2. **Meeting notes** — creates a meeting note for any uncaptured meeting, filed in the right project folder (or `🤝 Meetings/` as a fallback).
3. **Cascading updates** — ripples through all related files: People interaction logs, Project status, To-Do (completed items off, new items on), Memory.md strategic context.
4. **Brain updates** — logs decisions to `Decisions.md`, patterns to `Patterns.md`, mistakes to `Gotchas.md`.

**Why it matters:** One input (your `/eod` conversation) ripples through the entire vault. Without this, your vault goes stale — you have orphaned meetings, outdated project statuses, people profiles that never compound. `/gn` is what makes the second brain actually feel alive.

> **The two-step evening flow:** `/eod` (gather) → `/gn` (write). You can skip `/eod` and go straight to `/gn` if you've been talking to Claudian throughout the day and everything is already in context.

---

### `/dump` — Quick capture

**When:** Anytime during the day — a burst of thoughts, a voice note, meeting notes you want captured before you forget.

**What it does:** Takes raw, unstructured input and routes it to the right place in the vault:

| What you give it | Where it goes |
|---|---|
| A reflection or day recap | `📓 Journals/` |
| Meeting notes from memory | `🚀 Projects/<Project>/Meetings/` |
| A new idea | `💡 Ideas/` |
| Tasks or action items | `📥 Inbox/To-Do.md` |
| Info about a person | `👤 People/` |
| Project status update | `🚀 Projects/` |
| Something you learned | `📚 Learnings/` |

It parses the input, determines the type (or splits mixed input into multiple files), applies the right frontmatter and format, and runs cascading updates on related files.

**`/dump` vs. normal chat:** Normal chat is conversational and selective — Claudian captures things as they naturally come up. `/dump` is deliberate batch mode — you're about to share a lot and want all of it structured and saved. Use `/dump` when you have a "brain dump" ready to go.

---

### `/setup` — Health check and recovery

**When:** On first run, or any time something feels broken.

Verifies plugin configs, folders, slash commands, and required files. Reports anything missing with the exact action to fix it. Run this if slash commands stop showing up, the daily journal is blank, or something in the vault feels off.

---

### The daily rhythm

```
Morning                    Day                    Evening
  │                         │                        │
  ▼                         ▼                        ▼
/gm                      /dump                    /eod
(orient)             (capture as needed)         (gather)
                                                    │
                                                    ▼
                                                  /gn
                                                (write)
```

Most days: `/gm` in the morning → `/eod` + `/gn` at the end. `/dump` whenever something happens during the day that you want captured immediately rather than at end-of-day.

---

## Two ways to talk to Claude

- **Claudian (chat panel inside Obsidian)** — best for: summarizing the note you have open, drafting, reflecting, connecting ideas across the vault. Reads your current note + vault context.
- **Claude Code (terminal)** — best for: running Lark CLI commands (calendar, tasks, docs, messages), running slash commands like `/gn`, automating workflows. You can run it inside the **bundled Obsidian Terminal** (`Cmd+P` → "Terminal: Open Terminal") so you never have to leave the app, or in any external terminal.

Both share the same vault context. Use whichever is closer to what you're doing right now.

---

## Example prompts to try

### In Claudian
- *"Summarize the note I have open into 3 bullets and an action list"*
- *"What action items are in my To-Do?"*
- *"Help me fill in today's journal"*
- *"What themes keep coming up across my journals this week?"*
- *"Draft a project brief from my notes in `💡 Ideas/`"*

### In Claude Code
- *"What's on my calendar today?"*
- *"Find the leave policy doc on Lark"*
- *"Create a task: Review onboarding checklist, due Friday"*
- *"Search my Lark messages for 'quarterly review'"*
- *"Pull yesterday's meeting transcript and write a summary"*

### Combining both
- *Prep* — Check tomorrow's calendar in Claude Code, then in Claudian draft talking points from past meeting notes
- *Capture* — Take quick meeting notes in Obsidian, ask Claudian to extract action items, then in Claude Code create Lark tasks from them
- *Review* — In Claude Code list this week's Lark meetings, then in Claudian reflect on patterns across your journals

---

## Tips

- **Speak, don't type.** Install [Wispr Flow](https://wisprflow.ai/r?NICK3397) — press a hotkey anywhere in Obsidian and just talk. Works in Indonesian and English. Speaking to Claudian is 3-4x faster than typing and feels less like "writing notes" and more like thinking out loud. This is especially valuable for `/dump` mid-day and `/gn` at night.
- **Daily journaling compounds.** Even 2 minutes a day. `/dump` during the day, `/gn` to close.
- **One note per person in `👤 People/`.** Update after every interaction. In 3 months you have a compounding CRM.
- **Don't organize perfectly.** Capture first, organize later. Claude can find anything.
- **Notes without links are bugs.** Every new note should link to at least one other.
- **Lark Docs sync** — if you push a vault note to Lark, add the resulting Lark URL to the note's frontmatter as `source:`. Two-way reference.

---

## Troubleshooting

### Claudian / Obsidian

| Problem | Fix |
|---|---|
| Claudian icon not in sidebar | Settings → Community plugins → enable Claudian. Restricted mode must be off. |
| Claudian not responding | Sign in to your Claude subscription in Claudian settings (no API key — use the subscription login) |
| Daily journal opens blank | Run `/setup` in Claudian — the template path is likely broken |
| Slash commands missing in Claude Code | Run `/setup` — verifies that `.claude/commands/` has all expected files |
| Periodic Notes plugin not loading | Settings → Community plugins → enable Periodic Notes |
| Claudian says "command not found" for `claude` / `lark-cli` / `node` | Use the bundled **Obsidian Terminal** instead (`Cmd+P` → "Terminal: Open Terminal"). It has full shell access. (This is a macOS quirk — GUI apps don't see Homebrew / nvm / asdf paths the way your terminal does. Terminal works because it spawns a real shell.) |

### Lark CLI (only if you set it up)

| Problem | Fix |
|---|---|
| "not logged in" | `lark-cli auth login --recommend` |
| "permission denied" / `99991679` | Ping whoever set up the shared Lark app — a scope needs to be added in the Lark Developer Console |
| "token expired" | `lark-cli auth login --recommend` again |
| Lark skills missing in Claude Code | Re-run `npx skills add larksuite/cli -y -g`. Still missing → ping whoever shared this template with you |
| `lark-cli` command not found | Re-run the install steps from `_Pre-Install Setup.md` |

---

## Quick reference (for the curious)

You don't need to memorize these — Claude figures them out for you. But if you want to try the Lark CLI directly:

```bash
lark-cli calendar +agenda                   # Today's schedule
lark-cli task +get-my-tasks                 # My open tasks
lark-cli docs +search --query "..."         # Search Lark docs / wiki
lark-cli contact +search-user --query "..." # Find a colleague
lark-cli profile list                       # Check active profile
```

Full command reference: https://github.com/larksuite/cli

---

> Questions? Ping whoever shared this template with you on Lark.

> 🗑️ *This is your onboarding guide — feel free to delete this file once you've gone through setup and feel at home with the daily flow. The vault works fine without it.*
