# Hooks Development Guide

## Language Policy

**Python-first**: All hooks MUST be written in Python.

Bash is allowed ONLY when:
- Hook is less than 10 lines
- No logic (just calling a single command)
- No conditionals or loops

## Directory Structure

```
scripts/hooks/
├── lib/                    # Shared utilities
│   ├── __init__.py
│   ├── detector.py         # Project type detection
│   └── response.py         # Hook response builders
├── session_context.py      # SessionStart: inject context
├── flow_check.py           # SessionStart: workflow compliance
├── skill_suggester.py      # SessionStart: suggest skills
├── git-push-guard.py       # PreToolUse: confirm git push
├── pretool-secret-guard.py # PreToolUse: block secrets
├── prompt-guard.py         # UserPromptSubmit: validate input
└── stop-done-criteria.py   # Stop: enforce completion criteria
```

## Hook Template

```python
#!/usr/bin/env python3
"""Hook description.

Event: SessionStart | PreToolUse | UserPromptSubmit | Stop
"""

import json
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.detector import detect_project_types
from lib.response import session_output, block, ask


def main() -> None:
    # For hooks that receive input
    data = json.load(sys.stdin)

    # Your logic here
    # ...

    # Output response
    session_output("Your message")


if __name__ == "__main__":
    main()
```

## Available Utilities

### lib.detector

```python
from lib.detector import detect_project_types, detect_flux, has_tests

# Detect all project types
types = detect_project_types()
# Returns: {"helm": bool, "gitops": bool, "go": bool, ...}

# Check for Flux GitOps
is_flux = detect_flux()

# Check for tests
has_tests = has_tests()
```

### lib.response

```python
from lib.response import session_output, block, ask, allow

# SessionStart: output message
session_output("**Project type:** Helm chart")

# PreToolUse: block action
block("Git push blocked. Run manually.")

# PreToolUse: ask for permission
ask("Git push requires confirmation")

# PreToolUse: allow (no output, exit 0)
allow()
```

## Hook Events

| Event | Trigger | Input | Use Case |
|-------|---------|-------|----------|
| SessionStart | Session begins | `{}` | Inject context, detect project |
| PreToolUse | Before tool execution | `{"tool_name": "...", "tool_input": {...}}` | Validate, block, ask permission |
| UserPromptSubmit | User sends message | `{"prompt": "..."}` | Validate commands |
| Stop | Session ends | `{}` | Enforce completion criteria |

## Adding a New Hook

1. Create `scripts/hooks/your_hook.py` using the template above
2. Add entry to `hooks/hooks.json`:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolName",  // optional, for PreToolUse
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/hooks/your_hook.py"
          }
        ]
      }
    ]
  }
}
```

3. Test locally:

```bash
echo '{}' | python3 plugins/skillbox/scripts/hooks/your_hook.py
```

## Testing Hooks

```bash
# Test SessionStart hooks
echo '{}' | python3 plugins/skillbox/scripts/hooks/session_context.py
echo '{}' | python3 plugins/skillbox/scripts/hooks/flow_check.py
echo '{}' | python3 plugins/skillbox/scripts/hooks/skill_suggester.py

# Test PreToolUse hooks
echo '{"tool_name": "Bash", "tool_input": {"command": "git push"}}' | \
  python3 plugins/skillbox/scripts/hooks/git-push-guard.py

# Run with Claude Code
claude --plugin-dir ./plugins/skillbox
```
