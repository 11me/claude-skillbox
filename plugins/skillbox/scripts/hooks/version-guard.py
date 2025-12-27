#!/usr/bin/env python3
"""PreToolUse hook: Block HelmRelease writes with empty version field.

Enforces Context7 usage for version resolution in Flux GitOps projects.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "lib"))
from response import ask


def main() -> None:
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input", {})

    # Only check Write/Edit to yaml files
    file_path = tool_input.get("file_path", "")
    if not file_path.endswith((".yaml", ".yml")):
        return  # Allow silently

    content = tool_input.get("content", "") or tool_input.get("new_string", "")
    if not content:
        return  # Allow silently

    # Check for HelmRelease with empty version
    if "kind: HelmRelease" in content:
        # Pattern: version: "" or version: '' (empty string with comment)
        if re.search(r'version:\s*["\']["\']', content):
            return ask(
                reason=(
                    "HelmRelease has empty version. Use Context7 first:\n\n"
                    '1. resolve-library-id: libraryName="{chart-name}"\n'
                    '2. get-library-docs: topic="helm installation"\n'
                    "3. Set version from documentation\n\n"
                    "This ensures you're using the current stable version."
                ),
                event="PreToolUse",
            )

    # Allow all other cases silently


if __name__ == "__main__":
    main()
