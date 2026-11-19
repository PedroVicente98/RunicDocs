---
title: "NPC knowledge web"
tags:
  - "vision"
created: "2026-11-19"
modified: "2026-11-19"
---

A view of what an NPC knows, drawn as circles grouped by topic and joined by their `requires` and `next` relations. It shows how much is left to learn from that NPC without saying what it is.

### What the web shows

* **Known entries** are lit and colored by depth, whoever taught them: entries learned from other NPCs or sources light up too.  
* **Unknown Common, Doctrine and Expertise entries** are dark circles. A dark circle shows its depth once the entry before it in its chain is known; an entry that requires nothing shows its depth from the start.  
* **Hidden and Lost entries never show** until the character learns them.  
* **Topics** are labeled "?" until a typed hit, a choice or a known entry opens them.  
* **Reframed Doctrine** gets a ring, linked to the entry that clarifies it (see [[Knowledge entries#Beliefs and misreadings|Beliefs and misreadings]]).  
* **Counts:** Common, Doctrine and Expertise show known out of total; Hidden and Lost show only how many were found.

### Data

* The server sends unknown circles as opaque handles, per character, with no title or id, so datamining shows counts and shape only.  
* *Numbers: a web of about 40 circles costs 40 × 6 bytes plus its edges ≈ 0.5 KB per opening.*  
* *Open: NPCs whose filters match many entries (a temple priest with 150) need topics that collapse.*
