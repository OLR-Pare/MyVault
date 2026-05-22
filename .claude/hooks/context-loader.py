#!/usr/bin/env python3
"""
SessionStart hook — inject active context from 🧠 Brain/Memory.md.

Reads Memory.md and emits a compact summary of the Active Strategic Context
as a systemMessage so every session starts knowing what's active — no need
to manually say "read my memory file."

Output: {"systemMessage": "..."} or silent exit 0 if Memory.md is missing/empty.
"""
import json
import os
import re
import sys

VAULT = os.environ.get(
    "CLAUDE_PROJECT_DIR",
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

MEMORY_PATH = os.path.join(VAULT, "\U0001f9e0 Brain", "Memory.md")

# Max bullet lines to show per section (keeps systemMessage lean)
MAX_BULLETS_PER_SECTION = 3
# Max sections to include (first N are most recent — file is newest-first)
MAX_SECTIONS = 8


def extract_active_context(content: str) -> tuple[list[str], int]:
    """
    Extract H3 sections from '## Active Strategic Context'.
    Returns (list_of_summary_blocks, total_section_count).
    """
    h2_match = re.search(r"^## Active Strategic Context\s*$", content, re.MULTILINE)
    if not h2_match:
        return [], 0

    section_start = h2_match.end()
    next_h2 = re.search(r"^## ", content[section_start:], re.MULTILINE)
    section_body = (
        content[section_start: section_start + next_h2.start()]
        if next_h2
        else content[section_start:]
    )

    h3_pattern = re.compile(r"^### (.+)$", re.MULTILINE)
    h3_matches = list(h3_pattern.finditer(section_body))
    total = len(h3_matches)

    summaries = []
    for i, m in enumerate(h3_matches[:MAX_SECTIONS]):
        heading = m.group(1).strip()
        body_start = m.end()
        body_end = (
            h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(section_body)
        )
        body = section_body[body_start:body_end].strip()

        bullets = [
            ln.strip()
            for ln in body.splitlines()
            if ln.strip().startswith("- ") or ln.strip().startswith("* ")
        ][:MAX_BULLETS_PER_SECTION]

        block = f"**{heading}**"
        if bullets:
            block += "\n" + "\n".join(bullets)
        summaries.append(block)

    return summaries, total


def main():
    # Consume stdin (hook protocol requires it) — ignore payload for SessionStart
    try:
        sys.stdin.read()
    except Exception:
        pass

    try:
        with open(MEMORY_PATH, encoding="utf-8") as f:
            content = f.read()
    except OSError:
        sys.exit(0)  # Memory.md not found — silent

    summaries, total = extract_active_context(content)
    if not summaries:
        sys.exit(0)

    shown = len(summaries)
    body = "\n\n".join(summaries)

    msg = (
        f"\U0001f9e0 Vault context loaded ({shown} of {total} active items "
        f"from Memory.md):\n\n{body}"
    )
    if total > shown:
        msg += f"\n\n...and {total - shown} more. See [[\U0001f9e0 Brain/Memory.md]] for full context."

    sys.stdout.write(json.dumps({"systemMessage": msg}))
    sys.exit(0)


if __name__ == "__main__":
    main()
