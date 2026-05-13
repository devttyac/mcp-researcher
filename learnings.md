---
skill: mcp-researcher
schema_version: 1.0
created: 2026-04-23
last_updated: 2026-04-23
rule_count: 0
next_rule_id: 1
---

# Learnings — MCP Researcher

This file stores constraints learned from user feedback. The `mcp-researcher` skill reads it at the start of every run and applies the rules to its output. New rules are appended at the end of each run after each task.

## How to read this file

Each rule has:

- **ID** — stable identifier (`R-NNNN`, never reused even if the rule is deleted)
- **Date** — when the rule was added
- **Category** — `critical_error`, `quality_improvement`, or `user_preference`
- **Rule** — short, specific, actionable sentence
- **Why** — the feedback or incident that prompted it
- **Applied in** — optional list of run IDs where the rule fired

## How to apply these rules

When `mcp-researcher` runs:

1. Read this file before starting the task.
2. For each rule, check whether it applies to the current task.
3. Enforce `critical_error` rules as hard constraints. Violating one means stopping and revising.
4. Apply `quality_improvement` rules unless the task explicitly overrides them.
5. Apply `user_preference` rules by default; override only when the user gives a per-task instruction that conflicts.

If two rules conflict, surface both to the user and ask which applies to this task. Do not silently pick one.

## Categories

### Critical errors — hard constraints

Rules in this section are non-negotiable. If you notice yourself about to violate one, stop and revise before continuing. These are things the user has explicitly told you never to do again.

<!-- CRITICAL_ERROR_RULES_START -->
<!-- New critical_error rules go here, one per block, most recent first -->

_(No rules yet. Run the skill and provide feedback to populate this section.)_

<!-- CRITICAL_ERROR_RULES_END -->

### Quality improvements — strong advisory

Rules in this section represent things the user wants done better. Apply them unless clearly inappropriate for the current task. If you skip one, note why in your output.

<!-- QUALITY_IMPROVEMENT_RULES_START -->
<!-- New quality_improvement rules go here, one per block, most recent first -->

_(No rules yet.)_

<!-- QUALITY_IMPROVEMENT_RULES_END -->

### User preferences — stylistic defaults

Rules in this section are personal or stylistic preferences. Apply them by default; a per-task instruction from the user can override them.

<!-- USER_PREFERENCE_RULES_START -->
<!-- New user_preference rules go here, one per block, most recent first -->

_(No rules yet.)_

<!-- USER_PREFERENCE_RULES_END -->

## Rule block format

When appending a new rule, use this exact block:

```markdown
### R-NNNN — short title
- **Added:** YYYY-MM-DD
- **Category:** critical_error | quality_improvement | user_preference
- **Rule:** One imperative sentence. What to do or not do, when, and how.
- **Why:** One sentence citing the feedback or incident that prompted it.
- **Applied in:** (optional — append run IDs as they occur)
```

After writing the rule, increment `next_rule_id` in the frontmatter and update `rule_count` and `last_updated`.

## Fail-safes

- **Corruption** — if the skill can't parse this file, it warns the user once and continues with whatever rules it could read.
- **Conflict** — if two rules contradict, the skill surfaces both and asks the user which applies. This is the human's call.
- **Overgrowth** — when `rule_count` > 100 or this file exceeds 2,000 lines, the skill prompts the user to run a pruning pass.
- **Overconstraint** — if applying all stored rules would make the task impossible, the skill stops, lists the conflicts, and asks which to relax.

## Integration note

This file is the public zero-rule template for the `mcp-researcher` skill. It is safe to distribute because it contains no personal learned rules or local run history.
