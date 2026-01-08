#!/usr/bin/env bash
#
# setup-loop.sh - Initialize code audit loop state
# Based on Ralph pattern (like discovery-loop)
#

set -euo pipefail

# Default values
MAX_PASSES=5
TARGET_PATH="."
COMPLETION_SIGNAL="AUDIT_COMPLETE"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --max-iteration|--max-passes)
            MAX_PASSES="$2"
            shift 2
            ;;
        --completion-signal)
            COMPLETION_SIGNAL="$2"
            shift 2
            ;;
        *)
            # Non-option argument is target path
            TARGET_PATH="$1"
            shift
            ;;
    esac
done

# Validate max_passes is numeric
if ! [[ "$MAX_PASSES" =~ ^[0-9]+$ ]]; then
    echo "Error: --max-iteration must be a positive integer, got: $MAX_PASSES"
    exit 1
fi

# Validate target path exists
if [[ ! -d "$TARGET_PATH" ]]; then
    echo "Error: Target path does not exist: $TARGET_PATH"
    exit 1
fi

# Detect project language
detect_language() {
    local path="$1"
    if [[ -f "$path/go.mod" ]]; then
        echo "go"
    elif [[ -f "$path/package.json" ]]; then
        if [[ -f "$path/tsconfig.json" ]]; then
            echo "typescript"
        else
            echo "javascript"
        fi
    elif [[ -f "$path/pyproject.toml" ]] || [[ -f "$path/requirements.txt" ]]; then
        echo "python"
    elif [[ -f "$path/Cargo.toml" ]]; then
        echo "rust"
    elif [[ -f "$path/pom.xml" ]] || [[ -f "$path/build.gradle" ]]; then
        echo "java"
    else
        echo "unknown"
    fi
}

# Create .claude directory if it doesn't exist
mkdir -p .claude

# Detect language
DETECTED_LANG=$(detect_language "$TARGET_PATH")

# Get current timestamp
STARTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Get project name from directory
PROJECT_NAME=$(basename "$(cd "$TARGET_PATH" && pwd)")

# Create state file
STATE_FILE=".claude/audit-loop.local.md"

cat > "$STATE_FILE" << EOF
---
active: true
pass: 1
max_passes: $MAX_PASSES
target_path: "$TARGET_PATH"
detected_lang: "$DETECTED_LANG"
completion_signal: "<audited>${COMPLETION_SIGNAL}</audited>"
started_at: "$STARTED_AT"
---

# Code Audit: $PROJECT_NAME

## Target
$TARGET_PATH ($DETECTED_LANG)

## Audit Strategy

**Pass 1: Architecture Scan**
- Project structure, module boundaries
- Entry points, dependency graph
- Identify critical areas

**Pass 2: Security Audit**
- Input validation, injection risks
- Auth/authz patterns
- Sensitive data handling

**Pass 3: Code Quality**
- CLAUDE.md compliance
- Language-specific best practices
- Anti-patterns, code smells

**Pass 4: Performance Analysis**
- N+1 queries, resource leaks
- Concurrency issues
- Scalability concerns

**Pass 5: Synthesis**
- Prioritize by severity
- Executive summary
- Actionable recommendations

## Instructions

You are in a code audit loop. Each pass:

1. **Review** previous findings in .claude/audit-findings.md
2. **Focus** on this pass's specific category
3. **Analyze** the codebase for issues in that category
4. **Document** findings with severity and location
5. **Identify** areas needing attention in next pass

When audit is complete (all critical areas analyzed, synthesis done), output:

\`\`\`
<audited>${COMPLETION_SIGNAL}</audited>
\`\`\`

## Current Pass

Pass 1 of $MAX_PASSES: **Architecture Scan**

Focus on:
- Project structure and organization
- Entry points (main files, handlers)
- Module boundaries and dependencies
- Identify critical areas for security/performance review
EOF

# Create findings file
FINDINGS_FILE=".claude/audit-findings.md"
if [[ ! -f "$FINDINGS_FILE" ]]; then
    cat > "$FINDINGS_FILE" << EOF
# Code Audit: $PROJECT_NAME

**Target:** $TARGET_PATH
**Language:** $DETECTED_LANG
**Started:** $STARTED_AT

## Executive Summary

[To be filled after final pass]

## Scratchpad

<!--
Thinking space between passes. Record:
- Suspicious patterns to investigate
- Cross-module security concerns
- Performance red flags
- Questions for deeper analysis
-->

---

EOF
fi

# Output confirmation
echo "Code audit loop initialized!"
echo ""
echo "Target: $TARGET_PATH"
echo "Language: $DETECTED_LANG"
echo "Max passes: $MAX_PASSES"
echo "Completion signal: <audited>${COMPLETION_SIGNAL}</audited>"
echo ""
echo "State file: $STATE_FILE"
echo "Findings file: $FINDINGS_FILE"
echo ""
echo "The audit will continue until you output the completion signal or reach max passes."
echo ""
echo "---"
echo ""
echo "## Pass 1: Architecture Scan"
echo ""
echo "Analyze project structure, entry points, and identify critical areas for $PROJECT_NAME"
