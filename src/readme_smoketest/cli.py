from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from .analyze import analyze_records
from .metrics import summarize
from .model import Record


def load_records(path: Path) -> list[Record]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("dataset root must be a JSON array")
    return [Record.from_dict(item) for item in data]


def deterministic_payload(results: list[dict[str, Any]], summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "study_id": "joss-122-root-readme-pilot",
        "results": results,
        "summary": summary,
    }


def write_outputs(payload: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    json_path = output_dir / "pilot-results.json"
    json_path.write_text(json_text, encoding="utf-8")

    rows = [r for r in payload["results"] if r.get("eligible")]
    with (output_dir / "pilot-results.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "order",
                "doi",
                "title",
                "repository",
                "readme_sha",
                "external_docs",
                "install_safe",
                "first_use_safe",
                "strict_ready",
                "relaxed_ready",
                "naive_ready",
                "hard_defect_count",
                "hard_defects",
                "substitution_blocks",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **{key: row[key] for key in writer.fieldnames if key in row},
                    "hard_defect_count": len(row["hard_defects"]),
                    "hard_defects": ";".join(row["hard_defects"]),
                }
            )

    digest = hashlib.sha256(json_text.encode("utf-8")).hexdigest()
    (output_dir / "SHA256SUMS").write_text(f"{digest}  pilot-results.json\n", encoding="utf-8")


def run(dataset: Path, output_dir: Path) -> dict[str, Any]:
    records = load_records(dataset)
    results = analyze_records(records)
    summary = summarize(results)
    payload = deterministic_payload(results, summary)
    write_outputs(payload, output_dir)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="readme-smoketest")
    sub = parser.add_subparsers(dest="command", required=True)
    pilot = sub.add_parser("pilot", help="run the frozen JOSS issue 122 pilot")
    pilot.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/processed/readme-blocks.json"),
    )
    pilot.add_argument("--output-dir", type=Path, default=Path("results/reproduced"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "pilot":
            payload = run(args.dataset, args.output_dir)
            print(json.dumps(payload["summary"], ensure_ascii=False, indent=2, sort_keys=True))
            return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
