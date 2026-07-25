from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from readme_smoketest.cli import deterministic_payload, load_records, main, run

ROOT = Path(__file__).parents[1]
DATASET = ROOT / "data" / "processed" / "readme-blocks.json"


def test_load_records_requires_array(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON array"):
        load_records(path)


def test_load_records_frozen_sample_size() -> None:
    records = load_records(DATASET)
    assert len(records) == 20
    assert sum(record.host == "github" for record in records) == 19


def test_run_expected_pilot_results(tmp_path: Path) -> None:
    payload = run(DATASET, tmp_path)
    summary = payload["summary"]
    assert summary["strict_ready_count"] == 7
    assert summary["relaxed_ready_count"] == 19
    assert summary["repositories_with_hard_defects"] == 4
    assert summary["proposed_metrics"]["precision"] == 1.0
    assert summary["naive_confusion"]["fp"] == 4


def test_run_writes_machine_readable_outputs(tmp_path: Path) -> None:
    run(DATASET, tmp_path)
    assert (tmp_path / "pilot-results.json").is_file()
    assert (tmp_path / "pilot-results.csv").is_file()
    assert (tmp_path / "SHA256SUMS").is_file()


def test_sha256sums_matches_json(tmp_path: Path) -> None:
    run(DATASET, tmp_path)
    raw = (tmp_path / "pilot-results.json").read_bytes()
    expected = hashlib.sha256(raw).hexdigest()
    assert (tmp_path / "SHA256SUMS").read_text(encoding="utf-8") == (
        f"{expected}  pilot-results.json\n"
    )


def test_run_is_byte_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "a"
    second = tmp_path / "b"
    run(DATASET, first)
    run(DATASET, second)
    assert (first / "pilot-results.json").read_bytes() == (
        second / "pilot-results.json"
    ).read_bytes()
    assert (first / "pilot-results.csv").read_bytes() == (second / "pilot-results.csv").read_bytes()


def test_main_success(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["pilot", "--dataset", str(DATASET), "--output-dir", str(tmp_path)])
    assert code == 0
    assert '"strict_ready_count": 7' in capsys.readouterr().out


def test_main_missing_dataset_returns_two(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = main(
        [
            "pilot",
            "--dataset",
            str(tmp_path / "missing.json"),
            "--output-dir",
            str(tmp_path),
        ]
    )
    assert code == 2
    assert "error:" in capsys.readouterr().out


def test_deterministic_payload_schema() -> None:
    payload = deterministic_payload([], {"x": 1})
    assert payload == {
        "schema_version": "1.0",
        "study_id": "joss-122-root-readme-pilot",
        "results": [],
        "summary": {"x": 1},
    }


def test_published_result_has_expected_study_id(tmp_path: Path) -> None:
    run(DATASET, tmp_path)
    payload = json.loads((tmp_path / "pilot-results.json").read_text(encoding="utf-8"))
    assert payload["study_id"] == "joss-122-root-readme-pilot"
