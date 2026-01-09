#!/usr/bin/env python3
"""SessionStart hook: inject Go-specific guidelines.

Only activates if go.mod exists in current directory.
"""

import json
from pathlib import Path


def main() -> None:
    cwd = Path.cwd()

    # Only activate for Go projects
    if not (cwd / "go.mod").exists():
        return

    output_lines: list[str] = []

    # Try to load GO-GUIDELINES.md from plugin
    guidelines_path = Path(__file__).parent.parent.parent / "skills/go-development/GO-GUIDELINES.md"
    if guidelines_path.exists():
        guidelines = guidelines_path.read_text().strip()
        output_lines.append("## Go Guidelines")
        output_lines.append("")
        output_lines.append(guidelines)
        output_lines.append("")
    else:
        # Fallback
        output_lines.append("**Go Linter enforces:**")
        output_lines.append("- `userID` not `userId` (var-naming)")
        output_lines.append("- `any` not `interface{}` (use-any)")
        output_lines.append("- No `common/helpers/utils/shared/misc` packages")
        output_lines.append("")
        output_lines.append("→ Run `golangci-lint run` after completing Go tasks")
        output_lines.append("")

    output_lines.append("- Dependencies: always use `@latest` (hook enforces)")
    output_lines.append(
        "- Repository queries: use Filter pattern (`XxxFilter` + `getXxxCondition()`)"
    )

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
