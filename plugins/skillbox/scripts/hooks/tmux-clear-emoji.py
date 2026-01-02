#!/usr/bin/env python3
"""Clear emoji from tmux window name when user submits prompt or uses a tool.

Uses saved tmux state for consistent targeting across panes.
"""

import json
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.notifier import clear_tmux_window_emoji  # noqa: E402


def main() -> None:
    clear_tmux_window_emoji()
    print(json.dumps({}))


if __name__ == "__main__":
    main()
