# Independent replication submission validation checklist

## Identity and independence

- [ ] Unique study ID is present.
- [ ] Responsible individuals or organization are identified.
- [ ] Public preregistration URI and timestamp are present.
- [ ] Relationship to the original author is disclosed.
- [ ] Relationships to sampled projects are disclosed.
- [ ] Funding and conflicts are disclosed.
- [ ] AI assistance and exact role are disclosed.
- [ ] Independent human annotator count is not inflated by AI systems.

## Lock order

- [ ] Detector commit and source hashes were frozen before annotation.
- [ ] Sampling frame and stopping rule were frozen.
- [ ] Acquisition used immutable repository commits.
- [ ] Predictions were generated before reference labels.
- [ ] Prediction bytes match the recorded SHA-256 lock.
- [ ] Initial independent labels were preserved before reconciliation.
- [ ] Dynamic cases and tasks were locked before execution.

## Evidence integrity

- [ ] Raw attempts are preserved.
- [ ] Failed attempts remain reported.
- [ ] Corrections are separate and linked to originals.
- [ ] Deviations are dated and outcome-awareness is disclosed.
- [ ] Exact commands, environment, logs, and result hashes are present.
- [ ] A package-level SHA-256 manifest is present.
- [ ] Direct README blockers are separated from harness and compatibility failures.

## Analysis and claims

- [ ] Confusion matrix is internally consistent.
- [ ] Metrics use declared denominators.
- [ ] Missing and blocked cases are visible.
- [ ] Sampling design supports the stated generalization.
- [ ] Maintainer submissions are not counted as accepted corrections.
- [ ] Reach metrics are not counted as impact outcomes.
- [ ] Result status is one of the allowed five replication outcomes.
- [ ] Contradictory or unfavorable evidence is not hidden.

## Machine validation

- [ ] `python scripts/validate_replication_submission.py result.json` passes.
- [ ] All referenced artifacts exist or have durable public URIs.
- [ ] All SHA-256 values are 64 lowercase hexadecimal characters.
- [ ] Reviewer records validation date, role, and unresolved disputes.
