from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

SCRIPT = Path(__file__).parents[1] / "scripts" / "run_dynamic_case.py"
MANIFEST = Path("data/issue-121/dynamic-tests/case-manifest.json")


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_dynamic_case", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_harness_covers_exactly_the_locked_cases() -> None:
    module = load_script()
    manifest = json.loads(MANIFEST.read_text())
    case_ids = {case["case_id"] for case in manifest["cases"]}
    assert case_ids == set(module.CASE_STEPS)
    assert len(case_ids) == 10


def test_no_dynamic_command_requests_sudo() -> None:
    module = load_script()
    manifest = json.loads(MANIFEST.read_text())
    for case in manifest["cases"]:
        steps = module.common_steps(case) + module.CASE_STEPS[case["case_id"]]()
        assert all("sudo " not in step.command for step in steps)


def test_sklearn_success_dynamically_disproves_path_finding() -> None:
    module = load_script()
    manifest = json.loads(MANIFEST.read_text())
    case = next(case for case in manifest["cases"] if case["case_id"] == "D08-sklearn-migrator")
    relations = module.preliminary_relations(case, "SUCCESS")
    assert relations["strict_false_negative_completed"] is True
    assert relations["predicted_hard_findings_disproved_by_runtime_paths"] is True


def test_failed_case_does_not_claim_dynamic_confirmation() -> None:
    module = load_script()
    manifest = json.loads(MANIFEST.read_text())
    case = manifest["cases"][0]
    relations = module.preliminary_relations(case, "FAILURE")
    assert relations["strict_false_negative_completed"] is False
    assert relations["external_docs_supplemented"] is False
