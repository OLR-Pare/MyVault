# Pre-Install Setup — Second Brain Vault

Read this **before** you download the vault. This guide covers everything you need to install on your laptop once. After you're done, download from GitHub → extract → open in Obsidian → an in-vault `_Getting Started.md` takes you the rest of the way.

> 👋 **Never used Terminal before?** No problem. This pre-flight is the only time you'll really need it — once it's done, you'll live inside Obsidian / Claudian and rarely touch a command line again. Read the **"Opening Terminal"** box below first, then go through the steps top to bottom.

---

## Opening Terminal (if you've never done it)

Press `Cmd + Space` to open Spotlight, type **terminal**, press Enter. A black or white window will appear with a blinking cursor — that's it. You'll paste commands from this guide, hit Enter, and wait.

A few things to know so nothing surprises you:

- 🔒 **The password prompt.** When a command starts with `sudo`, your Mac will ask for your login password (the one you use to unlock your Mac). **It won't show characters as you type — that's normal, not broken.** Type, press Enter.
- 📋 **Copy commands one at a time.** Each code block in this guide has a copy button on hover. Paste into Terminal, press Enter, wait for it to finish, then move to the next.
- 🛟 **Nothing here can break your Mac.** All the commands below are standard developer setup — millions of people run them every day.
- ❓ **If something errors out**, copy the error message and ping whoever shared this template with you — don't keep retrying blindly.

---

## Step 0 — macOS only: Xcode Command Line Tools

Required by `npm` for some packages (`git`, native dependencies). It's a one-time install, ~500 MB, but **Apple's servers are slow** — typically 20–60 min. Start this first and let it run while you install the other tools.

```bash
xcode-select --install
```

This is **not** the full Xcode IDE (10+ GB from the App Store) — you don't need that. Just the Command Line Tools. If a dialog pops up, click **Install**, agree to the license, and walk away.

To verify it finished:

```bash
xcode-select -p
```

Should print a path like `/Library/Developer/CommandLineTools`.

---

## Step 1 — Install the rest

While Step 0 is downloading, install these. **Order matters: install Node.js first**, the others can be in any order, but the Lark CLI commands at the bottom won't work until Node is installed.

| #   | Tool                                        | Why                                                                                                                                                                                      | How / Where                                                                                                                          |
| --- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Node.js v18+                                | Lark CLI runs on Node                                                                                                                                                                    | GUI installer — https://nodejs.org/ (click the "LTS" download)                                                                       |
| 2   | Obsidian                                    | The note app                                                                                                                                                                             | GUI installer — https://obsidian.md/                                                                                                 |
| 3   | Claude Code (CLI)                           | Terminal-side AI, powers `/setup` etc.                                                                                                                                                   | Terminal install — https://claude.com/product/claude-code (follow their instructions, then run `claude` once to sign in via browser) |
| 4   | Lark CLI + skills                           | Talk to Lark from the terminal                                                                                                                                                           | Terminal install — see below                                                                                                         |
| 5   | Wispr Flow *(optional, highly recommended)* | System-wide voice dictation — speak to Claudian instead of typing. Significantly faster than typing and handles Indonesian well. Works in any app: Claudian, Claude.ai, Telegram, Slack. | https://wisprflow.ai/r?NICK3397<br>(FREE 1 month)                                                                                    |

> 🎙️ **Why Wispr Flow matters for this vault:** The whole point of `/dump`, `/gn`, and `/gm` is low-friction capture. You speak roughly 3-4x faster than you type, and Wispr Flow lets you just talk to Claudian like you'd talk to a friend — in English, Indonesian, or mixed. Once it's installed, press your hotkey anywhere, speak, and it transcribes directly into the chat input. No extra app to switch to.

---

## Step 2 — Lark CLI install

> 🛟 **Heads up:** Lark CLI here uses a **shared custom Lark app**, and you need credentials to connect to it.
> - **If someone shared this template with you** (a "distributor") — ask them for the App ID + Secret. They'll send it to you directly; it's not in this doc by design.
> - **If you found this on GitHub independently** — you can either skip this whole section (the vault works fine without Lark CLI), or create your own Lark custom app and use those credentials in the steps below.

Run these **one at a time** in your terminal.

**1. Install the CLI globally**

```bash
sudo npm install -g @larksuite/cli
```

This is your first `sudo` command — your Mac will ask for your login password. The cursor won't move while you type, that's normal. Press Enter when done.

**2. Install the Lark skills for Claude Code**

```bash
npx skills add larksuite/cli -y -g
```

⚠️ This step has been flaky in past installs. After running it, verify it worked: open Claude Code (`claude` in terminal), type `/`, and you should see `lark-*` skills in the autocomplete (`lark-calendar`, `lark-doc`, `lark-im`, etc.). If they don't appear, re-run the command. Still missing → ping whoever shared this template with you.

**3. Configure the shared Lark app**

```bash
lark-cli config init
```

- When prompted for **profile name**, use **`org-lark-cli`** (this name is required — the bundled `lark-minutes-debrief` skill expects it).
- When prompted for credentials, choose **"Enter app credentials yourself"**.
- Ask whoever shared this template with you for the **App ID + Secret**.

**4. Log in with your Lark account**

```bash
lark-cli auth login --recommend
```

A browser link will appear. Open it, log in with your Lark account, approve the permissions.

---

## Step 3 — Download and open the vault

1. Go to the GitHub repo: https://github.com/nickyudha/second-brain
2. Click **Code** → **Download ZIP**.
3. **Extract the zip.** You'll get a folder like `second-brain-main/` containing `README.md` and **`My Vault/`**.
4. **Drag the inner `My Vault/` folder into `~/Documents/`.** (You can rename it if you want — `My Brain`, `<YourName> Brain`, etc. The folder name becomes your vault name in Obsidian.)
5. **Open Obsidian.** From the welcome screen, click "Open folder as vault" → choose `~/Documents/My Vault/` (or whatever you renamed it to) → Open.
6. Obsidian opens the vault. `_Getting Started.md` should appear automatically in the main pane.

---

## Step 4 — Continue inside Obsidian

From here, **read `_Getting Started.md` inside the vault.** It walks you through:

- Trusting community plugins (one-time click)
- Signing into Claudian with your Claude subscription
- Running `/setup` to verify everything's wired
- Telling Claudian who you are (using a clever prompt that pulls your context from any AI you already use)
- Kickstart prompts to populate People, Projects, North Star, Company entities
- Daily workflow (`/dump`, `/gn`, `/gm`)

After that you're done with onboarding and the vault starts compounding.

---

> Questions? Ping whoever shared this template with you on Lark.

> 🗑️ *Install reference only — feel free to delete this file once everything's installed and working. You won't need it again unless you reinstall.*
