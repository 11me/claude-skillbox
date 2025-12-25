# Skillbox Skills Registry

Quick lookup for available skills, triggers, and outputs.

## Categories

### Core (Workflow & Git)

| Skill | Description | Triggers | Outputs |
|-------|-------------|----------|---------|
| [conventional-commit](core/conventional-commit/) | Git commits with Conventional Commits spec | "commit", "git message", "коммит" | Commit message |
| [beads-workflow](core/beads-workflow/) | Task tracking with beads CLI | "task", "todo", "bd", "issue" | Task state |
| [skill-creator](core/skill-creator/) | Create new Claude Code skills | "create skill", "scaffold skill" | SKILL.md |
| [serena-navigation](core/serena-navigation/) | Semantic code navigation | "serena", "find symbol", "symbol search" | Code insights, memories |

### Kubernetes (GitOps)

| Skill | Description | Triggers | Outputs |
|-------|-------------|----------|---------|
| [helm-chart-developer](k8s/helm-chart-developer/) | Helm charts with Flux + ESO | "helm", "chart", "gitops", "helmrelease" | Validated charts |

## Quick Lookup

### By Task

| Task | Skill |
|------|-------|
| Write commit message | conventional-commit |
| Track tasks/issues | beads-workflow |
| Navigate codebase semantically | serena-navigation |
| Create Helm chart | helm-chart-developer |
| Create new skill | skill-creator |

### By File Pattern

| Pattern | Skill |
|---------|-------|
| `Chart.yaml`, `values.yaml` | helm-chart-developer |
| `.beads/` | beads-workflow |
| `.serena/` | serena-navigation |
| `SKILL.md` | skill-creator |
| `helmrelease*.yaml` | helm-chart-developer |

### By Command

| Command | Skill/Action |
|---------|--------------|
| `/commit` | conventional-commit |
| `/skill-scaffold` | skill-creator |
| `/helm-scaffold` | helm-chart-developer |
| `/helm-validate` | helm-chart-developer |

## Skill Interactions

```
beads-workflow ←→ conventional-commit
     │              (task refs in commits)
     ↓
serena-navigation
     │ (memories persist discoveries)
     ↓
helm-chart-developer
     (validation before complete)
```

## Adding New Skills

See [skill-creator](core/skill-creator/) for templates and best practices.
