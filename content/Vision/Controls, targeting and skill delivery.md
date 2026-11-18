---
title: "Controls, targeting and skill delivery"
tags:
  - "vision"
  - "appendix/combat-review"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-11-16"
modified: "2026-11-16"
---

Decided in the combat conversation of 10 to 12 November 2026 (see [[RunicGame — Combat Systems Review]]). Combat takes from Black Desert its command combos (a direction or Shift plus a key) and the follow-up links between skills, and from ArcheAge about 28 skill picks at max level, status combos, combos between players and ancestral-style morphs (as Inscriptions). It rejects Black Desert's fast pace, animation cancelling as a damage technique, iframes inside attack skills and grabs that ignore super armor, and ArcheAge's tab target and free three-tree combinatorics.

### Controls and input

| Input | Rule |
| :---- | :---- |
| WASD | Movement. A and D only steer and are never part of a command |
| Sprint | Shift plus any direction starts a sprint in that direction. It continues while any direction is held (the direction can change) and ends when none is held; starting again needs Shift. Actions and skills end the sprint, except the jump |
| Space and Ctrl | Jump and dodge; players can swap them, and the roles of Shift, Ctrl and Space, in the settings (the sprint follows the key that becomes the modifier) |
| LMB and Shift+LMB | Light and heavy attack on every weapon |
| RMB (hold) | Guard on every weapon; its form depends on the weapon |
| Shift+RMB | The weapon's alt action, almost always with a movement component (a dash forward or backward); a design suggestion, not a rule |
| Q | A tap key; the default home of grabs and other control skills |
| Skill keys | Q, E, F, C: plain, W+, S+ and Shift+. X, Z, V: plain and Shift+. Shift with another key ignores W, so there are no Shift+W+ or Shift+S+ contexts. Extra combinations (W+V, Shift+V) are to be tested |
| Own combinations | Players can add combinations of their own (e.g. Q+E, F+E), saved in presets, with a reset button; combinations with action keys use a short waiting window |
| Hotbar | 1–5 and Shift+1–5 |
| Mouse | Three buttons (LMB, MMB, RMB) and the wheel; no side buttons by default. MMB and the wheel control the Ward (see Targeting) |
| R | Tap interacts. Hold opens a radial menu without a cursor: the mouse moves a pointer from the center, and releasing R picks |
| T | Auto-walk forward only (cruise mode) |
| Tab | Cursor mode. Out of combat, clicking a character targets it and RMB opens its interactions (friend, invite, examine); examine shows gear and some skills, like WoW |
| UI windows | I inventory, P character, K skills, J journal and so on; windows never use skill keys |

* **Press only.** Every skill fires on press, combinations included. Holding exists only for Guard and the R menu. *Open: charged attacks (Bow, Greatsword) either don't exist or holding comes back for them; a "press and press again" model is not wanted.*  
* **No double-tap** for anything; it is too error-prone.  
* **Input budget:** 22 commands (16 on Q, E, F, C and 6 on X, Z, V) plus 10 hotbar keys.  
* *Proposal: input resolution takes the most specific match first (Shift+key, then direction+key, then the key alone); a combination with no skill falls through to the next; dodge and Guard always win.*  
* **No macros.** Macros, sequences on one key and auto-chaining are forbidden, detected and bannable; add-ons count as hacks. Everything about input and display is configurable, and nothing changes what one press does.

### Command board

* Players place their active skills freely on a board of keys × contexts. Any skill can go in any cell; even fixed skills have configurable commands.  
* Two layouts of the same skills: the command board, in the style of Black Desert, and a standard skill bar, in the style of ArcheAge.  
* Combos follow skills, not keys: links and highlights point to the skill. The client decodes keys and the server receives only skill IDs. Players read enemies from animations and telegraphs, never from keys.  
* Each skill declares a primary and a secondary auto-placement position. The contexts (W+ engages, S+ defends, Shift+ empowers) are only preset orders, never rules.  
* An easy interface for presets and combinations, and an optional overlay like Black Desert's that shows the skill and its configured combination. The combo hint is visual only.  
* *Proposal: default layouts per class, saved per class and per skill preset; an Altar reset keeps the cells of the skills that remain.*

### Timeline and cancelling

* **One phase before the strike:** startup → active → recovery. The startup is the cast bar the player sees; cast time and startup are the same thing.  
* **A fixed start:** the first part of every action can't be cancelled. Its length is the action floor of that action type (default 0.25 s, adjustable).  
* **Cancelling** *(may change after playtests)*: after that, dodge cancels at any moment except the active phase and skips the remaining recovery; movement cancels a cast that roots; Guard and basic attacks also cancel, and whoever cancels inherits the remaining recovery at its start. The cooldown always applies. Nobody is stuck in an action unless it is already happening.  
* **Active frames:** nothing cancels them.  
* **Dodge** can't be cancelled; startup about 2 ticks and a large iframe window. **Guard** has its own startup (about 3 ticks) and ends on release or like any skill. A cancel never extends the iframe or the Guard.  
* Basic attacks and fast skills deal less damage and are naturally harder to dodge.  
* Attacks meant to be reacted to keep windups of at least 350 to 400 ms (see [[Ping resolution (Engine, Game)#Reaction window by ping|Reaction window by ping]]).

### Targeting

Combat is 100% action: no tab target on enemies, and hostile skills always follow the crosshair. There are two target slots.

| Slot | Who | How it is set | Used by |
| :---- | :---- | :---- | :---- |
| Action target | Any entity, enemy or ally | The exact entity under the crosshair; if none, the closest one within a short distance after a short dwell. Faint outline | Direction and path of action skills, the info frame and the light aim assist |
| Ward | An ally or yourself | MMB tap on an ally pins them; MMB hold pins yourself; the wheel cycles your group. Clear outline, with an optional arrow over the head | Target skills (heals, buffs, shields) |

* **Cycle group:** the party, team or another predetermined group, never neutral allies; they enter only by tapping MMB on them. The wheel cycles only once a Ward is set (a setting makes it always active). The MMB tap must be exactly on the person (about 1° of tolerance).  
* **No Ward:** a target skill goes to the ally closest to the crosshair (default) or to yourself (setting). Whether that fallback pins the ally or applies to that cast only is a setting; the default is that cast only.  
* **Two allies at once:** the crosshair on ally A and the Ward on ally B is legal: target skills go to B, action skills go where the player aims.  
* **Frames:** the action target and the Ward each show a frame like a tab-target MMO (health, mana, Resolve, buffs, debuffs, conditions), as a preview only, never a lock. Skills that combo with the target's states are highlighted, and allies that would benefit from a skill are highlighted while cycling.  
* *To test: radius about 5°, dwell about 100 ms on a direct hit and 250 ms on a closest guess; the frame lingers about 2 s.* A browser Targeting Lab tests the variant (see Visualizations).  
* **Dropped:** two targeting modes toggled by MMB, and a triage mode with Ctrl and party frames.

### Skill delivery and casting

| Delivery | How it works |
| :---- | :---- |
| Action | The crosshair sets direction and path; the action target never makes a skill home |
| Placed area | Aimed only during the first ~20% of the cast bar; then it locks, enemies see it for the rest of the cast, and it appears in place at the end. Not necessarily a projectile |
| Projectile | No path is shown; an area left on impact (fire after a fireball) appears where it hits |
| Target (Ward) | Goes to the Ward |
| Target-centered area | A circle on the Ward (e.g. an area heal); each skill locks in place or follows the Ward |
| Dual-use | A projectile, beam or area that hits the first entity or everything in its path; its effect depends on whether each one is an ally or an enemy (like Moira's beam), never on a mode |
| Self | On the caster |

* **Movement while casting:** Rooted (default), Slowed (speed set per skill) or Free (mostly basic attacks and the main kit). There is no automatic penalty: balance lives inside each skill. It applies to the startup and to channels.  
* Heals apply at once.

### Supports and combos

* Friendly skills snap to the ally in a generous cone; self-cast goes through the Ward.  
* Supports work in the combo system: an interface made for many heal, buff and shield skills and a few damage skills, mostly dual-use. Archetypes to cover: tanks, melee damage, ranged damage, mages (damage and tank) and healers (melee, ranged and mage).  
* **Combos** are ArcheAge-style status combos plus links ("after skill X within N ticks"), both through the [[Skills by components#Interaction framework|interaction framework]]. Combos read the target's state, whoever applied it, so players combo with each other.  
* Combo roles (Opener, Setter, Payoff, Link, Finisher, Answer) are a design checklist only and must not be rigid; Opener and Finisher remain real tags.  
* *Proposal: big payoffs consume the state, so only the first player cashes in; small bonuses don't.*

### Configurability

If something can be configurable, it should be: players play the way they prefer, and every setting has an accessible default. The limit is fairness: nothing changes what one press does.

**Practice and choice.** An instanced training area lets players pick any loadout, Discipline and level to test passives, combos and presets. The class choice at the start is diegetic: a cave with a bench of every weapon and a room with the Disciplines' pillars, with a preview, where the player can go back and forth until leaving the cave; after that, changes happen only at an Altar.
