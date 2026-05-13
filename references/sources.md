# MCP Researcher — Sourcing Reference

Detailed instructions for pulling data from each directory. Read this file during Step 2 of the skill.

---

## Source Priority

| Source | Best for | Quality signal | Tool |
|---|---|---|---|
| modelcontextprotocol/servers | Reference implementations | Highest — official | WebFetch |
| punkpeye/awesome-mcp-servers | Comprehensive inventory | High — community curated | WebFetch |
| Smithery (smithery.ai) | Install counts, categories, UX | High — adoption data | WebFetch |
| Glama (glama.ai/mcp/servers) | Secondary sweep, search | Medium | WebFetch |
| PulseMCP (pulsemcp.com) | New/recent additions | Medium — time-sensitive | WebFetch |
| Exa (mcp.exa.ai) | Discovering servers not yet in curated lists | Variable — use for breadth | `web_search_exa` / `web_fetch_exa` |
| mcpservers.org | Recent additions, category browsing | Medium — discovery only, no stats | WebFetch |

**Exa is available as an MCP connector** — use `web_search_exa` and `web_fetch_exa` tools when they are present in the session. Exa uses neural/semantic search, making it better than keyword search for finding newly published or obscure MCP servers. Use it as a sweep after the primary sources to catch anything not yet indexed in the curated lists.

A server appearing in 3+ sources scores a source-count bonus in trustworthiness. Note the count in the report.

---

## Source 1: punkpeye/awesome-mcp-servers (GitHub)

**URL:** `https://github.com/punkpeye/awesome-mcp-servers`

**How to read:**
- Fetch the README.md raw content
- Sections are organised by category (e.g., `## Databases`, `## Browser Automation`)
- Each entry is a markdown list item: `- [Name](repo-url) — description`
- For Digest mode: check recent commits on the repo to find newly added lines (look at the diff of the last 1–3 commits)
- For Deep-Dive mode: extract all entries under the relevant category section

**What to collect:**
- Server name, repo URL, description (from the list item)
- Then fetch the individual GitHub repo for full stats (stars, last commit, etc.)

**Edge cases:**
- Some entries link to npm packages or docs rather than GitHub repos — note these separately
- Entries with `(archived)` or `(deprecated)` tags: include but mark abandoned regardless of commit date

---

## Source 2: Smithery

**URL:** `https://smithery.ai`

**How to read:**
- Smithery lists servers with install counts and category tags
- For Digest mode: sort by "Newest" or "Recently Updated"
- For Deep-Dive mode: use the category filter matching the rotation category
- Each server page shows: description, tool definitions, install count, GitHub link

**What to collect:**
- Install count (key differentiator — not available elsewhere)
- Tool definitions exposed (listed on the server page)
- Category tags
- GitHub repo URL (use this to cross-reference with other sources)

**Note:** Smithery install counts reflect real adoption — weight these heavily when comparing servers in the same category.

---

## Source 3: Glama

**URL:** `https://glama.ai/mcp/servers`

**How to read:**
- Searchable directory with metadata
- Use the search bar for category terms (e.g., "database", "browser", "file")
- Each listing shows description, tags, and links to the repo

**What to collect:**
- Repo URL (for cross-referencing)
- Tags and description
- Any quality indicators shown

**Use as:** secondary sweep to catch servers not listed on awesome-mcp-servers or Smithery.

---

## Source 4: PulseMCP

**URL:** `https://pulsemcp.com`

**How to read:**
- Publishes weekly digests of new MCP servers
- Check the homepage or latest digest post for servers added in the past 7 days
- For Digest mode: focus on the most recent weekly post

**What to collect:**
- Server name and repo URL
- Brief description from the digest
- Publication date (to confirm recency)

**Note:** PulseMCP is a discovery source only — always follow up with the GitHub repo for stats.

---

## Source 5: modelcontextprotocol/servers (Official)

**URL:** `https://github.com/modelcontextprotocol/servers`

**How to read:**
- Official Anthropic reference implementations
- README lists servers by category with links
- Each server is a sub-folder in the repo with its own README

**What to collect:**
- Server name, description, category
- Tools exposed (in each server's README)
- Note: these have no "install count" via Smithery — treat as authoritative reference quality

**Use as:** the gold standard for implementation patterns. Always check if an official reference server exists in the category before recommending third-party alternatives.

---

## GitHub Repo Data Collection

For each server's GitHub repo, fetch the repo page and extract:

| Field | Where to find it |
|---|---|
| Stars | Top-right star count |
| Forks | Next to stars |
| Last commit | Below the repo name ("Updated X ago") |
| Open issues | Issues tab count |
| Contributors | Right sidebar "Contributors" section |
| Licence | Right sidebar "Licence" section |
| Language | Right sidebar "Languages" bar |
| Description | Under repo name |

For issue health: if the repo has a "Closed issues" count visible, use `closed / (open + closed)`. If not available without clicking through, skip issue health (set to 0) and note data unavailability.

**Rate limiting:** GitHub allows ~60 unauthenticated requests/hour. For large Deep-Dive sweeps (15+ servers), prioritise collecting stats for the top candidates by stars rather than fetching every server exhaustively.

---

## Source 6: Exa (MCP Connector)

**Tools:** `web_search_exa`, `web_fetch_exa`

**How to use:**
- Only available when the Exa MCP connector is attached (CCR trigger and interactive sessions with Exa connected)
- Run after all primary sources are exhausted — use Exa to catch servers not yet in any curated list

**Digest mode queries:**
```
web_search_exa: "new MCP server released site:github.com"
web_search_exa: "Model Context Protocol server npm published this week"
```

**Deep-Dive mode queries (substitute category):**
```
web_search_exa: "MCP server database postgres site:github.com"
web_search_exa: "Model Context Protocol browser automation tool"
```

**What to collect:**
- GitHub repo URL (use as canonical ID for deduplication)
- Description from the search result snippet
- Source: mark as "Exa discovery" — these are unverified until cross-referenced

**Important:** Treat Exa results as leads, not confirmed entries. Always fetch the GitHub repo to verify it is a genuine MCP server (check for `mcp` in the package name, README, or `server.ts`/`index.py` entrypoint) before including in the report. Exa's semantic search may surface related but non-MCP projects.

---

## Source 7: mcpservers.org

**URL:** `https://mcpservers.org/?sort=newest`

**How to read:**
- The "Latest MCPs" row on the homepage lists recently added servers
- Category tabs (Database, Cloud Service, Web Scraping, etc.) are useful for Deep-Dive sweeps
- Individual server pages link out to GitHub repos — use those as the canonical identifier

**What to collect:**
- Server name and GitHub repo URL (follow the server link to get the repo URL)
- Brief description from the listing
- Source: mark as "mcpservers.org"

**Use as:** Digest discovery source alongside PulseMCP — surfaces servers not yet in awesome-mcp-servers or Smithery. Treat entries as leads; always fetch the GitHub repo for actual stats (stars, commit date, forks).

**Note:** No per-server stats are shown on the directory — star counts, commit dates, and install counts must be collected from GitHub after discovery.

---

## Deduplication Rules

1. Match by GitHub repo URL (canonical identifier)
2. If two sources list different URLs for what appears to be the same server (e.g., npm package vs GitHub), use the GitHub URL as canonical and note both
3. Remove forks of the same server — keep the most-starred version unless the fork is clearly the maintained successor (check if original is archived)

---

## Quality Flags

Apply these flags in the report:

| Flag | Condition |
|---|---|
| ⚠ Abandoned | Last commit > 12 months ago |
| ✓ Official | Source is modelcontextprotocol/servers |
| ★ Multi-source | Appears in 3+ directories |
| 🔥 Trending | Added in past 7 days AND stars > 100 |
