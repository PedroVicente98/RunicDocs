---
title: "How the Engine uses Godot"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › How the Engine uses Godot"
created: "2026-10-14"
modified: "2026-10-30"
---

The Engine uses Godot’s lower layers (servers and ClassDB) and its editor; the scene tree is used only for authoring and player UI.

| Godot layer | What it is | Use in Runic |
| :---- | :---- | :---- |
| Servers | Low-level APIs with handles (RID): RenderingServer, AudioServer, DisplayServer | The presenter draws directly in the RenderingServer; audio plays on the AudioServer; the window comes from the DisplayServer |
| Object and ClassDB | Reflection: every registered class exposes methods, properties and signals to the editor | Marker nodes and data types get an inspector, saving and undo for free |
| Node and SceneTree | A tree of objects with a lifecycle; a scene (.tscn) is a saved subtree | Authoring maps and player UI screens; never a game entity |
| Resource | A data asset with a stable UID, saved as .tres, .res or a custom format | Imported meshes, materials and textures; Runic data files enter through ResourceFormatLoader and ResourceFormatSaver |
| Editor API | Docks, inspector plugins (EditorInspectorPlugin), 3D gizmos (EditorNode3DGizmoPlugin), import and export plugins, undo and redo | Runic tools, [[Cooker\|the Cooker]], attach docks and data editors |
| GDExtension and godot-cpp | Godot’s C interface and the official C++ wrapper; registration by levels (core, servers, scene, editor) | How all Runic code talks to Godot |
| LibGodot | Godot as a library: the host’s main creates the instance, calls start() and then iteration() once per frame | GameClient and [[Tools#RunicEditor\|RunicEditor]]; one instance per process, desktop platforms only |

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

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[Executables and Godot targets|Executables and Godot targets]] · [[Projects create open and the games editor library|Projects: create, open and the game’s editor library]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › How the Engine uses Godot · exported 2026-11-03
