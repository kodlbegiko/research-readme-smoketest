# Why a High-Precision README Checker Failed External Validation

**Sean Liu**  
Independent research project  
Publication commit: `4dfb0b961470974f9dc80a936db86450303d007a`

## Abstract

Static checks for research-software documentation are attractive because they are inexpensive, repeatable, and easy to automate. Their apparent precision, however, can conceal poor coverage and weak practical validity. This research note reports a preregistered external validation of Research README Smoketest v0.1.0, a frozen detector intended to identify whether root README files provided a copyable path from installation to a first meaningful use. The evaluation covered 38 eligible GitHub repositories associated with Journal of Open Source Software issue 121. The detector classified 7 repositories as strict-ready, while the human reference classified 24. The resulting confusion matrix was 7 true positives, 0 false positives, 14 true negatives, and 17 false negatives. Precision was 1.000, but recall was approximately 0.292, accuracy approximately 0.553, and F1 approximately 0.452. The preregistered accuracy gate of 0.750 failed. Three predicted hard findings were subsequently disproved under the study's correction policy. A separately locked ten-case dynamic validation produced 6 `SUCCESS`, 2 `SUCCESS_WITH_FRICTION`, 1 `FAILURE_DEPENDENCY_COMPATIBILITY`, and 1 `UNTESTABLE_HERE`; no direct README blocker was observed, and 8 of 9 testable cases completed the first meaningful task. These results did not support the detector's out-of-sample validity, the predictive value of its static findings for first-use friction, or productization as a GitHub Action. The main contribution is therefore methodological: a transparent negative result that preserves prediction locks, raw attempts, adjudications, correction reruns, machine-readable outputs, checksums, and a protocol for independent replication.

## 1. Research context

A root README is often the first operational interface between research software and a new user. It may contain installation commands, a minimal example, links to detailed documentation, data requirements, and the first observable output. Because this material is text, it is tempting to treat documentation readiness as a static classification problem. A checker can search for installation sections, code blocks, local paths, command-like examples, and other structural signals. The output can then be summarized as a readiness label or a set of findings.

That approach has a practical appeal. Static inspection is cheaper and safer than executing arbitrary third-party software. It can be run in continuous integration and may appear objective because the same rules are applied to every repository. Yet documentation is not merely a collection of tokens. A referenced path may be a runtime output rather than a missing input. A root README may deliberately delegate setup details to official documentation. A failed build may reflect dependency drift, a test harness mistake, an optional component, or an environment limitation rather than a README defect. A detector can therefore be internally consistent while measuring the wrong construct or missing many valid cases.

Research README Smoketest began as an exploratory pilot. The favorable pilot result was development-sample evidence, not proof of general validity. The issue-121 study was designed to answer the harder question: whether a frozen detector generalized to a new set of research-software repositories and whether its static findings predicted observed first-use friction. The study used prediction locking, a frozen decision protocol, separate reference annotation, locked dynamic cases, preserved raw attempts, formal adjudication, and limited correction reruns. The external validation was allowed to fail. It did.

## 2. Research question

The primary research question was:

> Does the frozen v0.1.0 detector validly classify root-README install-to-first-use readiness on an out-of-sample set of research-software repositories, and do its static findings predict practical first-use blockers strongly enough to justify productization?

Three operational decisions followed from this question:

1. whether out-of-sample detector validity was supported by the preregistered static gates;
2. whether predicted static findings corresponded to observed first-use friction in locked dynamic cases; and
3. whether the evidence justified maintainer intervention or a generally deployable GitHub Action.

The study was not designed to estimate documentation quality across all research software. It did not rank repositories, assess scientific merit, or claim that a root README must contain every possible instruction. Its scope was narrower: a conservative test of a specific frozen detector and a specific install-to-first-use construct.

## 3. Frozen detector and preregistered decision gates

The detector and evaluation sequence were frozen before aggregate reference outcomes were evaluated. The baseline commit was `2caeecc8678a4614f6fe6771df0ace6827a5f434`. The study order was: freeze detector and protocol; acquire the issue-121 repositories; generate and hash predictions; create reference labels; evaluate static metrics; lock dynamic cases and tasks; preserve raw attempts; adjudicate; run only permitted corrections; and make intervention and product decisions.

The primary static metrics were precision, recall, specificity, accuracy, F1, and the confusion matrix. The preregistered accuracy gate was 0.750. The study also required acceptable precision for hard findings before automated productization could be considered. This distinction was important. A classifier can obtain perfect positive precision by issuing very few positive classifications. Such a result may reduce one kind of error while producing unacceptable false negatives and poor overall accuracy. Product readiness therefore could not be inferred from precision alone.

The protocol also prohibited outcome-informed tuning. Rules could not be changed after issue-121 results were observed and then re-described as out-of-sample validation. Correction reruns were limited to narrow, documented questions about harness behavior or interpretation. They could not overwrite original attempts or convert a failed static gate into detector success.

## 4. Dataset and eligibility

The sampling source was Journal of Open Source Software issue 121. It contained 39 papers. Thirty-eight linked GitHub repositories met the preregistered eligibility criteria; one GitLab repository was excluded under the host rule. There was no replacement sampling.

The dataset was appropriate for an external test because it was distinct from the issue-122 development pilot. It was not, however, a probability sample of all research software. Repository ecosystems, languages, project maturity, and documentation conventions vary substantially. The results therefore support a decision about this detector on this external dataset, not a population-level prevalence estimate.

The original issue-121 acquisition preserved root README blob hashes and related evidence. A later integrity review identified a provenance limitation: not every sequence of README retrieval and relative-path checks was cryptographically pinned to one immutable repository commit. No observed case was shown to cross revisions, but the possibility was not excluded by construction. Future acquisition code was hardened to resolve one immutable commit before retrieving the README and checking paths. Frozen historical outputs were not rewritten.

## 5. Static evaluation

The detector predicted 7 of 38 repositories as strict-ready. The human reference labeled 24 as strict-ready. The confusion matrix was:

| | Reference strict-ready | Reference not strict-ready |
|---|---:|---:|
| Detector strict-ready | 7 | 0 |
| Detector not strict-ready | 17 | 14 |

The resulting metrics were:

| Metric | Result |
|---|---:|
| Eligible repositories | 38 |
| Predicted strict-ready | 7 |
| Human reference strict-ready | 24 |
| True positives | 7 |
| False positives | 0 |
| True negatives | 14 |
| False negatives | 17 |
| Precision | 1.000 |
| Recall | 0.292 |
| Specificity | 1.000 |
| Accuracy | 0.553 |
| F1 | 0.452 |
| Preregistered accuracy gate | 0.750 - failed |

The detector's precision was numerically perfect because all seven positive predictions agreed with the reference. That did not mean the detector was broadly effective. It identified only 7 of the 24 reference-ready repositories and missed 17. Its conservative decision boundary produced no false-positive readiness classifications but substantial under-detection. Accuracy was approximately 0.553, well below the 0.750 gate, and F1 was approximately 0.452.

The correct interpretation is not that precision is unimportant. Rather, precision answered only one question: when the detector declared strict readiness, how often did the reference agree? It did not answer how much readiness the detector found, whether its negative classifications were useful, or whether its findings predicted actual first-use blockers. The failed accuracy gate and low recall meant the external-validity decision was `NOT SUPPORTED`.

## 6. Dynamic validation design

Static agreement alone could not establish practical validity. The study therefore locked ten dynamic cases before execution. Each case specified a first meaningful task, observable success criterion, allowed documentation scope, environment constraints, and its relation to detector predictions. The selection was feasibility-based rather than representative. Dynamic results were not used to estimate population rates.

The raw attempt status was intentionally simple: `SUCCESS`, `FAILURE`, or `UNTESTABLE_HERE`. Raw evidence included exact commands, exit behavior, logs, timing, memory, disk use, and output observations. A non-zero command did not automatically establish a README defect. Formal adjudication could distinguish:

- a direct README blocker;
- dependency or package compatibility failure;
- a harness error;
- minor friction that did not prevent the first task;
- an optional component failure when the core task succeeded;
- official external-document supplementation; or
- an environment that could not safely test the frozen case.

Raw attempts remained immutable. When a permitted correction was run, it was stored separately with a one-difference rationale and its own evidence hashes.

## 7. Adjudication and correction policy

Adjudication was necessary because execution outcomes are causally ambiguous. A harness can assert the wrong output path. A package release can fail against a newer dependency. A subrepository may require the official parent distribution. A build may target an optional editor while the documented command-line interface already succeeds. Treating all such events as README defects would inflate apparent documentation failure and reward the detector for unrelated problems.

The final status vocabulary was:

- `SUCCESS`;
- `SUCCESS_WITH_FRICTION`;
- `FAILURE_README_BLOCKER`;
- `FAILURE_DEPENDENCY_COMPATIBILITY`;
- `FAILURE_OTHER`; and
- `UNTESTABLE_HERE`.

Corrections were not retries until something worked. They were permitted only for an unambiguous harness error or a predeclared narrow question. The original result stayed visible. Two correction reruns were allowed: one for `sklearn-migrator`, addressing an incorrect invocation and the interpretation of generated paths, and one for Boost.Geometry, testing the root README's explicit delegation to the full Boost distribution. Neither correction altered the detector rules or the reference labels.

## 8. Results

The ten raw attempts produced:

| Raw outcome | Count |
|---|---:|
| `SUCCESS` | 4 |
| `FAILURE` | 5 |
| `UNTESTABLE_HERE` | 1 |

After formal adjudication:

| Final outcome | Count |
|---|---:|
| `SUCCESS` | 6 |
| `SUCCESS_WITH_FRICTION` | 2 |
| `FAILURE_DEPENDENCY_COMPATIBILITY` | 1 |
| `UNTESTABLE_HERE` | 1 |
| `FAILURE_README_BLOCKER` | 0 |
| `FAILURE_OTHER` | 0 |

Nine cases were testable in the available environment. Eight completed their first meaningful task, yielding 8/9 testable first-task successes. The adjudicated sample contained three harness errors, two cases requiring official external-document supplementation, one dependency or compatibility blocker, and zero direct README blockers. None of the three predicted hard findings blocked first use.

These counts do not show that research-software READMEs are generally adequate. The dynamic sample was small and feasibility-selected. They do show that, within the locked test, the static detector's hard findings and negative classifications did not map cleanly onto observed first-use failure. The verdict for the predictive value of static findings was therefore `NOT SUPPORTED`.

## 9. Three dynamically disproved hard findings

The detector emitted three hard findings for `sklearn-migrator`, each treating a referenced relative path as if it were an upstream repository file that should already exist. The paths were:

- `input_model/all_data.json`;
- `input_model/y_pred.csv`; and
- a third generated input-model path recorded in the machine-readable disposition file.

The dynamic review showed that these paths were intended runtime outputs or user-created artifacts in the documented workflow rather than missing repository inputs. The initial harness also used an incorrect import and omitted documented version arguments. A permitted correction used the frozen documented API and completed a serialization/deserialization round trip. All three findings were marked `DISPROVED`.

This is a central failure mode for static documentation analysis. Syntax alone did not reveal the lifecycle of a path. A string that resembles a missing local file may identify a destination produced by a preceding command. Promoting such findings to automated maintainer reports would create false accusations despite the detector's apparently conservative design.

## 10. Harness error, dependency compatibility, and README defect

Three cases illustrate why causal classification mattered.

**GaPFlow.** The simulation completed all 200 steps and wrote timestamped output. The harness then checked a fixed `data/journal` location and returned a non-zero result. The task had succeeded; the assertion was wrong. Final status: `SUCCESS` with a documented harness error.

**WoodTapper.** The published PyPI version failed against changed scikit-learn and Cython internals. A current-source recheck succeeded after an upstream compatibility pin. The failure concerned dependency/package-release compatibility, not a detector finding and not necessarily a direct README defect. Final status: `FAILURE_DEPENDENCY_COMPATIBILITY`.

**Boost.Geometry.** Building only the geometry subrepository omitted headers supplied by the full Boost distribution. The root README delegated users to the official distribution; the same example succeeded there. The initial narrow checkout did not faithfully follow the documented scope. Final status: `SUCCESS_WITH_FRICTION`.

Kigali Sim provided an additional component-scope example. Its core Java command-line interface produced a non-empty CSV. An optional editor build failed because the harness bypassed the documented parser-generation workflow. Calling the entire repository unusable would have collapsed a component-specific harness mistake into a project-level documentation failure.

These distinctions do not excuse unclear documentation. They establish an evidentiary threshold: a README defect should be attributed only when the observed blocker is directly caused by the allowed documentation path and not better explained by environment, dependency drift, harness behavior, optional scope, or explicit delegation.

## 11. Maintainer intervention decision

The intervention phase did not send issue reports or pull requests. Kigali Sim already documented the omitted generation step. WoodTapper's current branch already contained the compatibility pin and warning. The `sklearn-migrator` findings were disproved, and the Boost.Geometry behavior reflected official distribution scope rather than a clear upstream defect.

Submitting reports in these circumstances would have been redundant, low-confidence, or misleading. The study therefore recorded zero contacts, zero accepted upstream corrections, and no measured user-benefit outcome. The maintainer intervention verdict was `INCONCLUSIVE`, not negative evidence against maintainers and not evidence of impact.

The choice not to contact repositories is part of the result. Automated finding systems impose review costs on maintainers. When static evidence fails dynamic scrutiny, restraint is a valid public-interest decision.

## 12. Why productization was stopped

Productization required more than a working command-line program. It required evidence that the detector generalized, that its hard findings were sufficiently reliable, and that its output corresponded to practical first-use problems. Those requirements were not met.

The accuracy gate failed. Recall was low. The three hard findings were false positives after dynamic examination. The locked dynamic sample observed no direct README blocker, while multiple apparent failures were attributable to harness behavior, dependency compatibility, or documentation scope. A GitHub Action would have operationalized these weaknesses by generating automated judgments in third-party repositories.

The formal decision was therefore:

- Detector out-of-sample validity: `NOT SUPPORTED`
- Static findings' predictive value for first-use friction: `NOT SUPPORTED`
- Maintainer intervention actual value: `INCONCLUSIVE`
- Overall productization: `NOT SUPPORTED`
- GitHub Action v0.2: not created and not planned

This does not prohibit all future research on documentation testing. It prohibits presenting this detector, tuned or unchanged on issue-121 evidence, as externally validated. A future detector would require a new question, new frozen implementation, new out-of-sample data, independent reference annotation, preregistered gates, and preserved evidence.

## 13. Threats to validity

### 13.1 Sampling and generalization

The 38 eligible repositories came from one JOSS issue. They were not randomly sampled from all research software. The ten dynamic cases were feasibility-selected. Neither part supports population-level prevalence claims.

### 13.2 Reference annotation independence

One autonomous agent performed the original sequential acquisition and reference annotation. The process was separated from frozen predictions, but it was not an independent second human rater and did not establish inter-rater reliability. AI re-reading of the same material would not repair that limitation.

### 13.3 Construct validity

"Strict-ready" operationalized a narrow install-to-first-use path. Projects may reasonably place details in linked documentation, notebooks, examples, package registries, or domain-specific workflows. The reference policy attempted to respect official delegation, but any binary readiness construct simplifies heterogeneous documentation practice.

### 13.4 Execution environment

Dynamic outcomes depend on operating system, architecture, network availability, dependency resolution, and safety limits. One case remained `UNTESTABLE_HERE`. Dependency failures may change over time, which is why immutable acquisition and environment records are required.

### 13.5 Adjudication discretion

Separating harness errors, component scope, compatibility problems, and README defects requires judgment. The study preserved rationales and raw evidence, but independent reviewers may disagree. Such disagreement should be reported, not hidden.

### 13.6 Multiple roles and conflicts

The same project developed the detector, ran the original validation workflow, and prepared this closeout. The negative decision and frozen evidence reduce incentives for favorable reinterpretation, but independent reproduction remains necessary.

## 14. Original acquisition provenance limitation

The original issue-121 acquisition recorded README blob SHAs but did not guarantee that every README request and every referenced-path check used one repository commit. A default branch can move between requests. No specific case was proven to combine revisions, yet the study cannot cryptographically rule it out.

This limitation was handled conservatively. Historical evidence was not regenerated or silently replaced. Future acquisition now resolves and records one immutable commit, retrieves the README at that commit, and performs path checks against the same commit. The publication distinguishes the frozen historical result from the hardened future protocol.

## 15. Independent replication protocol

Two replication modes should be kept separate.

**Computational reproduction** reruns the published pipeline against the preserved issue-121 artifacts to verify that metrics, hashes, and reports can be reconstructed. It can identify packaging, environment, or script defects. It does not create an independent reference standard if the same labels are reused.

**New-data replication** freezes the detector or another clearly identified implementation before annotation, preregisters a new sampling frame and gates, acquires repositories at immutable commits, locks predictions, and obtains genuinely independent human reference labels. It may reproduce, partially reproduce, contradict, or fail to resolve the original conclusion.

A valid submission should preserve initial annotation, disagreements, raw failed attempts, adjudications, deviations, machine-readable results, and SHA-256 manifests. AI assistance must be disclosed and cannot be counted as a second independent human annotator. Failed and blocked replications are acceptable outcomes.

## 16. Data and code availability

The public repository is `kodlbegiko/research-readme-smoketest`. The formal research tag is `research-closeout-issue-121`, resolving to publication commit `4dfb0b961470974f9dc80a936db86450303d007a`. The repository contains:

- frozen issue-121 predictions and prediction lock;
- reference labels and static results;
- locked dynamic case definitions;
- raw attempts, adjudications, and permitted correction attempts;
- JSON and CSV result files;
- SHA-256 manifests;
- intervention records;
- a machine-readable replication schema; and
- an evidence-governed public-interest log.

The key final checksum command is:

```bash
sha256sum -c results/issue-121/DYNAMIC-FINAL-SHA256SUMS
```

## 17. Citation and archival information

The repository includes `CITATION.cff` using Citation File Format 1.2.0. A GitHub research release has been reported by the owner, but release attributes and attached artifacts should be independently verified before being treated as archival facts in downstream metadata. At the time of this manuscript draft, no verified Zenodo DOI and no verified Software Heritage identifier are recorded. They must not be guessed or represented as complete while pending owner actions.

When a DOI or SWHID is genuinely issued, it should be added through a metadata-only change without modifying frozen evidence or scientific results.

## 18. Conflicts of interest

The author developed and evaluated the original detector and is the repository owner. This role creates an inherent interest in the project's interpretation. The study mitigates, but does not eliminate, that conflict through preregistered gates, frozen predictions, preservation of unfavorable results, separation of raw and adjudicated evidence, prohibition of outcome-informed tuning, and an open invitation for contradictory independent replication.

## 19. Funding statement

No external funding is claimed for this study. If institutional, commercial, or grant support is later identified, the published record should be corrected transparently.

## 20. AI assistance disclosure

AI systems assisted with software implementation, repository inspection, evidence organization, drafting, and editorial review. AI output was not treated as independent human annotation, independent replication, maintainer confirmation, or social-impact evidence. Scientific claims were constrained to preserved repository artifacts and explicit decision rules. The exact tools and interaction logs were not preserved as a complete reproducible record, which is a limitation of the assistance disclosure.

## 21. CRediT contribution statement

**Sean Liu:** Conceptualization; Methodology; Software; Validation; Investigation; Data Curation; Formal Analysis; Visualization; Writing - Original Draft; Writing - Review & Editing; Project Administration; Resources.

**AI-assisted systems:** supporting role in software generation, analysis assistance, documentation drafting, and quality checks; not an author and not an independent annotator or replicator.

## 22. Conclusion

A high precision value did not rescue this detector. Precision of 1.000 described seven correct positive classifications, but the detector missed 17 of 24 reference-ready repositories, achieved accuracy of approximately 0.553, and failed its preregistered 0.750 accuracy gate. Its three hard findings were dynamically disproved. In the locked dynamic sample, 8 of 9 testable cases completed the first meaningful task, and no direct README blocker was observed.

The responsible outcome was to stop productization. There is no GitHub Action v0.2, no tuning on issue-121 outcomes, and no claim that the detector is generally valid. The preserved negative result is more useful than an overstated tool: it shows why static documentation signals require causal adjudication, why raw failures must not be equated with README defects, and why favorable development evidence must survive external validation before automation is imposed on maintainers.

The research remains open to independent computational reproduction, human re-annotation, and new-data replication. Confirmation is not required. Contradiction, partial reproduction, inconclusive evidence, and blocked attempts are all scientifically reportable outcomes.
