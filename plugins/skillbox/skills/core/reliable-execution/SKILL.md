---
name: reliable-execution
description: Use when the user asks about "reliable execution", "session persistence", "context recovery", "checkpoint patterns", "handoff protocol", "agent reliability", "preventing context loss", or needs guidance on ensuring work survives context resets and session handoffs.
version: 1.0.0
---

# Reliable Execution — Patterns for Persistent Agent Work

## The Problem

Claude Code sessions have limited context. Long tasks risk:
- Context resets mid-implementation
- Lost progress after interruptions
- Incomplete handoffs between sessions
- Forgotten decisions and discoveries

## The Solution: 4-Layer Persistence Stack

```
┌─────────────────────────────────────────────┐
│              Session Layer                   │
│  TodoWrite — visible progress tracking      │
│  (Volatile: lost on context reset)          │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│              Task Layer                      │
│  Beads — high-level task lifecycle          │
│  (Persistent: survives sessions)            │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│            Knowledge Layer                   │
│  Serena Memories — persistent discoveries   │
│  (Persistent: survives everything)          │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│              Code Layer                      │
│  Git commits — permanent artifacts          │
│  (Permanent: version controlled)            │
└─────────────────────────────────────────────┘
```

**Key principle:** Each layer is a fallback for the one above.

---

## Pre-Flight Checklist

Before starting significant work, verify:

### 1. Task Tracking Active?
```bash
# Check beads
bd show 2>/dev/null || echo "No beads task"
```
→ If no task, create one: `bd create --title "Task description"`

### 2. Context Loaded?
- SessionStart hook injected `bd prime`?
- Serena memories available? `list_memories()`

### 3. TodoWrite Initialized?
Create subtasks for the implementation:
```
TodoWrite([
  {content: "Research existing patterns", status: "in_progress"},
  {content: "Implement core logic", status: "pending"},
  {content: "Add tests", status: "pending"}
])
```

### 4. Checkpoint Plan?
Identify when to save progress:
- After each major step
- Before risky operations (refactoring, migrations)
- When context feels full (~80% usage)
- Before ending session

---

## During Execution

### Track Progress Visibly
```
TodoWrite([
  {content: "Implement UserService", status: "completed"},
  {content: "Add unit tests", status: "in_progress"},
  {content: "Update documentation", status: "pending"}
])
```

### Save Discoveries
When you learn something important:
```
write_memory(
  memory_file_name="auth-patterns.md",
  content="# Auth Patterns\n\nDiscovered that..."
)
```

### Commit Incrementally
After completing logical units:
```bash
git add -A && git commit -m "feat: implement UserService"
```

### Create Checkpoints
Before context gets full or before risky changes:
```
/checkpoint
```

---

## Checkpoint Triggers

Create checkpoints when:

| Trigger | Type | What to Include |
|---------|------|-----------------|
| Major step completed | Progress | Completed work, next steps |
| Before refactoring | Pre-risk | Current state, rollback plan |
| Context feeling full | Overflow | Full state, all discoveries |
| Session ending | Handoff | Summary, recovery instructions |
| Complex bug found | Debug | Debug state, hypotheses, evidence |

---

## Session Handoff Protocol

When session is ending or context is resetting:

### Step 1: Sync Beads
```bash
bd sync
bd comments add <id> "Progress: Completed X, remaining Y"
```

### Step 2: Create Handoff Checkpoint

Include in checkpoint:
- **Task Context:** Current beads task, goal, status
- **Completed Work:** What was done
- **Remaining Work:** What's left
- **Current State:** Last file, test status, blockers
- **Key Discoveries:** Important findings
- **Next Steps:** Exactly what to do next
- **Recovery Instructions:** How to resume

### Step 3: Commit Pending Changes
```bash
git add -A && git commit -m "WIP: <current state>"
```

### Step 4: Report Checkpoint Location
Tell user:
```
Session checkpoint saved to `checkpoint-<timestamp>.md`.
To continue: Read this memory and resume from step X.
```

---

## Recovery Flow

When starting a new session:

### Step 1: Check for Checkpoints
```
list_memories()
```
Look for `checkpoint-*.md` files.

### Step 2: Read Most Recent
```
read_memory("checkpoint-<latest>.md")
```

### Step 3: Resume from State
Follow "Next Steps" from checkpoint.

### Step 4: Update Task Status
```bash
bd update <task-id> --status in_progress  # Resume beads task
```

---

## Checkpoint Structure Template

```markdown
# Checkpoint: <task-name>

**Created:** <timestamp>
**Task ID:** <beads-id>
**Status:** in_progress

## Goal
<What we're trying to achieve>

## Completed Work
- [x] Item 1
- [x] Item 2

## Remaining Work
- [ ] Item 3
- [ ] Item 4

## Current State
- **Last file modified:** <path>
- **Test status:** <passing/failing>
- **Blockers:** <none/description>

## Key Discoveries
1. <Important finding 1>
2. <Important finding 2>

## Files Changed
- `src/service.go` — Added UserService
- `tests/service_test.go` — Started tests

## Next Steps
1. <Exact next action>
2. <Following action>

## Recovery Instructions
To resume this work:
1. `bd update <id> --status in_progress`
2. Read `src/service.go` lines 50-100
3. Continue implementing <feature>
```

---

## Anti-Patterns

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| No task tracking | Lost context across sessions | Start with `bd create` |
| Discoveries in conversation only | Lost on reset | Use `write_memory()` |
| No progress visibility | Hard to resume | Use `TodoWrite` |
| Waiting until end to save | Risk of loss | Checkpoint after each step |
| Large uncommitted changes | Risk of loss | Commit incrementally |
| Vague checkpoints | Hard to resume | Include exact next steps |

---

## Example: Full Reliable Flow

```
User: "Implement user authentication"

1. CREATE TASK:
   bd create --title "Implement user authentication" -t feature -p 1
   bd update <id> --status in_progress

2. PLAN WITH TODOWRITE:
   - Research existing auth patterns
   - Implement UserService
   - Add login/logout endpoints
   - Write tests
   - Update documentation

3. RESEARCH (save discoveries):
   - Use serena to explore codebase
   - write_memory("auth-research.md", findings)

4. IMPLEMENT (checkpoint after each):
   - Complete UserService → checkpoint + commit
   - Complete endpoints → checkpoint + commit
   - Complete tests → checkpoint + commit

5. FINISH:
   bd close <id> --reason "Implemented with tests"
   bd sync
   Final checkpoint with summary
```

---

## Tool Integration

### Agents
- `task-tracker` — Manages beads task lifecycle
- `code-navigator` — Explores code with serena, saves discoveries
- `session-checkpoint` — Creates recovery checkpoints

### Commands
- `/checkpoint` — Save session progress
- `/init-workflow` — Initialize beads + serena

### Hooks
- `session_context` — Injects beads context at start
- `skill_suggester` — Suggests relevant skills

---

## Related Skills

- **beads-workflow** — Task tracking details
- **serena-navigation** — Code exploration and memory
- **context-engineering** — Managing context budget
- **production-flow** — Full development workflow
