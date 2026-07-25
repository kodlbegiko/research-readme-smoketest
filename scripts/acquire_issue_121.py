#!/usr/bin/env python3
"""Acquire JOSS issue 121 root READMEs and lock v0.1.0 predictions.

This script changes no detector rule. It converts a frozen sampling frame into the
existing Record schema, mechanically extracts fenced blocks, verifies conservative
relative-path candidates through the GitHub API, runs the frozen analyzer, and writes
machine-readable acquisition and prediction artifacts.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import os
import platform
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from readme_smoketest.analyze import analyze_records
from readme_smoketest.model import Record

API_ROOT = "https://api.github.com"
README_CANDIDATES = (
    "README.md",
    "README.rst",
    "README",
    "Readme.md",
    "readme.md",
    "README.markdown",
)
DOC_TERMS = (
    "documentation",
    "docs",
    "tutorial",
    "tutorials",
    "vignette",
    "guide",
    "manual",
    "wiki",
    "getting started",
    "user guide",
    "examples",
)
PATH_EXTENSIONS = (
    ".csv",
    ".tsv",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
    ".dat",
    ".npy",
    ".npz",
    ".parquet",
    ".pdb",
    ".xyz",
    ".nii",
    ".nii.gz",
    ".sh",
    ".py",
    ".r",
    ".ipynb",
)
FENCE_START = re.compile(r"^\s*(`{3,}|~{3,})\s*([^\s`]*)?.*$")
MARKDOWN_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+[^)]*)?\)")
URL = re.compile(r"https?://[^\s)>\]}'\"]+")
ANGLE = re.compile(r"<[^>\n]+>")
QUOTED_PATH = re.compile(r"[\"']([^\"'\n]+)[\"']")
BARE_PATH = re.compile(r"(?<![\w:/.-])([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+)")
EXPLAIN_TERMS = ("replace", "substitute", "change", "your ", "path/to", "set ")


class GitHubClient:
    def __init__(self, token: str | None) -> None:
        self.token = token
        self.request_count = 0

    def get_json(self, path_or_url: str) -> Any:
        url = path_or_url if path_or_url.startswith("http") else f"{API_ROOT}{path_or_url}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "research-readme-smoketest/0.1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.request_count += 1
        request = Request(url, headers=headers)
        with urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_text(self, url: str) -> str:
        headers = {"User-Agent": "research-readme-smoketest/0.1.0"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.request_count += 1
        request = Request(url, headers=headers)
        with urlopen(request, timeout=45) as response:
            return response.read().decode("utf-8")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(value), encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_heading(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().strip("#").strip())


def extract_blocks(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    heading = ""
    blocks: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        heading_match = MARKDOWN_HEADING.match(lines[index])
        if heading_match:
            heading = normalize_heading(heading_match.group(2))
            index += 1
            continue
        if index + 1 < len(lines):
            underline = lines[index + 1].strip()
            if lines[index].strip() and re.fullmatch(r"[=-]{3,}", underline):
                heading = normalize_heading(lines[index])
                index += 2
                continue
        fence_match = FENCE_START.match(lines[index])
        if not fence_match:
            index += 1
            continue
        fence = fence_match.group(1)
        language = (fence_match.group(2) or "").strip()
        start = index + 1
        index = start
        body: list[str] = []
        while index < len(lines):
            stripped = lines[index].lstrip()
            if stripped.startswith(fence[0] * len(fence)):
                break
            body.append(lines[index])
            index += 1
        code = "\n".join(body).strip("\n")
        nearby = "\n".join(lines[max(0, start - 8) : start]).lower()
        record: dict[str, Any] = {
            "heading": heading,
            "language": language,
            "text": code,
        }
        paths = candidate_paths(code)
        if paths:
            record["referenced_paths"] = paths
        if ANGLE.search(code):
            record["placeholder_explained"] = any(term in nearby for term in EXPLAIN_TERMS)
        blocks.append(record)
        index += 1
    return blocks


def clean_path(value: str) -> str | None:
    candidate = value.strip().strip("`.,;:()[]{}")
    if not candidate or len(candidate) > 240:
        return None
    if candidate.startswith(("http://", "https://", "/", "~/", "-", "$")):
        return None
    if any(char in candidate for char in "*?{}<>|&;"):
        return None
    lowered = candidate.lower()
    if not lowered.endswith(PATH_EXTENSIONS):
        return None
    if "/" not in candidate and not lowered.startswith(("data.", "example.")):
        return None
    while candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate or candidate.startswith("../"):
        return None
    return candidate


def candidate_paths(code: str) -> list[str]:
    candidates: set[str] = set()
    for value in QUOTED_PATH.findall(code):
        cleaned = clean_path(value)
        if cleaned:
            candidates.add(cleaned)
    for value in BARE_PATH.findall(code):
        cleaned = clean_path(value)
        if cleaned:
            candidates.add(cleaned)
    return sorted(candidates)[:20]


def external_documentation(text: str) -> tuple[bool, list[str]]:
    links: set[str] = set()
    for label, target in MARKDOWN_LINK.findall(text):
        context = f"{label} {target}".lower()
        if any(term in context for term in DOC_TERMS):
            links.add(target)
        elif "readthedocs" in target.lower() or ".github.io" in target.lower():
            links.add(target)
    for target in URL.findall(text):
        lowered = target.lower()
        if any(term.replace(" ", "") in lowered.replace("-", "") for term in DOC_TERMS):
            links.add(target)
        elif "readthedocs" in lowered or ".github.io" in lowered:
            links.add(target)
    return bool(links), sorted(links)


def decode_content(payload: dict[str, Any], client: GitHubClient) -> str:
    encoded = payload.get("content")
    if isinstance(encoded, str) and encoded:
        return base64.b64decode(encoded).decode("utf-8")
    download_url = payload.get("download_url")
    if isinstance(download_url, str) and download_url:
        return client.get_text(download_url)
    raise ValueError("GitHub content response has no readable content")


def fetch_readme(client: GitHubClient, repository: str, branch: str) -> tuple[str, str, str] | None:
    for candidate in README_CANDIDATES:
        encoded_path = quote(candidate, safe="")
        encoded_ref = quote(branch, safe="")
        try:
            payload = client.get_json(
                f"/repos/{repository}/contents/{encoded_path}?ref={encoded_ref}"
            )
        except HTTPError as error:
            if error.code == 404:
                continue
            raise
        if not isinstance(payload, dict):
            continue
        return candidate, str(payload["sha"]), decode_content(payload, client)
    return None


def path_exists(client: GitHubClient, repository: str, branch: str, path: str) -> bool:
    encoded_path = quote(path, safe="/")
    encoded_ref = quote(branch, safe="")
    try:
        client.get_json(f"/repos/{repository}/contents/{encoded_path}?ref={encoded_ref}")
    except HTTPError as error:
        if error.code == 404:
            return False
        raise
    return True


def acquire_record(
    client: GitHubClient, item: dict[str, Any], retrieved_at: str
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, dict[str, Any]]:
    base_metadata = {
        "order": item["order"],
        "doi": item["doi"],
        "title": item["title"],
        "repository": item["repository"],
        "host": item["host"],
        "retrieved_at": retrieved_at,
    }
    if item["host"] != "github":
        exclusion = {**base_metadata, "reason": "non_github"}
        return None, exclusion, base_metadata
    repository = str(item["repository"])
    try:
        repo_payload = client.get_json(f"/repos/{repository}")
    except HTTPError as error:
        exclusion = {
            **base_metadata,
            "reason": "inaccessible_repository",
            "http_status": error.code,
        }
        return None, exclusion, base_metadata
    branch = str(repo_payload["default_branch"])
    metadata = {
        **base_metadata,
        "default_branch": branch,
        "primary_language": repo_payload.get("language"),
        "repository_url": repo_payload.get("html_url"),
        "archived": bool(repo_payload.get("archived", False)),
    }
    readme = fetch_readme(client, repository, branch)
    if readme is None:
        exclusion = {**metadata, "reason": "no_recognizable_root_readme"}
        return None, exclusion, metadata
    readme_path, readme_sha, text = readme
    blocks = extract_blocks(text)
    path_candidates = sorted(
        {
            path
            for block in blocks
            for path in block.get("referenced_paths", [])
            if isinstance(path, str)
        }
    )
    path_index = {path: path_exists(client, repository, branch, path) for path in path_candidates}
    external_docs, external_links = external_documentation(text)
    record = {
        "order": item["order"],
        "doi": item["doi"],
        "title": item["title"],
        "repository": repository,
        "host": "github",
        "readme_sha": readme_sha,
        "external_docs": external_docs,
        "external_documentation_links": external_links,
        "blocks": blocks,
        "path_index": path_index,
        "manual_strict_ready": None,
        "manual_hard_defects": [],
        "notes": "Mechanical acquisition; reference annotation not yet created.",
    }
    metadata.update(
        {
            "root_readme_path": readme_path,
            "readme_sha": readme_sha,
            "readme_bytes": len(text.encode("utf-8")),
            "fenced_block_count": len(blocks),
            "external_documentation_links": external_links,
        }
    )
    return record, None, metadata


def prediction_rows(predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for value in predictions:
        rows.append(
            {
                "order": value["order"],
                "repository": value["repository"],
                "eligible": value["eligible"],
                "readme_sha": value.get("readme_sha", ""),
                "install_safe": value.get("install_safe", ""),
                "first_use_safe": value.get("first_use_safe", ""),
                "strict_ready": value.get("strict_ready", ""),
                "relaxed_ready": value.get("relaxed_ready", ""),
                "external_docs": value.get("external_docs", ""),
                "naive_ready": value.get("naive_ready", ""),
                "hard_defects": ";".join(value.get("hard_defects", [])),
                "substitution_blocks": value.get("substitution_blocks", ""),
                "exclusion_reason": value.get("exclusion_reason", ""),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sampling-frame",
        type=Path,
        default=Path("data/issue-121/sampling-frame.json"),
    )
    parser.add_argument("--output-dir", type=Path, default=Path("data/issue-121"))
    parser.add_argument("--token", default=os.environ.get("GH_TOKEN"))
    parser.add_argument("--sleep", type=float, default=0.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    items = read_json(args.sampling_frame)
    if not isinstance(items, list) or len(items) != 39:
        raise ValueError("sampling frame must contain exactly 39 ordered items")
    if [item["order"] for item in items] != list(range(1, 40)):
        raise ValueError("sampling frame order must be exactly 1..39")
    client = GitHubClient(args.token)
    retrieved_at = utc_now()
    records: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    metadata: list[dict[str, Any]] = []
    for item in items:
        record, exclusion, repository_metadata = acquire_record(client, item, retrieved_at)
        metadata.append(repository_metadata)
        if record is not None:
            records.append(record)
        if exclusion is not None:
            exclusions.append(exclusion)
        if args.sleep:
            time.sleep(args.sleep)
    typed = [Record.from_dict(record) for record in records]
    predictions = analyze_records(typed)
    raw_dir = args.output_dir / "raw"
    prediction_dir = args.output_dir / "predictions"
    write_json(raw_dir / "source-records.json", records)
    write_json(raw_dir / "repository-metadata.json", metadata)
    write_json(args.output_dir / "exclusions.json", exclusions)
    write_json(prediction_dir / "predictions.json", predictions)
    write_csv(prediction_dir / "predictions.csv", prediction_rows(predictions))
    environment = {
        "acquired_at": retrieved_at,
        "python": sys.version,
        "platform": platform.platform(),
        "api_requests": client.request_count,
        "sampling_frame_count": len(items),
        "eligible_count": len(records),
        "exclusion_count": len(exclusions),
    }
    write_json(raw_dir / "acquisition-environment.json", environment)
    hashed = [
        raw_dir / "source-records.json",
        raw_dir / "repository-metadata.json",
        args.output_dir / "exclusions.json",
        prediction_dir / "predictions.json",
        prediction_dir / "predictions.csv",
    ]
    sums = "".join(f"{sha256(path)}  {path.relative_to(args.output_dir)}\n" for path in hashed)
    (prediction_dir / "SHA256SUMS").write_text(sums, encoding="utf-8")
    print(canonical_json(environment), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
