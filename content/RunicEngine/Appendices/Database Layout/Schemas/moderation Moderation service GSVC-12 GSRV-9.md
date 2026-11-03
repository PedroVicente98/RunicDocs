---
title: "moderation — Moderation service (GSVC-12, GSRV-9)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › moderation — Moderation service (GSVC-12, GSRV-9)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Reports with evidence, sanctions, appeals and every GM action. Evidence captures live in object storage, not in [[Physical layout Proposal|PostgreSQL]].

| Table | Columns | Notes |
| :---- | :---- | :---- |
| reports | report\_id bigint PK; reporter\_id bigint ⇢ character.characters; reported\_id bigint ⇢ character.characters; reason text; evidence\_key text; weight real; status text; created\_at timestamptz | Weighted by the reporter's history. — evidence\_key: object-storage key of the last-60-s capture; status: open, reviewing, closed |
| sanctions | sanction\_id bigint PK; account\_id bigint ⇢ account.accounts; character\_id bigint ⇢ character.characters null; kind text; reason text; report\_id bigint → reports null; issued\_by bigint; starts\_at timestamptz; ends\_at timestamptz null; revoked\_at timestamptz null | Warning, mute, trade lock, temporary ban, permanent ban. |
| appeals | appeal\_id bigint PK; sanction\_id bigint UQ → sanctions; body text; state text; decided\_by bigint null; decided\_at timestamptz null | One appeal per sanction. |
| reporter\_weights | account\_id bigint PK ⇢ account.accounts; weight real; updated\_at timestamptz | Mass false reports do nothing. |
| gm\_actions | action\_id bigint PK; gm\_id bigint; kind text; target jsonb; reason text; at timestamptz | Audit of every GM action. |

---

↑ [[Schemas|Schemas]] · ← [[production Character service GSRV-7 GSVC-7|production — Character service (GSRV-7, GSVC-7)]] · [[behavior Behavior scoring service GSVC-11|behavior — Behavior scoring service (GSVC-11)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › moderation — Moderation service (GSVC-12, GSRV-9) · exported 2026-11-03
