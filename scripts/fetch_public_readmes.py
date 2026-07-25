#!/usr/bin/env python3
"""Optional acquisition helper for refreshing public GitHub README text.

The published pilot does not depend on this script. It preserves frozen extracted
blocks and blob hashes so reproduction does not require network access.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def github_json(url: str, token: str | None) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "readme-smoketest/0.1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise ValueError("unexpected GitHub response")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=Path("data/raw/source-records.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/acquired"))
    args = parser.parse_args()
    records = json.loads(args.sources.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    token = os.environ.get("GITHUB_TOKEN")
    manifest: list[dict[str, Any]] = []
    for record in records:
        if record.get("host") != "github":
            continue
        repository = str(record["repository"])
        url = f"https://api.github.com/repos/{repository}/readme"
        try:
            payload = github_json(url, token)
            content = base64.b64decode(str(payload["content"])).decode("utf-8")
        except (urllib.error.URLError, KeyError, UnicodeDecodeError, ValueError) as exc:
            manifest.append({"repository": repository, "status": "error", "error": str(exc)})
            continue
        destination = args.output_dir / f"{record['order']:02d}-{repository.replace('/', '__')}.md"
        destination.write_text(content, encoding="utf-8")
        manifest.append(
            {
                "repository": repository,
                "status": "ok",
                "path": str(destination),
                "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                "github_blob_sha": payload.get("sha"),
            }
        )
    (args.output_dir / "acquisition-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
