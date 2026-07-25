# Draft: research community post

## Negative results from external validation of a static research-software README checker

We are releasing the closeout materials for an external validation of a frozen static detector for install-to-first-use paths in research-software root READMEs.

The detector's out-of-sample validity was not supported. Across 38 eligible GitHub repositories, precision was 1.0, but recall was approximately 0.292 and accuracy approximately 0.553, below a preregistered 0.75 gate. Seventeen of 24 reference-ready repositories were missed. Three predicted hard defects were false positives and were dynamically disproved.

A preregistered ten-case dynamic validation also failed to show that the static findings predicted first-use blockers. Eight of nine testable cases completed their first meaningful task. Adjudication identified harness errors, dependency compatibility failures, component-scope issues, and external-document supplementation that would have been incorrectly collapsed into repository or README failure without evidence review.

The main contribution is methodological rather than a new tool. The repository preserves prediction locks, raw attempts, adjudications, corrections, checksums, intervention decisions, and a protocol for independent replication. It also records an explicit decision not to create a GitHub Action v0.2.

The sample is small and feasibility-selected, and one autonomous agent performed the sequential original reference annotation. No population claim or independent inter-rater claim is made. Independent reproduction and human re-annotation counts begin at zero.

We invite preregistered replications that use new data, independently controlled annotation, immutable acquisition commits, and preserved failed attempts. Confirming, contradicting, inconclusive, and blocked outcomes are all acceptable.
