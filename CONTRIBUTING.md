# Contributing

Contributions should preserve the distinction between evidence, inference, and unknowns.

## Development setup

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest --cov
python -m build
```

## Adding a detector

A new hard-defect rule must include:

1. a syntax- or repository-evidence definition that does not require guessing intent;
2. at least one positive and one negative unit test;
3. a documented false-positive boundary;
4. a frozen labeled example or synthetic fixture;
5. no execution of untrusted third-party commands.

Do not change the published issue-122 labels to improve metrics. Corrections must be documented in the changelog, include the original and revised evidence, and regenerate result hashes.

## Out-of-sample studies

Use a new dataset identifier and freeze the rule version before labeling aggregate results. Prefer two independent annotators and report agreement before evaluating classifier performance.
