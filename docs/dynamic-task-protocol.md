# Dynamic first-use task protocol

## Objective

Measure whether frozen static labels predict practical friction between opening the root README and obtaining one meaningful end-user output. The dynamic phase is a ten-case feasibility-aware validation sample, not a population estimate.

## Frozen order

1. Freeze detector v0.1.0 and the baseline commit.
2. Acquire issue 121 repositories and record root-README blob SHAs.
3. Commit detector predictions and hashes.
4. Create the human reference labels without changing rules or labels after outcomes are observed.
5. Lock the ten dynamic cases, task commands, success criteria, and safety limits before execution.
6. Preserve raw attempts before adjudication or correction.

## First meaningful task

Each case has one preregistered end-user task that must create an observable output. Import-only checks do not count unless import or initialization is the documented primary use. Optional component builds are reported separately and cannot erase a completed core first-use task.

## Raw evidence and adjudication

Raw status is immutable: `SUCCESS`, `FAILURE`, or `UNTESTABLE_HERE`. Formal adjudication is stored separately and uses only:

- `SUCCESS`
- `SUCCESS_WITH_FRICTION`
- `FAILURE_README_BLOCKER`
- `FAILURE_DEPENDENCY_COMPATIBILITY`
- `FAILURE_OTHER`
- `UNTESTABLE_HERE`

Each adjudication records the case ID, raw and final status, task completion, README blocker, dependency/compatibility blocker, minor friction, harness error, external-document supplementation, finding confirmation/disproof, evidence status, reason, supporting step IDs, correction attempt, time to first output, peak memory, and disk use.

A harness assertion or incorrect import is not a repository failure. A dependency failure is not automatically a README defect. Current documentation cannot replace a changed frozen README in the primary result.

## Permitted corrections

Only two post-run corrections were allowed:

1. sklearn-migrator: use the frozen documented random-forest regression module and required version arguments while preserving the same data, model, paths, and round-trip criterion.
2. Boost.Geometry: use the complete Boost distribution reached through the root README's official delegation while preserving the same C++ example and criterion.

Correction attempts are stored beside, not over, attempt 1. Exact commands, environment, stdout, stderr, reason, relation to the raw attempt, resource observations, and hashes are retained.

## Interpretation

A static finding predicts first-use friction only when the frozen documented path exercises it and the evidence shows that correcting or bypassing it changes the result. External documentation may supplement a root README and is reported separately. No inference beyond the ten locked dynamic cases is made.

## Stopping and integrity

Stop on a safety concern, resource limit, repeated infrastructure failure, or established success/failure. Do not silently change the task. Do not delete raw failures. Do not relabel static references or modify detector rules after observing results.
