---
title: Administration
---

Dgraph administration covers the operational tasks needed to manage, monitor, and maintain your Dgraph cluster.

## Core Administration Tasks

**[Admin Tasks](admin-tasks/)** - Administrative operations including data export, cluster shutdown, database deletion, and upgrade procedures. Also covers basic security configuration like IP whitelisting and authentication tokens.


**[Dgraph Zero Endpoints](dgraph-zero)** - Zero node configuration, cluster coordination, and administrative endpoints for managing cluster membership and data distribution.

## Security & Access Control

**[Security Configuration](/admin/security/)** - TLS configuration, port usage, and network security settings.

For enterprise security features including Access Control Lists (ACL), audit logging, and encryption at rest, see [Enterprise Features](/admin/enterprise-features/).

## Monitoring & Observability

**[Observability](/admin/observability/)** - Monitoring with Prometheus/Grafana, metrics collection, distributed tracing, and log format documentation.

**[Troubleshooting](troubleshooting)** - Common issues, OOM handling, file descriptor limits, and cluster setup verification.

## Configuration

**[Data Compression](data-compression)** - Configure disk compression algorithms (Snappy, Zstandard) for Alpha data storage.