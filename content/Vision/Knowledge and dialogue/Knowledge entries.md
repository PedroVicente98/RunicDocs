---
title: "Knowledge entries"
tags:
  - "vision"
created: "2026-11-19"
modified: "2026-11-19"
---

A knowledge entry is one piece of what the world knows: a fact, a belief, a recipe, a drop rate, a section of a profile. Lore and quests are written freely as campaign notes and split into entries afterwards (see [[Knowledge Workbench]]).

### Depths

An entry's depth is who in the world knows it.

| Depth | Who knows it |
| :---- | :---- |
| Common | Almost anyone where it applies; told to anyone who asks |
| Doctrine | A group's teaching or belief, shared by its members. It can be biased, and some doctrines are kept for members or for people the group trusts |
| Expertise | What specialists know through study or craft |
| Hidden | Kept secret by the few who know it; it needs trust or a lead |
| Lost | Known by no one alive; found only in ruins, records and other traces |

### Facets

Every entry is tagged on several facets at once, so NPC queries and the knowledge tab can filter finely, and one entry can belong to several categories:

* **Type:** person, place, faction, god, creature, plant, item, recipe, event, rune and so on.  
* **Domain:** history, the sea, a craft and so on.  
* **Sphere:** mundane, arcane, divine, cosmic or void.  
* **Concepts:** the world's base concepts the entry involves.  
* **Depth**, **reliability**, **perspective** (whose view it is), **scope** (a path such as world, continent, region, location), **era** and **status**.

### Relations

* **requires** and **requires_any:** groundwork the character must already know.  
* **next:** the following step of a chain. A chain can go deeper as it goes: a Common entry, then an Expertise one, then a Hidden one.  
* **related**, **about** (the subject it describes: a person, a place, a creature), **unlocks** (what learning it opens: a lead, a quest, a profile section) and **sources** (where it can be learned).  
* **conditions:** other requirements, in the condition language of [[NPC knowledge and trust#Trust and conditions|Trust and conditions]].  
* **gate:** extra trust for this entry only.  
* **clarifies:** on a deeper entry, pointing at the Doctrine it explains (see below).

### Beliefs and misreadings

* **Every entry is true.** Only Doctrine can be a misreading: a vague or partial reading of something true, never an invented lie.  
* **Belief first:** the belief shows plainly, as it was told. Once the character learns the entry that clarifies it, the belief is marked as reframed, with a link to that entry.  
* **Truth first:** the belief shows with that context from the start.  
* `clarifies` only points at a Doctrine entry, and only from an Expertise, Hidden or Lost one. The Workbench checks it.  
* **No confronting.** Holding two entries never opens an argument with an NPC, and there is no "contradicts" relation.

### Where knowledge comes from

* Answers in conversation, and items shown to NPCs (see [[Conversations]]).  
* Story dialogue, which can give knowledge unprompted. Meeting a key NPC unlocks the basics of their profile.  
* Overhear zones (see [[Quests and story#Quest design|Quest design]]).  
* Acting on the world: inspecting, fighting, killing, gathering, reading books and inscriptions (see [[Knowledge tab and bestiary]]).  
* **Leads:** a lead says something exists and can be asked about, but not what it is. Leads come from all of the above and from what an NPC says they want (see [[Knowledge exchange]]).

### Visibility

* **Knowledge never leaves the server** except as what a character has learned. Unknown entries reach a client only as opaque handles with no title or id (see [[NPC knowledge web]]), so datamining the client shows counts and shape, never content.  
* *Numbers: learned entries are a bitset per character, e.g. 5,000 entries ≈ 625 bytes.*

### Illustrative format

The names are placeholders, not canon.

```yaml
id: altar-pact
title: The Altar pact
depth: H
type: event
domain: [history]
sphere: divine
scope: world
requires: [altars-give-rest]
clarifies: altars-were-a-gift
gate: npc>=Trusted
```
