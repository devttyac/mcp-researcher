from __future__ import annotations

import json
from pathlib import Path

from conftest import run_subprocess


def _assert_success(result, output_path: Path) -> None:
    assert result.returncode == 0, (
        f"build_report.py exited {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
    assert output_path.is_file(), f"expected output HTML file: {output_path}"


def test_digest_build_succeeds(python_executable: str, build_script: Path, digest_fixture: Path, tmp_path: Path):
    output_path = tmp_path / "digest.html"
    result = run_subprocess([python_executable, str(build_script), str(digest_fixture), str(output_path)])

    _assert_success(result, output_path)
    html = output_path.read_text(encoding="utf-8")
    fixture = json.loads(digest_fixture.read_text(encoding="utf-8"))

    assert fixture["servers"][0]["name"] in html
    assert fixture["ideas"][0]["title"] in html
    assert fixture["sourcing_note"] in html


def test_deep_dive_build_succeeds(
    python_executable: str, build_script: Path, deep_dive_fixture: Path, tmp_path: Path
):
    output_path = tmp_path / "deep-dive.html"
    result = run_subprocess([python_executable, str(build_script), str(deep_dive_fixture), str(output_path)])

    _assert_success(result, output_path)
    html = output_path.read_text(encoding="utf-8")
    fixture = json.loads(deep_dive_fixture.read_text(encoding="utf-8"))

    assert fixture["category"] in html
    assert fixture["top_cards"][0]["name"] in html
    assert fixture["recommendation"] in html
