#!/bin/bash
# Ultra-fast emoji setting - pure bash, no Python overhead
# Used by PreToolUse to set emoji immediately before tool execution
#
# Usage: tmux-set-emoji-fast.sh <emoji>
# Example: tmux-set-emoji-fast.sh ❓

EMOJI="${1:-❓}"

# Exit if not in tmux
[[ -z "$TMUX" ]] && echo '{}' && exit 0

# Get pane-specific state file
PANE_ID="${TMUX_PANE:-default}"
SAFE_PANE_ID="${PANE_ID//%/_}"
STATE_DIR="${XDG_RUNTIME_DIR:-/tmp}/claude-skillbox"
STATE_FILE="$STATE_DIR/tmux-state$SAFE_PANE_ID.json"

# Extract pane_id from JSON using grep/sed (avoids Python)
TARGET="$TMUX_PANE"
if [[ -f "$STATE_FILE" ]]; then
    SAVED_PANE=$(grep -o '"pane_id"[[:space:]]*:[[:space:]]*"[^"]*"' "$STATE_FILE" 2>/dev/null | sed 's/.*"\([^"]*\)"$/\1/')
    [[ -n "$SAVED_PANE" ]] && TARGET="$SAVED_PANE"
fi

# Get current window name
CURRENT_NAME=$(tmux display-message -t "${TARGET:-$TMUX_PANE}" -p '#{window_name}' 2>/dev/null)
[[ -z "$CURRENT_NAME" ]] && echo '{}' && exit 0

# Remove existing emoji prefix
CLEAN_NAME=$(printf '%s' "$CURRENT_NAME" | sed 's/^[🔴⏳✅💤🔐❓][[:space:]]*//')

# Set new emoji
NEW_NAME="$EMOJI $CLEAN_NAME"
tmux rename-window -t "${TARGET:-$TMUX_PANE}" "$NEW_NAME" 2>/dev/null

echo '{}'
