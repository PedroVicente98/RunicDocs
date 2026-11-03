---
title: "Project layout and schemas"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Project layout and schemas"
created: "2026-10-14"
modified: "2026-10-30"
---

```text
RunicGame/                          (a RunicEngine project)
  project.godot  runic.project.json
  Content/
    World.tscn                      world scene: layout, macro terrain, RunicRegion3D proxies
    Regions/West/Greenvale.tscn     region scenes with detail and markers
    Regions/West/Highland.tscn
    FloatingIslands/IslandChain_01.tscn
    Volumes/DeepCaves.tscn
    SharedAssets/Buildings/  Rocks/  Vegetation/  Materials/
    UI/                             player UI scenes and themes
  SkyWorld/World.tscn               (a separate WorldId)
  Data/                             skills, items, AI, quests, spawn rules
  Build/Cooked/MainWorld/           (cooked output)
    MainWorld.runicworld
    SpatialIndex.bin
    Regions/Greenvale/region.header
    Regions/Greenvale/Sector_x_z/Cell_x_y_z.client
    Regions/Greenvale/Sector_x_z/Cell_x_y_z.server
    Volumes/...  HLOD/...  Packages/...

RegionSource (read from the region scene)
  id:               game:greenvale
  world:            MainWorld
  volumes:          (caves, rule areas)
  global_origin:    (...)          stored in double
  authored_polygon: (...)
  neighbor_regions: (...)
  terrain_source:   ...
  object_sources:   ...
  roads/rivers:     ...
  gameplay_markers: ...            spawn areas, interactables, routes, colliders
```

The [[Cooker|Cooker]] derives the automatic sectors and cells and the runtime package dependencies.

**Contract:** one logical world is authored in the [[Tools#RunicEditor|RunicEditor]] as a low-detail world scene plus detailed region scenes; Blender makes assets and glTF is the border. Region is an authored concept; sector and cell are automatic runtime structures; simulation ownership is separate. Terrain borders derive from canonical shared data and cook with neighbor aprons. Artists work in region-local coordinates with 64-bit global origins and read-only neighbor proxies. The Cooker reads the scenes and emits Runic-native server and client packages, and Godot’s export emits the client .pck; no scene survives cooking. The world is indexed by sparse 3D cells and authored volumes; [[World space coordinates cells and activation#Activation volumes|activation volumes]] around players decide what loads and simulates, and separate maps are separate worlds.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Authoring work per roadmap slice|Authoring work per roadmap slice]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Project layout and schemas · exported 2026-11-03
