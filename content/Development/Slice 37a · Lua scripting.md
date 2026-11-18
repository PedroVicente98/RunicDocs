---
title: "Slice 37a · Lua scripting"
aliases:
  - "Slice 37a"
tags:
  - "development"
  - "slice"
  - "progress/not-started"
slice: "37a"
status: "Not started"
owners: "Engine"
created: "2026-11-16"
modified: "2026-11-16"
---

**Slice:** 37a · **Status:** Not started · **Packages done:** 0 of 4 · **Owners:** Engine

← [[Slice 37 · Cross-border combat]] · [[RunicGame — Development|All slices]] · [[Slice 38 · Battle scale]] →

**Runnable result:** A boss phase and a quest condition written in Lua run in RunicServer and pass the same tests as their C++ versions; editing a script while the server runs changes the behavior at the next tick; a runaway script is stopped and logged without stalling the tick

**Proves:** Lua VM per simulation, sandbox and budgets, Lua entries behind the GameplayFlow, Quest and interaction registries, bytecode cooking, hot reload

**Godot:** RunicScript resource; script property and parameters on RunicInteractable3D and marker nodes; New Lua action or condition assistant

### Packages

- [ ] **SCR-1** · Lua runtime: one Lua VM per simulation, run on the simulation thread; the Lua version pinned with the build; a sandboxed environment (no io, os, load, debug or package); a memory cap per VM through its allocator; an instruction budget per call through the count hook; errors isolated per entry and logged with the script, line and entity · no issue · not started
    - Lua runtime: one Lua VM per simulation, run on the simulation thread; the Lua version pinned with the build; a sandboxed environment (no io, os, load, debug or package); a memory cap per VM through its allocator; an instruction budget per call through the count hook; errors isolated per entry and logged with the script, line and entity
    - **Done when:** A runaway loop is stopped within its budget and logged while the tick completes; a script cannot reach io, os or load; a script error fails only its own entry
    - **Needs:** [[Slice 5 · Moving entities|SIM-2]], [[Slice 9 · First cooker proof|CNT-1]]
- [ ] **SCR-2** · Bindings and the registry adapter: Entity, GlobalEntity and WorldPosition as opaque handles that keep their C++ type rules (a Lua integer never stands in for them); read-only contexts of GameplayFlow, Quest and interactions; a Lua function registered under an ID as an action, condition or trigger, behind the same registries as C++ entries; the ScriptBinding component (script and parameters) that an interactable calls on OnInteract; structural changes queued as commands; state between calls only in components · no issue · not started
    - Bindings and the registry adapter: Entity, GlobalEntity and WorldPosition as opaque handles that keep their C++ type rules (a Lua integer never stands in for them); read-only contexts of GameplayFlow, Quest and interactions; a Lua function registered under an ID as an action, condition or trigger, behind the same registries as C++ entries; the ScriptBinding component (script and parameters) that an interactable calls on OnInteract; structural changes queued as commands; state between calls only in components
    - **Done when:** A boss phase and a quest condition written in Lua pass the same tests as their C++ versions; the slice 37 handoff test passes with Lua entries; data that names an entry stays the same when its implementation moves between C++ and Lua
    - **Needs:** SCR-1, [[Slice 29 · Scripted sequences|GPL-5]], [[Slice 37 · Cross-border combat|FLOW-3]], [[Slice 37 · Cross-border combat|QST-3]]
- [ ] **SCR-3** · Script pipeline: the Cooker compiles scripts to bytecode for the pinned Lua version; hot reload swaps a changed script at the next safe tick and keeps simulation state; a lua-language-server annotation file generated from the bindings · no issue · not started
    - Script pipeline: the Cooker compiles scripts to bytecode for the pinned Lua version; hot reload swaps a changed script at the next safe tick and keeps simulation state; a lua-language-server annotation file generated from the bindings
    - **Done when:** A syntax error fails the cook with the file and line; a script edited while RunicServer runs changes the behavior at the next tick, with no restart; the annotation file lists every bound function
    - **Needs:** SCR-2, [[Slice 20 · Data-driven content|CNT-2]], [[Slice 20 · Data-driven content|COOK-2]]
- [ ] **GDT-17** · Scripts in the editor: the RunicScript resource and its import, a script property with the parameters the script declares on RunicInteractable3D and marker nodes, an inspector for those parameters, the New Lua action or condition assistant · no issue · not started
    - Scripts in the editor: the RunicScript resource and its import, a script property with the parameters the script declares on RunicInteractable3D and marker nodes, an inspector for those parameters, the New Lua action or condition assistant
    - **Done when:** A script assigned in the inspector cooks into a ScriptBinding component; the assistant writes a script that registers and opens in the IDE
    - **Needs:** [[Slice 21 · World partitions|GDT-7]], [[Slice 20 · Data-driven content|GDT-10]], SCR-3

*Generated by `tools/sync_development.py` from the [[Vertical-slice roadmap]], the work packages and the GitHub issues. Change those, then run it again.*
