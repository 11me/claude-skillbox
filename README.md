# claude-skillbox

> Specialized workflow plugins for Claude Code — modular, focused, production-ready.

[![CI](https://github.com/11me/claude-skillbox/actions/workflows/ci.yaml/badge.svg)](https://github.com/11me/claude-skillbox/actions/workflows/ci.yaml)
[![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)](https://github.com/11me/claude-skillbox/releases)
[![Python](https://img.shields.io/badge/python-3.12+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet?style=flat-square&logo=anthropic)](https://docs.anthropic.com/en/docs/claude-code)

## Plugins

Install only what you need:

| Plugin | Description |
|--------|-------------|
| **[workflow](plugins/workflow/)** | Beads task tracking, Serena navigation, commits, discovery |
| **[go-dev](plugins/go-dev/)** | Go development: services, repositories, OpenAPI |
| **[flux](plugins/flux/)** | Flux GitOps: scaffolding, refactoring, multi-environment |
| **[helm](plugins/helm/)** | Helm chart development: ESO, GitOps patterns |
| **[ts-dev](plugins/ts-dev/)** | TypeScript: Vitest, Drizzle, conventions |
| **[tdd](plugins/tdd/)** | Test-Driven Development workflow |
| **[ansible](plugins/ansible/)** | Ansible automation, Ubuntu hardening |
| **[harness](plugins/harness/)** | Long-running agent harness |
| **[python-dev](plugins/python-dev/)** | Python test generation (pytest) |
| **[rust-dev](plugins/rust-dev/)** | Rust test generation |

## Quick Start

```bash
# Add the marketplace
/plugin marketplace add 11me/claude-skillbox

# Install specific plugins
/plugin install workflow@11me-skillbox
/plugin install go-dev@11me-skillbox
/plugin install flux@11me-skillbox
```

Or test locally:

```bash
claude --plugin-dir ./plugins/workflow
claude --plugin-dir ./plugins/go-dev
```

## Plugin Details

### workflow

Personal workflow tools for cross-session development.

**Skills:**
- `beads` — Task tracking with beads CLI
- `serena` — Semantic code navigation
- `conventional-commit` — Structured commit messages
- `unified-workflow` — Complete task-to-commit workflow
- `context-engineering` — Long-session context management
- `skill-patterns` — Quality patterns (Do/Verify/Repair)
- `secrets-guardian` — Secrets protection (gitleaks)
- `discovery` — Self-questioning + Ralph pattern

**Commands:** `/commit`, `/checkpoint`, `/discover`, `/discover-loop`, `/init`, `/notify`, `/secrets`, `/scaffold`

**Agents:** task-tracker, session-checkpoint, code-navigator, feature-supervisor, verification-worker, discovery-explorer

---

### go-dev

Go development toolkit with production patterns.

**Skills:**
- `go-development` — Services, repositories, handlers, testing
- `openapi-development` — Spec-first API with oapi-codegen

**Commands:** `/add-service`, `/add-repository`, `/add-model`, `/review`, `/openapi-init`, `/openapi-add-path`, `/openapi-generate`

**Agents:** project-init, code-reviewer

---

### flux

Flux GitOps toolkit.

**Skills:**
- `scaffold` — Flux GitOps project scaffolding
- `refactor` — Restructure existing GitOps repos

**Commands:** `/init`, `/add-app`, `/add-infra`, `/refactor`

---

### helm

Helm chart development toolkit.

**Skills:**
- `helm-dev` — Production Helm charts, External Secrets, GitOps patterns

**Commands:** `/scaffold`, `/validate`, `/checkpoint`

---

### ts-dev

TypeScript development patterns.

**Skills:**
- `ts-conventions` — Code conventions
- `ts-database-patterns` — Drizzle ORM
- `ts-project-setup` — pnpm, Biome, Vite
- `ts-testing-patterns` — Vitest
- `ts-type-patterns` — Generics, utility types

**Agents:** project-init

---

### tdd

Test-Driven Development workflow.

**Skills:**
- `tdd-enforcer` — Red-Green-Refactor discipline

**Commands:** `/tdd`

---

### ansible

Ansible automation toolkit.

**Skills:**
- `ansible` — Ansible practices, Ubuntu hardening, SSH security

**Commands:** `/scaffold`, `/validate`

---

### harness

Long-running agent patterns for multi-session features.

**Skills:**
- `agent-harness` — Feature tracking, verification enforcement

**Commands:** `/init`, `/supervisor`, `/status`, `/verify`, `/update`, `/auto`

---

### python-dev

Python development.

**Skills:**
- `testing-pytest` — pytest patterns, fixtures, mocking

**Commands:** `/py-test`

---

### rust-dev

Rust development.

**Skills:**
- `testing-patterns` — Rust testing, rstest, mockall

**Commands:** `/rust-test`

## Architecture

```
plugins/
├── workflow/                # Personal workflow tools
│   ├── .claude-plugin/
│   ├── commands/
│   ├── agents/
│   ├── skills/
│   ├── hooks/
│   └── scripts/
├── go-dev/                  # Go development
│   ├── .claude-plugin/
│   ├── commands/
│   ├── agents/
│   ├── skills/
│   └── templates/
├── flux/                    # Flux GitOps
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/
├── helm/                    # Helm charts
│   ├── .claude-plugin/
│   ├── commands/
│   ├── skills/
│   └── scripts/
├── ts-dev/                  # TypeScript
│   ├── .claude-plugin/
│   ├── agents/
│   ├── skills/
│   └── templates/
├── tdd/                     # TDD
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/
├── ansible/                 # Ansible automation
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/
├── harness/                 # Long-running agents
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/
├── python-dev/              # Python
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/
└── rust-dev/                # Rust
    ├── .claude-plugin/
    ├── commands/
    └── skills/
```

## Development

```bash
# Clone
git clone https://github.com/11me/claude-skillbox.git
cd claude-skillbox

# Install pre-commit
uv tool install pre-commit
pre-commit install

# Test a plugin locally
claude --plugin-dir ./plugins/workflow
```

## License

[MIT](LICENSE)
