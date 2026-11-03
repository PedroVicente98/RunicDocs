---
title: "Repositories, build targets and processes"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Repositories, build targets and processes"
created: "2026-10-14"
modified: "2026-10-30"
---

Three repositories and one CMake build graph: RunicGame owns the executables, the Engine and Platform are libraries and services it builds on, and the server never links rendering or player UI code.

## Contents

- [[Repositories|Repositories]]
- [[Engine modules|Engine modules]]
- [[Game modules|Game modules]]
- [[Platform modules|Platform modules (Platform)]]
- [[Processes|Processes]]
- [[Four axes that must stay separate|Four axes that must stay separate]]
- [[Three event families|Three event families]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Principles and performance targets|Principles and performance targets]] · [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Repositories, build targets and processes · exported 2026-11-03
