#!/usr/bin/env python3
"""
PreToolUse hook — validate file path before Write or Edit tool calls.

Hard blocks (decision: block) for:
  R1: Em dash (—) in filename — use a space instead
  R3: Meeting notes inside 🚀 Projects/ must be in a Meetings/ subfolder

Exit 0 + no stdout = allow.
Exit 0 + JSON stdout with decision:block = reject before the tool runs.
"""
import json
import os
import re
import sys

# Vault root — prefer CLAUDE_PROJECT_DIR (set by Claude Code), fall back to
# computing 3 levels up from this script (.claude/hooks/pre-validate.py → vault/)
VAULT = os.environ.get(
    "CLAUDE_PROJECT_DIR",
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Files allowed in the vault root (everything else gets blocked)
VAULT_ROOT_WHITELIST = {
    "CLAUDE.md", "AGENTS.md", "GEMINI.md", "README.md", "Home.md",
    "_Getting Started.md", "_Pre-Install Setup.md", "vault-manifest.json",
    "CHANGELOG.md", "CONTRIBUTING.md", "ARCHITECTURE.md", "LICENSE",
    ".gitignore", ".gitkeep",
}

# Filename patterns that indicate a meeting note
MEETING_NAME_RE = re.compile(
    r"(meeting|call|sync|standup|stand[\-_]up|kickoff|kick[\-_]off|debrief|interview)",
    re.IGNORECASE,
)


def block(reason: str):
    """Emit a hard block decision and exit."""
    sys.stdout.write(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # Malformed payload — don't block

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    abs_path = (
        file_path
        if os.path.isabs(file_path)
        else os.path.join(VAULT, file_path)
    )
    filename = os.path.basename(abs_path)

    # R0: No user notes in vault root
    try:
        rel = os.path.relpath(abs_path, VAULT).replace("\\", "/")
        if "/" not in rel and filename not in VAULT_ROOT_WHITELIST:
            block(
                f"❌ VAULT RULE: '{filename}' would land in the vault root. "
                "All notes belong in a subfolder. "
                "Common homes: 📥 Inbox/, 💡 Ideas/, 📰 Clippings/"
            )
    except ValueError:
        pass  # Different drive (Windows) — skip check

    # R1: No em dash in filename
    if "—" in filename:  # — (em dash, U+2014)
        block(
            f"❌ VAULT RULE: Em dash (—) in filename ‘{filename}’. "
            "Use a space instead. Rename before writing."
        )

    # R3: Meeting notes inside 🚀 Projects/ must live in a Meetings/ subfolder
    projects_marker = "\U0001f680 Projects"  # 🚀 Projects
    if projects_marker in abs_path and filename.endswith(".md"):
        if MEETING_NAME_RE.search(filename):
            after_projects = abs_path[abs_path.index(projects_marker):]
            path_parts = after_projects.replace("\\", "/").split("/")
            # path_parts: ["🚀 Projects", "<client-or-category>", "<project>", ...]
            # "Meetings" must appear at depth 3+ (inside a project folder)
            inner_parts = path_parts[2:]
            if "Meetings" not in inner_parts:
                # Suggest the corrected path
                project_root = "/".join(path_parts[:3])
                block(
                    f"❌ VAULT RULE: Meeting note ‘{filename}’ must be inside a "
                    f"Meetings/ subfolder, not the project root. "
                    f"Correct path: {project_root}/Meetings/{filename}"
                )


if __name__ == "__main__":
    main()
