# Archival and dissemination status

Last reviewed: 2026-07-26  
Study: `joss-issue-121-external-validation`  
Repository: `kodlbegiko/research-readme-smoketest`

## Current research state

```text
PRESERVED AS NEGATIVE RESEARCH
OPEN FOR INDEPENDENT REPLICATION
NOT A PRODUCT
NO GITHUB ACTION V0.2
NO OUTCOME-INFORMED TUNING
```

## Phase 0 verification record

| Check | Status | Evidence / limitation |
|---|---|---|
| `main` exact commit | VERIFIED | `4dfb0b961470974f9dc80a936db86450303d007a` |
| Tag resolves to publication commit | VERIFIED | `research-closeout-issue-121` resolves to the same commit |
| Tag object is annotated | PENDING INDEPENDENT VERIFICATION | Current connector resolves the tag but does not expose the Git object type |
| Repository is public | VERIFIED | Public repository metadata |
| Repository is not archived read-only | VERIFIED | `archived=false` |
| README states negative result | VERIFIED | Root README status block |
| README states productization not supported | VERIFIED | Root README status block and final decisions |
| README states GitHub Action not planned | VERIFIED | Root README status block and product decision |
| Final evidence manifest exists | VERIFIED | `results/issue-121/DYNAMIC-FINAL-SHA256SUMS` |
| Final evidence manifest is checked by CI | VERIFIED IN CONFIGURATION | `.github/workflows/ci.yml`; current connector did not return a separate workflow-run record for the publication commit |
| Release exists, title is correct, not draft/prerelease, seven assets complete | OWNER-REPORTED; PENDING INDEPENDENT API VERIFICATION | Release API details were not readable through the current connector |
| Frozen evidence modified by this dissemination work | NO | This work is limited to metadata, manuscript, replication onboarding, outreach drafts, and impact governance |

## Exact owner verification: tag and release

Run in a clean clone:

```bash
git fetch --tags origin
test "$(git rev-parse research-closeout-issue-121^{})" = \
  "4dfb0b961470974f9dc80a936db86450303d007a"
test "$(git cat-file -t research-closeout-issue-121)" = "tag"
```

The second command must print `tag`; `commit` would indicate a lightweight tag.

Verify the published release with the GitHub CLI:

```bash
gh api \
  repos/kodlbegiko/research-readme-smoketest/releases/tags/research-closeout-issue-121 \
  --jq '{name,tag_name,draft,prerelease,html_url,assets:[.assets[].name]}'
```

Required values:

```text
name: Issue 121 External Validation — Negative Research Closeout
tag_name: research-closeout-issue-121
draft: false
prerelease: false
```

Required seven attached artifacts:

1. `dynamic-validation-results.json`
2. `dynamic-validation-results.csv`
3. `intervention-log.json`
4. `intervention-log.csv`
5. `DYNAMIC-FINAL-SHA256SUMS`
6. `research-manifest-issue-121.yml`
7. `EXTERNAL-VALIDATION.md`

Also verify the tagged source state:

```bash
git checkout --detach research-closeout-issue-121
sha256sum -c results/issue-121/DYNAMIC-FINAL-SHA256SUMS
```

If any tag, release, asset, or checksum differs, stop and record a discrepancy. Do not overwrite frozen evidence or silently replace release assets.

## CITATION.cff status

The file declares Citation File Format 1.2.0 and includes title, author, repository URL, license, abstract, and keywords. This dissemination change adds the publication commit, research tag version, and release date but does not invent a DOI or SWHID.

Automated validation command:

```bash
cffconvert --validate
```

CI installs the pinned publication-validation dependencies and runs this command.

## Zenodo status

```text
Status: PENDING OWNER ACTION
Verified concept DOI: NOT AVAILABLE
Verified version DOI: NOT AVAILABLE
```

Zenodo's GitHub integration requires an owner-connected GitHub account. The owner must:

1. sign in to Zenodo and connect the correct GitHub account;
2. open the GitHub integration page;
3. select **Sync now**;
4. find `kodlbegiko/research-readme-smoketest` and enable it;
5. confirm that the formal GitHub Release is ingested;
6. inspect title, author, abstract, license, keywords, related identifiers, tag, and files;
7. ensure the description explicitly says negative external-validation result, not a product, and no GitHub Action v0.2;
8. publish the record;
9. record the actual concept DOI and version DOI; and
10. open a metadata-only pull request adding those verified values to `CITATION.cff`, the research manifest, README, and this status file.

Do not enter a reserved, guessed, or draft DOI as if it were published.

## Software Heritage status

```text
Status: PENDING OWNER ACTION
Save Code Now request ID: NOT RECORDED
Snapshot SWHID: NOT RECORDED
```

Submit the public origin through Software Heritage Save Code Now. A command-line route is:

```bash
curl -X POST \
  'https://archive.softwareheritage.org/api/1/origin/save/git/url/https://github.com/kodlbegiko/research-readme-smoketest/'
```

Preserve the response containing the origin URL, request date, request status, task status, request URL or request ID, and eventual snapshot SWHID. Poll the returned request URL or query the request ID until the task is `succeeded`. Then verify that the archived snapshot contains the formal tag and publication commit.

Only after a real `swh:1:snp:...` or other applicable SWHID is returned may the identifier be added to repository metadata. A pending or accepted request is not a completed archive.

## Dissemination window

The bounded dissemination window begins on **2026-07-26**.

- Earliest decision point, 90 days: **2026-10-24**
- Default decision point, 105 days: **2026-11-08**
- Absolute end, 120 days: **2026-11-23**

The default decision memo should be prepared on 2026-11-08 unless a material independent result justifies waiting until the absolute end. This is a dissemination window, not authorization for indefinite outreach.

## Permitted activities during the window

- publish up to three reviewed public community posts;
- send up to eight individually approved invitations;
- answer protocol questions;
- receive issues and pull requests;
- validate independent submissions;
- record verified citations, reproductions, annotations, protocol adoption, decision changes, corrections, or user outcomes;
- correct metadata or protocol ambiguity without altering frozen results.

## Prohibited activities during the window

- detector rule tuning on issue-121 evidence;
- a v0.2 detector or GitHub Action;
- mass maintainer defect reports;
- repeated unsolicited follow-up;
- treating stars, views, downloads, or impressions as impact;
- treating AI review as independent human evidence;
- hiding contradictory or blocked replications.

## Decision rule at window close

If verified independent evidence exists, summarize its method, deviations, results, conflicts, and effect on the original conclusion. Change a conclusion only when the new evidence supports the change.

If no verified independent evidence exists, record:

```text
DISSEMINATION COMPLETED
NO INDEPENDENT EXTERNAL EVIDENCE RECEIVED
RESEARCH REMAINS PRESERVED
NO DETECTOR DEVELOPMENT AUTHORIZED
```

Then stop active outreach while leaving issues and pull requests open for future submissions.
