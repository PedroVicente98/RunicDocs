---
title: "Godot integration (Engine)"
tags:
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-13"
---

Godot enters the Engine as a library (LibGodot) in two roles: renderer, window, input, audio and player UI inside the client, and the authoring editor inside the RunicEditor. The simulation, networking, world, Platform and services of v3 do not change, the server never links Godot, and the RenderFrame is the only door from the Runic client into Godot.

### Role of Godot (decided)

| \# | Decision | What it means |
| :---- | :---- | :---- |
| 1 | Godot via LibGodot from slice 0 | It is in the first build, even idle or headless, and every slice pulls one piece of presentation or tooling into it |
| 2 | Godot is interface and renderer only | Authoring editor, rendering, window, input, audio and UI; it never runs a game rule |
| 3 | The server has no Godot | GameServer stays purely headless, as in v3 |
| 4 | The RenderFrame is the only door | Godot never reads Flecs, Jolt or domain modules; only GodotBridge talks to it |
| 5 | Prediction runs in the Runic simulation | The client predicts with Flecs, Jolt in double precision and RunicGame::Shared, the same code as the server |
| 6 | No gameplay nodes; GDScript out of the game | Nodes exist only for authoring (marker nodes) and player UI; no game entity is a node; GDScript is an editor tool language only |
| 7 | Godot built from source with modules removed | No fork; small documented patches only if something requires one |
| 8 | The Engine is not a plugin | Runic code talks to Godot through the GDExtension API (godot-cpp) compiled into Runic executables; only the game’s own editor code is a loaded library |
| 9 | The Engine is game-agnostic | The RunicEditor opens with no project and offers New project (from a template) and Open |
| 10 | Runic nodes are representation only | Spawn areas, volumes, interactables, water and colliders exist in the editor; the Cooker writes placements and the Engine creates everything by its own rules |
| 11 | One source, two outputs | The Cooker writes server and client packages from the same scenes; the client’s visual assets come from Godot’s importer and export |
| 12 | Player UI in Godot | Godot UI scenes (Control), including diegetic panels; nameplates and damage numbers on the batched path |
| 13 | Code in an external IDE, assistants in the editor | No embedded code editor; New Flecs system, New Go service and similar assistants generate the files |
| 14 | One Run button | It compiles what changed, cooks, keeps the local stack running and connects a development client |

![[arch-godot-in-the-editor-and-the-client-the-server-neve.png]]
*Godot in the editor and the client — the server never sees it*

*Godot in the editor and the client — the server never sees it*

The editor cooks one source into two outputs: the server runs without Godot, and on the client Godot only receives the RenderFrame the Runic runtime produces.

### Executables and Godot targets

Godot is one source tree compiled as a library in two targets: **editor** (the editor, importers and project manager) and **template** (runtime only: rendering, audio, input and resource loading). Each executable links the target it needs; the server links none.

| Executable | Built by | Godot | Runs |
| :---- | :---- | :---- | :---- |
| GameServer | The project’s CMake | None | Engine (simulation, network, world) \+ RunicGame::Server \+ RunicGame::Shared; the v3 server layers |
| GameClient (shipping) | The project’s CMake | Template target | Engine (network, prediction, extraction) \+ RunicGame::Client \+ RunicGame::Shared; reads the exported .pck |
| GameClient (development) | The project’s CMake | Editor target | The same client reading the project folder directly, without export, as Godot’s own play button does |
| RunicEditor | The Engine distribution | Editor target | The Godot editor \+ Runic tools (GodotTools) \+ the Cooker; loads the open project’s editor library |
| Cooker on build machines | — | Editor target, no window | The RunicEditor in headless mode with cook and export arguments |
| RunicBot | The Engine | None | The client runtime without presentation, many bot sessions per process, for scale tests |

```text
GameServer  = Engine (sim, network, world) + Game::Server + Game::Shared
              → no Godot

GameClient  = Engine (network, prediction, extraction) + Game::Client + Game::Shared
              + libgodot → window, rendering, input, audio, UI
              prediction in double → RenderFrame in float → Godot

RunicEditor = libgodot (editor) + Runic tools + Cooker
              + the open project's editor library
```

The inversion that organizes everything: **Godot does not use the client; the client uses Godot.** Inside the client, Godot does not know an MMO exists. It receives RenderingServer calls from the presenter, the UI scenes and the sounds. The “Godot renderer” is the same RenderingServer in both executables: in the editor it draws the authoring viewport, in the client the game.

### How the Engine uses Godot

The Engine uses Godot’s lower layers (servers and ClassDB) and its editor; the scene tree is used only for authoring and player UI.

| Godot layer | What it is | Use in Runic |
| :---- | :---- | :---- |
| Servers | Low-level APIs with handles (RID): RenderingServer, AudioServer, DisplayServer | The presenter draws directly in the RenderingServer; audio plays on the AudioServer; the window comes from the DisplayServer |
| Object and ClassDB | Reflection: every registered class exposes methods, properties and signals to the editor | Marker nodes and data types get an inspector, saving and undo for free |
| Node and SceneTree | A tree of objects with a lifecycle; a scene (.tscn) is a saved subtree | Authoring maps and player UI screens; never a game entity |
| Resource | A data asset with a stable UID, saved as .tres, .res or a custom format | Imported meshes, materials and textures; Runic data files enter through ResourceFormatLoader and ResourceFormatSaver |
| Editor API | Docks, inspector plugins (EditorInspectorPlugin), 3D gizmos (EditorNode3DGizmoPlugin), import and export plugins, undo and redo | Runic tools, the Cooker, attach docks and data editors |
| GDExtension and godot-cpp | Godot’s C interface and the official C++ wrapper; registration by levels (core, servers, scene, editor) | How all Runic code talks to Godot |
| LibGodot | Godot as a library: the host’s main creates the instance, calls start() and then iteration() once per frame | GameClient and RunicEditor; one instance per process, desktop platforms only |

Registration happens in an init function the executable hands to LibGodot. Authoring and UI classes register at the scene level; editor plugins only at the editor level, which the client never reaches.

```cpp
// Illustrative contract, not a frozen API.
void RegisterRunicClasses(godot::ModuleInitializationLevel level) {
    using namespace godot;
    if (level == MODULE_INITIALIZATION_LEVEL_SCENE) {
        ClassDB::register_class<RunicVolume3D>();
        ClassDB::register_class<RunicSpawnArea3D>();
    }
    if (level == MODULE_INITIALIZATION_LEVEL_EDITOR) {     // RunicEditor only
        ClassDB::register_class<RunicEditorPlugin>();
        EditorPlugins::add_by_type<RunicEditorPlugin>();
    }
}
```

Registering a property is what makes it appear in the inspector, save with the scene and support undo:

```cpp
class RunicVolume3D : public godot::Node3D {
    GDCLASS(RunicVolume3D, godot::Node3D)
    bool indivisible = false;
protected:
    static void _bind_methods() {
        using namespace godot;
        ClassDB::bind_method(D_METHOD("set_indivisible", "v"), &RunicVolume3D::set_indivisible);
        ClassDB::bind_method(D_METHOD("get_indivisible"), &RunicVolume3D::get_indivisible);
        ADD_PROPERTY(PropertyInfo(Variant::BOOL, "indivisible"), "set_indivisible", "get_indivisible");
    }
public:
    void set_indivisible(bool v) { indivisible = v; }
    bool get_indivisible() const { return indivisible; }
};
```

In the client, the presenter talks directly to the RenderingServer, with no node per entity:

```cpp
auto* rs = godot::RenderingServer::get_singleton();
godot::RID inst = rs->instance_create2(meshRid, scenarioRid);   // once, when the entity appears
rs->instance_set_transform(inst, xform);                       // only when it moves
rs->free_rid(inst);                                            // when it leaves interest
```

### Projects: create, open and the game’s editor library

The Engine is distributed ready to use and knows no game: the RunicEditor opens with no project, creates a new one from a template or opens an existing one. RunicGame is one such project.

```text
RunicEngine/ (distribution)
  bin/        RunicEditor, libgodot (editor and template targets), Cooker tools
  sdk/        Engine headers and libraries (Core, Simulation, Network, Client, GodotBridge…) + godot-cpp
  templates/  runic-mmo/  (the new-project template)
  platform/   Go SDK and Platform core services

MyGame/
  project.godot             ← what Godot opens
  runic.project.json        ← Runic manifest: Engine version, paths, executables, cook settings
  game_editor.gdextension   ← loads the game's editor library
  Content/                  ← assets, world and region scenes, UI scenes (Godot imports these)
  Data/                     ← schema-backed definitions: skills, items, AI, quests, spawn rules
  Tools/                    ← editor tools in GDScript (never reach the client)
  Source/    (.gdignore)
    Shared/ Server/ Client/ ← the game's C++: Flecs systems, rules, behaviors
    Editor/                 ← the game's marker nodes and docks
  Services/  (.gdignore)    ← Go: the game's services on the Platform SDK
  Build/     (.gdignore)    ← binaries and cooked packages
  CMakeLists.txt  go.work
```

An empty .gdignore file keeps a folder out of Godot’s importer, so code and binaries never clutter the asset panel.

```json
{
  "runic": 1,
  "engine": "0.4.0",
  "game": { "name": "RunicGame" },
  "paths": { "content": "Content", "data": "Data", "source": "Source",
             "services": "Services", "cooked": "Build/Cooked" },
  "executables": { "server": "RunicGameServer", "client": "RunicGameClient" },
  "cook": { "world": "Content/World.tscn", "cellSizeM": 64, "clientPck": "Build/Client/game.pck" }
}
```

1. The RunicEditor opens in Godot’s project manager, with **New** and **Open**.

2. **New** copies templates/runic-mmo/ and creates the whole layout above. How the project manager offers it is an open decision: a small patch in the project manager, or a Runic plugin that offers to initialize an empty project.

3. **Open** loads an existing project. The project manager opens a project by relaunching its own executable with –path; with LibGodot that executable is the RunicEditor, so its main passes the arguments to Godot unchanged.

**The game’s editor library.** A distributed RunicEditor cannot have a game’s C++ compiled in. The game’s marker nodes and docks (Source/Editor) become a library of the project, loaded by the editor through Godot’s GDExtension mechanism, which reloads it with the editor open. The Engine lives inside the RunicEditor; the game enters through this library, the same model as Unreal’s generic editor plus project module.

; game\_editor.gdextension, at the project root  
\[configuration\]  
entry\_symbol \= "game\_editor\_init"  
compatibility\_minimum \= "4.6"  
reloadable \= true

\[libraries\]  
windows.editor.x86\_64 \= "res://Build/bin/game\_editor.dll"  
linux.editor.x86\_64   \= "res://Build/bin/libgame\_editor.so"

The game’s server and client do not load libraries this way: the project’s CMake builds them against the Engine sdk/, like the v3 executables.

### Game code and the Run button

Game code is always compiled before it runs, and Godot never executes it. The Run button compiles what changed, cooks what changed and starts the processes; most iteration is data and never compiles.

| Written in | Becomes | Runs in |
| :---- | :---- | :---- |
| Source/Shared (rules and shared Flecs systems) | C++ compiled into both executables | The server with authority, the client for prediction |
| Source/Server (AI, quests, loot, server rules) | Part of the server executable | Server only |
| Source/Client (view models, game presentation) | Part of the client executable | Client only |
| Source/Editor (game marker nodes and docks) | The editor library, loaded and reloaded by the editor | Editor only |
| Services/ (Go) | Service binaries | Next to the server |
| Data/ and Content/ | Nothing to compile: cooked, or reloaded live | Read by server and client |

**External IDE and assistants.** C++ and Go are written in an external IDE. The editor generates what the IDE needs (compile\_commands.json for clangd, go.work, VS Code tasks and launch configurations), and a build error in the editor opens the file at its line. Assistants generate template files, register them in CMake or the right registry and open the result in the IDE: **New Flecs system**, **New behavior**, **New quest condition or action**, **New AI node**, **New data type** (a schema), **New marker node** and **New Go service**. Each costs days, the same flow as Unreal’s “New C++ class”.

**What Run does:**

1. Saves and cooks only the changed cells and definitions.

2. Compiles if code changed, with the same CMake the IDE uses, incrementally.

3. Keeps the local stack up: Platform services and the game’s Go services keep running between runs; only a service whose code changed restarts.

4. Starts the local server with the freshly cooked packages.

5. Starts the development client, already connected as one of your characters (or several clients).

RunicGameClient \--project . \--connect 127.0.0.1:7777 \--dev-ticket Build/dev.ticket \--character dev1

| Change | What happens | Typical time (estimate) |
| :---- | :---- | :---- |
| Data (skill, quest, behavior tree) | Reloads in the running server | Under 1 s |
| Map or asset | Cooks the affected cells and reloads them | A few seconds |
| One game .cpp | Recompiles, relinks and restarts the local server | 10 to 40 s, mostly linking |
| One Go service | go build and a restart of that service only | 2 to 10 s |
| The editor library | Recompiles and reloads inside the open editor | 10 to 30 s |

A server restart loses simulation state, but durable state stays in the services. A development checkpoint on stop returns you exactly where you were, with quests and inventory.

**Login and scenes.** Godot scenes are the UI of the v3 client states: Boot → Login → Server and character select → Loading → World. The Runic client owns the transitions (each state replaces its presentation layer, which shows its Godot UI scene). Login runs inside the client: the screen is Godot’s, the call to the accounts service is Runic code; a separate patching launcher is optional. The world is not a Godot scene: the World state shows the HUD scene while the presenter draws the cells and entities the server sends. Character creation uses a small 3D scene for the model; the data goes to the character service. In development, Run skips the screens with a ticket signed by the local key; to test login itself, run from the login screen.

### Building Godot

Godot enters as a submodule pinned to a release tag and is built from source in CI, in both targets, with every module off by default and only a list switched on. There is no fork: Godot ships a minor version every four to six months, and each would cost days of merging. If something can only be solved with a patch, such as hiding a menu, a few small documented patches sit on top of the tag.

|  | Client (template target) | Editor (editor target) |
| :---- | :---- | :---- |
| Kept | Rendering, audio, input, text server and fonts, texture and audio decoders for the .pck | Everything the client keeps, plus importers (glTF, images, fonts), the editor’s SVG icons and regex |
| Removed | GDScript, C\#, 2D and 3D physics (including Godot’s own Jolt), navigation, high-level multiplayer, WebRTC, WebSocket, XR | The same; GDScript returns at the tools phase (see [[Godot integration (Engine)#GDScript editor tools only\|GDScript]]) |
| Fine trim | A build profile generated by the editor with the classes the project uses | — |

Removing Godot’s physics also removes the risk of two Jolt copies in one process. Nodes are never removed: the editor and the viewports are made of them; the game only never uses them as entities.

\# custom.py for the Godot build (sketch; exact names to confirm on the pinned version)  
library\_type \= "shared\_library"          \# Godot as a library (LibGodot)  
modules\_enabled\_by\_default \= "no"       \# everything off  
module\_freetype\_enabled \= "yes"         \# then only the target's list  
module\_text\_server\_adv\_enabled \= "yes"  
\# … the rest of the client or editor list  
build\_profile \= "runic\_client.gdbuild"  \# unused classes out (template target only)

The first step of the slice 0 spike is to list the modules/ folder of the pinned version and write both lists. Without a cache a Godot build takes tens of minutes; with the SCons cache in CI only what changed recompiles. Module names change between versions, so the lists are reviewed at every Godot update, which is a decision with tests.

### GDScript: editor tools only

GDScript never runs in the game, for any game made on the Engine: the server has no Godot, and prediction needs the same C++ on both sides. It starts switched off and returns at the tools phase, only in the editor and behind locks.

1. **Slices 0 to 19:** the module is off in both targets.

2. **Slices 20 and 21** (content pipeline): it returns in the editor target together with the locks below; the client stays without it.

3. **Reversible:** switching it back on is a build option, and no content ever depends on it.

| Worth it | Examples |
| :---- | :---- |
| Procedural content generation | Scattering decorative vegetation and rocks, roads and rivers along curves, cliffs, village layouts |
| Import post-processing | Materials, the collision naming convention, LODs and Runic metadata when a glTF is imported |
| Batch operations | Renaming assets, swapping materials on hundreds of meshes, rendering item icons |
| Map validation | Floating rocks, interactables without an ID, overlapping volumes, a region without spawns |
| Utilities and visualizations | A spawn-density brush, heat maps, wind and route previews |
| Tool prototypes | Trying an idea before writing it in C++ in GodotTools |
| Community plugins | Generators and scatterers from Godot’s asset library |

| Not worth it | Why | Instead |
| :---- | :---- | :---- |
| Movement, combat, AI, quests, economy | The server has no Godot; prediction needs the same code on both sides | C++ in RunicGame::Shared and RunicGame::Server |
| Camera, input, UI logic | The client is built without GDScript | C++ in RunicGame::Client, view models and the binder |
| Visual-only behaviors | The same reason | Shaders, animations and presentation code |

Rule of thumb: GDScript is a tool of the project; a tool the Engine ships, or one that must be fast on large maps, is C++ in GodotTools.

| Layer | GDScript | How it is enforced |
| :---- | :---- | :---- |
| Server | Does not exist | No Godot; the Cooker writes only data |
| Shipping client | Cannot run | Built without the module: the final wall |
| Export | Blocked | The validator refuses scripts in anything bound for the .pck; the preset excludes Tools/, addons/ and \*.gd |
| Development client | Blocked on load | It uses the editor target, so the module exists in it; every scene it loads runs the export check and stops with an error |
| Godot’s “run scene” button | Intercepted | Godot runs a scene by relaunching its own executable; the RunicEditor’s main recognizes that mode and calls Runic’s Run instead, with no patch |
| Editor | Tools only | @tool scripts, EditorScript and plugins; a script without @tool in a content scene raises a warning |

The development client and Godot’s play button are the gaps that are not obvious: without those two locks a script would work when run from the editor and break only at export. All the locks are estimated at three to four weeks, spread over the tools phase.

**Clarity for the people using the Engine:**

1. The easy path is the right one: the assistants answer “I want to program gameplay”; Godot’s New script uses project templates (script\_templates/) that start as @tool with a two-line header explaining the rule.

2. Folders carry meaning: Tools/ is where GDScript lives; Source/ is where the game lives.

3. A problems dock lists violations on every save.

4. Messages teach: “Scene Map.tscn has the script door.gd. GDScript runs only in the editor, because the server has no Godot. For behavior, use New behavior; for a tool, move the script to Tools/.”

5. A documentation page, “What runs where”, compares the rule with Unreal’s Editor Utility Blueprints and Blender’s Python.

A tool produces ordinary content saved in the project; the Cooker reads the result, never the script. The result is saved and versioned rather than regenerated at cook time, so cooking only reads data and artists can adjust it by hand.

```gdscript
@tool
extends EditorScript   # runs from the editor; never in the game
```

const SEED := 1234

```gdscript
func _run() -> void:
    var root := get_scene()                  # the scene open in the editor
    var rng := RandomNumberGenerator.new()
    rng.seed = SEED                          # same seed, same result

    var mm := MultiMesh.new()
    mm.transform_format = MultiMesh.TRANSFORM_3D
    mm.mesh = preload("res://Content/Vegetation/pine.mesh")
    mm.instance_count = 500
    for i in mm.instance_count:
        var pos := Vector3(rng.randf_range(-200, 200), 0, rng.randf_range(-200, 200))
        mm.set_instance_transform(i, Transform3D(Basis(), pos))

    var inst := MultiMeshInstance3D.new()
    inst.multimesh = mm
    root.add_child(inst)
    inst.owner = root                        # saved with the scene: the result is ordinary content
```

Interactive resources never come from such a tool: a tree that can be cut or harvested is gameplay and spawns through a spawn area (see [[World authoring and cooking (Engine, Game)|World authoring and cooking]]); the tool handles decorative vegetation only.

```cpp
// GodotTools: Runic's export starts only if nothing scripted is bound for the client.
bool RunicExport::Validate(const ExportPlan& plan, Report& report) {
    for (const String& path : plan.Files()) {
        if (path.ends_with(".gd"))
            report.Error(path, "scripts never ship to the client");
        else if (IsScene(path) && SceneHasScriptedNode(path))
            report.Error(path, "scene has a node with a script");
    }
    return report.Ok();   // on error, Godot's export is never called
}

// Godot export plugin: tool folders never enter the package.
void RunicExportPlugin::_export_file(const String& path, const String& type,
                                     const PackedStringArray& features) {
    if (path.begins_with("res://Tools/") || path.begins_with("res://addons/"))
        skip();
}
```

If a studio ever wants designers to script quests and dialogue, the answer is a sandboxed language on the server (for example Luau), as many MMO servers do: a separate future Runic feature, never GDScript.

### Godot plugins

Part of Godot’s plugin ecosystem works in a Runic project; a plugin has to pass a technical filter (does it run in the Runic build?) and an architectural one (does what it does fit an engine whose gameplay runs outside Godot?).

| Plugin kind | In the Runic build |
| :---- | :---- |
| GDScript (addons/ with .gd files) | Loads in the editor from the tools phase on; never in the client |
| GDExtension (native library) | Loads if it only uses classes the build has, for the same Godot version, in single precision (binary-compatible with official Godot) |
| C++ module | Enters if added to the build |
| Asset pack (models, textures, shaders) | Always works; it is content |

The plugin’s role decides: an editor tool that generates content fits if the Cooker understands its output (a terrain plugin with its own format needs a Cooker adapter for the server heightfield); client presentation fits if it uses only classes of the client build (water shaders, sky, post-processing); gameplay inside Godot does not fit. LimboAI, for example, runs behavior trees inside Godot, while Runic AI runs on the server; it could only serve visual-only creatures or as a tree editor with a converter.

Godot does not declare plugin dependencies, so Runic adds four checks:

* **Published API per build:** the exact class list of each Runic build (–dump-extension-api) ships with each version; a plugin compiled against it fails at compile time if it uses something removed.

* **Validator on install:** reports scripts in a target without GDScript, extensions that fail to load because of a missing class, and scenes that use classes outside the client profile.

* **Export lock:** the same lock as above.

* **Optional manifest (runic.plugin.json):** where the plugin runs, what it needs and which Cooker adapter it provides; for third-party plugins without one, the validator infers it.

If an editor tool needs Godot’s physics or navigation (scattering vegetation casts rays against colliders), the editor profile may switch them back on at the tools phase; the client never.

### Threads, precision and input

* **Threads:** Godot’s scene tree is not thread-safe. Prediction and extraction run on Runic workers; the presenter applies everything on Godot’s main thread, and the RenderFrame stays double-buffered as in v3.

* **Precision:** Godot stays in single precision (no double-precision Godot build). The RenderFrame is camera-relative, and the presenter keeps its own origin, rebased about every 4 km (see [[Client runtime (Game on Engine)|Client runtime]]).

* **Input:** Godot owns the window, so input is born there. Godot’s UI consumes first, and what is left becomes an AppEvent that goes down the LayerStack: the v3 rule “the top handles first” unchanged.

### Slice 0 spike results (GDT-1)

The spike ran on Godot 4.7.2-stable and godot-cpp 10.0.0-stable (API 4.7). The RunicEditor, a Runic executable that owns main(), loads the editor library, creates the one instance with the command line unchanged, starts it and calls iteration() until the editor quits; a test plugin registered at the editor level loads and unloads.

| Finding | Consequence |
| :---- | :---- |
| The editor runs as a library, headless and windowed (Vulkan, Forward+), with the module lists and without GDScript; it exits cleanly, and the project manager opens and exits | Plan A holds; plan B stays only as the approved fallback (open decision 5) |
| The editor library is about 178 MB and builds in about 5 minutes with clang and lld on 8 jobs; the template library (with the build profile) is about 73 MB and 3 minutes | The SCons cache keeps CI builds short |
| Without GDScript the editor prints one benign error from the Create Plugin dialog, which selects the first script language when there is none | Report upstream (a one-line guard), carry a small documented patch, or hide plugin creation with the editor feature profile (GDT-2); it disappears when GDScript returns in slices 20–21 |
| Export templates refuse --path (built with disable_path_overrides) and run only the .pck next to the executable | The shipping lock stays on. Until the client .pck export (COOK-4, slice 22) the development client runs the editor library; the template library is checked by loading it |
| libgodot is loaded at runtime, not linked | One client binary runs the editor library in development and the template library when shipping; the headless check uses the link closure, so the server reaches no Godot target |
| Without Godot’s physics modules Godot warns unless the project selects its dummy physics servers | Projects set physics/3d/physics_engine and physics/2d/physics_engine to "Dummy"; the project template carries both (GDT-2) |
| godot-cpp 10 ships the 4.7 API; --dump-extension-api does not work through LibGodot | The published API per build needs the same profile built once as an executable (RUNIC_GODOT_API_FILE is ready for it) |
| Without a branding patch the RunicEditor shares Godot’s editor settings folder with an official Godot on the same machine | Owner decision: apply a branding patch (separate settings folder) or not |

Not verified by the spike: the project manager’s Open and New relaunching the RunicEditor with --path (GDT-2), Godot’s Play buttons relaunching it (Run is GDT-9; main() stops the relaunch until then), Windows and macOS, and the CI jobs on GitHub.

### Risks

* **LibGodot is new:** one instance per process, desktop platforms only. The editor as a library was the least tested path; the slice 0 spike proved it (see above), and plan B remains the fallback.

* **Build and version:** building Godot from source takes tens of minutes without a cache, and moving from 4.x to 4.y becomes a decision with tests.

* **Editor without GDScript:** the editor target must build and open without the module; the slice 0 spike confirmed it.

* **Module names change between versions:** the module lists are reviewed at every update.

* **Code RmlUi would have given:** the view-model binder is Runic’s own.

* **Arguments:** the project manager relaunches the executable with –path; main must pass every argument to Godot.

### Open decisions

| \# | Decision | Options | Recommendation |
| :---- | :---- | :---- | :---- |
| 1 | Data file format (skills, items, AI, quests) | Runic text files opened in Godot through a loader, or Godot .tres | Runic files: the server reads them without Godot and the v3 versioned schemas keep working |
| 2 | New project from the project manager | A small patch in Godot’s project manager, or a plugin that initializes an empty project | The plugin first; the patch only if the experience asks for it |
| 3 | Client animation | (A) the Runic evaluator with poses sent to RenderingServer skeletons, no nodes; (B) Godot’s AnimationTree driven by the animation intent | A keeps “no nodes” and controls crowd cost; B brings a visual blend editor |
| 4 | MusicDirector | Runic logic with a Godot backend, or code on the Godot side | Runic logic: generic, testable and independent of rendering |
| 5 | Fallback if the editor cannot run as a library | The RunicEditor becomes a Godot editor built by Runic that loads the Runic tools as a GDExtension | Approve now as plan B: the same code, only the owner of the process changes. The slice 0 spike passed (plan A holds), so plan B is only a fallback |
