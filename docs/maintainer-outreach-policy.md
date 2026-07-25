# Maintainer outreach policy

Maintainer contact is not a detector-validation metric and is never automatic. At most two repositories may be contacted in this closeout. Zero contacts is a valid outcome.

## Eligibility gate

Before contact, all conditions must hold:

1. Reproduce the problem on the current default branch or current documented release in a clean environment.
2. Save the current README and relevant-document blob SHAs.
3. Review existing issues and pull requests for the same problem.
4. Exclude harness errors, incomplete use of official build instructions, transient infrastructure failures, and researcher-created path assumptions.
5. Separate dependency or compatibility failures from documentation omissions.
6. Require a correction that does not guess scientific or product intent.
7. Keep the report repository-specific, short, and independently reproducible.

## Contact mode

- Deterministic one-line documentation correction: small pull request.
- Maintainer judgment required: issue.
- Current branch already fixes the problem, duplicate work exists, or uncertainty remains: no contact.

## Message requirements

A message must identify the exploratory external-validation context, environment and versions, minimal reproduction commands, observed result, and exact documentation fragment. It must invite the maintainer to correct the research interpretation. It must not criticize maintainers, demand a refactor, claim detector validation, or characterize submission as impact.

## Outcome accounting

Opening an issue or pull request is not social impact. Record the URL, date, maintainer response, correction or rejection, merge date, false-positive feedback, and measured clean-environment change. Count only accepted corrections, merged fixes, maintainer-provided ground truth, confirmed false positives, or verified improvements.

## Closeout decisions

- `artefactory/woodtapper`: no contact. PyPI 0.0.13 still fails, but current main pins scikit-learn 1.6.1, documents compatibility, installs, and completes first use. Release timing is not treated as a new defect.
- `SchmidtDSE/kigali-sim`: no contact. Official development documentation already contains the ANTLR generation flow omitted by the harness.
