# Skillbox Skills Registry

Specialized workflow layer extending Claude Code with domain expertise.

> **For project scaffolding:** Use Anthropic's `plugin-dev` plugin.
> Skillbox focuses on workflow orchestration, platform engineering, and testing excellence.

---

## Core Workflows (10 skills)

Task tracking, code memory, session persistence, and commit traceability.

| Skill | Description | Triggers |
|-------|-------------|----------|
| [unified-workflow](core/unified-workflow/) | Complete task → code → commit cycle | "start feature", "track task", "workflow" |
| [beads-workflow](core/beads-workflow/) | Cross-session task tracking | "task", "bd", "issue" |
| [serena-navigation](core/serena-navigation/) | Semantic code memory | "find symbol", "serena" |
| [conventional-commit](core/conventional-commit/) | Structured commit messages | "commit", "git message" |
| [context-engineering](core/context-engineering/) | Long-session context management | "context overflow", "token limit" |
| [discovery](core/discovery/) | Self-questioning + Ralph pattern loop | "discover", "discover-loop", "research" |
| [tdd-enforcer](core/tdd-enforcer/) | Red-Green-Refactor workflow | "tdd", "test first" |
| [skill-patterns](core/skill-patterns/) | Do/Verify/Repair, Guardrails | "improve skill", "quality patterns" |
| [secrets-guardian](core/secrets-guardian/) | Pre-commit secrets protection | "secrets", "gitleaks", "credentials" |
| [agent-harness](core/agent-harness/) | Multi-session feature orchestration | "harness", "long feature" |

---

## Go Development (2 skills)

Production Go patterns and API-first development.

| Skill | Description | Triggers |
|-------|-------------|----------|
| [go-development](go/go-development/) | Production Go patterns | "golang", "go project" |
| [openapi-development](go/openapi-development/) | Spec-first API design | "openapi", "swagger", "oapi-codegen" |

---

## TypeScript Development (5 skills)

Modern TypeScript patterns, tooling, and best practices.

| Skill | Description | Triggers |
|-------|-------------|----------|
| [ts-conventions](ts/conventions/) | Code conventions + API patterns (Hono, tRPC, Zod) | `*.ts`, `*.tsx`, "typescript" |
| [ts-project-setup](ts/project-setup/) | Project structure + modern tooling (pnpm, Biome, Vite) | "tsconfig", "monorepo", "biome" |
| [ts-type-patterns](ts/type-patterns/) | Generics, utility types, branded types | "generics", "typescript types" |
| [ts-testing-patterns](ts/testing-patterns/) | Vitest patterns | "vitest", "testing" |
| [ts-database-patterns](ts/database-patterns/) | Drizzle ORM patterns | "drizzle", "database" |

---

## Kubernetes / GitOps (3 skills)

Production Kubernetes, Helm charts, and Flux GitOps patterns.

| Skill | Description | Triggers |
|-------|-------------|----------|
| [helm-chart-developer](k8s/helm-chart-developer/) | Helm charts with Flux + ESO | "helm", "chart", "gitops" |
| [flux-gitops-scaffold](k8s/flux-gitops-scaffold/) | GitOps project scaffolding | "flux init", "gitops scaffold" |
| [flux-gitops-refactor](k8s/flux-gitops-refactor/) | GitOps repository refactoring | "flux refactor", "gitops cleanup" |

---

## Infrastructure (1 skill)

Server automation and hardening.

| Skill | Description | Triggers |
|-------|-------------|----------|
| [ansible-automation](infra/ansible-automation/) | Server hardening automation | "ansible", "server setup" |

---

## Quick Lookup

### By Task

| Task | Skill |
|------|-------|
| Start new feature | unified-workflow |
| Track work across sessions | beads-workflow |
| Navigate code semantically | serena-navigation |
| Write commit message | conventional-commit |
| Create Helm chart | helm-chart-developer |
| TDD workflow | tdd-enforcer |
| Problem-solving | discovery |
| Manage context | context-engineering |

### By Command

| Command | Skill/Action |
|---------|--------------|
| `/init-workflow` | Initialize beads + serena + CLAUDE.md |
| `/checkpoint` | Save session to serena memory |
| `/commit` | conventional-commit |
| `/discover` | discovery |
| `/discover-loop` | discovery (Ralph pattern) |
| `/cancel-discover-loop` | discovery |
| `/secrets-check` | secrets-guardian |
| `/helm-scaffold` | helm-chart-developer |
| `/flux-init` | flux-gitops-scaffold |
| `/harness-init` | agent-harness |

---

## Workflow Integration

```
                    ┌─────────────────────────────────┐
                    │      unified-workflow           │
                    │   (task → code → commit)        │
                    └─────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ beads-workflow│◄──►│serena-navigation│◄──►│conventional-  │
│ (tasks)       │    │ (code memory) │    │ commit        │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
           context-engineering    agent-harness
           (long sessions)       (multi-session)
```

---

## Adding New Skills

Use Anthropic's `plugin-dev` for skill creation mechanics.
For quality patterns (Do/Verify/Repair, Guardrails), see [skill-patterns](core/skill-patterns/).

---

**Total: 21 skills** across 5 domains
