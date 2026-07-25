#!/usr/bin/env python3
"""Validate impact-log structure, counts, and CSV/JSON consistency."""

from __future__ import annotations

import csv
import json
from collections import Counter
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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
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
        raise SystemExit(rendered)

    counted = Counter(
        TYPE_TO_COUNT[entry["evidence_type"]]
        for entry in log["entries"]
        if entry["counted"]
        and entry["verification_status"] == "VERIFIED"
        and entry["outcome_status"] == "ACCEPTED"
    )
    for name, value in log["counts"].items():
        if value != counted[name]:
            raise SystemExit(f"count mismatch for {name}: JSON={value}, entries={counted[name]}")

    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or rows[0]["record_type"] != "SUMMARY":
        raise SystemExit("impact-log.csv must begin with one SUMMARY row")
    summary = rows[0]
    for name, value in log["counts"].items():
        if int(summary[name]) != value:
            raise SystemExit(f"CSV summary mismatch for {name}")

    entry_rows = [row for row in rows[1:] if row["record_type"] == "EVIDENCE"]
    if len(entry_rows) != len(log["entries"]):
        raise SystemExit("CSV/JSON evidence-entry count mismatch")

    print("impact log valid")


if __name__ == "__main__":
    main()
