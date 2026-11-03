---
title: "How the systems connect"
tags:
  - "vision"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-10-30"
---

No activity lives in isolation: PvE, PvP, the open world and trade packs produce different resources that meet in endgame crafting, and the resulting gear goes back to the raids and the wars.

```mermaid
flowchart TB
  PVE["PvE — dungeons and raids<br/>raid-exclusive materials, drops and equipment"]
  PVP["Faction PvP<br/>gold, honor, special resources and contribution theft"]
  CRAFT["Endgame crafting<br/>raid mats + regional and special resources become<br/>weapons and armor used in raids and wars"]
  OW["Open world and housing<br/>gathering, farms, rare mobs, gold and regional resources"]
  TP["Trade packs<br/>carry production between regions;<br/>pay gold and special resources"]
  PVE --> CRAFT
  PVP --> CRAFT
  OW --> CRAFT
  TP --> CRAFT
  OW -- "production becomes cargo" --> TP
  TP -- "the cargo draws PvP" --> PVP
```

*Resource flow · 4 activities, 1 destination: PvE, PvP, the open world and trade packs converge in endgame crafting.*

*Resource flow · 4 activities, 1 destination (diagram from the 13 October version)*

Trade packs link the two halves: they carry the open world's production, create the PvP that pays honor and special resources, and build the regions through node missions and projects. Exploration feeds all of it with charts, routes and access to rare resources, and the world auction lets every player, PvE or PvP, sell what they make.
