---
title: Administration
---

Dgraph administration covers the operational tasks needed to manage, monitor, and maintain your Dgraph cluster.

## Core Administration Tasks

**[Dgraph Administration](/dgraph-overview/admin/dgraph-administration)** - Main administrative operations including data export, cluster shutdown, database deletion, and upgrade procedures. Also covers basic security configuration like IP whitelisting and authentication tokens.

**[Dgraph Alpha API Reference](/dgraph-overview/admin/dgraph-alpha)** - Alpha node HTTP and GraphQL endpoints for health monitoring, cluster management, and basic operations.

**[Dgraph Zero API Reference](/dgraph-overview/admin/dgraph-zero)** - Zero node configuration, cluster coordination, and administrative endpoints for managing cluster membership and data distribution.

## Security & Access Control

**[Security Configuration](/dgraph-overview/admin/security)** - TLS configuration, port usage, and network security settings.

For enterprise security features including Access Control Lists (ACL), audit logging, and encryption at rest, see [Enterprise Features](/dgraph-overview/admin/enterprise-features).

## Monitoring & Observability

**[Observability](/dgraph-overview/admin/observability)** - Monitoring with Prometheus/Grafana, metrics collection, distributed tracing, and log format documentation.

**[Troubleshooting](/dgraph-overview/admin/troubleshooting)** - Common issues, OOM handling, file descriptor limits, and cluster setup verification.

## Configuration

**[Data Compression](/dgraph-overview/admin/data-compression)** - Configure disk compression algorithms (Snappy, Zstandard) for Alpha data storage.