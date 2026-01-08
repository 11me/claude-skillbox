#!/usr/bin/env bash
#
# audit-stop.sh - Stop hook for code audit loop
# Based on Ralph pattern (same as discovery-stop.sh)
#
# This hook intercepts session exit and continues the audit loop
# until the completion signal is found or max passes reached.
#

set -euo pipefail

STATE_FILE=".claude/audit-loop.local.md"
FINDINGS_FILE=".claude/audit-findings.md"

# If no state file, allow normal exit
if [[ ! -f "$STATE_FILE" ]]; then
    exit 0
fi

# Read state from frontmatter
get_frontmatter_value() {
    local key="$1"
    grep "^${key}:" "$STATE_FILE" | head -1 | sed "s/^${key}: *//" | tr -d '"'
}

ACTIVE=$(get_frontmatter_value "active")
PASS=$(get_frontmatter_value "pass")
MAX_PASSES=$(get_frontmatter_value "max_passes")
COMPLETION_SIGNAL=$(get_frontmatter_value "completion_signal")

# If not active, allow normal exit
if [[ "$ACTIVE" != "true" ]]; then
    exit 0
fi

# Validate pass is numeric
if ! [[ "$PASS" =~ ^[0-9]+$ ]]; then
    echo "Warning: Invalid pass value in state file: $PASS" >&2
    rm -f "$STATE_FILE"
    exit 0
fi

# Validate max_passes is numeric
if ! [[ "$MAX_PASSES" =~ ^[0-9]+$ ]]; then
    MAX_PASSES=5
fi

# Read transcript from stdin (JSON with transcript_path)
INPUT=$(cat)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || true)

# Check for completion signal in last assistant message
if [[ -n "$TRANSCRIPT_PATH" ]] && [[ -f "$TRANSCRIPT_PATH" ]]; then
    LAST_ASSISTANT=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1 || true)

    if [[ -n "$LAST_ASSISTANT" ]]; then
        ASSISTANT_TEXT=$(echo "$LAST_ASSISTANT" | jq -r '.content[]? | select(.type == "text") | .text' 2>/dev/null | tr '\n' ' ' || true)

        if echo "$ASSISTANT_TEXT" | grep -q '<audited>.*</audited>'; then
            FOUND_SIGNAL=$(echo "$ASSISTANT_TEXT" | perl -0777 -pe 's/.*?<audited>(.*?)<\/audited>.*/$1/s' 2>/dev/null || true)
            EXPECTED_SIGNAL=$(echo "$COMPLETION_SIGNAL" | sed 's/<audited>//' | sed 's/<\/audited>//')

            if [[ "$FOUND_SIGNAL" = "$EXPECTED_SIGNAL" ]]; then
                rm -f "$STATE_FILE"
                echo ""
                echo "Code audit complete after $PASS pass(es)."
                echo "Findings saved to: $FINDINGS_FILE"
                exit 0
            fi
        fi
    fi
fi

# Check pass limit
if [[ "$MAX_PASSES" -gt 0 ]] && [[ "$PASS" -ge "$MAX_PASSES" ]]; then
    rm -f "$STATE_FILE"
    echo ""
    echo "Code audit reached maximum passes ($MAX_PASSES)."
    echo "Findings saved to: $FINDINGS_FILE"
    echo ""
    echo "Consider:"
    echo "  - Reviewing findings and synthesizing recommendations"
    echo "  - Restarting with more passes if needed"
    exit 0
fi

# Continue loop: increment pass
NEXT_PASS=$((PASS + 1))

# Update pass in state file
TEMP_FILE="${STATE_FILE}.tmp.$$"
sed "s/^pass: .*/pass: $NEXT_PASS/" "$STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$STATE_FILE"

# Update "Current Pass" section
if grep -q "Pass [0-9]* of" "$STATE_FILE"; then
    TEMP_FILE="${STATE_FILE}.tmp.$$"
    sed "s/Pass [0-9]* of/Pass $NEXT_PASS of/" "$STATE_FILE" > "$TEMP_FILE"
    mv "$TEMP_FILE" "$STATE_FILE"
fi

# Determine pass focus
get_pass_focus() {
    local pass="$1"
    local max="$2"

    if [[ "$pass" -eq "$max" ]]; then
        echo "Synthesis Report"
    else
        case "$pass" in
            1) echo "Architecture Scan" ;;
            2) echo "Security Audit" ;;
            3) echo "Code Quality" ;;
            4) echo "Performance Analysis" ;;
            5) echo "Synthesis Report" ;;
            *) echo "Deep Analysis (Pass $pass)" ;;
        esac
    fi
}

PASS_FOCUS=$(get_pass_focus "$NEXT_PASS" "$MAX_PASSES")

# Build system message with context
SYSTEM_MESSAGE="Code Audit - Pass $NEXT_PASS of $MAX_PASSES: $PASS_FOCUS

Review your previous findings in .claude/audit-findings.md and continue the audit.

Focus areas for $PASS_FOCUS:
$(case "$NEXT_PASS" in
    2) echo "- Input validation, injection risks
- Authentication/authorization patterns
- Sensitive data handling, secrets exposure" ;;
    3) echo "- CLAUDE.md compliance (if exists)
- Language-specific best practices
- Anti-patterns, code smells" ;;
    4) echo "- N+1 queries, resource leaks
- Concurrency issues, race conditions
- Scalability concerns" ;;
    *) echo "- Prioritize findings by severity
- Write executive summary
- Provide actionable recommendations
- Output completion signal when done" ;;
esac)

When audit is complete, output: $COMPLETION_SIGNAL"

# Escape newlines for valid JSON (reason field is what Claude sees)
ESCAPED_REASON=$(printf '%s' "$SYSTEM_MESSAGE" | sed ':a;N;$!ba;s/\n/\\n/g' | sed 's/"/\\"/g')

# Output JSON to continue loop
# NOTE: Only "decision" and "reason" are supported for Stop hooks
# "systemMessage" is NOT supported and will break the hook!
cat << EOF
{
  "decision": "block",
  "reason": "$ESCAPED_REASON"
}
EOF

exit 0
