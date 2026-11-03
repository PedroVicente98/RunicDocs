---
title: "Implementation order and definition of done"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › Implementation order and definition of done"
created: "2026-10-14"
modified: "2026-10-30"
---

1. Start the GodotLayer and open a window ([[GDB-1|GDB-1]]).

2. Implement DebugDraw lines and the line upload with the depth-tested and overlay materials.

3. Add a camera from the client into Godot’s viewport.

4. Implement grid, AABB, circle and sphere.

5. Implement cylinder, capsule, arrow, cone and OBB.

6. Implement the combat arc sector and arc volume.

7. Add filled shapes with opacity and debug text.

8. Visualize the predicted movement and the authoritative server position.

9. Add Path A of the [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] bridge; add the full Jolt debug interface only when needed.

10. Add the development overlay panel with layer toggles.

**Done when** a predicted capsule moves around a grid, the authoritative correction shows separately, attack volumes render with the same dimensions combat uses, and Jolt collision state can be inspected — without any simulation system calling Godot.

---

↑ [[Debug drawing|Debug drawing (Engine)]] · ← [[Performance and correctness|Performance and correctness]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › Implementation order and definition of done · exported 2026-11-03
