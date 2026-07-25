# Independent replication

## Status

This repository is a **negative external-validation result**, not a recommended README-checking product.

- Detector out-of-sample validity: **NOT SUPPORTED**
- Predictive value for first-use friction: **NOT SUPPORTED**
- Productization: **NOT SUPPORTED**
- GitHub Action v0.2: **not planned**

Independent work is welcome when it can support, contradict, or qualify these conclusions with new evidence.

## Research question

Can the frozen v0.1.0 static detector identify research-software root READMEs that provide a safe install-to-first-meaningful-use path, and do its findings predict observed first-use friction?

The issue-121 study found high strict-ready precision but low recall, failed its preregistered accuracy gate, produced three false-positive hard findings, and did not predict the observed dynamic blockers.

## Frozen materials

Do not modify these materials when reproducing the published issue-121 result:

- detector baseline commit: `2caeecc8678a4614f6fe6771df0ace6827a5f434`
- `data/issue-121/predictions/predictions.json`
- `data/issue-121/predictions/PREDICTION_LOCK.json`
- `data/issue-121/annotations/reference-labels.json`
- `data/issue-121/dynamic-tests/DYNAMIC_LOCK.json`
- raw dynamic attempts under `data/issue-121/dynamic-tests/results/`
- final adjudications under `data/issue-121/dynamic-tests/adjudications/`
- `results/issue-121/DYNAMIC-FINAL-SHA256SUMS`

## Reproduce the committed result

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

Reproduce the frozen static evaluation outside committed result directories:

```bash
rm -rf /tmp/readme-replication
mkdir -p /tmp/readme-replication/data/issue-121
cp -R data/issue-121/raw /tmp/readme-replication/data/issue-121/
cp -R data/issue-121/predictions /tmp/readme-replication/data/issue-121/
python scripts/evaluate_issue_121.py \
  --data-dir /tmp/readme-replication/data/issue-121 \
  --results-dir /tmp/readme-replication/results

diff -u \
  data/issue-121/annotations/reference-labels.json \
  /tmp/readme-replication/data/issue-121/annotations/reference-labels.json

diff -u \
  results/issue-121/static-validation-results.json \
  /tmp/readme-replication/results/static-validation-results.json
```

The evaluator verifies that the prediction file SHA-256 matches the prediction lock before producing reference results.

## Review the dynamic evidence

The ten dynamic cases were locked before execution. A valid review must keep separate:

1. the original raw attempt;
2. the formal adjudication;
3. any preregistered correction attempt;
4. any later current-branch recheck.

Do not replace a raw attempt with a correction result. Do not classify dependency or compatibility failures as README defects without direct evidence. Do not treat AI re-reading the same evidence as an independent human annotation.

## Run a new out-of-sample study

A new validity study must use:

- a newly preregistered dataset that was not selected after viewing outcomes;
- a detector version frozen before reference annotation;
- committed prediction hashes before human labels are created;
- at least one genuinely independent human reference annotator, with roles disclosed;
- preserved raw evidence and exact commands;
- a predeclared correction and adjudication policy;
- maintainer intervention counted separately from detector validity;
- explicit stopping rules and engineering gates.

Do not reuse JOSS issue 121 to tune rules and then call the resulting evaluation out-of-sample.

## What counts as independent replication

A result may be described as independent only when the replicator is not merely rerunning the original agent's judgments and independently controls the relevant execution or annotation process. Report funding, affiliations, conflicts, dataset selection, deviations, and all failed attempts.

Acceptable outcomes include:

- reproduced;
- partially reproduced;
- contradicted;
- inconclusive;
- blocked by unavailable evidence or infrastructure.

None is preferred in advance.

## Submit a result

Use:

- `docs/independent-replication-protocol.md`
- `docs/replication-result-schema.json`
- `docs/replication-submission-template.md`

Submit a pull request containing machine-readable results, hashes, a concise report, and links to independently controlled raw evidence. A GitHub issue containing only a conclusion is not a replication.
