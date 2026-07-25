#!/usr/bin/env python3
"""Write the pre-execution lock for the issue-121 dynamic task subset."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

STATIC_RESULT_SHA256 = "400c404de5338cff630f6147f18288b5b557341a6fb11d3da56b956c13b5f316"

CASES: list[dict[str, Any]] = [
    {
        "case_id": "D01-himap",
        "order": 1,
        "repository": "GroupiSP/himap",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "910c0bdfb8a9f4968110e6cac13a450573d6f4da",
        "ecosystem": "Python/Cython CLI",
        "predicted_strict_ready": False,
        "reference_strict_ready": True,
        "predicted_hard_findings": [],
        "strata": ["strict_false_negative", "python", "compiled_extension", "cli"],
        "documentation_scope": ["root_readme"],
        "predeclared_task": (
            "Install the published HiMAP package and run the documented Monte Carlo "
            "demonstration with `python -m himap.main --mc_sampling True`."
        ),
        "success_criterion": (
            "Command exits 0 and produces an observable model/result artifact or documented "
            "completion output."
        ),
        "timeout_seconds": 420,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 15, "disk_gib": 10},
        "safety_review": (
            "Isolated GitHub-hosted runner; no credentials; no sudo; public PyPI package; "
            "documented module invocation."
        ),
    },
    {
        "case_id": "D02-hlafreq",
        "order": 9,
        "repository": "BarinthusBio/HLAfreq",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "3525159e744286f3007d174bd80217d6963e5dd2",
        "ecosystem": "Python library with external data service",
        "predicted_strict_ready": False,
        "reference_strict_ready": True,
        "predicted_hard_findings": [],
        "strata": ["strict_false_negative", "python", "library", "external_service"],
        "documentation_scope": ["root_readme"],
        "predeclared_task": (
            "Install HLAfreq with pip, execute the documented Uganda locus-A minimal download, "
            "filter it, reduce resolution, and combine allele frequencies."
        ),
        "success_criterion": (
            "Commands exit 0 and return a non-empty combined allele-frequency result."
        ),
        "timeout_seconds": 300,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 15, "disk_gib": 10},
        "safety_review": (
            "Isolated runner; GET-style public data retrieval only; no credentials; no local "
            "privilege escalation."
        ),
    },
    {
        "case_id": "D03-woodtapper",
        "order": 17,
        "repository": "artefactory/woodtapper",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "b07652102469791d6b0c1ecab597a849a9aa31ae",
        "ecosystem": "Python/C++ library",
        "predicted_strict_ready": True,
        "reference_strict_ready": True,
        "predicted_hard_findings": [],
        "strata": ["true_positive", "python", "compiled_extension", "library"],
        "documentation_scope": ["root_readme"],
        "predeclared_task": (
            "Install WoodTapper, create a deterministic scikit-learn classification split, fit "
            "the documented SirusClassifier API, make predictions, and extract rules."
        ),
        "success_criterion": (
            "Commands exit 0, prediction length matches the test set, and at least one model or "
            "rule output is observable."
        ),
        "timeout_seconds": 420,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 15, "disk_gib": 10},
        "safety_review": (
            "Isolated runner; public PyPI packages; deterministic bundled sklearn data; no "
            "network after installation."
        ),
    },
    {
        "case_id": "D04-multimodars",
        "order": 21,
        "repository": "yungselm/multimoda-rs",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "e800131c61b0278714977389d92dd6999dbbd52f",
        "ecosystem": "Rust-powered Python library",
        "predicted_strict_ready": True,
        "reference_strict_ready": True,
        "predicted_hard_findings": [],
        "strata": ["true_positive", "python", "rust", "library"],
        "documentation_scope": ["root_readme", "bundled_example_data"],
        "predeclared_task": (
            "Install multimodars and execute the documented quick-example intravascular alignment "
            "against bundled example data, writing output to a temporary directory."
        ),
        "success_criterion": (
            "The documented API returns aligned objects without exception and writes at least one "
            "output artifact."
        ),
        "timeout_seconds": 420,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 15, "disk_gib": 10},
        "safety_review": (
            "Isolated runner; reviewed Python call; bundled public example data; output restricted "
            "to temporary workspace."
        ),
    },
    {
        "case_id": "D05-cowfootr",
        "order": 22,
        "repository": "juanmarcosmoreno-arch/cowfootR",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "c1ed625b365128550d66a7997c9ad6d624df3459",
        "ecosystem": "R/C library",
        "predicted_strict_ready": False,
        "reference_strict_ready": True,
        "predicted_hard_findings": [],
        "strata": ["strict_false_negative", "r", "compiled_extension", "library"],
        "documentation_scope": ["root_readme"],
        "predeclared_task": (
            "Install cowfootR from CRAN and run the documented single-farm quick-start calculations "
            "through total emissions and milk intensity."
        ),
        "success_criterion": (
            "R exits 0 and returns positive total-emissions and milk-intensity values."
        ),
        "timeout_seconds": 480,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 18, "disk_gib": 10},
        "safety_review": (
            "Isolated runner; CRAN package installation; deterministic numeric inputs; no "
            "credentials or external user data."
        ),
    },
    {
        "case_id": "D06-kigali",
        "order": 24,
        "repository": "SchmidtDSE/kigali-sim",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "ee0bd1e3b319d22db49e5016a8da4ab8040e38b4",
        "ecosystem": "Java CLI and JavaScript editor",
        "predicted_strict_ready": True,
        "reference_strict_ready": True,
        "predicted_hard_findings": [],
        "strata": ["true_positive", "java", "javascript", "cli", "web_build"],
        "documentation_scope": ["root_readme", "reviewed_editor_package_manifest"],
        "predeclared_task": (
            "Download the official Kigali Sim jar, run the documented Business-as-Usual "
            "QubecTalk simulation to CSV, then clone the matching repository and build the editor "
            "with its locked pnpm toolchain."
        ),
        "success_criterion": (
            "Java simulation exits 0 with a non-empty CSV; JavaScript build result is recorded "
            "separately and exits 0 for full case success."
        ),
        "timeout_seconds": 600,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 20, "disk_gib": 12},
        "safety_review": (
            "Ephemeral runner; official project jar; reviewed DSL; reviewed editor package.json "
            "and lockfile; no secrets; no remote shell piping."
        ),
    },
    {
        "case_id": "D07-gapflow",
        "order": 26,
        "repository": "hannes-holey/GaPFlow",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "45a5189c6849472e032a999b8cf7e97b08a0ef3c",
        "ecosystem": "Python/C++ scientific CLI",
        "predicted_strict_ready": False,
        "reference_strict_ready": True,
        "predicted_hard_findings": [],
        "strata": ["strict_false_negative", "python", "compiled_scientific", "cli"],
        "documentation_scope": ["root_readme"],
        "predeclared_task": (
            "Install GaPFlow, create the README's fixed-law journal-bearing YAML, run `python -m "
            "GaPFlow -i my_input_file.yaml`, and inspect documented output files."
        ),
        "success_criterion": (
            "Command exits 0 and creates config.yml, topo.nc, sol.nc, or history.csv under the "
            "configured output directory."
        ),
        "timeout_seconds": 600,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 20, "disk_gib": 12},
        "safety_review": (
            "Isolated runner; fixed-form example avoids MD/GP external data; no MPI production "
            "build; bounded simulation timeout."
        ),
    },
    {
        "case_id": "D08-sklearn-migrator",
        "order": 33,
        "repository": "anvaldes/sklearn-migrator",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "36a51525a013eb98b635f0ce8b2b3db1ae2a7bb4",
        "ecosystem": "Python library",
        "predicted_strict_ready": False,
        "reference_strict_ready": True,
        "predicted_hard_findings": [
            "missing_relative_path:input_model/all_data.json",
            "missing_relative_path:input_model/y_pred.csv",
            "missing_relative_path:output_model/y_pred_new.csv",
        ],
        "strata": [
            "strict_false_negative",
            "hard_finding_false_positive_candidate",
            "python",
            "library",
        ],
        "documentation_scope": ["root_readme"],
        "predeclared_task": (
            "Install sklearn-migrator, train and serialize a deterministic RandomForestRegressor, "
            "deserialize it in the same environment, compare predictions, and separately create "
            "the README-directed input_model/output_model runtime directories."
        ),
        "success_criterion": (
            "Round-trip prediction maximum absolute difference is below 1e-8 and runtime path "
            "creation succeeds without requiring upstream repository assets."
        ),
        "timeout_seconds": 360,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 15, "disk_gib": 10},
        "safety_review": (
            "Isolated runner; synthetic sklearn data; no pickle ingestion; generated JSON only; "
            "explicitly tests the predicted path semantics."
        ),
    },
    {
        "case_id": "D09-boost-geometry",
        "order": 34,
        "repository": "boostorg/geometry",
        "default_branch": "master",
        "readme_path": "README.md",
        "readme_sha": "6f898496335b9a0bf64def628d2ff63852af89bf",
        "ecosystem": "C++ header-only library",
        "predicted_strict_ready": False,
        "reference_strict_ready": False,
        "predicted_hard_findings": [],
        "strata": ["true_negative", "external_documentation_delegation", "cpp", "library"],
        "documentation_scope": [
            "root_readme",
            "official_linked_documentation",
            "repository_example",
        ],
        "predeclared_task": (
            "Follow the root README's documentation/example delegation, compile a minimal "
            "Boost.Geometry polygon-area program against the cloned header-only "
            "library, and run it."
        ),
        "success_criterion": (
            "C++14 compilation exits 0 and the executable reports polygon area 1 within numeric "
            "tolerance."
        ),
        "timeout_seconds": 300,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 12, "disk_gib": 10},
        "safety_review": (
            "Isolated runner; header-only public source; compiler invocation only; no package "
            "scripts or elevated privileges."
        ),
    },
    {
        "case_id": "D10-ecodive",
        "order": 37,
        "repository": "cmmr/ecodive",
        "default_branch": "main",
        "readme_path": "README.md",
        "readme_sha": "aba4ddfd2fc0fbfc0d4df5de10a7d94f7bc0",
        "ecosystem": "R/C library",
        "predicted_strict_ready": False,
        "reference_strict_ready": True,
        "predicted_hard_findings": [],
        "strata": ["strict_false_negative", "r", "compiled_extension", "library"],
        "documentation_scope": ["root_readme"],
        "predeclared_task": (
            "Install ecodive from CRAN and run the README's basic-object workflow using ex_counts, "
            "rarefy, shannon, faith, bray, and weighted_unifrac."
        ),
        "success_criterion": (
            "R exits 0 and returns the documented-size alpha/beta diversity results without "
            "external study data."
        ),
        "timeout_seconds": 480,
        "resource_caps": {"runner": "ubuntu-latest", "job_minutes": 18, "disk_gib": 10},
        "safety_review": (
            "Isolated runner; CRAN package; bundled example objects; no external personal or "
            "restricted data."
        ),
    },
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_manifest() -> dict[str, Any]:
    return {
        "study": "joss-issue-121-dynamic-first-use-validation",
        "status": "LOCKED_BEFORE_EXECUTION",
        "locked_after_static_result_sha256": STATIC_RESULT_SHA256,
        "selection_policy": (
            "Ten feasibility-screened cases fixed before execution; no outcome-driven replacement."
        ),
        "selected_count": len(CASES),
        "cases": CASES,
        "interpretation_rules": {
            "success": "Predeclared task and observable success criterion both met within cap.",
            "failure": (
                "Safe execution completed but the criterion was not met because of documented-path, "
                "compatibility, dependency, or runtime failure."
            ),
            "untestable_here": (
                "Safety, platform, restricted-data, GPU/HPC, or resource constraints prevent a "
                "valid attempt; not counted as project failure."
            ),
            "static_finding_direct_blocker": (
                "The exact frozen finding prevents the task and correction or bypass changes the outcome."
            ),
            "material_friction": (
                "The documented path requires a non-obvious correction, search, or documentation "
                "transition that materially changes completion."
            ),
            "external_docs_supplemented": (
                "Root README delegation is followed and supplies missing operational detail."
            ),
            "no_outcome_replacement": True,
        },
        "environment_policy": {
            "execution": "ephemeral GitHub-hosted Ubuntu runners",
            "no_secrets": True,
            "no_sudo": True,
            "network": (
                "public package registries, official project assets, and public repositories only"
            ),
            "logs": (
                "exact commands, exit codes, stdout/stderr, durations, disk use, and installed versions"
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("data/issue-121/dynamic-tests"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    manifest_text = canonical_json(manifest)
    manifest_sha = sha256_text(manifest_text)
    manifest_path = args.output_dir / "case-manifest.json"
    lock_path = args.output_dir / "DYNAMIC_LOCK.json"
    manifest_path.write_text(manifest_text, encoding="utf-8")
    lock = {
        "status": "LOCKED_BEFORE_EXECUTION",
        "manifest_sha256": manifest_sha,
        "static_result_sha256": STATIC_RESULT_SHA256,
        "selected_count": len(CASES),
        "execution_results_present_when_locked": False,
        "source_commit_before_lock": os.environ.get("SOURCE_COMMIT"),
    }
    lock_path.write_text(canonical_json(lock), encoding="utf-8")
    print(manifest_sha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
