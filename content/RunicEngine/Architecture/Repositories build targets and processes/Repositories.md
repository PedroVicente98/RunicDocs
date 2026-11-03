---
title: "Repositories"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Repositories, build targets and processes › Repositories"
created: "2026-10-14"
modified: "2026-10-30"
---

| Repository | License | Owns |
| :---- | :---- | :---- |
| RunicEngine | Open source (C++) | Engine modules, the entry point and ApplicationHost, the [[Tools#RunicEditor\|RunicEditor]] (the Godot editor through LibGodot) with GodotTools and [[Cooker\|the Cooker]], GodotBridge, the [[Tools#Testing at scale\|RunicBot]], the project template; pins Godot and godot-cpp |
| RunicPlatform | Open source (C++ and Go) | [[Networking stack sessions and responsiveness#Stack (decided)\|GameNetworkingSockets]] transport, server bindings (services bridge and lifecycle layers), Protobuf contracts, Go SDK, core services, building blocks, [[Platform and operations#Simulation placement\|Agones]] and Kubernetes manifests, dashboards |
| RunicGame | Closed source | GameClient and GameServer executables (RunicGameClient, RunicGameServer), game modules and the game’s editor library, Go game services, content; it is a RunicEngine project (project.godot, runic.project.json) |

RunicGame is the superproject: it pins RunicEngine and RunicPlatform as git submodules, which CI and releases build from. RunicPlatform pins RunicEngine the same way, so its C++ bindings build and test on their own. For daily work, a CMake option (RUNIC\_ENGINE\_DIR, RUNIC\_PLATFORM\_DIR) points at sibling checkouts instead. The Game’s executable targets are RunicGameClient and RunicGameServer; this document calls them GameClient and GameServer. RunicEngine pins Godot and godot-cpp as submodules at a release tag and builds libgodot from source in two targets (see Godot integration).

---

↑ [[Repositories build targets and processes|Repositories, build targets and processes]] · [[Engine modules|Engine modules]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Repositories, build targets and processes › Repositories · exported 2026-11-03
