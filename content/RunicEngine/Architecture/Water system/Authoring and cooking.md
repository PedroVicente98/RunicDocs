---
title: "Authoring and cooking"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Authoring and cooking"
created: "2026-10-14"
modified: "2026-10-30"
---

Water is authored in the [[Tools#RunicEditor|RunicEditor]] inside region scenes: rivers as RunicWaterBody3D nodes on a Path3D curve, lakes and oceans as bounded surfaces or volumes, waterfalls as connection and flow-volume markers, and current and wind maps as vector layers painted with a Runic editor tool. The shipping runtime never loads editor scenes; [[Cooker|the Cooker]] turns them into fragments.

```text
Node: GreatRiver_Main (RunicWaterBody3D, child Path3D)
  type          = river
  id            = game:great_river_main
  route         = game:great_river
  cross_section = engine:natural_river
  flow_profile  = game:medium_downstream
  material      = game:clear_river_water
```

* Read the curve and the node’s properties from the region scene.

* Validate the source in the Cooker.

* Sample the 3D centerline.

* Generate surface and LOD data for the client.

* Generate bounds and depth data.

* Generate or bake the flow representation, including ocean current fields.

* [[Combat#Resolve hard and light CC|Resolve]] WaterConnections.

* Split into Region, Sector and Cell fragments.

* Generate boundary aprons.

* Emit client water data (surfaces for the presenter).

* Emit server water assets.

Terrain coupling — carving the channel, riverbed and bank masks, wetness, vegetation and shoreline data — happens at cook time. At runtime, terrain and water are already cooked. A river is a gizmo-edited curve in the viewport, and the “see what the server sees” layer draws the cooked centerline, widths and flow arrows over it.

---

↑ [[Water system|Water system (Engine)]] · ← [[Streaming caves and cross-simulation continuity|Streaming, caves and cross-simulation continuity]] · [[Performance|Performance]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Authoring and cooking · exported 2026-11-03
