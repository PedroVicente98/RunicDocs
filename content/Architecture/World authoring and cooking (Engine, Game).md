---
title: "World authoring and cooking (Engine, Game)"
tags:
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-13"
---

The world is assembled in the RunicEditor (Godot) as one low-detail world scene plus detailed region scenes, Blender makes the assets, and the Cooker turns those scenes into Runic-native server and client packages; the shipping client and server never read an editor scene or a Blender file.

### Ownership

| Part | Owner | Contains |
| :---- | :---- | :---- |
| RunicEditor world tools (GodotTools) | Engine (tool) | World and region scenes, RunicRegion3D proxies, New region from layout, neighbor proxies, marker nodes, validation, the “see what the server sees” layer, cook launch |
| Cooker | Engine (tool) | Orchestration, Runic format writers, collision, nav and water cooking, incremental builds, validation |
| Runtime formats | Engine | World manifest, region headers, cell files, packages, collision, nav tiles, water fragments, spawn areas |
| Godot import and export | Godot, configured by Engine presets | Imported meshes, textures and materials; the client .pck |
| Blender export helper | Engine (optional tool) | Collision and LOD naming conventions and glTF export presets |
| World content | Game | World.tscn, region scenes, terrain, shared assets, marker nodes, spawn rules, water and wind maps, metadata values |
| Platform | Platform | Nothing in authoring or cooking |

### Godot and Blender

Blender makes assets; Godot assembles the world. The border is glTF (plus the terrain heightmap): nothing from a .blend reaches Godot or the Cooker, Blender never knows a game rule, and Godot never edits a mesh.

| Task | Where | Leaves as |
| :---- | :---- | :---- |
| Modeling rocks, buildings, props, weapons and characters | Blender | glTF |
| UVs and texture baking (normals, occlusion) | Blender or a texturing tool | Textures |
| Simplified collision meshes and hand-made LODs | Blender | glTF, with the naming convention |
| Rigs, skinning and animations | Blender | glTF with its clips |
| Large-scale terrain sculpting | Blender or a terrain tool | Heightmap (.exr) and masks |
| Asset import: default collision, LOD, compression | Godot | Import settings |
| Final materials and shaders | Godot | The project’s materials and shaders |
| World layout: regions, each region’s origin, asset placement | Godot | World and region scenes (.tscn) |
| Runic markers: spawn areas, volumes, interactables, routes, colliders | Godot | Marker nodes |
| Water: rivers, lakes, ocean | Godot | RunicWaterBody3D (rivers on Path3D) |
| Decorative vegetation and scattering | Godot, through tools | MultiMesh; interactive resources spawn by rule |
| Terrain painting and fine shaping | Godot, through a Runic tool or plugin | Terrain layers |
| Lighting, sky, environment and post-processing | Godot | Environment resources |
| Player UI | Godot | UI scenes |
| Data: skills, items, AI, quests, spawn rules | Godot, through schema inspectors | Runic data files |
| Cooking and export | Godot (RunicEditor) | Server and client packages |

* **One path:** meshes and animation enter through glTF; when an asset is re-exported, Godot re-imports it and updates the scenes that use it.

* **Units and axes:** meters and scale 1\. glTF is Y-up; Blender’s exporter converts from Blender’s Z-up, and Godot is already Y-up.

* **Identity:** an asset gets a stable UID in Godot, and the Cooker maps that UID to the Runic AssetId.

* **Collision:** the naming convention is decided once and documented in the project template, so the artist in Blender and the importer in Godot speak the same language.

### World scene and region scenes

The v3 model stays: one low-detail map with the layout and one file per region with the detail, together one world. In Godot both levels are scenes.

* **World.tscn** is the master plan (the old WorldLayout.blend): region boundaries, low-resolution macro terrain, major routes, large rivers and landmarks. Each region appears in it as a RunicRegion3D node that shows only a lightweight proxy of the region; a double click opens the detailed scene.

* **Regions/Greenvale.tscn** is the region with all its detail, edited near its local origin. Its root is a RunicRegion node with the RegionId, the boundary polygon and the global origin.

* **Neighbors and borders:** while a region is edited, its neighbors show as read-only proxies, placed by the difference between origins (computed in double and only then converted), with an overlap band on the border to match terrain and assets.

* **New region from layout** is v3’s “Create Region From Layout”: from a boundary drawn in World.tscn it creates the region scene with its origin, the cut of the macro terrain and the neighbor references. It is a one-time step; afterwards the region owns its detail.

* **64-bit origins:** Godot’s Vector3 is float32 and, 712 km from the origin, moves in 6.25 cm steps. A region origin is stored as three float properties (which Godot keeps as doubles) or as 64-bit integer centimeters, never as a Vector3.

```cpp
// Illustrative: in World.tscn
class RunicRegion3D : public godot::Node3D {
    GDCLASS(RunicRegion3D, godot::Node3D)
    godot::String regionScene;                    // "uid://…" of the detailed scene; never loaded here
    double originX = 0, originY = 0, originZ = 0; // global origin in double
    godot::Ref<godot::Mesh> proxy;                // lightweight version, rebuilt when the region is saved
};
```

**Gameplay regions are not terrain tiles.** A designer-facing region can have any polygon that follows geography, politics, biome or content, while terrain and streaming subdivisions stay a regular grid.

### Large worlds in the editor

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

* **The Cooker never loads everything either:** it cooks region by region (open, write cells, unload) and re-cooks only changed cells, so its memory is one region plus its neighbors’ borders.

* **Larger worlds:** at 1,000 km² or more the model is the same; only the proxies grow, and the world scene can use coarser proxies or split by continent.

### Seamless terrain and borders

* **One continuous terrain truth.** Region terrain derives from one canonical continuous source or canonical shared edge samples; neighboring artists never invent the same border twice.

* **Canonical sample grid.** For large natural terrain, canonical height samples are the truth rather than one arbitrary mesh. Regions own ranges of the global grid and share border samples exactly: if region A covers X 0 to 1024 and region B covers 1024 to 2048, both read the same sample at X \= 1024\. Artists sculpt in Blender or a terrain tool; import samples the result into the grid.

* **Aprons.** Each region and cell cooks slightly past its official boundary so derived data sees neighbor context; a border that matches positions but not normals, masks or LODs still shows a seam.

Aprons keep these continuous across a boundary:

* Geometry and height.

* Normals and tangents.

* Terrain material and biome masks.

* River and road splines.

* LOD and HLOD edges.

* Collision.

* Navmesh boundaries.

* Vegetation distribution, wetness and shoreline masks.

* Lighting and probe data where relevant.

**Region borders are technically boring:** crossing one never implies a terrain, renderer, physics or navmesh seam, a server boundary or a loading screen. Streaming and ownership are separate concerns.

### Marker nodes and what they cook into

Runic marker nodes exist only in the editor: RunicSpawnArea3D, RunicVolume3D, RunicInteractable3D, RunicWaterBody3D, RunicRoute3D and RunicCollider3D. Cooking turns them into placements and volumes, and on load the Engine creates Flecs entities by its own rules. The game adds its own marker types through its editor library.

| In the editor | The server receives | The client receives |
| :---- | :---- | :---- |
| Scenery mesh (rock, building) | Cooked Jolt collision | Mesh ID and transform per cell; the same collision near the player, for prediction |
| Terrain | Jolt heightfield | Terrain mesh and materials; the heightfield near the player |
| RunicSpawnArea3D (trees, crops, ores, mobs) | The area, its rule and candidate points | Nothing fixed; each spawned entity arrives replicated |
| RunicVolume3D (cave, PvP zone, flight zone) | AuthoredVolume | Only if it has a visible effect, such as fog |
| RunicInteractable3D (door, chest) | A placement that becomes a Flecs entity and a kinematic body | The visual; its state arrives replicated |
| Rivers and water bodies | Water fragments and flow fields | The water surface |
| (derived from collision) | Recast nav tiles | Nothing |
| Textures, materials, shaders | Nothing | Godot’s .pck |

Collision goes to both sides: the server needs it for authority and the client, near the player, for prediction. Both copies are the same Cooker output, in Runic’s Jolt in 64-bit, which is why prediction agrees with the server.

**How collision is marked:**

1. **Asset default:** in Godot’s import settings, each mesh says which collision it generates: the mesh itself, a convex hull, a simplified mesh or none.

2. **Collision mesh in the glTF:** the artist models the simple version and exports it alongside, under the naming convention.

3. **RunicCollider3D:** a box, sphere, capsule or convex shape placed in the map for invisible walls, stairs and similar cases. The colliders are Runic’s because Godot’s physics is not in the build.

**Why server and client agree:**

* **Same ID:** every cooked thing has a stable ID (cell plus placement), so “door 4812 opened” names the same object on both sides.

* **Same coordinates:** the editor saves the local position in float, near the region origin; the Cooker writes the global one in double, region origin plus local.

* **Same version:** each cell carries a hash and the world a build ID. On connect the server states its build; a client with another one updates before entering. In development both read the same output folder.

### Resources by spawn area (decided)

Interactive resources (trees that can be cut or harvested, crops such as potatoes and carrots, ores, herbs) are never placed one by one. They spawn by rules inside spawn areas; the map only says where they may appear. Decorative vegetation stays in MultiMesh with no entity.

| Stage | What happens |
| :---- | :---- |
| Authoring | A RunicSpawnArea3D (volume, polygon or painted mask) points at a rule in Data/, such as game:greenvale\_apples |
| Rule | A schema-backed file that says what, how many, when and where inside the area; complexity grows by levels |
| Cooking | The server receives the area and a list of valid candidate points (on the ground, acceptable slope, clear of rocks, reachable); the client receives nothing |
| Runtime | In the maintenance phase the spawn system evaluates the rules of active areas, picks points and queues commands; each resource becomes a Flecs entity with a static Jolt body |
| Replication | A resource reaches a client when it enters interest (about 20 bytes) and then only on state changes; 300 resources in view cost about 6 KB once |

* **Simple rules:** maximum alive, respawn time, minimum spacing.

* **Weighted rules:** weights by altitude, slope, surface, biome, season and time of day (from the Environment).

* **Complex rules:** a C++ behavior the Game registers (world events, depletion and migration, player activity), on the v3 custom-behavior model.

id: game:greenvale\_apples  
spawns: game:apple\_tree  
max\_alive: 40              \# per area  
respawn\_s: 900  
respawn\_at: new\_point      \# or same\_point: regrows in place  
placement:  
  min\_spacing\_m: 6  
  max\_slope\_deg: 25  
  surface: \[grass, dirt\]  
weights:                   \# optional  
  altitude\_m: { 0-300: 1.0, 300-600: 0.4 }  
  season:     { summer: 1.0, winter: 0.0 }  
custom: game:orchard\_event\_boost   \# optional

```yaml
id: game:apple_tree
kind: resource_node
states:
  full:   { visual: { mesh: game:apple_tree, show: [trunk, leaves, apples] }, collision: trunk }
  picked: { visual: { mesh: game:apple_tree, show: [trunk, leaves] },         collision: trunk }
  stump:  { visual: { mesh: game:apple_tree_stump },                           collision: stump }
interactions:
  pick: { from: full, to: picked, yields: { game:apple: 3-5 }, regrow_s: 600 }
  chop: { from: [full, picked], to: stump, requires: game:axe, yields: { game:wood: 4 }, regrow_s: 3600 }
```

* **No simulation of empty areas:** only areas in active cells spawn. When a cell loads, the area fills up to the count its rule expects for the time since the last visit, seeded, instead of having been simulated meanwhile: the same principle as world routines.

* **Engine and Game:** the Engine provides the volume, candidate sampling at cook time, the spawn API and rule primitives (engine:); the Game writes the rules and registers its own conditions (game:).

* **Persistence:** a common resource is ephemeral; after a restart the area refills by its rule. A rare resource that must survive restarts uses the durable path of the services.

* **States and visuals:** the resource definition maps each state to its visual and its collision; the asset comes from Blender with its states as parts or separate meshes. Falling when chopped is a client presentation cue; the server only records the state change.

* **In the editor:** the area previews its candidate points and expected density so the designer can adjust before running.

### Housing zones and basements

The rules are in the Vision: [[Economy, housing and land]] › Houses and Basements.

* **The tray:**
  * A housing zone is authored on the 8x8 slot grid.
  * The cook cuts a hole in the terrain heightfield under each zone, with the hole masks terrain sources already carry.
  * A cooked tray takes its place: a bottom at the deepest basement level, retaining edges, and one sheltered volume over the whole hollow. Like a cave volume, it has no wind or weather, and light comes only from emitters.
  * The cook rejects a zone whose tray meets a cave, rock, water body or Underground cell.
* **The cells:** the hollow is a grid of cells, 4x4 m wide and 3.5 m high per level.
* **The lids:** over each cell sits a 4x4 m lid, and the lids are the zone's ground.
  * Over earth, a lid is ordinary ground in the zone's material, so an empty plot looks like terrain.
  * Over a dug cell, the lid is the basement's ceiling and the floor of whatever is above.
* **The building grid:** the 4 m module is the plot's grid, and house designs snap to it. Sloped zones are built as terraces with retaining walls.
* **The tray's depth:** it is the basement's vertical limit, so that limit has to be set before housing zones are cooked.
* **Engine and Game:**
  * Hole masks, sheltered volumes and runtime building pieces with collision are generic Engine mechanisms.
  * The housing zone, the cell size and every housing rule are Game.
  * No runtime terrain edit and no runtime volume are needed.

### Interchange: glTF and terrain sources

glTF 2.0 and GLB are the mesh and scene interchange from Blender, imported by Godot. glTF is a source format, never the runtime world representation, and the Cooker reads geometry from the scenes Godot imported instead of running a second importer.

```text
.blend -> .glb/.gltf + terrain sources -> Godot import -> scenes in the RunicEditor -> Cooker -> Runic packages
                                                                                    -> Godot export -> client .pck
```

Large terrain is never forced into one glTF triangle mesh. Heightfield-like land uses a terrain source (for example a high-precision height.exr plus biome, material and hole or cave masks), while cliffs, caves, arches, overhangs, buildings, ruins, bridges and floating islands stay general meshes.

### Cooker

The Cooker is Runic code: the orchestration layer and native-format writer. It runs inside the RunicEditor from an export plugin, and build machines run the same RunicEditor without a window.

| Pipeline stage | Technology | Where it runs |
| :---- | :---- | :---- |
| Asset modeling | Blender | External application |
| Interchange | glTF 2.0 and GLB | Source data |
| Import, textures, LODs and materials | Godot importers | RunicEditor |
| World assembly and markers | RunicEditor (GodotTools) | Editor |
| Collision cooking and runtime | Jolt Physics | Cooker, client and server |
| Collision simplification | meshoptimizer | Cooker |
| Navmesh cooking | Recast | Cooker |
| Navigation runtime | Detour and DetourTileCache | GameServer |
| Package compression | Zstandard | Cooker, plus runtime decompression |
| Client visual package | Godot export (.pck) | RunicEditor |
| Rendering | Godot (libgodot, template target) | GameClient |
| Gameplay and world ECS | Flecs | Runtime |

| Executable | Links |
| :---- | :---- |
| GameClient | libgodot (template), godot-cpp, Jolt (for prediction and local collision), Flecs, Zstandard, Engine runtime |
| GameServer | Jolt, Flecs, Detour, Zstandard, Engine runtime |
| RunicEditor | libgodot (editor), godot-cpp, the Cooker (Jolt cooking, Recast, meshoptimizer, Zstandard, Runic writers), Engine runtime |

**One authored truth, many runtime products.** From one castle, terrain patch or region the Cooker emits Jolt collision shapes, Recast and Detour nav tiles, terrain cells and masks, world placements and metadata, water fragments and flow fields, spawn areas with candidate points, server-only gameplay and spatial data and client cell visual lists; Godot’s export emits the textures, meshes and materials. The runtime never needs to understand an editor scene.

### Cooked world files and packages

No scene survives cooking. The Cooker reads World.tscn and each region scene and writes the Runic format; at runtime there is no scene, only the manifest and the cells.

| In authoring (Godot) | Becomes when cooked | Who uses it at runtime |
| :---- | :---- | :---- |
| World.tscn | MainWorld.runicworld: region registry (ID, global origin, bounds, neighbors), global ocean and environment, package index | Server and client, at load |
| Regions/Greenvale.tscn | Greenvale/region.header plus 3D cells of 64 m, each as .server and .client | The server loads cells near players; the client near the camera |
| Meshes placed in the region | Visual list per cell (AssetId and transform relative to the cell); Jolt collision in the server cell | The presenter creates instances in the RenderingServer; server and prediction use the collision |
| Marker nodes | Placements, volumes, spawn areas, routes, water and nav tiles in the server cells | The server creates Flecs entities when the cell loads |
| Meshes, textures and materials in Content/ | The client .pck | Godot inside the client |

The region is the unit of authoring and organization; the cell is the unit of loading; and who owns each part of the world at runtime is decided by the v3 authority partition, never by the file. Every global position is the region origin (double) plus the position the editor saved, and inside a cell it is relative to the cell origin, small and precise in float again.

```text
MainWorld.runicworld
  WorldId and instance policy
  coordinate system and global-origin policy
  world bounds
  volume registry (caves, rule areas, indivisible volumes)
  continent registry
  region registry
  global ocean and environment references
  world transition and portal policies
  package and dependency indices
```

A logical region becomes a header, cells, terrain pages, collision pages, nav tiles and spawn areas, either as loose entries or packed into one .runicpak with an internal random-access table of contents. A continent is never compressed as one sequential stream; packages always allow independent random access so cells can stream.

| Client cook | Server cook |
| :---- | :---- |
| Cell visual lists (AssetId, transform, LOD and proxy references) | Jolt collision data |
| The .pck from Godot’s export: meshes, textures, materials, UI, audio | Detour navigation tiles |
| Client-safe data definitions | Spawn areas, placements and spatial metadata |
| Client water render data | Region rules and server world objects |
| Collision near the player for prediction | Server water fragments and flow representation |

**Incremental cooking and the editor loop.** The Cooker tracks dependencies: moving one rock in Greenvale re-cooks only the cells it touches and their seam-dependent neighbors, and never unrelated continents. In development: you move a rock and save; the Cooker re-cooks its cells in seconds; the local server reloads those cells at a safe point (unload and load, like streaming); the client reloads their visuals. The “see what the server sees” layer draws the cooked collision, volumes, spawn points and nav tiles over the viewport, so a rock that looks solid without collision shows up before the game runs. For a live preview of water or AI in the viewport, the editor can run a local headless Runic simulation; that is still Runic code, not Godot.

### Authoring work per roadmap slice

The pipeline grows inside the vertical-slice roadmap; gameplay never stops for a long “build the whole editor and cooker” phase.

| Roadmap slice | World and asset work |
| :---- | :---- |
| 0\. Build skeleton | libgodot in both targets; the RunicEditor spike; Cooker target and module boundaries; no production cooking yet |
| 6\. Editor shell | The RunicEditor opens the RunicGame project; project template and layout |
| 9\. First cooker proof | Blender to GLB, imported by Godot, collision cooked by the Runic Cooker; walk on it |
| 13\. Replication | The Run button feeds the client and the headless server the same cooked data |
| 15–19. Combat | Only the collision and metadata real combat obstacles and queries need |
| 20\. Data-driven content | Runic data files in the editor through schemas, stable asset IDs, live reload |
| 21\. World partitions | Major milestone: World.tscn and region scenes, marker nodes, region, sector, 3D cell, volume and spawn-area cooking, activation-volume streaming, Jolt cell collision, manifests, the server view layer; GDScript enabled for editor tools |
| 22\. World rendering | Godot import settings and the client .pck export |
| 23\. Animated characters | Skinned meshes and clips imported by Godot |
| 25\. Interest | Network relevance uses the same spatial vocabulary without coupling replication to presentation |
| 28–30. Persistence, sequences and quests | Persistent world-object IDs and authored gameplay markers in cooked regions |
| 31\. Navigation and spawning | Recast cooking, Detour runtime, spawn-area candidate points checked against the navmesh |
| 36\. Multiple simulations | Packages stay unchanged while different simulations own adjacent space and players transfer |
| 40–43. Water and environment | Water bodies, river curves, current and wind maps authored in the editor |
| 44+. Production world | HLOD, advanced terrain materials, light baking and probes, incremental cooking at scale, large-world validation, plugin compatibility |

**First cooker proof:** test\_region.glb imported by Godot into a test scene, its collision cooked into test.jolt and its placement into a test cell; the client draws the mesh through Godot, client and server collision work, and a character walks on it. Recast, HLOD, terrain splatmaps, world manifests, spawn areas, compression and region tools all wait until after this proof — complexity is earned one slice at a time.

**Graphics quality grows independently.** The full MMO architecture can run on programmer art and Godot’s default materials. Textured meshes, PBR materials, shadows, terrain shaders, sky, fog and water rendering, vegetation, baked lighting, post-processing and polish mature without redesigning the world-file architecture: the pipeline provides data, Godot decides final quality.

### Project layout and schemas

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
    SkyWorld/World.tscn             the sky world’s scene (a separate WorldId)
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

The Cooker derives the automatic sectors and cells and the runtime package dependencies.

**Contract:** one logical world is authored in the RunicEditor as a low-detail world scene plus detailed region scenes; Blender makes assets and glTF is the border. Region is an authored concept; sector and cell are automatic runtime structures; simulation ownership is separate. Terrain borders derive from canonical shared data and cook with neighbor aprons. Artists work in region-local coordinates with 64-bit global origins and read-only neighbor proxies. The Cooker reads the scenes and emits Runic-native server and client packages, and Godot’s export emits the client .pck; no scene survives cooking. The world is indexed by sparse 3D cells and authored volumes; activation volumes around players decide what loads and simulates, and separate maps are separate worlds.
