from __future__ import annotations

from pathlib import Path

from conftest import run_subprocess


def test_installed_copy_builds_without_vault_workdir(
    python_executable: str,
    digest_fixture: Path,
    deep_dive_fixture: Path,
    installed_copy_root: Path,
    tmp_path: Path,
):
    required_paths = [
        installed_copy_root / "SKILL.md",
        installed_copy_root / "implementation_guide.md",
        installed_copy_root / "learnings.md",
        installed_copy_root / "references" / "sources.md",
        installed_copy_root / "references" / "digest-template.html",
        installed_copy_root / "references" / "deep-dive-template.html",
        installed_copy_root / "scripts" / "build_report.py",
    ]
    for required_path in required_paths:
        assert required_path.exists(), f"installed copy missing required path: {required_path}"

    build_script = installed_copy_root / "scripts" / "build_report.py"
    digest_output = tmp_path / "installed-digest.html"
    deep_output = tmp_path / "installed-deep-dive.html"

    digest_result = run_subprocess(
        [python_executable, str(build_script), str(digest_fixture), str(digest_output)],
        cwd=tmp_path,
    )
    assert digest_result.returncode == 0, (
        f"installed-copy digest build failed\n"
        f"stdout: {digest_result.stdout}\n"
        f"stderr: {digest_result.stderr}"
    )

    deep_result = run_subprocess(
        [python_executable, str(build_script), str(deep_dive_fixture), str(deep_output)],
        cwd=tmp_path,
    )
    assert deep_result.returncode == 0, (
        f"installed-copy deep-dive build failed\n"
        f"stdout: {deep_result.stdout}\n"
        f"stderr: {deep_result.stderr}"
    )

    assert digest_output.is_file()
    assert deep_output.is_file()
