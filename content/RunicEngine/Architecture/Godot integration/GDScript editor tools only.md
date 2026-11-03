---
title: "GDScript: editor tools only"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › GDScript: editor tools only"
created: "2026-10-14"
modified: "2026-10-30"
---

GDScript never runs in the game, for any game made on the Engine: the server has no Godot, and prediction needs the same C++ on both sides. It starts switched off and returns at the tools phase, only in the editor and behind locks.

1. **Slices [[Slice 00 Build skeleton|0]] to [[Slice 19 Combat prototype|19]]:** the module is off in both targets.

2. **Slices [[Slice 20 Data-driven content|20]] and [[Slice 21 World partitions|21]]** (content pipeline): it returns in the editor target together with the locks below; the client stays without it.

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
| Server | Does not exist | No Godot; [[Cooker\|the Cooker]] writes only data |
| Shipping client | Cannot run | Built without the module: the final wall |
| Export | Blocked | The validator refuses scripts in anything bound for the .pck; the preset excludes Tools/, addons/ and \*.gd |
| Development client | Blocked on load | It uses the editor target, so the module exists in it; every scene it loads runs the export check and stops with an error |
| Godot’s “run scene” button | Intercepted | Godot runs a scene by relaunching its own executable; the [[Tools#RunicEditor\|RunicEditor]]’s main recognizes that mode and calls Runic’s Run instead, with no patch |
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

Interactive resources never come from such a tool: a tree that can be cut or harvested is gameplay and spawns through a spawn area (see World authoring and cooking); the tool handles decorative vegetation only.

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

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[Building Godot|Building Godot]] · [[Godot plugins|Godot plugins]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › GDScript: editor tools only · exported 2026-11-03
