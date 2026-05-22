---
description: "Vault health check + enable in-Obsidian editing of slash commands. Run on first launch or when something feels off."
---

Run a full health check on this vault. Execute the script below, then summarize the report to the user with a clear ✅/❌/⚠️ verdict on each check and specific fix instructions for any failures.

```bash
python3 <<'EOF'
import os, json, sys

vault = os.getcwd()
results = []

def ok(msg): results.append(('ok', msg))
def warn(msg): results.append(('warn', msg))
def fail(msg): results.append(('fail', msg))
def fix(action, msg): results.append(('fix', f'{action}: {msg}'))

# --- 1. Required folders ---
required_folders = [
    '📓 Journals', '🧠 Brain', '🧩 Templates', '👤 People',
    '🚀 Projects', '💡 Ideas', '🤝 Meetings', '📥 Inbox',
    '📎 Attachments', '📚 Learnings', '💼 Company',
]
for f in required_folders:
    if os.path.isdir(f):
        ok(f'folder exists: {f}/')
    else:
        fail(f'missing folder: {f}/')

# --- 2. Brain files ---
brain_files = ['User.md', 'Memory.md', 'North Star.md', 'Decisions.md', 'Patterns.md', 'Gotchas.md']
for f in brain_files:
    p = os.path.join('🧠 Brain', f)
    if os.path.isfile(p):
        ok(f'brain file exists: {p}')
    else:
        fail(f'missing brain file: {p}')

# --- 3. Template files ---
template_files = [
    'Daily Journal Template.md', 'Meeting Note Template.md',
    'Idea Note Template.md', 'Project Template.md',
    'Person Template.md', 'Learning Note Template.md',
    'Company Overview Template.md',
]
for f in template_files:
    p = os.path.join('🧩 Templates', f)
    if os.path.isfile(p):
        ok(f'template exists: {f}')
    else:
        warn(f'missing template: {f}')

# --- 3b. Bundled skills (auto-discovered from .claude/skills/) ---
skills_dir = os.path.join('.claude', 'skills')
if os.path.isdir(skills_dir):
    skills = sorted(d for d in os.listdir(skills_dir)
                    if os.path.isdir(os.path.join(skills_dir, d)) and not d.startswith('.'))
    if not skills:
        warn(f'{skills_dir}/ exists but contains no skills')
    for s in skills:
        skill_md = os.path.join(skills_dir, s, 'SKILL.md')
        if not os.path.isfile(skill_md):
            warn(f'skill folder has no SKILL.md: {s}')
            continue
        # Pull description from frontmatter
        desc = ''
        try:
            txt = open(skill_md).read()
            if txt.startswith('---'):
                fm_end = txt.find('\n---', 3)
                if fm_end > 0:
                    for line in txt[3:fm_end].splitlines():
                        if line.lower().startswith('description:'):
                            desc = line.split(':', 1)[1].strip().strip('"\'')
                            if len(desc) > 90:
                                desc = desc[:87] + '...'
                            break
        except Exception:
            pass
        ok(f'skill: {s}' + (f' — {desc}' if desc else ''))
else:
    warn(f'{skills_dir}/ missing')

# --- 4. Slash commands present ---
expected_commands = ['dump.md', 'gm.md', 'gn.md', 'setup.md']
for c in expected_commands:
    p = os.path.join('.claude', 'commands', c)
    if os.path.isfile(p):
        ok(f'slash command present: /{c[:-3]}')
    else:
        fail(f'missing slash command: {p}')

# --- 5. Templates core plugin config ---
tpl_path = '.obsidian/templates.json'
if os.path.isfile(tpl_path):
    try:
        tpl = json.load(open(tpl_path))
        folder = tpl.get('folder', '')
        if os.path.isdir(folder):
            ok(f'Templates plugin folder resolves: {folder}')
        else:
            fail(f'Templates plugin folder missing: {folder}')
            fix('EDIT', f'{tpl_path} → set folder to "🧩 Templates"')
    except Exception as e:
        fail(f'templates.json unreadable: {e}')
else:
    warn('templates.json missing — core Templates plugin has no folder configured')

# --- 7. Core plugins: daily-notes should be off (GN handles dailies) ---
cp_path = '.obsidian/core-plugins.json'
if os.path.isfile(cp_path):
    try:
        cp = json.load(open(cp_path))
        if cp.get('daily-notes') is True:
            warn("core plugin 'daily-notes' is enabled — disable it, GN handles journal creation")
        else:
            ok("core plugin 'daily-notes' disabled (GN handles dailies)")
    except Exception:
        pass

# --- 8. Community plugins enabled ---
comm_path = '.obsidian/community-plugins.json'
if os.path.isfile(comm_path):
    try:
        enabled = json.load(open(comm_path))
        for p in ['claudian', 'obsidian42-brat', 'terminal']:
            if p in enabled:
                ok(f'community plugin enabled: {p}')
            else:
                warn(f'community plugin NOT enabled: {p}')
    except Exception:
        pass

# --- 9. CLAUDE.md placeholder check ---
if os.path.isfile('CLAUDE.md'):
    txt = open('CLAUDE.md').read()
    if '[Your Name]' in txt or '[Your Role]' in txt:
        warn('CLAUDE.md not personalized yet — see _Getting Started.md Step 4 (do NOT edit manually; the prompt-driven flow is faster and richer)')
    else:
        ok('CLAUDE.md personalized')

# --- 10. User.md placeholder check ---
user_md = '🧠 Brain/User.md'
if os.path.isfile(user_md):
    txt = open(user_md).read()
    if '**Name:**\n' in txt or '**Name:** \n' in txt or '- **Name:**\n' in txt:
        warn(f'{user_md} not personalized yet — see _Getting Started.md Step 4 (do NOT edit manually; the prompt-driven flow is faster and richer)')
    else:
        ok(f'{user_md} has content')

# --- 11. Required Claude Code plugins (auto-install if missing) ---
required_cc_plugins = {
    'superpowers':          'Powers all slash commands (/gm, /gn, /eod, /dump, /weekly-review, etc.)',
    'claude-md-management': 'Keeps CLAUDE.md updated as rules evolve',
    'context7':             'Live library/framework doc lookup during coding',
}
import pathlib, subprocess
plugins_json = pathlib.Path.home() / '.claude' / 'plugins' / 'installed_plugins.json'
if plugins_json.exists():
    try:
        pdata = json.load(open(plugins_json))
        installed = pdata.get('plugins', {})
        for plugin, desc in required_cc_plugins.items():
            matches = [k for k in installed if k.startswith(plugin + '@')]
            if matches:
                ok(f'Claude Code plugin installed: {plugin} — {desc}')
            else:
                result = subprocess.run(
                    ['claude', 'plugin', 'install', plugin],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    ok(f'Claude Code plugin installed: {plugin} — {desc}')
                else:
                    fail(f'failed to install Claude Code plugin: {plugin} — {result.stderr.strip()}')
    except Exception as e:
        warn(f'Could not check/install Claude Code plugins: {e}')
else:
    warn('Claude Code plugins list not found — is Claude Code installed? (https://claude.ai/code)')

# --- 12. Task-done chime hook ---
CHIME_CMD = 'afplay /System/Library/Sounds/Glass.aiff &'
settings_json = pathlib.Path.home() / '.claude' / 'settings.json'
try:
    cfg = json.loads(settings_json.read_text()) if settings_json.exists() else {}
    stop_hooks = cfg.get('hooks', {}).get('Stop', [])
    already = any(
        h.get('command', '') == CHIME_CMD
        for entry in stop_hooks
        for h in entry.get('hooks', [])
    )
    if already:
        ok('task-done chime hook already configured (Glass)')
    else:
        cfg.setdefault('hooks', {}).setdefault('Stop', []).append({
            'hooks': [{'type': 'command', 'command': CHIME_CMD, 'timeout': 5}]
        })
        settings_json.write_text(json.dumps(cfg, indent=2))
        ok('task-done chime hook installed (Glass) — plays when Claude finishes a task')
except Exception as e:
    warn(f'Could not configure chime hook: {e}')

# --- 13. In-Obsidian edit symlinks ---
# .claude/ is hidden from Obsidian's file tree. These symlinks expose
# slash commands and skills inside 🧠 Brain/ so they're editable from
# inside Obsidian. Pure convenience — slash commands work fine without
# them. Doing this in Python (not shell) so it runs as part of the same
# subprocess as the health check above, no matter who invokes /setup.
symlink_pairs = [
    ('🧠 Brain/Commands', '../.claude/commands'),
    ('🧠 Brain/Skills',   '../.claude/skills'),
]
for link, target in symlink_pairs:
    if os.path.islink(link):
        ok(f'in-Obsidian edit link present: {link}')
    elif os.path.exists(link):
        warn(f'{link} exists as a real path — skipped (move it elsewhere if you want in-Obsidian editing)')
    else:
        try:
            os.symlink(target, link)
            ok(f'created in-Obsidian edit link: {link} -> {target}')
        except OSError as e:
            fail(f'could not create {link}: {e}')

# --- Output ---
print()
print('=' * 60)
print('VAULT HEALTH CHECK')
print('=' * 60)
for kind, msg in results:
    icon = {'ok': '✅', 'warn': '⚠️ ', 'fail': '❌', 'fix': '   →'}[kind]
    print(f'{icon} {msg}')
print()
counts = {k: sum(1 for r in results if r[0] == k) for k in ['ok', 'warn', 'fail']}
print(f"Summary: {counts['ok']} passing, {counts['warn']} warnings, {counts['fail']} failures")
sys.exit(0 if counts['fail'] == 0 else 1)
EOF
```

After running, tell the user:

1. **If all passing:** "Vault healthy. You're good to go."

2. **If warnings only:** list each warning briefly. Special handling for placeholder warnings (CLAUDE.md / User.md not personalized):
   - **Do NOT instruct the user to manually edit those files.** Manual editing is the low-quality path.
   - **Do NOT offer an inline shortcut to personalize them now.** That competes with Step 4 of `_Getting Started.md` and confuses the linear setup flow.
   - **Just tell them to continue with Step 4 in `_Getting Started.md`** ("Tell Claudian who you are"). That step has the full prompt-driven flow with Lark cross-check across User, North Star, Company, People, and Projects.
   - For other warnings (e.g. missing optional skill, plugin not enabled), just describe what they mean.

3. **If failures:** list each failure with the specific fix command/action, ordered by severity (missing folders/commands first, then plugin configs, then placeholder content).
