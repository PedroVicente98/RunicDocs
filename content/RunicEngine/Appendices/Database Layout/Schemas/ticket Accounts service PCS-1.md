---
title: "ticket — Accounts service (PCS-1)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › ticket — Accounts service (PCS-1)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · global cluster · Built on decisions.* Signing keys for connect tickets. Tickets are short-lived and never stored; simulations verify them locally with the public halves.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| signing\_keys | key\_id text PK; purpose text; public\_key bytea; private\_key\_ref text; created\_at timestamptz; activates\_at timestamptz; retires\_at timestamptz null | Rotating keys; development keys are a separate set that never works in production. — purpose: production, development; public\_key: loaded by every simulation; private\_key\_ref: secret-store path; the key itself is never in the database |

---

↑ [[Schemas|Schemas]] · ← [[account Accounts service PCS-1|account — Accounts service (PCS-1)]] · [[directory Accounts and Admission services PCS-1 PCS-6|directory — Accounts and Admission services (PCS-1, PCS-6)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › ticket — Accounts service (PCS-1) · exported 2026-11-03
