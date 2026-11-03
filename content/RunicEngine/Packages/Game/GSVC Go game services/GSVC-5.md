---
title: "GSVC-5 · Build persistence in the Character service"
aliases:
  - "GSVC-5"
tags:
  - "runicengine"
  - "package"
  - "repo/game"
id: "GSVC-5"
module: "GSVC Go game services"
slice: "33a"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Build persistence in the Character service: loadout, [[Weapon Class System#Disciplines|Discipline]], skill points and level choices (class and role are derived); [[Real exploration#Altars, death, respawn and teleports|Altar]] reset that redistributes the points

**Done when:** A build survives relog; an Altar reset rebuilds the [[Weapon Class System#Loadouts|loadout]] and redistributes the points exactly once

**Needs:** [[GSVC-1|GSVC-1]], [[GSH-6|GSH-6]], [[PBB-2|PBB-2]]

**Slice:** [[Slice 33a Exploration prototype|Slice 33a · Exploration prototype]]

**Module:** [[GSVC Go game services|GSVC · Go game services]] (Game)

**Defined in:** [[Game|Technical Architecture v4 › Game]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
