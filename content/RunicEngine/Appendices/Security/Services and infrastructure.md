---
title: "Services and infrastructure"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "Services and infrastructure"
created: "2026-10-22"
modified: "2026-10-22"
---

* **Two public doors only:** the login and API gateway, and the simulations ([[PINF-2|PINF-2]]). Services, databases, NATS, Prometheus ([[PBND-3|PBND-3]]), Grafana and [[Platform and operations#Simulation placement|Agones]] SDK ports stay private.
* **Between services:** mTLS, request limits, an audit log for privileged calls and secrets from a store ([[PSDK-1|PSDK-1]]); parameterized queries and per-service database users ([[PSDK-2|PSDK-2]]); network policies that deny by default ([[PINF-2|PINF-2]]).
* **Ticket signing keys** in a secret store and rotated ([[PCS-1|PCS-1]]).
* **Editor attach** is development-only and authenticated to staging, never on production ([[NET-7|NET-7]], [[GDT-13|GDT-13]]).
* **Simulation links** are authenticated by the Platform, and a client can never open one ([[PTR-3|PTR-3]]).

---

↑ [[Security|Security]] · ← [[Accounts|Accounts]] · [[DDoS|DDoS]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › Services and infrastructure · exported 2026-11-03
