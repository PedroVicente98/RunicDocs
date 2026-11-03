---
title: "Profession gear and actions"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
section: "Profession gear and actions"
created: "2026-10-19"
modified: "2026-10-30"
---

* **Decision.** Profession gear has its own slots and is always active. There is no [[Weapon Class System#Loadouts|loadout]] swap.  
* **Decision.** Profession gear never grants combat stats. Climbing gear is profession gear, and its effect on PvP is small because in-combat climbing costs are a percentage of the maximum.  
* **Decision.** Profession slots are generic (head, hands, feet, body, tool), so pieces from different kits can be mixed, with a set bonus for a full kit.  
* **Decision.** The Vision's weapon-swap rule is unchanged.  
* **Decision.** Every discrete action has a minimum cooldown of 0.25 s (interactions, starting and stopping a sprint, using an item and so on), to prevent spam in a highly interactive world.  
* **Decision.** Each action is a data envelope with its own code, and the action itself knows where it goes: the simulation, quests, the economy or other services. The goal is a world with many interactions and room for roleplay.  
* **Decision.** A generic entry gate in the simulation that owns the player applies the floor without knowing what the action does. Actions can share a rate key (e.g. all emotes together). Each connection has a flood budget (about 10 actions per second). A command sent up to about 0.2 s before the action is ready is queued. World objects have their own interval (e.g. a door, 1 s). Unknown action types are rejected, and a rejection at the destination does not refund the floor.

---

↑ [[Nodes Economy and Exploration|Nodes, Economy and Exploration]] · ← [[Stamina and climbing|Stamina and climbing]] · [[Professions|Professions]] →  
Source: [RunicGame — Appendix: Nodes, Economy and Exploration](https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit) › Profession gear and actions · exported 2026-11-03
