---
title: "AI editor (inside the RunicEditor)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › AI editor (inside the RunicEditor)"
created: "2026-10-14"
modified: "2026-10-30"
---

Runic builds its own editor inside the RunicEditor, on Godot’s GraphEdit, instead of embedding the standalone BehaviorTree.CPP editor. The library remains the executor; Runic owns the authoring experience so trees, NPC definitions, personalities, validation, asset management, world selection, [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] inspection and live debugging live in one tool.

| Runic::AI (server-safe runtime) | Runic::GodotTools, AI docks (editor only) |
| :---- | :---- |
| AI components, definitions and contracts | GraphEdit behavior-tree canvas |
| BehaviorTreeRuntime | Node palette |
| Perception and think systems | Asset browser |
| Event consumers | Node and property inspector |
| Intent producer | Personality editor, validation, runtime debugger, selected-NPC inspection |

Runic::AI never includes or links Godot or editor code; the AI docks use the public AI definition and debug interfaces to author and inspect.

```cpp
struct BehaviorTreeAsset {
    AssetId id;
    std::string name;
    std::string xml;
};

runtime.Load(treeAsset);   // runtime
editor.Open(treeAsset);    // editor: edits and saves the asset, never a live BT::Tree

struct AINodeMetadata {
    std::string_view name;
    std::string_view category;
    std::string_view description;
    bool engineNode = true;
};

// One registration feeds both execution and editor discovery.
template <class T>
void RegisterAINode(BT::BehaviorTreeFactory& factory, AIEditorRegistry& editorRegistry,
                    AINodeMetadata metadata) {
    factory.registerNodeType<T>(std::string(metadata.name));
    editorRegistry.Register<T>(metadata);   // category, docs, ownership, icons, allowed contexts
}
```

| Panel | Purpose |
| :---- | :---- |
| AI Assets | Create, duplicate, rename, organize, open and delete trees; browse NPC definitions and personality profiles |
| Behavior Tree Canvas | Create, select and connect nodes; arrange, zoom and pan; validate structure; edit subtrees |
| Inspector | Node ports and properties plus Runic metadata and documentation |
| NPC Definition Inspector | Assign tree, personality, perception profile, leash defaults and Game AI profile fields |
| Runtime Debug | The selected live NPC: active node path, working memory, target, reaction timer, utility scores, last events, last intent |
| Validation and Problems | Missing nodes, invalid ports, unknown ability or content IDs, unreachable branches, forbidden dependencies |

**Editor actions**

* New tree from a template: Empty, Basic Melee, Ranged, Companion, Boss Phase Skeleton.

* Create or edit CombatPersonality profiles and preview how biases change utility.

* Assign a tree to an NPC archetype and jump from the NPC inspector straight to its tree.

* Validate referenced abilities, statuses, factions and RunicGame content IDs against the loaded registries.

* Open a live entity from the Flecs inspector and attach the AI debugger to its BrainHandle.

* Visualize wake or sleep state, warn, detect and leash radii, target and last perception facts in the viewport with the debug layers.

* Save trees independently of the live simulation; hot reload only through a development-only safe-point operation.

**Interaction rules**

* Graph editing is editor state, not simulation state.

* Runtime highlights are read-only overlays unless a specific debug command is implemented.

* Live tree replacement happens only at an explicit safe point; a tree is never destroyed or replaced while it ticks.

* The editor’s node list comes from the runtime’s registration plus editor metadata, never a second hard-coded list.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Behavior-tree assets|Behavior-tree assets]] · [[Runtime AI debugging|Runtime AI debugging]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › AI editor (inside the RunicEditor) · exported 2026-11-03
