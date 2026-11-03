---
title: "Custom behaviors"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "RunicGame systems (Game) › Custom behaviors"
created: "2026-10-14"
modified: "2026-10-30"
---

```cpp
// Illustrative contract, not a frozen API.
struct BleedJumpParams { float jump_radius_m; uint8_t max_jumps; };

class BleedJump final : public SkillBehavior<BleedJumpParams> {
public:
    HookMask Hooks() const override { return Hook::OnKill; }

    void OnKill(const KillContext& ctx, const BleedJumpParams& p,
                BehaviorOutput& out) const override {
        auto next = ctx.Spatial().NearestEnemies(ctx.VictimPosition(),
                                                 p.jump_radius_m, p.max_jumps);
        for (EntityRef target : next)
            out.ApplyStatus(target, "game:bleed", ctx.SourceStatus());
    }
};

void RegisterGameBehaviors(BehaviorRegistry& registry) {
    registry.RegisterSkill<BleedJump>("game:bleed_jump");
}
```

```yaml
custom:
  id: game:bleed_jump
  params: { jump_radius_m: 8, max_jumps: 2 }
effects:
  - bleed: { buildup_pct: 40 }   # the standard component stays
```

A custom behavior never replaces standard components, so defenses, coefficients, caps and item effects keep working on it.

---

↑ [[RunicGame systems|RunicGame systems (Game)]] · ← [[Resolver|Resolver]] · [[Defense and threat|Defense and threat]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › RunicGame systems (Game) › Custom behaviors · exported 2026-11-03
