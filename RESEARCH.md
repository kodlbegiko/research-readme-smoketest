# Root README install-to-first-use paths in a JOSS pilot

## Abstract

This exploratory study tests whether root READMEs in recently published research software provide a copyable path from installation/build to first meaningful use. The sampling frame was frozen as the first 20 papers in Journal of Open Source Software issue 122 (June 2026). Nineteen linked repositories were hosted on GitHub and eligible. A manual protocol and dependency-free static preflight distinguished safe installation blocks, safe first-use blocks, explicit external documentation, unexplained substitutions, and four high-confidence defect families. Seven of 19 repositories (36.8%; Wilson 95% CI 19.1%–59.0%) met the strict root-README definition, below the preregistered 70% threshold. All 19 met a relaxed definition that accepts an explicit external documentation/tutorial route. Four repositories (21.1%; Wilson 95% CI 8.5%–43.3%) contained a statically demonstrable defect. A naive baseline produced four false positives; the proposed rules matched manual labels on the same development sample. The result supports only a narrow conclusion about root-document self-sufficiency. It does not show that non-strict repositories are unusable, nor does it establish out-of-sample checker accuracy.

## Background

Installation documentation is not merely descriptive: it is an operational dependency for first use. Gao, Treude, and Zahedi studied 400 GitHub repositories and 1,163 README commits involving installation sections, identifying errors in previous documentation, codebase changes, and documentation improvement as major update triggers. A 2026 study of novice installation sessions reported unclear or dysfunctional documentation, complicated processes, incompatibilities, and lack of feedback as recurring barriers.

Reproducibility guidance often makes the root README the entry point. The American Political Science Association tells authors to assume it is the first file examined and requires instructions for recreating the software environment and running code. Existing executable-documentation tools address adjacent problems: Runme parses shell blocks from Markdown, and pytest-codeblocks executes Python and shell blocks. They do not by themselves decide whether a root document composes installation and first use, whether an external tutorial is an intentional delegation, or whether a short cross-language fragment contains one of the high-confidence defects defined here.

JOSS is an intentionally strong sampling frame: it is a peer-reviewed journal for research software and considers open-source practices. That makes the sample relevant but biased toward projects likely to be better documented than arbitrary GitHub repositories.

## Research question

In the first 20 papers listed in JOSS issue 122, what proportion of linked GitHub research-software repositories provide a copyable root-README path from installation/build to first meaningful use, and can a conservative static preflight identify unambiguous defects without treating external documentation or missing examples as hard errors?

## Hypotheses

- **H1:** strict root-README readiness is below 70%; support additionally requires at least 15 eligible cases and a 95% Wilson upper bound below 70%.
- **H0:** strict readiness is at least 70%, or the evidence cannot distinguish H1 from H0.
- **H2:** strict incompleteness is substantially explained by external-document delegation rather than proven project unusability.

## Related work

- Installation README evolution: Gao et al., IEEE TSE 2025, DOI `10.1109/TSE.2025.3552614`.
- Novice installation challenges: Salerno, Treude, and Thongtanunam, Empirical Software Engineering 2026, DOI `10.1007/s10664-026-10885-5`.
- Executable Markdown: Runme CLI documentation, <https://docs.runme.dev/getting-started/cli/>.
- README code-block execution: pytest-codeblocks, <https://pypi.org/project/pytest-codeblocks/>.
- Reproducibility README expectations: APSA guidelines, <https://apsanet.org/publications/journals/american-political-science-review/guidelines-for-reproducibility/>.
- Sampling frame: JOSS issue 122, <https://joss.theoj.org/toc/issue/122>.

## Methods

The detailed frozen protocol is in `docs/methodology-preregistered.md`.

### Data

The official issue page listed 47 papers. The first 20 in issue order were selected without replacement. Nineteen linked to GitHub; Cosmologix linked to GitLab and was excluded under the GitHub-only acquisition protocol. Repository names, DOI identifiers, README Git blob hashes, extracted blocks, manually verified referenced-path existence, and labels are stored in JSON.

The extraction set is deliberately minimal. Full READMEs are not copied into the repository. This reduces redistribution and makes the benchmark stable, but it also prevents reinterpreting prose context without reacquisition.

### Manual labels

A repository was strict-ready when its root README contained at least one safe installation/build block and at least one safe first-use block. A block could serve both roles. Unexplained `<placeholder>` substitutions and hard defects made that block unsafe; another safe block could still satisfy the role.

The four hard-defect families were selected because they can be supported by direct syntax or repository-path evidence:

1. incomplete `git clone` target;
2. verified absent relative path;
3. `sudo apt get` typo;
4. undeclared assignment in an ES-module JavaScript example.

A repository was relaxed-ready if strict-ready or if the root README explicitly routed users to external documentation, a tutorial, package documentation, or a product guide.

### Baseline

The naive rule required an installation block and any runnable-looking non-install block, including tests or development setup, with no defect analysis. It intentionally represents a common but weak proxy: “there is install text and some code.”

### Analysis

The CLI parses the frozen JSON into typed records, classifies every block into one or more roles, detects preregistered defects, computes per-repository states, and writes deterministic JSON/CSV. Aggregate proportions use two-sided Wilson intervals. Manual labels are used as a development-set reference, not an independent test set.

## Results

### Main counts

| Metric | Result |
|---|---:|
| Papers sampled | 20 |
| Eligible GitHub repositories | 19 |
| Strict-ready | 7 (36.8%) |
| Strict-ready Wilson 95% CI | 19.1%–59.0% |
| Relaxed-ready | 19 (100%) |
| Repositories with hard defects | 4 (21.1%) |
| Hard-defect repository Wilson 95% CI | 8.5%–43.3% |

The H1 stopping and support criteria were met: 19 eligible cases exceeded the minimum of 15, and the upper Wilson bound for strict readiness was 59.0%, below the preregistered 70% threshold.

### Baseline comparison

| Method | TP | FP | TN | FN | Precision | Recall | Accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| Naive install + any runnable-looking block | 7 | 4 | 8 | 0 | 63.6% | 100% | 78.9% |
| Conservative preflight | 7 | 0 | 12 | 0 | 100% | 100% | 100% |

The conservative score is an in-sample descriptive fit. The same cases informed rule construction and evaluation, so these numbers must not be treated as expected production performance.

### Hard defects

Four exact defect pairs were manually labeled and detected:

- CGView.js: an ES-module example assigns `new CGView.Viewer(...)` to undeclared `cgv`;
- FAIRLinked: one example references `rresources/.../pmma_no_metadata_rows.csv`, while the verified repository path begins `resources/...`;
- liblsl.dart: `git clone --recurse-submodules` lacks a repository target;
- PAI: Linux requirements include `sudo apt get update`.

These findings do not invalidate the entire README. FAIRLinked and PAI still had separate safe install-to-first-use paths and therefore remained strict-ready.

## Error analysis

The naive baseline's four false positives came from distinct mechanisms:

1. CGView.js had install plus usage but the usage fragment contained a hard JavaScript defect.
2. Vibrant had build instructions plus a regression-test command, but no root-README first use of the product.
3. TikhonovFenichelReductions.jl had installation plus unit-test instructions, with practical use delegated externally.
4. PAI was initially vulnerable to a mutually exclusive block-role implementation; allowing one quick-start block to satisfy both install and first use corrected that analysis defect before the protocol output was frozen.

The final point is a recorded implementation failure, not a repository defect. It motivated multi-role block classification and dedicated regression tests.

## Sensitivity analysis

Accepting explicit external documentation changes readiness from 7/19 to 19/19. This is not a minor numerical adjustment; it changes the interpretation from “most projects lack an entry path” to “most projects route the entry path outside the root README.” Therefore:

- `KNOWN`: strict root self-sufficiency is uncommon in this sample under the frozen definition.
- `KNOWN`: all eligible root READMEs provide either a strict path or an external route.
- `INFERRED`: a reader restricted to the repository root experiences more friction than a reader willing and able to follow external links.
- `UNKNOWN`: whether external routes are current, accessible, complete, or successful for real users.

## Performance and reproducibility

On the audit container, 1,000 in-process analyses had a median time of about 0.00238 seconds and peak `tracemalloc` allocation of 52,309 bytes. These values are machine-specific and excluded from the deterministic result hash.

The canonical JSON result hash is:

```text
531f145706238996c499746bdb46c9f4d281221828b4f07691c68782ca2f80f8
```

Runs under `PYTHONHASHSEED=0` and `PYTHONHASHSEED=321` produce byte-identical JSON and CSV.

## Threats to validity

### Construct validity

Strict readiness is a deliberately narrow construct. It is not total documentation quality, scientific correctness, installation success, or reproducibility.

### Internal validity

One annotator extracted and labeled the data. Rule development and evaluation share the same sample. Manual errors and rule overfitting can therefore inflate apparent accuracy.

### External validity

The sample covers one JOSS issue, the first 20 entries, current default-branch READMEs, and 19 GitHub repositories. Domains, languages, and repository structures are heterogeneous but not representative by statistical design.

### Temporal validity

READMEs can change after retrieval. Blob hashes preserve what was reviewed, but the study does not reconstruct publication-time documentation.

### Execution validity

The study does not install and execute all projects. Such an experiment would require incompatible language toolchains, large scientific dependencies, containers, datasets, and domain-specific success criteria. Static hard defects are stronger than speculative executability claims but narrower.

## Ethical and safety considerations

All evidence came from public repositories. No secrets or personal records were intentionally collected. The report names repositories because the observations are directly verifiable documentation facts, but it avoids claims about maintainer competence, software security, or scientific validity. Any future outreach should invite correction and should not mass-file issues before independent replication.

## Negative results

- The checker cannot determine whether external documentation actually works.
- It cannot prove scientific examples are semantically correct.
- It cannot evaluate dynamic, interactive, GUI, HPC, or data-dependent onboarding by static text alone.
- It cannot claim out-of-sample 100% accuracy.
- A simple root-readiness metric alone would be misleading; the relaxed sensitivity entirely changes the practical interpretation.

## Conclusion

**SUPPORTED — The pilot evidence supports the stated hypothesis within the documented scope and limitations.**

Seven of 19 eligible repositories met the strict root-README install-to-first-use definition, and the 95% Wilson upper bound remained below the preregistered 70% threshold. Four high-confidence documentation defects were found. However, all 19 repositories supplied either a strict path or an explicit external documentation route. The credible contribution is therefore a reproducible distinction among root self-sufficiency, external delegation, and concrete static defects—not a claim that most sampled research software is unusable.

## Future work

The next credible step is a preregistered out-of-sample evaluation on a later JOSS issue, with two independent annotators and user-task observation for a small stratified subset. The rule set should remain frozen for that test. External documentation should be separately checked for link availability and one concrete first-use task, rather than folded into the root README score.
