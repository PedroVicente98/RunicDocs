---
title: "Ownership (Security)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "Ownership"
created: "2026-10-22"
modified: "2026-10-22"
---

| Measure | Engine | Platform | Game |
| :---- | :---- | :---- | :---- |
| Need-to-know | Field audiences, send ranges ([[SIM-6\|SIM-6]], [[NET-4\|NET-4]]) |  | Audience per field, rare-node ranges ([[GSH-1\|GSH-1]], [[GSRV-7\|GSRV-7]]) |
| Decoding and budgets | Bounded decoding, fuzzing, budgets ([[NET-1\|NET-1]], [[NET-3\|NET-3]], [[NET-5\|NET-5]], [[SIM-2\|SIM-2]]) |  | Budget values ([[GSH-1\|GSH-1]]) |
| Transport and tickets |  | Handshake, no amplification, ticket rules, server identity, link authentication ([[PTR-1\|PTR-1]], [[PTR-2\|PTR-2]], [[PTR-3\|PTR-3]]) |  |
| Client integrity | Signed manifests, file hashes, release flag ([[ASSET-2\|ASSET-2]], [[COOK-4\|COOK-4]]); integrity channel ([[NET-9\|NET-9]]) |  | [[The client\|Anti-cheat]], launcher, signing ([[GAME-2\|GAME-2]], [[GAME-3\|GAME-3]]) |
| Behavior detection | Counters, combat samples ([[SIM-7\|SIM-7]], [[CMB-9\|CMB-9]]) | Publishing ([[PBND-5\|PBND-5]]) | Scoring ([[GSVC-11\|GSVC-11]]) |
| Economy | Adversarial [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] tests ([[DSIM-3\|DSIM-3]]) | Supply counts, audit, compensation ([[PBB-1\|PBB-1]], [[PBB-2\|PBB-2]]) | Supply alerts, rollback, holds ([[GSVC-2\|GSVC-2]], [[GSVC-4\|GSVC-4]]) |
| Accounts |  | Login security ([[PCS-1\|PCS-1]]) | New-device holds, young-account limits ([[GSVC-4\|GSVC-4]]) |
| Services | Development-only attach ([[NET-7\|NET-7]], [[GDT-13\|GDT-13]]); development tickets for [[Tools#Testing at scale\|RunicBot]] ([[CLI-9\|CLI-9]]) | mTLS, limits, audit, private services ([[PSDK-1\|PSDK-1]], [[PSDK-2\|PSDK-2]], [[PBND-3\|PBND-3]], [[PINF-2\|PINF-2]]) |  |
| [[DDoS\|DDoS]] |  | Edge, hidden origins, filters ([[PINF-3\|PINF-3]]); admission ([[PCS-6\|PCS-6]]) |  |
| Moderation |  | Chat limits ([[PCS-5\|PCS-5]]) | Reports, sanctions, moderation ([[GSRV-9\|GSRV-9]], [[GSVC-12\|GSVC-12]]) |
| [[Supply chain and releases\|Supply chain]] | CI hardening for all three repositories ([[BUILD-1\|BUILD-1]]) |  |  |

---

↑ [[Security|Security]] · ← [[Moderation|Moderation]] · [[Stage plan|Stage plan]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › Ownership · exported 2026-11-03
