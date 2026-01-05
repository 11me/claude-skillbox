---
name: discovery
description: Use when the user asks about "discover", "explore problem", "find insights", "analyze problem", "research", "investigate", "deep dive", or needs guidance on systematic self-questioning for novel problem-solving.
allowed-tools: Read, Grep, Glob
version: 1.0.0
---

# Self-Questioning Discovery System

AI-powered discovery through systematic self-questioning. Generates novel insights by asking the right questions before answering.

## Concept

Inspired by:
- **Self-Prompted Chain-of-Thought (SP-CoT)**: LLMs generating their own reasoning chains
- **AI Scientist (Sakana AI)**: Autonomous hypothesis generation and testing
- **Socratic Method**: Discovery through questioning assumptions

## Commands

### `/discover <problem> [--deep]`

Quick self-questioning for problem-solving.

```bash
# Quick mode (default): 3-5 focused questions
/discover "How to optimize this API endpoint?"

# Deep mode: full 4-phase exploration
/discover "Design a scalable notification system" --deep
```

**Output:**
1. Self-generated questions about the problem
2. Cross-domain analogies (Tech + Business/UX patterns)
3. Novel insights and recommendations

---

## Quick Mode (default)

### Phase 1: Generate Self-Questions

Ask yourself these categories:

**Assumption Check:**
- What am I assuming about this problem?
- Which constraints are real vs perceived?
- What would happen if I challenged the obvious solution?

**Cross-Domain (Tech):**
- What existing pattern in [relevant framework] solves similar problems?
- How would this scale to 10x the current load?
- What's the simplest solution that could work?

**Cross-Domain (Business/UX):**
- What would frustrate a user about the obvious approach?
- How do successful products handle this?
- What's the hidden cost of complexity here?

### Phase 2: Answer Questions

For each question, provide a brief insight. Look for:
- Unexpected connections
- Hidden assumptions that could be challenged
- Analogies from other domains

### Phase 3: Synthesize

Combine findings into:
1. **Key Insight**: The most surprising/valuable discovery
2. **Recommendation**: Concrete next step
3. **Alternative Frame**: Different perspective

---

## Deep Mode

Triggered by `--deep` flag or keywords: "architecture", "design", "scale", "system", "pattern"

### 4 Phases:

1. **Decomposition**: Break problem into sub-questions
   - What are the core components?
   - What dependencies exist?
   - What's the minimum viable solution?

2. **Cross-Domain**: Find analogies from other fields
   - How does [other domain] solve this?
   - What patterns from [framework X] apply?
   - What would a [role] think about this?

3. **Challenge**: Question hidden assumptions
   - What if the opposite were true?
   - What constraint is artificial?
   - What would an expert in [other field] notice?

4. **Synthesis**: Combine insights
   - What's the novel solution?
   - What's the trade-off?
   - What's the next step?

---

## Question Patterns

### Tech-Focused
- What existing pattern in [framework] solves this?
- How would this scale to 10x load?
- What's the simplest solution that could work?
- Which constraint is artificial vs real?

### Business/Design
- What would frustrate a user about this?
- How do successful products handle this?
- What's the hidden cost of this complexity?
- What would a PM ask about this?

### Socratic
- What am I assuming here?
- What would happen if the opposite were true?
- What domain has solved a similar problem?
- What would an expert in [other field] notice?

---

## Cross-Domain Triggers

| Keyword | Explore |
|---------|---------|
| "optimize" | Caching patterns, CDN strategies |
| "scale" | Distributed systems, sharding |
| "user flow" | UX patterns, onboarding funnels |
| "error handling" | Resilience engineering, circuit breakers |
| "auth" | OAuth flows, session patterns |
| "data" | ETL patterns, data modeling |
| "performance" | Profiling, async processing |
| "security" | OWASP, threat modeling |

---

## Output Format

```markdown
## Self-Questions Generated

1. [Question about assumptions]
2. [Question about constraints]
3. [Cross-domain question - Tech]
4. [Cross-domain question - Business/UX]
5. [Adversarial question - why might this fail?]

## Insights

### [Question 1]
[Brief answer/insight]

### [Question 2]
[Brief answer/insight]

...

## Discovery Summary

**Key Insight:** [Most valuable discovery]

**Recommendation:** [Concrete next step]

**Alternative Frame:** [Different perspective on the problem]
```

---

## Anti-Patterns

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| Jump to solution | Miss non-obvious insights | Always question first |
| Ask obvious questions | Waste thinking time | Challenge assumptions |
| Single-domain thinking | Limited perspective | Cross-domain analogies |
| Accept constraints | Miss opportunities | Question every limit |

---

## Examples

### Example 1: API Optimization

**Problem:** "How to optimize this API endpoint?"

**Self-Questions:**
1. What's actually slow? (assumption: whole endpoint)
2. Is caching possible? (constraint: always fresh data?)
3. What would Redis solve? (cross-domain: caching)
4. What would a DBA notice? (cross-domain: query patterns)
5. Why might optimization fail? (adversarial)

**Key Insight:** 80% of requests are for the same 20 items — cache those.

### Example 2: Architecture Design

**Problem:** "Design notification system" (--deep)

**Phase 1 (Decomposition):**
- What triggers notifications?
- What channels needed? (email, push, SMS)
- What's the delivery SLA?

**Phase 2 (Cross-Domain):**
- How does Slack handle real-time?
- How does Amazon handle millions of emails?
- What patterns does Firebase use for push?

**Phase 3 (Challenge):**
- Do we really need real-time for all notifications?
- What if we batch non-urgent ones?
- Is eventual consistency acceptable?

**Phase 4 (Synthesis):**
- Tiered system: urgent (real-time) vs batched (hourly digest)
- Use message queue for durability
- Start with email, add channels incrementally

---

## Guardrails

**NEVER:**
- Skip the questioning phase and jump to solutions
- Ask obvious questions that waste reasoning capacity
- Limit thinking to a single domain
- Accept all constraints without questioning

**MUST:**
- Always generate questions before answering
- Include cross-domain analogies (Tech + Business/UX)
- Synthesize findings into actionable insights
- Challenge hidden assumptions explicitly

## Trigger Examples

Prompts that should activate this skill:
- "Help me discover the root cause of this bug"
- "Explore this problem from different angles"
- "What questions should I ask about this feature?"
- "Deep dive into this architecture decision"
- "Research approaches for handling..."
- "Investigate why this is failing"

## Related Skills

- **context-engineering** — Managing discovery context
- **unified-workflow** — Persisting discoveries in workflow
- **serena-navigation** — Exploring codebase for insights

## Version History

- 1.0.0 — Initial release (adapted from t3chn/skills)
