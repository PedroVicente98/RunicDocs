---
title: "Sailing, swimming and naval play (Game)"
tags:
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-13"
---

RunicGame builds its seas on the Engine water and environment APIs: ships, sails, cargo, naval combat, breath, sea threats and nautical charts are game data and rules, while the Engine only floats, moves and samples.

### Ownership

| Game system | Built on (Engine) | Durable state (Platform) |
| :---- | :---- | :---- |
| Ship classes: hull, sails, oars, cargo capacity, crew stations, cannon slots | Jolt dynamic body, BuoyantBody, WatercraftMovement | Ship ownership in the item ledger |
| Sailing controls: helm, sail trim, anchor, oars | WatercraftMovement intents, wind | — |
| Cargo and trade packs on board | CargoOf relationships, group handoff | — (trade packs are world entities) |
| Passengers, boarding, falling overboard | PassengerOf, CharacterVirtual on moving bodies, CharacterWaterMovement | — |
| Naval combat: cannons, ramming, hull damage, breaches and flooding, sinking | Ability toolkit with the ship as source, the impact pipeline, BuoyancyProfile scale and righting strength, water samples at breach points | Repairs through the economy game service |
| Swimming, diving and breath | CharacterWaterMovement, WaterInteractionState | — |
| Sea threats and water bosses | AI framework, CharacterWaterMovement, perception, SwimMovementModifiers | — |
| Nautical charts | Map knowledge, cooked current and wind fields | Learned charts in the character service |
| Naval raids | Instances, lent ships | Raid rewards |
| Tides, storms and sea gimmicks | Tides, weather overrides | Event schedule in the world-events game service |

### Ships

* **A ship is an entity** with Transform, a Jolt dynamic body, BuoyantBody, WatercraftMovement and ShipTag, plus Game components: hull points, compartments with breach limits, cargo capacity, crew stations and cannon slots. Ship classes, from small boats to large warships, are data. Each class lists the part slots it allows (hull, bow, masts, sails, helm, cannons and more), and part upgrades are data that change the ship's stats (e.g. an ice bow takes less ice damage, a ram bow deals more collision damage).

* **Controls are intents:** the helm steers, sail trim scales sail force, the anchor adds heavy drag, oars or other propulsion move small boats without wind. The helmsman applies acceleration and rotation, and currents push the ship off its heading, so holding a course needs constant correction. With nobody at the helm both intents are zero, while the ship keeps its momentum, its sail force as trimmed and the current: it drifts. Ship classes set lateral\_current\_influence, so a clipper holds its course in a side current far better than a galleon, and their hull depth is their draft ([[RunicGame — Ideias]], [[SEA-01 Ship Handling and Sea Balance|SEA-01]]).

* **Passengers** stand on deck as CharacterVirtuals carried by the moving body. Boarding is walking or jumping onto the deck; falling overboard switches the character to swimming.

* **Cargo:** trade packs aboard are CargoOf entities. When a ship sinks they become floating objects (BuoyantBody and ObjectWaterMovement) that drift with the current and can be looted, which feeds piracy and PvP.

* **Range bonus at sea:** a rule-pipeline condition (caster is a passenger of a ship) adds the small range bonus [[RunicGame — Complete MMORPG Vision|the game vision]] gives eligible skills.

* **Handoff:** hull, passengers and cargo transfer to the next simulation together, in one authority epoch.

* **Ownership and persistence:** owned ships are items in the Platform ledger; the ship spawns at a dock, and damage and repairs are economy operations. Proposal: a sunk ship returns damaged to its home port and its cargo stays at sea.

### Naval combat

* **Cannons** are abilities whose source is a crewed ship station, using projectile shapes that hit hulls and characters on deck. Wind affects them only if the skill sets the wind flag.

* **Hull damage** goes through the impact pipeline on the ship entity, with Game defense stages and values per ship class. A ship has one Game resource pool of hull points: cannons, ramming and sea creatures deal fixed damage; environment events (big waves, lightning, waterspouts, maelstroms) deal a percentage of the ship's maximum hull points, small per hit for events that hit many times and large for a single hit, so every ship class takes them the same way; and water counts as hull points drained.

* **Ramming** reads Jolt contacts; the Game turns contact speed and mass into damage.

* **Sinking:** at zero hull points the Game lowers the BuoyancyProfile scale over a few seconds, so the ship physically sinks while passengers swim away. Ships never capsize: the righting strength keeps them upright, so the worst a ship takes is damage and water.

* Breaches belong to a hull compartment, and each compartment has a breach limit; the main body takes the most. About 5 times a second the Game tests each open breach with WaterSystem::TrySample; a breach under water drains hull points at a fixed rate, so a single breach left open can sink a ship.

* Repair heals in three ways: closing breaches, removing water (which restores what the water drained) and repairing the hull and stations (which restores fixed damage). Each ship part has its own repair kit with durability, and using a kit needs no profession level. Removing water uses bailing, described next.

* A bucket is an inventory item used for bailing. Each ship class authors its compartments as volumes in ship space, so bigger ships have more; when a character stands in a compartment with water, the interaction prompt appears. Filling stows the weapon, which stays equipped, and sets a carrying-water state built on the GameplayAPI character state, movement modifiers and interactions: no sprint (normal movement speed is unchanged), kept through damage and CC (a stun only stops movement), and ended only by the player. Emptying sends the aim direction with the action; the server casts one short ray along the aim against the ship's own collision only, and the throw counts as out when the ray hits nothing of the ship within the throw distance, its end point lies outside the ship's footprint and the pitch stays below a limit (window and opening shapes sit on a pass-through collision layer the ray ignores); it then removes that water and restores the hull points it drained; otherwise the water goes back into the ship. The splash is a client-only cosmetic projectile, so nothing is simulated on the server; each throw costs one ray against one body and one point-in-box test.

* A big wave that hits a ship from the side deals damage and opens a breach; whirlpools pull ships toward their center. Both are Environment events (see [[Environment wind, currents, tides, waves and weather (Engine)#Waves|Waves]]).

* Storm lightning strikes the highest point, usually a mast, and damages it; in the water it stuns and damages characters within a radius. Lightning comes only from storms, never from player abilities.

* Replication per ship: hull points, the water per compartment and about 3 bytes per breach, sent only when they change.

* **Naval raids:** the instance limits the number of ships, lends each player a raid ship, allows the raid ship or the player’s own but not both, and expires lent ships when the raid ends.

### Swimming, diving and breath

* SwimProfiles vary by race (the sea-born race swims faster, a convenience trait) and may vary by armor once the vision document settles armor effects.

* **Breath:** while head\_submerged, a breath meter drains; the sea-born race has more breath. An empty meter applies drowning damage. Below a set depth the meter drains faster, and diving gear reduces that.

* **Abilities in water:** skills can require “not swimming” through tags; underwater light falls off with depth through the water body’s attenuation values.

* Currents push swimmers through their profile’s current influence, so crossing a strong river is a real obstacle.

### Sea threats

* Each sea region has its own creatures (sharks, reef creatures, sea monsters) using CharacterWaterMovement, behavior trees and perception profiles; some are drawn to ship lanterns at night.

* Small boats are more vulnerable: creatures can target hulls as well as swimmers.

* Water bosses use SwimMovementModifiers for charges, dives and breaches.

### Nautical charts

* Charts are map knowledge for the sea. Reading a chart unlocks a region overlay of currents, prevailing winds by season, reefs and safe routes, drawn on the client map from the cooked fields.

* The server sends the overlay when the chart is learned; it is not shipped openly with the client, so the knowledge keeps its market value. The water around the player still streams normally, because sailing needs it.

* Player cartographers make charts by sailing with a cartography kit: the cells sailed while recording set the chart’s coverage and value.

* Charts are tradeable items, and regions whose currents or winds change with the seasons can get new editions. Charts map the cyclic routine of sea and wind currents; a high-proficiency chart syncs with the current state, and a maximum-proficiency chart sees scheduled events (Proposal: each event defines from when it can be predicted).

### Tides, storms and sea gimmicks

* Tidal regions open paths at low tide from the Game’s tide tables.

* Regional weather brings storms with stronger wind, rougher swell, darker light and harder steering; a world-events game service can trigger special storms and sea-monster events through Platform directives.

* A storm ritual, a relatively expensive player ritual, can request a storm override for an area through the same world-events service, one per region at a time.

* Sailing on open sea switches the music context to sailing through Game presentation.

### Sea hazards

* Hazards follow one rule: the server simulates the simplest model that decides gameplay, and the client sells the spectacle (fog walls, spray, debris, lightning, sound). The game design is in RunicGame — Ideias, [[HAZARD-01 Environmental Hazards|HAZARD-01]]. Hazard effects go through Resolve and Tolerance like attacks, unless a hazard is flagged in its data to ignore them (e.g. slips).

* Static hazards (the ocean floor, reefs, sandbanks, glaciers) are terrain and collision cooked from the map's hazard layer, plus tagged hazard volumes in the spatial index: reef, shallow, freezing water, vent, kelp, fog bank and calm zone. Reef, sandbank and iceberg hits are Jolt contacts that the Game turns into damage, and reef and iceberg hits also open breaches.

* Freezing water and vents are volume or water-body tags: while a character's WaterInteractionState says it is swimming inside one, the Game applies condition build-up through status storage and its build-up policy (Chill or Burn) at the status tick rate, with the build-up rate set per water body or volume.

* Fog banks are volumes whose density scales the perception radius and visibility tiers of everyone inside. They drift by the wind function, so their position is a pure function of world time, like any routine. Calm zones are areas where the wind routine's speed is zero.

* Drifting icebergs are BuoyantBody objects with ObjectWaterMovement; the mostly underwater ones simply have most of their collision below the surface.

* Events (giant waves, waterspouts, maelstroms) are Environment overrides. A waterspout or a maelstrom center is one entity with a position routine and a radius: at about 10 Hz it queries the ships inside its radius, pushes them with a swirling current override, and the Game applies the damage. Inside a maelstrom the Game deals chip damage to ships sailing against its current and heavy damage at its center, enough to sink most ships in seconds; an entrance maelstrom moves a ship that reaches its center, with its whole group, into a rift or raid instance. Lightning uses the highest-point query from Weather.

* False lights and sirens are NPCs with perception and behavior trees; a siren's pull is an offset added to the helm's WatercraftMovement intent while its song lasts.

* Ships can anchor anywhere, deep ocean included: the anchor adds heavy drag and doesn't need the seafloor.

* Cost: static hazards do no work until something touches them, through contacts and volume membership the engine already computes; a cyclic hazard is a pure function with nothing replicated per tick; an event is one override fact plus one entity; a vortex's 10 Hz radius query touches only the ships near it.

### Ship attachments

* An attachment is an entity linked to a ship by an AttachedTo relationship to a hull socket, like passengers (PassengerOf) and cargo (CargoOf). It has no physics body: its transform is the socket's transform on the ship, so it costs no movement simulation.

* Engine needs: hull sockets authored per ship class in the editor (a point and a normal in ship space, flagged as reachable from the deck or only over the side), the AttachedTo relationship, and attachments in the ship's transfer-snapshot group, so they cross simulation borders with the ship (WATER-7).

* Each attachment is a light Character: a Game health pool, its statuses and one small behavior that ticks every 0.5 to 1 s. It drains hull points, adds weight (a step in the BuoyancyProfile scale), tags the ship for an AI's or a faction's perception (tracking), spawns boarders or applies build-up to the characters on deck. Each sea region has its own attachment types, from basic to dangerous, so no region is fully safe.

* Removal uses normal combat: hit volumes reach sockets near the rail; sockets low on the hull need a character leaning over the side, an interaction that exposes them and can make them fall; fire and cleanses act through the status system.

* Cost: about 64 bytes of server state per attachment. With a limit of 1 to 8 per ship, by ship type, and 100 ships at sea carrying them, that is at most 800 attachments, about 50 KB, and 800 to 1,600 behavior ticks per second, well under 1% of one core. Network: one spawn and one death event (about 16 bytes each) and a health value sent only when it changes; attachments add no movement traffic, because they follow the ship's transform.

* Visuals sell it: the client grows tentacles, chains or coral on the hull from the socket and the attachment type. The game design is in RunicGame — Ideias, [[ATTACH-01 Ship Attachments|ATTACH-01]].

### Sea acceptance list

1. Board a ship at a dock and sail to an island, faster with a favorable current and wind than against them.

2. Load trade packs as cargo, cross a simulation border with passengers aboard, and arrive with nothing lost.

3. Sink a ship with cannon fire; passengers swim and the cargo floats and drifts with the current.

4. Dive until the breath meter empties and drowning damage starts; the sea-born race lasts longer.

5. A sea creature attacks a small boat at night, drawn by its lantern.

6. Read a nautical chart and see the region’s currents and winds appear on the map.

7. A storm event roughens the sea and makes steering harder in two simulations at once.

8. A cannonball opens a breach below the water line; hull points drain until the breach is closed, and removing the water restores them.

9. A big wave from the side damages a ship and opens a breach; in a storm swell ships roll and pitch but never capsize.

10. Storm lightning strikes a mast and stuns swimmers nearby.

11. A character fills a bucket in a flooded compartment, keeps carrying it through a stun and empties it through a window or over the side; a throw that hits the ship or goes too high returns the water.

12. A ship that hits a sandbank takes collision damage and keeps moving.

13. Inside a fog bank, enemy ships and nameplates appear only up close.

14. A Hull Leech latches onto a ship, drains hull points until the crew kills it, and crosses a simulation border with the ship.

15. A swimmer in freezing water slows down from Chill build-up.

16. With nobody at the helm, a clipper and a galleon cross the same side current; the clipper drifts much less, and it passes over a sandbank that the galleon hits.

17. A big wave takes the same percentage of hull points from a clipper and from a galleon.
