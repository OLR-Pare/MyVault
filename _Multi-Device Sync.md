# Multi-Device Sync (Mobile ↔ Desktop)

Optional setup. **The vault works fine single-device — skip this entirely if you only use one device.**

Set this up if you want to write a journal on your phone in the morning and have it on your laptop by lunch. The `session-handoff` skill, `/gm` `/gn` `/eod` cascades, and the Reopen Safety Check (all documented in [[CLAUDE]]) become useful once sync is in place.

**The mechanism:** your vault becomes a **private GitHub repo**, Obsidian Git auto-pulls/pushes every few minutes, and Claude Code mobile/web clones the same repo per session.

**Time:** ~10 min one-time setup.

---

## ⚠️ Read this first — privacy of your accounts

This setup gives **any device logged into your Claude account** full read/write access to your vault. That includes journals, People profiles, financial notes, private decisions — anything in the vault.

**Same applies to your GitHub account**: the OAuth grant gives Claude Code mobile read/write to your private vault repo.

### When this matters

If you share either account with anyone — family member, colleague, teammate, or any other arrangement (whether it's a personal account passed around or a multi-seat plan) — everyone on that account can see your vault and write changes back via mobile.

### If your accounts are shared, you have three options

**1. Don't enable mobile sync.** The vault works fully single-device on your laptop. You lose mobile capture but keep privacy. Skip this whole doc.

**2. Use a separate personal Claude account for vault sync.** Sign up for Claude Pro on your own email and use that for mobile/web sessions against your vault. Your shared work account stays separate from your private vault. Same approach for GitHub if needed.

**3. Accept the tradeoff.** Only do this if your vault has no sensitive content — no personal journals, no private decisions, no financial notes, no private People profiles. Rare to actually meet this bar; most vaults accumulate sensitive content quickly.

### If you're the only person with access to both accounts

You're good, proceed. The rest of this doc assumes that's the case.

---

## Prerequisites — you'll need these before starting

- **A GitHub account.** Free. Sign up at https://github.com/signup if you don't have one (~2 min — pick a username, verify your email, done). You'll use this same account on desktop (for pushing your vault) and mobile (for Claude Code's GitHub OAuth in Step 6).
- **Homebrew on your Mac.** Needed in Step 2 to install the GitHub CLI. If you went through `PRE-INSTALL.md`, you may not have it yet — install from https://brew.sh/ (one paste-into-Terminal line). You'll know if it's installed by running `which brew` in Terminal — if it prints a path, you have it.
- **Your vault is already open in Obsidian** with `/setup` run successfully. If you haven't done that yet, finish `_Getting Started.md` first.

Once those are in place, work through the steps in order. Estimated time: ~10 min if you're already comfortable with Terminal, ~20 min if it's your first time.

---

## 1. Install the Obsidian Git plugin

Open Obsidian → **Settings → Community plugins**.

If it's your first time using community plugins, click **"Turn on community plugins"** (you'll see a one-time consent dialog from Obsidian).

Then:
1. Click **"Browse"**
2. Search for **"Obsidian Git"** (by Vinzent)
3. Click **Install**
4. Click **Enable**

Verify in the left sidebar: a **"Source Control"** view should now appear (looks like a branch icon).

> **Why this is a manual step, not bundled:** Obsidian's community plugin registry always serves the current version of Obsidian Git. Bundling it would freeze the version at template release date. Installing via the UI takes 30 seconds and ensures you get the latest version with auto-updates.

---

## 2. Authenticate GitHub

**Open Terminal** first (press `Cmd + Space` → type `terminal` → Enter). Then paste these one at a time:

```bash
brew install gh        # only if you don't have it yet. If Homebrew isn't installed, get it from https://brew.sh/ first
gh auth login          # opens a browser, takes ~30 sec
```

When `gh auth login` asks what to authenticate with, just hit Enter through the prompts (the defaults are correct for our use). The last step opens your browser to confirm — click Authorize, return to Terminal, done.

---

## 3. Create a private GitHub repo

Go to https://github.com/new and fill in:
- **Repository name:** use the **same name as your vault folder** (e.g. if your vault is `~/Documents/MyVault`, name the repo `MyVault`). Keeps things easy to track.
- **Visibility: Private** — critical, your vault has personal data.

Leave everything else as the defaults.

Click **"Create repository"**. On the next page, copy the HTTPS URL it shows you (looks like `https://github.com/USERNAME/MyVault.git`).

---

## 4. Push your vault to GitHub

Back in Terminal (still open from Step 2), paste these one at a time. **Replace the path and URL** with your own — change `~/Documents/MyVault` to wherever your vault actually lives, and paste your repo URL from Step 3 in place of the placeholder:

```bash
cd ~/Documents/MyVault
git init
git add .
git commit -m "initial vault"
git branch -M main

 https://github.com/USERNAME/MyVault.git
git push -u origin main
```

> **First time using git?** You may see a prompt like "Please tell me who you are" — follow the on-screen hint, run the two `git config --global` commands it suggests, then re-run `git commit`.
>
> **Tip for finding your vault path:** in Obsidian, click your vault name in the bottom-left, then **"Manage vaults"** to see the full path. Or right-click the folder in Finder → "New Terminal at Folder" to skip the `cd` step.

---

## 5. Configure Obsidian Git plugin (optional — defaults work)

Open Obsidian → Settings → Community plugins → **Obsidian Git** → Options.

**The defaults are good for most users** — auto-pull and auto-push every few minutes, with sensible commit messages. You don't need to change anything unless you want to.

If you want to tweak them, the two settings that matter most:
- **Vault backup interval (minutes)** — how often it auto-commits + pushes. Default works; set to `15` if you want less frequent commits.
- **Auto pull interval (minutes)** — how often it pulls changes from GitHub. Default works; set to `15` to match.

**Sanity test the sync is working:** edit any note → open Command Palette (`Cmd+P`) → run **"Obsidian Git: Commit-and-sync"** → refresh your GitHub repo page in the browser. The new commit should appear within a few seconds.

> **Don't see the Obsidian Git options panel?** Restart Obsidian once and check Community plugins again.

---

## 6. Connect Claude Code mobile/web (the real value)

This is what unlocks the mobile↔desktop workflow:

1. Install Claude Code mobile (iOS/Android) or visit claude.com/code on the web
2. **Sign in with your personal Claude account** — see the privacy warning below first
3. Connect GitHub OAuth (same account that owns the vault repo)
4. When you start a new session, pick your vault repo from the list
5. The session sandbox clones fresh `main` at start, pushes back on wrap-up

> ⚠️ **Reminder:** see the privacy section at the top of this doc. If you share your Claude or GitHub account with anyone, stop and fix that before signing in — otherwise they'll have full read/write access to your vault via mobile.

After this, the cross-device flow is:

| Phrase | What happens |
|---|---|
| `"hand off to mobile"` on desktop | Skill writes a pickup doc to `📥 Inbox/Handoffs/`, force-pushes to main. Open mobile → paste the resume command → continue. |
| `"we are done, merge and clean up"` on mobile | Squash-merges the session branch to main. Desktop Obsidian Git pulls within a few minutes. |
| Open an old mobile chat after merge | Reopen Safety Check fetches main, reports ✅ Safe / ⚠️ Mixed / 🛑 Stale before continuing. |

---

## 7. Done — test the loop

1. Edit a note on desktop → wait a few minutes → check GitHub for the commit
2. Open Claude Code mobile → start a session → see the note you edited
3. Edit the note on mobile → wrap up → check desktop for the change (Obsidian Git pulls on its interval)

If something doesn't sync, run `/setup` from Claudian. It auto-fixes the most common issues (community plugins enabled, hooks wired).

---

## Common gotchas

| Symptom | Cause | Fix |
|---|---|---|
| `git push` rejected ("Updates were rejected") | Repo accidentally created with README/.gitignore/license | `git pull --rebase origin main` then re-push, or delete + recreate the GitHub repo empty |
| Obsidian shows no "Source Control" view | Plugin enabled but not loaded | Restart Obsidian |
| Mobile sandbox shows "no repositories available" | OAuth scope missing private-repo access | Re-sign-in with broader scope; check github.com/settings/applications |
| Mobile changes not showing on desktop | Obsidian Git auto-pull hasn't fired yet | Command Palette → "Obsidian Git: Pull" |
| Commits piling up on `claude/<topic>` branch instead of main | Wrap-up phrase missed | On mobile: "we are done, merge to main and clean up" |
| 3+ orphan `claude/*` branches accumulating | Mobile sandbox can't self-delete (403) | Run `/setup` on desktop — surfaces reap commands |

---

## What this unlocks

- Voice-capture ideas on mobile while commuting → on desktop by the time you sit down
- Start a `/dump` brain dump on iPad in the morning → continue on desktop in the evening
- Triage notes via Claude Code mobile when away from laptop
- Hand off complex work between devices via the `session-handoff` skill

The first time the loop works end-to-end is the moment the template stops being "a template" and becomes "your second brain."

---

## Related

- [[CLAUDE]] — full multi-device protocol rules (Vault Sync, Reopen Safety Check, Cross-Device Continuity)
- [[_Getting Started]] — vault personalization (Step 4)
