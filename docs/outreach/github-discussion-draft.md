# Draft: GitHub Discussion

## A README checker passed its development sample and failed external validation

We tested a frozen static checker intended to identify research-software root READMEs with a safe path from installation to first meaningful use.

On 38 eligible repositories from a new JOSS issue, the checker achieved precision 1.0 but recall about 0.292 and accuracy about 0.553, below the preregistered 0.75 accuracy gate. It missed 17 reference-ready repositories. Three predicted hard findings were also disproved by manual review and a correction rerun.

A locked ten-case dynamic study reinforced the negative result. Eight of nine testable cases completed the first meaningful task, no predicted hard finding became a blocker, and no direct README blocker was observed. Several apparent failures were instead harness errors, dependency compatibility problems, optional-component build issues, or cases repaired by official external documentation.

We therefore stopped productization. There will be no GitHub Action v0.2 and no retuning on the evaluation dataset.

The repository now preserves the prediction lock, raw attempts, formal adjudications, correction attempts, checksums, and an independent-replication protocol. The useful question is not whether the detector can be made to look better on the same data, but whether another independently designed study reproduces or contradicts the result.

Feedback is welcome on the methodology, evidence boundaries, and replication protocol. GitHub activity alone will not be counted as impact, and a differing result is as useful as a confirming one when the evidence is preserved.
