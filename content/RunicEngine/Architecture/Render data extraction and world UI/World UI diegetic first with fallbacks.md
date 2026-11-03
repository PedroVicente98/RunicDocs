---
title: "World UI: diegetic first, with fallbacks"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Render data, extraction and world UI (Engine, Game) › World UI: diegetic first, with fallbacks"
created: "2026-10-14"
modified: "2026-10-30"
---

Most UI lives in the world. Every world widget is authored once by the Game as a Godot UI scene (Control nodes and a theme), and the Engine decides how it is drawn from distance, on-screen count and frame budget. A widget declares its preferred mode and its fallbacks, so the same nameplate can be a full element up close and one instance in a batched draw across a battlefield. Player UI scenes are the one accepted use of nodes in the game: they are interface only and never hold game state.

| Mode | In Godot | Typical use | Cost |
| :---- | :---- | :---- | :---- |
| Diegetic panel | A UI scene inside a SubViewport whose texture sits on a quad or a mesh surface; input by ray, converted into panel coordinates | Notice boards, ship helm, crafting stations, shop signs, spell tomes | One offscreen render per visible panel, only when its content changes |
| Anchored element | Label3D or Sprite3D with an MSDF font, facing the camera or fixed to the object | The target’s nameplate, the interaction prompt tilted on a rock, a mount’s saddle, a chair, speech bubbles | A position update each frame; text layout when content changes |
| Batched | One MultiMesh of labels and bars from an atlas | Nameplates and damage numbers in crowds and battles | One draw call for all; the atlas changes only when a name or a style changes |
| Screen HUD | Ordinary UI scenes | Skill bar, inventory, map, chat | Standard Godot UI |

A diegetic panel at 512 by 512 in RGBA8 is 1 MB of video memory, so 20 active panels cost about 20 MB; a SubViewport redraws only when its content changes. Compared with RmlUi, Godot’s UI brings a visual scene editor, themes, localization, HarfBuzz text shaping and ready 3D UI; it has no declarative data binding, so [[How the Engine uses Godot|GodotBridge]] adds a small binder.

```cpp
// Illustrative: GodotBridge view-model binder
binder.Bind(vm.health,     hud, "HealthBar:value");
binder.Bind(vm.playerName, hud, "Name:text");
binder.Bind(vm.skills,     hud, "SkillBar:slots");   // list → slots
binder.Flush();   // each frame: only changed fields become set() calls on controls
```

* **Visibility follows gameplay.** Anchors carry the PvP visibility tier, so a Hidden player shows no nameplate and a Silhouette shows a reduced one.

* **Input reaches the UI first.** A click on a diegetic panel becomes a ray, the ray hits the panel’s quad, the hit becomes panel coordinates, and that panel’s SubViewport receives the event. Any action becomes a normal command that the server validates.

* **The UI never reads [[Simulation core Flecs and Jolt#Flecs rules|Flecs]].** Positions come from world anchors in the frame packet; content comes from Game view models.

* **Budgets protect the frame.** Each widget type has a cap per mode; beyond it, widgets fall back to the next mode, and battle mode lowers the caps.

```yaml
# Example values; the Game sets its own.
WorldWidget: game:nameplate
  Scene:     ui/nameplate.tscn      Theme: ui/world.theme
  Modes:     Anchored (targeted or within 30 m) -> Batched (within 120 m) -> Hidden
  Budget:    40 anchored, 500 batched; battle mode: 10 anchored
  Binds:     name, guild, health, visibilityTier

WorldWidget: game:notice_board
  Scene:     ui/notice_board.tscn
  Modes:     Diegetic (within 12 m) -> Hidden
  Surface:   mesh socket board_face, 1024 by 768 texels
```

---

↑ [[Render data extraction and world UI|Render data, extraction and world UI (Engine, Game)]] · ← [[Debug layers first the Godot look later|Debug layers first, the Godot look later]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Render data, extraction and world UI (Engine, Game) › World UI: diegetic first, with fallbacks · exported 2026-11-03
