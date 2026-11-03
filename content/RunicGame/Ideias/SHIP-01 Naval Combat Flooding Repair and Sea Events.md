---
title: "SHIP-01 · Naval Combat: Flooding, Repair and Sea Events"
aliases:
  - "SHIP-01"
  - "Naval Combat: Flooding, Repair and Sea Events"
tags:
  - "runicgame"
  - "idea"
  - "status/open"
id: "SHIP-01"
status: "Open"
source: "RunicGame — Ideias"
source_url: "https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit"
created: "2026-10-17"
modified: "2026-11-03"
---

**ID:** SHIP-01 · **Status:** Open

Ships never capsize: a big wave, a cannon or a collision deals damage and lets water in, never more. A ship has one health bar and sinks when it reaches zero, and water counts as health drained.

* **Two kinds of damage:** fixed damage from cannons and collisions, damage from events like big waves as a percentage of maximum health ([[SEA-01 Ship Handling and Sea Balance|SEA-01]]), and water. Each open breach below the water line drains the ship's health at a fixed rate, so a single breach left open can sink the ship; more breaches, faster drain.  
* **Repair heals:** closing breaches, bailing water (which heals what the water drained) and repairing the hull and the stations (which heals the fixed damage from cannons).  
* **Compartments and breaches:** each breach belongs to a compartment, and each compartment has a breach limit; the main body takes more breaches than the others. A breach drains only while its position is below the water line. *(proposal: bow 3, body 6, stern 3.)*  
* **Water line:** the sea is a height field made of sine waves, the same on the server and the client, so checking a breach is just comparing its height with the sea's height at that point. *(proposal: a heavily loaded ship sits lower, so more breaches go under; cargo like [[Trade packs and routes|trade packs]] makes a ship more vulnerable.)*  
* **What opens breaches:** cannon fire, collisions (ramming, reefs, icebergs), sea creatures and big waves. Normal player skills don't breach a hull. There are no explosive barrels and no items that explode on a ship.  
* **Bailing:** a bucket is an inventory item. Inside a compartment with water a prompt appears; filling puts the weapon on the back (it stays equipped) and the character starts carrying water. Carrying water doesn't slow normal movement, but the character can't sprint. Damage and CC never cancel it (a stun only stops the character moving); only the player cancels it. To empty, the player aims and throws, and a small cosmetic splash plays. The throw goes out of the ship when the ship's mesh isn't in the aim within the throw distance and the angle isn't too high; windows and other openings don't count as the ship's mesh. Otherwise the water goes back into the ship. Bigger ships have more compartments. *(proposal: filling and throwing take about 0.5 s each; the throw reaches about 3 to 4 m and also needs its end point outside the ship's footprint, so a throw across an open deck doesn't count; the angle limit is about 25° above the horizon; canceling or a bad throw puts the water back in the compartment it came from; using a skill or dodging is the player's choice, so it cancels the carry; buckets have quality, which sets capacity, and durability, like the kits.)*  
* **Repair kits:** each part (hull, sails, rigging, cannons…) is repaired with its own kit, made by a specific profession. Using a kit needs no profession level. Kits have durability, so one kit fixes several things. *(proposal: hull kits from Carpentry, sail and rigging kits from Tailoring, cannon kits from Machining; the crafter's quality sets the kit's durability.)*  
* **Not a resource sink:** because kits have durability, a little wood makes a lot of repair. There are no single-use planks like in Sea of Thieves.  
* **Ocean loot:** chests and shipwrecks can have kits. *(proposal: looted kits have less durability than crafted ones, so they don't undercut crafters.)*  
* **Big waves:** an event, like the rogue waves in Assassin's Creed IV: Black Flag, but less telegraphed. A big wave from the side deals damage and starts water coming in. *(proposal: taking it bow-on deals little damage, so the answer is to turn into it; forecasts warn of the storm area, never of the exact wave, [[INTEL-01 Resource Richness and Perishable Information|INTEL-01]].)*  
* **Whirlpools:** an event that pulls ships toward its center. *(proposal: damage near the center.)*  
* **Lightning:** a storm event, never from players. Lightning in the water stuns and damages. *(proposal: it strikes the tallest point, usually a mast, and damages it; a lightning-rod part protects.)*  
* **Storm ritual:** a ritual ([[RITUAL-01 Rituals|RITUAL-01]]) can summon a storm. It's relatively expensive, but far from divine level. *(proposal: a few minutes over an area, raising wind, waves and lightning for everyone, the caster's ships included; one per region at a time.)*  
* **Navigation:** all these events force changes in navigation.

**Engine:** described in [[Architecture|RunicEngine — Technical Architecture v4]] (Water: buoyancy and performance; Environment: Waves and Weather; Sailing, swimming and naval play: Naval combat).

---

↑ [[Ideias|Ideias]]  
Source: [RunicGame — Ideias](https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit) · exported 2026-11-03
