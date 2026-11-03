---
title: "RunicGame — Appendix: Nodes, Economy and Exploration"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
created: "2026-10-19"
modified: "2026-10-30"
aliases:
  - "Nodes, Economy and Exploration"
---

Design appendix from the conversations of 13 to 19 October 2026, to be merged later into the game vision and the technical architecture. It was compared with the Drive versions of "[[Vision|RunicGame — Visão Completa do MMORPG]]" (13 Oct, including later manual edits) and "[[Architecture|RunicEngine — Technical Architecture v4]]" (14 Oct). It replaces the Portuguese draft of 19 Oct.  
The first two sections list every difference from those documents. The rest describes each system in detail, and the requirements at the end are split by repository: Engine, Game and Platform. Every item is labeled Decision, Proposal, Open or Dropped. Numbers are examples for tuning. Updated on 30 October 2026 after an economy review: one global auction, regional price movement in trade-pack demand, regions made of a city node and its child nodes, fixed weekly guild income, [[Regional economy#Prosperity and node missions|node missions]], teleports without a cargo fee and one global chest.

## Contents

- [[Differences from the Vision (Nodes and Economy)|Differences from the Vision]]
- [[Differences from Technical Architecture v4 (Nodes and Economy)|Differences from Technical Architecture v4]]
- [[Already applied to the Vision on 30 Oct the English rewrite also took|Already applied to the Vision (on 30 Oct the English rewrite also took in every row of the table above)]]
- [[Pillar 8 Play without obligation|Pillar 8: Play without obligation]]
- [[Labor|Labor]]
  - [[Labor#Labor reserve|Labor reserve]]
- [[Combat state|Combat state]]
- [[Nodes|Nodes]]
  - [[Nodes#What a node is|What a node is]]
  - [[Nodes#Node ecology|Node ecology]]
  - [[Nodes#Connections|Connections]]
  - [[Nodes#Guilds, regions and nodes|Guilds, regions and nodes]]
- [[Regional economy|Regional economy]]
  - [[Regional economy#Specialty and regional bonus|Specialty and regional bonus]]
  - [[Regional economy#Prosperity and node missions|Prosperity and node missions]]
  - [[Regional economy#Auction tax and guild income|Auction tax and guild income]]
  - [[Regional economy#How the pieces connect|How the pieces connect]]
- [[Auction storage and mail|Auction, storage and mail]]
  - [[Auction storage and mail#Teleports and portals|Teleports and portals]]
- [[Market Isle|Market Isle]]
- [[Trade packs and routes|Trade packs and routes]]
- [[Maps and cartography|Maps and cartography]]
  - [[Maps and cartography#Map detail levels|Map detail levels]]
  - [[Maps and cartography#Events on the map|Events on the map]]
  - [[Maps and cartography#Chart layers|Chart layers]]
  - [[Maps and cartography#Surveying|Surveying]]
  - [[Maps and cartography#Triangulation (base chart on land)|Triangulation (base chart on land)]]
- [[Stamina and climbing|Stamina and climbing]]
  - [[Stamina and climbing#Stamina|Stamina]]
  - [[Stamina and climbing#Climbing|Climbing]]
  - [[Stamina and climbing#Ships|Ships]]
  - [[Stamina and climbing#Engine notes|Engine notes]]
- [[Profession gear and actions|Profession gear and actions]]
- [[Professions|Professions]]
  - [[Professions#Decisions|Decisions]]
  - [[Professions#Larceny coin purses|Larceny: coin purses]]
  - [[Professions#Principles|Principles]]
  - [[Professions#Per profession|Per profession]]
  - [[Professions#References from other MMORPGs|References from other MMORPGs]]
- [[Progression|Progression]]
- [[Requirements by repository (Nodes and Economy)|Requirements by repository]]
  - [[Requirements by repository (Nodes and Economy)#Engine|Engine]]
  - [[Requirements by repository (Nodes and Economy)#Game|Game]]
  - [[Requirements by repository (Nodes and Economy)#Platform|Platform]]
- [[Open (Nodes and Economy)|Open]]
- [[Dropped (Nodes and Economy)|Dropped]]

---

↑ [[index|RunicDocs]]  
Source: [RunicGame — Appendix: Nodes, Economy and Exploration](https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit) · exported 2026-11-03
