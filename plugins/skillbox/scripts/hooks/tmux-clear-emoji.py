#!/usr/bin/env python3
"""Clear emoji from tmux window name when user submits prompt."""

import json
import os
import subprocess


def main() -> None:
    if "TMUX" not in os.environ:
        print(json.dumps({}))
        return

    try:
        # Get current window name
        result = subprocess.run(
            ["tmux", "display-message", "-p", "#{window_name}"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        if result.returncode == 0:
            current_name = result.stdout.strip()
            # Remove emoji prefix (🔴, ⏳, ✅)
            clean_name = current_name.lstrip("🔴⏳✅ ")
            if clean_name != current_name:
                subprocess.run(
                    ["tmux", "rename-window", clean_name],
                    timeout=1,
                    check=False,
                )
    except (subprocess.TimeoutExpired, OSError):
        pass

    print(json.dumps({}))


if __name__ == "__main__":
    main()
