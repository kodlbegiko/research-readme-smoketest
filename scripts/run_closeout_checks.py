from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class StepResult:
    step_id: str
    name: str
    command: str
    started_at: str
    completed_at: str
    duration_seconds: float
    return_code: int
    stdout_log: str
    stderr_log: str
    peak_rss_kib: int | None


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_peak_rss(stderr: str) -> int | None:
    match = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", stderr)
    return int(match.group(1)) if match else None


def run_step(
    root: Path,
    step_id: str,
    name: str,
    command: str,
    *,
    cwd: Path | None = None,
    timeout: int = 900,
) -> StepResult:
    logs = root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    stdout_path = logs / f"{step_id}.stdout.log"
    stderr_path = logs / f"{step_id}.stderr.log"
    started = utc_now()
    started_monotonic = time.monotonic()
    wrapped = ["/usr/bin/time", "-v", "bash", "-lc", command]
    try:
        completed = subprocess.run(
            wrapped,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
            env={**os.environ, "PIP_DISABLE_PIP_VERSION_CHECK": "1"},
        )
        return_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as exc:
        return_code = 124
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr if isinstance(exc.stderr, str) else "") + "\nTIMEOUT\n"
    duration = time.monotonic() - started_monotonic
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return StepResult(
        step_id=step_id,
        name=name,
        command=command,
        started_at=started,
        completed_at=utc_now(),
        duration_seconds=round(duration, 6),
        return_code=return_code,
        stdout_log=str(stdout_path.relative_to(root)),
        stderr_log=str(stderr_path.relative_to(root)),
        peak_rss_kib=parse_peak_rss(stderr),
    )


def directory_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def write_environment(root: Path) -> None:
    info = {
        "captured_at": utc_now(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": sys.version,
        "executable": sys.executable,
    }
    (root / "environment.json").write_text(
        json.dumps(info, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_hashes(root: Path) -> None:
    lines: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "SHA256SUMS":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
    (root / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def finish_result(root: Path, payload: dict[str, Any]) -> None:
    payload["workspace_bytes"] = (
        directory_size(root / "workspace") if (root / "workspace").exists() else 0
    )
    payload["completed_at"] = utc_now()
    (root / "result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    shutil.rmtree(root / "workspace", ignore_errors=True)
    write_hashes(root)


def sklearn_correction(output: Path) -> dict[str, Any]:
    root = output / "D08-sklearn-migrator" / "attempt-2-harness-correction"
    workspace = root / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    write_environment(root)
    steps: list[StepResult] = []

    steps.append(
        run_step(
            root,
            "01-clone-frozen-source",
            "clone frozen source",
            "git clone --depth 1 https://github.com/anvaldes/sklearn-migrator.git source && "
            "git -C source checkout fe0e197d78faf8a17a34fd90025d23cbad37af0b",
            cwd=workspace,
            timeout=240,
        )
    )
    steps.append(
        run_step(
            root,
            "02-verify-frozen-readme",
            "verify frozen README blob",
            'test "$(git -C source hash-object README.md)" = '
            '"36a51525a013eb98b635f0ce8b2b3db1ae2a7bb4"',
            cwd=workspace,
            timeout=30,
        )
    )
    steps.append(
        run_step(
            root,
            "03-create-venv",
            "create virtual environment",
            "python -m venv venv",
            cwd=workspace,
            timeout=120,
        )
    )
    steps.append(
        run_step(
            root,
            "04-install-published-package",
            "install sklearn-migrator",
            "venv/bin/python -m pip install --upgrade pip && "
            "venv/bin/python -m pip install sklearn-migrator",
            cwd=workspace,
            timeout=600,
        )
    )
    script = r"""import json
from pathlib import Path

import numpy as np
import sklearn
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn_migrator.regression.random_forest_reg import (
    deserialize_random_forest_reg,
    serialize_random_forest_reg,
)

input_dir = Path("input_model")
output_dir = Path("output_model")
input_dir.mkdir()
output_dir.mkdir()
X, y = make_regression(
    n_samples=120,
    n_features=5,
    noise=0.1,
    random_state=0,
)
model = RandomForestRegressor(n_estimators=20, random_state=0)
model.fit(X, y)
expected = model.predict(X[:20])
serialized = serialize_random_forest_reg(model, sklearn.__version__)
(input_dir / "all_data.json").write_text(json.dumps(serialized))
np.savetxt(input_dir / "y_pred.csv", expected, delimiter=",")
restored = deserialize_random_forest_reg(serialized, sklearn.__version__)
observed = restored.predict(X[:20])
np.savetxt(output_dir / "y_pred_new.csv", observed, delimiter=",")
max_difference = float(np.max(np.abs(expected - observed)))
assert max_difference < 1e-8
assert (input_dir / "all_data.json").is_file()
assert (input_dir / "y_pred.csv").is_file()
assert (output_dir / "y_pred_new.csv").is_file()
print(json.dumps({
    "max_abs_difference": max_difference,
    "sklearn_version": sklearn.__version__,
    "input_dir_created_by_user": True,
    "output_dir_created_by_user": True,
}, sort_keys=True))
"""
    command = (
        "cat > corrected_roundtrip.py <<'PY'\n"
        + script
        + "PY\nvenv/bin/python corrected_roundtrip.py"
    )
    steps.append(
        run_step(
            root,
            "05-run-corrected-roundtrip",
            "run corrected random-forest round trip",
            command,
            cwd=workspace,
            timeout=420,
        )
    )
    steps.append(
        run_step(
            root,
            "06-capture-packages",
            "capture package versions",
            "venv/bin/python -m pip freeze",
            cwd=workspace,
            timeout=60,
        )
    )
    success = all(step.return_code == 0 for step in steps[:5])
    payload: dict[str, Any] = {
        "case_id": "D08-sklearn-migrator",
        "attempt": "attempt-2-harness-correction",
        "original_attempt_relation": (
            "Preserves the locked attempt-1 failure; this is a separate harness correction."
        ),
        "correction_reason": (
            "Attempt 1 imported a nonexistent module and omitted the documented sklearn "
            "version arguments."
        ),
        "only_task_semantic_difference": (
            "The import path and required call signature were aligned to the frozen README/API; "
            "dataset, model, random seeds, round-trip criterion, and user-created runtime paths "
            "were unchanged."
        ),
        "frozen_readme_blob_sha": "36a51525a013eb98b635f0ce8b2b3db1ae2a7bb4",
        "source_commit": "fe0e197d78faf8a17a34fd90025d23cbad37af0b",
        "status": "SUCCESS" if success else "FAILURE",
        "predicted_findings": [
            "missing_relative_path:input_model/all_data.json",
            "missing_relative_path:input_model/y_pred.csv",
            "missing_relative_path:output_model/y_pred_new.csv",
        ],
        "predicted_findings_disposition": "DISPROVED" if success else "NOT_DISPROVED",
        "runtime_paths_require_upstream_assets": False if success else None,
        "steps": [asdict(step) for step in steps],
    }
    finish_result(root, payload)
    return payload


def boost_correction(output: Path) -> dict[str, Any]:
    root = output / "D09-boost-geometry" / "attempt-2-external-doc-delegation"
    workspace = root / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    write_environment(root)
    steps: list[StepResult] = []

    steps.append(
        run_step(
            root,
            "01-clone-frozen-source",
            "clone frozen Boost.Geometry source",
            "git clone --depth 1 --branch master https://github.com/boostorg/geometry.git source",
            cwd=workspace,
            timeout=240,
        )
    )
    steps.append(
        run_step(
            root,
            "02-verify-frozen-readme",
            "verify frozen README blob",
            'test "$(git -C source hash-object README.md)" = '
            '"6f898496335b9a0bf64def628d2ff63852af89bf"',
            cwd=workspace,
            timeout=30,
        )
    )
    steps.append(
        run_step(
            root,
            "03-install-complete-boost-package",
            "install complete Boost development package",
            "sudo apt-get update && sudo apt-get install -y libboost-all-dev",
            cwd=workspace,
            timeout=900,
        )
    )
    source = r"""#include <cmath>
#include <iostream>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>

int main() {
  namespace bg = boost::geometry;
  using point = bg::model::d2::point_xy<double>;
  bg::model::polygon<point> polygon;
  bg::read_wkt("POLYGON((0 0,0 1,1 1,1 0,0 0))", polygon);
  bg::correct(polygon);
  const double area = bg::area(polygon);
  std::cout << area << "\n";
  return std::abs(area - 1.0) < 1e-12 ? 0 : 1;
}
"""
    command = (
        "cat > boost_geometry_example.cpp <<'CPP'\n"
        + source
        + "CPP\n"
        + "g++ -std=c++14 -O2 boost_geometry_example.cpp -o boost-example\n"
        + "./boost-example"
    )
    steps.append(
        run_step(
            root,
            "04-compile-and-run-example",
            "compile and run the same polygon-area example",
            command,
            cwd=workspace,
            timeout=240,
        )
    )
    steps.append(
        run_step(
            root,
            "05-capture-toolchain",
            "capture compiler and Boost package versions",
            "g++ --version && dpkg-query -W -f='${Package} ${Version}\\n' 'libboost*-dev' | sort",
            cwd=workspace,
            timeout=60,
        )
    )
    success = all(step.return_code == 0 for step in steps[:4])
    payload: dict[str, Any] = {
        "case_id": "D09-boost-geometry",
        "attempt": "attempt-2-external-doc-delegation",
        "original_attempt_relation": (
            "Preserves the locked attempt-1 failure; this is a separate official-distribution "
            "correction."
        ),
        "correction_reason": (
            "Attempt 1 cloned only the geometry subrepository, while the root README identifies "
            "it as part of Boost and delegates to official Boost documentation/distribution."
        ),
        "only_task_semantic_difference": (
            "The same C++ source and success criterion were used; the include source changed "
            "from the incomplete subrepository to the complete distribution package."
        ),
        "frozen_readme_blob_sha": "6f898496335b9a0bf64def628d2ff63852af89bf",
        "official_installation_path": (
            "Ubuntu archive package libboost-all-dev (complete Boost development headers)"
        ),
        "non_root_document_pages": 2,
        "external_searches": 0,
        "external_docs_supplemented": success,
        "status": "SUCCESS" if success else "FAILURE",
        "steps": [asdict(step) for step in steps],
    }
    finish_result(root, payload)
    return payload


def woodtapper_recheck(output: Path) -> dict[str, Any]:
    root = output / "intervention-rechecks" / "woodtapper-current"
    workspace = root / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    write_environment(root)
    steps: list[StepResult] = []
    commit = "3c8f9ff07108d901a662326912a6d82dddaf7047"

    steps.append(
        run_step(
            root,
            "01-clone-current-default-branch",
            "clone current default branch",
            "git clone --depth 1 https://github.com/artefactory/woodtapper.git source && "
            f"git -C source checkout {commit}",
            cwd=workspace,
            timeout=240,
        )
    )
    steps.append(
        run_step(
            root,
            "02-verify-current-documentation",
            "verify current README and package metadata blobs",
            'test "$(git -C source hash-object README.md)" = '
            '"b07652102469791d6b0c1ecab597a849a9aa31ae" && '
            'test "$(git -C source hash-object pyproject.toml)" = '
            '"13ecb5be9c59a16735351bd57d8072fc7a518b6c"',
            cwd=workspace,
            timeout=30,
        )
    )
    steps.append(
        run_step(
            root,
            "03-create-published-venv",
            "create clean published-package environment",
            "python -m venv published-venv && "
            "published-venv/bin/python -m pip install --upgrade pip",
            cwd=workspace,
            timeout=180,
        )
    )
    steps.append(
        run_step(
            root,
            "04-install-published-command",
            "rerun documented published install command",
            "published-venv/bin/python -m pip install woodtapper",
            cwd=workspace,
            timeout=600,
        )
    )
    steps.append(
        run_step(
            root,
            "05-create-current-source-venv",
            "create clean current-source environment",
            "python -m venv source-venv && source-venv/bin/python -m pip install --upgrade pip",
            cwd=workspace,
            timeout=180,
        )
    )
    steps.append(
        run_step(
            root,
            "06-install-current-source",
            "install current default branch",
            "source-venv/bin/python -m pip install ./source",
            cwd=workspace,
            timeout=900,
        )
    )
    task = r"""from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from woodtapper.extract_rules import SirusClassifier

X, y = make_classification(n_samples=120, n_features=6, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0, stratify=y
)
model = SirusClassifier(
    n_estimators=50,
    max_depth=2,
    quantile=10,
    p0=0.01,
    random_state=0,
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
assert len(predictions) == len(X_test)
print({"prediction_count": len(predictions)})
"""
    command = "cat > current_task.py <<'PY'\n" + task + "PY\nsource-venv/bin/python current_task.py"
    steps.append(
        run_step(
            root,
            "07-run-current-source-task",
            "run documented Sirus first-use task",
            command,
            cwd=workspace,
            timeout=600,
        )
    )
    steps.append(
        run_step(
            root,
            "08-capture-package-versions",
            "capture package versions",
            "published-venv/bin/python -m pip freeze || true; "
            "echo '--- current source ---'; source-venv/bin/python -m pip freeze || true",
            cwd=workspace,
            timeout=60,
        )
    )

    published_install_succeeded = steps[3].return_code == 0
    current_source_succeeded = steps[5].return_code == 0 and steps[6].return_code == 0
    payload: dict[str, Any] = {
        "repository": "artefactory/woodtapper",
        "default_branch_commit": commit,
        "readme_blob_sha": "b07652102469791d6b0c1ecab597a849a9aa31ae",
        "package_metadata_blob_sha": "13ecb5be9c59a16735351bd57d8072fc7a518b6c",
        "purpose": (
            "Maintainer-intervention eligibility recheck; not part of the locked 10-case "
            "primary result."
        ),
        "published_install_succeeded": published_install_succeeded,
        "current_default_branch_source_succeeded": current_source_succeeded,
        "readme_contains_binary_compatibility_warning": True,
        "package_metadata_pins_scikit_learn": "==1.6.1",
        "candidate_intervention": bool(
            not published_install_succeeded and not current_source_succeeded
        ),
        "reason": (
            "Contact is potentially warranted only if both the documented published install "
            "and the current default branch remain broken. If current source succeeds, the "
            "problem is already addressed upstream and release timing is not treated as a new "
            "defect."
        ),
        "steps": [asdict(step) for step in steps],
    }
    finish_result(root, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    summary = {
        "generated_at": utc_now(),
        "sklearn_migrator": sklearn_correction(output),
        "boost_geometry": boost_correction(output),
        "woodtapper_current_recheck": woodtapper_recheck(output),
    }
    (output / "closeout-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_hashes(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
