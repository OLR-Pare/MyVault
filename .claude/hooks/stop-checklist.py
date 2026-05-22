#!/usr/bin/env python3
"""
Stop hook — print cascade checklist at session end.

Fires every time Claude stops. Reminds Claude to check whether
cascading updates (People, Decisions, Memory, To-Do) actually happened
before the session closes.

Exits silently when stop_hook_active=True to prevent recursive triggering.
"""
import json
import sys


def main():
    # Guard against recursive triggering
    try:
        raw = sys.stdin.read()
        if raw.strip():
            payload = json.loads(raw)
            if payload.get("stop_hook_active") is True:
                sys.exit(0)
    except Exception:
        pass  # Malformed input — still print the checklist

    checklist = (
        "Session end — verify these cascades happened:\n"
        "  - People mentioned → 👤 People/ interaction logs updated?\n"
        "  - Decisions made → 🧠 Brain/Decisions.md logged?\n"
        "  - Project status changed → 🧠 Brain/Memory.md updated?\n"
        "  - New tasks surfaced → 📥 Inbox/To-Do.md updated?\n"
        "  - Meeting note created → linked to project + people tagged?\n"
        "If anything was missed, fix it now before stopping."
    )

    sys.stdout.write(checklist + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
