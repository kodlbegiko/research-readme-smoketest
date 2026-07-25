#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text()
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one literal replacement, found {count}")
    target.write_text(text.replace(old, new, 1))


def regex_once(path: str, pattern: str, replacement: str) -> None:
    target = Path(path)
    text = target.read_text()
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"{path}: expected one regex replacement, found {count}: {pattern}")
    target.write_text(updated)


def patch_dynamic_harness() -> None:
    path = Path("scripts/run_dynamic_case.py")
    text = path.read_text()
    if "import signal\n" not in text:
        replace_once(
            str(path),
            "import re\nimport shutil\nimport subprocess\n",
            "import re\nimport shutil\nimport signal\nimport subprocess\n",
        )

    replacement = '''def terminate_process_group(
    process: subprocess.Popen[str], grace_seconds: int = 5
) -> tuple[str, str]:
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        return process.communicate(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        return process.communicate()


def run_step(
    spec: StepSpec,
    workspace: Path,
    logs_dir: Path,
    index: int,
    environment: dict[str, str],
) -> dict[str, Any]:
    stdout_path = logs_dir / f"{index:02d}-{slug(spec.name)}.stdout.log"
    stderr_path = logs_dir / f"{index:02d}-{slug(spec.name)}.stderr.log"
    started_at = utc_now()
    started = time.perf_counter()
    timed_command = ["/usr/bin/time", "-v", "bash", "-lc", spec.command]
    timed_out = False
    process = subprocess.Popen(
        timed_command,
        cwd=workspace,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=spec.timeout_seconds)
        return_code = process.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        return_code = 124
        stdout, stderr = terminate_process_group(process)
        stderr += (
            f"\\nTIMEOUT after {spec.timeout_seconds} seconds; "
            "process group terminated\\n"
        )
    duration = time.perf_counter() - started
    stdout_path.write_text(stdout, encoding="utf-8", errors="replace")
    stderr_path.write_text(stderr, encoding="utf-8", errors="replace")
    memory_match = MEMORY_RE.search(stderr)
    peak_rss_kib = int(memory_match.group(1)) if memory_match else None
    return {
        **asdict(spec),
        "started_at": started_at,
        "completed_at": utc_now(),
        "duration_seconds": duration,
        "return_code": return_code,
        "timed_out": timed_out,
        "peak_rss_kib": peak_rss_kib,
        "stdout_log": stdout_path.name,
        "stderr_log": stderr_path.name,
        "stdout_excerpt": short_log(stdout),
        "stderr_excerpt": short_log(stderr),
    }


def common_steps'''
    regex_once(
        str(path),
        r"def run_step\(.*?\n\n\ndef common_steps",
        replacement,
    )

    text = path.read_text()
    start = text.index("def himap_steps()")
    end = text.index("\n\ndef hlafreq_steps()", start)
    block = text[start:end]
    dedent = block.index("textwrap.dedent(")
    first = block.index('"""', dedent)
    second = block.index('"""', first + 3)
    command = '''"""\\n                set -euo pipefail
                mkdir -p task
                cd task
                ../venv/bin/python -m himap.main --mc_sampling True
                artifact="$(find . -type f \\( -path '*/results/*' -o -name '*.csv' -o -name '*.png' \\) -print -quit)"
                test -n "$artifact"
                find . -type f \\( -path '*/results/*' -o -name '*.csv' -o -name '*.png' \\) -print | sed -n '1,20p'
                """'''
    block = block[:first] + command + block[second + 3 :]
    path.write_text(text[:start] + block + text[end:])


def patch_prediction_lock() -> None:
    path = "scripts/evaluate_issue_121.py"
    helper_marker = "def verify_prediction_lock(data_dir: Path)"
    text = Path(path).read_text()
    if helper_marker not in text:
        replace_once(
            path,
            '''def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()
''',
            '''def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_prediction_lock(data_dir: Path) -> dict[str, Any]:
    lock_path = data_dir / "predictions/PREDICTION_LOCK.json"
    prediction_path = data_dir / "predictions/predictions.json"
    if not lock_path.exists():
        raise FileNotFoundError("prediction lock must exist before reference evaluation")
    lock = read_json(lock_path)
    if lock.get("annotations_present_when_locked") is not False:
        raise ValueError("prediction lock does not prove annotations were absent")
    expected = lock.get("prediction_json_sha256")
    if not isinstance(expected, str) or not expected:
        raise ValueError("prediction lock has no prediction_json_sha256")
    actual = sha256(prediction_path)
    if actual != expected:
        raise ValueError(
            f"prediction file hash does not match lock: expected {expected}, got {actual}"
        )
    return lock
''',
        )

    text = Path(path).read_text()
    if 'lock = verify_prediction_lock(args.data_dir)' not in text:
        regex_once(
            path,
            r'''    lock_path = args\.data_dir / "predictions/PREDICTION_LOCK\.json"\n.*?    records = read_json\(args\.data_dir / "raw/source-records\.json"\)''',
            '''    lock = verify_prediction_lock(args.data_dir)
    records = read_json(args.data_dir / "raw/source-records.json")''',
        )


def patch_acquisition_commit_pin() -> None:
    path = "scripts/acquire_issue_121.py"
    text = Path(path).read_text()
    if "def resolve_commit(" not in text:
        replace_once(
            path,
            "def path_exists(client: GitHubClient, repository: str, branch: str, path: str) -> bool:\n",
            '''def resolve_commit(client: GitHubClient, repository: str, branch: str) -> str:
    encoded_ref = quote(branch, safe="")
    payload = client.get_json(f"/repos/{repository}/commits/{encoded_ref}")
    if not isinstance(payload, dict) or not isinstance(payload.get("sha"), str):
        raise ValueError(f"unable to resolve immutable commit for {repository}@{branch}")
    return str(payload["sha"])


def path_exists(client: GitHubClient, repository: str, branch: str, path: str) -> bool:
''',
        )

    text = Path(path).read_text()
    if '"acquired_commit_sha": acquired_commit_sha' not in text:
        replace_once(
            path,
            '''    branch = str(repo_payload["default_branch"])
    metadata = {
        **base_metadata,
        "default_branch": branch,
        "primary_language": repo_payload.get("language"),
''',
            '''    branch = str(repo_payload["default_branch"])
    acquired_commit_sha = resolve_commit(client, repository, branch)
    metadata = {
        **base_metadata,
        "default_branch": branch,
        "acquired_commit_sha": acquired_commit_sha,
        "primary_language": repo_payload.get("language"),
''',
        )
        replace_once(
            path,
            "    readme = fetch_readme(client, repository, branch)\n",
            "    readme = fetch_readme(client, repository, acquired_commit_sha)\n",
        )
        replace_once(
            path,
            "    path_index = {path: path_exists(client, repository, branch, path) for path in path_candidates}\n",
            '''    path_index = {
        path: path_exists(client, repository, acquired_commit_sha, path)
        for path in path_candidates
    }
''',
        )


def append_tests() -> None:
    path = Path("tests/test_dynamic_harness.py")
    text = path.read_text()
    if "import os\n" not in text:
        text = text.replace(
            "import importlib.util\nimport json\nimport sys\n",
            "import importlib.util\nimport json\nimport os\nimport sys\nimport time\n",
            1,
        )
    if "test_timeout_terminates_descendant_process_group" not in text:
        text += '''


def test_himap_task_propagates_failure_and_requires_task_artifact() -> None:
    module = load_script()
    task = next(step for step in module.himap_steps() if step.phase == "task")
    assert "set -euo pipefail" in task.command
    assert 'test -n "$artifact"' in task.command
    assert "find . ../venv" not in task.command


def test_timeout_terminates_descendant_process_group(tmp_path: Path) -> None:
    module = load_script()
    logs = tmp_path / "logs"
    logs.mkdir()
    command = (
        "python -c 'import pathlib, subprocess, time; "
        "p=subprocess.Popen([\"sleep\", \"30\"]); "
        "pathlib.Path(\"child.pid\").write_text(str(p.pid)); time.sleep(30)'"
    )
    result = module.run_step(
        module.StepSpec("timeout tree", "task", command, 1),
        tmp_path,
        logs,
        1,
        dict(os.environ),
    )
    assert result["timed_out"] is True
    assert result["return_code"] == 124
    pid = int((tmp_path / "child.pid").read_text())
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        stat = Path(f"/proc/{pid}/stat")
        if not stat.exists() or stat.read_text().split()[2] == "Z":
            break
        time.sleep(0.05)
    else:
        raise AssertionError(f"descendant process {pid} survived timeout")
'''
    path.write_text(text)

    path = Path("tests/test_issue121_reference.py")
    text = path.read_text()
    if "import hashlib\n" not in text:
        text = text.replace(
            "import importlib.util\nfrom pathlib import Path\n",
            "import hashlib\nimport importlib.util\nimport json\nfrom pathlib import Path\n\nimport pytest\n",
            1,
        )
    if "test_prediction_file_must_match_prediction_lock" not in text:
        text += '''


def test_prediction_file_must_match_prediction_lock(tmp_path: Path) -> None:
    module = load_script()
    prediction_dir = tmp_path / "predictions"
    prediction_dir.mkdir()
    prediction_path = prediction_dir / "predictions.json"
    prediction_path.write_text("{}\\n")
    lock = {
        "annotations_present_when_locked": False,
        "prediction_json_sha256": "0" * 64,
    }
    (prediction_dir / "PREDICTION_LOCK.json").write_text(json.dumps(lock))
    with pytest.raises(ValueError, match="prediction file hash does not match lock"):
        module.verify_prediction_lock(tmp_path)

    lock["prediction_json_sha256"] = hashlib.sha256(prediction_path.read_bytes()).hexdigest()
    (prediction_dir / "PREDICTION_LOCK.json").write_text(json.dumps(lock))
    assert module.verify_prediction_lock(tmp_path) == lock
'''
    path.write_text(text)

    path = Path("tests/test_issue121_pipeline.py")
    text = path.read_text()
    if "import base64\n" not in text:
        text = text.replace(
            "import importlib.util\nfrom pathlib import Path\n",
            "import base64\nimport importlib.util\nfrom pathlib import Path\n",
            1,
        )
    if "test_acquisition_pins_readme_and_path_checks_to_one_commit" not in text:
        text += '''


def test_acquisition_pins_readme_and_path_checks_to_one_commit() -> None:
    module = load_script()

    class FakeClient:
        def __init__(self) -> None:
            self.urls: list[str] = []

        def get_json(self, url: str):
            self.urls.append(url)
            if url == "/repos/example/project":
                return {
                    "default_branch": "main",
                    "language": "Python",
                    "html_url": "https://github.com/example/project",
                    "archived": False,
                }
            if url == "/repos/example/project/commits/main":
                return {"sha": "abc123"}
            if url == "/repos/example/project/contents/README.md?ref=abc123":
                readme = "```python\\nopen('examples/input.csv')\\n```\\n"
                return {
                    "sha": "readme-blob",
                    "content": base64.b64encode(readme.encode()).decode(),
                }
            if url == "/repos/example/project/contents/examples/input.csv?ref=abc123":
                return {"sha": "path-blob"}
            raise AssertionError(url)

        def get_text(self, url: str) -> str:
            raise AssertionError(url)

    client = FakeClient()
    item = {
        "order": 1,
        "doi": "10.example/test",
        "title": "Example",
        "repository": "example/project",
        "host": "github",
    }
    record, exclusion, metadata = module.acquire_record(
        client, item, "2026-07-26T00:00:00Z"
    )
    assert exclusion is None
    assert record is not None
    assert record["path_index"] == {"examples/input.csv": True}
    assert metadata["acquired_commit_sha"] == "abc123"
    content_requests = [url for url in client.urls if "/contents/" in url]
    assert content_requests
    assert all("ref=abc123" in url for url in content_requests)
'''
    path.write_text(text)


def main() -> int:
    patch_dynamic_harness()
    patch_prediction_lock()
    patch_acquisition_commit_pin()
    append_tests()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
