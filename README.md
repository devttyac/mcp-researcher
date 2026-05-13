# mcp-researcher

`mcp-researcher` is a public MCP research skill package that sources, evaluates, and reports on MCP servers from curated directories.

## What it does

- runs in two modes: `Digest` and `Deep-Dive`
- reads structured research data and builds interactive HTML reports
- ships the runtime assets required by `scripts/build_report.py`
- keeps repo-level E2E validation under `tests/e2e/` with fixtures under `tests/fixtures/`

## Package layout

Runtime package contents:

- `.codex-plugin/plugin.json`
- `SKILL.md`
- `implementation_guide.md`
- `learnings.md`
- `references/`
- `scripts/`

Repo-only validation contents:

- `tests/e2e/`
- `tests/fixtures/`

The release zip remains runtime-only. The test tree is validated in the repo before release but is not packaged in the zip under the current contract.

## Path model

All relative paths resolve from the directory containing `SKILL.md`.

- `./learnings.md` is the package-local learnings template
- `references/` contains the templates and sourcing reference
- `scripts/build_report.py` is the package-local report builder
- `./outputs/` is the package-local output directory

Codex plugin metadata lives at `.codex-plugin/plugin.json` and points the plugin skill surface at the repo root via `"skills": "./"` so the existing runtime package layout remains unchanged.

## Modes

- `Digest` focuses on recent changes and short-form findings.
- `Deep-Dive` focuses on one category at a time and produces a full ranked comparison.

## Validation

Current repo-level validation includes:

- repo E2E from `tests/e2e`
- installed-copy portability checks
- runtime-only zip verification before release

Run locally with:

```bash
python3 -m pytest tests/e2e
```

The same repo E2E suite is intended to run in GitHub Actions on pushes, pull requests, and manual workflow dispatch.

## Releases

- `v0.1.0` — initial public release export
- `v0.1.1` — portable public package improvements
- `v0.1.2` — explicit path-resolution guidance plus repo-level E2E validation assets

Latest published release:

- https://github.com/devttyac/mcp-researcher/releases/tag/v0.1.2
