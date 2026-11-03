---
title: "world — World events and World routines services (GWTH-1, GSVC-9)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › world — World events and World routines services (GWTH-1, GSVC-9)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Event schedules and runs, world bosses, divine events, routine exceptions, operator events, Chaos rifts.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| event\_schedule | schedule\_id bigint PK; event\_id text; cycle\_ms bigint; jitter\_ms int; next\_at timestamptz; enabled bool | Recurring events on a cycle that does not match the clock. — event\_id: ContentId |
| event\_runs | run\_id bigint PK; event\_id text; kind text; region\_id int null; node\_id text ⇢ territory.nodes null; state text; triggered\_by bigint null; outcome jsonb null; announced\_at timestamptz null; started\_at timestamptz null; ended\_at timestamptz null | Every event that happened, including capital invasions and divine events. — kind: scheduled, dynamic, admin, divine, invasion; state: announced, running, completed, failed |
| event\_participants | run\_id bigint PK → event\_runs; character\_id bigint PK ⇢ character.characters; contribution int; reward\_op uuid null | PK (run\_id, character\_id). |
| world\_bosses | boss\_id text PK; state text; next\_spawn\_at timestamptz null; last\_killed\_at timestamptz null | Unique bosses, land and ocean. — boss\_id: ContentId; state: alive, dead, respawning |
| boss\_kills | kill\_id bigint PK; boss\_id text → world\_bosses; participant\_count int; top\_guild\_id bigint ⇢ guild.guilds null; killed\_at timestamptz | Kill history; contributions go to Rankings. |
| divine\_weights | weight\_id bigint PK; scope text; scope\_id text; multiplier real; reason text; set\_by bigint; until timestamptz | Admin mediation: raise the chance of divine events against a monopoly. — scope: region, guild |
| routine\_exceptions | exception\_id bigint PK; routine\_id text; entity\_id bigint null; kind text; offset\_ms bigint; cause\_fact uuid; created\_at timestamptz; fades\_at timestamptz | Player-caused exceptions to routines (a delayed escort, a sunk caravan) and how they fade back. — kind: delayed, sunk, destroyed, captured |
| operator\_events | operator\_event\_id bigint PK; kind text; target jsonb; payload jsonb; starts\_at timestamptz; duration\_ms bigint; directive\_id bigint ⇢ directive.directives null; created\_by bigint | Wind, current and weather events from the admin panel; delivered as Platform directives. — kind: wind, current, weather |
| rifts | rift\_id bigint PK; map\_id int; pos\_x double; pos\_y double; pos\_z double; theme\_creature text; level smallint; state text; instance\_id bigint ⇢ instance.instances null; opened\_at timestamptz; expires\_at timestamptz null | Chaos rifts: hidden dungeons anywhere, revealed up close or by deciphered scrolls. — state: hidden, revealed, entered, closed |
| rift\_reveals | rift\_id bigint PK → rifts; lineage\_id bigint PK ⇢ character.lineages; via\_item bigint null; revealed\_at timestamptz | Who revealed a rift. PK (rift\_id, lineage\_id). |

---

↑ [[Schemas|Schemas]] · ← [[housing Housing service|housing — Housing service]] · [[ranking Rankings service GSVC-8|ranking — Rankings service (GSVC-8)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › world — World events and World routines services (GWTH-1, GSVC-9) · exported 2026-11-03
