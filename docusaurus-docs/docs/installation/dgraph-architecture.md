---
title: Architecture
---

Dgraph is a distributed graph database built for horizontal scalability, high availability, and high performance.

## Core Components

A Dgraph cluster consists of two types of nodes working together:

### Dgraph Zero (Control Plane)

Zero nodes manage cluster coordination and metadata. Each cluster requires at least one Zero node.

**Responsibilities:**
- **Cluster Membership**: Track which Alpha nodes are part of the cluster
- **Data Distribution**: Assign predicates to Alpha groups for balanced load
- **Transaction Coordination**: Allocate transaction timestamps and UIDs
- **Rebalancing**: Automatically redistribute data as the cluster scales
- **Schema Management**: Coordinate schema changes across the cluster

**Ports:**
- `5080` - Internal gRPC (Alpha ↔ Zero communication, Live/Bulk Loader)
- `6080` - HTTP admin endpoint (cluster state, assignments)

**High Availability:**
Deploy 3 Zero nodes for fault tolerance. They form a Raft group (group 0) for consensus.

See [Zero API Reference](admin/dgraph-zero) for HTTP endpoints and administrative operations.

### Dgraph Alpha (Data Plane)

Alpha nodes store data and serve queries. Clusters need at least one Alpha node.

**Responsibilities:**
- **Data Storage**: Store graph data (nodes, edges, predicates)
- **Index Management**: Maintain indexes for efficient queries
- **Query Execution**: Process DQL and GraphQL queries
- **Mutation Handling**: Execute data mutations with ACID guarantees
- **Predicate Ownership**: Each Alpha group owns specific predicates

**Ports:**
- `7080` - Internal gRPC (Alpha ↔ Alpha, Alpha ↔ Zero)
- `8080` - External HTTP (client queries, admin)
- `9080` - External gRPC (client connections)

**High Availability:**
Deploy 3 Alphas per group for data replication. Each group forms a Raft quorum.

See [Alpha API Reference](/dgraph-overview/admin/dgraph-alpha) for health monitoring and [Admin API](admin/dgraph-administration) for backup, export, and other operations.

## Cluster Architecture

### Minimum Cluster (Development)

```
┌─────────────┐
│ Dgraph Zero │ :5080
└──────┬──────┘
       │
┌──────▼───────┐
│ Dgraph Alpha │ :7080, :8080, :9080
└──────────────┘
```

**Use case:** Local development, testing
**Configuration:** 1 Zero, 1 Alpha
**Characteristics:** No HA, no sharding

### High Availability Cluster

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Zero Node 1 │   │ Zero Node 2 │   │ Zero Node 3 │
│  (Leader)   │───│  (Follower) │───│  (Follower) │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                  │                  │
       └──────────────────┴──────────────────┘
                          │
       ┌──────────────────┴──────────────────┐
       │                  │                   │
┌──────▼───────┐   ┌──────▼──────┐    ┌──────▼──────┐
│ Alpha Node 1 │   │ Alpha Node 2│    │ Alpha Node 3│
│  (Leader)    │───│  (Follower) │────│  (Follower) │
│  Group 1     │   │  Group 1    │    │  Group 1    │
└──────────────┘   └─────────────┘    └─────────────┘
```

**Use case:** Production workloads
**Configuration:** 3 Zeros, 3 Alphas (replicas=3)
**Characteristics:**
- Tolerates 1 node failure per group
- All predicates replicated 3x
- No data sharding (single group)

### Sharded HA Cluster

```
                    Zero Cluster (3 nodes)
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    Group 1              Group 2             Group 3
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Alpha 1,2,3   │   │ Alpha 4,5,6   │   │ Alpha 7,8,9   │
│ Predicates:   │   │ Predicates:   │   │ Predicates:   │
│ - name        │   │ - friend      │   │ - location    │
│ - age         │   │ - email       │   │ - bio         │
└───────────────┘   └───────────────┘   └───────────────┘
```

**Use case:** Large datasets (>1TB), horizontal scaling
**Configuration:** 3 Zeros, 9 Alphas (3 groups × 3 replicas)
**Characteristics:**
- Data sharded across multiple groups
- Each group has 3x replication
- Horizontal scalability

## Data Model

### Predicate-Based Sharding

Unlike traditional graph databases that shard by nodes, Dgraph shards by **predicates** (relationship types):

- Each predicate is assigned to an Alpha group
- All Alpha nodes in a group serve the same predicates
- Queries for a predicate route to its owning group
- Cross-predicate queries are distributed across groups

**Example:**
```
Group 1: name, age, email
Group 2: friend, follows
Group 3: location, company
```

**Automatic Rebalancing:**

Zero continuously monitors disk usage across groups and automatically rebalances predicates to maintain even distribution:

- Runs rebalancing checks every 8-10 minutes
- Moves predicates from high-usage groups to lower-usage groups
- During a predicate move:
  - The predicate becomes temporarily read-only
  - Queries continue to be served normally
  - Mutations are rejected and should be retried after the move completes
- Each additional Alpha allows Zero to further split and redistribute predicates

### Replication and Consistency

Dgraph uses **Raft consensus** for replication. Both Zero and Alpha nodes form Raft consensus groups:

- **Raft Groups**: Nodes of the same type (all Zeros or all Alphas in a group) form a Raft group
- **Leader Election**: Each Raft group elects a single leader among its peers
- **Followers**: Non-leader nodes in a group are called followers
- **Automatic Failover**: If the leader becomes unavailable (network partition, machine shutdown), the group automatically elects a new leader to continue operations
- **Replication**: Each Alpha group uses Raft consensus for replication
- The `--replicas` flag on Zero controls replication factor per group
- Writes require majority (quorum) acknowledgment
- Linearizable reads and writes
- Snapshot isolation for transactions

**Replica Configuration:**

The `--replicas` flag determines how many nodes serve the same group:

- `--replicas=1`: No replication (single node per group)
- `--replicas=3`: 3 nodes per group, tolerates 1 node failure (recommended)
- `--replicas=5`: 5 nodes per group, tolerates 2 node failures

:::tip
Always use odd numbers for replicas (1, 3, 5) to maintain proper quorum. Even numbers (2, 4) don't provide additional fault tolerance.
:::

## Scaling Strategies

### Vertical Scaling (Per-Node)
- Add CPU cores for higher concurrency
- Add RAM for larger working sets
- Use faster SSDs for better I/O

### Horizontal Scaling

**Add Replicas (No Sharding):**
Start with `--replicas=3`, add 3 more Alphas → still 1 group, more replication (6x)

**Add Groups (Sharding):**
Start with 3 Alphas (group 1), add 3 more Alphas → Zero creates group 2, rebalances predicates

**Best Practice:**
- Keep Alpha count as multiple of `--replicas` setting
- 6 Alphas with `--replicas=3` = 2 groups with 3x replication each
- 9 Alphas with `--replicas=3` = 3 groups with 3x replication each

## Query Flow

1. **Client connects** to any Alpha node (HTTP/gRPC)
2. **Alpha parses query** and identifies required predicates
3. **Local predicates** are queried directly
4. **Remote predicates** are fetched from other Alphas via distributed joins
5. **Results are merged** and returned to client

**Performance:** N-hop queries require only N network hops, regardless of data size.

## Operational Characteristics

### Resource Requirements

| Component | CPU | Memory | Disk IOPS |
|-----------|-----|--------|-----------|
| Alpha (prod) | 8+ cores | 16GB+ | 3000+ |
| Zero (prod) | 2-4 cores | 4GB | 1000+ |

### Fault Tolerance

With 3 replicas per group:
- **1 node down**: Cluster fully operational
- **2 nodes down**: Read-only mode (no quorum for writes)
- **3 nodes down**: Group unavailable

### Backup and Recovery

- **Binary backups** (Enterprise): Incremental, production-ready
- **Exports**: Full RDF/JSON exports via admin API
- **Point-in-time recovery** available with binary backups

## Monitoring

Key metrics to monitor:
- Raft health (`/health` endpoint)
- Disk usage per Alpha
- Query latency (p50, p95, p99)
- Transaction throughput
- Pending proposals (write backpressure)

See [Monitoring](/dgraph-overview/admin/observability/monitoring) for Prometheus/Grafana setup.

## Security Considerations

- **Network Isolation**: Zero nodes can run in private network
- **TLS Encryption**: Enable for client connections and inter-node communication
- **Access Control**: Use ACL (Enterprise) for fine-grained permissions
- **IP Whitelisting**: Restrict admin endpoints to trusted IPs

## Next Steps

- [Choose a Deployment Pattern](/dgraph-overview/installation/deployment-patterns)

