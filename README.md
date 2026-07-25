# Research README Smoketest

## Research question

In the first 20 papers of **JOSS issue 122 (June 2026)**, how many linked GitHub research-software repositories provide a copyable root-README path from installation/build to first meaningful use, and can a conservative static preflight find unambiguous defects without calling every missing example an error?

## Why it matters

A root README is often the first operational interface between research software and a new user. Broken commands, missing local files, or installation-only instructions create avoidable friction before scientific functionality can even be evaluated. This project measures a narrow, testable part of that problem; it does **not** equate root-README incompleteness with an unusable project.

## Pilot design

- fixed sample: first 20 papers in official JOSS issue-122 order;
- 19 GitHub repositories eligible; one GitLab repository excluded under the frozen protocol;
- manual labels for strict root-README readiness and four high-confidence defect families;
- naive baseline versus a conservative standard-library preflight;
- strict sensitivity: root README contains a safe install path and safe first-use path;
- relaxed sensitivity: strict-ready **or** explicit external documentation/tutorial route;
- preregistered H1 threshold: strict-ready below 70%, at least 15 eligible cases, and 95% Wilson upper bound below 70%.

## Main result

**SUPPORTED within the documented pilot scope.**

| Result | Value |
|---|---:|
| Strict root-README ready | 7 / 19 (36.8%) |
| 95% Wilson interval | 19.1%–59.0% |
| Relaxed-ready with external docs accepted | 19 / 19 (100%) |
| Repositories with a high-confidence hard defect | 4 / 19 (21.1%) |
| Naive baseline false positives | 4 |
| Conservative preflight fit on development sample | 0 FP, 0 FN |

The 100% relaxed result is the most important restraint: most strict failures reflect documentation placement, not proven project unusability. The four concrete hard-defect cases were an incomplete `git clone`, a verified missing relative path, `apt get`, and an undeclared assignment in an ES-module example.

## Reproduce in one command

```bash
python -m pip install -e . && PYTHONHASHSEED=0 readme-smoketest pilot --output-dir reproduced-results
```

Expected SHA-256 for `reproduced-results/pilot-results.json`:

```text
531f145706238996c499746bdb46c9f4d281221828b4f07691c68782ca2f80f8
```

## Limitations

This is an exploratory pilot, not a population prevalence estimate. It covers one JOSS issue, uses current root READMEs rather than publication-time tags, develops and evaluates rules on the same small sample, has one annotator, and does not execute heterogeneous scientific stacks. Read `RESEARCH.md` and `docs/red-team.md` before reusing the headline numbers.

## CLI

Run the frozen benchmark:

```bash
readme-smoketest pilot --output-dir results/reproduced
```

Exit codes:

| Code | Meaning |
|---:|---|
| 0 | analysis completed and outputs written |
| 2 | invalid input, unreadable dataset, or CLI error |

The CLI intentionally does not claim arbitrary README code is executable. It checks the frozen extracted blocks for conservative roles, unexplained substitutions, and four high-confidence defect types.

## Full validation

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest
pytest --cov
python -m build
PYTHONHASHSEED=0 readme-smoketest pilot --output-dir /tmp/a
PYTHONHASHSEED=321 readme-smoketest pilot --output-dir /tmp/b
diff -u /tmp/a/pilot-results.json /tmp/b/pilot-results.json
diff -u /tmp/a/pilot-results.csv /tmp/b/pilot-results.csv
```

## Repository map

- `RESEARCH.md` — complete report
- `research-manifest.yml` — sources, hashes, commands, metrics, environment, limitations
- `docs/methodology-preregistered.md` — hypotheses, definitions, baseline, stopping rule
- `docs/candidate-selection.md` and `docs/candidates.json` — 21 assessed candidate questions
- `docs/red-team.md` — twelve adversarial critiques and revised conclusion
- `data/raw/` — frozen source records
- `data/processed/` — extracted blocks and manual labels
- `results/published/` — JSON, CSV, hashes, and secondary performance observation
- `src/` — dependency-free checker and CLI
- `tests/` — 65 classification, defect, metric, CLI, and end-to-end tests

## Data and ethics

The study uses public repository metadata and short command/example fragments. It stores no intentional personal data and does not redistribute full third-party READMEs. Findings are documentation observations, not security vulnerabilities or judgments about scientific merit.

## License and citation

Original code, labels, and documentation are MIT licensed. Third-party repository content remains under its original license. Cite this pilot using `CITATION.cff`.
