# Implementation Guide — MCP Researcher

This guide explains how the `mcp-researcher` skill's feedback loop works, how to set it up, and how to maintain it over time. Keep this file alongside `SKILL.md` and `learnings.md`. It is for humans, not for Claude to load at runtime.

## What you built

A skill that:

1. Reads `learnings.md` at the start of every run and applies stored rules.
2. Sources MCP servers from 5 curated directories cross-referenced for quality.
3. Calculates a visible composite Quality Score (0–100) per server.
4. Generates a self-contained interactive HTML report with Chart.js visuals, sortable tables, and statistics — saved to your vault.
5. Runs in two modes on a daily schedule: Digest (Mon–Fri) and Deep-Dive category rotation (Sat–Sun).
6. Asks for feedback after each task and appends any corrections to `learnings.md`.

## The honest mechanism

Claude does not silently learn between sessions. There is no background process that updates files on its own. The "learning" is the result of two explicit steps every run:

- **Step 0 (start of run):** Claude reads `learnings.md` because `SKILL.md` tells it to.
- **Step 8 (end of run):** Claude asks for feedback because `SKILL.md` tells it to, and writes any new rule to `learnings.md`.

If Claude skips either step, nothing learns. The discipline lives in the skill file.

## Setup checklist

Before relying on this skill:

- [ ] Confirm `SKILL.md` is in `.claude/skills/mcp-researcher/` and discoverable
- [ ] Confirm `learnings.md` sits in the same directory
- [ ] Verify the `learnings_path` field in `SKILL.md` frontmatter is the correct absolute path
- [ ] Run the skill once with a trivial task to confirm it loads, executes, and asks for feedback
- [ ] Provide a real correction during that first run so the first rule gets written
- [ ] Run the skill a second time and confirm the first rule gets loaded and applied

If the second run doesn't reference the rule, something is wrong — troubleshoot before relying on the skill.

## Invocation

- **Slash command:** `/mcp-researcher` followed by the task or topic
- **Natural language:** "find MCP servers for X", "daily MCP digest", "MCP deep dive on databases", "what MCP servers are there for file ops", or any phrasing that signals MCP server research

The skill's first action is to read `learnings.md` and report the rule count. If the file is missing, it creates one automatically.

## Quality Score formula

The composite score (0–100) shown as a badge on every server:

| Component | Weight | Source |
|---|---|---|
| Stars (log-normalized to 10k) | 40 pts | GitHub |
| Freshness (days since last commit, linear decay over 1yr) | 30 pts | GitHub |
| Install count (log-normalized to 50k) | 20 pts | Smithery |
| Issue health (closed / total issues ratio) | 10 pts | GitHub |

Badge colours: green (80–100), amber (60–79), orange (40–59), red (0–39).

## Daily schedule modes

| Day | Mode | What it does |
|---|---|---|
| Mon–Fri | Digest | New/updated servers in past 24h — trends, what just shipped |
| Sat–Sun | Deep-Dive | Full category analysis — all servers in one domain, ranked and compared |

Category rotation (Deep-Dive): tracks `last_category` in `Research Notes/MCP/MOC.md` frontmatter. Rotate through: Databases → Browser automation → File system → Cloud → Dev tools → Communication → AI & LLM tooling → repeat.

## Report output

All reports are self-contained HTML files:
- No external CDN calls — Chart.js embedded inline
- Dark mode via `prefers-color-scheme: dark`
- Responsive layout
- Sortable tables (click column header)
- Live filter input (searches name and description)

Saved to: `Research Notes/MCP/YYYY-MM-DD [Digest | {Category} Deep-Dive].html`
MOC updated at: `Research Notes/MCP/MOC.md`

## Writing good feedback

The feedback loop only works as well as the feedback you provide:

- **Be specific.** "Don't include archived repos in the main table" is usable. "Make it better" is not.
- **Include the why.** The why helps Claude generalise to similar situations.
- **Name the scope.** Is this a rule for every run, or just this task?
- **Categorise.** "Never do this again" → `critical_error`. "This would be nice" → `user_preference`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Skill ignores learned rules | Step 0 skipped or `learnings_path` wrong | Verify absolute path in `SKILL.md` frontmatter |
| Rules feel oppressive | Too many `critical_error` rules | Re-categorise to `quality_improvement`; run a pruning pass |
| Duplicate rules accumulate | No dedup check on append | Step 9 checks for near-duplicates; run manual pruning if needed |
| Contradicting rules | Feedback shifted over time | Step 0 surfaces the conflict; resolve manually in `learnings.md` |
| HTML report won't open offline | External CDN reference crept in | Chart.js must be embedded inline — check the generated HTML source |
| MOC not updated | Vault save step skipped | Re-run Step 6 manually or check that `Research Notes/MCP/` exists |

## Maintenance and pruning

A `learnings.md` file is a living document. Run a pruning pass every ~30 rules:

1. Read through all rules in each category.
2. Merge duplicates.
3. Mark obsolete rules `status: retired` (don't delete — keeps ID history intact).
4. Promote `quality_improvement` rules that have been reliably correct to `critical_error`.
5. Demote `critical_error` rules causing false positives to `quality_improvement`.

## Scheduling

To run this skill automatically on a daily schedule, use the `/schedule` skill. Point it at this skill with a cron expression (e.g. `0 8 * * *` for 8am daily). The skill detects the day of week at runtime to select Digest vs Deep-Dive mode automatically.

## Version

Generated 2026-04-23. Skill `mcp-researcher` v1.0.0 with self-learning feedback loop via `self-learning-skill-scaffold`.
