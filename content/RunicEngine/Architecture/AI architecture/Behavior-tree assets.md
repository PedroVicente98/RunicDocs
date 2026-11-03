---
title: "Behavior-tree assets"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Behavior-tree assets"
created: "2026-10-14"
modified: "2026-10-30"
---

```xml
<root BTCPP_format="4">
  <BehaviorTree ID="BasicMelee">
    <ReactiveFallback>
      <Sequence>
        <HasReactableThreat/>
        <ChooseDefense/>
      </Sequence>
      <Sequence>
        <HasCombatTarget/>
        <Fallback>
          <Sequence>
            <CanAttackTarget/>
            <ChooseAttack/>
          </Sequence>
          <ApproachTarget/>
        </Fallback>
      </Sequence>
      <Sequence>
        <IsAlerted/>
        <InvestigateAlert/>
      </Sequence>
      <Idle/>
    </ReactiveFallback>
  </BehaviorTree>
</root>
```

| Node | Responsibility |
| :---- | :---- |
| HasReactableThreat | Reads AIWorkingMemory and reaction timing; never discovers global events itself |
| ChooseDefense | Scores legal, meaningful defense families and emits one intent |
| HasCombatTarget | Checks that memory holds a current target |
| CanAttackTarget | Checks a coarse attack opportunity; final legality stays with command validation |
| ChooseAttack | Utility or priority choice among available abilities; emits UseAbility |
| ApproachTarget | Emits a movement goal through navigation and movement |
| IsAlerted, InvestigateAlert | The warn-radius behavior: walk to the sensed position, look around, give up after a Game-defined time |
| Idle | No expensive world scan; maintenance systems own wake conditions |

| Engine reusable nodes | Game content-specific nodes |
| :---- | :---- |
| HasCombatTarget, HasReactableThreat, TargetInRange, HealthBelow, IsAlerted, ChooseDefense, ApproachTarget, InvestigateAlert, ReturnHome | DragonWingSweepPolicy, NavalBoardingDecision, WorldBossContributionMechanic, named encounter phase logic |
| Generic ability-selection hooks and utility helpers | Actual skill IDs, encounter priorities, faction and game rules, boss mechanics |

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Intents become ordinary commands|Intents become ordinary commands]] · [[AI editor inside the RunicEditor|AI editor (inside the RunicEditor)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Behavior-tree assets · exported 2026-11-03
