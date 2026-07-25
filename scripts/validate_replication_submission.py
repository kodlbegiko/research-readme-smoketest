#!/usr/bin/env python3
"""Validate an independent replication result against the published schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - command-line dependency message
    raise SystemExit(
        "jsonschema is required. Install with `python -m pip install 'jsonschema[format]'`."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "replication-result-schema.json"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc


def validate_schema(schema: dict[str, Any]) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", nargs="?", type=Path)
    parser.add_argument("--check-schema", action="store_true")
    args = parser.parse_args()

    schema = load_json(SCHEMA_PATH)
    validator = validate_schema(schema)
    if args.check_schema and args.result is None:
        print(f"schema valid: {SCHEMA_PATH}")
        return 0
    if args.result is None:
        parser.error("provide a result JSON file or use --check-schema")

    instance = load_json(args.result)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        for error in errors:
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            print(f"{location}: {error.message}", file=sys.stderr)
        return 1

    print(f"replication result valid: {args.result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
