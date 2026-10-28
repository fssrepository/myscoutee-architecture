# 5. Evidence, decisions and change control

**Status:** architecture assessment as of the [source ledger](sources.md), not a roadmap commitment.

## Verified versus proposed

| Claim | Evidence level | Practical consequence |
| --- | --- | --- |
| Backend source has one product Java source owner and eight configured KVM assemblies | Configuration and shared runtime README | Inspect/build/test each runtime form independently |
| Backend source Compose defaults to single-member Mongo replica set | Packaging reference and Compose configuration | Change streams are available; database failover is not established |
| Installed Compose product has its own deployment evidence | Release and installation records | Do not apply that qualification to source stacks or the KVM lab |
| Big Data, Elastic, 2FA, security and infra labs work in isolation | Their own READMEs | No MyScoutee integration is implied |
| A RUP-to-agile path could guide future delivery | [Methods comparison](../methods/rup-to-agile.md) and external process sources | A proposal, not evidence that MyScoutee uses RUP, OpenUP or Scrum |

## Architecture decisions to record when changes are proposed

| Decision | Question to answer before implementation |
| --- | --- |
| Split-runtime promotion | Which domain/API contracts, data ownership rules, rollback and monolith/KVM checks make a release acceptable? |
| Product observability | Which events/metrics/logs, privacy controls and response ownership justify a telemetry pipeline? |
| Big Data adoption | Which product question exceeds current Mongo/Redis/statistics capability, and which source of truth feeds it? |
| 2FA integration | Which login and recovery policy owns factor enrollment and enforcement, and how is the trusted backend-to-factor API secured? |
| Registry participation | Which operator consent, host egress, key/receipt backup and independent endpoint policy apply? |
| Recovery objective | What RPO/RTO is required, and what tested restore proves it across Mongo, objects and Registry identity? |

These are **decision prompts**, not planned features. The source owners and their QA/release workflows remain authoritative. This repository should link accepted decisions and update its diagrams only after implementation or an explicitly adopted target architecture.

## Update rule

For each material change: (1) identify the canonical owner and revision; (2) update the relevant source ledger row and status; (3) adjust diagrams, data paths and trust boundaries; (4) distinguish configuration, runtime verification and published-release evidence; (5) regenerate and visually check the PDF. Do not copy private credentials, scanner reports or live user data into this repository.
