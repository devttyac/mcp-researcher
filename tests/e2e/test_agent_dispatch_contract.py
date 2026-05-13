from __future__ import annotations

from pathlib import Path

import pytest


def test_claude_dispatch_contract_is_explicit(
    skill_root: Path, digest_dispatch_prompt: Path, deep_dive_dispatch_prompt: Path
):
    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    digest_prompt = digest_dispatch_prompt.read_text(encoding="utf-8")
    deep_dive_prompt = deep_dive_dispatch_prompt.read_text(encoding="utf-8")

    assert "Resolve all relative file paths from the directory containing this `SKILL.md`." in skill_md
    assert "what's new in MCP" in skill_md
    assert "Digest" in skill_md
    assert "Deep-Dive" in skill_md
    assert "what's new in MCP" in digest_prompt
    assert "deep-dive" in deep_dive_prompt


def test_gemini_dispatch_uses_shared_claude_skill_surface(
    vault_policy_root: Path | None, skill_root: Path
):
    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")

    assert "scripts/build_report.py" in skill_md
    assert "references/sources.md" in skill_md

    if vault_policy_root is None:
        pytest.skip("Vault policy files are not present in the staged public repo surface")

    gemini_md = (vault_policy_root / "GEMINI.md").read_text(encoding="utf-8")
    assert "share `.claude/` infrastructure" in gemini_md
    assert ".claude/skills/" in gemini_md


def test_codex_dispatch_surface_is_registered_or_recorded_gap(vault_root: Path):
    codex_skill_root = vault_root / ".agents" / "skills" / "mcp-researcher"

    if not codex_skill_root.exists():
        pytest.skip("Codex live dispatch surface is not registered under .agents/skills in this checkout")

    if codex_skill_root.is_symlink():
        target = codex_skill_root.resolve()
        assert target.name == "mcp-researcher"
        assert (target / "SKILL.md").is_file()
        return

    assert (codex_skill_root / "SKILL.md").is_file()
