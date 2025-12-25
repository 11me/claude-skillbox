"""Hook response builders for Claude Code hooks."""

import json


def session_output(message: str) -> None:
    """Output message for SessionStart hooks.

    Args:
        message: The message to output (supports markdown).
    """
    if message:
        print(json.dumps({"output": message}))


def block(reason: str, event: str = "PreToolUse") -> None:
    """Block action with reason.

    Args:
        reason: The reason for blocking.
        event: The hook event name.
    """
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": event,
                    "permissionDecision": "block",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def ask(reason: str, event: str = "PreToolUse") -> None:
    """Ask for user permission.

    Args:
        reason: The reason for asking.
        event: The hook event name.
    """
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": event,
                    "permissionDecision": "ask",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def allow() -> None:
    """Allow action without output (exit 0, no output)."""
    pass
