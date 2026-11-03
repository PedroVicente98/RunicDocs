---
title: "DMG-01 · Damage Types"
aliases:
  - "DMG-01"
tags:
  - "ideias"
  - "idea"
  - "status/in-game-vision"
id: "DMG-01"
status: "In game vision"
game_vision: "Skills by components › Damage types and defenses"
source: "RunicGame — Ideias"
source_url: "https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit"
created: "2026-10-17"
modified: "2026-11-03"
---

**ID:** DMG-01 · **Status:** In game vision · **Game vision:** [[Skills by components#Damage types and defenses|Skills by components › Damage types and defenses]]

Armor has two pools, physical and magical, each blended per piece. Plate is the best against physical damage and great against magical. Leather is good against both, below plate on both. Cloth is great against magical damage and low against physical.

**Physical subtypes** are a small matrix against armor weight, with no stat of their own, averaged per piece. A skill declares its subtype (ex.: a sword thrust is pierce).

* **Slash:** \+10% against cloth, 0 against leather, −10% against plate.  
* **Pierce:** 0 against cloth, \+10% against leather, 0 against plate.  
* **Blunt:** −10% against cloth, 0 against leather, \+10% against plate.

**Magic subtypes** are rules against the defense tools, never stats on items, so there are no enchant chores. You counter them by playing (dodge, block, cleanse), never by gearing.

* **Elemental:** magical armor and full Guard block; builds Burn, Chill and Shock ([[BUILD-01 Conditions, Build-up, Resolve and Tolerance|BUILD-01]]).  
* **Arcane:** ignores about 30% of magical armor; full Guard block; no states.  
* **Occult:** passes through Guard at reduced damage (ex.: 50%); lower raw damage; curses, which can be cleansed.

Final damage \= raw damage × (1 − reduction of the pool) × subtype multiplier.

**Creature traits** live on the content side: Armored (counts as plate), Ethereal (takes half physical damage) and Fire-born (immune to Burn). The bestiary reveals them ([[BEST-01 Bestiary|BEST-01]]).
