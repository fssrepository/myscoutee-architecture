# Source ledger and evidence rules

**Inspection date:** 27 October 2026. Revisions below are local checkout HEADs unless marked as a recorded submodule. They are a documentation baseline, not a claim that every deployed host runs those commits. Follow the owner repository for later changes.

| Owner | Revision inspected | Principal evidence |
| --- | --- | --- |
| [`myscoutee-backend`](https://github.com/fssrepository/myscoutee-backend/tree/62d7f776) | `62d7f776` | Product code, packaging and QA |
| [`myscoutee-frontend`](https://github.com/fssrepository/myscoutee-frontend/tree/9f21466c) | `9f21466c` recorded backend submodule | Browser application and adapters |
| [`myscoutee-base`](https://github.com/fssrepository/myscoutee-base/tree/f56a9a4) | `f56a9a4` | Shared Java libraries |
| [`myscoutee-microservices`](https://github.com/fssrepository/myscoutee-microservices/tree/09ad976) | `09ad976` | KVM/K3s build and deployment runtime |
| [`myscoutee-registry`](https://github.com/fssrepository/myscoutee-registry/tree/d0ca986) | `d0ca986` | Independent Registry protocol and server |
| [`myscoutee-template`](https://github.com/fssrepository/myscoutee-template/tree/f829ec1) | `f829ec1` | Separate product using shared dependencies |
| [`myscoutee-bigdata`](https://github.com/fssrepository/myscoutee-bigdata/tree/fc5e9bf) | `fc5e9bf` | Synthetic data-processing lab |
| [`myscoutee-elastic`](https://github.com/fssrepository/myscoutee-elastic/tree/8b36f4b) | `8b36f4b` | Source-search and Elastic lab |
| [`myscoutee-security`](https://github.com/fssrepository/myscoutee-security/tree/58bc8c0) | `58bc8c0` | Isolated security-scanning lab |
| [`myscoutee-2fa`](https://github.com/fssrepository/myscoutee-2fa/tree/3e26f9c) | `3e26f9c` | Standalone factor-service lab |
| [`myscoutee-infra`](https://github.com/fssrepository/myscoutee-infra/tree/9a6812b) | `9a6812b` | Disposable provisioning lab |
| [`myscoutee-roadmap`](https://github.com/fssrepository/myscoutee-roadmap/tree/439577a) | `439577a` | Retrospective work and release history |

Other owners named in the context map are linked by repository rather than pinned here; no implementation-level claim in this guide depends on their exact uninspected revision.

## Evidence hierarchy

1. **Current implementation and configuration** define what the inspected source can build or run.
2. **Versioned runtime/QA evidence** establishes which paths were actually exercised. It does not automatically qualify another environment.
3. **Released artifact and installation evidence** establishes a specific release and host, not a newer checkout.
4. **Lab README or roadmap** establishes a lab or proposal only. No integration is inferred from a neighboring checkout.
5. **Owner recollection** records a lead about historical events. Keep it explicitly attributed until an incident log, support case, invoice or other contemporaneous artifact confirms the details.

When revising this repository, update the ledger and the relevant claim together. No credentials, private host paths, tokens, live user data or unreviewed scanner reports belong here.
