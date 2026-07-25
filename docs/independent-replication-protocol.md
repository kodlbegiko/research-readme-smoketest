# Independent replication protocol

## Purpose

This protocol supports independent attempts to reproduce, contradict, or qualify the negative issue-121 external-validation result. It does not authorize modification or productization of the frozen v0.1.0 detector.

## Required preregistration

Before acquiring source material or viewing aggregate outcomes, record:

- study identifier and public timestamp;
- sampling source, inclusion and exclusion rules, order, and target sample size;
- detector commit and file hashes;
- primary and secondary outcomes;
- engineering gates;
- reference-label definitions;
- annotator identities or anonymized roles and independence statement;
- dynamic-case selection strata and stopping rules;
- execution safety and resource limits;
- correction, adjudication, and missing-data policy;
- maintainer-contact eligibility and impact policy.

Any change after preregistration must be dated, justified, and reported as a deviation.

## Sequential lock order

Use this order:

1. freeze detector and protocol;
2. freeze sampling frame;
3. acquire each repository at one immutable commit;
4. generate predictions;
5. commit prediction files and hashes;
6. create independent human reference labels;
7. evaluate static metrics;
8. lock dynamic cases and tasks;
9. preserve raw attempts;
10. adjudicate without deleting raw evidence;
11. run only predeclared corrections;
12. consider maintainer intervention separately;
13. publish all results, including negative and blocked outcomes.

## Acquisition requirements

For each repository, record:

- host and canonical repository identifier;
- default branch name;
- immutable acquired commit SHA;
- root README path and blob SHA;
- acquisition timestamp;
- relevant metadata and API request failures;
- exclusions and reasons.

README retrieval and relative-path checks must use the same immutable commit. Do not combine evidence from moving branch tips.

## Prediction lock

The prediction lock must include:

- detector commit and relevant source hashes;
- dataset and acquisition manifest hashes;
- canonical prediction-file SHA-256;
- assertion that reference labels were absent when locked;
- environment and command used;
- timestamp and responsible party.

Reference evaluation must reject a prediction file whose bytes do not match the lock.

## Reference annotation

At least one reference annotator must be genuinely independent of the original issue-121 autonomous annotation process. Prefer two independent humans and report agreement before reconciliation.

Annotators must classify the predeclared constructs rather than optimize detector metrics. Preserve initial labels, disagreement records, reconciliation decisions, and rationale. AI assistance must be disclosed and is not a second independent human annotator.

## Dynamic validation

Lock each dynamic task before execution. Each case must define:

- first meaningful task;
- observable success criterion;
- allowed documentation scope;
- environment and resource caps;
- prohibited commands and safety review;
- timeout and process-group termination behavior;
- relation to detector predictions.

Store exact commands, exit codes, stdout, stderr, timing, memory, disk use, and hashes. A successful install alone is not task success unless installation is the documented product-level task.

## Adjudication

Permitted final statuses are:

- `SUCCESS`
- `SUCCESS_WITH_FRICTION`
- `FAILURE_README_BLOCKER`
- `FAILURE_DEPENDENCY_COMPATIBILITY`
- `FAILURE_OTHER`
- `UNTESTABLE_HERE`

Distinguish direct README blockers, compatibility failures, minor friction, harness errors, and external-document supplementation. Preserve the raw status even when the final status changes.

## Corrections

A correction is allowed only when its reason and scope were predeclared or when it repairs an unambiguous harness error without changing the scientific task. Store it in a separate attempt directory with:

- relation to the original attempt;
- one-difference description;
- exact commands and environment;
- complete result and compact logs;
- result hashes;
- statement that it does not overwrite the raw attempt.

## Maintainer intervention

Contact is optional and cannot validate the detector by itself. Before contact, verify current default branch behavior, relevant documentation, existing issues and pull requests, and whether the problem requires guessing maintainer intent.

Count submissions, responses, accepted corrections, merged changes, and measured user benefit separately. Submission alone is not impact.

## Analysis

Report counts and uncertainty without population claims unsupported by the sampling design. At minimum report:

- sample and exclusions;
- confusion matrix and all preregistered metrics;
- engineering-gate outcomes;
- missing and blocked cases;
- dynamic first-task success among testable cases;
- predicted findings confirmed and disproved;
- harness errors and compatibility blockers;
- external-document supplementation;
- deviations and limitations.

## Submission package

A replication package should contain:

- completed submission template;
- JSON conforming to `docs/replication-result-schema.json`;
- preregistration reference;
- acquisition and prediction locks;
- reference labels and disagreement records;
- raw dynamic evidence and adjudications where applicable;
- SHA-256 manifests;
- environment and dependency records;
- concise interpretation that allows disagreement with the original conclusion.
