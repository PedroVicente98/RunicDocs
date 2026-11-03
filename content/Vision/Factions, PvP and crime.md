---
title: "Factions, PvP and crime"
tags:
  - "vision"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-10-30"
---

There are three factions: Faction 1 (Continent 1), Faction 2 (Continent 2\) and the Pirates. Every character starts in a continental faction and, through their own actions, can move to the other or become a pirate. Working names and lore: [[RunicGame — Lore]].

| Faction | Where it lives | Group PvE with | PvP against |
| :---- | :---- | :---- | :---- |
| Faction 1 | Continent 1 | Its own faction and pirates | Faction 2 and Pirates |
| Faction 2 | Continent 2 | Its own faction and pirates | Faction 1 and Pirates |
| Pirates | Open-sea islands | Any faction | Everyone |

* **Crime.** Only an Outlaw can attack their own faction. Killing someone of your own faction is a crime and generates Infamy when the victim reports it; enough Infamy turns the character into a pirate (see [[Factions, PvP and crime#Outlaw and Infamy|Outlaw and Infamy]]).  
* **Changing continental faction** needs raising reputation with the other faction and also committing a crime against the current one: the break must be a visible choice. *Proposal: it also needs the Language profession.*  
* **Group PvE.** Continental factions do dungeons and raids only among themselves, with PvE and PvP mode characters together. World bosses are PvPvE and accept only PvP mode. Pirates can do PvE with both factions: that is the advantage of playing the hardest faction. In the boss region, also PvPvE, every PvP mode character competes for contribution in the same space.  
* **Sources of PvP.** Faction wars, intercepting trade packs, node wars, disputes on the wild continent, stealing contribution in the boss region and Outlaws against their own faction.

### Participation modes

PvP is the default mode; PvE mode protects from combat between players and gives access to most of the PvE and the economy. Both modes share the same continuous world, with no separate servers, instances or regions.

| Activity | PvE mode | PvP mode |
| :---- | :---- | :---- |
| Exploration, world PvE, dungeons and raids | Yes | Yes |
| Farming, gathering, housing, crafting and the economy | Yes | Yes |
| Sailing ordinary ships | Yes | Yes |
| Buying and using charts | Yes | Yes |
| Surveying (making charts) | No | Yes |
| World bosses and the boss region (PvPvE) | No | Yes |
| Trade packs, even on the safe routes | No | Yes |
| Piracy, guild wars, node wars and territory | No | Yes |

* **Isolation in the open world.** PvE and PvP characters don't affect each other with skills: no damage, CC, healing, buffs, shields, cleanse or resurrection between the modes, even in the same group.  
* **No physical blocking.** One mode doesn't block the movement, projectiles or strikes of the other, and can't be used as a shield.  
* **Mixed groups.** PvE and PvP characters can be in the same group to talk and explore; the group doesn't unlock combat cooperation or restricted rewards.  
* **PvE instance.** Inside dungeons and raids, everyone plays under the same PvE rules and can heal, buff and revive each other. The character's mode doesn't change; on leaving, the open-world rules return.  
* **Changing mode** happens only at the Great Altar of the faction capital, validated by the server. Pirates have no PvE mode.  
* **Trade packs** need PvP mode, even on the safe routes. The only safe routes are those of the starting areas: the shortest, the least profitable and repeatable without limit. Every other route, on land and at sea, is exposed to PvP. PvE mode doesn't pick up, carry, load, unload or deliver trade packs, not through the inventory, mail or transfers either.  
* **Ships.** A ship carrying trade packs automatically becomes a PvP trade ship. PvE characters can stay aboard only as passengers: they don't steer, use the sails, cannons or repairs, or touch the cargo or the ship's inventory. On ordinary ships the usual owner and crew permissions apply.  
* **A shared economy.** One economy for both modes: the PvE farmer sells, and the PvP merchant takes the cargo along the risky route.  
* **Cartography.** Surveying is PvP, so PvE characters don't make charts; they buy them. This is checked when the chart is created.

### Jurisdiction

Jurisdiction is the rule of the place where the character is: Open world, Sanctuary, Safe route (the trade routes of the starting areas) or PvE instance. It is different from the Participation mode, the character's PvE or PvP choice, and from the Balance Profile, the Base, PvE or PvP values of each hit. None of the three is ever called just "context".

### Who finds whom

The attacker decides: the queries of each actor's skills choose which entities it finds. Ordinary mobs need no marking; the target only needs its category (player, mob or world boss). In the Open world:

| Actor | Hostile skills find | Support skills find |
| :---- | :---- | :---- |
| Mob | Any player | Mobs |
| World boss | Only PvP mode players | — |
| PvE mode player | Mobs, never world bosses | PvE mode allies |
| PvP mode player | Mobs, world bosses and hostile PvP players | PvP mode allies; an active Outlaw only receives support from another Outlaw |

* **Hostile PvP players:** enemy factions, pirates and active Outlaws of your own faction. If the attacker is an Outlaw, their whole faction in PvP mode counts. Group members never count.  
* **World boss:** it targets only PvP players, so a PvE player can't pull or kite the boss.  
* **PvE instance:** all players form one PvE group; mobs target any player.  
* **Sanctuary and Safe route:** players' hostile skills never find players.

### Outlaw and Infamy

Outlaw is a toggle skill, only for PvP mode characters: when on, it allows attacking your own faction. PvE mode isolation always wins.

* **Cooldown.** After turning it on, it can only be turned off after about 30 min without attacking your own faction: each hit on a character of your own faction restarts the count. Healing or buffing another Outlaw doesn't restart it.  
* **Both ways.** While on, hostile skills, area ones included, find PvP players of your own faction (except the group), and your whole faction can attack the Outlaw without committing a crime.  
* **Support.** An active Outlaw only receives healing and buffs from another Outlaw; whoever helps isn't marked.  
* **Infamy.** Killing someone of your own faction generates Infamy only when the victim reports it, within a time window; damage without a kill generates none. Enough Infamy turns the character into a pirate, and Infamy decays slowly over time.  
* **Protected zones.** Sanctuary and Safe route ignore the Outlaw.  
* **No escape into PvE.** You can't switch to PvE mode with Outlaw on or with Infamy above zero.  
* *Proposal: Outlaw stays on after death.*
