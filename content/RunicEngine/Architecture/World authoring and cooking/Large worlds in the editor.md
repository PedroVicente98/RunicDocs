---
title: "Large worlds in the editor"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Large worlds in the editor"
created: "2026-10-14"
modified: "2026-10-30"
---

World.tscn never loads the detail: it holds references to the regions and a proxy of each. Instancing a scene inside another loads all of it in Godot, which is why RunicRegion3D does not instance its region.

1. Opening World.tscn shows every region as a proxy, plus the macro terrain.

2. A double click on a region opens its scene in another tab; only then is its detail loaded.

3. Neighbors appear as proxies, not as full scenes.

4. When a region is saved, a Runic tool simplifies its content and rebuilds its proxy in the world.

Estimate for a 100 km² world (10 by 10 km in 25 regions of 2 by 2 km):

| What is loaded | Size |
| :---- | :---- |
| World macro terrain at 8 m resolution | 1,250 × 1,250 \= 1.6 million 16-bit samples, about 3 MB |
| 25 proxies of about 20,000 triangles | 500,000 triangles; a common GPU draws millions per frame |
| **Total when opening the world** | **A few MB** |
| One detailed region: terrain at 0.5 m | 4,000 × 4,000 \= 16 million samples, about 32 MB |
| One detailed region: 200,000 decorative trees and rocks in MultiMesh | 48 bytes per instance, about 10 MB |
| **Total when opening a region** | **Tens of MB, plus the meshes** |
| All 25 detailed regions at once | Over 1 GB and a huge node count; what the model avoids |

* **Decorative vegetation in MultiMesh:** one node draws thousands of instances; a node per tree would make the scene tree enormous.

* **Precision:** detail is edited only inside a region, near its local origin; the world scene is at layout scale.

* **The [[Cooker|Cooker]] never loads everything either:** it cooks region by region (open, write cells, unload) and re-cooks only changed cells, so its memory is one region plus its neighbors’ borders.

* **Larger worlds:** at 1,000 km² or more the model is the same; only the proxies grow, and the world scene can use coarser proxies or split by continent.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[World scene and region scenes|World scene and region scenes]] · [[Seamless terrain and borders|Seamless terrain and borders]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Large worlds in the editor · exported 2026-11-03
