#!/usr/bin/env python3
"""SessionStart hook: check production workflow compliance.

Checks for:
- CLAUDE.md presence
- Pre-commit hooks installation
- Beads initialization
- Tests presence
"""

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.detector import has_tests
from lib.response import session_output


def main() -> None:
    cwd = Path.cwd()
    output_lines: list[str] = []
    missing_count = 0

    # Check CLAUDE.md presence
    claude_md = cwd / "CLAUDE.md"
    claude_md_alt = cwd / ".claude" / "CLAUDE.md"

    if not claude_md.exists() and not claude_md_alt.exists():
        output_lines.append("Missing: CLAUDE.md (AI context file)")
        missing_count += 1

    # Check pre-commit hooks
    pre_commit_config = cwd / ".pre-commit-config.yaml"
    pre_commit_hook = cwd / ".git" / "hooks" / "pre-commit"

    if pre_commit_config.exists():
        if not pre_commit_hook.exists():
            output_lines.append("Pre-commit not installed: Run `pre-commit install`")
            missing_count += 1
    else:
        output_lines.append("Missing: .pre-commit-config.yaml")
        missing_count += 1

    # Check beads initialization
    beads_dir = cwd / ".beads"
    if not beads_dir.is_dir():
        output_lines.append("Optional: No .beads/ directory (task tracking)")

    # Check tests
    if not has_tests(cwd):
        output_lines.append("No tests found: Consider adding tests/")

    # Summary for multiple missing items
    if missing_count >= 2:
        output_lines.append("")
        output_lines.append("Suggestion: Multiple workflow components missing.")
        output_lines.append("Consider running project initialization to set up:")
        output_lines.append("- CLAUDE.md for AI context")
        output_lines.append("- Pre-commit hooks for quality gates")
        output_lines.append("- Beads for task tracking")

    # Output if there's something to report
    if output_lines:
        message = "**Workflow Check:**\n" + "\n".join(f"- {line}" for line in output_lines)
        session_output(message)


if __name__ == "__main__":
    main()
