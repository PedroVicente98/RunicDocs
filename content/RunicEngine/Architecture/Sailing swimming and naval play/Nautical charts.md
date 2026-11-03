---
title: "Nautical charts"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Sailing, swimming and naval play (Game) › Nautical charts"
created: "2026-10-14"
modified: "2026-10-30"
---

* Charts are map knowledge for the sea. Reading a chart unlocks a region overlay of currents, prevailing winds by season, reefs and safe routes, drawn on the client map from the cooked fields.

* The server sends the overlay when the chart is learned; it is not shipped openly with the client, so the knowledge keeps its market value. The water around the player still streams normally, because sailing needs it.

* Player cartographers make charts by sailing with a cartography kit: the cells sailed while recording set the chart’s coverage and value.

* Charts are tradeable items, and regions whose currents or winds change with the seasons can get new editions. Charts map the cyclic routine of sea and wind currents; a high-proficiency chart syncs with the current state, and a maximum-proficiency chart sees scheduled events (Proposal: each event defines from when it can be predicted).

---

↑ [[Sailing swimming and naval play|Sailing, swimming and naval play (Game)]] · ← [[Sea threats|Sea threats]] · [[Tides storms and sea gimmicks|Tides, storms and sea gimmicks]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Sailing, swimming and naval play (Game) › Nautical charts · exported 2026-11-03
