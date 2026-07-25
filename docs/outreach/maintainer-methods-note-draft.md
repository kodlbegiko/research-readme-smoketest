# Draft: maintainer methods note

## What this negative README-checker study learned about reporting documentation defects

This study tested an automated checker against research-software READMEs and decided not to productize it. The most useful maintainer-facing lesson was not a list of defects; it was a stricter standard for deciding when a report is justified.

Before contacting a maintainer, a documentation-validation workflow should distinguish:

- a direct README blocker from a dependency or compatibility failure;
- the documented core first-use path from an optional development component;
- a repository defect from a harness assertion error;
- a root README gap from an explicit delegation to official external documentation;
- a missing upstream asset from an output directory the user is expected to create.

In this study, three predicted hard findings were false positives. A simulation initially marked failed had actually completed. An editor build failure came from skipping the repository's documented generation script. A package-install failure was caused by dependency compatibility and had already been addressed on the current branch.

As a result, no maintainer issue or pull request was submitted. Zero contacts was the correct outcome because no high-confidence, non-duplicate intervention remained. Submission alone would not have counted as impact.

The released protocol preserves raw attempts, requires immutable acquisition commits, verifies prediction locks, terminates timed process groups, and keeps correction attempts separate. Maintainers are invited to correct the study's interpretation, but the detector itself is not presented as validated or recommended.
