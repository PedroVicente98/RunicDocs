---
title: "account — Accounts service (PCS-1)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › account — Accounts service (PCS-1)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · global cluster · Built on decisions.* Accounts, credentials, devices, sessions and entitlements. Accounts are global; everything game-side lives in the shard databases.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| accounts | account\_id bigint PK; global\_player\_id bigint UQ; email citext UQ; email\_verified\_at timestamptz null; status text; home\_datacenter text; locale text; created\_at timestamptz; last\_login\_at timestamptz null; version int | One per person. GlobalPlayerId is issued here. — global\_player\_id: GlobalPlayerId ([[CORE-1\|CORE-1]]); status: active, suspended, banned, closed; home\_datacenter: sa, na, eu; version: optimistic concurrency |
| credentials | account\_id bigint PK → accounts; password\_hash text; password\_changed\_at timestamptz; breach\_checked\_at timestamptz null | Password data kept apart from the profile. — password\_hash: Argon2id; breach\_checked\_at: known-breach check on new passwords |
| mfa\_factors | factor\_id bigint PK; account\_id bigint → accounts; kind text; secret\_ref text; label text null; created\_at timestamptz; last\_used\_at timestamptz null | 2FA with authenticator apps and passkeys. — kind: totp, passkey; secret\_ref: encrypted secret or passkey public key |
| devices | device\_id bigint PK; account\_id bigint → accounts; fingerprint\_hash bytea; first\_seen\_at timestamptz; last\_seen\_at timestamptz; trusted\_at timestamptz null | New-device detection; unique per (account\_id, fingerprint\_hash). — first\_seen\_at: the Trade service reads it for new-device holds |
| sessions | session\_id uuid PK; account\_id bigint → accounts; device\_id bigint → devices; ip\_hash bytea; created\_at timestamptz; expires\_at timestamptz; revoked\_at timestamptz null | Login sessions; sign-out everywhere revokes all. |
| login\_attempts | attempt\_id bigint PK; account\_id bigint → accounts null; ip\_hash bytea; success bool; at timestamptz | Rate limits per address and per account. 30-day retention. Partitioned daily. |
| email\_tokens | token\_hash bytea PK; account\_id bigint → accounts; purpose text; expires\_at timestamptz; used\_at timestamptz null | Verification, password reset and new-device emails. — purpose: verify, reset, new\_device |
| entitlements | entitlement\_id bigint PK; account\_id bigint → accounts; kind text; starts\_at timestamptz; ends\_at timestamptz null; source\_ref text; created\_at timestamptz | Early access, [[Business model launch visuals and audio#Subscription\|subscription]], free tier, purchases (launch phases). — kind: subscription, early\_access, free\_tier, purchase; source\_ref: payment provider reference |
| entitlement\_events | event\_id bigint PK; entitlement\_id bigint → entitlements; kind text; payload jsonb null; at timestamptz | History of every entitlement change. — kind: granted, renewed, expired, refunded |

---

↑ [[Schemas|Schemas]] · [[ticket Accounts service PCS-1|ticket — Accounts service (PCS-1)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › account — Accounts service (PCS-1) · exported 2026-11-03
