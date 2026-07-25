# Annotation guide v1

Status: frozen for JOSS issue 121 reference labeling.

## Unit of analysis

One JOSS paper-linked software repository and its current default-branch root README at the acquired Git blob SHA.

## Evidence statuses

- `KNOWN`: directly supported by README syntax, repository path lookup, or observed execution.
- `INFERRED`: plausible interpretation requiring assumptions.
- `UNKNOWN`: evidence is insufficient.
- `DISPROVED`: tested claim is false.
- `UNTESTABLE HERE`: current safe environment cannot test it.

Only `KNOWN` evidence can create a manual hard-defect label.

## Block extraction

Record fenced code blocks with their nearest preceding heading, language tag, exact short text, referenced relative paths, and whether angle-bracket substitutions are explicitly explained. Do not redistribute full READMEs.

## Safe installation/build path

Mark true when at least one root-README block provides a concrete installation or build operation and the block has neither a frozen hard defect nor an unexplained angle-bracket substitution. Package-manager commands, environment creation, source builds, and complete clone commands may qualify.

## Safe first meaningful use

Mark true when at least one root-README block gives a concrete end-user invocation or a language example under an explicit usage/example/quick-start context, and the block has neither a frozen hard defect nor an unexplained substitution. Test, lint, benchmark-maintainer, and contribution-only commands do not qualify by themselves.

## Strict and relaxed readiness

- `strict_ready = safe_installation AND safe_first_meaningful_use`.
- `external_docs = root README explicitly links or routes the reader to documentation, tutorial, vignette, package guide, or product guide relevant to setup or use`.
- `relaxed_ready = strict_ready OR external_docs`.

A repository may contain a hard defect in one block and still be strict-ready through separate safe blocks.

## Frozen hard defects

### Missing clone target

A non-comment line begins with `git clone`; after removing command options, no repository/path target remains.

### Verified missing relative path

A code block references a repository-relative path, and an exact lookup at the acquired default-branch commit confirms the path is absent. Do not infer absence from spelling alone.

### `sudo apt get`

A non-comment command contains the token sequence `sudo apt get`.

### Undeclared ES-module assignment

A JavaScript/TypeScript fenced block contains an `import` statement and assigns `new ...` to a bare identifier not declared in that block with `const`, `let`, or `var`.

## Uncertainty

Do not label API semantics, dependency compatibility, scientific validity, external link freshness, GUI behavior, required data availability, or platform support as hard defects without direct evidence. Preserve these as notes and route feasible cases to dynamic testing.

## Reference annotation fields

For each repository record:

- acquisition identifiers and README SHA;
- safe installation/build;
- safe first meaningful use;
- strict-ready;
- external docs;
- relaxed-ready;
- unexplained placeholder blocks;
- hard defects, each with heading, language, excerpt, rationale, evidence status, and dynamic-test need;
- uncertainty notes;
- annotation duration.

## Independence limitation

The primary reference set is single-annotator unless a distinct human independently labels it. Repeated model passes are quality checks, not inter-rater evidence.