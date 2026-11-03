---
title: "territory — Territory service (new)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › territory — Territory service (new)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Proposal. Regions and nodes with [[Regional economy#Prosperity and node missions|prosperity]], weekly missions, owner guilds and their fixed weekly payout; weekly node wars; castles on the neutral continent.* Not yet in the Architecture's service list.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| nodes | node\_id text PK; region\_id int; parent\_node\_id text → nodes null; kind text; owner\_guild\_id bigint ⇢ guild.guilds null; prosperity smallint; full\_weeks smallint; specialty text null; war\_cost\_bp int; updated\_at timestamptz; version int | One per node; static data (borders, connections, climate) stays in content. A game region is a city node plus the child nodes whose parent it is; a guild owns up to 3 nodes or one region, never both. — node\_id: ContentId; parent\_node\_id: the region's city node, null for the city itself and for transitional nodes; kind: city, capital, village, mine, forest, farm, port, island, transitional; prosperity: 1 to 5, unused for transitional nodes; full\_weeks: 100% weeks toward the next level, not necessarily consecutive, reset when the level changes; war\_cost\_bp: automatic cost while at war |
| node\_missions | node\_id text PK → nodes; week\_start date PK; mission\_kind text PK; template\_id text null; quota int; delivered int; fixed\_price bigint null | This week's missions for the node, about three rotating kinds per [[Nodes#What a node is\|node]] type, not all deliveries. PK (node\_id, week\_start, mission\_kind). — fixed\_price: set when posted, above the market, fixed for the week |
| node\_contributions | contribution\_id bigint PK; node\_id text → nodes; week\_start date; character\_id bigint ⇢ character.characters; template\_id text; quantity int; at timestamptz | Deliveries by anyone, PvE players included. Partitioned monthly. |
| node\_week\_results | node\_id text PK → nodes; week\_start date PK; completion\_pct smallint; level\_before smallint; level\_after smallint | 60% keeps the level, two 100% weeks raise it, level 5 needs 100%; 150% and 200% give a temporary buff, never a level. PK (node\_id, week\_start). |
| node\_ownership | node\_id text PK → nodes; since timestamptz PK; guild\_id bigint ⇢ guild.guilds; until timestamptz null; via\_war\_id bigint → node\_wars null | History of owners. PK (node\_id, since). |
| node\_wars | war\_id bigint PK; node\_id text → nodes; attacker\_guild\_id bigint ⇢ guild.guilds; defender\_guild\_id bigint ⇢ guild.guilds null; week\_start date; scheduled\_at timestamptz; state text; winner\_guild\_id bigint null | One challenge per guild per week: UNIQUE (attacker\_guild\_id, week\_start). — state: scheduled, running, resolved, cancelled |
| guild\_payouts | node\_id text PK → nodes; period\_start date PK; guild\_id bigint ⇢ guild.guilds; amount bigint | Fixed weekly payout to the ruling guild by tier and prosperity, with mission and project bonuses inside the cap. PK (node\_id, period\_start). |
| resource\_richness | node\_id text PK → nodes; resource\_kind text PK; richness smallint; rotates\_at timestamptz | Rotating richness per resource kind. PK (node\_id, resource\_kind). |
| castles | castle\_id bigint PK; region\_id int UQ; zone\_id text; guild\_id bigint ⇢ guild.guilds; state text; hp int; built\_at timestamptz | Neutral continent only: one castle per region, in one of its designated zones; fixed once placed. On the faction continents the ruling guild uses the city and an exclusive guild building. — state: building, standing, damaged |
| castle\_structures | structure\_id bigint PK; castle\_id bigint → castles; kind text; hp int; state text | Walls, gates and buildings with their own HP. |

---

↑ [[Schemas|Schemas]] · ← [[jobs Economy service|jobs — Economy service]] · [[mail Mail service|mail — Mail service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › territory — Territory service (new) · exported 2026-11-03
