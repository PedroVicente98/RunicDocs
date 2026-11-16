---
title: "Business model, launch, visuals and audio"
tags:
  - "vision"
  - "appendix/rendering-lighting-visibility"
  - "appendix/content-pipeline"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-11-16"
---

### Business model

* **Decided:** a subscription, and no cash shop under any circumstance, not even for cosmetics. The Market Isle never sells anything for real money.  
* **Open:** the base model next to the subscription, free-to-play (limited free play, with the subscription giving full access) or buy-to-play. One possibility under consideration is free-to-play plus the subscription, with buy-to-play expansions; it isn't decided.

### Launch

**Open, with the business model.** The plan of the earlier version was early access for subscribers, a pay-to-play launch period of a month or more, and then free access opened gradually so the servers aren't overloaded. Whether it stays depends on the base model.

### Subscription

The subscription is the main income and creates one clear barrier: whoever plays without it knows from the start what they don't have, and nothing surprises them later.

| Benefit | Subscriber | Without subscription |
| :---- | :---- | :---- |
| Owning land and paying tax | Yes | No |
| Offline labor regeneration and the labor reserve | Yes | No |
| Maximum labor | The same | The same |
| Early access | Yes, if the launch plan stays | No |

The class reset and inventory expansions are paid with in-game gold, not real money.

### Visuals

* A collection of mounts and pets, as in WoW.  
* Transmog as an account wardrobe: obtaining or equipping an item unlocks its appearance forever, applied as a visual slot. Nobody needs to keep old items.  
* Weapon appearances per weapon type, which fits the class system.  
* Dungeons and raids give exclusive cosmetics. Heritage visuals per race: cultural armor, mount and glider.  
* **Art direction:** World of Warcraft's identity (color, readable shapes, armor design) on bodies with near-real proportions like Black Desert's, so weapon swings can be animated in detail, at a fidelity between World of Warcraft and ArcheAge. Crimson Desert's fidelity is out of scope. Mid-poly characters in a low-poly, stylized world, with mid-poly exceptions (some ships and items); stylized textures like World of Warcraft's, never a move to realism. Immersion comes from the player's integration with the world, not from graphics: volumetric atmosphere even with simple models, and everything moves (grass, leaves, banners, sails, capes), reading the same wind as gameplay, so players read the wind before gliding or setting sails. Reference for proportions and movement: Never Be Alone. Details: [[Content pipeline and art direction (Game)]].  
* **Platforms:** Linux, Windows and macOS; no mobile.  
* **Render distance:** everything is rendered as far as possible with levels of detail, and fog never limits distance; it represents only real fog. Air haze is always on and never zero: from a mountain, other continents fade out, so the world feels bigger than it is (Elden Ring is the reference). Lighting works at any sun angle; global illumination is a graphics setting. Details: [[Rendering, lighting and visibility (Engine, Game)]].  
* **Attack feel:** short anticipation, overshoot and follow-through, fast through the hit and slower in recovery, a client-only hitstop of 2 to 4 frames on impact, weapon trails, a small camera shake and strong sound.

### Custom soundtrack (client only)

* The soundtrack belongs to the player: albums and presets per context (combat, farming, sailing, city), chosen in an interface option. Sound effects can't be changed, so every player hears the same combat cues.  
* Radio mode per context: a combat radio, a farming radio, a sailing radio. Each radio remembers the track and the point where it stopped and moves on to the next.
