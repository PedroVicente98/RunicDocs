---
title: "Physical layout (Proposal)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Physical layout (Proposal)"
created: "2026-10-26"
modified: "2026-10-30"
---

| Part | What it is |
| :---- | :---- |
| Global cluster | One PostgreSQL cluster for the account, ticket and directory schemas. Read by login and server select only; the simulations never touch it, and they verify tickets with public keys they already hold. |
| Shard database | One database per shard (a world in the docs' sense) with every shard schema: the Platform's coordinator, instance, directive, social, ledger and wallet, and all Game schemas. Proposal: start with one PostgreSQL cluster per datacenter holding all its shard databases; a busy shard moves to its own cluster with no schema change. |
| Schema per service | Each Go service owns one or more schemas and has its own database role with rights only on them. No service reads another's tables; it asks the owner over gRPC or listens to its NATS facts. Columns marked REF are logical references across schemas, without a foreign key constraint. |
| Ledger and wallet together | The ledger and wallet schemas sit in the same database, so the Platform can move items and currency in one transaction ([[PBB-3\|PBB-3]], used by trades, auctions and mail). |
| PgBouncer | Transaction pooling in front of each cluster, so many service replicas share a small number of server connections. |
| Partitioning | Append-only history (ledger entries, wallet entries, chat log, [[Labor\|labor]] events, sales, behavior summaries, audit) is partitioned by time, so old partitions are archived to object storage or dropped by retention instead of deleted row by row. |
| Object storage | Report evidence (the last-60-second captures) and archived partitions live in S3-compatible object storage; PostgreSQL keeps only their keys. |
| Migrations | Each service owns forward-only migrations in its own folder, applied by the SDK at deploy. |

---

↑ [[Database Layout|Database Layout]] · ← [[Decisions this layout builds on|Decisions this layout builds on]] · [[Conventions Proposal|Conventions (Proposal)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Physical layout (Proposal) · exported 2026-11-03
