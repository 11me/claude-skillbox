#!/usr/bin/env python3
"""SessionStart hook: inject TDD guidelines when TDD mode is enabled.

TDD mode is detected via:
1. Explicit config in .claude/tdd-enforcer.local.md
2. Auto-detect by presence of test files
"""

import json
import sys
from pathlib import Path

# Import shared detection utilities from workflow plugin
# This avoids code duplication between plugins
_workflow_lib = Path(__file__).parent.parent.parent.parent / "workflow/scripts/hooks/lib"
if _workflow_lib.exists():
    sys.path.insert(0, str(_workflow_lib))
    from detector import detect_tdd_mode
else:
    # Fallback if workflow plugin not available
    def detect_tdd_mode(cwd: Path) -> dict[str, bool]:
        """Minimal fallback detection."""
        result = {"enabled": False, "strict": False}
        config_path = cwd / ".claude" / "tdd-enforcer.local.md"
        if config_path.exists():
            try:
                content = config_path.read_text(errors="ignore")
                if "enabled: true" in content:
                    result["enabled"] = True
                if "strictMode: true" in content:
                    result["strict"] = True
            except OSError:
                pass
        return result


def main() -> None:
    cwd = Path.cwd()
    output_lines: list[str] = []

    tdd_status = detect_tdd_mode(cwd)
    if not tdd_status["enabled"]:
        return

    # Try to load TDD-GUIDELINES.md from plugin
    guidelines_path = Path(__file__).parent.parent.parent / "skills/tdd-enforcer/TDD-GUIDELINES.md"

    mode_label = "STRICT" if tdd_status["strict"] else "ACTIVE"
    output_lines.append(f"## TDD Mode ({mode_label})")
    output_lines.append("")

    if guidelines_path.exists():
        guidelines = guidelines_path.read_text().strip()
        output_lines.append(guidelines)
    else:
        output_lines.append("**Cycle:** RED -> GREEN -> REFACTOR")
        output_lines.append("1. Write failing test FIRST")
        output_lines.append("2. Minimal implementation to pass")
        output_lines.append("3. Refactor with tests passing")

    output_lines.append("")

    if output_lines:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": "\n".join(output_lines),
                    }
                }
            )
        )


if __name__ == "__main__":
    main()
