---
title: "Audio (Engine, Game)"
tags:
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

Audio is client presentation only: the simulation decides what happened, RunicGame turns it into semantic audio events and music contexts, and the Engine’s audio system plays them. Players may replace the soundtrack, never sound effects, and nothing they choose can change gameplay.

### Ownership

| Part | Owner | Contains |
| :---- | :---- | :---- |
| Runic::Audio | Engine | Backend interface (implemented by GodotBridge on Godot’s AudioServer), sources and handles, buses and mixing, semantic event routing, MusicDirector, albums, soundtrack presets, local profile persistence, playback state, crossfades and transitions |
| Audio content and presentation rules | Game | Concrete music contexts, default soundtrack assignments, sound-effect event definitions, context priority, bundled music and sounds, the soundtrack settings screens |
| Soundtrack configuration | Player (local file) | Active preset, user presets, albums, track paths, playback state |
| Platform | Platform | Nothing in the soundtrack path; no service is needed |
| GameServer | Game | No audio backend, decoders, profiles or soundtrack UI |

Runic::Audio depends only on Core and Assets. It never depends on combat, AI, quests, simulation authority, Platform networking or persistence services. Godot’s AudioServer sits behind its backend interface, so the registry and the MusicDirector stay free of Godot; where the MusicDirector finally lives is an open decision (see [[Godot integration (Engine)|Godot integration]]).

![[arch-audio-routing-sound-effects-and-soundtrack.png]]
*Audio routing — sound effects and soundtrack*

*Audio routing — sound effects and soundtrack*

Both branches start from semantic identifiers the Game picks; only the soundtrack branch reads the player’s preset, so a custom or broken preset can never affect gameplay.

### Semantic sound-effect events (Engine routing, Game definitions)

Gameplay presentation code never names a file. It plays a semantic event, which the AudioEventRegistry resolves to a route and then to a source.

```cpp
// Avoid: PlaySound("Audio/Combat/SwordHit03.wav");
audio.PlayEvent("game:combat.sword_hit.light");
```

```yaml
game:combat.sword_hit.light:
  variants: [sword_hit_01, sword_hit_02, sword_hit_03]
  selection: random_no_repeat
  bus: combat_sfx
  spatial: true
  volume: 0.9
```

* **Developer features:** random, weighted, no-repeat and sequential variants; material-specific routing; pitch and volume ranges; spatial or non-spatial playback; bus assignment; live reload in development; debug inspection.

* **Not player-remappable.** A full MMORPG has thousands of sound events; exposing them would bloat settings, confuse players, add support burden and risk breaking combat readability. Routing exists for content production, not as a modding surface.

### Music contexts (Game defines, Engine resolves)

A MusicContext names a musical situation, not a track: game:music.exploration, combat, boss, farming, sailing, city, dungeon, raid, character\_select. RunicGame owns the set and may grow it.

* **Fallback chains** keep old presets valid when contexts are added: boss falls back to combat, then default; a future underwater\_exploration falls back to exploration, then the default soundtrack.

* **Priority** when several contexts are valid at once is Game presentation policy. An illustrative order: boss, raid or dungeon special state, combat, cutscene, city or sailing or farming, exploration, default.

* **Presentation cues:** server gameplay flows may emit a cue such as game:dragon\_phase\_2; the client resolves it through the active preset. Music that players cannot override is an explicit, rare Game exception.

### Soundtrack presets, albums and radio state (Engine)

A preset maps music contexts to albums. The original Runic soundtrack is itself a built-in, read-only preset using the same machinery; user presets can be created, duplicated, renamed, imported, exported and deleted.

| Album setting | Options |
| :---- | :---- |
| Playback | Sequential, Shuffle, ShuffleNoRepeat |
| Transition | Immediate, Crossfade, FinishCurrentTrack |
| Resume | ResumePreviousPosition, RestartCurrentTrack, StartNextTrack |

Each album keeps its own playback state, so switching contexts suspends a station instead of restarting it. Farming at track 4, 03:17, switches to combat at track 2, 01:11; when combat ends, farming resumes at track 4, 03:17.

```cpp
// Illustrative contract, not a frozen API.
struct MusicAlbum {
    AlbumId id;
    std::vector<MusicTrack> tracks;
    PlaybackMode playback_mode;
    TransitionMode transition_mode;
    ResumeMode resume_mode;
};

struct AlbumPlaybackState {
    TrackId current_track;
    uint32_t playlist_index;
    double playback_position_seconds;
    uint64_t shuffle_state;
};

class MusicDirector {
public:
    void SetContext(MusicContextId context);
    void SetActivePreset(SoundtrackPresetId preset);
    MusicContextId CurrentContext() const;
    SoundtrackPresetId ActivePreset() const;
};
```

### Player settings and local files (Game screens, Engine profiles)

* **Audio settings:** master, music, sound-effect and dialogue volumes, plus the active soundtrack preset.

* **Advanced soundtrack editor:** the context-to-album table for a preset, and an album editor for its tracks and its playback, transition and resume settings.

* **Local files:** ordinary audio files such as .wav, .ogg, .mp3 and .flac, as far as the chosen decoder supports them. The game never ships third-party soundtracks without rights.

* **Local persistence:** active preset, user presets, albums, track paths, context mappings, playback position, current track and shuffle state. No Platform service; cloud sync of settings could come later but is never required.

### Security and authority rules

* Soundtrack content is never executable: presets cannot load DLLs, scripts, codec plugins or native extensions disguised as audio.

* Remote streaming URLs are out of scope for now; they bring caching, privacy and network-security concerns of their own.

* The server never stores or sends player-local file paths, preset names or playback state.

* Music reacts only to facts the client may already know. No music cue may reveal something the visibility tiers hide, such as an unseen enemy starting an attack.

### Failure behavior

* A missing or unreadable track falls back in order: the next valid track in the album, then the fallback context’s album, then the Runic default soundtrack. A broken preset never crashes the client or touches gameplay.

* Importing a preset validates its schema version, context IDs, track references, playback modes and fallback configuration, and rejects executable payloads. Unknown future contexts resolve through fallbacks instead of failing the load.

### Developer tooling (Engine)

The RunicEditor and client development builds show the current music context and its fallback chain, the active preset, album, track and position, transition state, bus volumes, recent audio events, how each event resolved, missing mappings and missing user files. Developers can trigger any registered event or music context by hand.

### Acceptance tests

| Test | Passes when |
| :---- | :---- |
| Default soundtrack | With no custom profile, Runic Original is active and every context resolves to Game defaults with no backend service |
| Custom preset | Separate local albums for exploration and combat switch with the configured transition and resume from stored state |
| Radio behavior | Farming resumes at its stored track and position after combat, and after a client restart as the policy says |
| Context compatibility | An old preset without a new context resolves it through fallback and stays editable |
| Broken local track | A deleted file is skipped or falls back without a crash, and the editor reports it |
| Sound-effect boundary | An event resolves through the registry, has no player remapping UI, and is inspectable in tooling |
| Headless boundary | The GameServer builds with no audio backend or soundtrack dependency, and gameplay is identical whatever soundtrack clients use |
