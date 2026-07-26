#!/usr/bin/env python3
"""Validate impact-log structure, counts, and CSV/JSON consistency."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "jsonschema is required. Install with `python -m pip install -e '.[publication]'`."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "results" / "public-interest" / "impact-log.json"
CSV_PATH = ROOT / "results" / "public-interest" / "impact-log.csv"
SCHEMA_PATH = ROOT / "docs" / "impact-entry-schema.json"

TYPE_TO_COUNT = {
    "independent_reproduction": "independent_reproductions",
    "independent_human_reannotation": "independent_human_reannotations",
    "external_citation": "external_citations",
    "accepted_upstream_correction": "accepted_upstream_corrections",
    "measured_user_benefit": "measured_user_benefit_outcomes",
    "protocol_adoption": "protocol_adoptions",
    "documented_productization_decision_change": "documented_productization_decision_changes",
}

ENTRY_FIELDS = (
    "evidence_id",
    "evidence_type",
    "date",
    "source",
    "independent_party",
    "verification_status",
    "possible_duplication",
    "conflict_of_interest",
    "outcome_status",
    "supporting_url_or_archive",
    "reviewer_identity_or_role",
    "notes",
    "counted",
)


class ImpactLogValidationError(ValueError):
    """Raised when public impact records disagree or violate governance rules."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_csv_bool(value: str, *, evidence_id: str) -> bool:
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ImpactLogValidationError(
            f"CSV counted must be true or false for {evidence_id}: {value!r}"
        )
    return normalized == "true"


def normalize_json_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {field: entry[field] for field in ENTRY_FIELDS}


def normalize_csv_entry(row: dict[str, str]) -> dict[str, Any]:
    evidence_id = row.get("evidence_id", "<missing evidence_id>")
    missing = [field for field in ENTRY_FIELDS if field not in row]
    if missing:
        raise ImpactLogValidationError(
            f"CSV evidence row {evidence_id} is missing columns: {', '.join(missing)}"
        )
    normalized: dict[str, Any] = {field: row[field] for field in ENTRY_FIELDS}
    normalized["counted"] = parse_csv_bool(row["counted"], evidence_id=evidence_id)
    return normalized


def index_entries(
    entries: list[dict[str, Any]], *, source_name: str
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for entry in entries:
        evidence_id = str(entry.get("evidence_id", ""))
        if not evidence_id:
            raise ImpactLogValidationError(f"{source_name} entry is missing evidence_id")
        if evidence_id in indexed:
            raise ImpactLogValidationError(
                f"duplicate evidence_id in {source_name}: {evidence_id}"
            )
        indexed[evidence_id] = entry
    return indexed


def validate_entry_consistency(
    json_entries: list[dict[str, Any]], csv_entry_rows: list[dict[str, str]]
) -> None:
    normalized_json = [normalize_json_entry(entry) for entry in json_entries]
    normalized_csv = [normalize_csv_entry(row) for row in csv_entry_rows]
    json_by_id = index_entries(normalized_json, source_name="JSON")
    csv_by_id = index_entries(normalized_csv, source_name="CSV")

    if json_by_id.keys() != csv_by_id.keys():
        missing_in_csv = sorted(json_by_id.keys() - csv_by_id.keys())
        missing_in_json = sorted(csv_by_id.keys() - json_by_id.keys())
        raise ImpactLogValidationError(
            "CSV/JSON evidence IDs differ: "
            f"missing in CSV={missing_in_csv}, missing in JSON={missing_in_json}"
        )

    for evidence_id, json_entry in json_by_id.items():
        csv_entry = csv_by_id[evidence_id]
        differing = [
            field for field in ENTRY_FIELDS if json_entry[field] != csv_entry[field]
        ]
        if differing:
            details = ", ".join(
                f"{field}: JSON={json_entry[field]!r}, CSV={csv_entry[field]!r}"
                for field in differing
            )
            raise ImpactLogValidationError(
                f"CSV/JSON evidence mismatch for {evidence_id}: {details}"
            )


def validate_files() -> None:
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    log = load_json(JSON_PATH)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(log),
        key=lambda error: list(error.path),
    )
    if errors:
        rendered = "\n".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ImpactLogValidationError(rendered)

    counted = Counter(
        TYPE_TO_COUNT[entry["evidence_type"]]
        for entry in log["entries"]
        if entry["counted"]
        and entry["verification_status"] == "VERIFIED"
        and entry["outcome_status"] == "ACCEPTED"
    )
    for name, value in log["counts"].items():
        if value != counted[name]:
            raise ImpactLogValidationError(
                f"count mismatch for {name}: JSON={value}, entries={counted[name]}"
            )

    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or rows[0]["record_type"] != "SUMMARY":
        raise ImpactLogValidationError("impact-log.csv must begin with one SUMMARY row")
    summary = rows[0]
    if summary["as_of_utc"] != log["as_of_utc"]:
        raise ImpactLogValidationError("CSV summary as_of_utc does not match JSON")
    if summary["study_id"] != log["study_id"]:
        raise ImpactLogValidationError("CSV summary study_id does not match JSON")
    if summary["log_status"] != log["status"]:
        raise ImpactLogValidationError("CSV summary log_status does not match JSON")
    for name, value in log["counts"].items():
        if int(summary[name]) != value:
            raise ImpactLogValidationError(f"CSV summary mismatch for {name}")

    unexpected = [
        row.get("record_type", "")
        for row in rows[1:]
        if row.get("record_type") != "EVIDENCE"
    ]
    if unexpected:
        raise ImpactLogValidationError(
            f"unexpected CSV record types after SUMMARY: {unexpected}"
        )
    entry_rows = rows[1:]
    validate_entry_consistency(log["entries"], entry_rows)


def run_self_test() -> None:
    entry: dict[str, Any] = {
        "evidence_id": "impact-0001",
        "evidence_type": "external_citation",
        "date": "2026-07-26",
        "source": "https://example.org/citation",
        "independent_party": "Independent researcher",
        "verification_status": "VERIFIED",
        "possible_duplication": "No duplicate located",
        "conflict_of_interest": "None disclosed",
        "outcome_status": "ACCEPTED",
        "supporting_url_or_archive": "https://example.org/archive",
        "reviewer_identity_or_role": "Repository owner",
        "notes": "Synthetic validator self-test",
        "counted": True,
    }
    matching_row = {
        "record_type": "EVIDENCE",
        **{
            field: ("true" if field == "counted" else str(entry[field]))
            for field in ENTRY_FIELDS
        },
    }
    validate_entry_consistency([entry], [matching_row])

    mismatched_row = deepcopy(matching_row)
    mismatched_row["source"] = "https://example.org/different-source"
    try:
        validate_entry_consistency([entry], [mismatched_row])
    except ImpactLogValidationError:
        pass
    else:  # pragma: no cover
        raise ImpactLogValidationError("self-test failed to detect a CSV/JSON mismatch")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run a synthetic consistency test instead of validating repository files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        if args.self_test:
            run_self_test()
            print("impact log validator self-test passed")
        else:
            validate_files()
            print("impact log valid")
    except ImpactLogValidationError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
