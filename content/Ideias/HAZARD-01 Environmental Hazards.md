---
title: "HAZARD-01 · Environmental Hazards"
aliases:
  - "HAZARD-01"
tags:
  - "ideias"
  - "idea"
  - "status/open"
id: "HAZARD-01"
status: "Open"
source: "RunicGame — Ideias"
source_url: "https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit"
created: "2026-10-17"
modified: "2026-11-03"
---

**ID:** HAZARD-01 · **Status:** Open

Things that make navigating the world difficult, at sea and on land. They're simulated the simplest way possible, and the visuals sell the illusion. Every hazard warns before it hurts, has an answer (knowledge, a ship part, a skill or a route) and guards a reward. Hazard effects go through Resolve and Tolerance like attacks from NPCs and players; a hazard that ignores them says so in its own line (ex.: slips). *(proposal: no upkeep chores; ships take damage from events and fights, never from routine trips.)*

* **Static:** baked into the map and never changes: the ocean floor, reefs, sandbanks (shallow spots), cliffs, plateaus and glaciers. Explored and charted.  
* **Cyclic:** a seeded routine, like wind and currents: fog banks, calm zones and tides. Charted, with new editions when the seed changes.  
* **Events:** storms, giant waves, waterspouts, maelstroms, earthquakes, eruptions, floods, avalanches and mudslides. Cartographers chart and forecast the weather that can cause them ([[INTEL-01 Resource Richness and Perishable Information|INTEL-01]]) and where they can happen, but never exactly when: the server rolls each event with a hidden seed.

**Sea:**

* **Deep ocean:** most of the ocean is deep, and ships can still anchor there. Bigger swell, more giant waves and deep-sea creatures. When diving, breath drains faster below a set depth, and diving gear reduces it.  
* **Fog banks:** lower the perception radius, so ships, nameplates and reefs stay hidden until close; they drift with the wind. Charts, lighthouses, foghorns and ship bells answer them.  
* **Freezing water:** swimmers take Chill build-up, which slows them, at a rate set by each water.  
* **Glaciers and icebergs:** collision obstacles. Some drift with the current, and some are mostly underwater, so hitting one opens a breach ([[SHIP-01 Naval Combat Flooding, Repair and Sea Events|SHIP-01]]). Pack ice slows ships a lot. An ice bow, one of the ship upgrades ([[MOV-02 Travel Depth|MOV-02]]), handles ice better.  
* **Reefs and sandbanks:** static shallow spots. Hitting a reef or a sandbank deals collision damage, and a reef also opens breaches. A ship hits only the ones shallower than its draft, so a clipper passes over many that stop a galleon ([[SEA-01 Ship Handling and Sea Balance|SEA-01]]). Breaking white water shows where they are, if you can see it.  
* **Calm zones:** no wind, so sailing ships stall. Oars, currents or knowing the routine get a ship out.  
* **Storms:** extreme wind and currents, giant waves (the damage event), lightning on water that damages and stuns, waterspouts and maelstroms ([[SHIP-01 Naval Combat Flooding, Repair and Sea Events|SHIP-01]]).  
* **Waterspouts:** a moving vortex that damages sails and masts and throws players off the deck.  
* **Maelstroms:** a huge whirlpool that pulls ships in. Sailing against its current deals chip damage; the center deals heavy damage and sinks most ships in seconds if the crew doesn't act. Some rifts and raids are entered through a maelstrom. *(proposal: an entrance maelstrom looks different, ex.: a colored glow and runes in the water, so crews can tell it apart.)*  
* **More:** false lights (will-o'-wisps that look like lighthouses and lead ships onto reefs), sirens (their song gives the helmsman Madness build-up and pulls the steering toward the rocks), seafloor vents (boiling water burns swimmers and makes steam fog) and kelp forests (they slow ships and root swimmers).

**Land:**

* **Verticality:** plateaus, cliffs, ravines and uneven ground. Mounts have a slope limit, falls hurt, and some places are reached only by gliding down or climbing.  
* **Inland storms:** lightning hits high ground, and wind pushes gliders. Blizzards bring low visibility and Chill build-up; sandstorms bring low visibility and damage to anyone exposed.  
* **Rain:** each region has a rain level: none, drizzle, heavy or monsoon, like Terraria's rain. It comes from the weather routine, so cartographers can chart rainy seasons and forecast them ([[INTEL-01 Resource Richness and Perishable Information|INTEL-01]]). The higher the rain level, the higher the chance of floods and mudslides, and the more slippery the slopes.  
* **Ground:** each region also has a ground level (dry, damp, mud or soaked) that follows the rain like snow: it rises one level after some time under rain that strong or stronger, and a timer drops it one level at a time while the rain is lighter, so mud outlasts the rain. Deserts dry fast and swamps slowly. Damp is a wet look and slightly slippery steep slopes; at mud, soil, grass and farmland turn into mud, difficult terrain that slows; soaked is deep mud, slower and with no sprint. Rock, sand and paved roads never turn to mud.  
* **Slippery slopes:** wet ground and ice make characters slip on foot. The chance of slipping grows gradually with the slope angle, never a step where 30° is safe and 31° always slides, and wetter ground starts it at gentler angles. A second roll decides how bad the slip is, worse on steeper slopes: a stumble (the character stays on its feet and loses speed briefly), prone with no slide (it gets up after a moment), or prone and sliding. Each outcome fades into the next by angle, so near a transition both can happen, and a slide starts only where the slope beats the ground's grip. A slide goes straight into climbing mode, where the player holds on to grip and stop; on very steep wet rock the grip can fail and only slow the slide. Climbing on wet rock can slip the same way. Gear and drier ground push everything to steeper angles. A slip is a movement state, not a CC, so it ignores Resolve and Tolerance. *(proposal, illustrative, in mud with no gear: under 15° no slip; 15–22° up to 8% per second, stumbles; 22–28° up to 25%, stumbles or prone; 28–33° up to 50%, prone with no slide; 33–40° up to 100%, prone and sliding; over 40° always, and faster; sprinting doubles the chance and walking slowly halves it.)*  
* **Mounts on slippery ground:** mounts have a lower slope limit on wet ground and slip in the same tiers, with their own angles. Stumble: no dismount, and the mount loses a bit of speed. Prone: the mount goes prone with the rider still on it, with no slide. Slide: the rider is thrown off, and the mount goes prone and slides along with the rider to the end of the slide area, where the slope flattens. To recall it, unsummon it and summon it again. The mount keeps its health, so fall damage it took stays. Trade packs stay where they are, the mount's on the mount and the player's on the player's back; when the mount is unsummoned, its pack stays on the spot ([[TRADE-01 Trade Packs|TRADE-01]]). *(proposal: sure-footed mounts slip at steeper angles, and climbing mounts grip during a slide the way a player does.)*  
* **Floods:** as the ground gets wetter, rivers get stronger currents, then rise and widen past their banks; in a monsoon they flood their plains, low areas with no water become temporary lakes, fords close and mobs move to high ground. Canyons and dry beds get flash floods: a front of water that travels down the channel, with a rumble and dust a few seconds before. Nobody marks where: the terrain decides ([[RunicEngine — Technical Architecture|RunicEngine — Technical Architecture v4]], Land hazards). After the rain the water drains over tens of minutes, and the mud lasts longer. *(proposal, illustrative: a given canyon gets a flash flood about every 4 to 6 hours in heavy rain and about once an hour in a monsoon.)*  
* **Earthquakes:** they never change the terrain; they only open caves for a while, since a cave entrance has a closed model and an open one. Rockfalls are hazard areas. *(proposal: animals flee and dust falls a few seconds before.)*  
* **Volcanoes:** an eruption is visual effects plus hazard zones that deal fire damage at random spots and leave damaging ground behind; ash clouds lower visibility, and lava flows along fixed channels (Burn and damage). When it ends, ore richness around the volcano and its spawn script are set to their maximum.  
* **Swamps and bogs:** they slow, and gas pockets apply Poison build-up.  
* **Snow:** difficult terrain with a snow look. Each snowfield region has a snow level (none, light, heavy or deep) that rises while it snows, and a timer drops it one level at a time while it isn't snowing. Light snow is only visual, heavy snow slows, and deep snow slows a lot, blocks sprinting and keeps some mounts out. Snowshoes and snow mounts reduce the slow, drift zones at the bottom of slopes count one level deeper, and footprints are drawn only on the client.  
* **Avalanches and mudslides:** weather events on slopes found from the terrain, never something players set off easily. Avalanches happen only when the snow there is heavy or deep, mudslides only when the ground is soaked. A slide knocks down and damages whoever it hits, and its landing area becomes deep snow or mud for a while. *(proposal: a mudslide over a road blocks it until players clear it.)* The cooker generates each path (start, path and landing area), and markers drawn by hand only add, remove or adjust one (Map authoring markers, in the content pipeline appendix).  
* **Traversal gear:** like snowshoes for snow, mud and slippery ground have gear that makes them easier: mud boots for mud, and climbing spikes for slippery slopes and climbing in the rain. *(proposal: they're profession gear in the feet slot, [[EQUIP-01 Equipment Slots|EQUIP-01]].)*  
* **Roads and routes:** roads connect the main places and resist these hazards: paved roads never turn to mud, are less slippery, and are raised or bridged over the channels that flood. Players use them most of the time, but many places have no road, or the road makes a huge detour, ex.: down to the bottom of the continent and back up the whole plateau. So there's a safe long way and a dangerous short way with climbing, and rain makes the short way riskier. This is map design with geography in mind.  
* **More:** magnetic anomalies that spin the compass (there's no minimap, [[UI-01 Interface and Navigation|UI-01]]), mirages with fake landmarks, Chaos woods that loop you back unless you read the signs, and low-gravity Chaos patches.

New islands and new terrain come only with patches, never at random.

**Engine:** RunicEngine — Technical Architecture v4 (Sea hazards, Ship attachments and Land hazards).
