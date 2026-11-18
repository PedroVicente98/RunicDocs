---
title: "RunicGame — Appendix: Rendering, Lighting and Visibility"
tags:
  - "archive"
  - "appendix"
  - "appendix/rendering-lighting-visibility"
source: "RunicGame — Appendix: Rendering, Lighting and Visibility"
source_url: "https://docs.google.com/document/d/1oP7aeYNn9fGfT7xAMSHeonojFWWq9fCQ5hKgLHjO7nc/edit"
created: "2026-11-09"
modified: "2026-11-09"
---

Design appendix from the conversation of 9 November 2026 about visual direction, far rendering, lighting, fog and haze, and how far entities are visible. To be merged later into RunicGame — Visão Completa do MMORPG, RunicEngine — Technical Architecture v4, RunicGame — Appendix: Content Pipeline and Art Direction (26 Oct) and RunicGame — Ideias. It builds on the Content Pipeline and Art Direction appendix and does not repeat it.  
**In short:** mid-poly characters in a low-poly, stylized world. Everything is rendered as far as possible with levels of detail (LOD); fog never hides distance. Air haze is always on and makes the world feel bigger than it is. Lighting comes from cook-time bakes that work at any sun angle, plus real-time sun shadows up to 100 m. Entities are visible up to 1 km, less in darkness, and the client only knows what the player knows: an unseen attacker leaves a colored silhouette on screen. The far entity tier is a future idea, after the vertical slice.  
**Labels.** Decision: stated or accepted in the conversation. Proposal: recommended, not yet accepted. Open: a known question. Dropped: considered and rejected. Future idea: goes to Ideias. Numbers are planning estimates; CPU costs are ±3× unless noted, and final values come from measuring in Godot.

## Where each part goes

| Destination | What goes there |
| :---- | :---- |
| Vision | Visual direction, platforms, the render-distance and fog principles, haze, the visibility rules (1 km, light, blindness, silhouettes and their colors), NPCs in distant cities and ports |
| Architecture v4 | Client runtime (visibility range, silhouettes, IK, GI quality levels, haze and fog layers), World authoring and cooking (light bakes, HLOD, far terrain, impostors), Godot integration (Terrain3D as a runtime node), interest management and combat netcode notes |
| Content Pipeline and Art Direction appendix | Painted light, master shaders, animation tools, root-motion extraction, the impostor plugin, polygon budget decision |
| Ideias | The far entity tier and the sound-cue channel (Future idea) |

## Differences from existing documents

| Document › section | What it says today | What this appendix changes |
| :---- | :---- | :---- |
| Content Pipeline appendix › Texture approach | Stylized physically based textures; warns that painted highlights do not move with the sun | Unchanged. Painted light is limited to cues that are true at any hour (crevices, worn edges, cool tint); the top-down gradient lives in the master shader (Decision) |
| Content Pipeline appendix › Budgets | Player 25k to 35k triangles | Characters are mid-poly; everything else is low-poly, with mid-poly exceptions such as some ships and items (Decision). Environment budgets still need numbers (Open) |
| Content Pipeline appendix › Environment and Open | Impostors: Engine task or plugin (Open) | Octahedral Impostor LOD plugin, for now (Decision) |
| Content Pipeline appendix › Animation | Quaternius main source, Mixamo internal only, retargeting in Godot, hit markers | Adds root-motion extraction into skill movement data, Cascadeur for swings, foot and hand IK (Decision) |
| Architecture v4 › Godot integration | Godot nodes are authoring representations; the cook creates everything without nodes | Terrain3D runs as a Godot node on the client: an exception (Decision). The server is unaffected |
| Architecture v4 › World authoring and cooking | Terrain hydrology derived from the elevation layer at cook time | Adds light bakes (horizon, sky visibility, canopy, server darkness grid), HLOD proxies and far-terrain canopy (Decision) |
| Architecture v4 › combat netcode | Telegraph fast-forward, defender grace (150 ms), predicted impact effects | They apply only to entities the client knows. Hits from unseen attackers resolve on the server; hits on unseen targets are confirmed after a round trip (Decision) |
| Architecture v4 › interest management | Processing ellipse of about 1 km around players | Entities are sent up to 1 km at most, shortened by light, with hysteresis; the client knows only what the player knows (Decision) |

## 1. Visual direction

* **Decision.** Characters are mid-poly. Everything else is low-poly, with mid-poly exceptions (some ships, items). The environment may become mid-poly later.  
* **Decision.** Stylized, World of Warcraft-like textures on characters and world. The style stays stylized; a move to realism (Crimson Desert level) is not a goal.  
* **Decision.** Reference: Never Be Alone (open-world survival, Early Access on 8 Dec 2026) for proportions and movement, not for its attacks.  
* **Decision.** Immersion comes from the player's integration with the world, not from graphics. Volumetric atmosphere even with simple models.  
* **Decision.** Painted light, only what is true at any hour: crevices and gaps between plates about 10% to 25% darker, convex edges slightly lighter (wear), a cooler tint in occluded areas. Never directional highlights or cast shadows. The headless Blender build bakes AO and curvature masks per asset and blends them into the base color with a strength stored in the recipe, so every variant gets it and runtime cost is zero.  
* **Decision.** The soft "lighter on top" gradient is computed in the master shader from the world-up direction (about 2 operations per pixel), so it stays correct when a character lies down.  
* **Decision.** Weighted normals on hard-surface props; tree canopies get normals transferred from a sphere or blob proxy so leaf clusters shade as one soft volume.  
* **Decision.** Everything moves: vertex wind on grass, leaves, banners and sails; spring bones on capes, hair and belts. All wind visuals read the gameplay wind function, so players read the wind before gliding or setting sails.  
* **Decision.** Density: low-poly geometry pays for grass, props, particles (pollen, dust, leaves) and decals.  
* **Decision.** Two shared master shaders, one for characters and one for the environment, with a custom light function: wrapped diffuse plus rim light.  
* **Decision.** The high-res path stays available but is not planned: a fixed skeleton contract (standard bone names, named sockets), gameplay never reads meshes, materials are parameters on the master shaders, and today's meshes become the far LODs.

## 2. Animation

* **Decision.** One standard skeleton (the Content Pipeline appendix's shared skeleton).  
* **Decision.** Attack feel: short anticipation, overshoot and follow-through, fast through the hit and slower in recovery with the cancel window inside the recovery, client-only hitstop of 2 to 4 frames on impact, weapon trails, a small camera shake and strong sound.  
* **Decision.** Attacks can move the character; the movement happens in the simulation. Clips play in place on the moving capsule. Lunges can be authored with root motion in Blender or Cascadeur; the build step extracts the root curve into the skill's movement data and removes it from the clip, so the feet do not slide. The validation script checks the curve against the skill path, like it checks hit markers.  
* **Decision.** Foot IK, client only: sample the ground under each foot from the terrain heightmap, lower the pelvis by the larger gap, bend each leg with a two-bone solver, tilt the foot to the slope (capped at about 30°), fade in when standing or walking and out when airborne, rolling or attacking (about 0.1 s). Within 30 to 50 m only; well under 0.5 ms per frame for about 50 characters. Hand IK keeps the off hand on spears and greatswords when bone-scaled heights change arm length. Where it runs depends on Architecture v4 open decision 3 (Runic evaluator or Godot's IK nodes, back in Godot 4.6).  
* **Decision.** Edge loops: at least three at elbows and knees, plus density at shoulders, armpits and hips (Content Pipeline appendix). One ring pinches like a kinked hose; three or more fold like a sleeve.  
* **Decision.** Mixamo and other existing animations work on these models: animation drives bones, not polygons. Licensing stays as in the Content Pipeline appendix.

| Tool | What it does | Pipeline step | License or cost |
| :---- | :---- | :---- | :---- |
| MPFB2 | Parametric human bodies | Base bodies | Core assets CC0, code GPL |
| Rigify | Blender's rig generator: friendly controls over the standard deform bones | Animation editing | Free, built in |
| Quaternius UAL 1 and 2 | Humanoid animation library | Main source | CC0 |
| Mixamo | Animation library and auto-rigger | Internal use only | Free; no redistribution in templates |
| Cascadeur | Physics-assisted keyframing: set key poses, it fills the body and fixes momentum and balance | Swings | Free non-commercial; Indie plan from about $8/month (annual) for FBX export |
| Phone video mocap | Raw motion from video | Staff and sword moves | Varies |
| Godot retargeting | Maps any humanoid clip onto the standard skeleton | Import | Built in |

Flow: source clip → retarget to the standard skeleton → polish in Blender or Cascadeur → split into timing phases, add the hit marker, extract root motion → validation script → library.

## 3. Platforms and renderer

* **Decision.** Linux, Windows and macOS. No mobile.  
* **Decision.** Godot's Forward+ rendering method (the full desktop renderer; volumetric fog and SDFGI need it): Direct3D 12 or Vulkan on Windows, Vulkan on Linux, Metal on Apple Silicon with MoltenVK as the fallback on Intel Macs.

## 4. Far rendering

* **Decision.** Render as far as possible with LOD. Fog is never used to limit distance.  
* **Decision.** Terrain3D: a C++ GDExtension (MIT) using geometric clipmaps, as in The Witcher 3, for terrains up to 65.5 × 65.5 km with 10 levels of detail and 32 textures. The 51.2 km map fits. It runs as a Godot node on the client. The server's Jolt heightfield comes from the same cooked heightmap.  
* **Decision.** HLOD proxies per region, built by the cooker after placement: all static props merged into one simplified mesh with one texture (example: 300 objects at 2k triangles, 600k in total, become one mesh of 5k to 20k and one draw call), switched with Godot's visibility ranges. HLOD stays at slice 44+ as in Architecture v4.  
* **Decision.** Trees: mesh LODs up to about 300 m, impostors up to 2 to 3 km, then the forest is baked into the far terrain (canopy color and height written into the far terrain tiles from the flora layer).  
* **Decision.** Impostors: the Octahedral Impostor LOD plugin, for now. It bakes 144 views per object from the editor and switches with visibility ranges. Its license is free for private and commercial use with credit to its author. As an editor tool whose output is cooked, it fits the GDScript rule.  
* **Decision.** Camera-relative rendering (64-bit world positions turned into small floats around the camera) and Godot's reversed-Z depth buffer. A float32 position at 50 km from the camera is still accurate to about 4 mm.  
* **Open.** Confirm in the vertical slice that Terrain3D's LOD rings reach tens of kilometers at the chosen vertex spacing. For reference, a clipmap of 10 to 11 rings reaches about 65 km with 0.3M to 1M triangles.  
* **Open.** If the Engine itself ever ships the impostor plugin, check that its license allows redistribution.

## 5. Atmosphere: haze and fog

### Haze

* **Decision.** Air haze is always on and never zero. Its clear-day minimum is the natural diffusion of light: other continents fade out from a mountain, and the world feels bigger than it is. Elden Ring is the reference: mountain ranges as layered silhouettes, each paler than the one before; ridges and cloud layers hiding parts of distant terrain; a few landmarks visible from everywhere.  
* **Decision.** The haze parameter is visibility (V): the distance where an object's contrast drops to 2% (Koschmieder: extinction = 3.912 / V). V is a slider in the editor, set by eye from the 2,500 m mountain. Weather only lowers it.  
* **Proposal.** Start the clear-day minimum around V = 15 km if another continent is about 20 km away.  
* **Proposal.** Terrain beyond V uses its coarsest LOD; it is still rendered.

| Real-world condition | Visibility |
| :---- | :---- |
| Mountain air after rain | 100+ km |
| Typical clear day | 20 to 40 km |
| Hazy summer day | 5 to 10 km |
| Mist | 1 to 2 km |
| Fog | Under 1 km |

Contrast left at each distance:

| Distance | V = 30 km (crisp) | V = 15 km (scale feel) | V = 8 km (hazy) |
| :---- | :---- | :---- | :---- |
| 1 km | Clear (88%) | Clear (77%) | Slightly washed (61%) |
| 5 km | Clear but bluish (52%) | Washed (27%) | Faint (9%) |
| 10 km | Washed (27%) | Faint silhouette (7%) | Gone |
| 20 km | Faint silhouette (7%) | Gone (0.5%) | Gone |

### Fog

* **Decision.** Fog only represents real fog, with as little performance cost as possible.  
* **Decision.** Three layers that hand over to each other: (1) haze, everywhere; (2) far fog banks, a cheap shader layer like a soft fog deck at the top height of each fog-bank area (a few hundred triangles each), density from node climate, edges drifting with the wind function; (3) near volumetric fog (FogVolumes) within volumetric fog's limited range. As you approach a bank, layer 2 fades out while layer 3 fades in, so the fog creeps in instead of switching on.  
* **Decision.** Fog, sky, wind and color grading come from node climate data. AgX tonemapping, color grading per biome and time of day, blended between nodes and hours.  
* **Open.** Measure the cost of the far fog-bank layer.

## 6. Lighting

* **Decision.** No outdoor lightmaps: they bake one sun position, and 600 km² at one texel per m² is about 600M texels, several GB, for a single time of day.  
* **Decision.** Cook-time bakes that do not depend on the sun, derived from GIMP layers that already exist, like terrain hydrology (table below).  
* **Decision.** Changing a region rebakes it plus a margin of about 10 km: at low sun a 1,000 m ridge throws a shadow nearly 6 km long.  
* **Decision.** Optional GIMP "light" layer for painted overrides (a cursed forest, the sanity region, magical glow), following the marker conventions and feeding both the client bake and the server darkness grid.  
* **Decision.** Real-time sun shadows use Godot's default 100 m. Beyond that, horizon maps (mountains), canopy maps (forests) and AO (creases) take over, with a fade at the edge. Going to 200 m would cover 4× the ground and redraw up to 4× the objects into the shadow map.  
* **Decision.** Global illumination as a graphics setting: High = SDFGI + SSAO, Medium = SSIL + SSAO, Low = SSAO. The bakes are present at every level, so Low still looks right.  
  * SDFGI: builds a coarse 3D shape copy of the static scene around the camera and traces light bounces through it every frame; works with a moving sun and needs no bake; default reach about 205 m; costs a few ms on the GPU, can leak light through thin walls, and only static geometry feeds it.  
  * SSAO: darkens contact areas and creases using only what is on screen. Cheap.  
  * SSIL: the same idea, adding bounced color from nearby on-screen pixels. Cheap, but blind to light off screen.  
* **Open.** Which GI level is the default, after testing, including on Apple Silicon.  
* **Open.** Shadows when gliding or flying above about 100 m (the ground is then beyond the shadow distance; forests still look right through the canopy bake) and large landmarks at mid-distance. Check once flight exists; options are a larger distance while airborne or a High quality option.

| Bake | Input | What it gives | Size and time (approx.) |
| :---- | :---- | :---- | :---- |
| Terrain horizon map | Elevation | Mountain and valley shadows at any sun angle and any distance | 8 directions at 16 m: about 19 MB for 600 km² of land (the ocean needs none); under a minute for the whole map on an 8-core CPU, about 1 s per region |
| Sky visibility | Horizon map | Darker ambient light in valleys and canyons | Derived, nearly free |
| Canopy occlusion | Flora layer and tree placement | Dark forest floor, near and far | About 4 m, a terrain texture channel |
| Server darkness grid | Sky visibility and canopy | Darkness input for the server's visibility range (dense forests are darker) | 32 m grid, about 2.6 MB for the whole map |
| Per-asset AO and curvature | Each model | The painted-light cues | Headless Blender build |
| Interior lightmaps | Dungeons, caves, the Underground | Full baked light where lights never move | Once per prefab in Godot (GPU). House interiors with windows get baked AO plus real-time sun |

## 7. Entity visibility

* **Decision.** The client only knows what the player knows. The server never sends an entity the player cannot see.  
* **Decision.** Range = class range × ambient light × target emission × weather, clamped between about 1 m and 1 km. Ambient light comes from the time of day, weather, node, the Underground and the server darkness grid. Target emission counts: lanterns, torches and fires make a target visible further, so sailing dark is possible. Complete darkness and blindness status effects bring it to about 1 m: the character and the space around it.  
* **Decision.** Height has no effect on vision or on the range.  
* **Decision.** The range is computed at simulation rate. Hysteresis: an entity enters at range R and leaves only beyond R + 10%, so a player walking along the edge, or a flickering torch changing R by 2% to 3%, does not make entities blink in and out (each re-entry would cost a creation packet of about 100 to 300 bytes).  
* **Decision.** Effects and projectiles are judged by their own position and light, never by the caster's: a fireball or flaming arrow is visible when the shooter is not; a plain arrow in darkness is not; a glowing ground telegraph is.  
* **Decision.** Unknown attackers: no telegraph fast-forward and no defender grace; the hit resolves on the server. Hitting an unknown target gives no predicted impact; the confirmation arrives after one round trip (about 50 to 150 ms).  
* **Decision.** When blindness ends, entities appear with a fade of about 0.3 s, which reads as eyes adjusting. A one-time burst of about 50 entities × 200 B ≈ 10 KB.  
* **Proposal.** Recheck membership at 5 to 10 Hz instead of every simulation tick; entities only cross the range far from the player.

### Silhouettes of unknown entities

* **Decision.** Every interaction with an unknown entity (it hits you, or you hit it) sends an anonymous event: position, facing and size class, about 12 bytes. The client draws a generic silhouette for that size class (humanoid, large creature, ship), so gear never reveals identity.  
* **Decision.** The position is where the attack came from: the release point for ranged attacks, the attacker's position for melee.  
* **Decision.** Silhouettes stay on screen, frozen in place, for each unknown entity interacted with. Because honest clients keep them, a cheat gains nothing by keeping them.  
* **Decision.** Color by relation: red = enemy, white = neutral, green = ally, blue = party.  
* **Decision.** Damage over time and auras do not create a silhouette on every tick: one per direct hit, or one per attacker every few seconds, so a poison never becomes a tracking beacon.  
* **Proposal.** One silhouette per unknown entity: a newer interaction moves it, using a random handle scoped to the viewer (never the real ID). It is removed when the entity becomes visible, when combat ends (30 s after the last hostile action) or above a cap of about 20.  
* **Proposal.** The server decides the color at the moment of the interaction, from the viewer's side: an Outlaw of your own faction who attacks you is red; players in PvE mode count as allies; aggressive mobs are red and passive mobs white; party blue overrides ally green.  
* **Proposal.** A color-blind option with a second cue (outline style or icon) besides color.  
* **Future idea.** The same anonymous-event channel can carry sound cues in the dark (footsteps, casting).

### Costs and effort (approx.)

| Piece | CPU (1,000 players, 30 Hz) | Effort |
| :---- | :---- | :---- |
| Range per observer (about 50 ns) | About 1.5 ms per second (0.15% of a core) | 2 to 4 days with the server ambient-light model |
| Membership, about 100 candidates each (about 3 ns per pair) | About 1% of a core at 30 Hz; 0.15% to 0.3% at 5 to 10 Hz | 2 to 5 days with hysteresis |
| Silhouette events | Negligible | 3 to 5 days (rough) |

## 8. NPCs in distant cities and ports

* **Decision.** Distant cities and ports show their NPCs. The routine is a function of seed and time, so the client computes the same positions as the server without network traffic. Inside 1 km the real entities replace them with a short fade; a mismatch at 1 km is under 2 pixels.  
* **Decision.** No split into kinds of NPCs.

## 9. Future idea: far entity tier (for Ideias)

After the vertical slice; very low priority.

* Anonymous proxies beyond 1 km: class, position (about 1 m), heading and flags, about 8 to 10 bytes each at 1 Hz; about 1 KB/s per player for 100 proxies. Never an ID, name or gear.  
* Ranges per class from screen size (1080p, 60° vertical field of view): a player is 1.7 px at 1 km; a ship with a 30 m mast is 5.6 px at 5 km, 2.8 px at 10 km and 1.4 px at 20 km; a 200 m smoke column or beam is 37 px at 5 km and 3.7 px at 50 km. So players up to about 2 km, ships up to about 20 to 30 km.  
* Occlusion from baked horizon profiles: 256 m cells (40,000 for the map), 64 directions, 6 distance rings, 30 to 50 MB, about a minute to bake; a test is 20 to 50 ns. Biased toward visible, because the client's renderer hides what is behind a hill anyway. Height bands would model occlusion only, since height has no effect on range.  
* Recomputed only when something changes cell (256 m), not every second: about 1 to 2 ms of CPU per second (0.1% to 0.2% of a core) instead of about half a core with per-pair ray marching.  
* One far-view service per world: input about 40 KB/s for 5,000 far-visible entities, output 0.5 to 1 KB/s per player.  
* Extras: a channel for landmark event visuals; far proxies for scheduled NPC traffic from the routine service; a spyglass that raises class ranges; an optional horizon check inside 1 km (about 1% to 3% of a core at 5 Hz).  
* References: Valorant's fog of war (server withholds positions; precomputed visibility), DayZ's network bubble (20 m, 150 m, 1,000 m and 4,000 m for distant sounds, despawn at +10%), WoW's server visibility by size class (about 100 yards on continents), PlanetSide 2 (about 1,000 m, infantry culled before vehicles) and Sea of Thieves as the warning (ships replicated far, so ESP tools show every ship).  
* Effort: about 3 to 5 weeks (far-view service 1 to 2 weeks, client proxies about 1 week, horizon bake and server test 1 to 2 weeks, event visuals 1 to 3 days).

## Dropped

* Fog as a render-distance limit.  
* A network floor that sends attackers the player cannot see (replaced by silhouettes).  
* Height raising the visibility range.  
* Real-time sun shadows at 200 to 400 m as the default.  
* Splitting NPCs into ambient, interactive and gameplay kinds.  
* The far entity tier in the current plan (moved to Future idea).

## Requirements by repository

### Engine

* Interest management: visibility range function with ambient light, emission and weather, the 1 m to 1 km clamp, hysteresis, and anonymous silhouette events with a viewer-scoped handle.  
* Combat netcode: telegraph fast-forward, defender grace and predicted impacts limited to known entities.  
* Cooker: horizon map, sky visibility, canopy occlusion, server darkness grid, HLOD proxies, far-terrain canopy, interior lightmaps, rebake of a region plus margin.  
* Terrain3D integration as a client runtime node; cooked heightmap for Jolt on the server.  
* Impostor plugin in the editor, output cooked.  
* Haze, far fog banks and near volumetric fog driven by environment data; the V slider in the editor; GI quality levels; master shader support.  
* Animation: foot and hand IK; root-motion extraction in the Blender build tool.

### Game

* Node climate values: haze V per weather, fog banks, wind, color grading.  
* Master shaders, painted-light strengths per recipe, environment polygon budgets.  
* Class ranges, emission values, silhouette colors and rules, skill movement curves.  
* Optional GIMP light layer.

### Platform

* Nothing new. The far-view service would belong here if the future idea is built.

## Open

* Default GI level, after testing, including on Apple Silicon.  
* The clear-day haze value and its weather values, set with the slider.  
* Terrain3D's far reach at the chosen vertex spacing.  
* Shadows while gliding or flying, and mid-distance landmarks.  
* Silhouette lifetime, cap and color edge cases (proposals above).  
* Environment polygon budgets.  
* Where IK runs (Architecture v4 open decision 3).  
* Cost of the far fog-bank layer.  
* Impostor plugin license if the Engine ships it.

## Sources

* [Never Be Alone on Steam](https://store.steampowered.com/app/3012110/)  
* [Godot docs: Volumetric fog and fog volumes](https://docs.godotengine.org/en/4.5/tutorials/3d/volumetric_fog.html)  
* [Godot docs: Internal rendering architecture](https://docs.godotengine.org/en/latest/engine_details/architecture/internal_rendering_architecture.html)  
* [CG Channel: Godot 4.6 features](https://www.cgchannel.com/2026/01/discover-5-key-features-for-cg-artists-in-godot-4-6/)  
* [Terrain3D](https://github.com/TokisanGames/Terrain3D)  
* [Godot Asset Library: Octahedral Impostor LOD](https://godotengine.org/asset-library/asset/5528)  
* [MakeHuman and MPFB license](https://static.makehumancommunity.org/about/license.html)  
* [Cinevva: Mixamo and alternatives (2026)](https://app.cinevva.com/guides/free-character-animations-rigging)  
* [Cascadeur pricing](https://www.rfp.wiki/design-multimedia/media-entertainment/3d-animation-vfx-software/cascadeur/cinema-4d)  
* [Riot: Demolishing wallhacks with VALORANT's fog of war](https://technology.riotgames.com/node/108)  
* [DayZ network bubble settings](https://feedback.bistudio.com/T185319)  
* [TrinityCore visibility distances](https://trinitycore.net/df/d14/objectdefines_8h_source)  
* [PlanetSide 2 render distance discussion](https://steamcommunity.com/app/218230/discussions/0/350540973994102404)  
* [Sea of Thieves ESP framework](https://gh.r-mj.com/DougTheDruid/SoT-ESP-Framework)  
* [Ten Ton Hammer: Black Desert pop-in](https://www.tentonhammer.com/columns/black-desert-online-why-is-the-pop-in-so-bad)
