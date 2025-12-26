---
description: Initialize project for production workflow (beads + serena + CLAUDE.md)
---

# /init-project

Initialize the current project with production workflow tools.

## What This Does

1. **Beads** — Task tracking with `bd` CLI
2. **Serena** — Code memory and semantic navigation
3. **CLAUDE.md** — AI quick reference
4. **Pre-commit** — Code quality hooks
5. **Tests** — TDD compliance directory

## Usage

Run the initialization script:

```bash
# Full setup (recommended)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/init-project.py

# With custom name
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/init-project.py --name "My Project"

# Minimal (beads + CLAUDE.md only)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/init-project.py --minimal

# Skip pre-commit
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/init-project.py --skip-precommit
```

## After Initialization

1. Review `CLAUDE.md` and customize for your project
2. Update `.serena/memories/overview.md` with architecture details
3. Create first task: `bd create --title "..." -t task`
4. Commit: `git add -A && git commit -m "chore: init production workflow"`

## Checklist

```
[ ] .beads/ exists (bd init)
[ ] .serena/project.yml exists
[ ] .serena/memories/overview.md written
[ ] CLAUDE.md with quick start
[ ] .pre-commit-config.yaml configured
[ ] pre-commit install executed
[ ] First commit made
```
