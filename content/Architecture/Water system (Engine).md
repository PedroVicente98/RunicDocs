---
title: "Water system (Engine)"
tags:
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

Water is a queryable, streamed spatial field, not a global height plane: any position can be sampled for surface, depth, flow and submersion. Buoyancy and movement are separate components that consume those facts, so passive water costs nothing and only ships, swimmers and drifting objects pay.

The system covers oceans, lakes, rivers, canals, cave rivers, underground seas, rapids, waterfalls, currents, swimming characters, floating rigid bodies and watercraft. It deliberately avoids general fluid simulation and models only what gameplay needs: macro surface position, surface normal, depth, flow, submersion, connectivity and optional dynamic state.

### Ownership

| Part | Owner | Contains |
| :---- | :---- | :---- |
| WaterSystem and water bodies | Engine | Stable WaterBody and WaterRoute identities, cooked runtime fragments, the sampling API, planar, ocean, spline-river and flow-volume implementations, connection semantics |
| Interaction components | Engine | BuoyantBody, CharacterWaterMovement, ObjectWaterMovement, WatercraftMovement, WaterInteractionState |
| Streaming and handoff integration | Engine | Water fragments inside Region, Sector and Cell streaming; continuity across simulations |
| Authoring, cooking and debugging | Engine | RunicWaterBody3D and flow-painting tools in the RunicEditor, the Cooker’s water pipeline, validation, debug drawing |
| Water content | Game | Named oceans, rivers, lakes, cave waterways, current and wind maps, waterfalls; materials, VFX, audio, wave style, foam |
| Profiles | Game | SwimProfile, BuoyancyProfile, ObjectWaterMovementProfile, WatercraftMovementProfile values |
| Water gameplay rules | Game | Breath and drowning, ability restrictions in water, magical currents, tide events, boss modifiers, navigation policy per connection |
| Ship contents | Game | Cargo, cannons, sails, crew, faction, equipment, trade and combat rules |
| Durable water state | A Game service stores it on the Go SDK; Game decides | Dam, lock or water-level states that must survive restarts |

### Core model: water reports facts

```cpp
// Illustrative contract, not a frozen API.
struct WaterSample {
    bool         valid = false;
    WaterBodyId  body  = InvalidWaterBody;

    WorldPosition surface_position;  // 64-bit world position
    Vec3  surface_normal {0, 1, 0};
    Vec3  flow_velocity {0, 0, 0};   // world space; includes current modulation

    float depth      = 0.0f;
    float submersion = 0.0f;
    WaterFlags flags {};
};

WaterSample sample;
if (water.TrySample(position, sample)) { /* ocean, lake, river or flow volume */ }
```

* The caller never needs to know which kind of water body answered.

* The WaterSystem reports facts; it never decides an entity’s response. Each movement component consumes the same sample in its own way.

* The server samples the macro gameplay surface. Godot on the client adds ripples, foam, displacement, spray, reflections, refraction, wakes and visual waves on top without the server simulating them.

* The sample already includes the environment’s contribution (tide level, time-varying current and, on oceans, gameplay swell and wave events), so consumers never query the environment separately for water.

**Non-goals:** no Navier-Stokes grid, no SPH or per-particle server simulation, no pressure, erosion or real-time river formation, no centimeter agreement between shader waves and gameplay water, and no assumption that water is horizontal.

### Water bodies and routes

Every water body has a stable namespaced ID (game:great\_western\_ocean, game:aster\_river\_upper, game:aster\_river\_cave, game:deepwater\_sea). A WaterRoute groups the fragments of one logical waterway — the surface, cave and underground parts of the Aster River load independently but share game:aster\_river.

| Body type | Representation | Typical uses |
| :---- | :---- | :---- |
| PlanarWaterBody | Bounded polygon with a constant or offset surface height | Lakes, reservoirs, enclosed water, tests |
| OceanWaterBody | Very large bounded surface, a deterministic gameplay swell and a cooked current field | Seas and oceans, including underground oceans |
| SplineRiverBody | 3D centerline spline with width, depth and flow profiles | Rivers, canals, cave rivers, descending waterways |
| FlowVolume | 3D volume with a directional or vector flow field | Waterfalls, rapids, spillways, whirlpools, underwater current tunnels |

### Rivers are 3D splines

A river surface descends continuously through world space; it is never a stack of horizontal planes. Each control point, or sampled distance along the spline, can define width, depth, flow speed, cross-section, bank metadata and rapids markers; the Cooker turns them into an efficient sampled runtime form.

```cpp
struct RiverControlPoint {
    WorldPosition position;
    float width;
    float depth;
    float base_flow_speed;
    RiverPointFlags flags;
};

// Simplest flow: along the spline tangent at the authored speed.
Vec3 direction = Normalize(river.Centerline().TangentAt(s));
Vec3 flow      = direction * river.FlowSpeedAt(s);
```

Flow speed is an authored profile with an optional slope contribution. The Engine promises deterministic, understandable gameplay water, not exact hydrodynamics. Complex bodies use a cooked low-resolution vector field for bends, eddies, side currents, currents around islands, harbor circulation, rapids or magical flows — still a cheap interpolation at runtime.

### Ocean currents

* Each OceanWaterBody carries a cooked current field: a coarse vector grid (for example one vector per 512 m), interpolated at sample time. A 600 km² map needs about 2,300 vectors.

* Current fields are authored as painted vector layers or generated from coastlines and a prevailing direction, then cooked with the world.

* The Environment modulates them over time — tide phase, season, weather — with deterministic functions, so the same position and world time always give the same current everywhere.

* The same cooked field feeds nautical charts on the Game side.

### Connections form a graph

Water bodies link into a graph. One route can run from a mountain lake through the upper river, rapids and the lower river (with a side canal), into a cave river, a deep river and finally an underground sea.

| Connection | Meaning | Navigation example |
| :---- | :---- | :---- |
| Smooth | Continuous surface and flow blend | Ordinary river segments |
| Estuary | River-to-lake or river-to-ocean blend | Current fades into the sea |
| Rapids | Navigable, high flow and turbulence | Fast downstream passage |
| Waterfall | Surface discontinuity plus a downward FlowVolume | Often downstream-only or non-navigable |
| Canal | Authored controlled connection | Artificial waterway |
| Lock | Stateful controlled elevation change | Later feature |
| Custom | Game policy on Engine connection data | Special world mechanics |

* **Smooth transitions** blend surface position, normal, flow and presentation parameters across a transition region, so a vessel never hits a physics discontinuity where one body ends and another begins.

* **Waterfalls** are a FlowVolume between the upper and lower surfaces; the Game’s navigation policy marks them navigable, downstream-only, restricted or non-navigable.

* **Rapids** stay a continuous sloped surface with stronger flow and optional vector-field turbulence.

### Runtime API

```cpp
// Illustrative contract, not a frozen API.
class WaterSystem {
public:
    bool TrySample(const WorldPosition& position, WaterSample& out) const;
    bool TrySample(const WorldPosition& position, WaterQueryContext& context,
                   WaterSample& out) const;          // cached locality

    void QueryBodies(const WorldBounds& bounds,
                     SmallVector<WaterBodyId, 8>& out) const;

    void RegisterFragment(const CookedWaterFragment& fragment);
    void UnregisterFragment(WaterFragmentId fragment);
};

struct WaterQueryContext {
    WaterBodyId     previous_body     = InvalidWaterBody;
    WaterFragmentId previous_fragment = InvalidWaterFragment;
};
```

* **Lookup path:** world position, then Sector, 3D Cell, the cell’s candidate water fragments, then the precise sample. The WaterSystem never scans every river in the world.

* **Cached locality:** moving entities usually stay in the same fragment, so the context tests the previous fragment before any broader cell lookup.

* **Thread safety:** sampling is read-only and safe from any worker in a parallel phase; fragment registration happens only at streaming safe points.

### Buoyancy and movement are separate components

BuoyantBody makes a Jolt dynamic body float. A BuoyancyProfile can also set a righting strength that keeps the body upright: ships roll and pitch with the swell but never capsize. Current does not belong to buoyancy: a movement component decides how much flow an entity follows and how much it propels itself. An object can therefore float without moving, drift with the current, sail, or use a future custom movement.

![[arch-water-interaction-environment-to-jolt-and-characte.png]]
*Water interaction — environment to Jolt and characters*

*Water interaction — environment to Jolt and characters*

The Environment shapes every sample (tide level, current over time, swell) and gives ships their wind; only the four components turn those facts into forces for Jolt or desired motion for characters.

```cpp
struct BuoyancyProfile {
    Span<BuoyancyPoint> points;   // sampled every tick
    float buoyancy_scale;
    float linear_water_drag;
    float angular_water_drag;

    float righting_strength;      // keeps the body upright; ships never capsize
};

struct BuoyantBody { BuoyancyProfileId profile; };
```

| Movement component | Physical model | Current behavior | Examples |
| :---- | :---- | :---- | :---- |
| CharacterWaterMovement | CharacterVirtual | Profile-controlled current influence | Players, NPCs, enemies, bosses, sharks |
| ObjectWaterMovement | Jolt dynamic body \+ BuoyantBody | Follows current; self-propulsion may be zero | Crates, debris, drifting wreckage, lost cargo |
| WatercraftMovement | Jolt dynamic body \+ BuoyantBody | Current plus propulsion, sails (wind), steering and braking | Boats, ships, rafts |
| Custom movement | Engine extension point | Defined by its policy | Future special vehicles |

```text
AnchoredFloatingPlatform : Transform, JoltDynamicBody, BuoyantBody
                           (floats, does not follow current)
DriftingCrate            : Transform, JoltDynamicBody, BuoyantBody,
                           ObjectWaterMovement (self velocity 0, current coupling > 0)
MerchantShip             : Transform, JoltDynamicBody, ShipTag, BuoyantBody,
                           WatercraftMovement
Player                   : Transform, CharacterVirtual, CharacterTag,
                           CharacterMovement, CharacterWaterMovement
```

Tags such as ShipTag and CharacterTag classify entities but never select behavior: a floating crate is not a ship, and a future magical floating vehicle can use BuoyantBody with a different movement component.

### Characters, ships, objects and bosses

**Characters swim, they do not float as rigid bodies.** CharacterWaterMovement owns the character version of floating, swimming acceleration, vertical swimming, drag, surface behavior and current influence, and feeds desired motion into the CharacterVirtual.

```cpp
struct SwimProfile {
    float max_speed, vertical_speed, acceleration, deceleration;
    float passive_float_strength;   // humanoids drift up; sharks 0
    float sink_speed;               // heavy armor sinks faster
    float water_drag;
    float current_influence;
};

struct WaterInteractionState {      // written once per tick, read by everyone
    WaterBodyId body;
    float submerged_fraction;
    bool  feet_submerged;
    bool  swimming;
    bool  head_submerged;           // the Game drives breath from this
};
```

WaterInteractionState lets animation, audio, combat, UI and Game rules read water facts without each issuing its own query.

**Watercraft** combine player or AI intent with the local flow and the local wind, then apply forces and torques to the Jolt body. Downstream is naturally faster than upstream, and a sailing ship depends on the wind angle. The Engine never knows what a ship carries or who owns it. WatercraftMovementProfile gains lateral\_current\_influence: current\_influence scales the flow along the hull and lateral\_current\_influence the flow across it, so a ship class can barely drift in side currents. Draft needs no new field: a hull's collision shape reaches down to its keel, so the seafloor, reefs and sandbanks touch it only where they are shallower.

```cpp
struct WatercraftMovementProfile {
    float propulsion_force;         // oars, engines, magic
    float reverse_force;
    float steering_force;
    float braking_force;
    float current_influence;
    float sail_force;               // 0 = no sails; scaled by wind (see Environment)
    CurveId sail_angle_curve;       // efficiency by angle between wind and heading
    float lateral_resistance;       // keel: resists sideways drift from wind
};

struct ObjectWaterMovementProfile {
    float self_propulsion   = 0.0f;
    float current_influence = 1.0f;
};

struct SwimMovementModifiers {      // temporary boss charges, buffs
    float speed_multiplier = 1.0f, acceleration_multiplier = 1.0f;
    float turn_multiplier  = 1.0f, current_influence_multiplier = 1.0f;
};
```

**Water bosses** stay Characters to the movement system: a SwimProfile with very high speed, acceleration or turn authority, and AI intents such as circle, dive, charge, breach or retreat. The Engine executes the swimming; the Game decides why and when.

### Boundaries with the rest of the Engine

| Boundary | Rule |
| :---- | :---- |
| Jolt | Jolt owns collision, integration, mass, contacts and dynamic ship motion. Buoyancy and watercraft systems turn samples into forces before the Jolt step; CharacterWaterMovement turns them into desired motion for the CharacterVirtual. |
| Flecs | River samples, vector-field cells and water tiles are never entities. Flecs holds WaterInteractionState, profile references, movement components, dynamic modifiers, AI intent and tags. |
| Scheduler | Buoyancy and water movement run in the 30 Hz realtime phase, step 4, before the Jolt step. Static water never ticks; tide and weather state update at 10 Hz in the Environment. |
| Movement and handoff | Ships carry passengers on deck because CharacterVirtuals update every tick on moving bodies. A ship hands off as a group with its passengers and cargo in one authority epoch. |
| Light and perception | Each water body may define underwater light attenuation by depth (Game values); luminosity and visibility use it like any ambient profile. |
| AI | Sea creatures use CharacterWaterMovement; AI intents are executed by the same movement as players. |
| Audio | WaterInteractionState drives water sound events; the Game’s presentation picks the sailing music context. |
| Presentation | The WaterSystem never calls Godot. Presentation extracts water render data; Godot adds all visual detail. |
| Network | Static water ships in cooked world packages and is never replicated per tick. Replication carries only dynamic changes: flow multipliers, water-level offsets, lock or dam state, temporary current modifiers, world-event changes. |
| Persistence | Durable water state is stored by a Game service on the Platform Go SDK and reaches the simulation through the service port when the owning region loads. |

| Server and runtime water data | Client presentation additions |
| :---- | :---- |
| Spline and planar surface samples | Render surface mesh and LODs |
| Bounds and spatial fragments | Water material and shader parameters |
| Depth and flow representation | Normal maps, foam, visual flow maps |
| Connections and navigation metadata | Reflection and refraction parameters |
| Dynamic gameplay state | Particles, spray, wakes |

### Streaming, caves and cross-simulation continuity

* **Fragments follow cells:** World, Region, Sector, Cell, then the cell’s cooked water fragments. A simulation loads only the fragments of its own space; a 50 km river is never resident everywhere.

* **Rivers enter caves without instances:** a surface river enters a cave volume and becomes an underground river that reaches an underground ocean, as one logical route with no teleport or loading screen.

* **Seams:** the Cooker emits fragments with boundary aprons from the same source spline, so position, width, depth, tangent, normal and flow agree across region and cell boundaries.

* **Cross-simulation ships:** water is static data, not transferred in a handoff. Neighbor simulations load matching fragments, and the ship moves with the make-before-break protocol, prepared before authority commits.

* **Open ocean** is analytic inside the OceanWaterBody’s bounds; only coastlines, current fields and special areas are cooked, so huge seas cost almost no storage.

### Authoring and cooking

Water is authored in the RunicEditor inside region scenes: rivers as RunicWaterBody3D nodes on a Path3D curve, lakes and oceans as bounded surfaces or volumes, waterfalls as connection and flow-volume markers, and current and wind maps as vector layers painted with a Runic editor tool. The shipping runtime never loads editor scenes; the Cooker turns them into fragments.

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

* Resolve WaterConnections.

* Split into Region, Sector and Cell fragments.

* Generate boundary aprons.

* Emit client water data (surfaces for the presenter).

* Emit server water assets.

Terrain coupling — carving the channel, riverbed and bank masks, wetness, vegetation and shoreline data — happens at cook time. At runtime, terrain and water are already cooked. A river is a gizmo-edited curve in the viewport, and the “see what the server sees” layer draws the cooked centerline, widths and flow arrows over it.

### Performance

* A loaded river with nobody interacting does essentially no work per tick; cost scales with active consumers, not kilometers of water.

* Ship and character water movement run at 30 Hz with the rest of movement and physics.

* A vessel samples a few buoyancy points (typically 4 to 8), one or two flow samples and one wind sample per tick; with cell filtering and cached locality these are small interpolations, so hundreds of vessels cost far less than any fluid simulation.

* Lakes and rivers keep a flat or smoothly sloped authoritative surface with client-only visual waves; oceans with naval play use the deterministic gameplay swell (see [[Environment wind, currents, tides, waves and weather (Engine)|Environment]]), which does not change this API.

### Debugging and validation

* **Debug drawing:** body bounds and loaded fragments; river centerlines and sampled surface points; width and depth cross sections; flow arrows, vector-field cells and FlowVolumes; the connection graph and navigation rules; buoyancy points, submersion and applied forces; each character’s WaterInteractionState and body; cell and simulation ownership at fragment boundaries; query counts, cache hit rate and active consumers.

* **Cooker validation:** zero or negative width, invalid depth, unintended spline self-intersection, large elevation jumps in a Smooth connection, missing or dangling connection references, neighbor boundary mismatches, a waterfall modeled as a smooth navigable surface without a FlowVolume, invalid route topology, duplicate IDs.

* **Extension points stay small:** planar, ocean, spline river, flow volume, BuoyantBody and the three movement components. New provider interfaces are added only when a real feature needs them.

### Implementation stages

| Stage | Contents |
| :---- | :---- |
| A. Vertical proof | WaterSystem registry and sampling; planar water and one descending spline river; fragment registration in cells; four-point BuoyantBody on a Jolt body; current-only ObjectWaterMovement; basic WatercraftMovement; CharacterWaterMovement; basic editor authoring (RunicWaterBody3D); debug drawing of centerline, surface and current |
| B. Generalize | Connections, river-to-ocean blending, rapids and waterfalls; ocean current fields; profiles and stable IDs; client and server package split; incremental water cooking; dynamic water-level state; WaterInteractionState for animation, audio and gameplay; navigation metadata; ocean gameplay swell, wave events (big waves, whirlpools) and the righting strength |
| C. Production | Large fleet profiling and telemetry; tides, locks and stateful waterways; advanced rendering, shoreline foam and wakes; water navigation graph and AI vessel routes; cross-simulation stress tests on long waterways |

**Definition of done for the first water slice:** author a descending river in the RunicEditor and cook it; stream it across at least two cells with no seam; render it on the client and sample its surface and current on the server; a boat with BuoyantBody and WatercraftMovement travels downstream faster than upstream; a BuoyantBody-only object floats without drifting; a crate with ObjectWaterMovement drifts with zero self-propulsion; a character swims with current influence and no rigid-body buoyancy; the river enters a cave volume continuously and reaches an underground lake or ocean without a teleport or instance; repeated with two networked clients, ship and character transitions stay continuous.
