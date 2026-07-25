from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "evaluate_issue_121.py"


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("evaluate_issue_121", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reference_strict_labels_are_complete() -> None:
    module = load_script()
    assert len(module.REFERENCE_STRICT_TRUE) == 24
    assert module.REFERENCE_STRICT_TRUE <= set(range(1, 40)) - {15}
    assert set(module.FALSE_NOTES) == (set(range(1, 40)) - {15}) - module.REFERENCE_STRICT_TRUE
    assert set(module.TRUE_NOTES) == module.REFERENCE_STRICT_TRUE


def test_install_labels_cover_every_strict_label() -> None:
    module = load_script()
    assert module.REFERENCE_STRICT_TRUE <= module.REFERENCE_INSTALL_TRUE


def test_sklearn_path_predictions_are_frozen_for_reference_review() -> None:
    module = load_script()
    assert module.SKLEARN_FALSE_POSITIVES == (
        "missing_relative_path:input_model/all_data.json",
        "missing_relative_path:input_model/y_pred.csv",
        "missing_relative_path:output_model/y_pred_new.csv",
    )


def test_prediction_file_must_match_prediction_lock(tmp_path: Path) -> None:
    module = load_script()
    prediction_dir = tmp_path / "predictions"
    prediction_dir.mkdir()
    prediction_path = prediction_dir / "predictions.json"
    prediction_path.write_text("{}\n")
    lock = {
        "annotations_present_when_locked": False,
        "prediction_json_sha256": "0" * 64,
    }
    (prediction_dir / "PREDICTION_LOCK.json").write_text(json.dumps(lock))
    with pytest.raises(ValueError, match="prediction file hash does not match lock"):
        module.verify_prediction_lock(tmp_path)

    lock["prediction_json_sha256"] = hashlib.sha256(prediction_path.read_bytes()).hexdigest()
    (prediction_dir / "PREDICTION_LOCK.json").write_text(json.dumps(lock))
    assert module.verify_prediction_lock(tmp_path) == lock
