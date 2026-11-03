---
title: "RunicEngine — Appendix: Database Layout"
tags:
  - "archive"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
created: "2026-10-26"
modified: "2026-10-30"
---

Design appendix from the conversation of 26 October 2026, to be merged later into the technical architecture. It lays out every PostgreSQL schema, table and column, which service owns each, and where C++ and Go reach the database. Items built on existing decisions are marked as such; everything new is a Proposal until reviewed. Numbers are estimates for planning.  
Interactive map with relationship diagrams per schema: [Runic Database Map](https://claude.ai/artifact/GnVBh8fVBYPhck9onfEjRR)  
Size: 32 schemas, 167 tables, 1,042 columns.

## Decisions this layout builds on

* PostgreSQL is the only database; every service is built on the Platform Go SDK (Architecture v4, PSDK-2).  
* The C++ simulation never talks to a database. The Engine may not depend on databases, gRPC or NATS, and nothing blocks the 30 Hz tick (principle 5).  
* The simulation sends durable operations through the Engine's service port (SIM-5); the Platform's ServicesBridgeLayer turns them into asynchronous gRPC calls and NATS messages (PBND-1, PBND-4), and results come back at safe ticks.  
* Every durable change is an operation with an ID, so retries are safe. Durable writes happen at explicit boundaries: logout, trade, upgrade, loot, world transition and the periodic checkpoint.  
* The item ledger and the currency wallets are Platform mechanisms with no game rules (PBB-1 to PBB-3); the Game's Inventory, Economy and Trade services apply the rules.  
* Accounts are global; worlds (shards) are hosted in regional datacenters.  
* Game definitions (items, skills, creatures, quests, nodes) are data files with namespaced ContentIds, cooked and loaded by server and services. The database stores references to them, never the definitions.

## Physical layout (Proposal)

| Part | What it is |
| :---- | :---- |
| Global cluster | One PostgreSQL cluster for the account, ticket and directory schemas. Read by login and server select only; the simulations never touch it, and they verify tickets with public keys they already hold. |
| Shard database | One database per shard (a world in the docs' sense) with every shard schema: the Platform's coordinator, instance, directive, social, ledger and wallet, and all Game schemas. Proposal: start with one PostgreSQL cluster per datacenter holding all its shard databases; a busy shard moves to its own cluster with no schema change. |
| Schema per service | Each Go service owns one or more schemas and has its own database role with rights only on them. No service reads another's tables; it asks the owner over gRPC or listens to its NATS facts. Columns marked REF are logical references across schemas, without a foreign key constraint. |
| Ledger and wallet together | The ledger and wallet schemas sit in the same database, so the Platform can move items and currency in one transaction (PBB-3, used by trades, auctions and mail). |
| PgBouncer | Transaction pooling in front of each cluster, so many service replicas share a small number of server connections. |
| Partitioning | Append-only history (ledger entries, wallet entries, chat log, labor events, sales, behavior summaries, audit) is partitioned by time, so old partitions are archived to object storage or dropped by retention instead of deleted row by row. |
| Object storage | Report evidence (the last-60-second captures) and archived partitions live in S3-compatible object storage; PostgreSQL keeps only their keys. |
| Migrations | Each service owns forward-only migrations in its own folder, applied by the SDK at deploy. |

## Conventions (Proposal)

| Value | Type | Rule |
| :---- | :---- | :---- |
| IDs | bigint (int64) | Matches the Engine's 64-bit IDs. Proposal: persistent entities (characters, ships, trade packs, crops, survey tools) use their database ID as their GlobalEntityId, with the kind in the top bits. |
| Operation IDs | uuid (128-bit) | SimulationId plus sequence for operations the simulation starts (stable event IDs, EVT-1); services make their own for theirs. |
| World positions | double precision × 3 | WorldPosition is 64-bit (decided); stored as pos\_x, pos\_y, pos\_z with the real Y. |
| Local offsets | real | Furniture inside a house is a local 32-bit offset, never a world position. |
| Money | bigint | Smallest currency unit; no floating point anywhere near money. |
| Real time | timestamptz | Cooldowns, expiries, schedules. |
| World time | bigint milliseconds | Since the map's world epoch (coordinator.maps), so every simulation agrees. |
| Content references | text | Namespaced ContentIds such as game:item/iron\_sword, validated by services at boot against the cooked data. |
| Game-defined blobs | jsonb | Only where the shape belongs to the Game and is read whole: item payload, quest branches, appearance sliders. |
| Concurrency | version int | Optimistic concurrency on rows several writers touch. |

## Where each thing lives

Mobs, stats and definitions are not database rows. The database holds only what must survive a restart and cannot be recomputed.

| Thing | Content (cooked data) | Simulation (memory) | Database |
| :---- | :---- | :---- | :---- |
| Creatures and mobs | Definitions, stats, AI trees, loot tables, spawn areas and routines | Every live mob: HP, threat, position, AI memory | No row per mob. Only world bosses, bestiary knowledge, routine exceptions and kill-based lockouts |
| Character stats | Formulas and base values per race, class, level and gear | Resolved attributes: level, gear, build and buffs together | Never stored; rebuilt on load. Only effects that outlive a session (character\_effects) |
| Characters | Races, classes, skill definitions | Position, health, statuses, cooldowns, combat state | Character row, build, checkpoint, progression, durable cooldowns |
| Items | Item definitions, grades, recipes | A mirror of equipped items and their modifiers (GPL-4) | Every item instance in the ledger: owner, slot, payload |
| Skills | Skills, trees, timelines | Timelines, cooldowns, input queue | Points spent, milestone choices, skill bars |
| Quests and story | Quest and chapter definitions | Quest runtime: objectives advance in the same tick | Progress, completions, rewards, branches taken |
| World | Regions, volumes, node borders and connections, spawn areas, routes, water | Loaded cells, spawned resources, routine positions | Node state, castles, houses, crops, animals, trade packs, events, rifts |
| Currency | Currency definitions | Nothing; the simulation only requests changes | Wallets with double-entry history |
| Map knowledge | The cell grid from the cook | Cells crossed since the last batch | Bitsets per Lineage, map, layer and kind |
| Soundtrack and client settings | Albums shipped with the game | Nothing | Nothing: playlists stay on the player's machine (local profile) |

## Connections

### C++: no database connection

The GameServer never opens a database connection, and neither does the Cooker or the RunicEditor. The simulation states what must become durable; the Platform's C++ bridge carries it to the Go services; only Go services hold PostgreSQL connections. A slow database therefore delays a result by some ticks, never the tick itself, and a retried operation commits once.

| Piece | Where | What it does |
| :---- | :---- | :---- |
| SimulationPort | RunicEngine · Runic::Simulation (SIM-5), header-only Runic::SimulationPort | Outbox of durable operations with stable IDs and an inbox of results drained at safe ticks. The Engine's only door to persistence; it knows no service, SQL or protocol. |
| Persistence bridge | RunicGame · RunicGame::Server (Source/Server/Persistence) | Decides what is durable: builds EnterWorld, GrantLoot, Checkpoint and the other operations from Flecs state, and applies their results. The Game's only C++ that knows durable state exists. |
| ServicesBridgeLayer | RunicPlatform · server bindings (PBND-1, PBND-4) | Implements the service port: asynchronous gRPC calls and NATS publish and subscribe on I/O threads, completions queued for safe ticks. The only C++ that holds network clients to services. |
| Snapshot contributors | RunicEngine · DistributedSimulation (DSIM-3) | Handoff between simulations moves state simulation to simulation, never through the database. |

```cpp
// Illustrative, not a frozen API. RunicGame::Server persistence bridge.
// The simulation never sees SQL, a connection or a service address.
void OnLootRolled(SimContext& sim, const LootRolled& fact) {
    sim.ServicePort().Submit({
        .id      = fact.stableId,                 // SimulationId + sequence
        .service = ServiceId::Inventory,
        .method  = "GrantLoot",
        .payload = EncodeGrant(fact),
    });
}

// At the safe point of a later tick:
for (const OpResult& r : sim.ServicePort().DrainResults())
    ApplyGrantResult(sim.World(), r);             // mirror the ledger in Flecs (GPL-4)
```

### What the simulation sends and receives

| Flow | Channel | Service | Tables touched |
| :---- | :---- | :---- | :---- |
| Enter world | gRPC, parallel | Character.Load, Inventory.Load, Quest.LoadActive, Guild and Family summary | character.\*, inventory.owner\_containers, ledger.\*, quest.quest\_progress, guild.\*, family.\* |
| Region load (a simulation takes authority) | gRPC | Territory, World, Housing, Commerce: LoadRegion(region\_id) | territory.nodes, castles; world.world\_bosses, routine\_exceptions, rifts; housing.properties, crops, animals; commerce.trade\_packs on the ground or floating |
| Loot, consume, craft, upgrade | gRPC with op ID | Inventory, Economy, Character (labor) | ledger.operations and items, wallet.entries, economy.upgrade\_attempts, character.labor\_events, production.craft\_log |
| Trade, auction, mail, job board | gRPC with op ID | Trade, Economy, Mail | trade.\*, economy.listings and sales, jobs.\*, ledger and wallet in one transaction |
| Quest, kill and map facts | NATS JetStream (replayable) | Quest, Character, Rankings, Territory | quest.processed\_facts and quest\_progress, character.bestiary and map\_knowledge, ranking.\*, territory.node\_contributions |
| Checkpoint | gRPC batch, about every 60 s (proposal), on logout and on world transition | Character.Checkpoint | character.character\_checkpoint, character\_effects, durable\_cooldowns |
| Behavior summaries | NATS, lossy stream | Behavior scoring | behavior.minute\_summaries |
| Inbound to the simulation | NATS subscriptions, delivered at safe ticks | Directives, Moderation, Guild, Territory, Mail | Weather and current events, mutes and kicks, guild and family changes for nameplates and hostility, node owner and auction tax changes, mail notices |

### Go: one pool per service, one schema per service

Each service opens one pool (pgx) through PgBouncer with its own role and search\_path, wraps every operation in the SDK's idempotent transaction and writes the facts it publishes into its outbox in the same transaction.

| Service | Layer | Code | Schemas it owns |
| :---- | :---- | :---- | :---- |
| Accounts and Admission | Platform | RunicPlatform/services/accounts | account, ticket, directory |
| World Coordinator | Platform | RunicPlatform/services/coordinator | coordinator |
| Instance allocation | Platform | RunicPlatform/services/instances | instance |
| World directives | Platform | RunicPlatform/services/directives | directive |
| Chat and party groups | Platform | RunicPlatform/services/social | social |
| Item ledger and wallets | Platform | RunicPlatform/services/ledger | ledger, wallet |
| Character | Game | RunicGame/Services/character | character, cartography, justice, production |
| Inventory | Game | RunicGame/Services/inventory | inventory, vehicle |
| Quest | Game | RunicGame/Services/quest | quest |
| Economy | Game | RunicGame/Services/economy | economy, commerce, jobs |
| Trade | Game | RunicGame/Services/trade | trade |
| Mail | Game | RunicGame/Services/mail | mail |
| Guild | Game | RunicGame/Services/guild | guild, family |
| Housing | Game | RunicGame/Services/housing | housing, access |
| Territory (new) | Game | RunicGame/Services/territory | territory |
| World events and World routines | Game | RunicGame/Services/world | world |
| Rankings | Game | RunicGame/Services/ranking | ranking |
| Moderation | Game | RunicGame/Services/moderation | moderation |
| Behavior scoring | Game | RunicGame/Services/behavior | behavior |
| Deploy pipeline | Game | CI | content (read-only mirror) |

```go
// Illustrative, not a frozen API. RunicGame/Services/inventory/grant.go
// One pool per service, its own role, its own schema (search_path=inventory).
func (s *Service) GrantLoot(ctx context.Context, req *pb.GrantLoot) (*pb.GrantResult, error) {
    return sdk.Idempotent(ctx, s.db, req.OpId, func(tx sdk.Tx) (*pb.GrantResult, error) {
        bag, err := s.containers.Role(tx, "character", req.CharacterId, "bag", "-")
        if err != nil { return nil, err }
        res, err := s.ledger.Grant(ctx, req.OpId, bag, req.Items) // Platform ledger, same op ID
        if err != nil { return nil, err }
        tx.Exec(`UPDATE loot_grants SET status='committed', ledger_op=$1 WHERE grant_id=$1`, req.OpId)
        tx.Outbox("inventory.loot_granted", res)                   // published to NATS after commit
        return res, nil
    })
}
```

### Numbers

| Load | Estimate |
| :---- | :---- |
| Checkpoints | 5,000 players every 60 s ≈ 83 upserts per second per shard, about 200 bytes each ≈ 17 KB/s |
| Loot | If every player loots once a minute: ≈ 83 ledger operations per second, 3 to 5 row writes each |
| Headroom | A PostgreSQL primary on 8 vCPU and NVMe handles thousands of small write transactions per second, so these loads use a small fraction of it (order of magnitude; measure) |
| Connections | About 20 services × 2 replicas × 10 pooled connections ≈ 400 client connections; PgBouncer serves them with about 50 to 80 server connections |
| Items | 50,000 characters × 300 items × about 250 bytes ≈ 3.75 GB plus indexes |
| Item history | At 83 operations per second × 4 entries × 250 bytes ≈ 7 GB a day at full load, which is why ledger entries are partitioned monthly and archived |
| Map knowledge | 18 KB raw per 600 km² surface layer per kind; sparse bitsets compress well, so about 20 to 60 KB per Lineage in practice (estimate) |
| Behavior | 1.8 GB a day at 10,000 players (Security appendix), kept 14 days |

## Schemas

Notation: PK primary key (several PK columns \= composite key), UQ unique, → foreign key inside the schema, ⇢ logical reference to another service's schema (no constraint), null \= nullable; every other column is NOT NULL. double \= double precision.

### account — Accounts service (PCS-1)

*Platform · global cluster · Built on decisions.* Accounts, credentials, devices, sessions and entitlements. Accounts are global; everything game-side lives in the shard databases.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| accounts | account\_id bigint PK; global\_player\_id bigint UQ; email citext UQ; email\_verified\_at timestamptz null; status text; home\_datacenter text; locale text; created\_at timestamptz; last\_login\_at timestamptz null; version int | One per person. GlobalPlayerId is issued here. — global\_player\_id: GlobalPlayerId (CORE-1); status: active, suspended, banned, closed; home\_datacenter: sa, na, eu; version: optimistic concurrency |
| credentials | account\_id bigint PK → accounts; password\_hash text; password\_changed\_at timestamptz; breach\_checked\_at timestamptz null | Password data kept apart from the profile. — password\_hash: Argon2id; breach\_checked\_at: known-breach check on new passwords |
| mfa\_factors | factor\_id bigint PK; account\_id bigint → accounts; kind text; secret\_ref text; label text null; created\_at timestamptz; last\_used\_at timestamptz null | 2FA with authenticator apps and passkeys. — kind: totp, passkey; secret\_ref: encrypted secret or passkey public key |
| devices | device\_id bigint PK; account\_id bigint → accounts; fingerprint\_hash bytea; first\_seen\_at timestamptz; last\_seen\_at timestamptz; trusted\_at timestamptz null | New-device detection; unique per (account\_id, fingerprint\_hash). — first\_seen\_at: the Trade service reads it for new-device holds |
| sessions | session\_id uuid PK; account\_id bigint → accounts; device\_id bigint → devices; ip\_hash bytea; created\_at timestamptz; expires\_at timestamptz; revoked\_at timestamptz null | Login sessions; sign-out everywhere revokes all. |
| login\_attempts | attempt\_id bigint PK; account\_id bigint → accounts null; ip\_hash bytea; success bool; at timestamptz | Rate limits per address and per account. 30-day retention. Partitioned daily. |
| email\_tokens | token\_hash bytea PK; account\_id bigint → accounts; purpose text; expires\_at timestamptz; used\_at timestamptz null | Verification, password reset and new-device emails. — purpose: verify, reset, new\_device |
| entitlements | entitlement\_id bigint PK; account\_id bigint → accounts; kind text; starts\_at timestamptz; ends\_at timestamptz null; source\_ref text; created\_at timestamptz | Early access, subscription, free tier, purchases (launch phases). — kind: subscription, early\_access, free\_tier, purchase; source\_ref: payment provider reference |
| entitlement\_events | event\_id bigint PK; entitlement\_id bigint → entitlements; kind text; payload jsonb null; at timestamptz | History of every entitlement change. — kind: granted, renewed, expired, refunded |

### ticket — Accounts service (PCS-1)

*Platform · global cluster · Built on decisions.* Signing keys for connect tickets. Tickets are short-lived and never stored; simulations verify them locally with the public halves.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| signing\_keys | key\_id text PK; purpose text; public\_key bytea; private\_key\_ref text; created\_at timestamptz; activates\_at timestamptz; retires\_at timestamptz null | Rotating keys; development keys are a separate set that never works in production. — purpose: production, development; public\_key: loaded by every simulation; private\_key\_ref: secret-store path; the key itself is never in the database |

### directory — Accounts and Admission services (PCS-1, PCS-6)

*Platform · global cluster · Proposal.* The list of shards for server select, capacity, the login queue and an index of where each account has characters.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| shards | shard\_id int PK; name text UQ; datacenter text; status text; population\_band text; opened\_at timestamptz | A shard is what the docs call a world: one server copy of the game, with its own database. — datacenter: sa, na, eu; status: open, locked, maintenance, closed; population\_band: shown in server select |
| shard\_capacity | shard\_id int PK → shards; max\_concurrent int; queue\_enabled bool; updated\_at timestamptz | Per-shard capacity limits for the launch phases. |
| lineage\_index | account\_id bigint PK ⇢ account.accounts; shard\_id int PK → shards; lineage\_id bigint; character\_count smallint; last\_played\_at timestamptz null | Lets server select show the account's characters without querying every shard. PK (account\_id, shard\_id). — lineage\_id: id inside that shard's database |
| login\_queue | entry\_id bigint PK; shard\_id int → shards; account\_id bigint ⇢ account.accounts; cohort\_id text → admission\_cohorts null; enqueued\_at timestamptz; admitted\_at timestamptz null | Persisted queue so a restart keeps everyone's place. |
| admission\_cohorts | cohort\_id text PK; rule jsonb; opens\_at timestamptz | Waves by account cohort for the gradual free-to-play phase. |

### coordinator — World Coordinator (PCS-2, PCS-7)

*Platform · shard database · Built on decisions.* Maps, regions, neighbors, live simulations and who owns what. Operational state the Coordinator must recover after its own restart.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| maps | map\_id int PK; content\_id text; kind text; world\_epoch\_ms bigint | The Engine's WorldId: the main world, the sky world, instance maps. — map\_id: WorldId; content\_id: game:map/...; kind: main, persistent, instance\_template; world\_epoch\_ms: start of world time for the Environment clock |
| regions | region\_id int PK; map\_id int → maps; content\_id text; origin\_x double; origin\_y double; origin\_z double; boundary jsonb; content\_build text | Cooked regions with their 64-bit origin. — origin\_x: WorldPosition, 64-bit; boundary: polygon from the cook; content\_build: cook build that produced it |
| region\_neighbors | region\_id int PK → regions; neighbor\_id int PK → regions; border\_kind text | Neighbor topology for handoff candidates. PK (region\_id, neighbor\_id). — border\_kind: land, sea, sky |
| simulations | simulation\_id bigint PK; pod\_name text; node\_name text; state text; vcpus smallint; started\_at timestamptz; heartbeat\_at timestamptz | Running GameServer pods. — simulation\_id: SimulationId; state: starting, ready, draining, shutdown |
| authority\_assignments | assignment\_id bigint PK; region\_id int → regions; partition\_bounds jsonb null; simulation\_id bigint → simulations; epoch bigint; assigned\_at timestamptz; released\_at timestamptz null | Which simulation owns a region or an authority partition, with its epoch. — partition\_bounds: null \= the whole region; never cuts an indivisible volume; epoch: AuthorityEpoch |
| placement\_moves | move\_id bigint PK; simulation\_id bigint → simulations; from\_node text; to\_node text; reason text; started\_at timestamptz; finished\_at timestamptz null | Move-by-handoff history (load, traffic, resize). — reason: load, traffic, resize |

### instance — Instance allocation (PCS-4)

*Platform · shard database · Built on decisions.* Instances allocated from Agones fleets: dungeons, raids, naval raids, the Market Isle, rifts, arenas.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| instances | instance\_id bigint PK; map\_id int ⇢ coordinator.maps; kind text; simulation\_id bigint ⇢ coordinator.simulations null; owner\_group\_id bigint ⇢ social.parties null; state text; created\_at timestamptz; closes\_at timestamptz null | One row per allocated copy of a map. — instance\_id: InstanceId; kind: dungeon, raid, naval\_raid, shop\_island, rift, battleground, arena; state: allocating, ready, running, closing, closed |
| instance\_members | instance\_id bigint PK → instances; entity\_id bigint PK; joined\_at timestamptz; left\_at timestamptz null | Who entered. PK (instance\_id, entity\_id). — entity\_id: a character's GlobalEntityId |

### directive — World directives (PCS-3)

*Platform · shard database · Built on decisions.* Time-boxed world-wide overrides (weather, wind, current) with an effective world time and a duration.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| directives | directive\_id bigint PK; kind text; target jsonb; payload jsonb; effective\_world\_ms bigint; duration\_ms bigint; source text; created\_by bigint null; created\_at timestamptz; cancelled\_at timestamptz null | Delivered to every simulation through NATS; applied at the same world time everywhere. — kind: weather, wind, current, custom; target: region, node or area; effective\_world\_ms: world time, not wall time; source: the Game service or operator panel that asked |

### social — Chat and party groups (PCS-5)

*Platform · shard database · Built on decisions.* Parties and raid groups, friends and blocks, chat channels and a short chat log for moderation.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| parties | party\_id bigint PK; kind text; leader\_entity\_id bigint; loot\_rule jsonb; created\_at timestamptz; disbanded\_at timestamptz null | Parties and raid groups (up to 40). — kind: party, raid |
| party\_members | party\_id bigint PK → parties; entity\_id bigint PK; subgroup smallint; joined\_at timestamptz | PK (party\_id, entity\_id). — subgroup: raid groups of five |
| relations | subject\_entity\_id bigint PK; object\_entity\_id bigint PK; kind text PK; created\_at timestamptz | Friends and blocks. PK (subject, object, kind). — kind: friend, block |
| chat\_channels | channel\_id bigint PK; kind text; scope\_ref bigint null; created\_at timestamptz | Say, party, guild, faction, region, whisper, custom. — scope\_ref: guild, party or region the channel belongs to |
| chat\_log | message\_id bigint PK; channel\_id bigint → chat\_channels; sender\_entity\_id bigint; body text; flags int; sent\_at timestamptz | Kept 30 days (example) as moderation evidence. Partitioned daily. — flags: filtered, reported |

### ledger — Item ledger (PBB-1)

*Platform · shard database (same database as wallet) · Built on decisions.* Containers, slots and item instances with atomic transfers and operation IDs. Mechanisms only: the Game gives meaning to owner kinds, container kinds and the item payload.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| containers | container\_id bigint PK; owner\_kind text; owner\_id bigint; kind text; scope text null; capacity int; created\_at timestamptz; version int | Any place an item can be: bag, equipment, storage, guild bank, house chest, mail, escrow. — owner\_kind: opaque to the Platform: character, lineage, guild, house, ship, mail, escrow...; kind: game-defined: bag, equipment, storage, profession\_kit...; scope: game-defined location, e.g. a guild bank's city; capacity: expansions are ledger operations |
| items | item\_id bigint PK; template\_id text; quantity int; container\_id bigint → containers; slot int; payload jsonb; created\_op uuid → operations; created\_at timestamptz; version int | Every item instance. UNIQUE (container\_id, slot). — template\_id: ContentId of the item definition; payload: game-defined: grade, durability, binding, infusion, crafter, chart edition... |
| operations | op\_id uuid PK; kind text; requested\_by text; request\_hash bytea; status text; created\_at timestamptz; committed\_at timestamptz null | One row per durable item operation; the idempotency key of the ledger. — op\_id: SimulationId \+ sequence, or service-made; kind: grant, move, split, merge, consume, destroy, capacity; requested\_by: service name; status: committed, rejected, compensated |
| operation\_entries | entry\_id bigint PK; op\_id uuid → operations; item\_id bigint; template\_id text; from\_container bigint null; from\_slot int null; to\_container bigint null; to\_slot int null; quantity\_delta int; payload\_before jsonb null; payload\_after jsonb null | Audit history of every item movement. Never deleted. Partitioned monthly. — item\_id: not an FK: the item may be destroyed |
| supply\_counters | template\_id text PK; period\_start date PK; created bigint; destroyed bigint | Supply per item type and period (Security appendix). PK (template\_id, period\_start). |
| compensations | compensation\_id bigint PK; original\_op uuid → operations; compensating\_op uuid → operations; reason text; approved\_by bigint; at timestamptz | Rollback by a compensating operation, never by deleting history. |

### wallet — Currency wallets (PBB-2, PBB-3)

*Platform · shard database (same database as ledger) · Built on decisions.* Balances and atomic transfers in double entry: every transfer's entries sum to zero, and faucets and sinks are system wallets. Same database as the ledger so item and currency move in one transaction.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| wallets | wallet\_id bigint PK; owner\_kind text; owner\_id bigint; currency\_id text; balance bigint; version int | UNIQUE (owner\_kind, owner\_id, currency\_id). — owner\_kind: character, lineage, guild, node, escrow, system; currency\_id: ContentId: gold, honor, profession tokens, Market Isle coins...; balance: CHECK \>= 0, smallest unit |
| system\_wallets | wallet\_id bigint PK → wallets; purpose text | Faucets and sinks, so the economy's inflow and outflow are visible. — purpose: loot\_faucet, npc\_vendor\_sink, tax\_sink, repair\_sink, quest\_faucet... |
| transfers | op\_id uuid PK; kind text; requested\_by text; status text; created\_at timestamptz; committed\_at timestamptz null | One per currency operation; shares the op\_id space with the ledger. — status: committed, rejected, compensated |
| entries | entry\_id bigint PK; op\_id uuid → transfers; wallet\_id bigint → wallets; delta bigint; balance\_after bigint | Double-entry lines. Partitioned monthly. |
| currency\_supply | currency\_id text PK; period\_start date PK; minted bigint; burned bigint | Minted and burned per period. PK (currency\_id, period\_start). |

### character — Character service (GSVC-1, 5, 7, 10)

*Game · shard database · Built on decisions.* Lineage (the account inside a shard) and characters: progression, build, checkpoint, professions, exploration, faction and crime, map knowledge, Altars, collections, labor.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| lineages | lineage\_id bigint PK; account\_id bigint UQ ⇢ account.accounts; labor int; labor\_reserve int; labor\_updated\_at timestamptz; online\_character\_id bigint → characters null; created\_at timestamptz; version int | The account inside this shard. Labor, map knowledge, the Altars shown on the map and collections are account-wide, so they hang here; respawn and teleports use each character's own discovered Altars. — labor: current labor; labor\_reserve: return bonus, up to twice the bar, never expires; labor\_updated\_at: regeneration is computed from this, never ticked; online\_character\_id: one character online per account |
| characters | character\_id bigint PK; lineage\_id bigint → lineages; name citext UQ; race\_id text; faction\_id text; level smallint; xp bigint; title\_id text null; state text; played\_seconds bigint; created\_at timestamptz; last\_login\_at timestamptz null; last\_logout\_at timestamptz null; deleted\_at timestamptz null; version int | One playable character. — character\_id: also its GlobalEntityId (proposal); race\_id: ContentId; faction\_id: ContentId; state: active, locked, deleted; deleted\_at: restore window |
| character\_appearance | character\_id bigint PK → characters; body jsonb; voice\_id text null; updated\_at timestamptz | Character creation data (BDO-style sliders). |
| character\_checkpoint | character\_id bigint PK → characters; map\_id int; instance\_id bigint; region\_id int; pos\_x double; pos\_y double; pos\_z double; yaw real; health int; resources jsonb; saved\_at timestamptz; source\_op uuid | Where and how the character was at the last checkpoint. Written only by the simulation, through the bridge. — map\_id: WorldId; instance\_id: 0 \= the open world; pos\_x: WorldPosition, 64-bit; resources: mana, stamina and other resources; source\_op: the checkpoint operation |
| character\_effects | character\_id bigint PK → characters; effect\_id text PK; source\_ref text; stacks smallint; expires\_at timestamptz null; remaining\_ms int null; payload jsonb null | Effects that outlive a session (food, wedding guest buff). Combat statuses never come here. PK (character\_id, effect\_id). — effect\_id: ContentId; expires\_at: real-time effects; remaining\_ms: effects that pause while offline |
| durable\_cooldowns | character\_id bigint PK → characters; cooldown\_key text PK; ready\_at timestamptz | Long cooldowns that must survive logout: teleport, Outlaw toggle, Altar reset, divorce lock. PK (character\_id, cooldown\_key). |
| character\_build | character\_id bigint PK → characters; weapon\_set\_id text; discipline\_id text; altar\_locked\_at timestamptz; reset\_count int; version int | The named class: fixed weapon set plus Discipline, chosen and locked at the Altar. — weapon\_set\_id: ContentId of the class's weapon set; discipline\_id: ContentId |
| skill\_allocations | character\_id bigint PK → characters; tree\_kind text PK; skill\_id text PK; tier smallint; rank smallint | Points spent per tree; class trees are the merge of weapon and Discipline skills. PK (character\_id, tree\_kind, skill\_id). — tree\_kind: discipline, mount, aerial |
| milestone\_choices | character\_id bigint PK → characters; milestone\_level smallint PK; choice\_id text; chosen\_at timestamptz | Level milestone choices (e.g. level 35: fire, ice or lightning); changed only by an Altar reset. |
| skill\_bars | character\_id bigint PK → characters; bar\_kind text PK; slot smallint PK; skill\_id text | Bar layout per context. PK (character\_id, bar\_kind, slot). — bar\_kind: main, mount, aerial |
| ui\_layout | character\_id bigint PK → characters; layout jsonb; updated\_at timestamptz | Movable and hideable panels and keybinds, roaming between machines. |
| professions | character\_id bigint PK → characters; profession\_id text PK; proficiency bigint; mastery\_slot smallint null; mastered\_at timestamptz null | Proficiency per profession; three active masteries per character (adjustable), enforced by the service. — mastery\_slot: 1 to 3 |
| exploration | character\_id bigint PK → characters; exploration\_xp bigint; unspent bigint; updated\_at timestamptz | Exploration XP, separate from combat progression. |
| adventurer\_unlocks | character\_id bigint PK → characters; unlock\_id text PK; rank smallint; bought\_at timestamptz | Exploration shop: flight, stamina ranks, moving objects. PK (character\_id, unlock\_id). |
| faction\_state | character\_id bigint PK → characters; participation text; outlaw bool; outlaw\_since timestamptz null; outlaw\_locked\_until timestamptz null; infamy int; pirate bool; changed\_at timestamptz | PvP or PvE mode, Outlaw and Infamy, pirate status. Mirrored in the simulation. — participation: pvp, pve; outlaw\_locked\_until: the toggle cooldown, reset by attacks on the own faction |
| infamy\_reports | report\_id bigint PK; offender\_id bigint → characters; reporter\_id bigint → characters; victim\_id bigint null; amount int; region\_id int; at timestamptz | Reports that raised Infamy. |
| titles | character\_id bigint PK → characters; title\_id text PK; earned\_at timestamptz | Earned titles. PK (character\_id, title\_id). |
| loot\_lockouts | character\_id bigint PK → characters; lockout\_id text PK; week\_start date PK; loot\_count smallint; last\_at timestamptz | Raid loot 3 times a week, world boss once (adjustable). PK (character\_id, lockout\_id, week\_start). — lockout\_id: raid or boss ContentId |
| name\_history | character\_id bigint PK → characters; changed\_at timestamptz PK; old\_name citext | Renames, for moderation. PK (character\_id, changed\_at). |
| lineage\_altars | lineage\_id bigint PK → lineages; altar\_id text PK; discovered\_at timestamptz | Altars the Lineage has found, shown on the map only; respawn and teleports use the Altars the character itself has discovered (character\_altar\_visits, proposed). PK (lineage\_id, altar\_id). |
| map\_knowledge | lineage\_id bigint PK → lineages; map\_id int PK; layer text PK; kind text PK; bitmap bytea; version int; updated\_at timestamptz | One bit per 64 m cell, per map layer and knowledge kind. About 18 KB raw for a 600 km² surface layer, much less compressed. — layer: y band: surface, underground, sky; kind: discovered, mapped\_terrain, mobs, events, resources, currents...; bitmap: zstd-compressed bitset |
| learned\_charts | lineage\_id bigint PK → lineages; edition\_id bigint PK ⇢ cartography.chart\_editions; learned\_at timestamptz | Charts read by the Lineage. PK (lineage\_id, edition\_id). |
| collections | lineage\_id bigint PK → lineages; kind text PK; content\_id text PK; source text; unlocked\_at timestamptz | Account-wide collections: wardrobe, mounts, pets, emotes. PK (lineage\_id, kind, content\_id). |
| bestiary | lineage\_id bigint PK → lineages; creature\_id text PK; kills int; observation smallint; unlocked\_tiers int; first\_seen\_at timestamptz | Knowledge from kills and observation. PK (lineage\_id, creature\_id). — unlocked\_tiers: bitmask |
| labor\_events | event\_id bigint PK; lineage\_id bigint → lineages; delta int; reason text; profession\_id text null; op\_id uuid null; at timestamptz | Every labor gain and spend, with the profession that spent it. Partitioned monthly. |

### cartography — Character service

*Game · shard database · Built on decisions.* Chart editions, survey jobs and the triangulation tools placed in the world, and perishable information.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| chart\_editions | edition\_id bigint PK; chart\_kind text; region\_id int; node\_id text null; season text null; coverage bytea; created\_at timestamptz | A chart's content: kind, area, season. Chart items point to an edition in their payload. — chart\_kind: land, nautical, mobs, resources, events...; coverage: cells this edition covers |
| survey\_jobs | job\_id bigint PK; character\_id bigint ⇢ character.characters; node\_id text ⇢ territory.nodes; chart\_kind text; state text; score real null; result\_edition\_id bigint → chart\_editions null; started\_at timestamptz | A survey in progress at one node; scored by geometry only. — state: placing, measuring, done, failed, abandoned |
| survey\_markers | marker\_id bigint PK; job\_id bigint → survey\_jobs; item\_id bigint ⇢ ledger.items; pos\_x double; pos\_y double; pos\_z double; state text; destroyed\_by bigint null; placed\_at timestamptz | The three tools placed in the world; others can destroy them. — marker\_id: GlobalEntityId of the placed tool; item\_id: the tool item, recovered or lost; state: placed, recovered, destroyed |
| perishable\_reports | report\_id bigint PK; kind text; node\_id text ⇢ territory.nodes; data jsonb; item\_id bigint ⇢ ledger.items null; expires\_at timestamptz | Rotating resource richness and event timers that expire. — kind: resource\_richness, event\_timer |

### justice — Character service

*Game · shard database · Proposal.* ArcheAge-style trials with player jurors and judges. Still an idea in the Vision; tables shown so the shape is known.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| trials | trial\_id bigint PK; defendant\_id bigint ⇢ character.characters; infamy\_at\_trial int; judge\_id bigint ⇢ character.characters null; state text; verdict text null; sentence\_minutes int null; scheduled\_at timestamptz; decided\_at timestamptz null | A trial for a character with enough Infamy. — state: pending, in\_session, decided, expired |
| trial\_jurors | trial\_id bigint PK → trials; juror\_id bigint PK ⇢ character.characters; vote text null; voted\_at timestamptz null | PK (trial\_id, juror\_id). |
| jail\_sentences | sentence\_id bigint PK; character\_id bigint ⇢ character.characters; trial\_id bigint → trials null; starts\_at timestamptz; ends\_at timestamptz; served\_seconds int; released\_at timestamptz null | Time served, kept across logouts. |

### inventory — Inventory service (GSVC-2)

*Game · shard database · Built on decisions.* Game meaning over the Platform ledger: which container is whose bag, equipment, profession kit or global storage; loot grants; supply alerts.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| owner\_containers | owner\_kind text PK; owner\_id bigint PK; role text PK; scope text PK; container\_id bigint UQ ⇢ ledger.containers; created\_at timestamptz | Maps a game role to a ledger container. PK (owner\_kind, owner\_id, role, scope). — owner\_kind: character, lineage, guild, house, ship; role: bag, equipment, profession\_kit:mining, storage, guild\_bank, house\_chest, library...; scope: bank location for the guild bank, '-' otherwise (personal storage is one global chest) |
| loot\_grants | grant\_id uuid PK; character\_id bigint ⇢ character.characters; source text; status text; ledger\_op uuid ⇢ ledger.operations null; created\_at timestamptz | A loot grant is applied once across reconnects. — grant\_id: the kill fact's stable ID; source: kill, chest, quest, event, coin\_purse; status: pending, committed, rejected |
| supply\_alerts | alert\_id bigint PK; template\_id text; period date; threshold bigint; observed bigint; raised\_at timestamptz; acknowledged\_by bigint null | Daily supply alerts from the ledger counters. |

### vehicle — Inventory service

*Game · shard database · Proposal.* State that belongs to summon items: ships with their stations, mounts, and ship construction sites.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| ships | ship\_id bigint PK; summon\_item\_id bigint UQ ⇢ ledger.items; owner\_id bigint ⇢ character.characters; template\_id text; name text null; hull\_hp int; state text; permission\_level text; last\_pos\_x double null; last\_pos\_y double null; last\_pos\_z double null; summoned\_at timestamptz null; version int | A ship lives as a summon item; this row holds its state between summons. — ship\_id: GlobalEntityId while summoned; template\_id: clipper, brigantine, galleon...; state: stored, summoned, sinking, sunk, destroyed; permission\_level: crew, party, guild, anyone |
| ship\_stations | ship\_id bigint PK → ships; station\_key text PK; hp int; state text; ammo int null | Each station is destroyed and repaired separately. PK (ship\_id, station\_key). — station\_key: cannon\_port\_1, sail\_main, repair, arcane, archer...; state: ok, destroyed |
| mounts | mount\_id bigint PK; summon\_item\_id bigint UQ ⇢ ledger.items; owner\_id bigint ⇢ character.characters; template\_id text; name text null; level smallint; xp bigint; state text; revive\_at timestamptz null; kit\_mods jsonb | Mount state between summons. — state: stabled, summoned, downed; kit\_mods: skill changes the mount brings |
| construction\_sites | site\_id bigint PK; owner\_id bigint ⇢ character.characters; design\_template\_id text; port\_node\_id text ⇢ territory.nodes; pos\_x double; pos\_y double; pos\_z double; delivered jsonb; state text; created\_at timestamptz; expires\_at timestamptz | Ship platform from a Market Isle design; returns the design if unfinished in about 4 h. — site\_id: GlobalEntityId of the platform; delivered: packs delivered so far; state: building, completed, expired |

### quest — Quest service (GSVC-3)

*Game · shard database · Built on decisions.* Quest progress and rewards, stored idempotently from quest facts; branching story chapters and skips for alts.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| quest\_progress | character\_id bigint PK ⇢ character.characters; quest\_id text PK; state text; branch jsonb; objectives jsonb; started\_at timestamptz; updated\_at timestamptz; completed\_at timestamptz null; version int | Active and finished quests. PK (character\_id, quest\_id). — state: active, completed, failed, abandoned; branch: choices taken so far (quests are trees); objectives: counter per objective |
| quest\_completions | character\_id bigint PK ⇢ character.characters; quest\_id text PK; times int; last\_completed\_at timestamptz | Repeatables and profession quest lines. PK (character\_id, quest\_id). |
| processed\_facts | fact\_id uuid PK; character\_id bigint ⇢ character.characters; quest\_id text; applied\_at timestamptz | Every quest fact applied, by its stable ID: a replayed fact changes nothing. Partitioned weekly. |
| quest\_rewards | reward\_op uuid PK; character\_id bigint ⇢ character.characters; quest\_id text; ledger\_op uuid ⇢ ledger.operations null; wallet\_op uuid ⇢ wallet.transfers null; status text; created\_at timestamptz | Reward commits through the ledger and wallets. |
| story\_progress | character\_id bigint PK ⇢ character.characters; chapter\_id text PK; branch\_path jsonb; completed\_at timestamptz null | Main story chapters with every branch kept for replay. PK (character\_id, chapter\_id). |
| lineage\_story\_skips | lineage\_id bigint PK ⇢ character.lineages; chapter\_id text PK; first\_completed\_at timestamptz | Chapters an alt of the same account may skip. PK (lineage\_id, chapter\_id). |

### economy — Economy service (GSVC-4)

*Game · shard database · Built on decisions.* Upgrades and their RNG, the global auction, price history and bounds, the black market, Market Isle limits.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| upgrade\_attempts | attempt\_op uuid PK; character\_id bigint ⇢ character.characters; item\_id bigint ⇢ ledger.items; kind text; before jsonb; after jsonb; success bool; at timestamptz | Upgrades, grade attempts, rerolls and dismantling (destroys the item and returns part of its materials; a unique effect becomes a gem holding an Infusion Rune). Partitioned monthly. — kind: level, grade, reroll, dismantle |
| pity\_counters | lineage\_id bigint PK ⇢ character.lineages; counter\_key text PK; value int; updated\_at timestamptz | Guarantee counters live on the server, never the client. PK (lineage\_id, counter\_key). |
| auction\_houses | house\_id int PK; node\_id text ⇢ territory.nodes; faction\_scope text null | Auction counters where players list and claim; every counter serves the same global auction. |
| listings | listing\_id bigint PK; house\_id int → auction\_houses; seller\_id bigint ⇢ character.characters; item\_id bigint ⇢ ledger.items; template\_id text; quantity int; unit\_price bigint; currency\_id text; status text; listed\_at timestamptz; expires\_at timestamptz | Listed items wait in the auction's escrow container until they sell. The seller fills a gross or a net price and the buyer pays the listed price; an expired listing sends a mail notice and is claimed at any counter. — house\_id: the counter where it was listed; status: active, sold, expired, claimed, cancelled |
| sales | sale\_id bigint PK; listing\_id bigint → listings; buyer\_id bigint ⇢ character.characters; quantity int; unit\_price bigint; tax bigint; at timestamptz | Every sale with the seller's tax, kept entirely by the NPC as a sink. Partitioned monthly. |
| price\_history | template\_id text PK; day date PK; low bigint; high bigint; avg\_price bigint; volume int | Daily figures of the global auction; the 7-day median feeds node missions, pack payouts and the black market. PK (template\_id, day). |
| price\_bounds | template\_id text PK; min\_price bigint; max\_price bigint; set\_by bigint; updated\_at timestamptz | Minimum and maximum price per item, tunable by admins. When an item is out of stock or above the maximum, an NPC listing sells it at a high price. |
| vendor\_limits | lineage\_id bigint PK ⇢ character.lineages; offer\_id text PK; period\_start date PK; bought int | Market Isle purchase limits. PK (lineage\_id, offer\_id, period\_start). |

### commerce — Economy service

*Game · shard database · Built on decisions.* Trade packs: world entities, not inventory items, with their origin node and the route a Go service records; pack demand per region and the black market's stock.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| trade\_packs | pack\_id bigint PK; template\_id text; origin\_node\_id text ⇢ territory.nodes; crafted\_by bigint ⇢ character.characters; state text; holder\_entity\_id bigint null; map\_id int null; pos\_x double null; pos\_y double null; pos\_z double null; delivery\_node\_id text ⇢ territory.nodes null; payout bigint null; crafted\_at timestamptz; delivered\_at timestamptz null; version int | A pack's durable state; floating packs stay until a hard reset. — pack\_id: GlobalEntityId; state: carried, cargo, dropped, floating, delivered, destroyed; holder\_entity\_id: carrier or vehicle |
| pack\_route | pack\_id bigint PK → trade\_packs; seq smallint PK; node\_id text ⇢ territory.nodes; danger smallint; entered\_at timestamptz | Nodes passed; repeats and loops are ignored when pricing. PK (pack\_id, seq). — danger: danger level when passed |

### trade — Trade service (GSVC-4)

*Game · shard database · Built on decisions.* Two-party trades with confirmations, and the transfer holds for new devices and young accounts.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| trade\_sessions | trade\_id bigint PK; a\_character\_id bigint ⇢ character.characters; b\_character\_id bigint ⇢ character.characters; state text; a\_confirmed bool; b\_confirmed bool; op\_id uuid ⇢ ledger.operations null; created\_at timestamptz | Commits as one ledger plus wallet operation. — state: open, locked, committed, cancelled |
| trade\_offers | trade\_id bigint PK → trade\_sessions; side char PK; line smallint PK; item\_id bigint ⇢ ledger.items null; quantity int null; currency\_id text null; amount bigint null | PK (trade\_id, side, line). — side: a or b |
| transfer\_holds | hold\_id bigint PK; account\_id bigint ⇢ account.accounts; reason text; until timestamptz; created\_at timestamptz | New-device and young-account holds on trade, mail and auction withdrawals. — reason: new\_device, young\_account |

### jobs — Economy service

*Game · shard database · Built on decisions.* The community job board with its internal bank: a job can be taken without the collateral; failing leaves a negative balance that blocks new jobs.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| job\_postings | job\_id bigint PK; poster\_id bigint ⇢ character.characters; kind text; node\_id text ⇢ territory.nodes null; spec jsonb; reward bigint; collateral bigint; currency\_id text; escrow\_wallet\_id bigint ⇢ wallet.wallets; state text; deadline\_at timestamptz; created\_at timestamptz | A job and its escrowed reward. — kind: craft, gather, deliver, ceremony...; spec: what must be delivered; state: open, taken, delivered, cancelled, failed, expired |
| job\_assignments | job\_id bigint PK → job\_postings; worker\_id bigint ⇢ character.characters; collateral\_mode text; state text; taken\_at timestamptz; due\_at timestamptz; closed\_at timestamptz null | Who took the job and how the collateral was covered. — collateral\_mode: paid, borrowed; state: active, delivered, cancelled, failed |
| board\_accounts | character\_id bigint PK ⇢ character.characters; balance bigint; blocked bool; updated\_at timestamptz | The board's internal bank; the only balance in the game that may go negative. — balance: below zero \= debt; blocked: true while balance \< 0 |
| board\_entries | entry\_id bigint PK; character\_id bigint → board\_accounts; job\_id bigint → job\_postings null; delta bigint; reason text; at timestamptz | Every debt and repayment. |

### territory — Territory service (new)

*Game · shard database · Proposal. Regions and nodes with prosperity, weekly missions, owner guilds and their fixed weekly payout; weekly node wars; castles on the neutral continent.* Not yet in the Architecture's service list.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| nodes | node\_id text PK; region\_id int; parent\_node\_id text → nodes null; kind text; owner\_guild\_id bigint ⇢ guild.guilds null; prosperity smallint; full\_weeks smallint; specialty text null; war\_cost\_bp int; updated\_at timestamptz; version int | One per node; static data (borders, connections, climate) stays in content. A game region is a city node plus the child nodes whose parent it is; a guild owns up to 3 nodes or one region, never both. — node\_id: ContentId; parent\_node\_id: the region's city node, null for the city itself and for transitional nodes; kind: city, capital, village, mine, forest, farm, port, island, transitional; prosperity: 1 to 5, unused for transitional nodes; full\_weeks: 100% weeks toward the next level, not necessarily consecutive, reset when the level changes; war\_cost\_bp: automatic cost while at war |
| node\_missions | node\_id text PK → nodes; week\_start date PK; mission\_kind text PK; template\_id text null; quota int; delivered int; fixed\_price bigint null | This week's missions for the node, about three rotating kinds per node type, not all deliveries. PK (node\_id, week\_start, mission\_kind). — fixed\_price: set when posted, above the market, fixed for the week |
| node\_contributions | contribution\_id bigint PK; node\_id text → nodes; week\_start date; character\_id bigint ⇢ character.characters; template\_id text; quantity int; at timestamptz | Deliveries by anyone, PvE players included. Partitioned monthly. |
| node\_week\_results | node\_id text PK → nodes; week\_start date PK; completion\_pct smallint; level\_before smallint; level\_after smallint | 60% keeps the level, two 100% weeks raise it, level 5 needs 100%; 150% and 200% give a temporary buff, never a level. PK (node\_id, week\_start). |
| node\_ownership | node\_id text PK → nodes; since timestamptz PK; guild\_id bigint ⇢ guild.guilds; until timestamptz null; via\_war\_id bigint → node\_wars null | History of owners. PK (node\_id, since). |
| node\_wars | war\_id bigint PK; node\_id text → nodes; attacker\_guild\_id bigint ⇢ guild.guilds; defender\_guild\_id bigint ⇢ guild.guilds null; week\_start date; scheduled\_at timestamptz; state text; winner\_guild\_id bigint null | One challenge per guild per week: UNIQUE (attacker\_guild\_id, week\_start). — state: scheduled, running, resolved, cancelled |
| guild\_payouts | node\_id text PK → nodes; period\_start date PK; guild\_id bigint ⇢ guild.guilds; amount bigint | Fixed weekly payout to the ruling guild by tier and prosperity, with mission and project bonuses inside the cap. PK (node\_id, period\_start). |
| resource\_richness | node\_id text PK → nodes; resource\_kind text PK; richness smallint; rotates\_at timestamptz | Rotating richness per resource kind. PK (node\_id, resource\_kind). |
| castles | castle\_id bigint PK; region\_id int UQ; zone\_id text; guild\_id bigint ⇢ guild.guilds; state text; hp int; built\_at timestamptz | Neutral continent only: one castle per region, in one of its designated zones; fixed once placed. On the faction continents the ruling guild uses the city and an exclusive guild building. — state: building, standing, damaged |
| castle\_structures | structure\_id bigint PK; castle\_id bigint → castles; kind text; hp int; state text | Walls, gates and buildings with their own HP. |

### mail — Mail service

*Game · shard database · Built on decisions.* Mail headers and claim state. Mail carries items; postage is charged per unit and grows with the item's tier or value, and claimed items go to the inventory or the global chest.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| mails | mail\_id bigint PK; sender\_id bigint ⇢ character.characters null; recipient\_id bigint ⇢ character.characters; subject text; body text; attachment\_container\_id bigint ⇢ ledger.containers null; postage bigint; cod\_amount bigint null; sent\_at timestamptz; opened\_at timestamptz null; claimed\_at timestamptz null; expires\_at timestamptz | Attachments travel in a ledger container owned by the mail. — sender\_id: null \= system mail; postage: per unit, weighted by tier or value |

### guild — Guild service

*Game · shard database · Built on decisions.* Guilds, ranks and permissions, members, applications, guild log, bank permissions per location, alliances.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| guilds | guild\_id bigint PK; faction\_id text; name citext UQ; tag text null; leader\_id bigint ⇢ character.characters; level smallint; xp bigint; alliance\_id bigint → alliances null; created\_at timestamptz; disbanded\_at timestamptz null; version int | One guild. |
| guild\_ranks | rank\_id bigint PK; guild\_id bigint → guilds; name text; position smallint; permissions bigint | Ranks with a permission bitmask. |
| guild\_members | character\_id bigint PK ⇢ character.characters; guild\_id bigint → guilds; rank\_id bigint → guild\_ranks; contribution bigint; joined\_at timestamptz | One guild per character. |
| guild\_applications | application\_id bigint PK; guild\_id bigint → guilds; character\_id bigint ⇢ character.characters; kind text; message text null; state text; created\_at timestamptz | Applications and invites. — kind: application, invite |
| guild\_log | entry\_id bigint PK; guild\_id bigint → guilds; actor\_id bigint; kind text; payload jsonb null; at timestamptz | Joins, kicks, bank moves, wars. Partitioned monthly. |
| bank\_permissions | guild\_id bigint PK → guilds; scope text PK; rank\_id bigint PK → guild\_ranks; tab smallint PK; can\_deposit bool; withdraw\_per\_day int | Guild banks are local; permissions per bank location, rank and tab. — scope: bank location |
| alliances | alliance\_id bigint PK; name citext UQ; created\_at timestamptz; dissolved\_at timestamptz null | Alliances are a system; admins regulate informal ones. |
| alliance\_members | alliance\_id bigint PK → alliances; guild\_id bigint PK → guilds; joined\_at timestamptz | PK (alliance\_id, guild\_id). |

### family — Guild service

*Game · shard database · Built on decisions.* Family (ArcheAge-style mini guild per character, may mix factions) and marriage, which is per character, between different Lineages.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| families | family\_id bigint PK; name citext UQ; leader\_id bigint ⇢ character.characters; created\_at timestamptz; disbanded\_at timestamptz null | One family. |
| family\_members | character\_id bigint PK ⇢ character.characters; family\_id bigint → families; role text; joined\_at timestamptz | One family per character. |
| marriages | marriage\_id bigint PK; character\_a bigint ⇢ character.characters; character\_b bigint ⇢ character.characters; family\_name text null; altar\_id text; officiant\_id bigint null; state text; divorce\_by bigint null; divorce\_requested\_at timestamptz null; divorce\_effective\_at timestamptz null; remarry\_lock\_until timestamptz null; ceremony\_at timestamptz | Ceremony at an Altar; unilateral divorce takes about 48 h, together it is instant. One active marriage per character (partial unique index). — family\_name: optional couple name, the account name is unchanged; officiant\_id: null \= NPC priest; state: active, divorce\_pending, divorced |
| marriage\_guests | marriage\_id bigint PK → marriages; character\_id bigint PK ⇢ character.characters; buff\_until timestamptz | Guests get a small buff for a few hours. PK (marriage\_id, character\_id). |

### access — Housing service

*Game · shard database · Built on decisions.* Permissions per resource and per character. Lineage-mates and spouses get access by rule, not by rows, so permissions never chain through several marriages.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| grants | grant\_id bigint PK; resource\_kind text; resource\_id bigint; grantee\_kind text; grantee\_id bigint null; mask int; granted\_by bigint ⇢ character.characters; granted\_at timestamptz; expires\_at timestamptz null | Who may use, open, pilot, harvest or manage something. — resource\_kind: house, farm, ship, chest, vehicle, item; grantee\_kind: character, family, guild, party, public; mask: use, open, pilot, harvest, manage |

### housing — Housing service

*Game · shard database · Built on decisions.* Open-world land: zones, plots, properties built from designs, construction stages, furniture, crops and animals.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| land\_zones | zone\_id text PK; region\_id int; node\_id text ⇢ territory.nodes null; kind text; open bool | Where housing and farms may be built. — zone\_id: ContentId; kind: housing, farm, mixed; open: new areas open over time |
| plots | plot\_id bigint PK; zone\_id text → land\_zones; grid\_x int; grid\_z int; size text | Grid slots. UNIQUE (zone\_id, grid\_x, grid\_z). |
| properties | property\_id bigint PK; plot\_id bigint UQ → plots; owner\_lineage\_id bigint ⇢ character.lineages; owner\_character\_id bigint ⇢ character.characters; design\_template\_id text; state text; built\_at timestamptz null; upkeep\_due\_at timestamptz; frozen\_at timestamptz null; version int | A house or farm; the count per Lineage is limited by content rules. — state: constructing, complete, frozen, demolished |
| construction\_progress | property\_id bigint PK → properties; stage smallint PK; required jsonb; delivered jsonb | Materials per construction stage. PK (property\_id, stage). |
| furniture | furniture\_id bigint PK; property\_id bigint → properties; item\_id bigint ⇢ ledger.items; local\_x real; local\_y real; local\_z real; yaw real | Placed furniture, local to the property. — local\_x: 32-bit: local offset, not a world position |
| crops | crop\_id bigint PK; property\_id bigint → properties null; planter\_id bigint ⇢ character.characters; seed\_template text; pos\_x double; pos\_y double; pos\_z double; state text; planted\_at timestamptz; ready\_at timestamptz; tended\_at timestamptz null | Planted crops, on a plot or in the open world. — crop\_id: GlobalEntityId; state: growing, ready, withered, harvested |
| animals | animal\_id bigint PK; property\_id bigint → properties; species\_template text; state text; born\_at timestamptz; last\_cared\_at timestamptz; sick\_since timestamptz null | Neglected animals get sick but never die; only slaughter removes them. — state: young, adult, sick, slaughtered |

### world — World events and World routines services (GWTH-1, GSVC-9)

*Game · shard database · Built on decisions.* Event schedules and runs, world bosses, divine events, routine exceptions, operator events, Chaos rifts.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| event\_schedule | schedule\_id bigint PK; event\_id text; cycle\_ms bigint; jitter\_ms int; next\_at timestamptz; enabled bool | Recurring events on a cycle that does not match the clock. — event\_id: ContentId |
| event\_runs | run\_id bigint PK; event\_id text; kind text; region\_id int null; node\_id text ⇢ territory.nodes null; state text; triggered\_by bigint null; outcome jsonb null; announced\_at timestamptz null; started\_at timestamptz null; ended\_at timestamptz null | Every event that happened, including capital invasions and divine events. — kind: scheduled, dynamic, admin, divine, invasion; state: announced, running, completed, failed |
| event\_participants | run\_id bigint PK → event\_runs; character\_id bigint PK ⇢ character.characters; contribution int; reward\_op uuid null | PK (run\_id, character\_id). |
| world\_bosses | boss\_id text PK; state text; next\_spawn\_at timestamptz null; last\_killed\_at timestamptz null | Unique bosses, land and ocean. — boss\_id: ContentId; state: alive, dead, respawning |
| boss\_kills | kill\_id bigint PK; boss\_id text → world\_bosses; participant\_count int; top\_guild\_id bigint ⇢ guild.guilds null; killed\_at timestamptz | Kill history; contributions go to Rankings. |
| divine\_weights | weight\_id bigint PK; scope text; scope\_id text; multiplier real; reason text; set\_by bigint; until timestamptz | Admin mediation: raise the chance of divine events against a monopoly. — scope: region, guild |
| routine\_exceptions | exception\_id bigint PK; routine\_id text; entity\_id bigint null; kind text; offset\_ms bigint; cause\_fact uuid; created\_at timestamptz; fades\_at timestamptz | Player-caused exceptions to routines (a delayed escort, a sunk caravan) and how they fade back. — kind: delayed, sunk, destroyed, captured |
| operator\_events | operator\_event\_id bigint PK; kind text; target jsonb; payload jsonb; starts\_at timestamptz; duration\_ms bigint; directive\_id bigint ⇢ directive.directives null; created\_by bigint | Wind, current and weather events from the admin panel; delivered as Platform directives. — kind: wind, current, weather |
| rifts | rift\_id bigint PK; map\_id int; pos\_x double; pos\_y double; pos\_z double; theme\_creature text; level smallint; state text; instance\_id bigint ⇢ instance.instances null; opened\_at timestamptz; expires\_at timestamptz null | Chaos rifts: hidden dungeons anywhere, revealed up close or by deciphered scrolls. — state: hidden, revealed, entered, closed |
| rift\_reveals | rift\_id bigint PK → rifts; lineage\_id bigint PK ⇢ character.lineages; via\_item bigint null; revealed\_at timestamptz | Who revealed a rift. PK (rift\_id, lineage\_id). |

### ranking — Rankings service (GSVC-8)

*Game · shard database · Built on decisions.* Seasons, ranked arena ratings, match history, world boss contributions and leaderboards.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| seasons | season\_id bigint PK; kind text; starts\_at timestamptz; ends\_at timestamptz | PvP and other ranked seasons. — kind: pvp, boss, honor |
| pvp\_ratings | character\_id bigint PK ⇢ character.characters; bracket text PK; season\_id bigint PK → seasons; rating int; wins int; losses int | PK (character\_id, bracket, season\_id). — bracket: 1v1, 2v2, 3v3, 5v5 |
| pvp\_matches | match\_id bigint PK; kind text; bracket text null; instance\_id bigint ⇢ instance.instances; started\_at timestamptz; ended\_at timestamptz null | Arenas and battlegrounds. — kind: arena, battleground |
| match\_participants | match\_id bigint PK → pvp\_matches; character\_id bigint PK ⇢ character.characters; team smallint; result text; rating\_before int null; rating\_after int null; kills int; deaths int | PK (match\_id, character\_id). |
| boss\_contributions | kill\_id bigint PK ⇢ world.boss\_kills; character\_id bigint PK ⇢ character.characters; contribution int | PK (kill\_id, character\_id). |
| leaderboards | board\_id text PK; season\_id bigint PK → seasons; subject\_id bigint PK; score bigint; rank int; updated\_at timestamptz | Computed boards. PK (board\_id, season\_id, subject\_id). — subject\_id: character or guild |

### production — Character service (GSRV-7, GSVC-7)

*Game · shard database · Proposal.* Crafting history and player music compositions. Gathering and farming results arrive as ledger operations and labor events.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| craft\_log | craft\_op uuid PK; character\_id bigint ⇢ character.characters; recipe\_id text; quantity int; labor\_spent int; quality jsonb; ledger\_op uuid ⇢ ledger.operations; at timestamptz | Every craft with labor spent and quality rolls. Partitioned monthly. |
| compositions | composition\_id bigint PK; author\_id bigint ⇢ character.characters; title text; notation text; complexity smallint; created\_at timestamptz | Songs written in the note editor; score items point to them. — notation: the editor's note format |

### moderation — Moderation service (GSVC-12, GSRV-9)

*Game · shard database · Built on decisions.* Reports with evidence, sanctions, appeals and every GM action. Evidence captures live in object storage, not in PostgreSQL.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| reports | report\_id bigint PK; reporter\_id bigint ⇢ character.characters; reported\_id bigint ⇢ character.characters; reason text; evidence\_key text; weight real; status text; created\_at timestamptz | Weighted by the reporter's history. — evidence\_key: object-storage key of the last-60-s capture; status: open, reviewing, closed |
| sanctions | sanction\_id bigint PK; account\_id bigint ⇢ account.accounts; character\_id bigint ⇢ character.characters null; kind text; reason text; report\_id bigint → reports null; issued\_by bigint; starts\_at timestamptz; ends\_at timestamptz null; revoked\_at timestamptz null | Warning, mute, trade lock, temporary ban, permanent ban. |
| appeals | appeal\_id bigint PK; sanction\_id bigint UQ → sanctions; body text; state text; decided\_by bigint null; decided\_at timestamptz null | One appeal per sanction. |
| reporter\_weights | account\_id bigint PK ⇢ account.accounts; weight real; updated\_at timestamptz | Mass false reports do nothing. |
| gm\_actions | action\_id bigint PK; gm\_id bigint; kind text; target jsonb; reason text; at timestamptz | Audit of every GM action. |

### behavior — Behavior scoring service (GSVC-11)

*Game · shard database · Built on decisions.* Per-minute behavior summaries, scores, flags and ban waves. Features and thresholds stay secret and server-side.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| minute\_summaries | character\_id bigint PK ⇢ character.characters; minute timestamptz PK; summary bytea | About 128 bytes per player per minute; about 1.8 GB a day at 10,000 players. 14-day retention. PK (character\_id, minute). Partitioned daily. |
| scores | character\_id bigint PK ⇢ character.characters; model\_version int PK; score real; features jsonb; updated\_at timestamptz | PK (character\_id, model\_version). |
| flags | flag\_id bigint PK; character\_id bigint ⇢ character.characters; score real; reason text; reviewed\_by bigint null; outcome text null; created\_at timestamptz | Automation only flags; a person reviews before any permanent ban. |
| ban\_waves | wave\_id bigint PK; scheduled\_at timestamptz; executed\_at timestamptz null | Detect now, ban later in batches. |
| wave\_members | wave\_id bigint PK → ban\_waves; account\_id bigint PK ⇢ account.accounts; flag\_id bigint → flags | PK (wave\_id, account\_id). |

### content — Deploy pipeline (read-only for services)

*Game · shard database · Proposal.* Optional mirror of the cooked content catalog for admin panels and an armory site. Definitions themselves stay in the cooked Data files.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| builds | build\_id text PK; engine\_version text; published\_at timestamptz; notes text null | Each published content build. |
| entries | content\_id text PK; build\_id text PK → builds; kind text; name text; data\_hash bytea | One row per ContentId in a build. PK (content\_id, build\_id). — kind: item, skill, creature, quest, node, region, recipe, currency... |

### _std — Go SDK (PSDK-2, PSDK-3)

*Platform · every service schema · Built on decisions.* Four tables the Platform Go SDK creates in every service schema: idempotency, transactional outbox and inbox for NATS, and the audit log for privileged calls.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| idempotency\_keys | op\_id uuid PK; request\_hash bytea; response bytea; created\_at timestamptz; expires\_at timestamptz | A retried operation commits once (PSDK-2). Rows expire after the retry window. — op\_id: stable operation ID from the caller; request\_hash: same ID with a different body is rejected; response: stored answer returned on retry |
| outbox | seq bigint PK; subject text; payload bytea; created\_at timestamptz; published\_at timestamptz null | Facts written in the same transaction as the change; a relay publishes them to NATS after commit. — seq: identity; subject: NATS subject, e.g. character.checkpointed; payload: Protobuf message (Contracts) |
| inbox | message\_id uuid PK; subject text; received\_at timestamptz | NATS messages already consumed, so a redelivered message changes nothing. |
| audit\_log | audit\_id bigint PK; actor text; action text; target text; payload jsonb null; at timestamptz | Privileged calls and operator actions (Security appendix, PSDK-1). Never deleted. Partitioned monthly. — actor: service, GM or operator identity |

## Differences from the Architecture v4 and the Vision

* Naming: the Architecture uses "world" both for a server copy and for the Engine's WorldId. This layout calls the server copy a shard (shard\_id) and the Engine's WorldId a map (map\_id).  
* Map knowledge is account-wide, so it hangs on the Lineage (character.map\_knowledge); the Lineage also records the Altars it has found, for the map only (character.lineage\_altars), while respawn and teleports use each character's own discovered Altars (character\_altar\_visits, proposed).  
* Vertentes were removed, and the Architecture was updated on 30 Oct; character\_build stores the class's weapon set and the Discipline.  
* New Game services not in the Architecture's list: Territory (nodes, node wars, castles), Moderation and Behavior scoring (already in the Security appendix). The job board joins Economy, Family and marriage join Guild, Justice and Cartography join Character, Vehicles join Inventory.  
* New Platform tables: the directory schema in the global cluster (shards, capacity, login queue, lineage index for server select) and the standard per-schema tables (idempotency, outbox, inbox, audit).  
* Labor and its return reserve are account-wide (Lineage), not per character.  
* Economy review of 2026-10-30 (RunicGame — Appendix: Nodes, Economy and Exploration): one global auction whose counters all serve the same market, one global chest, the auction tax kept entirely by the NPC, mail priced per unit, regions made of a city node and its child nodes, node missions and fixed guild payouts. Proposed tables not drawn yet: region\_pack\_demand (pack price per region and type, recovering over time), black\_market\_stock (goblin price and stock per type and tier), region\_projects (structures, wear and tier limit), pack\_deliveries (payout, deliverer and crafter shares) and character\_altar\_visits (Altars each character has discovered, for respawn and teleports).

## Open

* One database per shard inside a shared cluster per datacenter, or one cluster per shard from the start.  
* Whether account-wide things (collections, map knowledge, Altars) carry across shards for an account with characters on several, or stay per shard as drawn here.  
* Checkpoint interval (60 s proposed) and whether vitals are part of it.  
* Bestiary per Lineage (drawn here) or per character.  
* The justice system (trials and jurors) is still an idea in the Vision.  
* Chat log and behavior retention periods (30 and 14 days are examples).  
* Whether the content mirror is worth having before an admin panel or armory site exists.
