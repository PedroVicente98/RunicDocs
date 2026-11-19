---
title: "NPC knowledge and trust"
tags:
  - "vision"
created: "2026-11-19"
modified: "2026-11-19"
---

Every NPC declares what it knows with a query, and what it will tell with gates. Nobody writes a list of answers per NPC.

### What an NPC knows

* **Personal entries,** listed by id: the king knows his own family.  
* **Filters:** a query by maximum depth, domains, concepts, spheres, types, scope (entries about its home and the places above it) and perspective (a temple's priest holds the temple's doctrine). Role templates carry the filters, so every lower priest of a temple knows the same things.  
* **Language:** an NPC answers only in its own language (`lang:x`).

### Trust and conditions

* Each depth has a gate on the NPC, met by any one of several sources, and an entry can add a gate of its own.  
* Gates and conditions use one small language: `npc>=Trusted` (standing with this NPC), `org:x>=Friendly`, `region:path>=Known`, `prof:x>=N`, `lang:x`, `quest:x`, `item:x`, `faction:x`, `race:x`, `level>=N`.  
* **Refusals:** an NPC can refuse outlaws, high Infamy, the enemy faction or pirates. A refused character gets Common answers at most.  
* **Standing** with an NPC belongs to the character and grows through the [[Knowledge exchange]], quests and other actions. Its tiers run from Acquaintance through Trusted to Confidant (names provisional). *Proposal: standing never decays, at about 6 bytes per NPC per character.*

### The answers

The server checks an entry in this order and stops at the first result:

1. **Doesn't know:** the NPC doesn't hold the entry. A Hidden or Lost word asked without a lead answers this way too, so typing can't fish for secrets.  
2. **Already known:** the character knows it, so the choice doesn't appear.  
3. **Refuses:** the language or a refusal rule keeps the NPC from discussing it with this character.  
4. **Needs groundwork:** the character lacks a required entry or condition. The NPC says what to learn first, which doubles as a hint.  
5. **Needs more trust:** a gate isn't met, and the NPC deflects.  
6. **Tells:** the character learns the entry.

Every result draws its line from a phrase pool (see [[Conversations#Dialogue layers|Dialogue layers]]).
