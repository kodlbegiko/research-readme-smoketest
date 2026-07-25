# Public dissemination pack

**Status:** DRAFTS ONLY - zero posts sent from this repository workflow.  
**Use condition:** insert a verified DOI only after Zenodo publication. Until then, state `DOI pending` and link the formal GitHub Release.  
**Release:** https://github.com/kodlbegiko/research-readme-smoketest/releases/tag/research-closeout-issue-121  
**Replication protocol:** https://github.com/kodlbegiko/research-readme-smoketest/blob/main/docs/independent-replication-protocol.md

## 1. Research software engineering community

### Draft

We published a negative external-validation result for a static checker that assessed whether research-software root READMEs offered a copyable path from installation to first meaningful use.

The detector looked strong on one metric: precision was 1.000. But it classified only 7 repositories as strict-ready while the human reference classified 24. Recall was approximately 0.292, accuracy approximately 0.553, and the preregistered accuracy gate was 0.750. High precision was not enough because the detector missed 17 of 24 reference-ready repositories.

The practical check was also unfavorable. Three predicted hard findings were dynamically disproved. Across ten locked dynamic cases, 8 of 9 testable cases completed their first meaningful task, and no direct README blocker was observed. Several apparent failures were instead harness errors, dependency compatibility problems, component-scope mismatches, or cases where the root README delegated to official documentation.

We therefore stopped productization. This is not a recommended checker, and no GitHub Action v0.2 is planned.

The release preserves predictions, locks, raw attempts, adjudications, correction reruns, JSON/CSV results, and checksums. Independent computational reproduction, human re-annotation, and new-data replication are welcome. A replication may support, partly support, contradict, remain inconclusive, or be blocked.

External outcomes currently remain zero: 0 independent reproductions, 0 independent human re-annotations, 0 external citations, 0 accepted upstream corrections attributable to the closeout, and 0 measured user-benefit outcomes.

Release: https://github.com/kodlbegiko/research-readme-smoketest/releases/tag/research-closeout-issue-121  
Replication protocol: https://github.com/kodlbegiko/research-readme-smoketest/blob/main/docs/independent-replication-protocol.md  
DOI: [PENDING - INSERT ONLY AFTER VERIFIED PUBLICATION]

## 2. Open science and reproducibility community

### Draft

A negative result is only useful when the unfavorable evidence remains inspectable.

Research README Smoketest v0.1.0 was frozen before an external validation on 38 eligible GitHub repositories. It achieved precision of 1.000, but recall of approximately 0.292 and accuracy of approximately 0.553. The preregistered accuracy gate was 0.750, so detector validity was not supported. Three predicted hard findings were later disproved under a narrow, evidence-preserving correction policy.

A ten-case dynamic validation kept raw attempts separate from adjudication. The raw record contained five failures; after examining commands, outputs, documentation scope, dependencies, and harness behavior, the final result was 6 successes, 2 successes with friction, 1 dependency-compatibility failure, and 1 case untestable in the available environment. No direct README blocker was observed, and 8 of 9 testable first tasks succeeded.

The project did not retune the detector on the external dataset and did not turn the negative result into a product. No GitHub Action v0.2 is planned. The repository includes prediction locks, immutable evidence, formal adjudications, checksums, a replication schema, and an impact log that begins at zero rather than treating stars, views, or downloads as social benefit.

Independent results do not need to agree with the original conclusion. Reproduced, partially reproduced, contradicted, inconclusive, and blocked outcomes are all accepted if the evidence and deviations are preserved.

Release: https://github.com/kodlbegiko/research-readme-smoketest/releases/tag/research-closeout-issue-121  
Replication protocol: https://github.com/kodlbegiko/research-readme-smoketest/blob/main/docs/independent-replication-protocol.md  
DOI: [PENDING - INSERT ONLY AFTER VERIFIED PUBLICATION]

Current verified external outcomes: all zero.

## 3. Empirical software engineering and documentation research community

### Draft

We report an external-validation failure that illustrates why classifier precision cannot substitute for construct and predictive validity in documentation research.

A frozen static detector evaluated root-README install-to-first-use readiness across 38 eligible research-software repositories. Confusion matrix: TP 7, FP 0, TN 14, FN 17. Precision was 1.000, recall approximately 0.292, specificity 1.000, accuracy approximately 0.553, and F1 approximately 0.452. The preregistered accuracy gate of 0.750 failed.

The detector also emitted three hard findings that treated relative paths as missing repository inputs. Dynamic review showed that the paths were workflow-generated artifacts; all three findings were disproved. In ten preregistered dynamic cases, no direct README blocker was observed, while harness errors, dependency drift, optional-component scope, and explicit external-document delegation materially changed adjudication.

The resulting decisions are intentionally unfavorable: out-of-sample detector validity not supported; predictive value for first-use friction not supported; maintainer intervention value inconclusive; productization not supported. The feasibility-selected dynamic sample is not represented as a population sample, and the original sequential annotation is not described as independent inter-rater evidence.

The full evidence package and a machine-readable replication schema are available. We invite independent computational reproduction, human re-annotation, and new-data replication, including contradictory results.

Release: https://github.com/kodlbegiko/research-readme-smoketest/releases/tag/research-closeout-issue-121  
Replication protocol: https://github.com/kodlbegiko/research-readme-smoketest/blob/main/docs/independent-replication-protocol.md  
DOI: [PENDING - INSERT ONLY AFTER VERIFIED PUBLICATION]

Verified external outcomes at launch: 0 reproductions, 0 independent re-annotations, 0 citations, 0 attributable accepted corrections, and 0 measured user-benefit outcomes.
