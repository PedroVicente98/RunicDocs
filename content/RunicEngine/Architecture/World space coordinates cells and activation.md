---
title: "World space: coordinates, cells and activation (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World space: coordinates, cells and activation (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

Positions are 64-bit doubles with a real Y axis, the world is indexed by sparse 3D cells, and activation volumes around players decide what loads and simulates. There are no spatial layers.

## 64-bit coordinates (decided)

World positions are 64-bit doubles in meters with a real Y axis: altitude and depth are ordinary coordinates. The smallest unit gameplay relies on is 1 cm. This closes the choice between doubles and cell-relative coordinates: the server works in doubles everywhere, and only the wire is cell-relative. A 32-bit position loses about 1 cm of precision for every 130 km from the origin, which an engine meant for continent-scale worlds cannot accept; a double stays far below 1 cm across any planet-sized space.

| Place | Precision |
| :---- | :---- |
| Server simulation and [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] | 64-bit double positions (Jolt in double precision); shapes and local math stay 32-bit |
| Network | Quantized relative to the entity’s cell origin on all three axes (16 bits per axis on 64 m cells ≈ 1 mm) |
| Client rendering | 32-bit relative to the camera in the [[RenderData in Core\|RenderFrame]]; inside Godot relative to the presenter’s own origin, rebased about every 4 km (Godot stays single precision) |
| Authoring | Region-local coordinates in the [[Tools#RunicEditor\|RunicEditor]] plus a 64-bit region origin stored as doubles, never as a Godot Vector3 |

## Which values are 64-bit (decided)

One rule decides 64 or 32 bits, and the compiler enforces it: a point in the world is 64-bit, everything else is 32-bit, going up is implicit and going down happens only through a named function.

| It is… | Type | Bits |
| :---- | :---- | :---- |
| A place in the world | WorldPosition | 64 |
| The difference between two places | WorldDelta | 64 |
| Direction, velocity, size, rotation, local offset, shape | Vec3, Quat | 32 |

| Where 64 becomes 32 | How |
| :---- | :---- |
| Physics | Jolt’s RVec3 in double for positions; the rest in float |
| Network | Quantized relative to the cell: 16 bits per axis on 64 m cells is about 1 mm |
| Extraction and presenter | Camera-relative in the RenderFrame; relative to the presenter’s origin inside Godot |
| [[Cooker\|Cooker]] | The region origin in double plus the local position the editor saved in float |

Float32 step size by distance from the origin: about 0.03 mm at 500 m, 0.24 mm between 2 and 4 km, 1 mm between 8 and 16 km and 8 mm between 64 and 128 km. That is why the editor works each region near its local origin and the presenter rebases about every 4 km. Where v3 used Vec3d for a point (WaterSample, RiverControlPoint, AIWorkingMemory, AIIntent, SkillStartedEvent), v4 uses WorldPosition.

```cpp
// Core/Public/WorldSpace.hpp — illustrative contract, not a frozen API.
struct WorldPosition { double x, y, z; };   // a point in the world, meters, real Y
struct WorldDelta    { double x, y, z; };   // a difference between points (may span 100 km)

constexpr WorldDelta    operator-(WorldPosition a, WorldPosition b) { return { a.x - b.x, a.y - b.y, a.z - b.z }; }
constexpr WorldPosition operator+(WorldPosition p, WorldDelta d)    { return { p.x + d.x, p.y + d.y, p.z + d.z }; }
constexpr WorldPosition operator-(WorldPosition p, WorldDelta d)    { return { p.x - d.x, p.y - d.y, p.z - d.z }; }
constexpr WorldDelta    operator+(WorldDelta a, WorldDelta b)       { return { a.x + b.x, a.y + b.y, a.z + b.z }; }
constexpr WorldDelta    operator*(WorldDelta d, double s)           { return { d.x * s, d.y * s, d.z * s }; }
inline    WorldPosition operator+(WorldPosition p, Vec3 local)      // float goes up with no loss
    { return { p.x + local.x, p.y + local.y, p.z + local.z }; }
// Not defined: WorldPosition + WorldPosition, WorldPosition * scalar,
// or any implicit conversion to Vec3. Writing any of them does not compile.

constexpr double DistanceSq(WorldPosition a, WorldPosition b) {
    const WorldDelta d = a - b;
    return d.x * d.x + d.y * d.y + d.z * d.z;
}

// The only way down to 32 bits. Debug builds refuse offsets too large for float.
constexpr double kMaxLocalOffsetM = 10'000.0;   // at 10 km the float step is about 1 mm
inline Vec3 ToLocal(WorldDelta d) {
    RUNIC_ASSERT(d.x * d.x + d.y * d.y + d.z * d.z < kMaxLocalOffsetM * kMaxLocalOffsetM);
    return { float(d.x), float(d.y), float(d.z) };
}
```

```cmake
# Inside runic_add_module, for every target
if(MSVC)
    target_compile_options(${target} PRIVATE /we4244 /we4305)   # double → float and truncation become errors
else()
    target_compile_options(${target} PRIVATE -Werror=float-conversion)
endif()

# In Runic::Core, where GLM is PUBLIC: vec3 ↔ dvec3 only by explicit conversion
target_compile_definitions(RunicCore PUBLIC GLM_FORCE_EXPLICIT_CTOR)
```

On MSVC, C4244 also catches lossy integer conversions, so the first build will report more than double to float. Godot is outside this rule on purpose: it only ever receives floats that the presenter has already made small.

## Spatial hierarchy

| Level | Nature | Purpose |
| :---- | :---- | :---- |
| World | Persistent world identity (WorldId) | Global coordinates and registry; each separate map is its own WorldId |
| Region | Authored content area (a [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] entity) | Gameplay state: PvP rules, ambient light profile, music, spawns, gimmick |
| Sector | Automatic coarse XZ bucket (e.g., 512 m) | Streaming and coarse lookup |
| Cell | Automatic fine 3D bucket (e.g., 64 m), sparse | Candidate lookup for combat, AI, interest, light, map knowledge |
| Volume | Authored 3D volume, placed in the RunicEditor | Caves and underground spaces, flight zones, build zones, rule areas, indivisible volumes |
| SimulationOwner | Runtime assignment | Which process is authoritative now |

* Cell, sector and region transitions inside one simulation are index updates, never entity recreation or [[Networking replication interest and handoff#Simulations, handoff and ghosts|handoff]].

* Gameplay locations (a harbor, a market) are game data volumes and may cross any partition.

* Large objects (ships, world bosses, floating islands) register in every cell their bounds touch, deduplicated on query.

## Sparse 3D cells and exact queries

* **Cells are 3D and sparse by column.** A cell key is (x, y, z) at a fixed size per world. Each XZ column stores only the Y cells that hold content or activity, so empty air and solid rock cost nothing; Cell\[x\]\[y\]\[z\] is never allocated everywhere.

* **Every test is exact XYZ.** Combat is action-based and characters jump, glide and fly, so a query gathers the 3D cells its volume touches and then tests exactly (Jolt shapes, CharacterVirtual). A 2D distance is never a gameplay answer.

* **One vocabulary, separate structures.** Region, Sector, Cell and Volume give streaming, server scope, interest, navigation, AI, spawning, persistence and tools a shared spatial language, while each subsystem keeps its own specialized structure.

| Concern | Internal structure |
| :---- | :---- |
| World partition | Region, Sector, sparse 3D Cell, authored Volumes |
| Physics | Jolt broadphase |
| Rendering | Frustum and occlusion culling, HLOD, GPU visibility structures |
| Navigation | Navmesh tiles; 3D flight paths for flying actors |
| Networking | Interest candidate sets |
| AI | Spatial candidates and activation |

* **Visual relevance is not simulation relevance.** A client may render a distant HLOD mountain, a city silhouette, a floating island or the ocean while receiving no NPC, player or projectile data from that area.

## Activation volumes

* Each player carries an activation volume: an asymmetric ellipsoid around the player, wider than it is tall (e.g., 1 km horizontally and less vertically; the Game sets the radii). The union of all players’ volumes decides which cells load and which simulate. A cell outside every volume is not simulated.

* The smaller vertical radius keeps spaces far above or below the player, such as a deep cave or a high island, out of the active set until the player approaches them.

* Transitions use prepare, commit and release thresholds: a cell starts loading when it nears the union, becomes active inside it, and unloads only after it has stayed outside a larger release volume. Walking back and forth on an edge never thrashes loads.

* The client streams presentation with the same idea and its own, usually larger, radii, plus LOD, HLOD and world proxies at distance.

## Volumes for caves and rules

* Caves, underground spaces and other rule areas are RunicVolume3D nodes placed in the RunicEditor and cooked with the cells they touch. A volume carries a kind the Game gives meaning to (a cave, a flight zone with its altitude ceiling, a castle build zone, a light or music profile) and is queried with exact XYZ.

* Underground spaces live in the main world beneath the surface, in the same coordinates; nothing in the Engine knows Surface, Sky or Underground. Weather, wind and skylight read volume flags (a cave volume is sheltered and dark).

* **Indivisible volumes** (an island, a castle, a docked ship) are flagged so that no ownership boundary ever cuts them: the whole volume always belongs to one simulation.

```cpp
// Illustrative contract, not a frozen API.
struct WorldPosition { double x, y, z; };     // meters; y is real altitude or depth

struct CellKey {                              // a sparse 3D cell (e.g., 64 m)
    WorldId world;
    int32_t x, y, z;
};

struct ActivationVolume {                     // asymmetric ellipsoid around a player
    WorldPosition center;
    float horizontal_radius_m;                // Game value (e.g., 1,000 m)
    float vertical_radius_m;                  // smaller than the horizontal radius
};

struct AuthoredVolume {                       // placed in the editor, cooked with its cells
    VolumeId     id;
    VolumeKindId kind;                        // meaning given by the Game
    bool         indivisible;                 // never cut by an ownership boundary
};
```

## Sparse and expandable world

* The coordinate space reaches far beyond current content: sector and cell coordinates are 32-bit integers, which at 512 m per sector span far more than any planet.

* Only cells with content or activity exist in memory. Empty sea and unbuilt land cost nothing; open ocean is generated by the water system, not stored as cells.

* A new continent is new regions in that space. A content patch adds its cooked cells, streaming makes them appear without restarts or loading screens, and the [[Platform and operations#Simulation placement|World Coordinator]] assigns their simulation.

## Worlds, instances and transitions

The world is presented as seamless places but authored, cooked, streamed and simulated in many pieces. “One world” is a property of the logical identity and the coordinate space, not of one source file, one runtime package or one simulation process.

* **Process boundary versus world and instance boundary.** A process boundary answers “who computes this?”; a world boundary answers “which map is this?”; an instance boundary answers “which copy of that map is this?”. A neighboring region may run in another simulation process and still be the same world.

* **The main world** is WorldId \= MainWorld, InstanceId \= 0: the surface, its floating islands and its underground spaces in one continuous coordinate space.

* **Separate persistent maps** are their own WorldId with InstanceId 0, shared by every player (the Game’s sky world is one). **Instances** (dungeons, raids, the shop island) are extra InstanceIds of a map.

* **Worlds never share a border.** There is no handoff or ghost between worlds. A world transition is a checkpoint plus a new connect ticket: the source simulation checkpoints the character through the service port, the Platform issues a ticket for the destination simulation, and the client connects there while it loads the destination. Presentation covers the load (the Game flies the character through the clouds); portals to other maps and entries to instances use the same path.

* **Partition:** Region (authored gameplay and content concept), then automatic Sector, then automatic Cell (engine spatial structures). Simulation ownership is separate again and is never encoded as “one chunk equals one server”.

## Runtime loading and ownership

* **Client streaming:** cells inside the client’s activation volume, with LOD, HLOD and world proxies at distance. Detailed cell assets include meshes, textures, vegetation, collision needed for local prediction, audio and presentation data; a world or continent proxy covers very distant geography.

* **Server streaming:** cells inside the union of activation volumes: static collision, gameplay and world metadata, nav tiles where active, spawn, routine and state definitions and spatial indices — never textures, vegetation shaders or other presentation data.

* **Ownership:** spatial boundaries never encode server identity. A simulation may own many quiet cells or regions; a busy area can later move or split without changing world coordinates or authored assets. Seamless handoff uses overlap, ghosting and a single authority epoch, so players never see a loading screen or an explicit reconnect.

* **Floating islands** are fixed, indestructible bodies inside the main world that at most rise and sink slightly. Each is an indivisible volume, so it never crosses a simulation boundary.

* **Archived but supported:** a moving island carrying a castle would be a kinematic indivisible volume that hands off as one group, like a ship ([[WATER-7|WATER-7]]).

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Simulation core Flecs and Jolt|Simulation core: Flecs and Jolt (Engine)]] · [[Water system|Water system (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World space: coordinates, cells and activation (Engine) · exported 2026-11-03
