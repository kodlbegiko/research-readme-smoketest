# Contributing

This repository is a negative research archive, not an active detector product.

## Accepted contribution types

Contributions should be limited to:

- reproducibility or checksum fixes;
- corrections to documentation or metadata;
- independently produced replication packages;
- independently controlled human re-annotation evidence;
- accessibility and preservation improvements;
- verified updates to the public-interest impact log;
- security fixes that do not alter frozen scientific outputs.

## Out of scope

Do not submit:

- new v0.1.0 detector rules;
- tuning against JOSS issue 121;
- a GitHub Action or service wrapper;
- relabeled historical reference data intended to improve metrics;
- deleted or overwritten raw failed attempts;
- correction reruns presented as detector success;
- AI re-reading presented as an independent human annotation;
- unverified impact claims;
- mass maintainer reports generated from detector output.

A future detector version requires its own preregistration, new dataset, frozen predictions, independent reference annotation, and separate repository or clearly separated study namespace.

## Development setup

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

Do not regenerate committed historical outputs unless the contribution explicitly documents a reproducibility defect and preserves both original and corrected evidence.

## Independent replication submissions

Follow:

- `REPLICATION.md`
- `docs/independent-replication-protocol.md`
- `docs/replication-result-schema.json`
- `docs/replication-submission-template.md`

A replication pull request must include a new study ID, preregistration reference, machine-readable results, raw-evidence location, hashes, deviations, independence statement, and an interpretation that permits disagreement with the original result.

## Public-interest claims

Follow `docs/impact-measurement-policy.md`. Update both impact logs in one reviewed change. GitHub activity, submissions, downloads, and social reach are not verified impact outcomes by themselves.

## Pull-request requirements

Each pull request should state:

1. whether frozen issue-121 evidence changes;
2. why the change is allowed under this policy;
3. commands executed;
4. affected hashes;
5. research-integrity risks;
6. whether external claims or counts change;
7. any manual archive or release action required.

Prefer small, auditable changes. Preserve the distinction between evidence, inference, and unknowns.
