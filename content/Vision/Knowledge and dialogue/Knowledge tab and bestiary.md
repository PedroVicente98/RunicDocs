---
title: "Knowledge tab and bestiary"
tags:
  - "vision"
created: "2026-11-19"
modified: "2026-11-19"
---

Where knowledge is kept: one tab for everything, in sections. [[Bestiary demo]] shows the bestiary's rules.

### The knowledge tab

* **One system, many sections.** People, places, factions, gods, creatures, plants, recipes and drop rates are all knowledge. How each section is laid out matters as much as what it holds. *Proposal: tabs for People, Places, Factions and organizations, Gods and faiths, Peoples, Bestiary, Flora and resources, History, and Runes and magic.*  
* **Profiles** are the unit, like Crimson Desert's: a person, place, creature or plant has a profile in sections (basics, family, ancestry, history and so on). Each section unlocks from its own source: a first meeting, a discovery, a kill, an observation or a conversation.  
* **Counts depend on the kind of information.** Some show their maximum (Common, Doctrine and Expertise entries, the number of creatures); others show nothing until discovered (Hidden and Lost entries, secret drops).  
* **One rule everywhere:** ordinary things show as unknown placeholders, so the player knows they exist; secrets don't appear at all until found.

### The bestiary

Like Terraria's bestiary, but deeper:

* **Basics** unlock by interacting with the creature: inspecting it (R), dealing damage to it or taking damage from it.  
* **Kills** unlock more, and kill thresholds unlock more again: behavior, weaknesses and so on.  
* **The loot table** reveals each drop at its own threshold, so the full table never shows at once: first that the creature drops it, then, after more kills, the drop rate. The rates shown are the loot table's true rates.  
* **Secret items** appear only once dropped.  
* **Conditional drops** have requirements, such as an active questline, and only drop while the requirement holds.  
* **Used in** lists the recipes the character knows that use the creature's drops.  
* **Lore** sections come from knowledge learned elsewhere, such as a sailors' tale (Doctrine).  
* *Proposal: plants work the same way, with inspecting and gathering in place of fighting.*  
* *Numbers: per character, a kill count, interaction flags and secret-drop bits ≈ 4 bytes per creature, so 120 creatures ≈ 0.5 KB. Rates come from the loot table, not from counters per character.*

### Illustrative format

The names are placeholders, not canon.

```yaml
creature: tide-lurker
reveal:
  basics: any(inspect, hit, hurt_by)
  behavior: kills>=1
  weaknesses: kills>=10
  lore: entry:lurker-sailor-tale
loot:
  - { item: lurker-scale, seen: kills>=1,  rate: kills>=25 }
  - { item: brine-sac,    seen: kills>=10, rate: kills>=50 }
  - { item: drowned-coin, seen: dropped, secret: true, drop_if: quest:drowned-bell.active }
```
