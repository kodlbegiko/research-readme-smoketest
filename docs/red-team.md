# Red-team and falsification review

## 1. The problem is not important

**Evidence considered:** installation documentation is the first operational barrier for many software users, and recent empirical studies report unclear or dysfunctional documentation and version incompatibility as recurring installation challenges. Reproducibility guidance also treats the root README as the first file reviewers inspect.

**Finding:** partially rejected. The problem is operationally relevant, but this pilot does not measure downstream scientific error or user abandonment. Importance is therefore `INFERRED`, not directly quantified here.

## 2. The sample is severely biased

JOSS publishes peer-reviewed research software and evaluates open-source practices. This likely selects for documentation quality above the broader GitHub population.

**Finding:** accepted. The sample is narrow and plausibly an upper-quality slice. No prevalence claim beyond the first 20 issue-122 papers is justified.

## 3. Existing tools are already sufficient

Runme executes shell blocks from Markdown; pytest-codeblocks tests Python and shell code blocks. These tools are useful once blocks are executable and suitably annotated.

**Additional comparison:** the selected checker targets missing install-to-first-use composition, conservative cross-language static defects, and strict-versus-external-document delegation. It does not replace execution tools.

**Finding:** partly rejected. Existing tools overlap but do not make the same scoped decision. Integration with them is preferable to competition.

## 4. The metric is wrong

Root README self-sufficiency may be a style preference rather than usability.

**Additional test:** relaxed readiness accepts an explicit external documentation route. Strict readiness is 7/19 (36.8%), while relaxed readiness is 19/19 (100%).

**Finding:** accepted. The strict metric measures root-document self-sufficiency, not whole-project usability. This materially narrows the conclusion.

## 5. The result is a property of this issue

**Evidence:** all cases come from one issue and a five-day publication window.

**Finding:** accepted. Month, journal, domain mix, and issue-order effects are not estimated.

## 6. Information leakage

The rule set was developed while reviewing the same 19 eligible cases used for evaluation.

**Finding:** accepted. The observed 100% proposed classification and hard-defect scores are descriptive fit, not out-of-sample accuracy. An independent issue and second annotator are required.

## 7. The baseline is too weak

The baseline merely requires install plus any runnable-looking non-install block and ignores defects.

**Additional test:** it produced 4 false positives, 0 false negatives, 63.6% precision, and 78.9% accuracy. The proposed rules eliminate those errors on this development sample.

**Finding:** accepted. The baseline is intentionally simple, not state of the art. The useful result is the exact failure analysis, not a claim of superiority over all tools.

## 8. Statistical or numerical processing is wrong

**Checks performed:** exact count assertions, confusion-matrix tests, Wilson interval tests, 65-unit-test suite, repeated deterministic output, and independent recomputation from machine-readable CSV/JSON.

**Finding:** no numerical defect found, but a single implementation and reviewer remain correlated sources of error.

## 9. The result cannot generalize

**Finding:** accepted. The study cannot estimate all JOSS, all research software, or user success rates.

## 10. Maintenance costs exceed value

The checker uses no runtime dependencies and four narrow hard-defect rules. Language ecosystems and documentation conventions will still change.

**Finding:** currently low maintenance, but expanding into general executability would sharply increase complexity. Scope should remain conservative.

## 11. AI-native capability will replace this method

An AI system can interpret prose and infer missing steps, but model outputs are nondeterministic and may silently invent commands. Deterministic preflight remains useful as a CI gate; AI can propose repairs after a finding.

**Finding:** not disproved either way. Replacement is `UNKNOWN`; complementary use is more plausible than direct substitution.

## 12. Maintainers have no adoption incentive

No maintainer study or external installation was conducted.

**Finding:** accepted. Adoption value is `UNKNOWN`. A future study should send issue/PR suggestions only after independent validation and measure acceptance.

## Rule-ablation interpretation

Each observed hard-defect family occurs in one repository. Removing any one rule drops exact hard-defect recall from 100% to 75% on this tiny development sample. This is not evidence that all four rules deserve equal long-term priority; it only shows that no observed family is redundant within the sample.

## Revised conclusion after red team

The pilot supports a narrow claim: **root README install-to-first-use self-sufficiency was below the preregistered threshold in this fixed JOSS sample, and four concrete defects were statically demonstrable.** It does not support a claim that 12 repositories are unusable, that the checker has 100% future accuracy, or that root README completeness causes failed scientific reproduction.
