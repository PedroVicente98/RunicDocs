---
title: "character — Character service (GSVC-1, 5, 7, 10)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › character — Character service (GSVC-1, 5, 7, 10)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Lineage (the account inside a shard) and characters: progression, build, checkpoint, professions, exploration, faction and crime, map knowledge, [[Real exploration#Altars, death, respawn and teleports|Altars]], collections, [[Labor|labor]].

| Table | Columns | Notes |
| :---- | :---- | :---- |
| lineages | lineage\_id bigint PK; account\_id bigint UQ ⇢ account.accounts; labor int; labor\_reserve int; labor\_updated\_at timestamptz; online\_character\_id bigint → characters null; created\_at timestamptz; version int | The account inside this shard. Labor, map knowledge, the Altars shown on the map and collections are account-wide, so they hang here; respawn and teleports use each character's own discovered Altars. — labor: current labor; labor\_reserve: return bonus, up to twice the bar, never expires; labor\_updated\_at: regeneration is computed from this, never ticked; online\_character\_id: one character online per account |
| characters | character\_id bigint PK; lineage\_id bigint → lineages; name citext UQ; race\_id text; faction\_id text; level smallint; xp bigint; title\_id text null; state text; played\_seconds bigint; created\_at timestamptz; last\_login\_at timestamptz null; last\_logout\_at timestamptz null; deleted\_at timestamptz null; version int | One playable character. — character\_id: also its GlobalEntityId (proposal); race\_id: ContentId; faction\_id: ContentId; state: active, locked, deleted; deleted\_at: restore window |
| character\_appearance | character\_id bigint PK → characters; body jsonb; voice\_id text null; updated\_at timestamptz | Character creation data (BDO-style sliders). |
| character\_checkpoint | character\_id bigint PK → characters; map\_id int; instance\_id bigint; region\_id int; pos\_x double; pos\_y double; pos\_z double; yaw real; health int; resources jsonb; saved\_at timestamptz; source\_op uuid | Where and how the character was at the last checkpoint. Written only by the simulation, through the bridge. — map\_id: WorldId; instance\_id: 0 \= the open world; pos\_x: WorldPosition, 64-bit; resources: mana, [[Stamina and climbing#Stamina\|stamina]] and other resources; source\_op: the checkpoint operation |
| character\_effects | character\_id bigint PK → characters; effect\_id text PK; source\_ref text; stacks smallint; expires\_at timestamptz null; remaining\_ms int null; payload jsonb null | Effects that outlive a session (food, wedding guest buff). Combat statuses never come here. PK (character\_id, effect\_id). — effect\_id: ContentId; expires\_at: real-time effects; remaining\_ms: effects that pause while offline |
| durable\_cooldowns | character\_id bigint PK → characters; cooldown\_key text PK; ready\_at timestamptz | Long cooldowns that must survive logout: teleport, [[Factions PvP and crime#Outlaw and Infamy\|Outlaw]] toggle, Altar reset, divorce lock. PK (character\_id, cooldown\_key). |
| character\_build | character\_id bigint PK → characters; weapon\_set\_id text; discipline\_id text; altar\_locked\_at timestamptz; reset\_count int; version int | The named class: fixed weapon set plus [[Weapon Class System#Disciplines\|Discipline]], chosen and locked at the Altar. — weapon\_set\_id: ContentId of the class's weapon set; discipline\_id: ContentId |
| skill\_allocations | character\_id bigint PK → characters; tree\_kind text PK; skill\_id text PK; tier smallint; rank smallint | Points spent per tree; class trees are the merge of weapon and Discipline skills. PK (character\_id, tree\_kind, skill\_id). — tree\_kind: discipline, mount, aerial |
| milestone\_choices | character\_id bigint PK → characters; milestone\_level smallint PK; choice\_id text; chosen\_at timestamptz | Level milestone choices (e.g. level 35: fire, ice or lightning); changed only by an Altar reset. |
| skill\_bars | character\_id bigint PK → characters; bar\_kind text PK; slot smallint PK; skill\_id text | Bar layout per context. PK (character\_id, bar\_kind, slot). — bar\_kind: main, mount, aerial |
| ui\_layout | character\_id bigint PK → characters; layout jsonb; updated\_at timestamptz | Movable and hideable panels and keybinds, roaming between machines. |
| professions | character\_id bigint PK → characters; profession\_id text PK; proficiency bigint; mastery\_slot smallint null; mastered\_at timestamptz null | Proficiency per profession; three active masteries per character (adjustable), enforced by the service. — mastery\_slot: 1 to 3 |
| exploration | character\_id bigint PK → characters; exploration\_xp bigint; unspent bigint; updated\_at timestamptz | [[Real exploration#Exploration XP\|Exploration XP]], separate from combat progression. |
| adventurer\_unlocks | character\_id bigint PK → characters; unlock\_id text PK; rank smallint; bought\_at timestamptz | Exploration shop: flight, stamina ranks, moving objects. PK (character\_id, unlock\_id). |
| faction\_state | character\_id bigint PK → characters; participation text; outlaw bool; outlaw\_since timestamptz null; outlaw\_locked\_until timestamptz null; infamy int; pirate bool; changed\_at timestamptz | PvP or PvE mode, Outlaw and [[Factions PvP and crime#Outlaw and Infamy\|Infamy]], pirate status. Mirrored in the simulation. — participation: pvp, pve; outlaw\_locked\_until: the toggle cooldown, reset by attacks on the own faction |
| infamy\_reports | report\_id bigint PK; offender\_id bigint → characters; reporter\_id bigint → characters; victim\_id bigint null; amount int; region\_id int; at timestamptz | Reports that raised Infamy. |
| titles | character\_id bigint PK → characters; title\_id text PK; earned\_at timestamptz | Earned titles. PK (character\_id, title\_id). |
| loot\_lockouts | character\_id bigint PK → characters; lockout\_id text PK; week\_start date PK; loot\_count smallint; last\_at timestamptz | Raid loot 3 times a week, world boss once (adjustable). PK (character\_id, lockout\_id, week\_start). — lockout\_id: raid or boss ContentId |
| name\_history | character\_id bigint PK → characters; changed\_at timestamptz PK; old\_name citext | Renames, for moderation. PK (character\_id, changed\_at). |
| lineage\_altars | lineage\_id bigint PK → lineages; altar\_id text PK; discovered\_at timestamptz | Altars the Lineage has found, shown on the map only; respawn and teleports use the Altars the character itself has discovered (character\_altar\_visits, proposed). PK (lineage\_id, altar\_id). |
| map\_knowledge | lineage\_id bigint PK → lineages; map\_id int PK; layer text PK; kind text PK; bitmap bytea; version int; updated\_at timestamptz | One bit per 64 m cell, per map layer and knowledge kind. About 18 KB raw for a 600 km² surface layer, much less compressed. — layer: y band: surface, underground, sky; kind: discovered, mapped\_terrain, mobs, events, resources, currents...; bitmap: zstd-compressed bitset |
| learned\_charts | lineage\_id bigint PK → lineages; edition\_id bigint PK ⇢ cartography.chart\_editions; learned\_at timestamptz | Charts read by the Lineage. PK (lineage\_id, edition\_id). |
| collections | lineage\_id bigint PK → lineages; kind text PK; content\_id text PK; source text; unlocked\_at timestamptz | Account-wide collections: wardrobe, mounts, pets, emotes. PK (lineage\_id, kind, content\_id). |
| bestiary | lineage\_id bigint PK → lineages; creature\_id text PK; kills int; observation smallint; unlocked\_tiers int; first\_seen\_at timestamptz | Knowledge from kills and observation. PK (lineage\_id, creature\_id). — unlocked\_tiers: bitmask |
| labor\_events | event\_id bigint PK; lineage\_id bigint → lineages; delta int; reason text; profession\_id text null; op\_id uuid null; at timestamptz | Every labor gain and spend, with the profession that spent it. Partitioned monthly. |

---

↑ [[Schemas|Schemas]] · ← [[wallet Currency wallets PBB-2 PBB-3|wallet — Currency wallets (PBB-2, PBB-3)]] · [[cartography Character service|cartography — Character service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › character — Character service (GSVC-1, 5, 7, 10) · exported 2026-11-03
