---
title: "Conversations"
tags:
  - "vision"
created: "2026-11-19"
modified: "2026-11-19"
---

How a conversation with an NPC reveals knowledge. [[Conversation demo]] shows these rules in action.

### Dialogue layers

* **Templated dialogue in layers:** base connectors every NPC has, then role, region, location, profession and unique layers. A more specific layer replaces or adds to a more general one, so a lower priest in another town keeps the same dialogue with that town's flavor.  
* **Phrase pools:** every kind of answer has several equivalent lines that NPCs cycle through. Formulaic, but never identical.  
* **Unique dialogue** only where it matters, such as a king or a high priest.  
* **Story dialogue is separate:** fixed lines and choices, written with the mission. It can give knowledge unprompted.  
* **Volunteering:** an NPC can offer an entry unprompted, usually a Common one.

### Choices and typing

* **One query system serves both.** Choices can be full sentences and carry intent; typing searches word by word.  
* **Choices give knowledge.** They come from what the character has: the NPC's role topics, follow-ups to what it just learned, leads, items it can show and story beats.  
* **Typing digs.** A typed word that matches a topic the NPC knows opens that topic: its name appears on the [[NPC knowledge web]] and new choices appear. Typing never gives knowledge directly.  
* Words match a topic's keywords and synonyms ("altar", "altars", "shrine").  
* Hidden and Lost keywords only match when the character holds a lead for them.  
* *Proposal: the first hit on a topic with an NPC gives Language XP. The Language level raises maximum patience (e.g. from 3 to 6) and, higher up, adds near-miss hints ("she knows something close to that").*

### Leads

* A lead is a primed topic: the character knows something exists, from another NPC, a book, an overheard line, a showing or an NPC's wants, without knowing what it is.  
* A lead can be asked about as a choice or typed. An NPC who doesn't hold it answers like any "doesn't know".

### Showing

* The character can show an item or other evidence ("Show the inscription"). It works like a choice whose condition is the item (`item:x`), and it can give knowledge or a lead.

### Patience

* Every NPC has patience for each character. A typed word it doesn't know and an offer it doesn't want cost patience. Other actions cost nothing, but the game never says which actions cost.  
* **Patience refills on a hard real-time timer**, per NPC and character, that nothing can bypass.  
* **At 0, every knowledge option disappears:** typing, choices, showing and offers, even the ones that cost nothing, so they can't be tried. Only quest dialogue and services (bank, vendor and the like) remain.  
* *Open: whether players see the patience meter, the base amount and the refill time (e.g. one point every 15 minutes).*  
* *Numbers: patience lives in server memory only for recent conversations, about 5 bytes × 20 NPCs × 1,000 online players ≈ 100 KB.*
