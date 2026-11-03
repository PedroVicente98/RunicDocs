---
title: "RunicGame — Appendix: Nodes, Economy and Exploration"
tags:
  - "archive"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
created: "2026-10-19"
modified: "2026-10-30"
---

Design appendix from the conversations of 13 to 19 October 2026, to be merged later into the game vision and the technical architecture. It was compared with the Drive versions of "RunicGame — Visão Completa do MMORPG" (13 Oct, including later manual edits) and "RunicEngine — Technical Architecture v4" (14 Oct). It replaces the Portuguese draft of 19 Oct.  
The first two sections list every difference from those documents. The rest describes each system in detail, and the requirements at the end are split by repository: Engine, Game and Platform. Every item is labeled Decision, Proposal, Open or Dropped. Numbers are examples for tuning. Updated on 30 October 2026 after an economy review: one global auction, regional price movement in trade-pack demand, regions made of a city node and its child nodes, fixed weekly guild income, node missions, teleports without a cargo fee and one global chest.

## Differences from the Vision

| Vision section | What the Vision said before 30 Oct | What this appendix changes |
| :---- | :---- | :---- |
| Design pillars | Seven pillars | New pillar 8, "Play without obligation": no dailies, login streaks or losses for being away; recurring content is weekly and community-driven |
| Pillar 6, Subscription, Regional economy (labor) | Same maximum labor for everyone; only subscribers regenerate offline; labor is character state | Labor is account-wide. Labor reserve: with a full bar, offline regeneration fills a reserve of up to 1× the maximum that never expires. The reserve is for subscribers only, following the existing offline rule |
| Real exploration: Maps as a resource | Three map types (city map sold by NPCs, exploration map, nautical chart) per region. Cartography records what the player travels, and a Carta is more complete and valuable the more was traveled | Three map detail levels (fog, discovered, mapped). Charts per node and per layer (base, resources, fauna, events, environment); no map holds everything. Surveying is a PvP minigame with its own tools (triangulation on land, sextant at sea). A finished chart has no grade: placement quality changes time and labor. The player always sees their exact position; a node's chart adds the node's information. Charts unlock in-game interactions. Starter areas come surveyed, with charts for sale. A chart is consumed when used |
| Real exploration: Exploration XP | Exploration shop with adventurer abilities or resources | The shop also sells stamina upgrades. Items found on summits are one source of the shop's currency. Exploration discoveries cost labor and belong to Cartography, whose labor they use |
| Real exploration: Professions | Jeweler, leather, blacksmith, fishing, farming, animal husbandry, cartography, nautical charts and language | New rule: every labor cost belongs to a profession. List: the 23 professions based on ArcheAge's (in the Vision since 30 Oct), with coin purses in Larceny and exploration in Cartography. Farming and husbandry stay professions. Profession gear in its own always-active slots; minigames with capped bonuses and a batch mode |
| Real exploration: Altars | Proposal: Altars do not teleport between each other | Changed: settlement Altars are teleport destinations (the Lineage sees them on the map, but respawn and teleports use only the Altars each character has discovered); only when idle; a fixed fee plus distance, more between continents; from the field also a consumable and a long cooldown; no cargo fee; fixed world portals with a toll |
| Factions: Participation modes | Table "Base map cartography: PvE yes"; "PvE mode makes base maps" | Surveying is PvP, so PvE mode does not create base maps: PvE players buy charts |
| Recorded decisions: Castles | One castle per region, built by the dominant guild | A region is a city node with its child nodes. A guild holds up to 3 nodes or one region, never both. Castles exist only on the neutral continent; on the faction continents the ruling guild uses the city and an exclusive guild building. Guild income is a fixed weekly payout |
| Economy, housing and land: Regional economy | Specialty per region; regional auction houses | Specialty per node and per region, with material-return bonuses; faction capitals specialize in finished products, goods and equipment; one global auction, with regional price movement in trade-pack demand; prosperity 1 to 5 through weekly node missions; one global chest; mail with postage per unit |
| Economy, housing and land: tax | "Tax" is the weekly land tax paid from the tax fund | The auction tax, paid by the seller and kept entirely by the NPC as a sink, is separate from the weekly land tax. Guilds get a fixed weekly payout instead of a tax share |
| Regional economy: trade packs | Carry a region's production to another and pay gold and special resources | Pack types copied from ArcheAge (specialty, aged, cargo, resource, military aid). Specialty payout follows the destination region's demand; resource packs build and maintain the regions. The route service and the origin node stay |
| Inventory and Market Isle | Instanced shop selling inventory expansions, furniture, houses, vehicles and gliders; currency for non-inventory items undefined | The Market Isle sells designs (blueprints), not finished items. Gliders are crafted at a table; a ship design opens a protected construction platform near a lighthouse port; a house design becomes a construction on the player's land. Designs and everything built from them are bound and never tradeable; special currencies are allowed. The portal is free and requires being idle |
| Movement and vehicles | Mounts that climb; no character climbing | Character climbing with stamina, difficulty per surface, gear and never-climbable surfaces. Ship hulls are climbed only with boarding hooks, the ship's crew ropes or movement skills. Open: whether climbing mounts use stamina |
| Defense: Guard per weapon | Spear: "sprint with frontal Guard" | Sprinting now costs stamina. The Spear's sprint with Guard is a separate skill and costs no stamina |
| Races | Sea folk: more breath and faster swimming | Compatible: breath stays separate from stamina, and the trait changes base swim speed, not the cost of fast swimming |
| Recorded decisions: Weapon swap | Weapon swap only out of combat | Unchanged. Profession gear lives in separate slots that are always active, so there is no loadout swap at all |
| Combat (new rule) | No definition of combat state | Combat starts on the first hostile action and ends 30 s after the last one |
| Infinite progression | Vertical power stops at the expansion cap; what is infinite is horizontal | Compatible and reinforced: progression is horizontal for most of the game, vertical only on gear |
| Housing: crops and animals | Crops keep their state when land freezes | Ready crops never wither. Neglected animals get sick but never die, unless the player slaughters them for meat |
| What the engine and platform must support | Rows for Maps, Progression, Housing and economy, and Platform with the old rules | Update those rows and add Nodes, Stamina and climbing, Profession gear and Actions (see Requirements by repository) |
| Recorded decisions, Still proposed, Open | None of this appendix's topics | Add the decisions and open items listed here |

## Differences from Technical Architecture v4

| Architecture section | What the Architecture says today | What this appendix changes |
| :---- | :---- | :---- |
| None (PvE and PvP participation) | v4 has no participation modes, Jurisdiction, mode isolation or Outlaw; the Vision has them since 13 Oct | Small component with mode, faction, Outlaw state and timers; target discovery decided by the attacker, filtered by target category; Jurisdiction as a rule volume (WORLD-2); PvE and PvP characters do not collide with each other but ride the same ship; timers in world time, inside the handoff snapshot |
| World space: volumes (WORLD-2) | Authored volumes for caves, flight zones, build zones, rule areas and indivisible volumes | New volume kind: the Node. Nodes have complex borders that follow the region border and tile it exactly with their neighbors. A region is a city node with its child nodes; open sea between islands belongs to transitional nodes. Cooked into node IDs per cell; cells on a border are marked mixed and resolved with an exact point-in-polygon test. About 64 bytes per node |
| World authoring: resources by spawn area | Volumes define the possible spawn locations of interactive resources | Kept, and extended: volumes mark which resource type can grow there, generically or for specific species. Each node's climate and environment decide which species actually exist. Hostile mobs are placed by hand in volumes that can hold several mob types and exact positions |
| Environment: weather | Weather state per region | Each node carries climate and environment data, which drives its fauna, flora and resources. Open: how node climate maps onto the runtime weather state per region |
| GPL-1: movement modes | Walk, sprint, dash, glide, mount; Water registers swimming | Character climbing as a movement mode. Stamina is spent by sprinting, fast swimming and climbing |
| GPL-7: flight and climbing | "Climbing mounts"; a mount climbs a marked wall | Free character climbing: a short cast to the wall, climb class and drain stored in the physics material per triangle, defaults by asset type (structures never climbable). Vertical cliffs need meshes because heightfields are 2.5D. Pitons, fixed ropes and hooks as world entities; ship ropes and hook ropes as climbable segments |
| Swimming, diving and breath | Breath meter when submerged; the sea folk swim faster | Breath stays; fast swimming spends stamina |
| None (stamina) | No stamina resource | Stamina with two cost modes (percentage of max in combat, flat value out of combat), regeneration as a percentage of max, owned by the server and predicted on the client through RunicGame::Shared |
| None (combat state) | No combat state rule | Combat starts on the first hostile action and ends 30 s after the last one; it gates teleports and switches stamina costs |
| Map knowledge (GSRV-6, GCL-4) | One bit per explored cell per character; reading a Carta merges the cells its cartographer recorded; cartography records cells traveled | The per-cell bit stays and marks "discovered". Discovered areas show one static image, the same for everyone, baked when the world is cooked. Mapped areas show a real-time top-down render of terrain only, never players, ships or mobs. Charts are per node and per layer, made by survey minigames resolved on the server, and consumed when used. Layer data goes only to chart owners. The player's exact position is always shown; a node's chart adds the node's information |
| Nautical charts | Made by sailing with a kit; cells sailed set coverage and value | Nautical charts per node, made by a minigame (star fixes, soundings, drift buoys), with no grade. The overlay is still sent only to chart owners |
| Services: Character; GSVC-7 | Labor in the Character service, per character; offline regeneration only for subscribers | Labor and its reserve are account-wide; the reserve is subscriber-only and computed at login from the logout time |
| Services: Economy | Regional auction houses, taxes and land fund | Territory and economy services: regions and nodes, prosperity through weekly missions, region projects, fixed weekly guild payouts, scheduled wars and the 3-node limit. One global auction with a seller tax kept by the NPC, NPC listings at the price cap, pack demand per region and the black market. Rolling market averages for missions, packs and the black market |
| Services: Guild | Membership, roles, progression and rules | Alliances, with admin tools to regulate guilds acting as unofficial alliances; up to 3 nodes per guild, or one region |
| Services: Mail | Delivery and claim rules | Mail carries items, with postage per unit that grows with the item's tier or value |
| Items: trade packs | World entities carried on the back or in vehicles | Go route service: node entries recorded by the server, danger recorded on entry, loops erased, detour cap. The pack keeps its origin node |
| Instances and world entities: Market Isle | Shop island as an instance | The island sells designs. Ship construction platforms become protected, timed world entities near lighthouse ports; house constructions become entities on the player's land |
| GameplayFlow: movement | "Teleport where explicitly legal" | Teleport only when idle (out of combat, no event, survey, trade pack or vehicle); a fixed fee plus distance, more between continents, computed on the server, with no cargo fee; game-started teleports are free; unstuck limited to the surroundings |
| Rule pipeline: "resolved loadout" | "Loadout" is the rule set compiled per character | Open: the clash is back, since the game now calls its fixed weapon pairs loadouts (CLASS-02); the compiled rule set may need another name. Profession gear never feeds the combat rule set |
| Input queue | Combat queue with a 200 to 400 ms window and one queued action | A 0.25 s floor on every discrete action, per rate key, skills included; the combat queue stays for combat |
| Sessions | The client connects straight to the simulation; interaction commands delivered per command type | Actions are envelopes per type, each with its own code and destination (simulation, quests, economy). The entry gate lives in the simulation that owns the player, with the floor per rate key and a flood budget per connection; its timers go into the handoff snapshot |
| GSRV-7, GSVC-10: professions | Gathering, crafting, farming and trade-pack production defined later; nine professions | Minigames seeded and resolved on the server, with the client sending only timestamped inputs; batch mode; profession gear slots; Larceny coin purse tiers; animal sickness; expanded list; labor tied to professions |

## Already applied to the Vision (on 30 Oct the English rewrite also took in every row of the table above)

* Pillar 7, "One world, the risk you choose".  
* PvE and PvP participation modes, Jurisdiction and the "Who finds whom" table, with target discovery decided by the attacker.  
* Outlaw and Infamy.  
* Balance Profile instead of "context".  
* Rune naming rule: nothing is ever just "Rune".  
* World bosses and the boss region as PvPvE.  
* The Skill API example now costs mana instead of stamina.

Apart from the Skill API example, these topics are not yet in Architecture v4 (see the first row of the table above).

## Pillar 8: Play without obligation

**Decision.** No dailies, login streaks or rewards that punish time away. Nobody loses anything personal by being away. Recurring content is weekly and community-driven, and its rewards are good but never necessary.  
Where the pillar already applies:

* Node prosperity belongs to the node, not to players.  
* The labor reserve rewards returning subscribers, with no deadline to use it.  
* Ready crops never wither, and neglected animals get sick but never die.

## Labor

* **Decision.** Every labor cost belongs to a profession. Actions without a profession cost no labor, only action time. Example: raising the anchor now costs only time, which reverses the earlier decision that charged labor.  
* **Decision.** Climbing is not a profession and costs no labor; it uses stamina. Exploration discoveries, such as items on summits, cost labor and belong to Cartography, since that labor is what cartography uses.  
* **Decision.** Labor is account-wide, shared by all characters. Alts do not add labor.  
* **Open.** Whether profession proficiency is account-wide or per character.

### Labor reserve

**Decision.** Subscribers who are away do not lose their labor regeneration:

* Offline, labor regenerates to the maximum as usual.  
* Once the bar is full, regeneration fills a reserve at a reduced rate (25% of the maximum per week).  
* The reserve is capped at 1× the maximum, so total available labor never exceeds twice the bar.  
* Spending uses the reserve first, so the normal bar keeps regenerating.  
* The reserve never expires; it only runs out when spent.  
* Labor and the reserve are account-wide.  
* The reserve is for subscribers only, following the existing rule that only subscribers regenerate offline.  
* It fills only offline with a full bar; daily players never get one and do not need one.  
* It shows as a second segment of the labor bar.

Example with a maximum of 1,000: three weeks away after the bar fills gives 1,000 labor plus 750 in reserve. A daily player still generates far more labor per month; a returning player is simply not punished.

## Combat state

* **Decision.** A character enters combat on the first hostile action, immediately.  
* **Decision.** Combat ends 30 s after the last hostile action.  
* Combat state gates teleports (a teleport needs the character idle, which includes out of combat) and switches stamina costs to the in-combat mode.

## Nodes

### What a node is

* **Decision.** The node is the unit of the regional economy, production and map discovery, defined as a volume. A region is a city node (the parent) with its child nodes: villages, mines, forests, farms, ports and islands. Every point of the map belongs to a node.  
* **Decision.** Each node type has its own prosperity and missions (see Prosperity and node missions).  
* **Decision.** At sea, a node that can be owned needs an island, a lighthouse or a dock. Open water, reefs and wrecks belong to transitional nodes, which no guild can own and which have no missions or prosperity; they exist so that connections, danger and the route service cover the whole map.  
* **Decision.** Nodes have complex borders: they follow the region's border and close exactly against their neighbors, with no gaps or overlaps. The editor validates this.  
* **Decision.** Some world rules are per node: controlled events and spawns, agriculture, climate and environment.  
* **Decision.** The map has three height bands (sky, surface, underground). The bands exist only in the interface; the engine stays in XYZ.  
* Engine: each node is a single cheap struct of about 64 bytes (1,000 nodes take about 64 KB per map). Node volumes are cooked into node IDs per cell, so "which node am I in" is a lookup done only when an entity changes cell. Cells on a border are marked mixed and resolved with an exact point-in-polygon test, which keeps borders precise. Shared economic state lives in a Go service, not in the struct.

### Node ecology

* **Decision.** Each node carries climate and environment data, which decide the fauna, flora and resources that exist there.  
* **Decision.** Map volumes define where a resource type can grow (ore, flora, fauna and so on), and the node decides which species actually grow. Example: one node has bananas and potatoes as flora and pigs and rats as animals.  
* **Decision.** Volumes can be generic ("potatoes and bananas can grow here") or specific ("only rats here"), so a designer can build a rat-infested area when they want one. This keeps content creation simple.  
* **Decision.** Hostile mobs are placed by hand in volumes. A volume can hold several mob types (goblins and wolves together) and exact positions.

### Connections

* **Decision.** Nodes are linked by connections. Nodes joined by a road are stronger than nodes joined over a mountain, and trade across weak connections costs more, because the resource becomes rarer.  
* **Decision.** A node at war adds an automatic cost to paths through it, and values rise while the war lasts.  
* **Decision.** Connection cost \= length × type factor: road 1.0; sea lane 1.2; trail or river 1.5; mountain pass 3.0.

### Guilds, regions and nodes

* **Decision.** Guilds take child nodes through node wars, and a large guild can take a whole region instead. A guild holds at most 3 nodes or one region, never both, so small guilds hold nodes and large guilds hold regions. The limit is a hard block.  
* **Decision.** On the neutral continent the ruling guild builds a castle in one of the region's castle zones. On the faction continents it uses the city itself and has an exclusive guild building.  
* **Decision.** Guild income works like Black Desert's: a fixed weekly payout by tier and prosperity, paid by the game. A region pays much more than a node, according to how well the ruling guild maintains it. Bonuses (a node mission at 200%, many region projects) count only inside the weekly cap, which is the fixed value of each prosperity level.  
* **Decision.** Wars are scheduled and need an active attacker. Each guild can challenge one node per week.  
* **Decision.** Alliances exist. Admins can regulate guilds that act as an alliance outside the system.  
* **Decision.** A guild needs about 10 active members to hold a node.  
* **Open.** What else the ruling guild decides besides spending packs on the region's projects.

## Regional economy

### Specialty and regional bonus

* **Decision.** Each node has a specialty family (ore, wood, fiber, fish and others). Refining or crafting that family at a station in the node returns part of the materials.  
* **Decision.** Base return anywhere: 5%. Anywhere in a region whose set includes that family: more (example: 10%). In the specialty node: the most, 15% to 35%, depending on prosperity.  
* **Decision.** Each region has a set of families (example: Carpentry, Logging, Leatherwork and Printing), and each node in it focuses on one or two of them.  
* **Decision.** Faction capitals also have a specialty: finished products, goods and equipment.

Example: in a mining node at prosperity 3, refining 100 ore returns 25, so the bars effectively cost 75 ore. Elsewhere they cost 95 ore. With ore at 10 silver, a batch costs about 750 against 950, roughly 21% cheaper, and the bars sell for the same price anywhere through the global auction.  
Consequences: with one global auction, prices are the same everywhere. The specialty pays off in production, so crafters travel to the node to refine and craft, and regional price movement lives in trade-pack demand.  
Tuning rule: the specialty bonus must exceed the cost of bringing the materials to the node (a teleport or the trip). Otherwise crafters stay home and specialization disappears.

### Prosperity and node missions

**Decision.** Each node has a prosperity level from 1 to 5, raised by a weekly community mission. Each node type has about three kinds of mission that rotate, and not all are deliveries: a mine asks for tools and props, a forest has a fire to fight, a village needs defense against raiders. Any player can take part, PvE players included.  
**Decision.** Missions pay a fixed price above the market, set when the mission is posted (example: 1.2× the rolling average) and fixed for the week, so taking part always pays.  
**Decision.** Delivering more than 100% gives a temporary buff, never a level: 150% gives it for 3 days and 200%, the cap, for 5 days. Proposal: the buff is 60% of the way to the next level's bonus.  
**Decision.** Resource and specialty packs feed the missions and the region's maintenance, and everything delivered is consumed by the projects.

| Week result | Levels 1 to 4 | Level 5 |
| :---- | :---- | :---- |
| 100% | Counts toward the next level; 2 counts give \+1 level | Holds |
| 60% to 99% | Holds | Loses 1 level |
| Below 60% | Loses 1 level | Loses 1 level |

**Decision.** The two 100% weeks do not need to be consecutive, and the count resets when the level changes.

| Prosperity | Effect |
| :---- | :---- |
| Higher | Bigger specialty bonus, more vendor stock, more trade-pack demand |
| Lower | Smaller bonus, thinner vendor stock, hostile spawns creeping back |

* **Lock.** At any level, the Altar, storage and the auction keep working. A neglected node never traps anyone's items.  
* Why this is not a chore: prosperity belongs to the node. Missions pay a fixed price above the market with no special reward, and missing a week costs no individual anything. The two-weeks-at-100% rule involves the guild more without punishing absence.  
* **Decision.** Region maintenance: the ruling guild spends the packs delivered to the city on building and repairing the region's structures. Projects give players bonuses and the ruling guild extra income inside the weekly cap. Projects wear down and need packs to stay up, and the region's tier limits how many are active.  
* **Decision.** Example projects, with more to come later: roads (mount speed on the region's roads), bridges and docks (shorter routes), workshops (a processing or crafting bonus), watch towers (patrols, fewer hostile mobs), shipyard (cheaper ship building and repair), lighthouse (visibility in fog near the coast), inn (a rest buff), Altar and temple (cheaper teleports to the city).

### Auction tax and guild income

* **Decision.** The auction has one tax, paid by the seller when the item sells, and the NPC keeps all of it as a sink. Only game admins change it, with 24 h notice.  
* **Decision.** Guilds earn no share of the auction tax; their income is the fixed weekly payout (see Guilds, regions and nodes).  
* **Decision.** This tax is called the "auction tax"; the weekly land tax keeps its name.

### How the pieces connect

Gatherers sell on the global auction, and crafters refine and craft in the specialty nodes. Trade packs turn materials into gold and special resources, and their payout follows each region's demand. Packs delivered to a city build and maintain the region, which raises prosperity and the ruling guild's fixed income. The auction tax, teleport fees, repairs and the black market's falling prices drain gold back out.

## Auction, storage and mail

* **Decision.** One auction for the whole world and every item. Prices are the same everywhere; regional price movement lives in trade-pack demand.  
* **Decision.** The seller deposits the item, which waits in the auction until it sells. The listing has a gross and a net price field: filling one shows the other, so the seller sees exactly what the tax takes, and the buyer pays only the listed price. If the listing expires, a mail notice arrives and the item is claimed back at any auction counter.  
* **Decision.** Every item has a minimum and a maximum price (PRICE-01). When an item is out of stock or the market goes above the maximum, an NPC listing appears and sells at a high price, which caps the market.  
* **Decision.** Personal storage is one global chest.  
* **Decision.** Auction purchases go to the inventory or the global chest. The guild bank is tied to its location.  
* **Decision.** Mail carries items. Sending is never free: postage is charged per unit and grows with the item's tier or value (example weights: common 1, uncommon 3, rare 10, epic 30, legendary 100, so 10 commons cost the same as 1 rare).  
* **Decision.** Teleports have no cargo fee (see Teleports and portals).  
* **Decision.** Unstuck only moves the player to the nearest safe spot within about 200 m, with a cooldown. Quest and event teleports go only to fixed destinations.  
* **Decision.** Hubs on the neutral continent emerge on their own, with no special benefits.  
* **Decision.** Black market: four passive goblins hidden in the world, one in an alley of each faction capital, one in the neutral continent's starting city and one on the pirate island. They buy only crafted equipment, which carries its crafter's name, and pay the current average auction price at once (proposal: the 7-day median with a minimum number of sales).  
* **Decision.** Each piece sold lowers what the goblins pay for that type and tier, and the price recovers as mobs drop the stock. When a regular vendor pays more, selling to the goblins stops on its own.  
* **Decision.** Items the goblins buy go into the drops of mobs of that tier. A piece sold to a goblin a second time is destroyed, like a sale to any vendor.  
* **Decision.** Mobs never drop gold. They drop materials and sometimes coin purses with gold and random resources, which cost labor to open, by tier.

### Teleports and portals

* **Decision.** A teleport only starts when the character is idle: out of combat, with no event, survey in progress, trade pack or vehicle.  
* **Decision.** Destinations are the settlement Altars of the player's faction or neutral ones. The Lineage sees on the map every Altar it has found, but each character must discover an Altar itself before respawning or teleporting there: respawn is at the nearest Altar that character has discovered.  
* **Decision.** Cost: a fixed fee plus a fee by distance, much higher between continents. From the field, the teleport also uses a consumable and has a long cooldown; from Altar to Altar, only the fees. There is no cargo fee.  
* **Decision.** Fixed world portals connect specific places (example: the bottom of one faction's continent to the bottom of the other's) and charge a high toll. Trade packs and mounts can't go through.  
* **Decision.** The Market Isle portal is free, since it is not travel. It returns the player to the same spot and also requires being idle.

## Market Isle

* **Decision.** The Market Isle sells designs (blueprints), not finished items. A design is consumed when crafting.  
* **Decision.** Gliders: the design is used at a crafting table.  
* **Decision.** Ships: using the design opens a construction platform near the water, close to a port with a lighthouse. Players add the resource packs to it. The platform is protected. If the construction is not finished within about 4 h, the platform disappears and the design returns to the player. Finishing the construction gives the item that summons the ship.  
* **Decision.** Houses: the design becomes a construction on the player's own land, and the finished house becomes an entity on that plot.  
* **Decision.** Designs and everything built from them (gliders, ship summon items, houses) are bound and never tradeable. Only the resources supplied for construction are tradeable. The island can use special currencies.  
* Inventory expansions keep the Vision's rule (paid with game gold).

## Trade packs and routes

* **Decision.** Only trade packs keep an origin node. Other items have no origin, because resources are already specific to certain areas.  
* **Decision.** Payout uses the node distance between origin and destination, not the path traveled.  
* **Decision.** A Go service records the pack's route, ignores repeated nodes, loops and convoluted paths, and builds a direct route that rewards the dangerous nodes crossed. This encourages crossing dangerous areas without rewarding walking in circles.  
* **Decision.** Payout \= cheapest-path distance × (1 \+ danger of the route's nodes). Each node's danger is recorded on entry. A detour longer than 1.5× the cheapest path only gets the cheapest path's danger. If the pack is stolen, the record continues with the new carrier.  
* **Decision.** Pack types, copied from ArcheAge: specialty packs from the region's packing bench (one per region, near its city node, with that region's recipes); aged packs from the larder, where aging honey, wine or cheese raises the value; cargo packs, consolidated by Commerce, which pay more the faster they arrive; resource packs (wood, iron, stone, fabric) from the processing stations (sawmill, smelter, loom, mason's table), which are less limited than the packing bench; and military aid packs.  
* **Decision.** Specialty packs combine several resources, sometimes with extra steps, and can pay well above their inputs: the route payout times the destination region's demand.  
* **Decision.** Resource packs never pay more than the auction value of their contents plus the effort. They build and repair the regions' structures and feed node missions, paying more before a mission reaches 100% and less after.  
* **Decision.** Military aid packs: a weapon pack and an armor pack made from basic crafted gear. The pack's tier is the items' tier, tiers can't be mixed, and no weapon type is required. They feed missions (village defense, watch towers) and nodes at war.  
* **Decision.** Demand per region works like a stock market: each delivery lowers that pack type's price there, it recovers over time, and events move it. Packs are delivered at specific points: cities, ports and islands.  
* **Decision.** The board in each city shows its own region's demand live; other regions' demand comes from a Commerce demand report, which goes stale.  
* **Decision.** When someone else delivers a pack, the deliverer gets 80% of the profit and the crafter 20%.  
* **Decision.** Construction uses packs, as in ArcheAge: buildings and their repairs, and vehicles at creation, except vehicles made at a bench, such as gliders. Resource amounts use the simplest clipper as the standard and labor costs copy ArcheAge's for now; every number is for balancing.  
* **Decision.** Packs delivered to a city go entirely to its projects; they never return to the auction.

## Maps and cartography

### Map detail levels

| Level | How it is reached | What the map shows |
| :---- | :---- | :---- |
| Fog | Default | Black, no map detail |
| Discovered | Walking through the area | One static image, the same for every player, baked when the world is cooked and refreshed when the world changes in an update |
| Mapped | The node's base chart | Real-time top-down render of the terrain, with zoom and a tilt into 3D; time of day, weather and floating-island motion. Never players, ships or mobs |

* **Decision.** The three detail levels above are the only levels of the map itself. Other charts add markers on top: monster spawns, flora types, resources, air and water currents, events.  
* **Decision.** The player always sees their exact position. Without a node's chart, the map shows nothing about the node; the chart adds the node's information in a Black Desert-style layout of nodes and connections: specialty, biome, environment, prosperity, owner and region.  
* **Decision.** The most basic chart already shows packing benches and vendors as icons and never expires. The map has many filters, one per kind of information the player buys or maps.  
* **Decision.** Charts unlock useful interactions in the game. That is why fan sites are fine: they show the information but cannot give the benefit.  
* **Decision.** A chart is consumed when used.  
* Engine: per Lineage, only the "discovered" bit per cell is stored (about 18 KB per map before compression). The real-time view is rendered from a cooked low-detail model of the world plus live state, so it reveals nothing about other players.

### Events on the map

* **Decision.** Without the events chart for a node, a player still sees that an event is happening there, but only while it runs or a few minutes before, as a marker on the region.  
* **Decision.** With it, the player sees a constant timer to the next events and their exact location.

### Chart layers

**Decision.** Each chart covers one layer of one node; no map holds everything. A finished chart has no quality grade.

| Layer | What it shows | In-game interaction |
| :---- | :---- | :---- |
| Base | Terrain, coast, paths, Altars, cave entrances; unlocks the Mapped level | Position on the map inside the node; route plotting |
| Resources | Spawn areas and what grows in them | Nearby resource areas highlighted in the world |
| Fauna | Species, danger, dens, patrol routines | Threat and aggro radius; patrol timing |
| Events | Where events happen and in which windows | Constant timers and exact locations; prediction at high proficiency |
| Environment | Currents, depth, reefs, whirlpools, weather | Live currents while sailing; prediction at high proficiency |

### Surveying

* **Decision.** Surveying is a PvP activity.  
* **Decision.** Each kind of cartography has its own tools and minigame (nautical charts use a sextant and other instruments). A survey applies only to the node where it is done.  
* **Decision.** Starter areas come surveyed, with charts for sale, so every player learns the mechanic.  
* **Consequence.** Since surveying is PvP, PvE players do not create base maps; they buy charts. This changes items 10 and 12.17 of the PvE/PvP contract v1.1 and the Vision's mode table.  
* **Decision.** Minigames of the other layers: nautical charts in open sea with star fixes at night and a line of soundings; environment with drift buoys tracked over time; fauna observed with a spyglass without being detected; resources from collected samples, whose quality depends on the gathering profession; events recorded by being present.

### Triangulation (base chart on land)

* **Decision.** The player places 3 tools in the world, inside the node. They exist for everyone, like trade packs: other factions, pirates and active Outlaws can destroy them and gain resources from it, and mobs attack them too. Hiding them until the survey ends is part of the game. They can be picked back up and are neither cheap nor expensive.  
* **Decision.** Placement quality is computed by geometry only: node area, triangle coverage and the angles of the three points. There is no line of sight.  
* **Decision.** Quality changes the survey's time and labor, not the finished chart.  
* **Decision.** Flow: place the 3 tools, see coverage and angle, see the computed time and labor, interact with the last tool and create the chart.  
* **Decision.** Coverage \= triangle area ÷ node area, up to 1\. The smallest angle scores 0 below 20° and 1 from 50°. Score \= coverage^0.6 × angle^0.4, with a minimum of 0.2 to start. Time \= base time ÷ score, up to 3×. Labor \= base labor × (2 − score).  
* **Decision.** Locks: one active set per character; tools expire after about 24 h; the cartographer stays inside the node during the survey; all 3 tools must survive to the end; the server recomputes the score from the real positions.

## Stamina and climbing

### Stamina

* **Decision.** Stamina is its own resource, separate from labor: labor is the economic budget in hours, stamina is physical effort in seconds and minutes.  
* **Decision.** Maximum stamina is raised in the exploration shop, which keeps it centralized. Items found on summits are one source of the shop's currency, among many others from exploration.  
* **Decision.** Uses: climbing, sprinting, fast swimming, open-sea fishing (stamina drains every second the fish is not caught) and other non-combat activities, such as moving heavy objects. Guard and evasion use their own charges, and combat skills never cost stamina.  
* **Decision.** In combat, costs are a fixed percentage of the maximum, so they last the same time for everyone. Out of combat, costs are a flat value per tick, so more stamina goes further.  
* **Decision.** Regeneration is always a percentage of the maximum, in and out of combat. Otherwise a larger maximum would take longer to refill and become a combat disadvantage.  
* **Decision.** The in-combat cost mode follows the combat state: it starts on the first hostile action and ends 30 s after the last. A chase before the first hit still uses flat costs; this is accepted.

### Climbing

* **Decision.** Climbing in the style of Crimson Desert, with stamina, for large vertical mountains and cliffs.  
* **Decision.** Getting hit while climbing deals the full normal damage and removes a fixed percentage of maximum stamina, regardless of the damage (e.g. 20%).  
* **Decision.** The terrain sets the stamina drain by difficulty. With gear, the gear sets the drain on the surfaces it covers, never making it worse. Surfaces that can only be climbed with gear have a drain that empties stamina in one tick.  
* **Decision.** The one-tick drain is a special value that empties the whole pool, so it works with any maximum; the character grabs and slips, which teaches that gear is needed. In combat the drain is divided by a fresh character's base stamina, so everyone climbs as if unupgraded.  
* **Decision.** Some surfaces can never be climbed, with any gear: castle and fort walls, barriers, zone boundaries, instance walls and house walls.  
* **Decision.** The default comes from the asset type: terrain and rock are climbable; every structure is not, and an artist opts a structure in on purpose (e.g. a ruined tower).  
* **Decision.** Spiked shoes (ice) and climbing gear (special surfaces) exist and also help on ordinary terrain. They sit in the profession gear slots, which are always active.  
* **Decision.** Consumables: the piton is a rest point that restores stamina, stays in the world for a while (about 2 h) and anyone can use it, with up to about 5 active per player; rope reduces the drain for a few minutes. A rope fixed between two pitons makes that stretch cheaper for everyone.  
* **Open.** Whether climbing mounts, already in the Vision, use stamina.

### Ships

* **Decision.** A ship's hull can be climbed only in three ways: with boarding hooks, which can be cut; with the crew ropes every ship has, which cannot be cut; or with movement skills to jump aboard.  
* **Decision.** Climbing gear has no effect on climbing ships.  
* **Decision.** The boarding hook is a consumable used from the hotbar. It is thrown as a projectile at a hull up to about 15 m away; the rope anchors to the ship and moves with it for about 30 s; anyone who can attack that ship can climb it; defenders cut it by attacking it or by interacting. Hooks only grab hulls, never walls or cliffs.

### Engine notes

* Climbing is a third movement component next to gliding and flying. A short cast finds the wall and reads the material, stored per triangle in the collision data.  
* Estimated cost: 2 to 4 casts per climber per tick, about 5 to 40 µs each. A hundred people climbing at once in one simulation use 0.5 to 4 ms of a 33 ms tick.  
* Heightfields are 2.5D and cannot make vertical walls or overhangs; large cliffs need meshes, with collision within 10 to 20 cm of the visuals. A 1 km by 500 m face at about 4 m² per triangle has about 125,000 triangles, loaded with the region.  
* Ship crew ropes and hook ropes are climbable line segments attached to the ship in ship-local coordinates, so they move with it and migrate with it in a handoff.  
* Hand and foot animation is visual only on the client; the server sees only the capsule and owns stamina.

## Profession gear and actions

* **Decision.** Profession gear has its own slots and is always active. There is no loadout swap.  
* **Decision.** Profession gear never grants combat stats. Climbing gear is profession gear, and its effect on PvP is small because in-combat climbing costs are a percentage of the maximum.  
* **Decision.** Profession slots are generic (head, hands, feet, body, tool), so pieces from different kits can be mixed, with a set bonus for a full kit.  
* **Decision.** The Vision's weapon-swap rule is unchanged.  
* **Decision.** Every discrete action has a minimum cooldown of 0.25 s (interactions, starting and stopping a sprint, using an item and so on), to prevent spam in a highly interactive world.  
* **Decision.** Each action is a data envelope with its own code, and the action itself knows where it goes: the simulation, quests, the economy or other services. The goal is a world with many interactions and room for roleplay.  
* **Decision.** A generic entry gate in the simulation that owns the player applies the floor without knowing what the action does. Actions can share a rate key (e.g. all emotes together). Each connection has a flood budget (about 10 actions per second). A command sent up to about 0.2 s before the action is ready is queued. World objects have their own interval (e.g. a door, 1 s). Unknown action types are rejected, and a rejection at the destination does not refund the floor.

## Professions

### Decisions

* Every labor cost belongs to a profession.  
* Cartography is a full minigame, per layer.  
* Gathering (mining, logging, herbalism) has specialized gear and quick-time events for better yields.  
* Fishing has a simple minigame for beginners and an expanded minigame. Sport fishing happens in open sea with boats and gear, and big fish are trade packs.  
* Jewelcrafting, alchemy, leatherworking, metallurgy, armorsmithing, weaponsmithing and others are crafting professions, each with its own flavor. Some can be simpler than others, but all have depth, such as gear that improves material return, quality or double yield.  
* Farming and animal husbandry are professions, practiced on the player's land: a cast bar and labor, with depth from placement and interaction with the world. Ready crops never wither. Animals neglected for a long time get sick but never die, unless the player slaughters them for meat.  
* Exploration is part of Cartography: discoveries that cost labor spend Cartography labor.  
* Language stays as in the Vision.  
* Dismantling returns part of the materials, more in a node with that profession's specialty, never more than a cap (example: 60% of the materials used). It is the same process as effect extraction: an item's effect becomes a gem, which can go into another weapon or be crushed into another resource.  
* Recipes are unique: there is no rule that a recipe uses the previous tier's item, although one line of equipment may.

### Larceny: coin purses

* **Decision.** Part of Larceny, built on grinding mobs. Mobs drop coin purses, and opening a purse costs Larceny labor.  
* **Decision.** Purses come in tiers. The higher the mob's level, the higher the tier it can drop, and it can also drop every lower tier.  
* **Decision.** Purses can yield a special resource, equivalent to ArcheAge's archeum. Its name is open and is never a plain "Rune".  
* **Decision.** High-tier purses are locked and use a lockpicking minigame; proficiency lowers the labor cost and improves the odds.

### Principles

* **Decision.** Labor caps volume; playing well raises the value of each labor point (quality, yield, material return), never the number of actions.  
* **Decision.** No idle loops: every catch and every craft needs a player action, and nothing repeats on its own.  
* **Decision.** Batch mode is allowed: skipping the minigame gives a plain result with no bonus.  
* **Decision.** The manual-skill bonus is capped (e.g. \+20% for perfect execution), because bots can automate quick-time events.  
* **Decision.** Each profession's gear is made by other professions, which ties the crafts together.

### Per profession

| Profession | Manual skill | Gear bonuses |
| :---- | :---- | :---- |
| Mining, logging, herbalism | Hit the vein's weak point, guide the tree's fall, pull the root without breaking it | Yield, double-yield chance, speed |
| Basic fishing | A tension bar from the very first fish, with no AFK phase | Rod, line, bait |
| Sport fishing | The fish shows its move and the player answers with the right technique; stamina is the timer | Rods, reels, lines, boats |
| Metallurgy | Keep the furnace inside a heat band | Material return, purity |
| Weaponsmithing and armorsmithing | Hammer strikes in rhythm on the glowing spot; quench timing | Quality chance, durability |
| Jewelcrafting | Each deeper cut raises quality and the risk of cracking the stone | Return on cracked stones, quality |
| Alchemy | Ingredients in order and on time; recipes discovered by experimenting | Double brew, potency |
| Leatherworking | Lay out pattern pieces on an irregular hide; a better layout yields more pieces | Hide yield, quality |
| Farming, husbandry | Cast bar and labor; placement and care of crops and animals | Growth speed, yield, animal health |
| Larceny (coin purses) | Lockpicking minigame on high-tier purses | Lower labor cost, better odds |

**Decision.** One shared crafting core (a 10 to 30 s session with a meter and a risk-and-reward step), to which each profession adds its own twist. This keeps development cost under control. The server seeds each minigame and decides the outcome; the client sends only timestamped inputs.

### References from other MMORPGs

* FFXIV: crafting as a turn-based puzzle with random conditions. The most involving, but solved rotations turn into macros.  
* Star Wars Galaxies: resources with varying stats, and surveying to find the best batches.  
* New World: gathering and crafting gear sets with yield bonuses.  
* Albion: one-click crafting, with depth in economic decisions (material return per city, focus).  
* Old School RuneScape: group skilling bosses, such as Tempoross for fishing.  
* ArcheAge: sport fishing that reacts to the fish, and farming in the open world. Its weak points are the early AFK fishing and cast-bar crafting.  
* BDO: AFK fishing and processing. The example to avoid, because idling earns almost as much as playing.

## Progression

**Decision.** Progression is horizontal for most of the game, with some vertical progression on gear. Stamina, climbing gear and the exploration shop grant reach, not power.

## Requirements by repository

### Engine

* Attacker-side target discovery filtered by target category, and collision layers that let PvE and PvP characters pass through each other while riding the same ship (pending since 13 Oct).  
* Node volumes that tile a region exactly, with editor validation (shared borders, no gaps or overlaps); cooked node IDs per cell, with mixed border cells resolved by an exact point-in-polygon test.  
* Resource-type volumes (generic or specific) and mob placement volumes with several types and exact positions, cooked with the world.  
* A climbing movement mode: wall cast, climb class and drain per physics material, asset-type defaults, cliff meshes and climbable line segments attached to moving ships.  
* A generic action entry gate in the owning simulation: action envelopes per type, a 0.25 s floor per rate key, a flood budget per connection, a short input buffer, and timers in the handoff snapshot.  
* Map rendering on the client: a baked static "discovered" image per map at cook time, and a real-time top-down terrain view from a cooked low-detail world model plus live state (time of day, weather, island motion), with no entities.

### Game

* Participation, Jurisdiction and Outlaw rules (pending since 13 Oct).  
* Combat state: enters on the first hostile action, ends 30 s after the last.  
* Stamina: two cost modes, percentage regeneration, server ownership and client prediction in RunicGame::Shared; climb drain tables, gear, pitons, ropes, boarding hooks and crew ropes.  
* Node data: climate, environment, species lists, specialty and connections.  
* Territory service (Go): regions and nodes, prosperity, weekly node missions, region projects, fixed weekly guild payouts, scheduled wars, the 3-node limit, alliances and admin tools.  
* Trade-pack route service (Go), with node entries recorded by the server.  
* The global auction (seller tax, gross and net price fields, NPC listings at the cap), pack demand per region, the black market, the global chest, mail postage per unit and teleport fees.  
* Labor and the reserve, account-wide, computed at login.  
* Charts per node and per layer, survey minigames, server-side triangulation scoring, layer data only to owners, event visibility rules, charts consumed on use.  
* Professions: server-seeded minigames, batch mode, profession gear slots, Larceny coin purse tiers, farming and husbandry with animal sickness.  
* Market Isle designs, ship construction platforms (protected, timed, near lighthouse ports) and house constructions on owned land.  
* Action policies per action type, as game data.

### Platform

* Nothing new. The appendix reuses existing Platform mechanisms: entitlements for the subscriber-only labor reserve, the item ledger's binding for Market Isle designs and their products, and instance allocation for the Market Isle.

## Open

* Whether profession proficiency is account-wide or per character.  
* Whether sport fishing is PvP-only, since big fish are trade packs and only PvP mode carries packs.  
* The full list of region projects and what each gives.  
* The mission catalog per node type (about three kinds each).  
* The numbers: the weekly payout per tier, how much more a region pays than a node, the region bonus (example: 10%) and the auction tax rate.  
* Whether a node can mark gathering as PvP-only.  
* Whether climbing mounts use stamina.  
* How node climate maps onto the runtime weather state per region.  
* The final name of the special resource found in coin purses (Larceny).

## Dropped

* An origin node on every item; only trade packs keep one.  
* A distance bonus on the price of ordinary items.  
* A contested hub with special benefits.  
* Line of sight between triangulation tools.  
* Charts with quality grades.  
* Profession and combat loadouts with swapping.  
* Boarding gear as profession gear; climbing gear on ship hulls.  
* A fixed, central table of actions.  
* A labor reserve with an expiry.  
* Summit items as direct stamina upgrades; they became exploration shop currency.  
* Labor to raise the anchor.  
* Faction capitals with no specialty.  
* A hard cap of 8 nodes per guild.  
* Per-character "discovered" images; one shared image is used instead.  
* Buying finished vehicles and houses at the Market Isle; it sells designs.  
* Local markets, local chests and auction houses per city, node or region; replaced by one global auction and one global chest.  
* The cargo fee on teleports, and mail limited to letters and small parcels.  
* The node market tax and the guild's share of it; replaced by a fixed weekly payout.  
* The shrinking guild tax share; replaced by a hard limit of 3 nodes.  
* The weekly list of materials; replaced by node missions.  
* Sea nodes fought over in naval battles; open sea is transitional.  
* Seeing your own position only with a chart.  
* Castles on every continent; they exist only on the neutral continent.  
* Teleports only to the capital or the player's house, and paid portals from the capital.  
* Community plazas and community packs.  
* Recipes that must use the previous tier's item.  
* Consuming an item to unlock its appearance.  
* Keeping unique or heroic items in the black market's rotation forever.
