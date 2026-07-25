#!/usr/bin/env python3
"""Generate the single-annotator reference evaluation after prediction lock."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import time
import tracemalloc
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from readme_smoketest.analyze import analyze_records
from readme_smoketest.metrics import classification_metrics, confusion, wilson_interval
from readme_smoketest.model import Record

REFERENCE_STRICT_TRUE = {
    1,
    4,
    9,
    11,
    12,
    17,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    35,
    37,
    38,
}

REFERENCE_INSTALL_TRUE = {
    1,
    2,
    3,
    4,
    6,
    9,
    10,
    11,
    12,
    14,
    16,
    17,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    35,
    36,
    37,
    38,
}

FALSE_NOTES = {
    2: "Concrete installation is present; product use is delegated to ReadTheDocs.",
    3: "Concrete installation is present; tutorials and use are delegated externally.",
    5: "Root README is an RST landing page with external installation and gallery routes.",
    6: "Root README has a PyPI install command; examples are routed to project documentation.",
    7: "Root README is a short landing page linking Tutorials & Docs, without a root path.",
    8: "Root README routes installation, getting started, and examples to ReadTheDocs.",
    10: "Root README has installation and maintainer tests but no end-user first-use example.",
    13: "Root README routes operational instructions to the GitHub wiki.",
    14: "Root README has installation only and links to the qdiv documentation.",
    16: "A binary download is concrete installation, but usage syntax has no concrete input task.",
    18: "The README installs rust-script and shows help/tests, not a project install/build path.",
    34: "Root README is a project landing page linking documentation/wiki, without a root path.",
    36: "Root README has user installation and test commands; practical use is in external docs.",
    39: "Root README is citation-oriented and routes operational material to project websites/wiki.",
}

TRUE_NOTES = {
    1: "Install commands and `python -m himap.main` invocations are both present.",
    4: "Conda installation and a complete YACHT quick demonstration are present.",
    9: "Conda installation and a minimal Python example are present.",
    11: "Conda/source installation and concrete `neat read-simulator` usage are present.",
    12: "Build/install commands and `./bin/UncertRadio` startup are present.",
    17: "PyPI/source installation and Python usage examples are present.",
    19: "Environment installation and a concrete `sparc -i input.yaml` quick start are present.",
    20: "R installation and multiple concrete package usage examples are present.",
    21: "PyPI installation and a Python quick example are present.",
    22: "R installation and quick-start/batch examples are present.",
    23: "Felino installation and concrete test/tutorial invocations are present.",
    24: "Build setup and a concrete Java CLI invocation are present.",
    25: "PyPI/source installation and Python mesh examples are present.",
    26: "PyPI installation and command-line/Python minimal examples are present.",
    27: "PyPI installation and library/CLI examples are present.",
    28: "PyPI installation and JAX usage examples are present.",
    29: "Package installation and multiple concrete Python/R usage examples are present.",
    30: "Pip installation and `wand-launcher`/quick-test invocations are present.",
    31: "Installer commands and a concrete bundled-data pipeline run are present.",
    32: "R installation and a complete dySEM workflow are present.",
    33: "PyPI installation and serialize/deserialize examples are present.",
    35: "PyPI installation and concrete `ado create`/`ado show` commands are present.",
    37: "R installation and concrete package usage examples are present.",
    38: "R installation and a usage example are present.",
}

SKLEARN_FALSE_POSITIVES = (
    "missing_relative_path:input_model/all_data.json",
    "missing_relative_path:input_model/y_pred.csv",
    "missing_relative_path:output_model/y_pred_new.csv",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(value), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reference_annotations(
    records: list[dict[str, Any]], metadata: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    metadata_by_order = {int(item["order"]): item for item in metadata}
    annotations: list[dict[str, Any]] = []
    for record in records:
        order = int(record["order"])
        strict = order in REFERENCE_STRICT_TRUE
        install = order in REFERENCE_INSTALL_TRUE
        first_use = strict
        external_docs = bool(record["external_docs"])
        hard_reviews: list[dict[str, Any]] = []
        if order == 33:
            for defect in SKLEARN_FALSE_POSITIVES:
                hard_reviews.append(
                    {
                        "predicted_finding": defect,
                        "reference_is_hard_defect": False,
                        "evidence_status": "DISPROVED",
                        "rationale": (
                            "The README explicitly tells the user to create input_model/ and "
                            "output_model/; the referenced JSON/CSV files are runtime products, "
                            "not repository assets that should exist upstream."
                        ),
                    }
                )
        annotations.append(
            {
                "order": order,
                "doi": record["doi"],
                "title": record["title"],
                "repository": record["repository"],
                "readme_sha": record["readme_sha"],
                "default_branch": metadata_by_order[order].get("default_branch"),
                "primary_language": metadata_by_order[order].get("primary_language"),
                "readme_bytes": metadata_by_order[order].get("readme_bytes"),
                "safe_installation_or_build": install,
                "safe_first_meaningful_use": first_use,
                "strict_ready": strict,
                "external_docs": external_docs,
                "relaxed_ready": strict or external_docs,
                "unexplained_placeholder_blocks": 0,
                "manual_hard_defects": [],
                "hard_finding_reviews": hard_reviews,
                "evidence_status": "KNOWN",
                "rationale": TRUE_NOTES[order] if strict else FALSE_NOTES[order],
                "requires_dynamic_validation": strict or install,
                "annotation_seconds": None,
                "annotation_time_note": "Per-repository timing was not instrumented.",
            }
        )
    return annotations


def metric_bundle(counts: dict[str, int]) -> dict[str, Any]:
    return {"confusion": counts, "metrics": classification_metrics(counts)}


def strict_metrics(
    predictions: list[dict[str, Any]], annotations: list[dict[str, Any]]
) -> dict[str, Any]:
    actual_by_order = {int(item["order"]): bool(item["strict_ready"]) for item in annotations}
    predicted = [bool(item["strict_ready"]) for item in predictions]
    actual = [actual_by_order[int(item["order"])] for item in predictions]
    naive = [bool(item["naive_ready"]) for item in predictions]
    return {
        "frozen_detector": metric_bundle(confusion(predicted, actual)),
        "naive_baseline": metric_bundle(confusion(naive, actual)),
    }


def hard_defect_metrics(
    predictions: list[dict[str, Any]], annotations: list[dict[str, Any]]
) -> dict[str, Any]:
    predicted_pairs = {
        (str(item["repository"]), str(defect))
        for item in predictions
        for defect in item.get("hard_defects", [])
    }
    actual_pairs = {
        (str(item["repository"]), str(defect))
        for item in annotations
        for defect in item.get("manual_hard_defects", [])
    }
    tp = len(predicted_pairs & actual_pairs)
    fp = len(predicted_pairs - actual_pairs)
    fn = len(actual_pairs - predicted_pairs)
    predicted_repositories = {repository for repository, _ in predicted_pairs}
    actual_repositories = {repository for repository, _ in actual_pairs}
    repo_fp = len(predicted_repositories - actual_repositories)
    total_negative_repositories = len(annotations) - len(actual_repositories)
    per_rule: dict[str, dict[str, Any]] = {}
    rule_names = (
        "missing_git_clone_target",
        "missing_relative_path",
        "apt_get_typo",
        "undeclared_module_assignment",
    )
    for rule in rule_names:
        predicted_rule = {pair for pair in predicted_pairs if pair[1].startswith(rule)}
        actual_rule = {pair for pair in actual_pairs if pair[1].startswith(rule)}
        rule_tp = len(predicted_rule & actual_rule)
        rule_fp = len(predicted_rule - actual_rule)
        rule_fn = len(actual_rule - predicted_rule)
        per_rule[rule] = {
            "predicted": len(predicted_rule),
            "actual": len(actual_rule),
            "tp": rule_tp,
            "fp": rule_fp,
            "fn": rule_fn,
            "precision": rule_tp / len(predicted_rule) if predicted_rule else None,
            "recall": rule_tp / len(actual_rule) if actual_rule else None,
        }
    return {
        "pair_level": {
            "predicted": len(predicted_pairs),
            "actual": len(actual_pairs),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": tp / len(predicted_pairs) if predicted_pairs else None,
            "recall": tp / len(actual_pairs) if actual_pairs else None,
            "recall_status": (
                "not_estimable_no_reference_positives" if not actual_pairs else "estimated"
            ),
        },
        "repository_level": {
            "predicted_positive_repositories": len(predicted_repositories),
            "actual_positive_repositories": len(actual_repositories),
            "false_positive_repositories": repo_fp,
            "false_positive_rate": (
                repo_fp / total_negative_repositories if total_negative_repositories else None
            ),
        },
        "per_rule": per_rule,
    }


def ecosystem_metrics(
    predictions: list[dict[str, Any]], annotations: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    annotation_by_order = {int(item["order"]): item for item in annotations}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for prediction in predictions:
        annotation = annotation_by_order[int(prediction["order"])]
        language = str(annotation.get("primary_language") or "Unknown")
        groups[language].append({"prediction": prediction, "annotation": annotation})
    rows: list[dict[str, Any]] = []
    for language, items in sorted(groups.items()):
        predicted = [bool(item["prediction"]["strict_ready"]) for item in items]
        actual = [bool(item["annotation"]["strict_ready"]) for item in items]
        counts = confusion(predicted, actual)
        rows.append(
            {
                "ecosystem": language,
                "n": len(items),
                "predicted_strict": sum(predicted),
                "reference_strict": sum(actual),
                "accuracy": classification_metrics(counts)["accuracy"],
                **counts,
            }
        )
    return rows


def length_sensitivity(
    predictions: list[dict[str, Any]], annotations: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    prediction_by_order = {int(item["order"]): item for item in predictions}
    ranked = sorted(annotations, key=lambda item: int(item.get("readme_bytes") or 0))
    rows: list[dict[str, Any]] = []
    for index in range(4):
        start = index * len(ranked) // 4
        end = (index + 1) * len(ranked) // 4
        group = ranked[start:end]
        predicted = [
            bool(prediction_by_order[int(item["order"])]["strict_ready"]) for item in group
        ]
        actual = [bool(item["strict_ready"]) for item in group]
        counts = confusion(predicted, actual)
        lengths = [int(item.get("readme_bytes") or 0) for item in group]
        rows.append(
            {
                "quartile": index + 1,
                "n": len(group),
                "min_bytes": min(lengths),
                "max_bytes": max(lengths),
                "median_bytes": statistics.median(lengths),
                "predicted_strict": sum(predicted),
                "reference_strict": sum(actual),
                "accuracy": classification_metrics(counts)["accuracy"],
            }
        )
    return rows


def performance_observation(records: list[dict[str, Any]]) -> dict[str, Any]:
    typed = [Record.from_dict(item) for item in records]
    durations: list[float] = []
    tracemalloc.start()
    for _ in range(1000):
        started = time.perf_counter()
        analyze_records(typed)
        durations.append(time.perf_counter() - started)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "iterations": 1000,
        "median_seconds": statistics.median(durations),
        "peak_tracemalloc_bytes": peak,
        "note": "Machine-specific observation; excluded from deterministic result hashes.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/issue-121"))
    parser.add_argument("--results-dir", type=Path, default=Path("results/issue-121"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    lock_path = args.data_dir / "predictions/PREDICTION_LOCK.json"
    if not lock_path.exists():
        raise FileNotFoundError("prediction lock must exist before reference evaluation")
    lock = read_json(lock_path)
    if lock.get("annotations_present_when_locked") is not False:
        raise ValueError("prediction lock does not prove annotations were absent")
    records = read_json(args.data_dir / "raw/source-records.json")
    metadata = read_json(args.data_dir / "raw/repository-metadata.json")
    predictions = read_json(args.data_dir / "predictions/predictions.json")
    annotations = reference_annotations(records, metadata)
    if len(annotations) != 38:
        raise ValueError("reference annotation must contain 38 eligible repositories")
    if sum(bool(item["strict_ready"]) for item in annotations) != 24:
        raise ValueError("frozen reference strict count changed")
    annotation_path = args.data_dir / "annotations/reference-labels.json"
    annotation_rows_path = args.data_dir / "annotations/reference-labels.csv"
    write_json(annotation_path, annotations)
    write_csv(
        annotation_rows_path,
        [
            {
                "order": item["order"],
                "repository": item["repository"],
                "readme_sha": item["readme_sha"],
                "primary_language": item["primary_language"],
                "readme_bytes": item["readme_bytes"],
                "safe_installation_or_build": item["safe_installation_or_build"],
                "safe_first_meaningful_use": item["safe_first_meaningful_use"],
                "strict_ready": item["strict_ready"],
                "external_docs": item["external_docs"],
                "relaxed_ready": item["relaxed_ready"],
                "manual_hard_defects": ";".join(item["manual_hard_defects"]),
                "rationale": item["rationale"],
            }
            for item in annotations
        ],
    )
    strict = strict_metrics(predictions, annotations)
    hard = hard_defect_metrics(predictions, annotations)
    reference_strict_count = sum(bool(item["strict_ready"]) for item in annotations)
    reference_relaxed_count = sum(bool(item["relaxed_ready"]) for item in annotations)
    predicted_strict_count = sum(bool(item["strict_ready"]) for item in predictions)
    predicted_relaxed_count = sum(bool(item["relaxed_ready"]) for item in predictions)
    metrics = {
        "study": "joss-issue-121-external-validation",
        "prediction_lock": lock,
        "sample_total": 39,
        "eligible_github_repositories": 38,
        "excluded": 1,
        "annotation": {
            "annotators": 1,
            "second_human_annotator": False,
            "agreement": None,
            "cohens_kappa": None,
            "limitation": "Sequential single-annotator reference labels; no inter-rater claim.",
            "batch_started_at": "2026-07-25T14:27:04Z",
            "batch_completed_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "per_repository_timing": "not_instrumented",
        },
        "prevalence": {
            "predicted_strict_count": predicted_strict_count,
            "predicted_strict_rate": predicted_strict_count / 38,
            "predicted_strict_wilson_95": list(wilson_interval(predicted_strict_count, 38)),
            "reference_strict_count": reference_strict_count,
            "reference_strict_rate": reference_strict_count / 38,
            "reference_strict_wilson_95": list(wilson_interval(reference_strict_count, 38)),
            "predicted_relaxed_count": predicted_relaxed_count,
            "predicted_relaxed_rate": predicted_relaxed_count / 38,
            "reference_relaxed_count": reference_relaxed_count,
            "reference_relaxed_rate": reference_relaxed_count / 38,
        },
        "strict_ready_classification": strict,
        "hard_defects": hard,
        "ecosystem_stratification": ecosystem_metrics(predictions, annotations),
        "readme_length_sensitivity": length_sensitivity(predictions, annotations),
        "external_doc_sensitivity": {
            "strict_prediction": [predicted_strict_count, 38],
            "strict_reference": [reference_strict_count, 38],
            "relaxed_prediction": [predicted_relaxed_count, 38],
            "relaxed_reference": [reference_relaxed_count, 38],
        },
        "engineering_gates": {
            "hard_defect_precision_min": 0.80,
            "hard_defect_precision_observed": hard["pair_level"]["precision"],
            "hard_defect_precision_pass": False,
            "hard_defect_false_positive_rate_max": 0.10,
            "hard_defect_false_positive_rate_observed": hard["repository_level"][
                "false_positive_rate"
            ],
            "hard_defect_false_positive_rate_pass": (
                hard["repository_level"]["false_positive_rate"] <= 0.10
            ),
            "strict_accuracy_min": 0.75,
            "strict_accuracy_observed": strict["frozen_detector"]["metrics"]["accuracy"],
            "strict_accuracy_pass": (strict["frozen_detector"]["metrics"]["accuracy"] >= 0.75),
            "static_productization_gate_pass": False,
        },
        "primary_static_verdict": "NOT SUPPORTED",
        "verdict_reason": (
            "Strict-ready accuracy is below the preregistered engineering gate, and all three "
            "predicted hard-defect pairs are reference false positives."
        ),
    }
    metrics_path = args.results_dir / "static-validation-results.json"
    write_json(metrics_path, metrics)
    write_csv(
        args.results_dir / "ecosystem-stratification.csv", metrics["ecosystem_stratification"]
    )
    write_csv(
        args.results_dir / "readme-length-sensitivity.csv",
        metrics["readme_length_sensitivity"],
    )
    write_json(args.results_dir / "performance-observation.json", performance_observation(records))
    deterministic_paths = [
        annotation_path,
        annotation_rows_path,
        metrics_path,
        args.results_dir / "ecosystem-stratification.csv",
        args.results_dir / "readme-length-sensitivity.csv",
    ]
    sums = "".join(f"{sha256(path)}  {path.as_posix()}\n" for path in deterministic_paths)
    (args.results_dir / "SHA256SUMS").write_text(sums, encoding="utf-8")
    print(canonical_json(metrics), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
