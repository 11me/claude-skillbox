---
name: production-flow
description: Use when the user asks about "production flow", "project setup", "new project", "init project", "add feature", "development workflow", "how to start", "best practices", or needs guidance on following the unified production flow for reliable code delivery.
version: 1.0.0
---

# Production Flow — Unified Development Workflow

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION FLOW STAGES                        │
├─────────────────────────────────────────────────────────────────┤
│  1. INIT      → pre-commit, beads, serena, CLAUDE.md            │
│  2. PLAN      → EnterPlanMode or feature planning               │
│  3. DEVELOP   → TDD (Red→Green→Refactor), convention skills     │
│  4. VERIFY    → pre-commit, type check, SAST, tests             │
│  5. REVIEW    → code review, address feedback                   │
│  6. SHIP      → /commit, PR, merge to main                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. New Project Setup

### Step 1.1: Initialize Project Structure

```bash
# Create project
mkdir my-project && cd my-project
git init

# Language-specific init (choose one)
go mod init github.com/user/project  # Go
uv init                               # Python
cargo init                            # Rust
pnpm init                             # TypeScript
```

### Step 1.2: Setup Quality Gates

```bash
# Create pre-commit config
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
EOF

# Install hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

### Step 1.3: Create CLAUDE.md

```bash
cat > CLAUDE.md << 'EOF'
# Project: my-project

## Overview
[Brief description]

## Tech Stack
- Language: [Go/TypeScript/Python/Rust]
- Framework: [if applicable]
- Database: [if applicable]

## Project Structure
```
src/           # Source code
tests/         # Test files
docs/          # Documentation
```

## Development Commands
```bash
# Run tests
[test command]

# Run linter
[lint command]

# Build
[build command]
```

## Conventions
- [Key convention 1]
- [Key convention 2]
EOF
```

### Step 1.4: Initialize Beads Task Tracking

```bash
# Create beads directory
bd init

# Add initial task
bd create --title "Initial project setup" -t task -p 1
bd update <id> --status in_progress
```

### Step 1.5: Initialize Serena (if using)

```bash
# Serena will auto-detect on first use
# Memories stored in .serena/memories/
```

### Step 1.6: First Commit

```bash
git add -A
git commit -m "chore: initial project setup

- Add pre-commit hooks
- Add CLAUDE.md
- Initialize beads task tracking"
```

---

## 2. Existing Project Setup

### Step 2.1: Clone and Assess

```bash
git clone <repo>
cd <repo>

# Check what exists
ls -la .pre-commit-config.yaml CLAUDE.md .beads/ 2>/dev/null
```

### Step 2.2: Add Missing Components

```bash
# If no CLAUDE.md - create one (see above)

# If no pre-commit - add it
pre-commit install

# If no beads - initialize
bd init
```

### Step 2.3: Read Project Context

```bash
# Let Claude read the project
cat CLAUDE.md

# Or use Serena for deep understanding
# (Serena auto-activates on project open)
```

---

## 3. Feature Development Flow

### Step 3.1: Create Task

```bash
# Add to beads
bd create --title "Implement user authentication" -t feature -p 1
bd update <id> --status in_progress

# Or use /task command
/task add "Implement user authentication"
```

### Step 3.2: Plan the Feature

```
Option A: Use EnterPlanMode
EnterPlanMode → Research → Create plan → Get approval

Option B: Quick planning
Discuss with Claude → Agree on approach → Start coding
```

### Step 3.3: Develop with TDD

```
RED PHASE:
1. Write failing test first
2. Run tests - confirm failure
3. Commit: "test: add failing test for X"

GREEN PHASE:
1. Write minimal code to pass
2. Run tests - confirm passing
3. Commit: "feat: implement X"

REFACTOR PHASE:
1. Improve code quality
2. Run tests - confirm still passing
3. Commit: "refactor: clean up X"
```

### Step 3.4: Checkpoint Progress

```bash
# After significant progress
/checkpoint

# Or manually add comment
bd comments add <id> "Completed auth service, starting endpoints"
```

### Step 3.5: Review Before Commit

```bash
# Run code review
/go-review  # for Go projects

# Check linting
pre-commit run --all-files
```

### Step 3.6: Commit and Push

```bash
# Use commit command
/commit

# Or manual with conventional format
git add -A
git commit -m "feat: implement user authentication"
git push
```

---

## 4. Code Review Process

### Reviewer Workflow

```bash
# Review changes
git diff main...HEAD

# Check tests pass
go test ./... -v
```

### Author Response

```bash
# Address each comment
# Re-run review after fixes

# Update PR
git add -A
git commit -m "fix: address review feedback"
git push
```

---

## 5. Hotfix Flow

```bash
# Create hotfix branch
git checkout -b hotfix/critical-bug

# Fix with TDD
# 1. Write test that exposes bug
# 2. Fix the bug
# 3. Verify test passes

# Commit
git commit -m "fix: resolve critical auth bypass"

# Fast-track review + merge
git push
# Create PR → merge to main
```

---

## 6. Release Flow

```bash
# Ensure main is clean
git checkout main
git pull

# All tests pass
pre-commit run --all-files

# Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push --tags

# Deploy (project-specific)
```

---

## Enforcement Mechanisms

### Automatic (Hooks)

| Hook | Stage | What it enforces |
|------|-------|------------------|
| Ruff/Biome/golangci-lint | pre-commit | Code style |
| mypy/tsc | pre-commit | Type safety |
| Bandit/gosec | pre-commit | Security |
| Gitleaks | pre-commit | No secrets |
| Conventional commits | commit-msg | Commit format |
| Tests | pre-push | All tests pass |

### Manual Checkpoints

| When | What to check |
|------|---------------|
| Before feature start | Task created in beads? |
| Before coding | Plan approved? |
| Before commit | Tests passing? Lint clean? |
| Before merge | CI green? PR approved? |

---

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `/init-workflow` | Init beads + serena + CLAUDE.md |
| `/checkpoint` | Save session progress |
| `/commit` | Create conventional commit |
| `/go-review` | Review Go project |
| `bd create` | Create beads task |
| `bd close <id>` | Complete task |

---

## Troubleshooting

### Pre-commit failing?

```bash
# See what's failing
pre-commit run --all-files

# Skip temporarily (emergencies only!)
git commit --no-verify -m "..."
```

### Tests failing?

```bash
# Run specific test
go test ./... -v -run TestName

# With verbose output
go test ./... -v
```

### Context overflow?

```bash
# Create checkpoint
/checkpoint

# Then ask Claude to summarize and continue
```

### Lost progress?

```bash
# Check Serena memories
ls .serena/memories/checkpoint-*

# Read latest
cat .serena/memories/checkpoint-latest.md
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| Skip tests | Bugs in prod | Always TDD |
| No task tracking | Lost context | Use beads |
| Giant commits | Hard to review | Small, focused |
| Skip review | Miss issues | Always review |
| Force push to main | Lose history | Never |
| Secrets in code | Security breach | Use .env + gitleaks |
| No CLAUDE.md | Context loss | Always create |

---

## Related Skills

- **context-engineering** — Managing AI context
- **reliable-execution** — Session persistence
- **beads-workflow** — Task tracking
- **tdd-enforcer** — TDD patterns
- **conventional-commit** — Commit messages
