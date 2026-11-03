---
title: "Godot plugins"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › Godot plugins"
created: "2026-10-14"
modified: "2026-10-30"
---

Part of Godot’s plugin ecosystem works in a Runic project; a plugin has to pass a technical filter (does it run in the Runic build?) and an architectural one (does what it does fit an engine whose gameplay runs outside Godot?).

| Plugin kind | In the Runic build |
| :---- | :---- |
| GDScript (addons/ with .gd files) | Loads in the editor from the tools phase on; never in the client |
| GDExtension (native library) | Loads if it only uses classes the build has, for the same Godot version, in single precision (binary-compatible with official Godot) |
| C++ module | Enters if added to the build |
| Asset pack (models, textures, shaders) | Always works; it is content |

The plugin’s role decides: an editor tool that generates content fits if [[Cooker|the Cooker]] understands its output (a terrain plugin with its own format needs a Cooker adapter for the server heightfield); client presentation fits if it uses only classes of the client build (water shaders, sky, post-processing); gameplay inside Godot does not fit. LimboAI, for example, runs [[Behavior-tree runtime|behavior trees]] inside Godot, while Runic AI runs on the server; it could only serve visual-only creatures or as a tree editor with a converter.

Godot does not declare plugin dependencies, so Runic adds four checks:

* **Published API per build:** the exact class list of each Runic build (–dump-extension-api) ships with each version; a plugin compiled against it fails at compile time if it uses something removed.

* **Validator on install:** reports scripts in a target without GDScript, extensions that fail to load because of a missing class, and scenes that use classes outside the client profile.

* **Export lock:** the same lock as above.

* **Optional manifest (runic.plugin.json):** where the plugin runs, what it needs and which Cooker adapter it provides; for third-party plugins without one, the validator infers it.

If an editor tool needs Godot’s physics or navigation (scattering vegetation casts rays against colliders), the editor profile may switch them back on at the tools phase; the client never.

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[GDScript editor tools only|GDScript: editor tools only]] · [[Threads precision and input|Threads, precision and input]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › Godot plugins · exported 2026-11-03
