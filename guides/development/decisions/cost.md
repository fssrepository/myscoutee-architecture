# Cost and efficiency decisions

**Status:** analytical framework; no current cloud bill, infrastructure price or savings claim is established here. Prices and provider terms change, so any concrete comparison needs dated quotes and measured workloads.

For the concrete provider comparison, see [why Netcup was simpler first](netcup-cloudflare-cloud.md) and the [AWS, Azure, Google Cloud and OCI billing matrix](cloud-provider-stacks-and-billing.md).

## What to count

A useful choice compares **total cost for the same service level**, not only a VM or database sticker price. Record workload volume and peaks, retention, backup/restore, egress, storage growth, operations time, security/qualification, deployment risk and migration effort. Separate one-time transition cost from recurring cost. Include developer-host and test-lab resources only when they are part of the decision. Keep the current product and experimental labs in different rows.

| Candidate | Current evidence | Cost question |
| --- | --- | --- |
| Packaged Compose on current host | Installed product runtime | What are measured host, storage, backup, support and availability costs? |
| Eight-service KVM/K3s laboratory | Separate deployment experiment | Does isolation/scaling justify more deployment and monitoring work at the same workload? |
| Big Data/Elastic labs | Synthetic or local experiments | Which real product question warrants additional data copies and retention? |
| Managed cloud or alternate graph store | Historical trial to locate; see [technology trials](technology-trials.md) | What measured capability, migration and operations benefit exceeds total cost? |

## Comparison protocol

1. Define the same workload, data size, concurrency, latency target, recovery target and privacy constraints for each candidate.
2. Measure the present baseline before proposing replacement. Use actual bills or dated provider quotes for external prices.
3. Model compute, storage, network egress, backups, licenses, support, human operations, migration and exit cost separately.
4. Test a bounded pilot with rollback and representative data; compare p50/p95 latency, throughput, failure recovery and total spend.
5. Record uncertainty, sensitivity to growth and the point at which the decision changes.

A cost reduction is supported only when the same functional, security and recovery requirements remain satisfied. A smaller monthly line item can be more expensive after migration and operational labor. This chapter authorizes no infrastructure change or purchasing decision.
