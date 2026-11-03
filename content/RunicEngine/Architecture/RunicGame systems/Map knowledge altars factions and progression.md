---
title: "Map knowledge, altars, factions and progression"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "RunicGame systems (Game) › Map knowledge, altars, factions and progression"
created: "2026-10-14"
modified: "2026-10-30"
---

* **Map knowledge:** one bit per explored cell per Lineage, shared by its characters — about 150,000 surface cells (≈ 18 KB before compression) per 600 km² map at 64 m cells; underground and floating-island cells add their own bits, so the map can show them separately. The simulation marks cells on the cell changes it already detects and sends batched updates to the character service; reading a chart unlocks its node layer for the Lineage and consumes it ([[Nodes Economy and Exploration|RunicGame — Appendix: Nodes, Economy and Exploration]]).

* **Altars:** world entities in the spatial index; the Altars a character has discovered are durable character state. Death respawns the character at the nearest Altar that character has discovered, in the world where it died, and choosing or resetting the loadout and the [[Weapon Class System#Disciplines|Discipline]], which redistributes the skill points, is an altar interaction that rebuilds the resolved [[Weapon Class System#Loadouts|loadout]]. The Lineage sees on the map every [[Real exploration#Altars, death, respawn and teleports|Altar]] its characters found, but respawn and teleports use only the character's own discovered Altars, so each character rediscovers them. Settlement Altars are teleport destinations once the character has visited them, for a fixed fee plus distance, much more between continents, and no cargo fee; from the field a teleport also uses a consumable and has a long cooldown, and from one Altar to another it costs only the fee (RunicGame — Appendix: Nodes, Economy and Exploration).

* **Factions:** faction, crime and pirate status are durable state mirrored in the simulation; PvP eligibility and group rules (pirates may group with both factions) are game data.

* **Named classes:** one of ten fixed loadouts plus one of five Disciplines is a [[Weapon Class System#Named classes|named class]] with exactly one role (Damage, Tank or Support); class and role are derived, never chosen. Weapon skills are the basic kit, unlocked by level with no point cost, with some level choices; skill points go only into the Discipline skills, in one merged tree per class. Combat skill points come only from levels, every max-level character has the same total, and there is no limit on active skills. There are no versatile weapons and no weapon-type swap: changing the loadout or the Discipline is an Altar reset that redistributes the points and the level choices.

* **Context kits:** mounted, gliding or winged characters use only their [[Weapon Class System#Context kit mount, glider and wing|context kit]], from per-class mount and aerial trees with their own points (in definition). The mount, glider or wing can modify the kit, and a mount’s kit is the same on the ground and in the air.

* **Mounts, gliders and wings:** the glider only glides; the wing is equipment that glides and flies in flight zones; mounts carry glide and flight as separate capabilities; other vehicles are summoned by scroll.

* **[[Real exploration#Exploration XP|Exploration XP]]:** a separate durable counter in the Character service, earned from discoveries the simulation reports and spent in an exploration shop on adventurer abilities (for example moving objects, traversal) or resources, never on combat skills or cosmetics.

* **Professions:** 23 professions based on ArcheAge's list level with practice; Cartography includes nautical charts and exploration, and Larceny includes opening coin purses (RunicGame — Appendix: Nodes, Economy and Exploration). Language proficiency gates communication with the other faction; Proposal: it is required to change faction.

* **Castles:** only on the neutral continent, one per region, built by the ruling guild in one of the region’s designated zones (authored volumes), fixed once placed; a castle is an indivisible volume. On the faction continents the ruling guild uses the city and an exclusive guild building (RunicGame — Appendix: Nodes, Economy and Exploration).

---

↑ [[RunicGame systems|RunicGame systems (Game)]] · ← [[Quests dialogue and world interactions|Quests, dialogue and world interactions]] · [[Land hazards|Land hazards]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › RunicGame systems (Game) › Map knowledge, altars, factions and progression · exported 2026-11-03
