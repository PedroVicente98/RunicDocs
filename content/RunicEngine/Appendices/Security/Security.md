---
title: "RunicEngine — Appendix: Security"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
created: "2026-10-22"
modified: "2026-10-22"
---

Design appendix from the conversation of 22 October 2026, to be merged later into the technical architecture and [[Vision|the game vision]]. It covers how the game can be attacked (the client, the protocol, bots, the economy, accounts, services, [[DDoS|DDoS]] and the [[Supply chain and releases|supply chain]]) and the defenses adopted for each, with the owning repository. Items are labeled Decision, Proposal or Open. Numbers are examples for tuning. The GitHub issues already carry these requirements under the security label; the section Changes to the GitHub issues lists them.

## Contents

- [[Decisions|Decisions]]
  - [[Decisions#Who attacks and why|Who attacks and why]]
- [[The client|The client]]
- [[The protocol|The protocol]]
  - [[The protocol#The ping helpers as an attack surface|The ping helpers as an attack surface]]
- [[Bots and scripts|Bots and scripts]]
- [[Economy exploits|Economy exploits]]
- [[Accounts|Accounts]]
- [[Services and infrastructure|Services and infrastructure]]
- [[DDoS|DDoS]]
- [[Supply chain and releases|Supply chain and releases]]
- [[Moderation|Moderation]]
- [[Ownership (Security)|Ownership]]
- [[Stage plan|Stage plan]]
- [[Changes to the GitHub issues|Changes to the GitHub issues]]
- [[Differences from the Vision and the Architecture|Differences from the Vision and the Architecture]]
- [[Open (Security)|Open]]
- [[Sources (Security)|Sources]]

---

↑ [[index|RunicDocs]]  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) · exported 2026-11-03
