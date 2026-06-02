---
type: idea
date: 2026-06-02
description: How to set up Obsidian Git plugin on mobile for 15-minute auto pull/push sync, mirroring the desktop setup.
tags: [idea, obsidian, git, mobile, sync, automation]
status: seed
source:
project:
---
# Idea - Obsidian Git Mobile Sync

## The Idea
> Replicate the 15-minute auto pull/push Obsidian Git setup from desktop onto mobile, so the vault stays in sync across devices without manual intervention.

## Setup Steps

### 1. Install the Plugin
- Obsidian → Settings → Community Plugins → Browse → search **Obsidian Git** → Install & Enable

### 2. Authentication (HTTPS + PAT)
SSH is not supported on mobile — use HTTPS with a GitHub Personal Access Token:
- GitHub → Settings → Developer Settings → Personal Access Tokens → Generate new token (classic)
- Scope needed: `repo`
- In Obsidian Git settings: set **Username** and **Password/Token** fields

### 3. Configure Auto-Sync
- **Auto pull interval**: `15` minutes
- **Auto push interval**: `15` minutes
- Enable **Pull on startup** — syncs immediately when app opens

### 4. Commit Message (Optional)
- Default format: `vault sync 2026-06-02` (use Obsidian Git's date variable) — makes mobile commits easy to identify in git log

## Key Difference vs Desktop

| | Desktop | Mobile |
|---|---|---|
| Background sync | Yes | No — app must be open |
| SSH keys | Supported | Not supported |
| Auth method | SSH or HTTPS | HTTPS + PAT only |

The 15-minute timer only runs while Obsidian is actively open on mobile. **Pull on startup** compensates for gaps when the app was closed.

## Why It Matters
- Keeps vault in sync across laptop and phone without manual git commands
- Reduces risk of conflicts from editing on multiple devices
- Pairs well with the [[🧠 Brain/Memory]] update workflow — changes made on mobile surface on desktop within 15 minutes

## Connection
- [[🧠 Brain/Memory]] — session context and active vault tooling
- [[📥 Inbox/To-Do]] — action item: complete mobile auth setup

## Next Steps
- [ ] Generate GitHub PAT with `repo` scope
- [ ] Enter credentials in Obsidian Git plugin settings on mobile
- [ ] Set auto pull/push intervals to 15 minutes
- [ ] Test: edit a note on mobile, confirm it appears on desktop within 15 min
