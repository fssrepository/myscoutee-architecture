# Technology trials and integration status

**Status:** evidence inventory and decision prompts. A nearby repository or prior experiment does not establish an application integration.

| Technology | Current scope | Current interpretation |
| --- | --- | --- |
| Kafka, ClickHouse, Spark, Flink and S3-compatible lake | Big Data lab | Runnable synthetic lab; not connected to product data |
| Elasticsearch, Kibana, Logstash, Beats and Fleet | Elastic lab | Runnable local CodeForge/telemetry lab; not a product SIEM/search deployment |
| TOTP/HOTP/WebAuthn factor service | 2FA lab | Standalone service; MyScoutee login integration not present |
| Ansible and Puppet | Infrastructure lab | Synthetic nginx provisioning comparison; no backend provisioning |
| Google Cloud trial | Mentioned as historical context by the requester; no versioned trial report found in the inspected repository READMEs/guides | **Evidence to recover** before describing workload, result or spend |
| Neo4j trial | Mentioned as historical context by the requester; no versioned trial report found in the inspected repository READMEs/guides | **Evidence to recover** before claiming graph-model fit or replacement value |

The requester also recalls contacting **Google Support** during an earlier Google-related effort; the support representative responded from the Philippines. No case record, date, diagnosis, recommendation or outcome was found in the inspected versioned guides. This is a historical recollection, not evidence of a Google Cloud product defect or a paid support contract.

For Google Cloud, recover the exact service (for example a VM, managed database or serverless product), date, region, workload, configuration, bill/quote, outcome and reason to continue or stop. For Neo4j, recover the graph model, dataset size, query patterns, measured comparison to the current Mongo/affinity path, licensing/deployment assumptions and data-sync implications. These are information needs, not assertions about what was previously tested.

## Before promoting a trial

A decision record should name the product problem, current owner and baseline, representative workload, data classification, integration contract, cost model, security/operations owner, rollback, measured result and status (`idea`, `lab`, `pilot`, `adopted`, `rejected`). Link immutable source evidence. The current architecture remains the product baseline until an owner implements and qualifies a change.
