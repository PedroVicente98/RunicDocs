---
title: "Stage plan"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "Stage plan"
created: "2026-10-22"
modified: "2026-10-22"
---

| Stage | Slices | Measures |
| :---- | :---- | :---- |
| Now | [[Slice 00 Build skeleton\|0]], [[Slice 05 Moving entities\|5]], [[Slice 12 Transport\|12]] to [[Slice 14 Prediction\|14]], [[Slice 21 World partitions\|21]], [[Slice 22 World rendering\|22]], [[Slice 25 Interest\|25]] | CI hardening; bounded decoding, fuzzing and budgets; ticket rules and server identity; field audiences; send ranges; signed manifests; release flag |
| Services and persistence | [[Slice 26 Service foundation\|26]] to [[Slice 28 Persistence\|28]], [[Slice 33a Exploration prototype\|33a]] | mTLS, limits and audit; login security; ledger and wallet supply counts and compensation; supply alerts |
| Scale and operations | [[Slice 36 Multiple simulations\|36]], [[Slice 38 Battle scale\|38]], [[Slice 39 Operations\|39]] | Adversarial handoff tests; authenticated simulation links; development tickets for [[Tools#Testing at scale\|RunicBot]]; the behavior pipeline; development-only attach; private services |
| Launch | [[Slice 44 Expansion\|44+]] | Edge and DDoS protection with relays; [[The client\|anti-cheat]]; signed launcher; reports and moderation; new-device holds; chat limits; admission queue |
| After launch | [[Slice 44 Expansion\|44+]] | Ban waves, honeypots, machine-learning scoring, a bug bounty, and occlusion-aware interest if measurements call for it |

---

↑ [[Security|Security]] · ← [[Ownership (Security)|Ownership (Security)]] · [[Changes to the GitHub issues|Changes to the GitHub issues]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › Stage plan · exported 2026-11-03
