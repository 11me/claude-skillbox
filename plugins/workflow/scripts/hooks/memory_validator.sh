#!/usr/bin/env bash
# memory_validator.sh - SessionStart hook for memory consistency validation
#
# Validates that .serena/memories references match current codebase state.
# Reports stale references to skills, files, or other memories.
#
# Exit 0 = always (non-blocking, informational only)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="$SCRIPT_DIR/memory_validator.py"

# Check if validator exists
if [[ ! -f "$VALIDATOR" ]]; then
    exit 0
fi

# Run validation (quiet mode - only output if issues found)
python3 "$VALIDATOR" --quiet 2>/dev/null || true

exit 0
