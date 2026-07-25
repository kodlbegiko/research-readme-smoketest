# Independent replicator onboarding

## One-page brief

This repository preserves a negative external validation of Research README Smoketest v0.1.0. The original study found precision of 1.000 but recall of approximately 0.292 and accuracy of approximately 0.553, below a preregistered 0.750 accuracy gate. Three predicted hard findings were disproved. In ten locked dynamic cases, eight of nine testable cases completed the first meaningful task and no direct README blocker was observed.

The objective of replication is not to defend this result. A valid independent submission may be:

- `REPRODUCED`;
- `PARTIALLY_REPRODUCED`;
- `CONTRADICTED`;
- `INCONCLUSIVE`; or
- `BLOCKED`.

Do not modify the frozen issue-121 detector and then describe the result as an out-of-sample replication. Do not count AI re-reading as a second independent human annotation. Preserve failed attempts, deviations, and unfavorable evidence.

## Choose the replication mode

### A. Computational reproduction

Purpose: verify that the published artifacts, hashes, scripts, metrics, and reports reconstruct from the frozen repository state.

Typical scope:

- checkout the formal tag or publication commit;
- install the documented development environment;
- verify all SHA-256 manifests;
- run tests and deterministic reconstruction checks;
- independently recompute static and dynamic summary metrics from preserved machine-readable data;
- report any packaging, environment, or script divergence.

This mode does **not** create independent human reference annotation when it reuses the published labels.

Estimated effort: 2-6 hours for a clean computational check; longer if environment incompatibilities require documented investigation.

### B. New-data replication

Purpose: evaluate a frozen detector on genuinely new repositories with independent annotation and a preregistered analysis.

Required sequence:

1. preregister the sampling frame, outcomes, gates, stopping rules, and adjudication policy;
2. freeze detector commit and source hashes;
3. acquire repositories at immutable commits;
4. generate predictions;
5. lock and hash predictions before reference labels exist;
6. obtain independent human reference labels;
7. calculate static outcomes;
8. lock dynamic cases and tasks before execution;
9. preserve raw attempts;
10. adjudicate without deleting raw evidence;
11. run only predeclared or unambiguous one-difference corrections;
12. publish all outcomes and deviations.

Estimated effort: 5-15 person-days for a small rigorous replication, depending on sample size, number of annotators, and dynamic execution complexity.

## Environment requirements

Minimum for computational reproduction:

- Git;
- Python 3.11 or 3.13;
- a POSIX-like environment for the published checksum command;
- enough disk space to build the package and inspect evidence files;
- no requirement to execute third-party dynamic cases unless explicitly included in the replication plan.

Additional requirements for new-data dynamic replication:

- isolated disposable environments or containers;
- explicit CPU, memory, disk, network, and timeout limits;
- process-group termination for timed commands;
- a safety review for third-party commands;
- immutable storage for raw logs and result files.

## Independent human annotator eligibility

An annotator is eligible as an independent human annotator when the person:

- did not create the original issue-121 reference labels;
- was not responsible for the frozen detector predictions;
- did not see aggregate outcomes before completing initial labels;
- applies the preregistered construct rather than attempting to improve detector metrics;
- discloses relationships to the original author and sampled repositories; and
- preserves initial labels before reconciliation.

A person may use disclosed AI assistance for clerical support, but AI output is not a second independent human annotation. Prefer two independent human annotators and report agreement before reconciliation.

## Conflict-of-interest disclosure

Disclose:

- employment, funding, collaboration, supervision, or close personal relationships with the original author;
- contribution to the detector, protocol, sampled repositories, or source publication venue;
- incentives tied to a favorable or unfavorable result;
- use of paid services or infrastructure provided by interested parties; and
- the exact role of AI systems.

A conflict does not automatically invalidate a study. It must be visible and considered in interpretation.

## Preregistration checklist

Before viewing aggregate outcomes, record:

- study ID and public timestamp;
- replication mode;
- sampling source, order, inclusion/exclusion rules, target size, and stopping rule;
- detector version, commit, and source hashes;
- primary and secondary outcomes;
- static and dynamic decision gates;
- label definitions and annotation instructions;
- annotator roles and independence criteria;
- agreement and reconciliation plan;
- dynamic-case selection method;
- allowed documentation scope;
- execution safety and resource limits;
- missing-data, adjudication, and correction policy;
- maintainer-contact and impact policy; and
- planned machine-readable outputs.

Any later change must be timestamped, justified, and reported as a deviation.

## Frozen prediction procedure

1. Run the detector only after the detector and acquisition manifest are frozen.
2. Canonicalize the prediction output deterministically.
3. Calculate SHA-256 for the prediction file.
4. Record detector commit, source hashes, acquisition-manifest hash, command, environment, and timestamp.
5. Commit or deposit the prediction file and lock in a location unavailable for silent replacement.
6. State that reference labels were absent or inaccessible at lock time.
7. Make the evaluator reject prediction bytes that do not match the lock.

## Immutable acquisition commit procedure

For each repository:

1. resolve one immutable commit SHA from the selected branch or tag;
2. record host, canonical repository ID, default branch, and acquisition timestamp;
3. retrieve the root README at that commit;
4. record README path and blob SHA;
5. perform relative-path checks at the same commit;
6. preserve API errors and exclusions; and
7. never combine a moving branch-tip README with path checks from a later revision.

## Raw evidence preservation

Store, without overwriting:

- exact commands and environment;
- start/end timestamps and exit status;
- stdout and stderr;
- resource observations;
- generated artifacts and their hashes;
- the raw outcome before adjudication;
- the relation of every correction to its original attempt; and
- a SHA-256 manifest covering the submission package.

## Failed-attempt reporting rule

A failed, timed-out, unsafe, or blocked attempt remains part of the record even when a later correction succeeds. Do not replace it, omit it from counts, or describe the correction as the original detector result. Report raw and adjudicated statuses separately.

## Submission package

Submit:

- a completed replication report;
- JSON conforming to `docs/replication-result-schema.json`;
- preregistration URI and timestamp;
- detector, acquisition, and prediction locks;
- independent reference labels and disagreement records;
- raw dynamic evidence and adjudications, if applicable;
- deviation report;
- environment and dependency records;
- SHA-256 manifests; and
- an interpretation that permits disagreement with the original conclusion.

Validate with:

```bash
python scripts/validate_replication_submission.py path/to/result.json
```

For a schema-only self-check:

```bash
python scripts/validate_replication_submission.py --check-schema
```
