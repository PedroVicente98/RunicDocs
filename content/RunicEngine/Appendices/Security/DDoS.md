---
title: "DDoS"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "DDoS"
created: "2026-10-22"
modified: "2026-10-22"
---

| Type | How it works | Target here |
| :---- | :---- | :---- |
| Volumetric | Fill the bandwidth, often amplified: DNS or CLDAP servers turn a small spoofed request into a large reply aimed at the victim | Simulation addresses |
| Protocol | Use up connection state with fake handshakes | Login, simulations |
| Application | Valid-looking but expensive requests | Login, APIs, ticks |

**Scale.** Cloudflare counted 23.2 million network-layer attacks in the first half of 2026. 90.6% ended in under 10 minutes and 96.6% stayed under 500 Mbps, but 935 exceeded 1 Tbps. Small, short attacks are the main risk here, because 500 Mbps already fills a typical game-server uplink.

**Biggest exposure.** Clients connect directly to simulation addresses, so whoever learns a node's address can flood it and take down every simulation on that node.

* **Upstream filtering ([[PINF-3|PINF-3]]).** Only a provider with more capacity than the attacker can absorb a volumetric flood. Options: hosts with game-tuned filtering on their game-server lines (OVHcloud is the usual example); AWS Global Accelerator, which includes Shield Standard (Shield Advanced costs US\$3,000 per month on a one-year commitment); game DDoS proxies such as Path.net or Gcore; own relays.
* **Hidden origins ([[PINF-3|PINF-3]]).** Clients reach only the edge. This is the same infrastructure as [[Part 1 Locked ping resolution#10. Relay routing|relay routing]] ([[Ping Resolution|Ping Resolution]], technique 10), so latency and DDoS protection are bought together once there is an audience. No Platform code change is needed, because identity comes from the ticket, never from the source address ([[PTR-2|PTR-2]]).
* **Cheap early drops.** The [[Networking stack sessions and responsiveness#Stack (decided)|GameNetworkingSockets]] challenge handshake means spoofed packets create no state; handshakes are limited per address ([[PTR-1|PTR-1]]); the ticket must come first, within a deadline ([[PTR-2|PTR-2]]); a kernel-level filter drops junk at scale ([[PINF-3|PINF-3]]).
* **Never amplify.** No unauthenticated reply is larger than its request ([[PTR-1|PTR-1]]).
* **HTTP behind a CDN** with rate limits ([[PINF-3|PINF-3]]); the login queue absorbs login floods ([[PCS-6|PCS-6]]).
* **No player addresses exposed.** Client and server only; voice, if ever added, goes through servers ([[PCS-5|PCS-5]]).
* **Fail small.** A flooded node is handled as a lost node, and the rest of the world keeps running ([[PINF-3|PINF-3]]).

---

↑ [[Security|Security]] · ← [[Services and infrastructure|Services and infrastructure]] · [[Supply chain and releases|Supply chain and releases]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › DDoS · exported 2026-11-03
