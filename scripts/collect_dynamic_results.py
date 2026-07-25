#!/usr/bin/env python3
"""Validate and index raw dynamic case results without interpreting friction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/issue-121/dynamic-tests/case-manifest.json"),
    )
    parser.add_argument(
        "--results-root",
        type=Path,
        default=Path("data/issue-121/dynamic-tests/results"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/issue-121"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = read_json(args.manifest)
    expected = [case["case_id"] for case in manifest["cases"]]
    documents: list[dict[str, Any]] = []
    for case_id in expected:
        result_path = args.results_root / case_id / "result.json"
        if not result_path.exists():
            raise FileNotFoundError(f"missing dynamic result: {result_path}")
        document = read_json(result_path)
        if document["case"]["case_id"] != case_id:
            raise ValueError(f"case mismatch in {result_path}")
        documents.append(document)
    discovered = sorted(path.parent.name for path in args.results_root.glob("*/result.json"))
    if discovered != sorted(expected):
        raise ValueError("dynamic result set differs from locked case manifest")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    index_path = args.output_dir / "dynamic-raw-index.json"
    index_path.write_text(canonical_json(documents), encoding="utf-8")
    rows: list[dict[str, Any]] = []
    for document in documents:
        case = document["case"]
        relations = document["preliminary_relations"]
        rows.append(
            {
                "case_id": case["case_id"],
                "order": case["order"],
                "repository": case["repository"],
                "ecosystem": case["ecosystem"],
                "predicted_strict_ready": case["predicted_strict_ready"],
                "reference_strict_ready": case["reference_strict_ready"],
                "predicted_hard_finding_count": len(case["predicted_hard_findings"]),
                "status": document["status"],
                "failure_reason": document["failure_reason"] or "",
                "attempt_duration_seconds": document["attempt_duration_seconds"],
                "installation_seconds": document["installation_seconds"],
                "task_seconds": document["task_seconds"],
                "total_seconds_to_first_output": (
                    document["total_seconds_to_first_output"] or ""
                ),
                "manual_command_steps": document["manual_command_steps"],
                "non_root_document_pages": document["non_root_document_pages"],
                "workspace_bytes": document["workspace_bytes"],
                "strict_false_negative_completed": relations[
                    "strict_false_negative_completed"
                ],
                "external_docs_supplemented": relations[
                    "external_docs_supplemented"
                ],
                "hard_findings_disproved_by_runtime_paths": relations[
                    "predicted_hard_findings_disproved_by_runtime_paths"
                ],
            }
        )
    csv_path = args.output_dir / "dynamic-raw-index.csv"
    write_csv(csv_path, rows)
    hashed_paths = [index_path, csv_path]
    hashed_paths.extend(
        args.results_root / case_id / "result.json" for case_id in expected
    )
    sums = "".join(
        f"{sha256(path)}  {path.as_posix()}\n" for path in hashed_paths
    )
    (args.output_dir / "DYNAMIC-SHA256SUMS").write_text(sums, encoding="utf-8")
    counts: dict[str, int] = {}
    for document in documents:
        status = str(document["status"])
        counts[status] = counts.get(status, 0) + 1
    print(canonical_json({"case_count": len(documents), "statuses": counts}), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
