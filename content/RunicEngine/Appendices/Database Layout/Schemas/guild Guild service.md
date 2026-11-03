---
title: "guild — Guild service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › guild — Guild service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Guilds, ranks and permissions, members, applications, guild log, bank permissions per location, alliances.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| guilds | guild\_id bigint PK; faction\_id text; name citext UQ; tag text null; leader\_id bigint ⇢ character.characters; level smallint; xp bigint; alliance\_id bigint → alliances null; created\_at timestamptz; disbanded\_at timestamptz null; version int | One guild. |
| guild\_ranks | rank\_id bigint PK; guild\_id bigint → guilds; name text; position smallint; permissions bigint | Ranks with a permission bitmask. |
| guild\_members | character\_id bigint PK ⇢ character.characters; guild\_id bigint → guilds; rank\_id bigint → guild\_ranks; contribution bigint; joined\_at timestamptz | One guild per character. |
| guild\_applications | application\_id bigint PK; guild\_id bigint → guilds; character\_id bigint ⇢ character.characters; kind text; message text null; state text; created\_at timestamptz | Applications and invites. — kind: application, invite |
| guild\_log | entry\_id bigint PK; guild\_id bigint → guilds; actor\_id bigint; kind text; payload jsonb null; at timestamptz | Joins, kicks, bank moves, wars. Partitioned monthly. |
| bank\_permissions | guild\_id bigint PK → guilds; scope text PK; rank\_id bigint PK → guild\_ranks; tab smallint PK; can\_deposit bool; withdraw\_per\_day int | Guild banks are local; permissions per bank location, rank and tab. — scope: bank location |
| alliances | alliance\_id bigint PK; name citext UQ; created\_at timestamptz; dissolved\_at timestamptz null | Alliances are a system; admins regulate informal ones. |
| alliance\_members | alliance\_id bigint PK → alliances; guild\_id bigint PK → guilds; joined\_at timestamptz | PK (alliance\_id, guild\_id). |

---

↑ [[Schemas|Schemas]] · ← [[mail Mail service|mail — Mail service]] · [[family Guild service|family — Guild service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › guild — Guild service · exported 2026-11-03
