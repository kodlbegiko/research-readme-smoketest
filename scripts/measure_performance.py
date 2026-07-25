#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import time
import tracemalloc
from pathlib import Path

from readme_smoketest.cli import load_records
from readme_smoketest.analyze import analyze_records
from readme_smoketest.metrics import summarize


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=Path("data/processed/readme-blocks.json"))
    parser.add_argument("--repeats", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=Path("results/published/performance.json"))
    args = parser.parse_args()
    if args.repeats <= 0:
        parser.error("--repeats must be positive")

    records = load_records(args.dataset)
    durations: list[float] = []
    tracemalloc.start()
    for _ in range(args.repeats):
        start = time.perf_counter()
        summarize(analyze_records(records))
        durations.append(time.perf_counter() - start)
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    payload = {
        "dataset": str(args.dataset),
        "repeats": args.repeats,
        "median_seconds": statistics.median(durations),
        "mean_seconds": statistics.fmean(durations),
        "p95_seconds": sorted(durations)[int(0.95 * (len(durations) - 1))],
        "peak_tracemalloc_bytes": peak,
        "note": (
            "Machine-specific exploratory measurement; excluded from deterministic result hash."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
