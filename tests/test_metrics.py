from __future__ import annotations

import math

import pytest

from readme_smoketest.metrics import (
    classification_metrics,
    confusion,
    defect_pairs,
    set_metrics,
    summarize,
    wilson_interval,
)


def test_confusion_counts() -> None:
    assert confusion([True, True, False, False], [True, False, True, False]) == {
        "tp": 1,
        "fp": 1,
        "tn": 1,
        "fn": 1,
    }


def test_confusion_rejects_different_lengths() -> None:
    with pytest.raises(ValueError):
        confusion([True], [True, False])


def test_classification_metrics_perfect() -> None:
    metrics = classification_metrics({"tp": 2, "fp": 0, "tn": 3, "fn": 0})
    assert all(value == 1.0 for value in metrics.values())


def test_classification_metrics_zero_denominators() -> None:
    metrics = classification_metrics({"tp": 0, "fp": 0, "tn": 0, "fn": 0})
    assert all(value == 0.0 for value in metrics.values())


def test_wilson_interval_bounds() -> None:
    lower, upper = wilson_interval(7, 19)
    assert 0.19 < lower < 0.20
    assert 0.58 < upper < 0.60


def test_wilson_interval_all_successes() -> None:
    lower, upper = wilson_interval(10, 10)
    assert 0.72 < lower < 0.73
    assert math.isclose(upper, 1.0)


def test_wilson_interval_rejects_zero_total() -> None:
    with pytest.raises(ValueError):
        wilson_interval(0, 0)


def test_defect_pairs() -> None:
    rows = [{"eligible": True, "repository": "a/b", "hard_defects": ["x", "y"]}]
    assert defect_pairs(rows, "hard_defects") == {("a/b", "x"), ("a/b", "y")}


def test_defect_pairs_excludes_ineligible() -> None:
    rows = [{"eligible": False, "repository": "a/b", "hard_defects": ["x"]}]
    assert defect_pairs(rows, "hard_defects") == set()


def test_set_metrics() -> None:
    result = set_metrics({("a", "x"), ("b", "y")}, {("a", "x"), ("c", "z")})
    assert result == {"tp": 1, "fp": 1, "fn": 1, "precision": 0.5, "recall": 0.5}


def test_set_metrics_empty() -> None:
    result = set_metrics(set(), set())
    assert result["precision"] == 0.0
    assert result["recall"] == 0.0


def test_summarize_rejects_no_eligible_records() -> None:
    with pytest.raises(ValueError):
        summarize([{"eligible": False}])


def test_summarize_rates() -> None:
    rows = [
        {
            "eligible": True,
            "repository": "a/a",
            "manual_strict_ready": True,
            "strict_ready": True,
            "relaxed_ready": True,
            "naive_ready": True,
            "hard_defects": [],
            "manual_hard_defects": [],
        },
        {
            "eligible": True,
            "repository": "b/b",
            "manual_strict_ready": False,
            "strict_ready": False,
            "relaxed_ready": True,
            "naive_ready": True,
            "hard_defects": ["x"],
            "manual_hard_defects": ["x"],
        },
    ]
    output = summarize(rows)
    assert output["strict_ready_rate"] == 0.5
    assert output["relaxed_ready_rate"] == 1.0
    assert output["hard_defect_repo_rate"] == 0.5
    assert math.isclose(output["naive_metrics"]["precision"], 0.5)
