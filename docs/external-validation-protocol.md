# JOSS issue 121 external validation protocol

Status: **FROZEN BEFORE ISSUE-121 PREDICTION AND REFERENCE LABELING**

Frozen baseline commit: `2caeecc8678a4614f6fe6771df0ace6827a5f434`

Dataset: every paper in official JOSS issue 121 order (May 2026), with no discretionary replacement.

## Research questions

1. Does the v0.1.0 detector retain acceptable out-of-sample performance?
2. Do frozen static findings predict reproducible first-use friction?
3. Do independently confirmed findings lead to accepted upstream corrections?

## Acquisition and exclusions

For every issue entry, record order, title, DOI, official software repository, host, default branch, root README path, README Git blob SHA, acquisition timestamp, primary ecosystem, and explicit external-documentation links.

Pre-frozen exclusions:

- repository host is not GitHub;
- linked resource is not the software source repository;
- repository is deleted, private, or inaccessible;
- no recognizable root README exists after checking `README.md`, `README.rst`, `README`, and case variants.

README length, complexity, language, installation difficulty, and detector outcome are not exclusion reasons. Every exclusion remains in `data/issue-121/exclusions.json`.

## Prediction lock

The sequence is mandatory:

1. freeze detector and acquisition rules;
2. acquire root README evidence;
3. extract blocks mechanically;
4. run the unchanged v0.1.0 detector;
5. write prediction JSON and CSV;
6. commit prediction files and SHA-256 manifest;
7. only then create reference annotations.

The same autonomous agent performs acquisition and later annotation, so true human cognitive blinding is impossible. Git history provides a temporal prediction lock, not an independent blinded-annotator guarantee.

## Frozen detector

No detector term, role rule, placeholder rule, or hard-defect rule may change during the primary evaluation. Prediction-affecting corrections must preserve the original locked output and be reported separately as post-hoc analysis.

The four frozen hard-defect families are:

1. `git clone` command with no non-option target;
2. referenced relative path independently verified absent;
3. `sudo apt get` command typo;
4. undeclared `new` assignment in an ES-module JavaScript/TypeScript block.

## Reference annotation

Reference labels follow `docs/annotation-guide-v1.md`. One annotator is permitted but must be reported as a limitation. Repeated outputs from the same AI system are not independent annotators. If a second human annotator is obtained, raw labels, disagreements, Cohen's kappa, and adjudication must all be retained.

## Primary engineering gates

- hard-defect precision >= 0.80;
- hard-defect false-positive rate <= 0.10;
- strict-ready classification accuracy >= 0.75.

These are continuation gates, not universal scientific standards. Missing positive findings make precision non-estimable and therefore do not satisfy the hard-defect gate.

## Dynamic validation

Select 8–12 feasible, stratified cases only after reference labels are locked. Execute only statically reviewed instructions in isolated environments. Record time to first meaningful output, commands, manual steps, external searches, documentation transitions, errors, resource use, success, and whether each static finding was a blocker, minor friction, externally repaired, or unrelated.

GPU-, HPC-, restricted-data-, GUI-only-, or otherwise infeasible cases are `UNTESTABLE HERE`, not failures.

## Maintainer intervention

Contact at most five upstream repositories, and only after the finding is current, independently rechecked, dynamically reproduced when feasible, not already reported, and fixable without guessing intent. A submitted issue or PR is outreach, not impact. Only accepted correction, merged fix, confirmed false positive, maintainer ground truth, or measured task improvement counts as an outcome.

## Productization gate

Do not build a GitHub Action or SaaS unless all requested validity, dynamic-friction, adoption, and maintenance conditions are met. Otherwise narrow the project to a hard-defect linter or stop with a documented negative result.

## Allowed verdicts

Each component and the overall study must use exactly one of: `SUPPORTED`, `NOT SUPPORTED`, `INCONCLUSIVE`, or `BLOCKED`.