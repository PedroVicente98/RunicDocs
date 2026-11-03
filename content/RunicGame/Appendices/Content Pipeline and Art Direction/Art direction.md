---
title: "Art direction"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Art direction"
created: "2026-10-26"
modified: "2026-10-30"
---


## Target

* **Decision.** The quality target is a mix of World of Warcraft and ArcheAge, or better than ArcheAge where the budget allows. Crimson Desert's fidelity is not a target: it draws one hero, while RunicGame must draw 100 against 100.
* **Decision.** World of Warcraft's problem for RunicGame is its character models, not its art style: their proportions do not allow detailed weapon swings. RunicGame wants models closer to Black Desert's.
* **Proposal.** Identity comes from color, shape language, armor design and textures. Proportions stay close to real anatomy with a slight heroic push: hands and shoulders a little larger, within what motion capture can handle.

Why the body matters more than the triangle count: World of Warcraft's large pauldrons, broad shoulders and oversized hands make an overhead arm clip through the armor, so its swings stay short and sideways, and its rigid gear pieces follow a single bone. Black Desert's swings come from motion capture (Pearl Abyss runs its own studio, later expanded to 1,000 m² with 150 cameras), and captured motion fits only bodies close to human proportions. On heroic proportions, captured hands go through the pauldrons.

## Reference games

| **Game** | **Character triangles** | **Where the number comes from** | **Notes** |
| :---- | :---- | :---- | :---- |
| World of Warcraft | About 5k per base model since Warlords of Draenor; 10k to 20k in full gear (estimate) | The Warlords of Draenor update raised models from under 1,000 to over 5,000 polygons (gnome: 956 to 5,408, with bones from 130 to 196). An HD model file with every hairstyle and gear piece has 27,060 triangles | Hand-keyed animation; heroic proportions |
| ArcheAge | 8.2k for a Firran body; 15k to 25k with armor (estimate) | Sketchfab upload of the Firran female, likely the base body | Simpler models, much detail in textures |
| Black Desert | 24.4k for an NPC (Valkyrie Tiphaine) | Game rip on Sketchfab | Player characters with costumes and hair are heavier. Many 100k+ "Black Desert" models online are fan recreations |
| Crimson Desert | Not published; likely 80k to 200k+ (estimate) | Comparison: Kratos in God of War (PS4) has 80,000 polygons, 32,000 of them in the face; Aloy's hair in Horizon Zero Dawn is 100k triangles | Single-player; GPU cloth and hair simulation |
| ArcheAge Chronicles | Not published | Unreal Engine 5; Steam Next Fest demo from 19 to 26 Oct 2026; Early Access planned for Q4 2026; one listing reports an RTX 3060 Ti as the minimum | The upper limit of what an MMO attempts today |

## Texture approach

**Proposal.** Stylized physically based textures: a simplified, painterly color texture with real roughness and metal maps, and an optional normal map at lower resolution.

| **Approach** | **What it is** | **Memory per 2K set (approx.)** | **Fit for RunicGame** |
| :---- | :---- | :---- | :---- |
| Realistic (Black Desert) | Plain color with no lighting painted in, a sculpted normal map, roughness and metal; the lighting does the work | 13 to 16 MB (3 full maps) | Blurs at low resolution, which matters in crowds |
| Hand-painted (World of Warcraft) | Light, shadow and highlights painted into the color texture; little or no normal map | About 5 MB (1 map) | Painted highlights do not move with the sun, which looks wrong with weather and the day cycle |
| Stylized physically based (hybrid) | Painterly color plus real roughness and metal; optional low-resolution normal map | 9 to 10 MB | Reacts to dynamic light and still looks good at 1K, about 4× less memory per character than 2K |

* **Proposal.** Much of World of Warcraft's look comes from saturated lighting, soft fog and color grading. In Godot these are environment resources, the cheapest part to change later.
* **Proposal.** Every asset (characters, mobs, props, environment) uses the same texture approach, and bought or free assets are filtered by it. Mixing styles is the usual mistake of small teams.
* **Proposal.** Before locking the approach, texture one armor piece in the realistic and the hybrid style and compare both in Godot under morning, noon and sunset light.

## Reference sources

* Wowhead Dressing Room: a 3D viewer in the browser to put any race in any armor set and play animations; the best way to study World of Warcraft's silhouettes and how armor sits on the body.
* ArtStation and 80.lv: artists from World of Warcraft, ArcheAge and Lost Ark often post wireframes, texture sheets and triangle counts.
* Gameplay videos at maximum settings, comparisons of low and ultra settings, and sieges or large PvP fights, which show what each game scales down.
* Other MMOs as points between stylized and realistic: Lost Ark (detailed stylized-realistic armor), Guild Wars 2 (painterly environments), Elder Scrolls Online (closer to realistic, large PvP) and Throne and Liberty (realistic, large sieges).
* Sketchfab: it counts triangles, but the vertex count rises in the engine at texture seams and hard edges, so check again after importing into Godot. The Model Inspector shows the wireframe and texture sizes. Prefer models tagged game-ready or real game rips. Filter by Animated and watch the elbows and shoulders to judge a rig.

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Related entries in Ideias|Related entries in Ideias]] · [[Budgets|Budgets]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Art direction · exported 2026-11-03
