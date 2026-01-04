#!/usr/bin/env python3
"""SessionStart hook: detect first session and suggest bootstrap.

If this is the first Claude session for a project (no harness initialized),
suggests running /harness-init to set up feature tracking.

This hook runs early in SessionStart to provide context before work begins.
"""

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.bootstrap import (
    detect_first_session,
    get_project_startup_commands,
    increment_session,
    is_harness_initialized,
)
from lib.features import load_features
from lib.response import session_output


def main() -> None:
    """Handle SessionStart event for harness."""
    cwd = Path.cwd()
    output_lines: list[str] = []

    # Case 1: First session (no harness)
    if detect_first_session(cwd):
        startup_cmds = get_project_startup_commands(cwd)

        output_lines = [
            "## First Session Detected",
            "",
            "This appears to be the first Claude session for this project.",
            "",
        ]

        if startup_cmds:
            output_lines.append("**Suggested bootstrap:**")
            output_lines.append("```bash")
            output_lines.extend(startup_cmds)
            output_lines.append("```")
            output_lines.append("")

        output_lines.extend(
            [
                "**Initialize harness:**",
                "Run `/harness-init` to:",
                "1. Execute startup commands",
                "2. Create `features.json` for tracking",
                "3. Record bootstrap state for future sessions",
                "",
                "Or skip harness with `/init-workflow` for basic setup only.",
            ]
        )

        session_output("\n".join(output_lines))
        return

    # Case 2: Harness initialized - increment session and show status
    if is_harness_initialized(cwd):
        session_num = increment_session(cwd)
        features = load_features(cwd)

        if features:
            summary = features.get_summary()
            verified = summary.get("verified", 0)
            total = len(features.features)

            output_lines.append(f"**Harness:** Session #{session_num}")
            output_lines.append(f"**Features:** {verified}/{total} verified")

            # Show next feature to work on
            next_feature = features.get_next_feature()
            if next_feature:
                output_lines.append(f"**Next:** {next_feature.id} ({next_feature.status.value})")

            # Show unverified implemented features (need verification)
            unverified_impl = features.get_implemented_unverified()
            if unverified_impl:
                output_lines.append("")
                output_lines.append(f"**Pending verification:** {len(unverified_impl)} feature(s)")
                for f in unverified_impl[:3]:
                    output_lines.append(f"  - {f.id}")
                if len(unverified_impl) > 3:
                    output_lines.append(f"  ... and {len(unverified_impl) - 3} more")

            output_lines.append("")
            session_output("\n".join(output_lines))


if __name__ == "__main__":
    main()
