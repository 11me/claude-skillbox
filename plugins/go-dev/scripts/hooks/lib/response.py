"""Hook response builders for Claude Code hooks (minimal version for go-dev)."""

import json


def ask(reason: str, event: str = "PreToolUse", context: str | None = None) -> None:
    """Ask for user permission."""
    output: dict = {
        "hookSpecificOutput": {
            "hookEventName": event,
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }
    if context:
        output["hookSpecificOutput"]["additionalContext"] = context
    print(json.dumps(output))


def allow(event: str | None = None) -> None:
    """Allow action."""
    if event:
        if event in ("Stop", "SubagentStop"):
            print(json.dumps({}))
        else:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": event}}))
