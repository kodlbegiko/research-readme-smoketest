# Research README Smoketest

> **Research status:** negative external-validation result  
> **Productization:** not supported  
> **GitHub Action:** not planned  
> **Repository role:** reproducible research archive and independent-replication entry point

The frozen v0.1.0 detector should **not** be adopted as a general README checker. Its preregistered issue-121 external validation failed the required accuracy and hard-finding precision gates, and its static findings did not predict observed first-use blockers.

## Final decisions

| Decision | Verdict |
|---|---|
| Detector out-of-sample validity | `NOT SUPPORTED` |
| Static findings' predictive value for first-use friction | `NOT SUPPORTED` |
| Maintainer intervention actual value | `INCONCLUSIVE` |
| Overall productization | `NOT SUPPORTED` |

There will be no GitHub Action v0.2 and no retuning on JOSS issue 121. A future detector can only be evaluated in a new preregistered study with a newly frozen version, new out-of-sample data, independent human reference annotation, and preserved raw evidence.

## Start here

- [`EXTERNAL-VALIDATION.md`](EXTERNAL-VALIDATION.md) — complete negative-result closeout
- [`REPLICATION.md`](REPLICATION.md) — independent replication entry point
- [`PUBLIC-INTEREST.md`](PUBLIC-INTEREST.md) — evidence ladder and current zero-impact baseline
- [`docs/public-summary.md`](docs/public-summary.md) — plain-language English summary
- [`docs/archival-plan.md`](docs/archival-plan.md) — long-term preservation and DOI status
- [`results/issue-121/dynamic-validation-results.json`](results/issue-121/dynamic-validation-results.json) — machine-readable dynamic result
- [`results/issue-121/DYNAMIC-FINAL-SHA256SUMS`](results/issue-121/DYNAMIC-FINAL-SHA256SUMS) — final evidence checksums

## External-validation result

JOSS issue 121 contained 39 papers. Thirty-eight linked GitHub repositories were eligible and one GitLab repository was excluded under the preregistered rule.

| Static result | Value |
|---|---:|
| Detector strict-ready | 7 / 38 |
| Human reference strict-ready | 24 / 38 |
| TP / FP / TN / FN | 7 / 0 / 14 / 17 |
| Precision | 1.000 |
| Recall | 0.292 |
| Specificity | 1.000 |
| Accuracy | 0.553 |
| F1 | 0.452 |
| Preregistered accuracy gate | 0.750 |

High precision did not compensate for missing 17 of 24 reference-ready repositories. The three predicted sklearn-migrator hard findings were false positives and were marked `DISPROVED` after a documented correction rerun.

## Dynamic validation

Ten cases were locked before execution. The original attempts remain unchanged.

Raw results:

```text
SUCCESS: 4
FAILURE: 5
UNTESTABLE_HERE: 1
```

Final adjudication:

```text
SUCCESS: 6
SUCCESS_WITH_FRICTION: 2
FAILURE_DEPENDENCY_COMPATIBILITY: 1
UNTESTABLE_HERE: 1
FAILURE_README_BLOCKER: 0
FAILURE_OTHER: 0
```

Eight of nine testable cases completed the first meaningful task. None of the three predicted hard findings became a blocker. Adjudication separated harness errors, dependency compatibility, optional components, and official external-document delegation from direct README defects.

The ten-case sample was feasibility-selected and does not support population inference.

## Research-integrity controls

The repository preserves:

- detector and protocol freeze before reference annotation;
- prediction files and a verified prediction lock;
- immutable commit pinning for future acquisition and path checks;
- raw dynamic attempts separate from adjudications and corrections;
- process-group termination for timed commands;
- explicit component and blocker classification;
- read-only PR validation workflows;
- final SHA-256 manifests;
- deterministic result checks under different `PYTHONHASHSEED` values.

Historical issue-121 acquisition preserved README blob SHAs but did not cryptographically pin every cross-request path check to one repository commit. Future acquisition is hardened; frozen historical outputs are not rewritten.

## Reproduce

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest
pytest --cov
python -m build
sha256sum -c results/issue-121/DYNAMIC-FINAL-SHA256SUMS
```

See `REPLICATION.md` for frozen static reproduction, dynamic-evidence review, and requirements for a genuinely new out-of-sample study.

## Public-interest status

At closeout:

```text
independent reproductions: 0
independent human re-annotations: 0
external citations: 0
accepted upstream corrections: 0
measured user-benefit outcomes: 0
```

Internal CI, GitHub activity, issue submission, downloads, and AI-generated review are not counted as external impact.

## Historical pilot

The repository began with an exploratory pilot on the first 20 papers in JOSS issue 122. That development-sample result appeared favorable but was not an out-of-sample validation. The issue-121 study was intentionally designed to test whether the detector generalized; it did not meet the required gates.

The frozen pilot remains reproducible for research history:

```bash
PYTHONHASHSEED=0 readme-smoketest pilot --output-dir reproduced-results
```

Expected SHA-256 for `reproduced-results/pilot-results.json`:

```text
531f145706238996c499746bdb46c9f4d281221828b4f07691c68782ca2f80f8
```

Do not use the pilot headline as evidence that the detector is generally valid.

## Repository map

- `data/issue-121/` — frozen acquisition, predictions, annotations, dynamic locks, raw attempts, and adjudications
- `results/issue-121/` — static and dynamic machine-readable results and checksums
- `results/interventions/` — maintainer-intervention decisions and evidence
- `results/public-interest/` — external outcome log, initially all zero
- `docs/independent-replication-protocol.md` — new-study protocol
- `docs/replication-result-schema.json` — machine-readable submission schema
- `docs/outreach/` — non-promotional dissemination drafts
- `src/` and `tests/` — frozen detector implementation and integrity tests

## License, conduct, and citation

Original code, labels, and documentation are MIT licensed. Third-party repository content remains under its original license.

- Citation: [`CITATION.cff`](CITATION.cff)
- Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)

The permanent DOI and research release are not yet created. Exact manual owner actions are documented in `docs/owner-actions-release-and-archive.md`.
