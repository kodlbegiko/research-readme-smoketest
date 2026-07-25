# Individual replication invitation draft

**Subject:** Invitation to independently reproduce or challenge a negative research-software validation result

Hello [NAME OR TEAM],

I am inviting a small number of research-software and reproducibility groups to independently examine a published negative result.

Research README Smoketest v0.1.0 was a frozen static detector for root-README install-to-first-use paths. On 38 eligible GitHub repositories, it achieved precision of 1.000 but recall of approximately 0.292 and accuracy of approximately 0.553, below a preregistered 0.750 accuracy gate. Three predicted hard findings were dynamically disproved. In ten locked dynamic cases, eight of nine testable cases completed the first meaningful task and no direct README blocker was observed.

The project therefore stopped productization. It is not a recommended checker, and no GitHub Action v0.2 is planned.

Your [COMMUNITY / TEAM / METHOD] is relevant because [SPECIFIC, EVIDENCE-BASED RATIONALE]. Possible contributions include:

- computational reproduction of the preserved calculations and hashes;
- independent human re-annotation under the published eligibility rules;
- a preregistered new-data replication; or
- methodological critique of the construct, gates, or adjudication policy.

Agreement is not expected. `REPRODUCED`, `PARTIALLY_REPRODUCED`, `CONTRADICTED`, `INCONCLUSIVE`, and `BLOCKED` are all acceptable outcomes when the evidence and deviations are preserved.

Formal release: https://github.com/kodlbegiko/research-readme-smoketest/releases/tag/research-closeout-issue-121

Replication protocol: https://github.com/kodlbegiko/research-readme-smoketest/blob/main/docs/independent-replication-protocol.md

DOI: [INSERT ONLY AFTER VERIFIED ZENODO PUBLICATION; OTHERWISE STATE PENDING]

At the time of this invitation, verified external outcomes are zero: no independent reproduction, independent human re-annotation, external citation, attributable accepted correction, or measured user benefit has been recorded.

Disclosure: I developed and evaluated the original detector and own the repository. AI systems assisted with implementation, evidence organization, and drafting, but are not counted as independent annotators or replicators.

There is no obligation to respond. I will not send repeated follow-ups unless requested.

Regards,

Sean Liu  
[OWNER TO ADD VERIFIED CONTACT DETAILS]
