---
title: "Environment: wind, currents, tides, waves and weather (Engine)"
tags:
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

Wind, time-varying currents, tides, gameplay swell and weather are deterministic functions of world time, position and a small replicated weather state. Every simulation and every client computes the same environment from the same inputs, so nothing about it is replicated per tick; the Game supplies the patterns and decides what they mean.

### Ownership

| Part | Owner | Contains |
| :---- | :---- | :---- |
| EnvironmentClock | Engine | Shared world time and what derives from it: time of day, tide phase, season, weather schedule steps |
| WindField | Engine | Cyclic baseline routine (direction at any angle, signed speed), cooked regional wind maps, altitude profile, deterministic gusts, wind volumes, weather scaling |
| Current modulation | Engine | Time variation of ocean current fields by a cyclic baseline routine, tide phase, season and weather; whirlpools as local current overrides |
| TideSystem | Engine | Water-level offset over time per water body or route |
| WaveField | Engine | Deterministic gameplay swell, required on oceans with naval play and scaled by weather; big-wave events from overrides |
| WeatherState | Engine | Per-region weather parameters, transitions, the baseline schedule evaluator and time-boxed overrides |
| Patterns and meaning | Game | Wind and current maps, tide profiles, day and season lengths, weather types and tables per region and season, storm effects, which abilities wind affects |
| Special weather decisions | Game | A Go world-events game service decides storms and other overrides |
| Override delivery | Platform | World directives (PCS-3) with an effective time and a duration, delivered through the services bridge to every simulation owning the affected regions |

### Environment clock

* World time counts from a world epoch the World Coordinator issues (read from configuration until PCS-2 ships in slice 36); each simulation derives it from its synchronized clock at start, advances it with the fixed-step master clock and corrects drift slowly.

* Clients receive world time at connection and in snapshots, so they evaluate the same functions as the server.

* Time of day (which drives ambient light), tide phase, season and the weather schedule step are all derived from world time; day length and season length are Game data.

### Wind

Wind at a position is composed of: the region’s baseline routine (a direction at any angle and a signed speed that cycle with world time), a cooked regional wind map (a coarse vector grid, e.g., one vector per 512 m), an altitude profile (stronger at height, zero inside sheltered volumes such as caves), the region’s weather multiplier, deterministic gusts (seeded noise that is smooth over time) and authored wind volumes such as updrafts and downdrafts.

A routine speed of 0 has no effect, and a negative speed reverses the push abruptly without changing the angle. Over the ocean the Game lets characters only glide, carried by this wind: gliding against it is impossible and pushes the character back.

```cpp
// Illustrative contract, not a frozen API.
struct WindSample {
    Vec3  velocity;      // m/s, world space
    float gust;          // 0..1, current gust strength
    float turbulence;    // for control noise and visuals
};
```

| Consumer | Uses wind for | Engine part | Game part |
| :---- | :---- | :---- | :---- |
| Sailing ships | Sail thrust by angle; sideways drift | WatercraftMovement sail model | Sail force, angle curve, keel resistance per ship class |
| Gliders and gliding mounts | Drift and lift from updrafts; over the ocean the wind carries gliders, and gliding against it is impossible | Glide movement mode | Glider and mount stats; updraft placement |
| Flying mounts and vehicles (flight zones) | Headwind and tailwind | Vehicle movement mode | Vehicle stats |
| Projectiles | Off by default; optional drift | Per-ability wind flag | Which abilities set it (e.g., cannonballs in storms) |
| Client visuals | Sails, flags, foliage, clouds, particles, rain direction | Render extraction | Art |
| Audio | Wind loops by intensity | Audio events | Sound design |
| Nautical charts | Prevailing wind overlay | Cooked wind maps | Chart items |

The sail model uses the apparent wind (wind minus ship velocity). Thrust is zero straight into the wind and peaks at the angles the Game’s curve chooses; the keel’s lateral resistance limits sideways drift.

$${F}_{sail}=s\times {\left|{{w}_{app}}\right|}^{2}\times \eta \left({\theta }\right)$$

s \= the ship’s sail force; w\_app \= apparent wind; θ \= angle between apparent wind and heading; η \= the Game’s efficiency curve.

### Currents over time

The base current comes from the water body (river profile, vector field or ocean current field). The Environment modulates it with a tidal term, a seasonal factor, the weather’s current multiplier and any active override:

$$c\left({p,t}\right)={c}_{0}\left({p}\right)\times \left({1+a\left({p}\right)\,sin\left({{\phi }_{tide}\left({t}\right)+\delta \left({p}\right)}\right)}\right)\times {k}_{season}\left({t}\right)\times {k}_{weather}\left({p,t}\right)$$

c0 \= cooked base current, which follows the same cyclic baseline routine model as wind; a and δ \= cooked tidal amplitude and phase offset; k \= Game-defined factors. WaterSample.flow\_velocity already contains the result.

### Tides

* A TideProfile (Game data) per water body or route sets period, amplitude and phase, or a custom curve; the water-level offset follows world time.

* Sampling includes the offset automatically, and estuaries blend river and sea levels.

* Terrain stays static, so low tide exposes walkable ground (tidal paths) and high tide turns it back into water where characters swim.

* Ships can ground in shallows at low tide; Jolt collision handles it and the Game decides warnings or damage.

### Waves

* Lakes and rivers keep a flat or smoothly sloped authoritative surface, with visual waves only on the client. Oceans with naval play always enable the WaveField, because ship damage and flooding read the real sea height.

* The WaveField is a sum of a few (e.g., 3 or 4\) deterministic swell components, amplitude scaled by weather, evaluated identically by the server (buoyancy points) and the client (rendering and prediction). Each sample costs a few sine evaluations.

* Visual detail beyond the gameplay swell never affects gameplay.

* Big waves are wave events: a local, traveling component added to the WaveField for a short time (position, direction, height, speed and start time), delivered as an Environment override. They are only slightly telegraphed, and every simulation and client evaluates them the same way, so the server knows which ships a big wave hits and from which side.

* Whirlpools are local current overrides (center, radius, inward and tangential strength, duration) that pull ships and swimmers toward the center.

* Water-line tests need no new API: WaterSystem::TrySample at any point already includes tide, swell and wave events, so the Game can tell whether a point on a moving hull is under water.

* Floods add a flood layer with a stage per channel stretch; TrySample still answers with one WaterSample (see [[RunicGame systems (Game)#Land hazards|Land hazards]]).

### Weather

* **WeatherState per region:** weather type (Game ID), intensity 0–1, wind multiplier, wave amplitude, precipitation, fog density, ambient light multiplier, current multiplier and transition progress.

* **Baseline schedule:** evaluated from the world seed, region, season and world time against Game weather tables, so every simulation and client agrees without messages.

* **Overrides:** special storms and magical weather are decided by a Game Go service and sent through Platform directives with an effective world time a few seconds ahead and a duration, after which the baseline returns, so every owning simulation applies them on the same tick. Clients receive the override once as a reliable fact. Storm lightning strikes are server events that the owning simulation picks from the weather type's strike rate and replicates as events (position and time); the Engine answers which entity is the highest point near a strike and which characters are in the water within a radius, and the Game applies the effects.

* **No weather or wind inside sheltered volumes (caves and underground spaces)**; light there comes only from ambient profiles and emitters.

| Weather effect | Connects to | Owner of the rule |
| :---- | :---- | :---- |
| Darker sky in storms | Ambient light, and through it perception radii and visibility tiers | Engine computes, Game sets values |
| Stronger wind and waves | Sailing, gliders, gameplay swell | Engine computes, Game sets values |
| Stronger or reversed currents | Water sampling, ships, swimmers | Engine computes, Game sets values |
| Fog | Client rendering; optionally a smaller PvP visible range | Game decides |
| Rain, thunder, lightning | Client visuals and audio; lightning strikes are also gameplay events (Game rules) | Game presentation |
| Creature behavior | AI rules (e.g., sea creatures surface in storms) | Game |

### Routines, events and world routines

* **Cyclic routines.** Wind and sea currents follow a baseline routine that cycles with world time and the world seed, so it is mappable: the Game’s cartographers chart it.

* **Operator events.** An operator panel in the Game’s world-events service schedules events that change wind or currents for a duration. They travel as Platform world directives with an effective time and a duration (PCS-3, ENV-5), and the baseline returns when they end. A high-proficiency chart syncs with the current state; a maximum-proficiency chart sees scheduled events. Proposal: each event defines from when it can be predicted.

* **World routines (ENV-6).** Escorts, trade routes, ships and mob routines use the same model: cooked routes and schedules, with position \= f(route, world time, seed). A cycle that does not match the clock plus a small seeded variation makes routines drift slowly and deterministically.

* **No simulation of empty areas.** When a cell activates, routine entities spawn where their routine puts them (GPL-8), so an NPC is at the right point when a player arrives.

* **Exceptions only.** A Game service stores only player-caused exceptions, such as a delayed escort, and each exception fades back into the routine over time (GSVC-9).

### Determinism, replication and handoff

* Every environment value is a pure function of position, world time, weather state and cooked fields, implemented once in Engine code that both client and server run.

* Replicated: world time (at connection and periodically), weather, wind and current overrides (reliable facts) and dynamic water states (locks, dams, magical currents). Never per-tick wind, current or wave values.

* Bit-exact agreement is not required: the server is authoritative and client prediction is corrected like any other.

* Neighboring simulations compute identical values at a border, and overrides reach every owner of the affected regions, so ships and gliders cross boundaries without a jump.

### API

```cpp
// Illustrative contract, not a frozen API.
struct WeatherSample {
    WeatherTypeId type;
    float intensity, wind_multiplier, wave_amplitude;
    float precipitation, fog_density;
    float ambient_light_multiplier, current_multiplier;
};

class Environment {
public:
    WorldTime    Now() const;
    TimeOfDay    TimeOfDayAt(WorldTime t) const;
    float        TidePhase(WaterBodyId body, WorldTime t) const;
    float        WaterLevelOffset(WaterBodyId body, WorldTime t) const;
    WindSample   SampleWind(const WorldPosition& p, WorldTime t) const;
    WeatherSample SampleWeather(RegionId region, WorldTime t) const;
    float        WaveHeight(WaterBodyId body, const WorldPosition& p, WorldTime t) const;
    RoutineSample SampleRoutine(RoutineId routine, WorldTime t) const;   // world routines (ENV-6)

    // From a Platform directive; takes effect at override.effective_time.
    void ApplyOverride(const EnvironmentOverride& override);
};
```

The WaterSystem calls the Environment internally for tide offsets, current modulation and swell; the Light API calls it for time of day and weather light; gliders and watercraft call SampleWind.

### Performance

* Each sample is an interpolation in a coarse cooked grid plus a few sine evaluations: constant cost, safe in parallel phases.

* The Environment’s own update runs at 10 Hz and only advances weather transitions and per-region caches.

* Memory: wind and current maps at 512 m need about 2,300 vectors each per 600 km² map. A continent-scale world of 1,000,000 km² needs about 3.8 million vectors per map (about 30 MB), streamed by sector so only nearby parts are resident.

* Network cost is near zero: world time, rare overrides and dynamic water states only.

### Acceptance tests

| Test | Passes when |
| :---- | :---- |
| Same wind everywhere | Two simulations and two clients sample identical wind at a shared border at the same world time |
| Sailing angles | A sailing ship gains speed at favorable wind angles and none straight into the wind, matching its Game curve |
| Leeway | A crosswind pushes a ship sideways in proportion to its lateral resistance |
| Tidal path | At low tide a tidal path is walkable; at high tide characters swim there |
| Storm override | A storm from the Game service applies on the same world time in two simulations; wind, waves and light change; clients follow without per-tick data |
| Updraft | A glider gains altitude crossing an authored updraft volume |
| Cave volume | Wind and weather sample as calm inside a cave volume; light comes only from ambient profiles and emitters |
| Projectile flag | Arrows ignore wind unless their skill sets the wind flag |
