# v0.1.0 release owner action

The connected GitHub tool can create branches, files, issues, and pull requests but does not expose tag or Release creation. Do not treat this document as evidence that a tag or Release exists.

After external-validation work is reviewed, the repository owner should:

1. Open the repository Releases page.
2. Create tag `v0.1.0` targeting baseline commit `2caeecc8678a4614f6fe6771df0ace6827a5f434`.
3. Set release title to `v0.1.0 — JOSS issue 122 reproducible pilot`.
4. Use the `CHANGELOG.md` v0.1.0 section as the release notes.
5. State prominently that issue 122 is a development-sample pilot and that issue 121 external validation is separate.
6. Do not move the tag to a later external-validation commit.
7. Verify that GitHub's generated source archive contains the baseline commit above.

Suggested repository description:

> Reproducible pilot and external validation of conservative root-README install-to-first-use checks for research software.

Suggested topics: `research-software`, `reproducibility`, `readme`, `documentation`, `joss`, `python`, `benchmark`.