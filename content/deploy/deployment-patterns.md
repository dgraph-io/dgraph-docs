+++
title = "Deployment Patterns"
weight = 3
type = "docs"
[menu.main]
  identifier = "deployment-patterns"
  parent = "deploy"
+++

This guide covers different Dgraph deployment patterns, from simple development setups to production-grade highly available clusters.

## Pattern Selection Guide

| Pattern | Use Case | Nodes | HA | Sharding | Data Loss Risk |
|---------|----------|-------|----|---------|----|
| Standalone | Local dev, learning | 1 Alpha | ❌ | ❌ | High |
| Single Group Basic | Dev/Test environments | 1 Zero, 1 Alpha | ❌ | ❌ | High |
| Single Group HA | Small production, <1TB | 3 Zeros, 3 Alphas | ✅ | ❌ | Low |
| Multi-Group Basic | Large datasets, no HA | 1 Zero, 3+ Alphas | ❌ | ✅ | Medium |
| Multi-Group HA | Large production, >1TB | 3 Zeros, 6+ Alphas | ✅ | ✅ | Low |

---

## 1. Standalone (Learning Environment)

**Best for:** First-time users, tutorials, local experimentation

### Docker

```sh
docker run -d -p 8080:8080 -p 9080:9080 \
  -v ~/dgraph:/dgraph \
  --name dgraph \
  dgraph/standalone:latest
```

**Includes:** Zero + Alpha in one container
**Access:** Ratel UI at `http://localhost:8080`

### Command Line (Linux)

```sh
# Terminal 1: Start Zero
dgraph zero --my=localhost:5080

# Terminal 2: Start Alpha
dgraph alpha --my=localhost:7080 --zero=localhost:5080
```

**Pros:** Quick to start, minimal resources
**Cons:** No HA, no persistence guarantees, not for production

---

## 2. Single Group - Basic (Development)

**Best for:** Development teams, staging environments, CI/CD

### Architecture

```
┌──────────────┐
│  Dgraph Zero │ :5080, :6080
└──────┬───────┘
       │
┌──────▼───────┐
│ Dgraph Alpha │ :7080, :8080, :9080
└──────────────┘
```

### Docker Compose

```yaml
version: "3.8"
services:
  zero:
    image: dgraph/dgraph:latest
    volumes:
      - dgraph-zero:/dgraph
    ports:
      - 5080:5080
      - 6080:6080
    command: dgraph zero --my=zero:5080
    
  alpha:
    image: dgraph/dgraph:latest
    volumes:
      - dgraph-alpha:/dgraph
    ports:
      - 8080:8080
      - 9080:9080
    command: dgraph alpha --my=alpha:7080 --zero=zero:5080

volumes:
  dgraph-zero:
  dgraph-alpha:
```

Start with: `docker-compose up -d`

### Command Line

```sh
# Start Zero
dgraph zero --my=<IP>:5080 -w data/zero

# Start Alpha
dgraph alpha --my=<IP>:7080 --zero=<ZERO_IP>:5080 -p data/alpha/p -w data/alpha/w
```

**Pros:** Realistic setup, persistent storage
**Cons:** No HA, single point of failure

---

## 3. Single Group - HA (Small Production)

**Best for:** Production workloads up to 1TB, small to medium traffic

### Architecture

```
Zero Cluster (3 nodes) - Raft Group 0
    ├─ Zero 1 :5080 (Leader)
    ├─ Zero 2 :5080 (Follower)
    └─ Zero 3 :5080 (Follower)
         │
Alpha Group 1 (3 replicas) - Raft Group 1
    ├─ Alpha 1 :7080, :8080, :9080 (Leader)
    ├─ Alpha 2 :7080, :8080, :9080 (Follower)
    └─ Alpha 3 :7080, :8080, :9080 (Follower)
```

### Setup Steps

**1. Start Zero Cluster:**

```sh
# Zero 1 (on host1)
dgraph zero --my=host1:5080 --raft "idx=1" --replicas=3

# Zero 2 (on host2)
dgraph zero --my=host2:5080 --raft "idx=2" --peer=host1:5080

# Zero 3 (on host3)
dgraph zero --my=host3:5080 --raft "idx=3" --peer=host1:5080
```

**2. Start Alpha Cluster:**

```sh
# Alpha 1 (on host1)
dgraph alpha --my=host1:7080 --zero=host1:5080,host2:5080,host3:5080

# Alpha 2 (on host2)
dgraph alpha --my=host2:7080 --zero=host1:5080,host2:5080,host3:5080

# Alpha 3 (on host3)
dgraph alpha --my=host3:7080 --zero=host1:5080,host2:5080,host3:5080
```

### Kubernetes (Helm)

```sh
helm repo add dgraph https://charts.dgraph.io
helm install my-dgraph dgraph/dgraph \
  --set zero.replicaCount=3 \
  --set alpha.replicaCount=3
```

**Characteristics:**
- Tolerates 1 node failure (in each group)
- All data replicated 3x
- No sharding (all predicates on all Alphas)
- Suitable for datasets up to ~1TB

**Pros:** High availability, automatic failover
**Cons:** Storage scales vertically only

---

## 4. Multi-Group - Basic (Sharding, No HA)

**Best for:** Development with large datasets (>1TB)

### Architecture

```
┌──────────────┐
│  Dgraph Zero │ :5080
└──────┬───────┘
       │
       ├─ Group 1: Alpha 1 :7080
       ├─ Group 2: Alpha 2 :7081 (port offset)
       └─ Group 3: Alpha 3 :7082 (port offset)
```

### Setup (Single Host with Port Offsets)

```sh
# Start Zero with replicas=1 (no replication)
dgraph zero --my=localhost:5080 --replicas=1

# Start Alpha nodes with port offsets
dgraph alpha --my=localhost:7080 --zero=localhost:5080 -p data/p1 -w data/w1
dgraph alpha --my=localhost:7081 --zero=localhost:5080 -p data/p2 -w data/w2 -o 1
dgraph alpha --my=localhost:7082 --zero=localhost:5080 -p data/p3 -w data/w3 -o 2
```

**Characteristics:**
- 3 Alpha groups (no replication within groups)
- Data sharded by predicate across groups
- Horizontal storage scaling
- No fault tolerance

**Pros:** Horizontal scalability, handles large datasets
**Cons:** No HA, any node failure loses data

---

## 5. Multi-Group - HA (Production Large-Scale)

**Best for:** Production workloads >1TB, high traffic, mission-critical

### Architecture

```
Zero Cluster (3 nodes)
    └─ Replicates cluster metadata
         │
         ├─ Group 1: Alpha 1,2,3 (3 replicas)
         │   └─ Predicates: name, age, email
         │
         ├─ Group 2: Alpha 4,5,6 (3 replicas)
         │   └─ Predicates: friend, follows
         │
         └─ Group 3: Alpha 7,8,9 (3 replicas)
             └─ Predicates: location, company
```

### Setup (9 Alpha Nodes across 3 Hosts)

**Zeros (3 nodes):**
```sh
# Host 1: Zero 1
dgraph zero --my=host1:5080 --raft "idx=1" --replicas=3

# Host 2: Zero 2
dgraph zero --my=host2:5080 --raft "idx=2" --peer=host1:5080

# Host 3: Zero 3
dgraph zero --my=host3:5080 --raft "idx=3" --peer=host1:5080
```

**Alphas (3 groups × 3 replicas = 9 nodes):**

```sh
# Host 1: Alphas 1, 4, 7
dgraph alpha --my=host1:7080 --zero=host1:5080,host2:5080,host3:5080 -p p1 -w w1
dgraph alpha --my=host1:7081 --zero=host1:5080,host2:5080,host3:5080 -p p4 -w w4 -o 1
dgraph alpha --my=host1:7082 --zero=host1:5080,host2:5080,host3:5080 -p p7 -w w7 -o 2

# Host 2: Alphas 2, 5, 8
dgraph alpha --my=host2:7080 --zero=host1:5080,host2:5080,host3:5080 -p p2 -w w2
dgraph alpha --my=host2:7081 --zero=host1:5080,host2:5080,host3:5080 -p p5 -w w5 -o 1
dgraph alpha --my=host2:7082 --zero=host1:5080,host2:5080,host3:5080 -p p8 -w w8 -o 2

# Host 3: Alphas 3, 6, 9
dgraph alpha --my=host3:7080 --zero=host1:5080,host2:5080,host3:5080 -p p3 -w w3
dgraph alpha --my=host3:7081 --zero=host1:5080,host2:5080,host3:5080 -p p6 -w w6 -o 1
dgraph alpha --my=host3:7082 --zero=host1:5080,host2:5080,host3:5080 -p p9 -w w9 -o 2
```

**Group Assignment:**
- Zero automatically assigns Alphas 1,2,3 → Group 1
- Zero assigns Alphas 4,5,6 → Group 2
- Zero assigns Alphas 7,8,9 → Group 3

**Characteristics:**
- 3 groups with 3x replication each
- Tolerates 1 node failure per group
- Data sharded across groups
- All predicates replicated 3x within their group

**Pros:** Maximum scalability and availability
**Cons:** Higher operational complexity, more resources

---

## Best Practices

### Node Placement

1. **Different Physical Hosts**: Run each replica on a separate machine
2. **Availability Zones**: Distribute across 3 AZs when possible
3. **Network Latency**: Keep inter-node latency <5ms for best performance

### Resource Planning

| Deployment | CPUs/Node | RAM/Node | Disk/Node |
|------------|-----------|----------|-----------|
| Development | 2 cores | 4GB | 50GB |
| Small Production | 8 cores | 16GB | 250GB SSD |
| Large Production | 16 cores | 32GB | 1TB NVMe |

### Scaling Strategy

**Vertical First:**
1. Start with HA single-group (3 Alphas)
2. Increase CPU/RAM per node as load grows

**Horizontal When:**
1. Dataset >1TB
2. Query latency increases despite vertical scaling
3. Need to isolate hot predicates

**Add 3 Alphas at a time** to maintain replication factor

---

## Deployment Checklist

Before production deployment:

- [ ] Set `--replicas=3` on Zero nodes
- [ ] Configure persistent storage volumes
- [ ] Enable TLS for client connections
- [ ] Set up IP whitelisting for admin endpoints
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Set up binary backups (Enterprise)
- [ ] Test failover scenarios
- [ ] Document cluster topology
- [ ] Plan capacity for 2x growth

---

## Next Steps

- [Configure Security]({{< relref "security" >}})
- [Set Up Monitoring]({{< relref "monitoring.md" >}})
- [Production Checklist]({{< relref "production-checklist.md" >}})
- [Administration Guide]({{< relref "admin" >}})
