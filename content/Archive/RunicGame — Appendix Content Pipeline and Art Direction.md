---
title: "RunicGame — Appendix: Content Pipeline and Art Direction"
tags:
  - "archive"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
created: "2026-10-26"
modified: "2026-10-30"
---

Design appendix from the conversation of 26 October 2026 about art direction and the content pipeline, to be merged later into the game vision and the technical architecture. It was compared with the Drive versions of [RunicGame — Visão Completa do MMORPG](https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit) (13 Oct), [RunicGame — Ideias](https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit) (25 Oct) and [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) (14 Oct).

In short: RunicGame keeps World of Warcraft's identity (color, readable shapes, armor design) on bodies with near-real proportions like Black Desert's, so weapon swings can be animated in detail, at a fidelity between World of Warcraft and ArcheAge. Crimson Desert's fidelity is out of scope, because it is a single-player budget. Content comes from a small set of human-made base models that scripts and recipes turn into many variants, so one or two developers can produce a vertical slice.

The first sections list the differences from those documents. The rest describes each part, and the requirements at the end are split by repository: Engine, Game and Platform. Every item is labeled Decision (stated in the conversation), Proposal (recommended, not yet accepted), Open or Dropped. Numbers are planning estimates; budgets are confirmed by measuring in Godot.

## Differences from the Vision

| **Vision section** | **What the Vision says today** | **What this appendix changes** |
| :---- | :---- | :---- |
| Lançamento, monetização, visuais e áudio › Visuais | Mount and pet collection, account-wide transmog wardrobe, weapon appearances per weapon type, exclusive cosmetics from dungeons and raids. No art direction | Adds an art direction (see Art direction). Transmog and weapon appearances are produced as variants of shared base models, and textures carry dye masks from the start (Proposal) |
| Raças | Three races with heritage visuals: cultural armor, mount and glider | All playable races share one skeleton and one hurtbox, so every animation works on every race (Proposal). Heritage armor is a variant set built on the shared armor bases |
| Defesa: Evasão, Guard e armaduras › Armaduras | Cloth, leather and plate change the iframe and the Guard | The same three classes are the three armor bases of the pipeline, one per body type (Decision). No armor stops the arm from going above the head (Proposal) |
| Skills por componentes › Atributos ocultos, públicos e perfis de tempo | Startup, active, recovery and cancel window in combat ticks (30 Hz); one timing profile per weapon and grip | Swing animations are authored in the same phases, and the pipeline checks each clip against its weapon's timing profile (Proposal) |
| O que a engine e a plataforma precisam suportar | No row for art or content production | Add a row for the content pipeline (see Requirements by repository) |

## Differences from Technical Architecture v4

| **Architecture section** | **What the Architecture says today** | **What this appendix changes** |
| :---- | :---- | :---- |
| World authoring and cooking › Godot and Blender | Blender makes assets and glTF is the border. Godot imports textures, LODs and materials; final materials and shaders live in Godot | Unchanged. Added on the Blender side: recipes, headless batch builds and a validation script that runs before the glTF export (Proposal) |
| World authoring and cooking › Ownership: Blender export helper | Optional Engine tool for collision and LOD naming conventions and glTF export presets | Grows into the build pipeline: recipe runner, attachment-point naming, budget validation and hit-marker export (Proposal). It stays game-agnostic; budgets and recipes are project data |
| Resources by spawn area › apple_tree example | Each state shows or hides parts of one mesh (show: [trunk, leaves, apples]) | Each state points at its own pre-merged mesh, built by the pipeline from the modular parts, so a tree draws as one mesh instead of three or four (Proposal) |
| Decorative vegetation; presenter (GDB-5) | Decorative vegetation in MultiMesh; repeated static meshes of a cell in one MultiMesh | Unchanged, plus per-instance color and texture-layer data for species variants, and impostors for distant trees (Proposal). HLOD stays at slice 44+ |
| Godot integration › Open decisions, item 3 (client animation) | (A) the Runic evaluator with poses sent to RenderingServer skeletons, or (B) Godot's AnimationTree driven by the animation intent | Not decided here. The crowd budget below needs update rates per distance and twist bones computed in code. Both are direct in option A and need checking in option B |
| Render data › Debug layers first, the Godot look later | Production look (GDB-13) from slice 44 | The proposed texture approach works with Godot's standard PBR material, so assets made before GDB-13 need no rework. Weather and biome shader layers wait for GDB-13 |
| Principles and performance targets › Targets | 100 vs 100 must feel perfect; 500 players in one region must still work | Character budgets below are derived from these targets |
| Client runtime › Animation | The server never evaluates animation; gameplay timing comes from ability timelines | Unchanged. The pipeline exports each clip's hit marker and checks it against the timeline (Proposal) |

## Related entries in Ideias

* GFX-01, Visual Style and Character Creation (Open): its next step was to study the graphics of other MMOs. This appendix records that study and the resulting target.
* RACE-02, Race Archetypes and Size (Open): its proposal of one hurtbox capsule and a narrow visual height band fits the shared skeleton proposed here.
* EQUIP-01, Equipment Slots (Open): the cloak and the back slot (glider or wing) need bone chains in the rig, and profession gear needs its own attachment points.
* DISC-02, Discipline Skills Follow the Weapon (Open): Discipline skills reuse the weapon's animations by default, which keeps the animation count per weapon low.

## Art direction

### Target

* **Decision.** The quality target is a mix of World of Warcraft and ArcheAge, or better than ArcheAge where the budget allows. Crimson Desert's fidelity is not a target: it draws one hero, while RunicGame must draw 100 against 100.
* **Decision.** World of Warcraft's problem for RunicGame is its character models, not its art style: their proportions do not allow detailed weapon swings. RunicGame wants models closer to Black Desert's.
* **Proposal.** Identity comes from color, shape language, armor design and textures. Proportions stay close to real anatomy with a slight heroic push: hands and shoulders a little larger, within what motion capture can handle.

Why the body matters more than the triangle count: World of Warcraft's large pauldrons, broad shoulders and oversized hands make an overhead arm clip through the armor, so its swings stay short and sideways, and its rigid gear pieces follow a single bone. Black Desert's swings come from motion capture (Pearl Abyss runs its own studio, later expanded to 1,000 m² with 150 cameras), and captured motion fits only bodies close to human proportions. On heroic proportions, captured hands go through the pauldrons.

### Reference games

| **Game** | **Character triangles** | **Where the number comes from** | **Notes** |
| :---- | :---- | :---- | :---- |
| World of Warcraft | About 5k per base model since Warlords of Draenor; 10k to 20k in full gear (estimate) | The Warlords of Draenor update raised models from under 1,000 to over 5,000 polygons (gnome: 956 to 5,408, with bones from 130 to 196). An HD model file with every hairstyle and gear piece has 27,060 triangles | Hand-keyed animation; heroic proportions |
| ArcheAge | 8.2k for a Firran body; 15k to 25k with armor (estimate) | Sketchfab upload of the Firran female, likely the base body | Simpler models, much detail in textures |
| Black Desert | 24.4k for an NPC (Valkyrie Tiphaine) | Game rip on Sketchfab | Player characters with costumes and hair are heavier. Many 100k+ "Black Desert" models online are fan recreations |
| Crimson Desert | Not published; likely 80k to 200k+ (estimate) | Comparison: Kratos in God of War (PS4) has 80,000 polygons, 32,000 of them in the face; Aloy's hair in Horizon Zero Dawn is 100k triangles | Single-player; GPU cloth and hair simulation |
| ArcheAge Chronicles | Not published | Unreal Engine 5; Steam Next Fest demo from 19 to 26 Oct 2026; Early Access planned for Q4 2026; one listing reports an RTX 3060 Ti as the minimum | The upper limit of what an MMO attempts today |

### Texture approach

**Proposal.** Stylized physically based textures: a simplified, painterly color texture with real roughness and metal maps, and an optional normal map at lower resolution.

| **Approach** | **What it is** | **Memory per 2K set (approx.)** | **Fit for RunicGame** |
| :---- | :---- | :---- | :---- |
| Realistic (Black Desert) | Plain color with no lighting painted in, a sculpted normal map, roughness and metal; the lighting does the work | 13 to 16 MB (3 full maps) | Blurs at low resolution, which matters in crowds |
| Hand-painted (World of Warcraft) | Light, shadow and highlights painted into the color texture; little or no normal map | About 5 MB (1 map) | Painted highlights do not move with the sun, which looks wrong with weather and the day cycle |
| Stylized physically based (hybrid) | Painterly color plus real roughness and metal; optional low-resolution normal map | 9 to 10 MB | Reacts to dynamic light and still looks good at 1K, about 4× less memory per character than 2K |

* **Proposal.** Much of World of Warcraft's look comes from saturated lighting, soft fog and color grading. In Godot these are environment resources, the cheapest part to change later.
* **Proposal.** Every asset (characters, mobs, props, environment) uses the same texture approach, and bought or free assets are filtered by it. Mixing styles is the usual mistake of small teams.
* **Proposal.** Before locking the approach, texture one armor piece in the realistic and the hybrid style and compare both in Godot under morning, noon and sunset light.

### Reference sources

* Wowhead Dressing Room: a 3D viewer in the browser to put any race in any armor set and play animations; the best way to study World of Warcraft's silhouettes and how armor sits on the body.
* ArtStation and 80.lv: artists from World of Warcraft, ArcheAge and Lost Ark often post wireframes, texture sheets and triangle counts.
* Gameplay videos at maximum settings, comparisons of low and ultra settings, and sieges or large PvP fights, which show what each game scales down.
* Other MMOs as points between stylized and realistic: Lost Ark (detailed stylized-realistic armor), Guild Wars 2 (painterly environments), Elder Scrolls Online (closer to realistic, large PvP) and Throne and Liberty (realistic, large sieges).
* Sketchfab: it counts triangles, but the vertex count rises in the engine at texture seams and hard edges, so check again after importing into Godot. The Model Inspector shows the wireframe and texture sizes. Prefer models tagged game-ready or real game rips. Filter by Animated and watch the elbows and shoulders to judge a rig.

## Budgets

### Character triangles

**Proposal.** Triangle budgets at full detail:

| **Part** | **Triangles** | **Notes** |
| :---- | :---- | :---- |
| Body and head | 12k to 16k | About 5k in the face, for Black Desert-style creation and expressions |
| Hair | 5k to 10k | Often the hidden cost |
| Armor (5 pieces) | +8k to 12k net | The body under each piece is hidden, so triangles are not paid twice |
| Weapon | 2k to 4k |  |
| Player total | 25k to 35k | Between the Black Desert NPC (24k) and AAA single-player characters |
| Lower-detail versions (LODs) | 50%, 20% and 8% of full detail | The farthest at about 2k to 3k, for sieges |
| Common mob | 8k to 20k |  |
| World boss | 50k to 150k | Only one on screen |

Detailed swings do not need more triangles: the Black Desert NPC above has 24k. What changes is where the triangles go (see Characters).

### Crowds

* 200 players (100 vs 100) at 30k with no LODs: 6M triangles. Shadows draw most of them one or two more times, so 12M to 18M per frame, with about 4M vertices skinned.
* 200 players with LODs (10 near at 30k, 40 mid at 12k, 150 far at 3k): about 1.2M triangles, 5× cheaper, with no visible difference at distance.
* 500 players with the same split (10, 40 and 450): about 2.1M triangles.
* Draw calls: 8 meshes per character (5 armor pieces, head, hair and weapon) × 200 players is 1,600 per pass, about 4,800 with two shadow passes. Merging distant players into one or two meshes with a shared texture brings it to about 550 to 700 per pass.
* Bones: 200 players × 140 bones × 60 updates per second is about 1.7M bone updates per second. With animation LODs (10 at the full rig and 60 Hz, 40 at about 70 bones and 30 Hz, 150 at about 25 bones and 15 Hz), it is about 224k per second, about 7× less. This matches the multi-rate scheduler.

### Texture memory

| **Size** | **Memory per map with mipmaps, block-compressed (approx.)** |
| :---- | :---- |
| 2K (2048 × 2048) | 5.3 MB |
| 1K | 1.3 MB |
| 512 | 0.35 MB |
| One fully unique character: 8 pieces at 2K with 3 maps each | About 130 MB |

Distant characters need small texture versions: a 256-pixel texture uses 1/64 of the memory of a 2K one.

## Characters

* **Decision.** Two body types, female and male, each with variation in height, width and similar.
* **Decision.** One armor model per weight class (cloth, leather, plate), fitted to the body types and then modified and morphed into variants.
* **Proposal.** One skeleton for every playable race and body type. Races already share one hurtbox (RACE-02), so every animation works on every race.
* **Proposal.** Bodies start from MPFB2 (MakeHuman Plugin for Blender, Blender 4.2 or later): parametric age, build and gender, automatic rigging with Rigify support, and characters with realistic proportions. Its code is GPLv3 and its bundled assets are CC0. The MakeHuman project's position is that output, including output generated through scripts, contains no program code, so it can be used without restriction. Check its triangle count against the 12k to 16k body budget.
* **Proposal.** Height and limb length come from bone scaling, which armor follows automatically. Body mass comes from 2 or 3 shape keys that the pipeline copies onto every armor piece with Blender's Data Transfer or Surface Deform. The hurtbox stays the same for everyone.
* **Proposal.** The body is split into the five armor regions (head, chest, hands, legs, feet). Each armor piece hides its region, which avoids clipping and spends no triangles twice.
* **Proposal.** Armor is built from the body surface: select the region, offset it outward and add details. It fits the body and inherits the skinning weights.
* **Proposal.** Nothing in any armor stops the arm from going above the head. Pauldrons are segmented and follow the collarbone and the upper arm.
* **Proposal.** At least three edge loops at elbows and knees, and extra density at the shoulder, armpit and hips.
* **Proposal.** Textures carry dye masks from the start, so one armor mesh gives many looks.

### Rig

**Proposal.** Bones per part:

| **Part** | **Bones** | **Why** |
| :---- | :---- | :---- |
| Standard humanoid with fingers | About 55 | Weapon grips, drawing a bow, playing instruments |
| Twist bones (upper arm, forearm, thigh, calf) | 8 to 16 | Stops the forearm from collapsing when the wrist rotates mid-swing |
| Corrective bones (shoulder, elbow, knee, hip) | 6 to 10 | Keeps the shape in extreme poses |
| Weapon bones | 3 to 5 | Both hands, back or hip, two-handed grips |
| Hair, cloak and cloth chains | 10 to 30 | Follow-through motion and physics; the cloak slot |
| Face | 30 to 60, or shape keys | Black Desert-style character creation and expressions |
| Total at full detail | About 110 to 170 |  |

## Animation

* **Decision.** The vertical slice uses free animations and rigs from the web.
* **Proposal.** Quaternius' Universal Animation Library 1 and 2 as the main source: 120+ and 130+ animations on a humanoid rig ready for Godot, under CC0. The second volume adds melee and armed combos, parkour, farming and fishing. The free Standard version of the first has 45 animations; the full set comes in the paid Pro and Source versions.
* **Proposal.** Mixamo only for internal use. It is free for commercial games, but its FAQ excludes templates and asset packages that redistribute its raw character or animation files, and forbids using its content to train machine-learning models. The Engine will be distributed, so its templates and samples ship only with CC0 or own animations. Check Adobe's current terms before use.
* **Proposal.** Later: motion capture packs for sword and spear combat, or markerless capture from phone video, polished in Blender for weight, anticipation and the hit frame.
* **Proposal.** Retargeting in Godot with SkeletonProfileHumanoid, which maps bones automatically and works best with common English bone names. Twist and corrective bones are not part of that profile; they are computed in code from the limb rotation, so they work with any retargeted clip.
* **Proposal.** Swings are built in the phases of the Vision's timing profiles (startup, active, recovery), each with a clean blend point, so cancelling into a dodge does not make the character jump. Example: a sword light attack has 6 ticks of startup (about 200 ms) and 8 ticks of recovery (about 267 ms).
* **Proposal.** The pipeline exports each clip's hit marker, and the validation script fails a clip whose marker differs from its weapon's timing profile by more than one tick (33 ms).
* **Proposal.** One skeleton per creature family: humanoid, quadruped, bird and so on. Mixamo and Quaternius cover humanoids only, so wolves need their own quadruped rig and animations, reused by every four-legged creature.

## Weapons

* **Decision.** One model per weapon type, built by script and morphed into variants. The Vision's weapon appearances per weapon type are these variants.
* **Proposal.** Weapons are rigid, so parametric generator scripts fit them well: blade length, guard width and handle as parameters. Blender's Geometry Nodes can expose the same parameters with an interface, and scripts can drive it.
* **Proposal.** Origin at the grip, with the attachment points socket_grip, socket_sheath and socket_tip. The tip feeds trails and effects only; combat uses the server's cast shapes.

## Mobs

* **Decision.** Mob variety comes from colors (wolves of different colors) and from the same model with different equipment (goblin archer, goblin warrior).
* **Proposal.** Mobs use the player equipment system: a mob is a body, an equipment list and a color palette, with no extra code.
* **Proposal.** Roaming elites (rare, larger versions of common mobs, in Ideias) are the same model scaled up with their own palette.
* **Proposal.** Goblins use the humanoid skeleton with different proportions. Retargeting handles locomotion; weapon swings need a check for hand contact.

## Environment

* **Decision.** Modular objects and sets of trees, rocks and props that change per biome and type. Species share a model with different textures and colors (apple and cherry). Trees are made of 3 or 4 parts (roots, trunk, canopy and leaves) that combine into different types and states.
* **Proposal.** Modular for authoring, merged for runtime: the pipeline combines the parts into finished meshes per type and state (full, harvested, stump, cut), so each tree draws as one mesh.
* **Proposal.** Decorative trees and rocks use MultiMesh, and species differ by per-instance color and texture-layer data instead of separate materials.
* **Proposal.** Distant trees become impostors, flat two-triangle images of the tree. Godot has no built-in impostors, so this is an Engine task or a plugin.
* **Proposal.** Biome variation (snow on upward faces, autumn color, dryness, wetness) comes from shader parameters driven by each node's climate, with no new models or textures.
* **Proposal.** Rocks, crates, planks and modular walls are good candidates for parametric generators.

Example with 2,000 trees on screen: as four separate parts with no instancing, about 8,000 draw calls and about 10M triangles. Merged, instanced and with LODs (100 near at 5k, 400 mid at 1k, 1,500 far as impostors), about 0.9M triangles and a few dozen draw calls.

## Ships

* **Decision.** Ships are modular. Stations (helm, cannons, anchor, mage, archer, repair and others) are models attached to the ship, each ship has its own hull, and mast types (such as the fore-and-aft sail at the stern) are reused and resized across ships.
* **Proposal.** Stations are prefabs that snap onto named attachment points on the hull (socket_cannon_01), each with its own collision and interaction volume.
* **Proposal.** Masts are scaled in length only, never uniformly, so thickness and texture density stay the same.
* **Proposal.** Sails move in a vertex shader driven by the ship's wind value from the wind system, with no bones.

## Textures and materials

* **Decision.** Textures are either procedural (ship wood, grass) or made by hand (items).
* **Decision.** Texture and asset quality is not a priority for the vertical slice.

|  | **Image texture** | **Procedural in the Godot shader** |
| :---- | :---- | :---- |
| Memory | 2K about 5.3 MB, 1K about 1.3 MB, 512 tiling about 0.35 MB | About 0 MB, only parameters |
| GPU work | A cheap hardware texture read per pixel | Math for every pixel, every frame: each noise layer is about 50 operations, so 4 layers are about 200 |
| At a distance | Mipmaps handle it | Shimmers unless fine detail fades out with distance |
| Variation | Fixed; repetition shows on large surfaces | Unlimited: changes with world position and live parameters |
| Ease of replicating | Hand-painted images cannot be regenerated; variety through masks and tints | Code in the repository with per-object parameters, but no files: it exists only while the game runs |

Four noise layers over half of a 1080p screen are about 300M operations per frame, a fraction of a percent of a mid-range GPU. The cost scales with pixels (4× at 4K) and with the number of such materials on screen.

* **Proposal.** Blender's procedural materials do not run in Godot, so they are always baked into images. A node graph plus a seed is a recipe: change a parameter and the pipeline re-bakes every variant (apple and cherry, oak and pine, new and old wood). The same look at runtime needs a Godot shader rewrite.
* **Proposal.** Characters, armor, weapons and items: unique image textures, baked or painted, with dye masks.
* **Proposal.** Ship wood, stone, grass and terrain: small tiling images (512 to 1K) reused across thousands of objects, with runtime variation by world position (tint, wear).
* **Proposal.** Weather and biome layers (snow, wetness, moss, autumn): procedural in the Godot shader, driven by node climate.

## Pipeline

### Sources and scripts

* **Decision.** Models are made by people. AI only writes Blender scripts that recreate a given model, so it can be imported into Blender and adjusted directly in the script.
* **Proposal.** Scripts suit models built from primitives and modifiers (weapons, masts, planks, crates, rocks, walls): 50 to 300 lines with readable parameters. For detailed meshes (bodies, detailed armor, faces), a 1:1 script is the mesh data written as Python numbers. A 20k-triangle model becomes 2 to 4 MB of code against about 0.7 MB of glTF, it must also carry UVs, weights and shape keys, and nobody edits it by hand. Those models stay as .blend or glTF files, and scripts store the operations applied on top: morphs, scaling, attaching parts, LODs and export.
* **Proposal.** Variants are recipes: a small JSON file per variant with the base model, morph values, parts, materials and colors. Headless Blender (blender -b -P build.py) rebuilds every variant from its recipe, so a change to a base updates all of its variants.

### Build flow

**Proposal.** Base .blend files and recipes, then the headless Blender build, then the validation script, then the glTF export. From glTF on, the flow is the one in Architecture v4: Godot import (textures, LODs, materials), RunicEditor scenes, the Cooker for server and client packages, and Godot's export for the client .pck.

### Naming and attachment points

**Proposal.** Attachment points are Blender empties with fixed names, read by the Engine when it imports the asset:

| **Name** | **Used for** |
| :---- | :---- |
| socket_grip, socket_sheath, socket_tip | Weapons: hand, carry position, trails and effects |
| socket_back | Glider, wing or trade pack |
| socket_cannon_NN, socket_helm, socket_anchor, socket_mast_NN | Ship stations and masts |
| socket_fruit_NN | Fruit on tree canopies |

### Validation script

**Proposal.** Every export runs the checks below; an asset that fails does not go into the game.

* Triangle count against the budget of its category.
* Bone names against the shared skeleton of its family.
* Scale (1 unit is 1 m) and origin (feet at 0 for characters, grip for weapons).
* Material count and texture sizes.
* Required attachment points present.
* Hit markers against the weapon's timing profile.
* A license entry for every third-party source.

### Version control and licenses

* **Proposal.** Sources (.blend files, textures, recipes) live in Git LFS. Generated outputs are not committed; they are rebuilt from the recipes.
* **Proposal.** A license manifest records the source and license of every asset (CC0, Mixamo, own work, AI-assisted scripts). Because the Engine is distributed, its templates and samples contain only CC0 or own assets.

## Map authoring markers

**Decision.** Every marker the map needs is catalogued here, and placing one must be quick and simple. Everything on the map is a painted layer, a point, an area or a path. Floods and slide paths need no markers: the cooker finds them from the elevation layer (terrain hydrology).

**Proposal.** Each marker type has a fixed name prefix (marker_...) and a fixed color in GIMP, and a validation step lists missing or broken markers before cooking, like the asset validation script.

### Painted layers (GIMP)

* **Decision.** One layer per information track: terrain type, elevation, biome, mob spawns, fauna and flora. Terrain type also says which ground turns to mud (soil, grass and farmland) and which never does (rock, sand and paved road), and a flood exclusion mask marks places that must never flood (ex.: cities).
* **Decision.** Snowfields and drift zones. Snow levels (none, light, heavy, deep) follow the weather, a timer drops a level while it isn't snowing, and drift zones at the bottom of slopes count one level deeper (HAZARD-01).
* **Decision.** Every sea region has its own attachment type (ATTACH-01).
* **Proposal.** Elevation continues under the sea, so the same layer gives the static seafloor, reefs and sandbanks.
* **Proposal.** A hazard layer with one color per tag: reef, shallow, freezing water (with its Chill rate), vent, kelp, swamp and magnetic anomaly.
* **Proposal.** A sea-region layer for attachment types, sea threats and weather regions.

### Points

* **Decision.** Hand-made content and landmarks (cities, camps, unique content): the generator only places a temporary object there.
* **Decision.** Altars: every city has one, and others are scattered across the world.
* **Decision.** Cave entrances, each with a closed and an open model; earthquakes open them for a while.
* **Decision.** Maelstroms that lead into rifts and raids.
* **Decision.** Packing benches (one per region, near its city node), processing stations, trade-pack delivery points (cities, ports and islands) and the four black-market goblins.
* **Proposal.** Docks and ports, lighthouses, shipwrecks and ocean chests, volcano centers, world boss arenas, and siren and false-light spawns.

### Areas

* **Decision.** Spawn areas for mobs and for trees that can be cut down; the other trees are fixed decorative models.
* **Decision.** Castle zones (the designated zones of each region, on the neutral continent only) and housing zones in 8×8 slots (LAND-01).
* **Decision.** Soft barriers around areas that aren't open yet: crossing one shows a countdown and sends the player back.
* **Decision.** Flight zones (the neutral continent and the Sky Island).
* **Decision.** Node volumes with their type (city, capital, village, mine, forest, farm, port, island) and their region, whose parent is the city node; open sea between islands, reefs and wrecks belong to transitional nodes.
* **Proposal.** Fog-bank and calm-zone areas, cave shelter volumes (no weather inside), updrafts, rockfall areas, and the eruption hazard area with its ore-richness ring.

### Paths

* **Decision.** Rivers, drawn as curves; a canyon river can flood.
* **Decision.** Roads, where auto-path works (besides mapped areas). Paved roads never turn to mud; the cooker raises them or bridges the channels where they would flood, and warns when a road would flood in a monsoon.
* **Decision.** Lava channels.
* **Decision.** Avalanche and mudslide paths: the cooker generates them from the elevation layer (start, path and landing area), and hand-placed markers only add, remove or adjust a path.
* **Proposal.** Routes for convoys, escorts, trade and public transport, with their stations (TRANSIT-01).

### Ship assets (Blender)

* **Decision.** Compartment volumes in ship space, each with its breach limit (SHIP-01).
* **Decision.** Windows and openings flagged so a bucket throw passes through them.
* **Decision.** The part slots each ship type allows: hull, bow, masts, sails, rigging, helm, cannons and figurehead (MOV-02).
* **Proposal.** Hull sockets for attachments, a point and a normal flagged as reachable from the deck or only over the side; a ship type has 1 to 8 of them (ATTACH-01).

## Vertical slice order

**Proposal.** Each step is a good size for one slice:

* Recipes, the validation script and the naming conventions.
* The MPFB2 bodies and one armor set made from the body.
* Quaternius animations retargeted in Godot.
* Trees merged into meshes per state and drawn with MultiMesh.
* One ship with its stations.
* The wolf and the goblin.

The Blender side can start before slices 22 (world rendering) and 23 (animated characters) of the roadmap. Until GDB-13, assets use Godot's standard material, which the proposed texture approach already fits.

## Requirements by repository

### Engine

* Blender export helper grown into a game-agnostic build tool: recipe runner for headless Blender, validation with budgets read from project settings, attachment-point and collision naming, hit-marker export.
* Skinned characters (ANIM-1, COOK-5, CLI-5, GDB-6): one skeleton per creature family, twist and corrective bones computed at runtime, animation update rates by distance, attachment points for weapons, cloak and back slot.
* Presenter (GDB-5): MultiMesh with per-instance color and texture-layer data, one mesh per resource state, impostors for distant vegetation, merged meshes and small texture versions for distant characters.
* Production look (GDB-13): shader layers for weather and biome driven by environment data.
* Map marker import: painted layers, points, areas and paths cooked into volumes, routes and placed objects, with a validation step that lists missing or broken markers.
* Terrain hydrology at cook time: channels, height above the channel, low spots and slide paths, with editor views for the flood at monsoon and the slide paths.

### Game

* Art direction and texture approach, locked after the side-by-side test.
* Two base bodies, three armor bases per body type, one base per weapon type, variant recipes and dye masks.
* Creature families: humanoid (goblin) and quadruped (wolf) rigs and animations.
* Tree, rock and prop sets with their states; ship hulls, stations and masts.
* Swing animations per weapon timing profile, with hit markers.
* License manifest for every third-party asset.
* The map marker catalog (Map authoring markers), filled while authoring the map.

### Platform

* Nothing new.

## Open

* The final texture approach, after the side-by-side test of the realistic and hybrid styles.
* Final triangle and bone budgets, after measuring a 100 vs 100 scene in Godot.
* Client animation (Architecture v4, open decision 3), checked against the crowd budget above.
* How distant characters use small texture versions in Godot.
* Impostors for distant vegetation: Engine feature or plugin.
* The source of quadruped animations.
* Which models become scripted generators and which stay as files.
* Face rig: bones, shape keys or both, for Black Desert-style creation.
* The visual height band between races (RACE-02 proposes ±10%).

## Dropped

* Crimson Desert-level fidelity as the visual target.
* World of Warcraft's heroic character proportions, such as pauldrons that block overhead swings. Its identity stays through color, shapes and textures.

## Sources

* [GameSpot: World of Warcraft's new character models and system requirements](https://www.gamespot.com/articles/will-world-of-warcraft-s-new-character-models-change-the-game-s-system-requirements/1100-6417319/)
* [GameSkinny: Warlords of Draenor updated character models](https://www.gameskinny.com/news/warlords-of-draenor-updated-character-models/)
* [WoW modding: HD character model triangle reduction](https://elijahketchersid.com/forums/thread-127.html)
* [Sketchfab: Ferre female ArcheAge](https://sketchfab.com/3d-models/ferre-female-archeage-5bf24b2d78bf41839417f797218d3129)
* [Sketchfab: Valkyrie Tiphaine from Black Desert](https://sketchfab.com/3d-models/valkyrie-tiphaine-from-black-desert-213d6fc64d3843de802d5b04b830e93c)
* [PlayStation Blog: polygonal evolution of Kratos and others](https://blog.playstation.com/archive/2019/12/16/from-kratos-to-the-fearsome-rathalos-see-the-polygonal-evolution-of-5-iconic-playstation-characters)
* [ResetEra: Aloy's hair in Horizon Zero Dawn](https://www.resetera.com/threads/highest-poly-character-model-used-in-a-game.84396/)
* [GamesBeat: BlackSpace Engine for Crimson Desert](https://gamesbeat.com/pearl-abyss-unveils-graphics-power-of-the-blackspace-engine-for-crimson-desert/)
* [Push Square: inside Pearl Abyss](https://www.pushsquare.com/features/inside-pearl-abyss-the-ambitious-studio-behind-ps5s-massive-crimson-desert)
* [Game World Observer: Pearl Abyss Art Center](https://gameworldobserver.com/?p=10408)
* [Gematsu: ArcheAge Chronicles demo](https://www.gematsu.com/2026/10/archeage-chronicles-limited-time-demo-for-pc-launches-october-19)
* [MMOlist: ArcheAge Chronicles status](https://mmo-list.com/games/archeage-chronicles)
* [TheGameExtras: ArcheAge Chronicles requirements](https://thegameextras.com/game/archeage-chronicles/)
* [Wowhead: transmog tools and Dressing Room](https://www.wowhead.com/transmog)
* [MeinMMO: World of Warcraft's graphics](https://mein-mmo.de/en/11-reasons-why-wow-is-still-the-best-mmorpg-in-2026,1578553/11/)
* [CG Channel: MPFB 2](https://www.cgchannel.com/2025/03/check-out-open-source-blender-character-generation-plugin-mpfb-2)
* [MakeHuman license](https://github.com/threos/makehuman-macos/blob/master/LICENSE.md)
* [Quaternius: Universal Animation Library](https://quaternius.itch.io/universal-animation-library)
* [OpenGameArt: Universal Animation Library 2](https://opengameart.org/content/universal-animation-library-2)
* [Adobe Community: Mixamo FAQ on licensing](https://community.adobe.com/questions-696/mixamo-faq-licensing-royalties-ownership-eula-and-tos-589400)
* [Godot docs: Retargeting 3D Skeletons](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/retargeting_3d_skeletons.html)
