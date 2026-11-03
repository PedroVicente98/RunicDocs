---
title: "access — Housing service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › access — Housing service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Permissions per resource and per character. Lineage-mates and spouses get access by rule, not by rows, so permissions never chain through several marriages.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| grants | grant\_id bigint PK; resource\_kind text; resource\_id bigint; grantee\_kind text; grantee\_id bigint null; mask int; granted\_by bigint ⇢ character.characters; granted\_at timestamptz; expires\_at timestamptz null | Who may use, open, pilot, harvest or manage something. — resource\_kind: house, farm, ship, chest, vehicle, item; grantee\_kind: character, family, guild, party, public; mask: use, open, pilot, harvest, manage |

---

↑ [[Schemas|Schemas]] · ← [[family Guild service|family — Guild service]] · [[housing Housing service|housing — Housing service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › access — Housing service · exported 2026-11-03
