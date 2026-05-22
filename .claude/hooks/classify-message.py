#!/usr/bin/env python3
"""
UserPromptSubmit hook — classify user messages and inject routing hints.

Reads the hook JSON payload from stdin, checks the `prompt` field against
signal patterns defined in classify-signals.json (same directory), and emits
hookSpecificOutput routing hints when matches are found.

Silently exits on malformed input, missing prompt, or zero matches.
Configure signals by editing classify-signals.json — no code changes needed.
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIGNALS_FILE = os.path.join(SCRIPT_DIR, "classify-signals.json")


def main():
    # Read stdin JSON payload
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)
        payload = json.loads(raw)
    except Exception:
        sys.exit(0)

    prompt = payload.get("prompt", "")
    if not isinstance(prompt, str) or not prompt:
        sys.exit(0)

    hook_event_name = payload.get("hook_event_name", "UserPromptSubmit")

    # Load signal definitions
    try:
        with open(SIGNALS_FILE, encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        sys.exit(0)  # No signals file — pass silently

    signals = config.get("signals", [])
    matched_messages = []

    prompt_lower = prompt.lower()
    for signal in signals:
        patterns = signal.get("patterns", [])
        message = signal.get("message", signal.get("name", ""))
        for pattern in patterns:
            # Word-boundary-aware match: pattern must not be surrounded by Latin letters.
            # Handles mixed Latin/non-Latin (e.g. Indonesian, emoji) correctly.
            escaped = re.escape(pattern.lower())
            regex = rf"(?<![a-zA-Z]){escaped}(?![a-zA-Z])"
            if re.search(regex, prompt_lower):
                matched_messages.append(message)
                break  # One match per signal is enough

    if not matched_messages:
        sys.exit(0)

    hints = "\n".join(f"- {m}" for m in matched_messages)
    additional_context = (
        "Content classification hints (act on these if relevant to the message):\n"
        + hints
        + "\n\nRemember: use proper templates, add [[wikilinks]], follow CLAUDE.md conventions."
    )

    sys.stdout.write(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": hook_event_name,
            "additionalContext": additional_context,
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
