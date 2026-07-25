# Owner actions: research release and permanent archive

The connected GitHub tooling used for this closeout cannot create tags, releases, Zenodo deposits, OSF records, or DOIs. Complete the following manually after the publication PR is merged and final `main` CI is green.

## 1. Record the final source commit

On GitHub, open the merged publication PR and copy its merge commit SHA. Confirm that `main` points to the same commit.

Do not use the earlier evidence-only merge commit if publication documents are missing from it.

## 2. Create the research tag

Create an annotated tag at the exact final `main` commit:

```bash
git fetch origin main
git checkout main
git pull --ff-only origin main
git tag -a research-closeout-issue-121 \
  -m "Issue 121 external validation negative research closeout"
git push origin research-closeout-issue-121
```

Confirm on GitHub that the tag points to the recorded final commit. Do not use `v0.2.0` or another product-version label.

## 3. Verify evidence before release

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest
pytest --cov
python -m build
sha256sum -c results/issue-121/DYNAMIC-FINAL-SHA256SUMS
```

Stop if any command fails.

## 4. Create the GitHub release

Tag:

```text
research-closeout-issue-121
```

Title:

```text
Issue 121 External Validation — Negative Research Closeout
```

Use this release description:

```markdown
## Research status

External validation did **not** support productization of the frozen v0.1.0 detector. This release is a reproducible negative research result, not a recommended README checker or GitHub Action.

## Results

- Detector out-of-sample validity: `NOT SUPPORTED`
- Static findings' predictive value for first-use friction: `NOT SUPPORTED`
- Maintainer intervention actual value: `INCONCLUSIVE`
- Overall productization: `NOT SUPPORTED`
- GitHub Action v0.2: not created and not planned

The issue-121 static evaluation covered 38 eligible GitHub repositories. Precision was 1.0, recall approximately 0.292, accuracy approximately 0.553, and the preregistered 0.75 accuracy gate was not met. Three predicted hard findings were disproved.

Ten dynamic cases were locked before execution. Raw attempts and correction attempts are preserved separately. Eight of nine testable cases completed the first meaningful task after adjudication; no predicted hard finding became a first-use blocker, and no direct README blocker was observed in this feasibility-selected sample.

## Limitations

- The ten dynamic cases do not support population inference.
- One autonomous agent performed the original sequential reference annotation; this is not independent inter-rater validation.
- The original issue-121 acquisition preserved README blob SHAs but did not cryptographically pin every cross-request path check to a single repository commit. The acquisition code is hardened for future replication; frozen historical outputs remain unchanged.
- Independent reproduction and independent human re-annotation counts were zero at closeout.
- No maintainer acceptance, merged correction, or measured user benefit is claimed.

## Verify

Run:

`sha256sum -c results/issue-121/DYNAMIC-FINAL-SHA256SUMS`

See `EXTERNAL-VALIDATION.md`, `REPLICATION.md`, `PUBLIC-INTEREST.md`, and `docs/archival-plan.md`.
```

Attach these files from the tagged commit:

- `results/issue-121/dynamic-validation-results.json`
- `results/issue-121/dynamic-validation-results.csv`
- `results/interventions/intervention-log.json`
- `results/interventions/intervention-log.csv`
- `results/issue-121/DYNAMIC-FINAL-SHA256SUMS`
- `research-manifest-issue-121.yml`
- `EXTERNAL-VALIDATION.md`

Do not describe download counts as impact.

## 5. Archive with Zenodo

1. Sign in to Zenodo using GitHub.
2. Enable the repository in Zenodo's GitHub integration.
3. Create the GitHub release above.
4. Wait for Zenodo to ingest the tagged release.
5. Inspect title, authors, abstract, license, keywords, related identifiers, and files.
6. Ensure the record says `negative external-validation result` and `not a product`.
7. Publish the deposit.
8. Record both concept DOI and version DOI.
9. Open a metadata-only PR adding the DOI to `CITATION.cff` and `docs/archival-plan.md`.

Do not insert a guessed or reserved DOI as if it were published.

## 6. Additional preservation

- Save the final repository or commit through Software Heritage and record the SWHID.
- Optionally mirror the release package to OSF or an institutional repository.
- Preserve the final source commit, release tag, archive identifiers, and checksum manifest together.

## Completion record

After all actions, update this section in a metadata-only PR:

```text
final main commit: <SHA>
research tag: research-closeout-issue-121
GitHub release URL: <URL>
Zenodo concept DOI: <DOI or NOT CREATED>
Zenodo version DOI: <DOI or NOT CREATED>
Software Heritage SWHID: <SWHID or NOT RECORDED>
OSF/institutional archive: <URL or NOT CREATED>
completed by: <person>
completed at UTC: <timestamp>
```
