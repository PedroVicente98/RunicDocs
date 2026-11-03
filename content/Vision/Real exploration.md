---
title: "Real exploration"
tags:
  - "vision"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-10-30"
---

Exploring is risky and knowledge is worth money: maps are merchandise, even the most basic mob needs attention, night is truly dark and death sends you to the nearest Altar.

### Maps as a resource

Map discovery is account-wide: it belongs to the Lineage and is shared by every character. The world is divided into nodes, and charts are sold per node and per layer. Details: [[RunicGame — Appendix Nodes, Economy and Exploration|RunicGame — Appendix: Nodes, Economy and Exploration]].

| Detail level | How it is reached | What the map shows |
| :---- | :---- | :---- |
| Fog | Default | Black, with no map detail |
| Discovered | Walking through the area | One static image, the same for every player, baked when the world is cooked and refreshed when the world changes in an update |
| Mapped | The node's base chart | A real-time top-down render of the terrain, with zoom and a tilt into 3D; time of day, weather and floating-island motion; never players, ships or mobs |

* **Your position:** the player always sees their exact position. Without a node's chart the map shows nothing about the node; the chart adds the node's information in a Black Desert-style layout of nodes and connections: specialty, biome, environment, prosperity, owner and region.  
* **Layers:** each chart covers one layer of one node: base (terrain, coast, paths, Altars, cave entrances), resources, fauna, events and environment (currents, depth, reefs, whirlpools, weather). No map holds everything, and a finished chart has no quality grade.  
* **Charts unlock interactions in the game:** position and route plotting, highlighted resource areas, threat, aggro radius and patrol timing, event timers and exact locations, live currents while sailing. That is why fan sites are fine: they show the information but can't give the benefit.  
* **A chart is consumed when used.** The most basic chart already shows packing benches and vendors as icons and never expires. The map has many filters, one per kind of information the player buys or maps.  
* **Events:** without a node's events chart, a player still sees that an event is happening there, but only while it runs or a few minutes before; with it, the player sees constant timers and exact locations.  
* **Surveying is a PvP activity**, with its own tools and minigame per layer (triangulation with three tools on land, a sextant and soundings at sea, drift buoys, a spyglass for fauna, samples for resources). A survey applies only to the node where it is done. Starter areas come surveyed, with charts for sale, so every player learns the mechanic. PvE players buy charts.  
* **Cartography is a profession** (with nautical charts and exploration in it): charts are player products, sold at the auction house and directly; copies cost paper, ink and labor.  
* **Current charts.** With high proficiency the cartographer syncs the chart with the current state of the currents; at max level they predict events. *Proposal: each event defines from when it can be predicted.*  
* Regions whose gimmick changes the terrain (tides, storms) can get new chart editions each season.

### Regional and hard mobs

Even the most basic mob telegraphs, blocks and positions itself; nothing dies from pressing one button. Each region has its own threats on land, in the air and in the water, tied to its gimmick.

| Medium | Example threat | What it makes harder | How to get around it |
| :---- | :---- | :---- | :---- |
| Land | Pack predators, ambushes on trails | Travel on foot and mounted, gathering | Map routes, groups, tough mounts |
| Air | Birds of prey and wyverns that knock down gliders | Gliders, wings, flight and cliff crossings | Glide low, safe hours, ranged skills |
| Water | Sharks, reef creatures, sea monsters | Swimming, diving and small boats | Bigger ships, nautical charts, lighting |

### Night and lighting

Night is truly dark: without light you can barely see the terrain and the enemies.

* **Torch:** held in a hand and lights well, so it trades a weapon for light.  
* **Lantern:** leaves the hands free, burns oil and lights less. *Proposal: an inventory item you toggle on, since there is no belt slot.*  
* **Skills with the Lighting component:** radius, duration and intensity of light, like any component. Since it is a tag, passives, item effects and interactions can read it (e.g. light-sensitive creatures back off).  
* **Light has a price:** some creatures are drawn to it, and in PvP it gives away your position.  
* The same system applies to the Underground.

### Altars, death, respawn and teleports

* **Respawn:** on death, the character respawns at the nearest Altar that this character has discovered, in the same map where they died. Only the character's own Altars count, so finding Altars is part of exploring with every character.  
* **Altars and the Lineage:** the Lineage sees on the map every Altar any of its characters has found, but respawn and teleports use only the Altars the character has visited, so each character has to rediscover them.  
* Every city has an Altar; others are scattered across the world, including islands, floating islands, the Sky Island and the Underground.  
* **At the Altar:** choosing and resetting the class (loadout and Discipline, with skill points and level choices redistributed), the respawn point and teleports. Switching between the PvE and PvP modes happens only at a faction capital's Great Altar.  
* **Teleports:** settlement Altars of the player's faction or neutral ones are destinations. A teleport only starts when the character is idle: out of combat, with no event, survey, trade pack or vehicle. The cost grows with distance, with a fixed fee and a much higher price between continents, and there is no cargo fee. From the field, a teleport also uses a consumable and has a long cooldown; from one Altar to another, only the cost.  
* **World portals:** fixed portals connect specific places (e.g. the bottom of one faction's continent to the bottom of the other's) and charge a high toll. Trade packs and mounts can't go through. The Market Isle portal is free.  
* **Unstuck** only moves the player to the nearest safe spot within about 200 m, with a cooldown. Quest and event teleports go only to fixed destinations.  
* **A light death penalty:** equipment loses durability; maps, equipment and quest items are not lost; trade packs drop on the spot and become a PvP target.

### Exploration XP

Exploring gives its own exploration XP, separate from the level. It is spent in an exploration shop on adventurer abilities (e.g. moving objects, traversal), on resources and on maximum stamina, and it never buys combat skills or cosmetics. Items found on summits are one source of the shop's currency. The advantage this gives veterans is acceptable: it grants reach, not power.

### Professions

Labor and proficiencies work almost one to one like ArcheAge's, but nobody can be the best at everything, so players need each other. Two limits do this:

* **Labor** limits how much you make. It belongs to the Lineage, so alts don't add labor. Every labor cost belongs to a profession; an action with no profession costs no labor, only its action time.  
* **Masteries** limit what you make at the top. Every profession levels freely up to a cap; past it, it needs a Mastery slot. Top recipes, the best yields, the specialty-node refining bonus and the highest quality need the mastery. Masteries are per character, 3 active at a time for now; the number is a server value tuned for balance.

**23 professions:** ArcheAge's 22 with Exploration folded into Cartography, plus Language. Names are provisional: Farming, Husbandry, Gathering, Mining, Logging, Fishing, Alchemy, Cooking, Handicrafts, Machining, Metalwork, Tailoring, Leatherwork, Weaponry, Carpentry, Masonry, Construction, Commerce, Larceny, Artistry, Printing, Cartography and Language.

* **Cartography** includes every chart, nautical charts too, and exploration: the labor spent on exploration discoveries (such as items on summits) is Cartography labor, since it is what cartography uses.  
* **Larceny** includes opening coin purses. Mobs drop coin purses in tiers (higher mobs drop higher tiers and every lower one); opening one costs labor, high-tier purses are locked and use a lockpicking minigame, and Larceny proficiency lowers the labor cost and improves the odds. Purses can yield a special resource, like ArcheAge's archeum; its name is open and is never a plain "Rune".  
* **Language** lets you talk with the other faction. *Proposal: it is a requirement to change faction.*  
* **Commerce, Printing and Artistry** are professions: Commerce owns everything about prices and trade packs, Printing makes papers and books, and Artistry is playing and composing music.  
* **Profession gear** has five generic slots (head, hands, feet, body and tool), always active, with a set bonus for a full kit and never combat stats. There is no loadout swap.  
* **Principles:** labor caps volume, and playing well raises the value of each labor point (quality, yield, material return), never the number of actions. No idle loops: every catch and craft needs a player action. Batch mode skips the minigame for a plain result. The manual-skill bonus is capped (e.g. \+20%). Each profession's gear is made by other professions.  
* **One shared crafting core:** a 10 to 30 s session with a meter and a risk-and-reward step, to which each profession adds its own twist. The server seeds each minigame and decides the outcome.  
* **Dismantling** returns part of the materials, more in a node with that profession's specialty, never more than a cap (e.g. 60% of the materials used).  
* **Recipes are unique:** there is no rule that a recipe uses the previous tier's item, although one line of equipment may. Crafted equipment carries its crafter's name.  
* **Profession quest lines** give extra profession XP, cosmetics and a profession currency, and help define the specialization; they are quest lines, never dailies.  
* Details: RunicGame — Appendix: Nodes, Economy and Exploration (Professions) and [[RunicGame — Ideias|Ideias]] ([[PROF-02 Professions and Masteries|PROF-02]]).
