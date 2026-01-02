"""Tmux state management for consistent pane/window targeting."""

import json
import os
import subprocess
from pathlib import Path

# State file location - use XDG or fallback to /tmp
_STATE_DIR = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "claude-skillbox"
_STATE_FILE = _STATE_DIR / "tmux-state.json"


def _run_tmux(args: list[str], timeout: int = 1) -> str | None:
    """Run tmux command and return stdout or None on failure."""
    if "TMUX" not in os.environ:
        return None
    try:
        result = subprocess.run(
            ["tmux", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


def get_current_pane_id() -> str | None:
    """Get current pane ID from tmux (e.g., %5)."""
    return _run_tmux(["display-message", "-p", "#{pane_id}"])


def get_current_window_id() -> str | None:
    """Get current window ID from tmux (e.g., @2)."""
    return _run_tmux(["display-message", "-p", "#{window_id}"])


def get_session_name() -> str | None:
    """Get current session name."""
    return _run_tmux(["display-message", "-p", "#{session_name}"])


def save_state() -> bool:
    """Save current tmux pane/window IDs to state file.

    Should be called on SessionStart to capture the correct context.
    Returns True if state was saved successfully.
    """
    if "TMUX" not in os.environ:
        return False

    pane_id = get_current_pane_id()
    window_id = get_current_window_id()
    session_name = get_session_name()

    if not all([pane_id, window_id, session_name]):
        return False

    state = {
        "pane_id": pane_id,
        "window_id": window_id,
        "session_name": session_name,
        "pid": os.getpid(),
    }

    try:
        _STATE_DIR.mkdir(parents=True, exist_ok=True)
        _STATE_FILE.write_text(json.dumps(state))
        return True
    except OSError:
        return False


def load_state() -> dict | None:
    """Load saved tmux state.

    Returns dict with pane_id, window_id, session_name or None if not available.
    """
    try:
        if _STATE_FILE.exists():
            return json.loads(_STATE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        pass
    return None


def get_pane_id() -> str | None:
    """Get pane ID from saved state or current context.

    Prefers saved state (set at SessionStart) for consistency,
    falls back to current pane if state is unavailable.
    """
    state = load_state()
    if state and state.get("pane_id"):
        return state["pane_id"]
    return get_current_pane_id()


def get_window_id() -> str | None:
    """Get window ID from saved state or current context.

    Prefers saved state (set at SessionStart) for consistency,
    falls back to current window if state is unavailable.
    """
    state = load_state()
    if state and state.get("window_id"):
        return state["window_id"]
    return get_current_window_id()


def get_window_name(target: str | None = None) -> str | None:
    """Get window name, optionally for a specific target.

    Args:
        target: tmux target (pane_id, window_id, or None for saved/current)
    """
    if target is None:
        target = get_pane_id()

    if target:
        return _run_tmux(["display-message", "-t", target, "-p", "#{window_name}"])
    return _run_tmux(["display-message", "-p", "#{window_name}"])


def rename_window(new_name: str, target: str | None = None) -> bool:
    """Rename window with explicit target.

    Args:
        new_name: New window name
        target: tmux target (uses saved window_id if None)

    Returns:
        True if rename succeeded
    """
    if "TMUX" not in os.environ:
        return False

    if target is None:
        target = get_window_id()

    args = ["rename-window"]
    if target:
        args.extend(["-t", target])
    args.append(new_name)

    return _run_tmux(args) is not None


def get_context_string() -> str | None:
    """Get tmux context string for notification title.

    Returns string like '[session:0] window-name' or None if not in tmux.
    """
    if "TMUX" not in os.environ:
        return None

    state = load_state()
    if state:
        # Use saved state for consistency
        pane_id = state.get("pane_id")
        if pane_id:
            return _run_tmux(
                [
                    "display-message",
                    "-t",
                    pane_id,
                    "-p",
                    "[#{session_name}:#{window_index}] #{window_name}",
                ]
            )

    # Fallback to current context
    return _run_tmux(["display-message", "-p", "[#{session_name}:#{window_index}] #{window_name}"])


def clear_state() -> None:
    """Clear saved state file."""
    try:
        if _STATE_FILE.exists():
            _STATE_FILE.unlink()
    except OSError:
        pass
