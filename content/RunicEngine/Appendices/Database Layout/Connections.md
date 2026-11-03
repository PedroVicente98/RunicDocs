---
title: "Connections"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Connections"
created: "2026-10-26"
modified: "2026-10-30"
---


## C++: no database connection

The GameServer never opens a database connection, and neither does the Cooker or the [[Tools#RunicEditor|RunicEditor]]. The simulation states what must become durable; the Platform's C++ bridge carries it to the Go services; only Go services hold [[Physical layout Proposal|PostgreSQL]] connections. A slow database therefore delays a result by some ticks, never the tick itself, and a retried operation commits once.

| Piece | Where | What it does |
| :---- | :---- | :---- |
| SimulationPort | RunicEngine · Runic::Simulation ([[SIM-5\|SIM-5]]), header-only Runic::SimulationPort | Outbox of durable operations with stable IDs and an inbox of results drained at safe ticks. The Engine's only door to persistence; it knows no service, SQL or protocol. |
| Persistence bridge | RunicGame · RunicGame::Server (Source/Server/Persistence) | Decides what is durable: builds EnterWorld, GrantLoot, Checkpoint and the other operations from [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] state, and applies their results. The Game's only C++ that knows durable state exists. |
| ServicesBridgeLayer | RunicPlatform · server bindings ([[PBND-1\|PBND-1]], [[PBND-4\|PBND-4]]) | Implements the service port: asynchronous gRPC calls and NATS publish and subscribe on I/O threads, completions queued for safe ticks. The only C++ that holds network clients to services. |
| Snapshot contributors | RunicEngine · DistributedSimulation ([[DSIM-3\|DSIM-3]]) | Handoff between simulations moves state simulation to simulation, never through the database. |

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

## What the simulation sends and receives

| Flow | Channel | Service | Tables touched |
| :---- | :---- | :---- | :---- |
| Enter world | gRPC, parallel | Character.Load, Inventory.Load, Quest.LoadActive, Guild and Family summary | character.\*, inventory.owner\_containers, ledger.\*, quest.quest\_progress, guild.\*, family.\* |
| Region load (a simulation takes authority) | gRPC | Territory, World, Housing, Commerce: LoadRegion(region\_id) | territory.nodes, castles; world.world\_bosses, routine\_exceptions, rifts; housing.properties, crops, animals; commerce.trade\_packs on the ground or floating |
| Loot, consume, craft, upgrade | gRPC with op ID | Inventory, Economy, Character ([[Labor\|labor]]) | ledger.operations and items, wallet.entries, economy.upgrade\_attempts, character.labor\_events, production.craft\_log |
| Trade, auction, mail, job board | gRPC with op ID | Trade, Economy, Mail | trade.\*, economy.listings and sales, jobs.\*, ledger and wallet in one transaction |
| Quest, kill and map facts | NATS JetStream (replayable) | Quest, Character, Rankings, Territory | quest.processed\_facts and quest\_progress, character.bestiary and map\_knowledge, ranking.\*, territory.node\_contributions |
| Checkpoint | gRPC batch, about every 60 s (proposal), on logout and on world transition | Character.Checkpoint | character.character\_checkpoint, character\_effects, durable\_cooldowns |
| Behavior summaries | NATS, lossy stream | Behavior scoring | behavior.minute\_summaries |
| Inbound to the simulation | NATS subscriptions, delivered at safe ticks | Directives, Moderation, Guild, Territory, Mail | Weather and current events, mutes and kicks, guild and family changes for nameplates and hostility, node owner and auction tax changes, mail notices |

## Go: one pool per service, one schema per service

Each service opens one pool (pgx) through PgBouncer with its own role and search\_path, wraps every operation in the SDK's idempotent transaction and writes the facts it publishes into its outbox in the same transaction.

| Service | Layer | Code | Schemas it owns |
| :---- | :---- | :---- | :---- |
| Accounts and Admission | Platform | RunicPlatform/services/accounts | account, ticket, directory |
| [[Platform and operations#Simulation placement\|World Coordinator]] | Platform | RunicPlatform/services/coordinator | coordinator |
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

## Numbers

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

---

↑ [[Database Layout|Database Layout]] · ← [[Where each thing lives|Where each thing lives]] · [[Schemas|Schemas]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Connections · exported 2026-11-03
