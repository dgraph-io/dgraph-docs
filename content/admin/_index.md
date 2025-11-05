+++
title = "Administration"
weight = 7
type = "docs"
aliases = ["/deploy/dgraph-administration"]
[menu.main]
  identifier = "admin"
  parent = ""

+++

Dgraph administration covers the operational tasks needed to manage, monitor, and maintain your Dgraph cluster.

## Core Administration Tasks

**[Dgraph Administration]({{< relref "dgraph-administration.md" >}})** - Main administrative operations including data export, cluster shutdown, database deletion, and upgrade procedures. Also covers basic security configuration like IP whitelisting and authentication tokens.

**[Dgraph Alpha API Reference]({{< relref "dgraph-alpha.md" >}})** - Alpha node HTTP and GraphQL endpoints for health monitoring, cluster management, and basic operations.

**[Dgraph Zero API Reference]({{< relref "dgraph-zero.md" >}})** - Zero node configuration, cluster coordination, and administrative endpoints for managing cluster membership and data distribution.

## Security & Access Control

**[Security Configuration]({{< relref "security" >}})** - TLS configuration, port usage, and network security settings.

For enterprise security features including Access Control Lists (ACL), audit logging, and encryption at rest, see [Enterprise Features]({{< relref "enterprise-features" >}}).

## Monitoring & Observability

**[Observability]({{< relref "observability" >}})** - Monitoring with Prometheus/Grafana, metrics collection, distributed tracing, and log format documentation.

**[Troubleshooting]({{< relref "troubleshooting.md" >}})** - Common issues, OOM handling, file descriptor limits, and cluster setup verification.

## Configuration

**[Data Compression]({{< relref "data-compression.md" >}})** - Configure disk compression algorithms (Snappy, Zstandard) for Alpha data storage.