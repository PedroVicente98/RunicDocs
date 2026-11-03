---
title: "Four axes that must stay separate"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Repositories, build targets and processes › Four axes that must stay separate"
created: "2026-10-14"
modified: "2026-10-30"
---

| Axis | Question it answers | Mechanism |
| :---- | :---- | :---- |
| Compile-time dependencies | Which code may use which code? | CMake targets |
| Process composition | Which coarse features run in this executable, and in what order? | ApplicationHost \+ [[Application and LayerStack\|LayerStack]] |
| Simulation scheduling | What simulation work runs now, and before what? | 60 Hz master scheduler, 30/20/10 Hz domains, explicit phases |
| Distributed topology | Which process owns this region or entity? | [[Platform and operations#Simulation placement\|World Coordinator]], SimulationOwner, authority epochs |

---

↑ [[Repositories build targets and processes|Repositories, build targets and processes]] · ← [[Processes|Processes]] · [[Three event families|Three event families]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Repositories, build targets and processes › Four axes that must stay separate · exported 2026-11-03
