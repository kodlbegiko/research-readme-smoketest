from __future__ import annotations

import math
from collections.abc import Iterable
from typing import Any


def confusion(predicted: Iterable[bool], actual: Iterable[bool]) -> dict[str, int]:
    tp = fp = tn = fn = 0
    for pred, truth in zip(predicted, actual, strict=True):
        if pred and truth:
            tp += 1
        elif pred and not truth:
            fp += 1
        elif not pred and truth:
            fn += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def classification_metrics(counts: dict[str, int]) -> dict[str, float]:
    tp, fp, tn, fn = (counts[key] for key in ("tp", "fp", "tn", "fn"))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    specificity = tn / (tn + fp) if tn + fp else 0.0
    accuracy = (tp + tn) / (tp + fp + tn + fn) if tp + fp + tn + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "accuracy": accuracy,
        "f1": f1,
    }


def wilson_interval(
    successes: int, total: int, z: float = 1.959963984540054
) -> tuple[float, float]:
    if total <= 0:
        raise ValueError("total must be positive")
    p = successes / total
    z2 = z * z
    denominator = 1 + z2 / total
    centre = (p + z2 / (2 * total)) / denominator
    margin = z * math.sqrt((p * (1 - p) + z2 / (4 * total)) / total) / denominator
    return max(0.0, centre - margin), min(1.0, centre + margin)


def defect_pairs(results: Iterable[dict[str, Any]], key: str) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for result in results:
        if not result.get("eligible"):
            continue
        for defect in result[key]:
            pairs.add((str(result["repository"]), str(defect)))
    return pairs


def set_metrics(predicted: set[tuple[str, str]], actual: set[tuple[str, str]]) -> dict[str, Any]:
    true_positives = len(predicted & actual)
    false_positives = len(predicted - actual)
    false_negatives = len(actual - predicted)
    precision = true_positives / len(predicted) if predicted else 0.0
    recall = true_positives / len(actual) if actual else 0.0
    return {
        "tp": true_positives,
        "fp": false_positives,
        "fn": false_negatives,
        "precision": precision,
        "recall": recall,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [result for result in results if result.get("eligible")]
    if not eligible:
        raise ValueError("no eligible GitHub repositories")
    manual_ready = [bool(result["manual_strict_ready"]) for result in eligible]
    proposed_ready = [bool(result["strict_ready"]) for result in eligible]
    naive = [bool(result["naive_ready"]) for result in eligible]
    strict_count = sum(proposed_ready)
    relaxed_count = sum(bool(result["relaxed_ready"]) for result in eligible)
    defect_repositories = sum(bool(result["hard_defects"]) for result in eligible)
    strict_ci = wilson_interval(strict_count, len(eligible))
    defect_ci = wilson_interval(defect_repositories, len(eligible))
    proposed_confusion = confusion(proposed_ready, manual_ready)
    naive_confusion = confusion(naive, manual_ready)
    proposed_defects = defect_pairs(eligible, "hard_defects")
    manual_defects = defect_pairs(eligible, "manual_hard_defects")
    return {
        "sample_total": len(results),
        "eligible_github_repositories": len(eligible),
        "strict_ready_count": strict_count,
        "strict_ready_rate": strict_count / len(eligible),
        "strict_ready_wilson_95": list(strict_ci),
        "relaxed_ready_count": relaxed_count,
        "relaxed_ready_rate": relaxed_count / len(eligible),
        "repositories_with_hard_defects": defect_repositories,
        "hard_defect_repo_rate": defect_repositories / len(eligible),
        "hard_defect_repo_wilson_95": list(defect_ci),
        "proposed_confusion": proposed_confusion,
        "proposed_metrics": classification_metrics(proposed_confusion),
        "naive_confusion": naive_confusion,
        "naive_metrics": classification_metrics(naive_confusion),
        "hard_defect_metrics": set_metrics(proposed_defects, manual_defects),
    }
