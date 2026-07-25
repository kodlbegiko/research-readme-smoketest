# Preregistered pilot methodology

Protocol frozen before calculating the aggregate result.

## Research question

In the first 20 papers listed in JOSS issue 122 (June 2026), what proportion of linked GitHub research-software repositories provide a copyable root-README path from installation/build to first meaningful use, and can a conservative static preflight identify unambiguous defects without treating external documentation or missing examples as hard errors?

## Hypotheses

- **H1:** Fewer than 70% of eligible GitHub repositories are strict root-README ready. Support requires at least 15 eligible repositories and the upper bound of a two-sided 95% Wilson interval below 70%.
- **H0:** At least 70% are strict root-README ready, or the sample is too small to distinguish H1 from H0.
- **H2:** A low strict rate is substantially explained by maintainers delegating first-use material to external documentation. The sensitivity definition therefore counts a repository as relaxed-ready when it is strict-ready **or** the root README provides a concrete external documentation/tutorial route.

## Operational definitions

### Eligible repository

A paper among the first 20 entries in issue order whose linked software repository is hosted on GitHub and whose root README can be retrieved. Non-GitHub hosting is excluded because the acquisition and path-verification protocol was fixed to GitHub.

### Safe installation block

A root-README fenced or indented command block that contains a recognizable installation/build command and has none of the preregistered hard defects or unexplained angle-bracket substitutions.

### Safe first-use block

A root-README code/command block under a usage, quick-start, example, run, or first-time-user context that invokes the software or gives a concrete language example, without preregistered hard defects or unexplained substitutions. A single quick-start block may satisfy both installation and first use.

### Strict root-README ready

At least one safe installation block **and** at least one safe first-use block exist in the root README.

This definition intentionally tests root-document self-sufficiency. It does **not** assert that a project without such a path is unusable or irreproducible overall.

### Relaxed-ready

Strict-ready, or the root README provides an explicit route to external installation, getting-started, tutorial, package, or product documentation.

### High-confidence hard defects

Only four families were eligible:

1. `git clone` has options but no repository target;
2. a README-referenced relative path was independently checked and absent;
3. `sudo apt get` is used instead of `apt-get` or `apt`;
4. an ES-module JavaScript example assigns a newly constructed object to an undeclared identifier.

Missing examples, external documentation, platform prerequisites, dynamic versions, placeholders that are explained, and commands requiring specialized scientific inputs are not classified as hard defects.

## Dataset and sampling

- Frame: JOSS issue 122, June 2026.
- Rule: first 20 papers in official issue order; no replacement after viewing results.
- Public source: <https://joss.theoj.org/toc/issue/122>.
- Unit: one linked software repository per paper.
- Frozen metadata: `data/raw/source-records.json`.
- Extracted, manually reviewed blocks and labels: `data/processed/readme-blocks.json`.
- Personal data: none intentionally collected.
- Copyright minimization: the dataset stores short command/example fragments, repository names, DOI identifiers, README blob hashes, and labels rather than full third-party READMEs.

## Baseline

The naive baseline marks a repository ready when it has an installation block plus any non-install code block classified as first-use, test, or development. It does not apply hard-defect rules. This represents a low-cost “README contains install plus some runnable-looking code” heuristic.

## Procedure

1. Freeze the first 20 issue entries and linked repositories.
2. Exclude non-GitHub repositories under the prespecified acquisition scope.
3. Retrieve the root README and record its Git blob SHA.
4. Extract candidate command/code blocks with their nearest heading.
5. Verify only referenced paths needed for hard-defect labels.
6. Assign manual strict-readiness and hard-defect labels before aggregate calculation.
7. Run the naive baseline and conservative preflight against the frozen dataset.
8. Compute strict and relaxed rates, 95% Wilson intervals, confusion matrices, and defect precision/recall.
9. Run deterministic reproduction under different `PYTHONHASHSEED` values.
10. Red-team the interpretation, especially the strict-versus-relaxed definition and same-sample rule development.

## Metrics

- strict-ready count and proportion;
- relaxed-ready count and proportion;
- repositories with at least one high-confidence hard defect;
- Wilson 95% intervals for strict readiness and defect-repository rate;
- baseline and proposed precision, recall, specificity, accuracy, F1, FP, and FN against manual labels;
- exact defect-pair precision and recall;
- processing time and peak Python allocation as machine-specific secondary measures;
- byte determinism of JSON and CSV outputs.

## Stopping rule

- Stop after the first 20 issue entries; do not add cases to improve significance.
- If fewer than 15 eligible GitHub repositories remain, classify the main hypothesis as `INCONCLUSIVE`.
- If the static labels require executing specialized software or interpreting scientific correctness, classify those cases as unknown rather than expanding the checker.
- If existing tools already provide the same conservative cross-language root-path analysis, stop and report duplication. The related-work review found executable-Markdown and language-specific code-block tools, but not the same scoped distinction.

## Decision rule

- `SUPPORTED`: H1's sample and Wilson criteria both pass, while limitations remain explicit.
- `NOT SUPPORTED`: strict readiness is at least 70%, or the Wilson upper-bound criterion fails with adequate sample.
- `INCONCLUSIVE`: fewer than 15 eligible cases or labels cannot be made credible.
- `BLOCKED`: public acquisition or execution constraints prevent a credible test.
