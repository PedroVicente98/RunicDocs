---
title: "_std — Go SDK (PSDK-2, PSDK-3)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › _std — Go SDK (PSDK-2, PSDK-3)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · every service schema · Built on decisions.* Four tables the Platform Go SDK creates in every service schema: idempotency, transactional outbox and inbox for NATS, and the audit log for privileged calls.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| idempotency\_keys | op\_id uuid PK; request\_hash bytea; response bytea; created\_at timestamptz; expires\_at timestamptz | A retried operation commits once ([[PSDK-2\|PSDK-2]]). Rows expire after the retry window. — op\_id: stable operation ID from the caller; request\_hash: same ID with a different body is rejected; response: stored answer returned on retry |
| outbox | seq bigint PK; subject text; payload bytea; created\_at timestamptz; published\_at timestamptz null | Facts written in the same transaction as the change; a relay publishes them to NATS after commit. — seq: identity; subject: NATS subject, e.g. character.checkpointed; payload: Protobuf message (Contracts) |
| inbox | message\_id uuid PK; subject text; received\_at timestamptz | NATS messages already consumed, so a redelivered message changes nothing. |
| audit\_log | audit\_id bigint PK; actor text; action text; target text; payload jsonb null; at timestamptz | Privileged calls and operator actions (Security appendix, [[PSDK-1\|PSDK-1]]). Never deleted. Partitioned monthly. — actor: service, GM or operator identity |

---

↑ [[Schemas|Schemas]] · ← [[content Deploy pipeline read-only for services|content — Deploy pipeline (read-only for services)]]  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › _std — Go SDK (PSDK-2, PSDK-3) · exported 2026-11-03
