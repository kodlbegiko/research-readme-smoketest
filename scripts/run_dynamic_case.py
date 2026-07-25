#!/usr/bin/env python3
"""Execute one pre-locked first-use case on an ephemeral runner."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import textwrap
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

MAX_LOG_CHARS = 8000
MEMORY_RE = re.compile(r"Maximum resident set size \(kbytes\):\s*(\d+)")


@dataclass(frozen=True)
class StepSpec:
    name: str
    phase: str
    command: str
    timeout_seconds: int
    required: bool = True


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def short_log(value: str) -> str:
    if len(value) <= MAX_LOG_CHARS:
        return value
    return value[: MAX_LOG_CHARS // 2] + "\n...[truncated]...\n" + value[-MAX_LOG_CHARS // 2 :]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


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
    try:
        completed = subprocess.run(
            timed_command,
            cwd=workspace,
            env=environment,
            text=True,
            capture_output=True,
            timeout=spec.timeout_seconds,
            check=False,
        )
        return_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        return_code = 124
        stdout = error.stdout if isinstance(error.stdout, str) else ""
        stderr = error.stderr if isinstance(error.stderr, str) else ""
        stderr += f"\nTIMEOUT after {spec.timeout_seconds} seconds\n"
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


def common_steps(case: dict[str, Any]) -> list[StepSpec]:
    repository = case["repository"]
    branch = case["default_branch"]
    readme_path = case["readme_path"]
    readme_sha = case["readme_sha"]
    return [
        StepSpec(
            "clone repository",
            "acquisition",
            (
                f"git clone --depth 1 --branch {branch} "
                f"https://github.com/{repository}.git source"
            ),
            180,
        ),
        StepSpec(
            "verify README blob",
            "acquisition",
            (
                f'test "$(git -C source hash-object {readme_path})" = "{readme_sha}"'
            ),
            30,
        ),
    ]


def python_venv_steps(package: str, timeout: int = 300) -> list[StepSpec]:
    return [
        StepSpec("create virtual environment", "installation", "python -m venv venv", 90),
        StepSpec(
            "upgrade pip",
            "installation",
            "venv/bin/python -m pip install --upgrade pip",
            120,
        ),
        StepSpec(
            f"install {package}",
            "installation",
            f"venv/bin/python -m pip install {package}",
            timeout,
        ),
    ]


def himap_steps() -> list[StepSpec]:
    return python_venv_steps("himap", 360) + [
        StepSpec(
            "run HiMAP Monte Carlo example",
            "task",
            textwrap.dedent(
                """
                mkdir -p task
                cd task
                ../venv/bin/python -m himap.main --mc_sampling True
                find . ../venv -type f \
                  \( -path '*/results/*' -o -name '*.csv' -o -name '*.png' \) \
                  -print | head -n 20
                """
            ).strip(),
            420,
        ),
        StepSpec(
            "capture Python packages",
            "environment",
            "venv/bin/python -m pip freeze",
            60,
            False,
        ),
    ]


def hlafreq_steps() -> list[StepSpec]:
    script = textwrap.dedent(
        """
        import HLAfreq

        base_url = HLAfreq.makeURL("Uganda", locus="A")
        aftab = HLAfreq.getAFdata(base_url)
        assert len(aftab) > 0
        aftab = HLAfreq.only_complete(aftab)
        aftab = HLAfreq.decrease_resolution(aftab, 2)
        caf = HLAfreq.combineAF(aftab)
        assert len(caf) > 0
        print(caf.head().to_string())
        print({"downloaded_rows": len(aftab), "combined_rows": len(caf)})
        """
    ).strip()
    return python_venv_steps("HLAfreq", 420) + [
        StepSpec(
            "run HLAfreq Uganda example",
            "task",
            f"venv/bin/python - <<'PY'\n{script}\nPY",
            300,
        ),
        StepSpec(
            "capture Python packages",
            "environment",
            "venv/bin/python -m pip freeze",
            60,
            False,
        ),
    ]


def woodtapper_steps() -> list[StepSpec]:
    script = textwrap.dedent(
        """
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from sklearn.datasets import load_breast_cancer
        from sklearn.model_selection import train_test_split
        from woodtapper import SirusClassifier, show_rules

        X, y = load_breast_cancer(return_X_y=True)
        X_train, X_test, y_train, _ = train_test_split(
            X, y, test_size=0.2, random_state=0, stratify=y
        )
        model = SirusClassifier(
            n_estimators=1000,
            max_depth=2,
            quantile=10,
            p0=0.01,
            random_state=0,
        )
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
        show_rules(model, max_rules=10)
        plt.savefig("woodtapper-rules.png", dpi=100)
        assert __import__("pathlib").Path("woodtapper-rules.png").stat().st_size > 0
        print({"predictions": len(predictions), "figure": "woodtapper-rules.png"})
        """
    ).strip()
    return python_venv_steps("woodtapper", 420) + [
        StepSpec(
            "run WoodTapper classifier example",
            "task",
            f"venv/bin/python - <<'PY'\n{script}\nPY",
            420,
        ),
        StepSpec(
            "capture Python packages",
            "environment",
            "venv/bin/python -m pip freeze",
            60,
            False,
        ),
    ]


def multimodars_steps() -> list[StepSpec]:
    script = textwrap.dedent(
        """
        import pathlib
        import multimodars as mm
        import numpy as np

        rest, stress, dia, sys, _ = mm.from_file_full(
            "source/examples/data/ivus_rest",
            "source/examples/data/ivus_stress",
            write_obj=True,
            output_path_ab="output/rest",
            output_path_cd="output/stress",
            output_path_ac="output/diastole",
            output_path_bd="output/systole",
        )
        cl_raw = np.genfromtxt(
            "source/examples/data/centerline_raw.csv",
            delimiter=",",
        )
        centerline = mm.numpy_to_centerline(cl_raw)
        aligned_pair, cl_resampled = mm.align_three_point(
            centerline,
            rest,
            main_ref_pt=(12.2605, -201.3643, 1751.0554),
            counterclockwise_ref_pt=(11.7567, -202.1920, 1754.7975),
            clockwise_ref_pt=(15.6605, -202.1920, 1749.9655),
            write=True,
            output_dir="output/aligned",
        )
        assert all(value is not None for value in (stress, dia, sys, aligned_pair))
        assert cl_resampled is not None
        artifacts = [path for path in pathlib.Path("output").rglob("*") if path.is_file()]
        assert artifacts
        print({"artifact_count": len(artifacts), "first": str(artifacts[0])})
        """
    ).strip()
    return python_venv_steps("multimodars", 420) + [
        StepSpec(
            "run multimodars quick example",
            "task",
            f"venv/bin/python - <<'PY'\n{script}\nPY",
            420,
        ),
        StepSpec(
            "capture Python packages",
            "environment",
            "venv/bin/python -m pip freeze",
            60,
            False,
        ),
    ]


def cowfoot_steps() -> list[StepSpec]:
    script = textwrap.dedent(
        """
        options(repos = c(CRAN = "https://cloud.r-project.org"))
        install.packages("cowfootR")
        library(cowfootR)
        boundaries <- set_system_boundaries("farm_gate")
        enteric <- calc_emissions_enteric(
          n_animals = 100,
          cattle_category = "dairy_cows",
          boundaries = boundaries
        )
        manure <- calc_emissions_manure(n_cows = 100, boundaries = boundaries)
        soil <- calc_emissions_soil(
          n_fertilizer_synthetic = 1500,
          n_excreta_pasture = 5000,
          area_ha = 120,
          boundaries = boundaries
        )
        energy <- calc_emissions_energy(
          diesel_l = 2000,
          electricity_kwh = 5000,
          boundaries = boundaries
        )
        inputs <- calc_emissions_inputs(
          conc_kg = 1000,
          fert_n_kg = 500,
          boundaries = boundaries
        )
        total_emissions <- calc_total_emissions(
          enteric, manure, soil, energy, inputs
        )
        milk_intensity <- calc_intensity_litre(
          total_emissions = total_emissions,
          milk_litres = 750000,
          fat = 4.0,
          protein = 3.3
        )
        rendered <- c(
          capture.output(print(total_emissions)),
          capture.output(print(milk_intensity))
        )
        stopifnot(any(grepl("Total CO2eq", rendered)))
        stopifnot(any(grepl("Intensity", rendered)))
        cat(rendered, sep = "\n")
        cat("\nversion=", as.character(packageVersion("cowfootR")), "\n")
        """
    ).strip()
    return [
        StepSpec(
            "install and run cowfootR quick start",
            "task",
            f"Rscript - <<'RS'\n{script}\nRS",
            480,
        ),
        StepSpec("capture R environment", "environment", "Rscript -e 'sessionInfo()'", 60, False),
    ]


def kigali_steps() -> list[StepSpec]:
    qta = textwrap.dedent(
        """
        start default
          define application "Commercial Refrigeration"
            uses substance "HFC-134a"
              enable domestic
              initial charge with 1 kg / unit for domestic
              initial charge with 0 kg / unit for import
              initial charge with 0 kg / unit for export
              equals 1430 kgCO2e / kg
              equals 1 kwh / unit
              set sales to 1 mt during year 1
              retire 5 % / year
              recharge 5 % with 0.85 kg / unit
            end substance
            uses substance "R-600a"
              enable domestic
              initial charge with 1 kg / unit for domestic
              initial charge with 0 kg / unit for import
              initial charge with 0 kg / unit for export
              equals 3 kgCO2e / kg
              equals 1 kwh / unit
              set sales to 1 kg during year 1
              retire 5 % / year
              recharge 5 % with 0.85 kg / unit
            end substance
          end application
        end default
        start policy "Permit"
          modify application "Commercial Refrigeration"
            modify substance "HFC-134a"
              cap sales to 80 % displacing "R-600a" during years 3 to 10
            end substance
          end application
        end policy
        start simulations
          simulate "Business as Usual"
          from years 1 to 10
          simulate "With Permit"
            using "Permit"
          from years 1 to 10
        end simulations
        """
    ).strip()
    write_qta = f"cat > script.qta <<'QTA'\n{qta}\nQTA"
    return [
        StepSpec(
            "download official Kigali Sim jar",
            "installation",
            "curl --fail --location --retry 3 "
            "https://kigalisim.org/kigalisim-fat.jar -o kigalisim-fat.jar",
            180,
        ),
        StepSpec("write documented QubecTalk example", "task", write_qta, 30),
        StepSpec(
            "run Kigali Sim Java CLI",
            "task",
            "java -jar kigalisim-fat.jar run -o output.csv script.qta && test -s output.csv",
            420,
        ),
        StepSpec(
            "build Kigali Sim JavaScript editor",
            "task",
            textwrap.dedent(
                """
                corepack enable
                corepack prepare pnpm@10.20.0 --activate
                cd source/editor
                pnpm install --frozen-lockfile
                pnpm run build
                """
            ).strip(),
            600,
        ),
        StepSpec(
            "capture JavaScript and Java versions",
            "environment",
            "java -version; node --version; pnpm --version; sha256sum kigalisim-fat.jar",
            60,
            False,
        ),
    ]


def gapflow_steps() -> list[StepSpec]:
    yaml = textwrap.dedent(
        """
        options:
            output: data/journal
            write_freq: 10
        grid:
            dx: 1.e-5
            dy: 1.
            Nx: 100
            Ny: 1
            xE: ['D', 'N', 'N']
            xW: ['D', 'N', 'N']
            yS: ['P', 'P', 'P']
            yN: ['P', 'P', 'P']
            xE_D: 877.7007
            xW_D: 877.7007
        geometry:
            type: journal
            CR: 1.e-2
            eps: 0.7
            U: 0.1
            V: 0.
        numerics:
            tol: 1e-9
            dt: 1e-10
            max_it: 200
        properties:
            shear: 0.0794
            bulk: 0.
            EOS: DH
            P0: 101325
            rho0: 877.7007
            T0: 323.15
            C1: 3.5e10
            C2: 1.23
        """
    ).strip()
    write_yaml = f"cat > my_input_file.yaml <<'YAML'\n{yaml}\nYAML"
    return python_venv_steps("GaPFlow", 600) + [
        StepSpec("write GaPFlow YAML", "task", write_yaml, 30),
        StepSpec(
            "run GaPFlow minimal simulation",
            "task",
            textwrap.dedent(
                """
                venv/bin/python -m GaPFlow -i my_input_file.yaml
                test -d data/journal
                find data/journal -maxdepth 1 -type f -print
                test -n "$(find data/journal -maxdepth 1 -type f -print -quit)"
                """
            ).strip(),
            600,
        ),
        StepSpec(
            "capture GaPFlow environment",
            "environment",
            "venv/bin/gpf_info || true; venv/bin/python -m pip freeze",
            90,
            False,
        ),
    ]


def sklearn_migrator_steps() -> list[StepSpec]:
    script = textwrap.dedent(
        """
        import json
        from pathlib import Path

        import numpy as np
        from sklearn.datasets import make_regression
        from sklearn.ensemble import RandomForestRegressor
        from sklearn_migrator.ensemble import (
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
        serialized = serialize_random_forest_reg(model)
        (input_dir / "all_data.json").write_text(json.dumps(serialized))
        np.savetxt(input_dir / "y_pred.csv", expected, delimiter=",")
        restored = deserialize_random_forest_reg(serialized)
        observed = restored.predict(X[:20])
        np.savetxt(output_dir / "y_pred_new.csv", observed, delimiter=",")
        max_difference = float(np.max(np.abs(expected - observed)))
        assert max_difference < 1e-8
        assert (input_dir / "all_data.json").is_file()
        assert (output_dir / "y_pred_new.csv").is_file()
        print({"max_abs_difference": max_difference})
        """
    ).strip()
    return python_venv_steps("sklearn-migrator", 360) + [
        StepSpec(
            "run sklearn-migrator round trip",
            "task",
            f"venv/bin/python - <<'PY'\n{script}\nPY",
            360,
        ),
        StepSpec(
            "capture Python packages",
            "environment",
            "venv/bin/python -m pip freeze",
            60,
            False,
        ),
    ]


def boost_steps() -> list[StepSpec]:
    source = textwrap.dedent(
        """
        #include <cmath>
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
          std::cout << area << "\\n";
          return std::abs(area - 1.0) < 1e-12 ? 0 : 1;
        }
        """
    ).strip()
    write_source = f"cat > boost_geometry_example.cpp <<'CPP'\n{source}\nCPP"
    return [
        StepSpec("write Boost.Geometry example", "task", write_source, 30),
        StepSpec(
            "compile Boost.Geometry example",
            "task",
            "g++ -std=c++14 -O2 -Isource/include boost_geometry_example.cpp -o boost-example",
            180,
        ),
        StepSpec("run Boost.Geometry example", "task", "./boost-example", 30),
        StepSpec("capture compiler version", "environment", "g++ --version", 30, False),
    ]


def ecodive_steps() -> list[StepSpec]:
    script = textwrap.dedent(
        """
        options(repos = c(CRAN = "https://cloud.r-project.org"))
        install.packages("ecodive")
        library(ecodive)
        counts <- rarefy(ex_counts)
        alpha <- shannon(counts)
        phylo_alpha <- faith(counts, tree = ex_tree)
        beta <- bray(counts)
        phylo_beta <- weighted_unifrac(counts, tree = ex_tree)
        stopifnot(length(alpha) == 4)
        stopifnot(length(phylo_alpha) == 4)
        stopifnot(nrow(as.matrix(beta)) == 4)
        stopifnot(nrow(as.matrix(phylo_beta)) == 4)
        print(alpha)
        print(phylo_alpha)
        print(as.matrix(beta))
        cat("version=", as.character(packageVersion("ecodive")), "\n")
        """
    ).strip()
    return [
        StepSpec(
            "install and run ecodive basic workflow",
            "task",
            f"Rscript - <<'RS'\n{script}\nRS",
            480,
        ),
        StepSpec("capture R environment", "environment", "Rscript -e 'sessionInfo()'", 60, False),
    ]


CASE_STEPS = {
    "D01-himap": himap_steps,
    "D02-hlafreq": hlafreq_steps,
    "D03-woodtapper": woodtapper_steps,
    "D04-multimodars": multimodars_steps,
    "D05-cowfootr": cowfoot_steps,
    "D06-kigali": kigali_steps,
    "D07-gapflow": gapflow_steps,
    "D08-sklearn-migrator": sklearn_migrator_steps,
    "D09-boost-geometry": boost_steps,
    "D10-ecodive": ecodive_steps,
}


def directory_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def preliminary_relations(case: dict[str, Any], status: str) -> dict[str, Any]:
    success = status == "SUCCESS"
    return {
        "strict_false_negative_completed": bool(
            success
            and not case["predicted_strict_ready"]
            and case["reference_strict_ready"]
        ),
        "external_docs_supplemented": bool(
            success and "external_documentation_delegation" in case["strata"]
        ),
        "predicted_hard_findings_disproved_by_runtime_paths": bool(
            success and case["case_id"] == "D08-sklearn-migrator"
        ),
        "manual_friction_classification_required": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id", required=True, choices=sorted(CASE_STEPS))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/issue-121/dynamic-tests/case-manifest.json"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = read_json(args.manifest)
    case = next(item for item in manifest["cases"] if item["case_id"] == args.case_id)
    output_dir = args.output_dir.resolve()
    logs_dir = output_dir / "logs"
    workspace = output_dir / "workspace"
    output_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir()
    environment = dict(os.environ)
    environment.update(
        {
            "GIT_TERMINAL_PROMPT": "0",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PYTHONHASHSEED": "0",
            "MPLBACKEND": "Agg",
        }
    )
    started_at = utc_now()
    started = time.perf_counter()
    steps = common_steps(case) + CASE_STEPS[args.case_id]()
    results: list[dict[str, Any]] = []
    status = "SUCCESS"
    failure_reason: str | None = None
    for index, spec in enumerate(steps, start=1):
        result = run_step(spec, workspace, logs_dir, index, environment)
        results.append(result)
        if spec.required and result["return_code"] != 0:
            if result["timed_out"]:
                status = "UNTESTABLE_HERE"
                failure_reason = f"Resource/time cap reached at step: {spec.name}"
            elif spec.name == "verify README blob":
                status = "UNTESTABLE_HERE"
                failure_reason = "Root README changed after acquisition; frozen task not executed."
            else:
                status = "FAILURE"
                failure_reason = f"Required step failed: {spec.name}"
            break
    completed_at = utc_now()
    total_seconds = time.perf_counter() - started
    required_results = [result for result in results if result["required"]]
    installation_seconds = sum(
        result["duration_seconds"]
        for result in required_results
        if result["phase"] in {"acquisition", "installation"}
    )
    task_seconds = sum(
        result["duration_seconds"]
        for result in required_results
        if result["phase"] == "task"
    )
    result_document = {
        "case": case,
        "status": status,
        "failure_reason": failure_reason,
        "started_at": started_at,
        "completed_at": completed_at,
        "total_seconds_to_first_output": total_seconds if status == "SUCCESS" else None,
        "attempt_duration_seconds": total_seconds,
        "installation_seconds": installation_seconds,
        "task_seconds": task_seconds,
        "manual_command_steps": len(required_results),
        "external_searches": 0,
        "non_root_document_pages": len(case["documentation_scope"]) - 1,
        "runner": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_job": os.environ.get("GITHUB_JOB"),
        },
        "steps": results,
        "workspace_bytes": directory_size(workspace),
        "preliminary_relations": preliminary_relations(case, status),
        "interpretation_note": (
            "Raw execution result only. Friction/blocker classification requires post-run "
            "review and cannot change the locked case or command."
        ),
    }
    (output_dir / "result.json").write_text(canonical_json(result_document), encoding="utf-8")
    print(canonical_json(result_document), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
