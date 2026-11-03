---
title: "SEA-01 · Ship Handling and Sea Balance"
aliases:
  - "SEA-01"
tags:
  - "ideias"
  - "idea"
  - "status/open"
id: "SEA-01"
status: "Open"
source: "RunicGame — Ideias"
source_url: "https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit"
created: "2026-10-17"
modified: "2026-11-03"
---

**ID:** SEA-01 · **Status:** Open

Sea content isn't only for large groups: a solo player or a duo on a clipper can cross the ocean and do much of the sea content, though not all of it. Every sea hazard can be overcome with a clipper, one way or another. Sea monsters and attachments are the extreme ones and already have their balance (the attachment limit per ship type, [[ATTACH-01 Ship Attachments|ATTACH-01]]); the other hazards are situational and affect everyone equally.

* **Clipper check:** content made with a galleon in mind can hit a clipper too hard, so every new sea hazard or activity is checked against a solo or duo clipper. The attachment limit per ship type is enough for now, but it stays under watch.  
* **Helm:** on every ship, the helmsman applies acceleration and rotation. Currents push the ship sideways, so holding a course needs constant correction. When nobody is at the helm, acceleration and rotation drop to zero, but the ship keeps its momentum, its sails keep pushing and the current carries it: it goes adrift.  
* **Side currents:** a current has its full effect along a ship's axis, from the bow or the stern, and only part of it from the side, by ship type. A clipper rides high on the surface, so side currents barely move it and it keeps its course with little correction, even with nobody at the helm. This is the clipper's advantage instead of a helm lock.  
* **Draft:** each ship type has a draft, how deep its hull sits. A ship hits only the reefs and sandbanks shallower than its draft, so a clipper passes over many that stop a galleon. *(proposal: cargo makes a ship sit lower, [[SHIP-01 Naval Combat Flooding, Repair and Sea Events|SHIP-01]], so a loaded clipper hits more.)*  
* **Event damage:** damage from events (big waves, lightning, waterspouts, maelstroms) is a percentage of the ship's maximum health, so it hits every ship type the same. An event that hits many times deals a small percentage per hit; a single big hit deals a large one. *(proposal, illustrative: a big wave from the side 15 to 25%, a lightning strike 3 to 5%.)*

**Engine:** [[RunicEngine — Technical Architecture|RunicEngine — Technical Architecture v4]] (Watercraft, Ships and Naval combat).
