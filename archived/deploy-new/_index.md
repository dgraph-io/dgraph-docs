+++
title = "Self-Managed Deployment"
weight = 9
type = "docs"
[menu.main]
  identifier = "deploy"
+++

This section covers deploying and managing Dgraph in self-managed environments, including on-premises infrastructure and cloud platforms (AWS, GCP, Azure).


---

## Documentation Structure

### Getting Started

Start here if you're new to Dgraph deployment:

- **[Getting Started]({{< relref "getting-started.md" >}})** - Installation methods and first steps
- **[Architecture]({{< relref "architecture.md" >}})** - Understanding Dgraph's distributed design

### Deployment

Learn how to deploy Dgraph for different use cases:

- **[Deployment Patterns]({{< relref "deployment-patterns" >}})** - From development to production-scale deployments
  - Standalone (learning)
  - Single group basic (development)
  - Single group HA (small production)
  - Multi-group basic (sharding without HA)
  - Multi-group HA (large-scale production)

### Configuration

Configure Dgraph for your specific needs:

- **[Configuration]({{< relref "configuration.md" >}})** - Complete configuration reference
- **[Production Checklist]({{< relref "production-checklist.md" >}})** - Ensure production-readiness

### Security

Secure your Dgraph deployment:

- **[Security Overview]({{< relref "security" >}})**
  - [TLS Configuration]({{< relref "security/tls-configuration.md" >}}) - Encryption setup
  - [Ports Usage]({{< relref "security/ports-usage.md" >}}) - Network and firewall configuration

### Operations

Day-to-day cluster management:

- **[Administration]({{< relref "admin" >}})**
  - [Dgraph Administration]({{< relref "admin/dgraph-administration.md" >}}) - Common admin tasks
  - [Monitoring]({{< relref "monitoring.md" >}}) - Prometheus and Grafana setup
  - [Troubleshooting]({{< relref "troubleshooting.md" >}}) - Common issues and solutions

### Reference

Detailed technical references:

- **[CLI Reference]({{< relref "cli-reference.md" >}})** - Complete command-line documentation

---

## Quick Start Paths

### I want to...

**Learn Dgraph:**
1. [Install using Docker standalone]({{< relref "getting-started.md#docker-recommended-for-quick-start" >}})
2. Follow the [Query Language guide](/query-language)

**Set up a development environment:**
1. [Understand the architecture]({{< relref "architecture.md" >}})
2. [Deploy a single group basic setup]({{< relref "deployment-patterns#2-single-group---basic-development" >}})
3. [Configure for your needs]({{< relref "configuration.md" >}})

**Deploy to production:**
1. Review the [Production Checklist]({{< relref "production-checklist.md" >}})
2. Choose between [Single Group HA]({{< relref "deployment-patterns#3-single-group---ha-small-production" >}}) or [Multi-Group HA]({{< relref "deployment-patterns#5-multi-group---ha-production-large-scale" >}})
3. [Configure security (TLS, ACL)]({{< relref "security" >}})
4. [Set up monitoring]({{< relref "monitoring.md" >}})

**Troubleshoot an issue:**
1. Check the [Troubleshooting Guide]({{< relref "troubleshooting.md" >}})
2. Review [Dgraph Administration]({{< relref "admin/dgraph-administration.md" >}})
3. Ask on [Dgraph Community Forums](https://discuss.dgraph.io/)

---

## What's a Dgraph Cluster?

A Dgraph cluster consists of:

- **Dgraph Zero nodes** - Manage cluster coordination, metadata, and data distribution
- **Dgraph Alpha nodes** - Store data, process queries, and execute mutations

**Minimum viable cluster:** 1 Zero + 1 Alpha  
**Production cluster:** 3 Zeros + 3+ Alphas (with HA)

See [Architecture]({{< relref "architecture.md" >}}) for detailed explanation.

---

## Deployment Options

### By Environment

| Environment | Recommended Setup | Guide |
|-------------|-------------------|-------|
| **Local Development** | Standalone Docker | [Getting Started]({{< relref "getting-started.md" >}}) |
| **Team Development** | Docker Compose or Single Group Basic | [Deployment Patterns]({{< relref "deployment-patterns#2-single-group---basic-development" >}}) |
| **Staging/QA** | Single Group HA (3+3) | [Single Group HA]({{< relref "deployment-patterns#3-single-group---ha-small-production" >}}) |
| **Small Production** | Single Group HA (3+3) | [Single Group HA]({{< relref "deployment-patterns#3-single-group---ha-small-production" >}}) |
| **Large Production** | Multi-Group HA (3+6 or 3+9) | [Multi-Group HA]({{< relref "deployment-patterns#5-multi-group---ha-production-large-scale" >}}) |

### By Data Size

| Data Size | Recommended Setup |
|-----------|-------------------|
| <100 GB | Single Group HA (3 Alphas) |
| 100 GB - 1 TB | Single Group HA (3-5 Alphas) |
| 1 TB - 10 TB | Multi-Group HA (6-9 Alphas, 2-3 groups) |
| >10 TB | Multi-Group HA (12+ Alphas, 4+ groups) |

---

## Key Concepts

### High Availability (HA)

HA configurations use **Raft consensus** with odd-numbered replicas (3 or 5) per group:

- **3 replicas:** Tolerates 1 node failure
- **5 replicas:** Tolerates 2 node failures

Set with `--replicas=3` flag on Zero nodes.

### Sharding

Dgraph shards data by **predicates** (not by nodes):

- Each predicate is assigned to an Alpha group
- Multiple groups enable horizontal scaling
- Zero automatically rebalances predicates across groups

### Replication

Within each Alpha group, all predicates are replicated to all group members:

- Provides fault tolerance
- Enables load distribution for read queries
- Requires majority (quorum) for writes

---

## Best Practices

### Infrastructure

✅ **Do:**
- Use SSD storage with 3000+ IOPS
- Allocate 8+ CPU cores per Alpha
- Provide 16GB+ RAM per Alpha
- Distribute nodes across availability zones
- Use static IPs or DNS for node discovery

❌ **Don't:**
- Use burstable instances (AWS t2/t3)
- Co-locate multiple replicas on same host
- Use shared storage (NFS, CEPH)
- Run on HDDs

### Security

✅ **Do:**
- Enable TLS for all connections
- Use IP whitelisting for admin endpoints
- Change default passwords immediately
- Store secrets in a secrets manager
- Regularly rotate certificates and keys

❌ **Don't:**
- Expose Zero admin ports publicly
- Use default credentials in production
- Store secrets in configuration files
- Skip certificate validation

### Operations

✅ **Do:**
- Set up monitoring from day one
- Configure automated backups
- Test failover scenarios regularly
- Document your runbooks
- Keep Dgraph updated

❌ **Don't:**
- Run without backups
- Ignore monitoring alerts
- Skip load testing before launch
- Scale to even number of replicas

---

## Common Scenarios

### Scenario: First Production Deployment

**Requirements:** Up to 500 GB data, medium traffic, need HA

**Recommended:**
1. Deploy Single Group HA: 3 Zeros + 3 Alphas
2. Use c5.2xlarge (AWS) or n2-standard-8 (GCP) instances
3. Enable TLS and ACL
4. Set up Prometheus monitoring
5. Configure daily full backups + 4-hour incremental

**See:** [Single Group HA]({{< relref "deployment-patterns#3-single-group---ha-small-production" >}}), [Production Checklist]({{< relref "production-checklist.md" >}})

### Scenario: Scaling Beyond 1TB

**Requirements:** 2TB data, growing rapidly, need to scale horizontally

**Recommended:**
1. Deploy Multi-Group HA: 3 Zeros + 6 Alphas (2 groups × 3 replicas)
2. Can scale to 9 Alphas (3 groups) or 12 Alphas (4 groups) as needed
3. Monitor predicate distribution across groups
4. Plan capacity for 2x growth

**See:** [Multi-Group HA]({{< relref "deployment-patterns#5-multi-group---ha-production-large-scale" >}})

### Scenario: Migration from Single Group to Multi-Group

**Requirements:** Current 3-Alpha cluster hitting storage limits

**Steps:**
1. Take full backup of existing cluster
2. Add 3 more Alpha nodes (Zero creates new group)
3. Zero automatically rebalances predicates
4. Monitor rebalancing progress
5. Verify data distribution

**Note:** This is a zero-downtime operation. Queries continue during rebalancing.

---

## Platform-Specific Guides

### Docker

- **Standalone:** [Getting Started - Docker]({{< relref "getting-started.md#docker-recommended-for-quick-start" >}})
- **Docker Compose:** [Getting Started - Docker Compose]({{< relref "getting-started.md#docker-compose-recommended-for-development" >}})
- **Swarm/Compose for Production:** [Deployment Patterns]({{< relref "deployment-patterns" >}})

### Kubernetes

- **Helm Charts:** Available at https://charts.dgraph.io
- **Operator:** Community-maintained at https://github.com/dgraph-io/dgraph-operator

### Bare Metal / VMs

- **Binary Installation:** [Getting Started - Binary Installation]({{< relref "getting-started.md#binary-installation-linux" >}})
- **Systemd Service:** See [Administration Guide]({{< relref "admin/dgraph-administration.md" >}})

### Cloud Platforms

**AWS:**
- Use c5/m5/r5 instances (not t2/t3)
- Use gp3 EBS volumes or instance storage
- Deploy across 3 availability zones

**GCP:**
- Use n2-standard or n2-highmem instances
- Use SSD persistent disks or local SSD
- Deploy across 3 zones in same region

**Azure:**
- Use D-series or E-series VMs
- Use Premium SSD managed disks
- Deploy across 3 availability zones

---

## Getting Help

### Documentation

- **Main Docs:** https://dgraph.io/docs/
- **GraphQL Docs:** https://dgraph.io/docs/graphql/
- **DQL (Query Language):** https://dgraph.io/docs/query-language/

### Community

- **Forum:** https://discuss.dgraph.io/
- **Discord:** https://dgraph.io/slack (bridged to Slack)
- **GitHub Issues:** https://github.com/dgraph-io/dgraph/issues

### Enterprise Support

- **Contact:** https://dgraph.io/support
- **Features:** SLA guarantees, direct engineering support, advanced features

---

## Next Steps

Choose your path:

- 🚀 **New User:** [Get Started]({{< relref "getting-started.md" >}})
- 🏗️ **Deploying:** [Architecture]({{< relref "architecture.md" >}}) → [Deployment Patterns]({{< relref "deployment-patterns" >}})
- ⚙️ **Configuring:** [Configuration Guide]({{< relref "configuration.md" >}})
- 🔒 **Securing:** [Security Overview]({{< relref "security" >}})
- 📊 **Operating:** [Administration]({{< relref "admin" >}}) → [Monitoring]({{< relref "monitoring.md" >}})
