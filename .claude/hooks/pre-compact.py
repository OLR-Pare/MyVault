#!/usr/bin/env python3
"""
PreCompact hook — inject Memory.md context before conversation compaction.

Fires when the user runs /compact. Reads 🧠 Brain/Memory.md and emits
a dense summary of active strategic context so the compacted conversation
preserves current vault state — active projects, open decisions, pending items.

Output: {"customSummary": "..."} — prepended to the compaction prompt.
Silent exit 0 if Memory.md is missing or empty.

Note: Claude Code fires this hook as "PreCompact". If the hook doesn't appear
to fire, verify the event name matches your Claude Code version.
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

# Compact gets more sections than SessionStart — it's a one-time event
MAX_SECTIONS = 15
MAX_BULLETS_PER_SECTION = 5


def extract_active_context(content: str) -> tuple[list[str], int]:
    """
    Extract H3 sections from '## Active Strategic Context'.
    Returns (list_of_section_blocks, total_section_count).
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

    blocks = []
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

        block = f"### {heading}"
        if bullets:
            block += "\n" + "\n".join(bullets)
        blocks.append(block)

    return blocks, total


def main():
    try:
        sys.stdin.read()
    except Exception:
        pass

    try:
        with open(MEMORY_PATH, encoding="utf-8") as f:
            content = f.read()
    except OSError:
        sys.exit(0)

    blocks, total = extract_active_context(content)
    if not blocks:
        sys.exit(0)

    shown = len(blocks)
    body = "\n\n".join(blocks)
    tail = (
        f"\n\n...and {total - shown} more active items not shown above."
        if total > shown
        else ""
    )

    custom_summary = (
        f"## Active Vault Context — preserve this in the compacted summary\n\n"
        f"Source: \U0001f9e0 Brain/Memory.md ({shown} of {total} active items)\n\n"
        f"{body}{tail}\n\n"
        f"INSTRUCTION: The compacted summary must retain the above active project "
        f"context so future turns have full strategic awareness without re-reading Memory.md."
    )

    # Output as hookSpecificOutput (standard hook pattern) so Claude Code
    # includes this as additionalContext before compaction runs.
    sys.stdout.write(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreCompact",
            "additionalContext": custom_summary,
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
