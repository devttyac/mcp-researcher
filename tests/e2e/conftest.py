from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


SKILL_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = SKILL_ROOT / "tests" / "fixtures"
DEFAULT_VAULT_ROOT = SKILL_ROOT.parents[2]


def run_subprocess(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.fixture
def skill_root() -> Path:
    return SKILL_ROOT


@pytest.fixture
def vault_root() -> Path:
    candidate = DEFAULT_VAULT_ROOT
    if (candidate / "GEMINI.md").is_file() and (candidate / "AGENTS.md").is_file():
        return candidate
    return candidate


@pytest.fixture
def vault_policy_root(vault_root: Path) -> Path | None:
    if (vault_root / "GEMINI.md").is_file() and (vault_root / "AGENTS.md").is_file():
        return vault_root
    return None


@pytest.fixture
def python_executable() -> str:
    return sys.executable


@pytest.fixture
def build_script(skill_root: Path) -> Path:
    return skill_root / "scripts" / "build_report.py"


@pytest.fixture
def digest_fixture() -> Path:
    return FIXTURES_DIR / "digest-sample.json"


@pytest.fixture
def deep_dive_fixture() -> Path:
    return FIXTURES_DIR / "deep-dive-sample.json"


@pytest.fixture
def digest_dispatch_prompt() -> Path:
    return FIXTURES_DIR / "dispatch-digest-prompt.txt"


@pytest.fixture
def deep_dive_dispatch_prompt() -> Path:
    return FIXTURES_DIR / "dispatch-deep-dive-prompt.txt"


@pytest.fixture
def installed_copy_root(tmp_path: Path, skill_root: Path) -> Path:
    install_root = tmp_path / "installed-mcp-researcher"
    install_root.mkdir()

    for rel_path in ["SKILL.md", "implementation_guide.md"]:
        shutil.copy2(skill_root / rel_path, install_root / rel_path)

    shutil.copytree(skill_root / "references", install_root / "references")
    shutil.copytree(skill_root / "scripts", install_root / "scripts")

    # Simulate the public release layout with a clean learnings template.
    (install_root / "learnings.md").write_text(
        "---\n"
        "created: 2026-05-13\n"
        "tags:\n"
        "  - mcp-researcher\n"
        "  - learnings\n"
        "status: seedling\n"
        "rule_count: 0\n"
        "---\n\n"
        "# Learnings\n\n"
        "## Critical Errors\n\n"
        "## Active Rules\n",
        encoding="utf-8",
    )

    return install_root
