# Maintainer outreach policy

No upstream maintainer may be contacted merely because the detector emits a finding.

## Eligibility checklist

All boxes must be true:

- finding is present in the current default-branch root README at a recorded blob SHA;
- the frozen rule emitted it before reference annotation;
- the reference annotator independently rechecked the exact fragment;
- repository path evidence is verified when applicable;
- dynamic reproduction was attempted when safely feasible;
- the correction does not require guessing product or scientific intent;
- no open or recently merged issue/PR already covers the same defect;
- the proposed message is specific to that repository.

## Contact mode

- one-line deterministic correction: small pull request;
- maintainer judgment required: issue;
- uncertainty remains: no contact.

At most five repositories may be contacted in this study.

## Required message content

- exact current README fragment or command;
- observed failure or syntax/path evidence;
- reproduction environment when available;
- minimal suggested correction;
- disclosure that the report comes from an exploratory documentation-validation study;
- invitation to correct the study's interpretation.

Do not criticize maintainer competence, imply a security vulnerability, mass-file templated reports, or claim scientific invalidity.

## Outcomes

Submission alone is not impact. Record URL, date, response, requested changes, acceptance/rejection, merge date, false-positive feedback, and resolution time. Count only merged documentation fixes, accepted corrections, confirmed false positives, maintainer-provided ground truth, or measured clean-environment improvement as intervention outcomes.