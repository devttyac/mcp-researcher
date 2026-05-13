---
name: mcp-researcher
description: Sources, evaluates, and reports on MCP servers from curated directories. Generates interactive HTML reports with charts, sortable tables, quality scores, statistics, and implementation ideas — saved to the vault. Always invoke this skill when the user wants to find, research, discover, or track MCP servers, even if they just ask what MCP servers are available for a topic. Triggers on: "find MCP servers for X", "MCP report", "research MCP servers", "what MCP servers exist for Z", "daily MCP digest", "MCP deep dive on [category]", "what's new in MCP", "source MCP servers for my project", or any external routine that invokes Digest or Deep-Dive mode.
feedback_trigger: after each task
learnings_path: /Users/aaronchan/Documents/Aaron's Obsidian Notes Vault/.claude/skills/mcp-researcher/learnings.md
---

# MCP Researcher

Generates interactive HTML research reports on MCP servers, saved to the vault. Applies learned rules from `learnings.md` on every run and captures feedback at the end so future reports improve.

## How learning works

Claude reads `learnings.md` at the start of every run and applies any stored rules. At the end, it asks one feedback question. If you give a correction, it writes a rule — that rule fires on every future run. Nothing updates silently between sessions; the discipline lives in these two explicit steps.

## Two Modes

**Digest**: surfaces new and updated servers from the recent period — trends, momentum, what just shipped.

**Deep-Dive**: full category analysis — every server in a domain, ranked, scored, and compared.

## Step 0 — Detect mode and read learnings.md

**Detect execution mode first.** You are running in **unattended mode** if any of these are true:
- The prompt contains `SCHEDULED_RUN=true` or similar flag
- An external routine explicitly invokes `Digest` or `Deep-Dive` with no human present
- There is no human present to respond to questions

In **unattended mode**: skip Steps 8–10 entirely. Never ask for feedback or wait for a response — there is no one to answer.

In **interactive mode**: all steps apply.

---

Read `/Users/aaronchan/Documents/Aaron's Obsidian Notes Vault/.claude/skills/mcp-researcher/learnings.md` before any other work.

- If the file is missing, create it using the learnings template structure and continue. Log that no rules exist yet.
- If the file is present but malformed, read what you can, warn once, and continue.
- Report to the user (interactive) or log (unattended): "Loaded N rules from learnings.md" and list any `critical_error` rules.

If two rules contradict: in interactive mode, surface both and ask. In unattended mode, apply the more recent rule and log the conflict in the failure report.

## Step 1 — Determine Mode

- User mentions a specific category → Deep-Dive on that category
- User says "what's new", "daily", or "digest" → Digest
- An external routine explicitly asks for `Digest` → Digest
- An external routine explicitly asks for `Deep-Dive` → Deep-Dive
- If there is no clearer signal, default to Digest

## Step 2 — Source Servers

Read `references/sources.md` — it is the single source of truth for which directories to check, mode-specific sourcing instructions, and deduplication rules.

**Error handling — sourcing failures:**

After attempting all sources, check the result count:

- **Zero servers found across all sources** → abort the normal flow. Jump to **Step ERR** immediately. Do not proceed to Steps 3–7.
- **Some sources failed but others returned results** → continue with what you have. Set report status to `⚠️ COMPLETED WITH ERRORS`. Record which sources failed and why in a `sourcing_errors` variable — this goes into the commit message summary and the report header.
- **All sources returned results** → continue normally. Status is `✅ COMPLETED`.

Log each source attempt: what URL was fetched, how many results it returned, and any error (timeout, 0 results, HTTP error). This log is included in the failure report if Step ERR fires.

## Step 3 — Collect Statistics Per Server

For each server, gather:

| Field | Source |
|---|---|
| Name, description, repo URL | Directory listing |
| Stars | GitHub repo page |
| Forks | GitHub repo page |
| Last commit date | GitHub repo page |
| Open issues count | GitHub repo page |
| Contributors count | GitHub repo page |
| Install count | Smithery profile page |
| Tool definitions exposed | README or Smithery |
| Licence | GitHub repo |
| Language | GitHub repo |
| Category/tags | Directory listing |

Flag as **⚠ Abandoned** if last commit > 12 months ago. Include but mark clearly.

## Step 4 — Calculate Quality Score (0–100)

Compute a visible composite score for each server:

```
Stars score      = min(log10(stars + 1) / log10(10000) * 40, 40)
Freshness score  = max(30 - (days_since_commit / 365) * 30, 0)
Install score    = min(log10(installs + 1) / log10(50000) * 20, 20)
Issue health     = (closed_issues / total_issues) * 10   [0 if no issues]

Quality Score = round(Stars + Freshness + Install + Issue Health)
```

Display as a badge: **84/100** — shown in the server table, deep-dive cards, and highlight card.

## Step 5 — Generate HTML Report

**Do not generate HTML or large Python scripts in the response.** Doing so routes large text through the model stream and causes stream idle timeout. Instead, use a two-step approach: write a small JSON data file, then call the pre-built build script.

### Step 5a — Write the data JSON

Use the Write tool to save all collected data to `/tmp/mcp-report-data.json`. The JSON is structured data only — no HTML strings. The build script handles all HTML generation.

**Digest JSON schema:**
```json
{
  "mode": "digest",
  "date": "YYYY-MM-DD",
  "day_of_week": "Monday",
  "sourcing_note": "awesome-mcp-servers · Smithery",
  "servers": [
    {"name":"…","url":"…","cat":"Browser Automation · Python · MIT","score":72,
     "stars":1240,"commit":"2025-03-01","lang":"TypeScript","src":"awesome-mcp",
     "desc":"lowercase keywords for filtering","abandoned":false}
  ],
  "top_chips": [
    {"icon":"⭐","text":"1.2k stars"},
    {"icon":"📅","text":"Mar 01, 2025"},
    {"icon":"📦","text":"500 installs"}
  ],
  "stats": {
    "avg_score": 54.2,
    "abandonment_pct": 12,
    "sources_count": 3,
    "gte40_count": 8,
    "peak_stars": 4200
  },
  "time_series": [
    {"label":"Apr 17","count":3},
    {"label":"Apr 18","count":5}
  ],
  "ideas": [
    {"title":"Idea title","body":"Idea body text."}
  ]
}
```

**Deep-Dive JSON schema:**
```json
{
  "mode": "deep-dive",
  "date": "YYYY-MM-DD",
  "category": "Cloud & infrastructure",
  "sourcing_note": "awesome-mcp-servers · Smithery",
  "exec_summary": "3–5 sentence plain text summary.",
  "servers": [
    {"name":"…","url":"…","subcat":"AWS","score":72,"stars":1240,
     "commit":"2025-03-01","installs":500,"complexity":"Medium",
     "lang":"Python","src":3,"desc":"…","abandoned":false}
  ],
  "stats": {
    "avg_score": 54.2,
    "abandonment_pct": 12,
    "sources_count": 3,
    "median_stars": 450,
    "median_days": 45
  },
  "top_cards": [
    {
      "score": 84,
      "name": "server-name",
      "url": "https://github.com/…",
      "meta": "TypeScript · MIT · 1.2k stars",
      "desc": "Short description.",
      "stats": {"stars":1240,"forks":89,"commit":"2025-03-01","installs":500,"contributors":12},
      "tools": ["tool_one","tool_two"],
      "examples": ["1. Use case one.","2. Use case two.","3. Use case three."],
      "pros": "Strength one. Strength two.",
      "cons": "Limitation one. Limitation two."
    }
  ],
  "subcats": [{"label":"AWS","count":5},{"label":"GCP","count":3}],
  "impl_map": [{"title":"Combo title","desc":"Combo description."}],
  "recommendation": "Plain text recommendation paragraph."
}
```

### Step 5b — Run the build script

```bash
python3 .claude/skills/mcp-researcher/scripts/build_report.py \
  /tmp/mcp-report-data.json \
  "Research Notes/MCP/YYYY-MM-DD [Mode or Category].html"
```

- Digest output: `Research Notes/MCP/YYYY-MM-DD Digest.html`
- Deep-Dive output: `Research Notes/MCP/YYYY-MM-DD [Category] Deep-Dive.html`

If the script errors, check the JSON for missing required fields and fix them. Do not fall back to inline HTML generation.

## Step 6 — Save to Vault

**File path:**
- Digest: `Research Notes/MCP/YYYY-MM-DD Digest.html`
- Deep-Dive: `Research Notes/MCP/YYYY-MM-DD [Category] Deep-Dive.html`

**MOC update:**
Append to `Research Notes/MCP/MOC.md`:
```markdown
- [YYYY-MM-DD Digest](YYYY-MM-DD Digest.html) — N new servers
- [YYYY-MM-DD Databases Deep-Dive](YYYY-MM-DD Databases Deep-Dive.html) — N servers, avg score X
```

If `Research Notes/MCP/` does not exist, create it and initialise `MOC.md` with a header and the first entry.

**Rotation tracking:**
Store `last_category` in `MOC.md` YAML frontmatter so the next Deep-Dive knows which category to use.

## Step 7 — Open and Confirm

In **interactive mode**: open the HTML file: `open "Research Notes/MCP/[filename].html"` and report the save path and Quality Score range.

In **unattended mode**: skip the `open` call. Log the save path and score range instead.

## Step 6b — External automation follow-up (optional, unattended mode only)

**This step is not part of the shipped package contract.** It only applies when an implementer adds an external unattended routine around the skill. In interactive mode, skip it.

Build the commit message using the run status determined in Step 2:

```
mcp-researcher: YYYY-MM-DD - MODE N servers, avg score X | EMOJI STATUS | Action: YES/NO
```

Examples:
```
mcp-researcher: 2026-04-26 - Digest 14 servers, avg score 62 | ✅ Completed | Action: NO
mcp-researcher: 2026-04-26 - Databases Deep-Dive 9 servers, avg score 71 | ✅ Completed | Action: NO
mcp-researcher: 2026-04-26 - Digest 0 servers | ❌ Failed — Exa returned no results | Action: NO
mcp-researcher: 2026-04-26 - Digest 6 servers (partial), avg score 58 | ⚠️ Completed with errors — Smithery fetch failed | Action: NO
```

**Status → Action mapping:**
- `✅ COMPLETED` → `Action: NO`
- `⚠️ COMPLETED WITH ERRORS` → `Action: YES` (review the sourcing errors)
- `❌ FAILED` → `Action: NO` (external automation may alert separately; no manual action is implied by this package alone)

**Git operations (with push retry to handle concurrent Obsidian backup commits):**

```bash
cd "/Users/aaronchan/Documents/Aaron's Obsidian Notes Vault"
git add "Research Notes/MCP/"
git config user.email "mcp-researcher@automation"
git config user.name "MCP Researcher"
git commit -m "mcp-researcher: YYYY-MM-DD - ..."
for i in 1 2 3; do
  git pull --rebase origin master && git push origin master && break
  sleep 5
done
```

If all three push attempts fail, log the error and stop. Any retry or alerting behavior belongs to the external automation layer, not to the shipped package itself.

## Step ERR — Failure report (fires when Step 2 returns zero servers)

This path exists to ensure the notification pipeline always fires, even on complete failure. A commit is better than silence.

1. **Write a minimal failure report** to `Research Notes/MCP/YYYY-MM-DD [Mode] FAILED.md`:

```markdown
---
date: YYYY-MM-DD
mode: Digest | Deep-Dive
status: FAILED
---

# MCP Researcher — Run Failed

**Date:** YYYY-MM-DD  
**Mode:** Digest | Deep-Dive  
**Status:** ❌ FAILED

## What happened

Zero servers were returned across all sources. The report was not generated.

## Source log

| Source | Attempted | Result |
|---|---|---|
| awesome-mcp-servers | ✅ | 0 results |
| Smithery | ❌ | Timeout |
| ... | | |

## Next steps

Check the source URLs manually. If the skill is wrapped in an external routine, the next unattended run may recover automatically once the sources are available again.
```

2. **Update the MOC** — append a failure entry:
```markdown
- [YYYY-MM-DD Digest FAILED](YYYY-MM-DD Digest FAILED.md) — ❌ Run failed — zero servers returned
```

3. **Commit and push** using Step 6b with status `❌ Failed` and the primary error reason in the message.

## Step 8 — Mandatory feedback request (interactive mode only)

**Skip this step entirely in unattended mode.**

This step is not optional in interactive runs — it is how the skill improves over time.

After presenting the report, ask the user:

> Anything I should remember for next time? Specific mistakes to avoid, preferences to apply, or things that worked well? I'll save it to learnings.md and apply it on future runs.

If the user gives no feedback or says "nothing", skip Step 9. Empty feedback means the run was fine.

## Step 9 — Write the rule

If the user provides substantive feedback, translate it into a rule and append to `learnings.md`:

1. **Categorise** — `critical_error` (never do again), `quality_improvement` (do better), or `user_preference` (stylistic default)
2. **Write it specifically** — not "be better at X" but "when doing X, always Y because Z"
3. **Include the why** — one sentence citing what prompted the rule
4. **Append, never overwrite** — add with an incrementing ID (read `next_rule_id` from frontmatter) and today's date
5. **Increment frontmatter** — update `next_rule_id`, `rule_count`, and `last_updated` in `learnings.md`
6. **Confirm** — tell the user: "Added rule R-NNNN to learnings.md: [rule text]"

Before appending, scan existing rules for similar text to avoid duplicates. If a near-duplicate exists, offer to update the existing rule instead.

## Step 10 — Pruning check

If `learnings.md` now exceeds 100 rules or 2,000 lines, prompt:

> Your learnings file has grown to [N] rules. Want to review and consolidate? Duplicate or obsolete rules make the file harder to apply.

Do not auto-prune. The user owns the rule store.

---

## Category Rotation (Deep-Dive)

Rotate in order; read `last_category` from `MOC.md` frontmatter to find the next:

1. Databases & data stores
2. Browser automation & web scraping
3. File system & document processing
4. Cloud & infrastructure
5. Developer tools & IDE integration
6. Communication & productivity
7. AI & LLM tooling

---

## Statistics to Surface in Reports

Beyond per-server stats, always include report-level aggregates:

- **Total servers found** and breakdown by source
- **Abandonment rate** — % with last commit > 12 months
- **Average / median Quality Score** for the set
- **Category distribution** — count and % per category
- **Freshness distribution** — how many updated in past 30 / 90 / 180 / 365 days
- **Week-over-week delta** (Digest only) — compare against previous Digest report in vault if available; surface growth or decline in new server count per category
