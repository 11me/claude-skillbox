"""Desktop notification utility using notify-send."""

import re
import shutil
import subprocess
from pathlib import Path


def _is_enabled() -> bool:
    """Check if notifications are enabled in .claude/skillbox.local.md."""
    config_path = Path.cwd() / ".claude" / "skillbox.local.md"
    if not config_path.exists():
        return True  # enabled by default

    try:
        content = config_path.read_text()
        # Parse YAML frontmatter
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            # Look for notifications: false
            if re.search(r"^\s*notifications:\s*false\s*$", frontmatter, re.MULTILINE):
                return False
        return True
    except OSError:
        return True


def notify(title: str, message: str, urgency: str = "normal") -> bool:
    """Send desktop notification via notify-send.

    Args:
        title: Notification title
        message: Notification body
        urgency: low, normal, critical

    Returns:
        True if notification sent successfully
    """
    if not _is_enabled():
        return False

    if not shutil.which("notify-send"):
        return False

    try:
        subprocess.run(
            [
                "notify-send",
                "--urgency",
                urgency,
                "--app-name",
                "Claude Code",
                title,
                message,
            ],
            timeout=5,
            check=False,
        )
        return True
    except (subprocess.TimeoutExpired, OSError):
        return False
