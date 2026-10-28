# Why Netcup was simpler first: cloud and edge cost anatomy

**Status:** dated decision analysis, 27 October 2026. This is not a current invoice or a commitment to migrate. Product facts come from the inspected MyScoutee source; provider billing terms come from linked official pages and must be rechecked for a purchase.

## The actual starting point

MyScoutee's packaged application is a Docker Compose deployment with nginx, Java API, MongoDB, Redis, MinIO, MCP and isolated demo services on one host. Installation records confirm the product runs on Netcup. Deployment records place the authoritative A record in Netcup CCP **CloudDNS** and specify outbound DNS and HTTPS for Let's Encrypt certificate issuance. They do not establish the host's exact monthly invoice.

Netcup's current [VPS product page](https://www.netcup.com/en/server/vps) advertises a fixed plan with CPU, RAM, SSD, included traffic and DDoS protection. That made a single-host, self-managed Compose installation a simpler initial purchasing and operations model: one primary server plan and one place to size the nine-container stack. It does **not** make the host highly available, eliminate backups or qualify the same workload at larger scale. A domain and any paid backup/add-on remain separate if the actual contract charges them.

## Like-for-like comparison, before adding managed services

A Google Cloud comparison should first model **one Compute Engine VM running the same Compose stack**, not immediately assume GKE, managed databases and a global load balancer. Conversely, a single VM on Google Cloud does not gain high availability merely by changing provider. Google's [Compute Engine pricing](https://cloud.google.com/products/compute/pricing) bills machine resources, while [disk and snapshot pricing](https://cloud.google.com/compute/disks-image-pricing) and [network pricing](https://cloud.google.com/vpc/network-pricing) cover separate usage. The exact bill depends on region, machine family, provisioned storage, egress, discounts and uptime.

| Cost or capability | Netcup single VPS | Google Cloud single VM | Optional managed/edge addition |
| --- | --- | --- | --- |
| CPU and memory | Plan resources in one recurring VPS price | Compute Engine machine resource charge | Autoscaling or multiple instances add capacity and cost |
| Primary disk | Plan SSD capacity; extras may cost more | Provisioned persistent disk charged separately, including unused allocated space | Managed DB/storage charges and replication add lines |
| Backup | Design, storage and restore test still required; plan/add-on terms matter | Disk snapshots/storage and any restore traffic billed separately | Managed backup/retention may add charges |
| Internet traffic | VPS page advertises included traffic, subject to plan/usage terms | Outbound data transfer is a separate meter; inbound rules differ | CDN can reduce origin bytes but has its own price model |
| Public DNS | Existing domain record managed in Netcup CCP CloudDNS | **Cloud DNS is optional** if Netcup remains authoritative; if selected, zones and queries are billed | Cloudflare DNS is another optional authority |
| Outbound DNS for provider calls | Host and containers need working name resolution and HTTPS egress | A Compute Engine VM has a default DNS resolver; paid Cloud DNS is not required merely to resolve Firebase endpoints | Custom forwarding, private zones or managed DNS policy are separate choices |
| Ingress and DDoS | Netcup VPS advertises DDoS protection; application still owns TLS/nginx policy | VM networking alone is not the same as a managed application edge | External load balancer, Cloud Armor, Cloudflare or CDN each have distinct scope/cost |
| Operations | Team patches host, containers, databases and recovery | Same if Compose stays on one VM | Managed services shift, but do not remove, integration/incident work |

This table distinguishes **a required billable component from an optional architectural choice**. A Google Cloud VM can run nginx directly, and the domain can continue using Netcup DNS; a load balancer, Cloud DNS, Cloud Armor, GKE or Cloud SQL is not inherently required. If one of those is chosen, include its charge and the benefit it actually provides. [Cloud Load Balancing pricing](https://cloud.google.com/load-balancing/pricing), [Cloud Armor pricing](https://cloud.google.com/armor/pricing).

For equivalent single-host options on the other major clouds, see the [AWS, Azure, Google Cloud and OCI stack and billing comparison](cloud-provider-stacks-and-billing.md). Its egress example isolates one traffic meter; this Netcup analysis remains the comparison to the current host.

## DNS: two different jobs

1. **Authoritative DNS** publishes where `myscoutee.com` points. The MyScoutee deployment reference records an A record in Netcup CCP CloudDNS. Google's [Cloud DNS](https://cloud.google.com/dns/pricing) is a separately metered alternative: managed zones plus queries, with no free tier in its published price list. Cloudflare offers [authoritative DNS on its free plan](https://developers.cloudflare.com/dns/faq/) without moving hosting. None of these is a prerequisite to moving only compute.
2. **Outbound recursive resolution** lets the host resolve external names, for example certificate and provider endpoints. The requester recalls needing it on the Netcup host for **Firebase token refresh**. The inspected Netcup guide independently requires outbound DNS and HTTPS for Let's Encrypt, but does not preserve a Firebase-specific incident, the token type or the exact failing endpoint. Firebase's [FCM server guidance](https://firebase.google.com/docs/cloud-messaging/server-environment) describes rotating short-lived OAuth access tokens; that is a possible context, not proof of which refresh the recollection refers to. This DNS job is distinct from the public A record. A [Compute Engine VM has a default resolver](https://docs.cloud.google.com/vpc/docs/advanced-vpc) for internal and public names, so buying a separately billed managed Cloud DNS zone is not a prerequisite for resolving Firebase endpoints. Network egress and resolver policy must still work.

The historical Firebase point concerns the **second** job. The Netcup CCP CloudDNS A record documents the **first** job, and the two should not be combined into a single cloud DNS cost. No separate Netcup DNS fee is evidenced in the inspected deployment record; verify the actual domain contract before calling it free.

## Where Cloudflare could help image browsing

The Java media endpoint gives **public** media a one-year public cache directive and **private** media `private, no-store` after an access-policy check. nginx serves static frontend assets and proxies `/media/public` to Java. This split matters more than the fact that both responses contain an image. [Cloudflare's cache behavior](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/) respects `private`/`no-store`, and [CDN setup](https://developers.cloudflare.com/cache/get-started/) caches eligible proxied static resources. DNS-only records do not route traffic through Cloudflare cache or HTTP DDoS filtering.

| Path | Possible edge treatment | Required proof |
| --- | --- | --- |
| Hashed frontend images/fonts | Cache through a proxied Cloudflare hostname; existing immutable/static headers are a good starting point | Correct versioning, purge/rollout and cache-hit checks |
| `/api/media/public?key=...` | Candidate for an explicit cache rule because the URL lacks a normal image extension; retain key/query separation and origin policy | No private key can reach the public route; no stale or cross-key image; measured hit ratio and origin egress |
| `/api/media/private?key=...` | **Bypass shared cache and image transformation** under the current user-specific access model | No shared-cache HIT, no user-to-user disclosure, preserved auth/session and `no-store` |

Cloudflare [Images transformations](https://developers.cloudflare.com/images/optimization/transformations/overview/) can resize/compress images served from an external origin. Its [pricing](https://developers.cloudflare.com/images/pricing/) meters unique transformations; storing images in Cloudflare Images adds storage/delivery meters. The Free tier currently includes 5,000 unique transformations per month, while the Paid tier has usage charges. Those products are optional: standard proxied CDN caching and DDoS protection can be evaluated first. Cloudflare warns that resizing authenticated images into a shared cache can expose user-specific content; that is why the current private route is excluded. [Authenticated-origin guidance](https://developers.cloudflare.com/images/optimization/transformations/control-origin-access/).

Cloudflare's [standard DDoS protection](https://developers.cloudflare.com/ddos-protection/) is available on all plans, but it protects the traffic actually routed through its edge. It does not replace origin hardening, application authorization or a plan for direct-to-origin traffic. Cloudflare can sit in front of Netcup; using it does not require moving the backend to Google Cloud. Its free [authoritative DNS](https://developers.cloudflare.com/dns/faq/) is a separate decision from enabling proxied HTTP traffic.

## Decision model

For a measured month, compare:

```text
Netcup total = actual VPS + domain + backup/add-ons + team operations
Google single-VM total = compute + provisioned disks + snapshots + outbound traffic
                       + chosen DNS/LB/security/CDN + team operations + migration
Netcup + Cloudflare total = Netcup total + selected Cloudflare plan/features
                            - measured origin egress or latency benefit
```

The last subtraction is a benefit estimate, not automatically a cash saving: included Netcup traffic may make origin-byte reduction valuable for latency/capacity before it reduces the invoice. Measure public/private image request counts, bytes, cache-hit rate, p95 viewing latency, peak load, false positives, and DDoS/incident needs. Then price the **same** service and recovery level in each candidate. A pilot should leave the private media path uncached and verify public image invalidation and TLS/host routing before any DNS cutover.
