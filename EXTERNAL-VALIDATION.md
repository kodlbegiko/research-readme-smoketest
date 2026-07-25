# External validation closeout

## Decision

**External validation did not support v0.1.0 detector productization.**

The project should not continue as a GitHub Action or generally adoptable README checker. It should be preserved as a reproducible negative research result, an external-validation dataset, and a research-method example. A future detector can be reconsidered only in a new preregistered study with new frozen rules and new out-of-sample data.

## Frozen evaluation order

The baseline was frozen at `2caeecc8678a4614f6fe6771df0ace6827a5f434`. Acquisition, detector predictions, prediction hashes, reference annotation, static evaluation, dynamic-case lock, raw dynamic attempts, adjudication, permitted corrections, and intervention decisions occurred in that order. Detector rules and reference labels were not modified after outcomes were observed.

## Static result

Issue 121 contained 39 papers, with 38 eligible GitHub repositories and one preregistered GitLab exclusion. The frozen detector predicted 7 strict-ready repositories; the reference labeled 24. The confusion matrix was TP 7, FP 0, TN 14, FN 17. Precision was 1.000, recall 0.292, specificity 1.000, accuracy 0.553, and F1 0.452. Accuracy missed the 0.75 gate. The three sklearn-migrator hard findings were all false positives, so hard-defect precision also missed its 0.80 gate.

**Detector out-of-sample validity: NOT SUPPORTED.**

## Dynamic result

The ten locked raw attempts were 4 `SUCCESS`, 5 `FAILURE`, and 1 `UNTESTABLE_HERE`. After evidence-preserving adjudication, the statuses were:

- `SUCCESS`: 6
- `SUCCESS_WITH_FRICTION`: 2
- `FAILURE_DEPENDENCY_COMPATIBILITY`: 1
- `UNTESTABLE_HERE`: 1
- all other failure classes: 0

Eight of nine testable cases completed the first meaningful task (0.888889). The adjudicated median time to first output was 28.598945 seconds. The raw-success-only median was 33.017382 seconds. Five of five testable strict false negatives completed first use; including the frozen-but-untestable ecodive case, this was five of six locked false negatives. None of the three predicted hard findings blocked first use, and all three were dynamically disproved.

Observed blocker/error counts were one dependency/compatibility blocker, two external-document-supplemented cases, three harness errors, and zero direct README blockers. Raw peak memory ranged from 19,848 to 537,056 KiB; raw disk use ranged from 10,100,893 to 1,306,538,910 bytes. Correction metrics are reported separately and are not substituted into raw attempt statistics.

**Static findings' predictive value for first-use friction: NOT SUPPORTED.**

## Material adjudications

- **GaPFlow:** simulation completed; the fixed `data/journal` assertion was a harness error. Final status: `SUCCESS`.
- **Kigali Sim:** Java CLI and CSV output succeeded. The optional direct editor build omitted the documented ANTLR generation flow. Final status: `SUCCESS_WITH_FRICTION`; core component `SUCCESS`, editor attempt `FAILURE_OTHER`.
- **sklearn-migrator:** the bad import and omitted version arguments were corrected against the frozen documented API. The round trip succeeded and all three path findings are `DISPROVED`.
- **Boost.Geometry:** the geometry subrepository alone was incomplete; the root README's official Boost delegation supplied the complete headers. The same example succeeded. Final status: `SUCCESS_WITH_FRICTION`.
- **WoodTapper:** PyPI 0.0.13 remained incompatible, but current main installed and ran after the upstream pin. Final status: `FAILURE_DEPENDENCY_COMPATIBILITY`, not a detector finding.
- **ecodive:** README provenance changed, so the frozen case remains `UNTESTABLE_HERE`.

## Corrections and raw evidence

Attempt 1 directories and failures remain unchanged. The two permitted correction attempts are separate directories with commands, environment, stdout, stderr, reasons, original-attempt relations, hashes, memory, and disk observations. No correction was counted as a detector true positive.

## Maintainer intervention

No issue or pull request was submitted. Kigali Sim already documented the omitted generation step. WoodTapper current main already contained the compatibility pin and warning and completed first use. Filing reports would have been redundant or low-confidence.

**Maintainer intervention actual value: INCONCLUSIVE.** No intervention occurred, and zero submissions are not presented as impact.

## Research-integrity review and hardening

Before merge, review identified five implementation risks that did not justify altering the frozen scientific results but required correction for safe reproduction and future studies:

- timed commands did not terminate the entire descendant process group;
- the HiMAP task command could mask a failed primary command with a successful trailing pipeline;
- the reference evaluator did not verify `predictions.json` against the prediction lock;
- future acquisition could query a README and referenced paths from different moving branch revisions;
- two pull-request workflows could write generated outputs back to the PR branch.

The merged implementation now terminates timed process groups, asserts HiMAP task artifacts, verifies prediction-file SHA-256 against its lock, resolves one immutable repository commit for README and path checks, and keeps pull-request validation workflows read-only. Regression tests and Python 3.11/3.13 CI cover these controls.

These fixes harden reproduction infrastructure. They do not retune the detector, change reference labels, delete raw attempts, or convert correction successes into detector true positives.

## Limitations

- The dynamic sample contains ten feasibility-selected cases and supports no population inference.
- One autonomous agent performed sequential acquisition and reference annotation; this is not independent inter-rater validation.
- The original frozen issue-121 acquisition retained README blob SHAs but did not record one repository commit SHA for every README/path-check request sequence. No observed case was shown to have crossed revisions, but that possibility was not cryptographically excluded. Future acquisition is commit-pinned; the frozen historical evidence remains unchanged.
- ecodive could not be safely replayed from the frozen acquisition state.
- Correction reruns answer narrow harness questions and cannot rehabilitate the failed static gates.
- Maintainer acceptance, merge, and measured user benefit were not observed.
- Independent reproduction, independent human re-annotation, citation, accepted upstream correction, and measured user-benefit counts were all zero at publication closeout.

## Product decision

**Overall productization: NOT SUPPORTED.**

There will be no GitHub Action v0.2, no rule tuning on issue 121, and no presentation of this detector as generally valid. The repository remains useful as a transparent negative result showing how prediction locking, raw-evidence preservation, adjudication, correction separation, and conservative intervention policy prevent favorable-result bias. Local upstream fixes, if accepted in future, must be logged as narrow public-interest outcomes and must not be interpreted as detector success.

The next valid sources of value are durable citation, public methodological translation, and genuinely independent external replication—not further tuning of this detector on the same evidence.
