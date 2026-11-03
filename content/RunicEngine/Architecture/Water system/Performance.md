---
title: "Performance"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Performance"
created: "2026-10-14"
modified: "2026-10-30"
---

* A loaded river with nobody interacting does essentially no work per tick; cost scales with active consumers, not kilometers of water.

* Ship and character water movement run at 30 Hz with the rest of movement and physics.

* A vessel samples a few buoyancy points (typically 4 to 8), one or two flow samples and one wind sample per tick; with cell filtering and cached locality these are small interpolations, so hundreds of vessels cost far less than any fluid simulation.

* Lakes and rivers keep a flat or smoothly sloped authoritative surface with client-only visual waves; oceans with naval play use the deterministic gameplay swell (see Environment), which does not change this API.

---

↑ [[Water system|Water system (Engine)]] · ← [[Authoring and cooking|Authoring and cooking]] · [[Debugging and validation|Debugging and validation]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Performance · exported 2026-11-03
