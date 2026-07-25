# Impact measurement policy

## Principle

Public-interest claims must follow evidence, not activity counts. The project records dissemination and engagement, but does not relabel them as impact without an externally verifiable outcome.

## Evidence classes

### 1. Research output

A versioned artifact exists and passes its integrity checks. Examples: protocol, result file, adjudication, checksum manifest, or archived release.

### 2. Dissemination

The result is presented to an audience. Examples: public post, talk, workshop, repository view, or release download. Dissemination may enable impact but is not an impact outcome by itself.

### 3. Independent reproduction

A party independent of the original autonomous annotation process follows a declared protocol, controls its own annotation or execution, preserves raw evidence, and publishes machine-readable results. Simple reruns of committed tests are reproducibility checks, not independent replication.

### 4. Maintainer-confirmed ground truth

A relevant upstream maintainer confirms or corrects the study's interpretation with repository-specific evidence. A response that only acknowledges receipt is not confirmation.

### 5. Accepted correction

An upstream issue is accepted as valid, a pull request is merged, or equivalent documented action occurs. Submission alone is not accepted correction.

### 6. Measured user benefit

A predeclared metric demonstrates a practical improvement, such as lower false-report rate, reduced maintainer triage time, improved first-use completion, or reduced documentation-review effort. Anecdotes may motivate measurement but do not establish the outcome.

### 7. General social impact

Evidence supports effects beyond isolated repositories and addresses representativeness, counterfactuals, confounding, and uncertainty. This project currently makes no such claim.

## Acceptance rules

Every non-zero outcome must include:

- unique event ID;
- event date and recording date;
- evidence class;
- source URI or immutable reference;
- responsible verifier;
- relationship to the project;
- verification status;
- short rationale;
- whether it duplicates another event;
- any dispute, reversal, or limitation.

Counts use unique verified outcomes only. One merged change referenced in several posts counts once. A reproduction with no independent annotation or execution does not count as independent.

## Prohibited substitutions

Do not substitute the following for impact:

- issue or PR submission;
- GitHub stars, watchers, forks, views, clones, or downloads;
- social engagement;
- AI-generated review;
- repository-owner self-attestation without external evidence;
- planned, pending, or promised work;
- detector predictions without reference validation;
- correction reruns presented as detector success.

## Updating the log

Update both machine-readable logs in one reviewed change:

- `results/public-interest/impact-log.json`
- `results/public-interest/impact-log.csv`

The JSON is authoritative. The CSV is a flat export. Record disputed or invalidated events rather than deleting them, and exclude them from verified counts.

## Initial state

As of the negative-research closeout, all external outcome counts are zero. The repository's completed internal research outputs are documented separately and are not added to external-impact counts.
