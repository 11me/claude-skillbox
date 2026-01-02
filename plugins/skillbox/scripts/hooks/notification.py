#!/usr/bin/env python3
"""Notification hook: send desktop notification when Claude needs attention."""

import json
import logging
import os
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.notifier import notify  # noqa: E402

# Configure logging to stderr
logging.basicConfig(
    level=logging.DEBUG if os.environ.get("SKILLBOX_DEBUG") else logging.WARNING,
    format="[notification] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Handle Notification event."""
    try:
        data = json.load(sys.stdin)
        notification_type = data.get("notification_type", "")
        message = data.get("message", "Claude needs attention")

        title_map = {
            "permission_prompt": "Permission Required",
            "idle_prompt": "Claude Waiting",
            "auth_success": "Auth Success",
            "elicitation_dialog": "Input Required",
        }

        title = title_map.get(notification_type, "Claude Notification")
        success = notify(title, message, urgency="normal")
        logger.debug(
            "Notification %s: type=%s, title=%s",
            "sent" if success else "skipped",
            notification_type,
            title,
        )

    except json.JSONDecodeError as e:
        logger.warning("Failed to parse notification data: %s", e)
    except KeyError as e:
        logger.warning("Missing required field in notification data: %s", e)
    except Exception as e:
        logger.error("Unexpected error in notification hook: %s", e)

    # Always allow notification to proceed
    print(json.dumps({}))


if __name__ == "__main__":
    main()
