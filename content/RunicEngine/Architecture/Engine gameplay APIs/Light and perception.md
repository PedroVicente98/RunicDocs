---
title: "Light and perception"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Engine gameplay APIs (Engine) › Light and perception"
created: "2026-10-14"
modified: "2026-10-30"
---

Light scales how far mobs notice entities and how far players see each other; it never changes how a hit is resolved.

| Element | What it is | What a game supplies |
| :---- | :---- | :---- |
| AmbientLightProfile | Light level per region and volume over time of day and weather, with a floor (“skylight”) | Curves per region, volume and weather |
| LightEmitter | Radius, intensity and duration on an entity or area | Torches, lanterns, lit abilities, items, area lights |
| Luminosity | Effective light on an entity: the brighter of ambient light and emitters reaching it | Nothing; computed |
| Concealment | Multiplier on how far others detect or see the entity | Stealth, invisibility, gear values |
| PerceptionProfile | Warn and detect base radii, minimum and maximum, light curve, dark vision | Per mob definition |
| VisibilityProfile | Maximum visible range, silhouette range, light curve | Global or per region |

* Emitters are indexed in cells, so luminosity is a few lookups in neighboring cells. It updates at 10 Hz for players and for mobs awake or near players; lighting a torch updates it at once.

* Mob radius \= base × light curve (target luminosity) × target concealment, clamped to the profile’s minimum and maximum. The minimum guarantees detection in total darkness.

* Inside the warn radius a mob investigates; inside the detect radius it engages. A game that sets warn at or below detect never uses warn.

* Stealth and invisibility are concealment values; zero means undetectable. A separate Aggroable toggle covers non-perception cases (dead, GM, protected).

---

↑ [[Engine gameplay APIs|Engine gameplay APIs (Engine)]] · ← [[Behavior registry contract|Behavior registry contract]] · [[Scripted sequences GameplayFlow and restrictions|Scripted sequences (GameplayFlow) and restrictions]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Engine gameplay APIs (Engine) › Light and perception · exported 2026-11-03
