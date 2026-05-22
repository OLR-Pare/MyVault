#!/usr/bin/env python3
"""
PostToolUse hook — validate note content after Write or Edit tool calls.

Emits non-blocking hookSpecificOutput warnings for:
  - Blank line after frontmatter closing ---
  - Missing `description` field in frontmatter (skipped for journal notes)
  - Missing `type`, `tags`, `date` fields in frontmatter
  - Meeting note missing `people:` field
  - Unfilled {{template}} placeholders
  - No [[wikilinks]] in substantive notes (>300 chars)
  - Broken [[wikilinks]] pointing to non-existent files

These are warnings, not hard blocks — the file is already written.
Claude sees the hints and should fix them in the same response.
"""
import json
import os
import re
import sys

# Vault root — prefer CLAUDE_PROJECT_DIR (set by Claude Code), fall back to
# computing 3 levels up from this script (.claude/hooks/post-validate.py → vault/)
VAULT = os.environ.get(
    "CLAUDE_PROJECT_DIR",
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Path segments that indicate files we should not validate
SKIP_SEGMENTS = [
    ".claude/", ".obsidian/", "Templates/", "🧩 Templates/",
    "_Getting Started", "_Pre-Install", "_About",
]

# Path segments that indicate journal notes (skip description check for these)
JOURNAL_SEGMENTS = ["📓 Journals/", "Journals/"]


def should_skip(file_path: str) -> bool:
    normalized = file_path.replace("\\", "/")
    # Skip non-markdown
    if not normalized.endswith(".md"):
        return True
    # Skip filenames starting with _ (scaffolding)
    if os.path.basename(normalized).startswith("_"):
        return True
    for seg in SKIP_SEGMENTS:
        if seg in normalized:
            return True
    return False


def is_journal(file_path: str) -> bool:
    normalized = file_path.replace("\\", "/")
    return any(seg in normalized for seg in JOURNAL_SEGMENTS)


def check_content(content: str, skip_description: bool = False) -> list[str]:
    warnings = []

    if content.startswith("---\n"):
        rest = content[4:]
        fm_end = re.search(r"^---\s*$", rest, re.MULTILINE)
        if fm_end:
            # Use fm_end.start()+3 (right after the literal ---) rather than
            # fm_end.end() because ^---\s*$ sometimes consumes the trailing \n
            # (when a blank line follows) and sometimes doesn't, making end()
            # unreliable. The two chars after --- are always \n + (blank|\w).
            after_close = rest[fm_end.start() + 3:]
            if after_close[:2] == "\n\n":
                warnings.append(
                    "Blank line after frontmatter closing ---. "
                    "Content must begin immediately after ---. Remove the blank line."
                )

            fm_body = rest[:fm_end.start()]

            if not skip_description and "description:" not in fm_body:
                warnings.append(
                    "Missing `description` field in frontmatter. "
                    "Add a ~150-char summary — helps with search and Bases views."
                )

            if "type:" not in fm_body:
                warnings.append(
                    "Missing `type` field in frontmatter. "
                    "Use: journal, meeting, idea, project, person, decision, note."
                )

            if "tags:" not in fm_body:
                warnings.append("Missing `tags` field in frontmatter.")

            if "date:" not in fm_body:
                warnings.append("Missing `date` field in frontmatter (YYYY-MM-DD).")

            # Meeting notes must list attendees
            if "type: meeting" in fm_body and "people:" not in fm_body:
                warnings.append(
                    "Meeting note missing `people:` field. "
                    "List attendees as wikilinks: people: ['[[Name]]']"
                )

    # Unfilled template placeholder
    if "{{" in content:
        warnings.append(
            "Unfilled template placeholder `{{...}}` found. "
            "Replace all placeholders before saving."
        )

    # Wikilink check: substantive notes must link to at least one other note
    if len(content) > 300 and "[[" not in content:
        warnings.append(
            "No [[wikilinks]] found. Every note must link to at least one other note."
        )

    return warnings


def build_filename_index(vault: str) -> set:
    """Walk the vault once and return a set of all .md filenames (basename only)."""
    index = set()
    try:
        for root, dirs, files in os.walk(vault):
            # Skip hidden dirs to keep the walk fast
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.endswith(".md"):
                    index.add(f)
    except OSError:
        pass
    return index


def strip_code_blocks(content: str) -> str:
    """Remove fenced code blocks and inline code so their content isn't scanned for wikilinks."""
    content = re.sub(r"```[\s\S]*?```", "", content)
    content = re.sub(r"~~~[\s\S]*?~~~", "", content)
    content = re.sub(r"`[^`\n]+`", "", content)
    return content


def check_broken_links(content: str, vault: str, current_file_path: str) -> list[str]:
    """
    Find [[wikilinks]] that don't resolve to an existing file.
    Skips content inside fenced code blocks and inline code to avoid false positives.
    Returns a list of broken link targets (capped at 5 to avoid spam).
    """
    content = strip_code_blocks(content)

    if "[[" not in content:
        return []

    filename_index = build_filename_index(vault)
    wikilink_re = re.compile(r"\[\[([^\]]+)\]\]")
    broken = []
    seen = set()

    for m in wikilink_re.finditer(content):
        raw = m.group(1)
        # Strip display text: [[Target|Display]] → Target
        target = raw.split("|")[0].strip()
        # Strip heading anchors: [[Target#Section]] → Target
        target = target.split("#")[0].strip()
        if not target or target in seen:
            continue
        seen.add(target)

        # Skip external-style references
        if target.startswith("http"):
            continue

        if "/" in target:
            # Path-based link — check relative to vault root
            abs_check = os.path.join(vault, target)
            exists = os.path.exists(abs_check) or os.path.exists(abs_check + ".md")
        else:
            # Filename-only link — resolved by Obsidian anywhere in vault
            exists = (target + ".md") in filename_index

        if not exists:
            broken.append(target)
        if len(broken) >= 5:
            break

    return broken


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    hook_event_name = payload.get("hook_event_name", "PostToolUse")

    if not file_path:
        sys.exit(0)

    if should_skip(file_path):
        sys.exit(0)

    journal = is_journal(file_path)
    tool_name = payload.get("tool_name", "")

    # For Write: content is already in tool_input — no disk read needed
    if tool_name == "Write":
        content = tool_input.get("content", "")
    else:
        # For Edit (and anything else): read the file as it now exists on disk
        abs_path = (
            file_path
            if os.path.isabs(file_path)
            else os.path.join(VAULT, file_path)
        )
        try:
            with open(abs_path, encoding="utf-8") as f:
                content = f.read()
        except OSError:
            sys.exit(0)

    warnings = check_content(content, skip_description=journal)

    # Dead link check — only when the note has wikilinks (skip the "no links" case)
    if "[[" in content:
        abs_path_for_links = (
            file_path if os.path.isabs(file_path) else os.path.join(VAULT, file_path)
        )
        broken = check_broken_links(content, VAULT, abs_path_for_links)
        for target in broken:
            warnings.append(
                f"Broken [[wikilink]]: `{target}` doesn't resolve to any vault file. "
                "Create the note or correct the link."
            )

    if not warnings:
        sys.exit(0)

    hint_list = "\n".join(f"  - {w}" for w in warnings)
    filename = os.path.basename(file_path.replace("\\", "/"))

    sys.stdout.write(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": hook_event_name,
            "additionalContext": (
                f"Vault hygiene warnings for `{filename}`:\n{hint_list}\n"
                "Fix these before moving on."
            ),
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
