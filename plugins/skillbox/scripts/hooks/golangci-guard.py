#!/usr/bin/env python3
"""PreToolUse hook: protects .golangci.yml files from unintended edits."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.response import allow, ask

# Paths where editing is always allowed (our own templates/development)
ALLOWED_PATHS = ("/templates/", "/skillbox/", "/claude-skillbox/")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        allow("PreToolUse")
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if tool_name not in ("Write", "Edit"):
        allow("PreToolUse")
        return

    # Not a golangci config file
    if Path(file_path).name not in (".golangci.yml", ".golangci.yaml"):
        allow("PreToolUse")
        return

    # Allow editing our own templates/skill files
    if any(allowed in file_path for allowed in ALLOWED_PATHS):
        allow("PreToolUse")
        return

    # For real project configs - ask for confirmation
    ask(
        reason="Modifying .golangci.yml — confirm this is intentional",
        event="PreToolUse",
        context=(
            "Linting config is a protected file.\nApprove if you explicitly requested this change."
        ),
    )


if __name__ == "__main__":
    main()
