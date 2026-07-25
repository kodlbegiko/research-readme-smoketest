# Why a High-Precision README Checker Still Failed External Validation

A static checker can look convincing while failing the decision it was meant to support.

Research README Smoketest v0.1.0 was designed as a conservative detector for install-to-first-use paths in research-software root READMEs. In its development pilot, the detector appeared precise. The issue-121 external validation tested whether that apparent strength held on new data and whether static findings predicted practical first-use friction.

They did not.

## The headline result

Across 38 eligible GitHub repositories from JOSS issue 121:

- the detector predicted 7 repositories as strict-ready;
- the human reference labeled 24 as strict-ready;
- TP / FP / TN / FN was 7 / 0 / 14 / 17;
- precision was 1.000;
- recall was approximately 0.292;
- accuracy was approximately 0.553;
- F1 was approximately 0.452.

Precision 1.0 meant that the detector's seven positive classifications were correct under the reference labels. It did **not** mean the detector found most repositories that were actually ready. It missed 17 of the 24 reference-positive repositories.

The preregistered accuracy gate was 0.75. The observed accuracy of about 0.553 failed that gate. A detector that rarely declares readiness can achieve high positive precision while remaining too incomplete for product decisions.

## The hard findings also failed

The detector emitted three hard findings for sklearn-migrator. Manual review and a permitted correction rerun showed that all three referenced paths were intended runtime outputs created by the user's script, not files missing from the upstream repository.

The correction used the documented regression random-forest module and completed a serialize/deserialize round trip. All three findings were marked `DISPROVED` and were not counted as true positives.

## Why dynamic first-use testing mattered

Ten cases were locked before execution. The raw attempts were four successes, five failures, and one untestable case. Formal adjudication separated repository behavior from harness errors, dependency failures, optional components, and external documentation.

After adjudication:

- 6 cases were `SUCCESS`;
- 2 were `SUCCESS_WITH_FRICTION`;
- 1 was `FAILURE_DEPENDENCY_COMPATIBILITY`;
- 1 remained `UNTESTABLE_HERE`;
- 0 were direct README blockers.

Eight of nine testable cases completed the first meaningful task. None of the three predicted hard findings blocked first use.

## Not every failure is a README defect

Three distinctions materially changed the result:

1. **Harness error:** GaPFlow completed its simulation, but the harness checked a fixed output path instead of the timestamped output directory.
2. **Dependency or compatibility failure:** WoodTapper's published package failed against changed scikit-learn/Cython internals. Current source later pinned a compatible version. That is not automatically a README defect.
3. **External-document delegation:** Boost.Geometry's root README directed users to the full Boost distribution. Compiling only the geometry subrepository omitted required headers; the official distribution completed the same task.

Kigali Sim also showed why component scope matters: its core Java CLI produced a non-empty CSV, while an optional direct editor build failed because the harness skipped the documented parser-generation workflow.

## Why preserve a negative result

Stopping productization is a valid research outcome. Publishing a GitHub Action after these results would convert an underperforming classifier into automated reports against maintainers. Preserving the failed gates, raw attempts, corrections, adjudications, and zero-impact baseline reduces pressure to hide unfavorable evidence.

The repository therefore remains:

- a reproducible negative external-validation result;
- a dataset for reviewing evidence and adjudication;
- an example of prediction locking and correction separation;
- an entry point for genuinely independent replication.

It is not a generally validated README checker.

## No GitHub Action v0.2

There will be no GitHub Action v0.2, no retuning on JOSS issue 121, and no claim that v0.1.0 is suitable for general adoption. A future detector can only be reconsidered through a new preregistered study, a newly frozen version, new out-of-sample data, and independent human reference annotation.

See `EXTERNAL-VALIDATION.md`, `REPLICATION.md`, and `PUBLIC-INTEREST.md` for the complete evidence and boundaries.
