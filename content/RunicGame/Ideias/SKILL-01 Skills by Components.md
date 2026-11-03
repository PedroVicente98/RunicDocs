---
title: "SKILL-01 · Skills by Components"
aliases:
  - "SKILL-01"
  - "Skills by Components"
tags:
  - "runicgame"
  - "idea"
  - "status/in-game-vision"
id: "SKILL-01"
status: "In game vision"
game_vision: "Skills by components"
source: "RunicGame — Ideias"
source_url: "https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit"
created: "2026-10-17"
modified: "2026-11-03"
---

**ID:** SKILL-01 · **Status:** In game vision · **Game vision:** [[Skills by components|Skills by components]]

Every skill is built from data components: damage type, delivery, shape, timeline, effects, CC, world utility and interaction rules. Components are also the tags that skill trees, role passives and unique effects read, so tuning one component tunes every skill that uses it.

Damage type only decides which defenses apply; effects and CC are declared separately. Each component has a global coefficient for PvE and for PvP.

Interactions are condition → modifier rules, checked by the server when the skill activates and when it hits. The states created by a hit (Bleed, Stagger, Frozen) are the conditions the next skills read, so ArcheAge-style combos appear without hand-written pairs.

The Custom component is only for truly unique behavior and never replaces the standard components.

Each weapon has one timing profile that sets the rhythm of light and heavy attacks and scales skill recovery.

*Updated 2026-10-30: one timing profile per weapon, since there are no versatile weapons (was: a timing profile per grip).*

---

↑ [[Ideias|Ideias]]  
Source: [RunicGame — Ideias](https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit) · exported 2026-11-03
