#!/usr/bin/env python3
"""Generate deterministic SVG figures for the issue-121 research note.

The script uses only the Python standard library. It can either write the SVG
files or verify that committed SVGs are byte-identical to regenerated output.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def confusion_svg() -> str:
    rows = read_rows("static-confusion-matrix.csv")
    data = {row["prediction"]: row for row in rows}
    cells = [
        (
            "Detector ready / Reference ready",
            int(data["strict_ready"]["reference_strict_ready"]),
            90,
            150,
        ),
        (
            "Detector ready / Reference not ready",
            int(data["strict_ready"]["reference_not_strict_ready"]),
            390,
            150,
        ),
        (
            "Detector not ready / Reference ready",
            int(data["not_strict_ready"]["reference_strict_ready"]),
            90,
            330,
        ),
        (
            "Detector not ready / Reference not ready",
            int(data["not_strict_ready"]["reference_not_strict_ready"]),
            390,
            330,
        ),
    ]
    parts = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="560" '
            'viewBox="0 0 760 560">'
        ),
        '<rect width="760" height="560" fill="white"/>',
        (
            '<text x="380" y="40" text-anchor="middle" font-family="sans-serif" '
            'font-size="24" font-weight="700">Static external-validation '
            "confusion matrix</text>"
        ),
        (
            '<text x="380" y="72" text-anchor="middle" font-family="sans-serif" '
            'font-size="15">38 eligible repositories</text>'
        ),
    ]
    for label, value, x, y in cells:
        parts.append(
            f'<rect x="{x}" y="{y}" width="280" height="140" rx="8" '
            'fill="none" stroke="black" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{x + 140}" y="{y + 48}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="14">{escape(label)}</text>'
        )
        parts.append(
            f'<text x="{x + 140}" y="{y + 105}" text-anchor="middle" '
            'font-family="sans-serif" font-size="42" font-weight="700">'
            f"{value}</text>"
        )
    parts.extend(
        [
            (
                '<text x="380" y="515" text-anchor="middle" '
                'font-family="sans-serif" font-size="15">'
                "TP / FP / FN / TN = 7 / 0 / 17 / 14</text>"
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def dynamic_svg() -> str:
    rows = read_rows("dynamic-outcomes.csv")
    max_count = max(int(row["count"]) for row in rows) or 1
    width = 920
    height = 520
    chart_left = 360
    chart_width = 500
    row_height = 62
    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">'
        ),
        f'<rect width="{width}" height="{height}" fill="white"/>',
        (
            '<text x="460" y="40" text-anchor="middle" font-family="sans-serif" '
            'font-size="24" font-weight="700">Adjudicated dynamic outcomes</text>'
        ),
        (
            '<text x="460" y="70" text-anchor="middle" font-family="sans-serif" '
            'font-size="15">10 locked cases; 8 of 9 testable first tasks '
            "succeeded</text>"
        ),
    ]
    for index, row in enumerate(rows):
        y = 110 + index * row_height
        count = int(row["count"])
        bar_width = round(chart_width * count / max_count)
        label = row["outcome"]
        parts.append(
            f'<text x="340" y="{y + 27}" text-anchor="end" '
            f'font-family="sans-serif" font-size="14">{escape(label)}</text>'
        )
        parts.append(
            f'<rect x="{chart_left}" y="{y}" width="{bar_width}" height="38" '
            'fill="none" stroke="black" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{chart_left + bar_width + 12}" y="{y + 27}" '
            'font-family="sans-serif" font-size="16" font-weight="700">'
            f"{count}</text>"
        )
    parts.extend(
        [
            (
                '<text x="460" y="495" text-anchor="middle" '
                'font-family="sans-serif" font-size="15">'
                "Direct README blockers observed: 0</text>"
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def write_or_check(path: Path, content: str, check: bool) -> None:
    if check:
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            raise SystemExit(f"figure mismatch: {path}")
    else:
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify committed SVGs")
    args = parser.parse_args()
    write_or_check(ROOT / "static-confusion-matrix.svg", confusion_svg(), args.check)
    write_or_check(ROOT / "dynamic-outcomes.svg", dynamic_svg(), args.check)


if __name__ == "__main__":
    main()
