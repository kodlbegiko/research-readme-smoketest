# Dynamic first-use task protocol

## Objective

Measure whether frozen static labels predict practical friction between opening the root README and obtaining one meaningful end-user output.

## Case selection

Select 8–12 cases after prediction and reference labels are locked. Stratify across predicted strict-ready/non-strict, external delegation, hard findings, prediction disagreements, ecosystems, CLI/library products, and feasible resource requirements.

Selection is feasibility-aware but not outcome-aware. Record every considered case and exclusion reason.

## Safety gate

Before execution:

1. inspect all proposed commands and package scripts;
2. reject commands requiring elevated privileges, secrets, external credentials, destructive writes, unrestricted remote scripts, or opaque binaries;
3. isolate each case in a fresh container or equivalent disposable environment;
4. cap CPU, memory, disk, and wall-clock duration;
5. do not execute repository code on the maintainer workstation.

## First meaningful task

Define a single concrete task before installation. It must produce an observable product-level result rather than only passing tests or importing a module, unless import/initialization is the documented primary first use.

## Recorded fields

- repository and acquired README SHA;
- environment image, OS, architecture, language/toolchain versions;
- predeclared task and success criterion;
- exact commands and ordered documentation pages used;
- installation duration and total time to first output;
- manual step count, external search count, and non-root-document page count;
- stdout/stderr excerpts and exit codes;
- peak memory and disk use when measurable;
- success, failure, or `UNTESTABLE HERE`;
- static finding relation: direct blocker, material friction, minor friction, unrelated, externally repaired, or not exercised;
- unexpected safety or reproducibility observations.

## Interpretation

A static finding predicts friction only when the documented path exercises it or a reasonable new user would select it, and correcting or bypassing it measurably changes the task. Infeasible GPU/HPC/restricted-data/GUI cases are not failures. External docs may repair a root README gap and must be reported separately.

## Stopping

Stop an individual case on safety concern, repeated non-documentation infrastructure failure, resource cap, or when success/failure is established. Do not silently change the task after observing results.