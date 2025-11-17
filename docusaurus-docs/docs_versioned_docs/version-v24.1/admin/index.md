---
title: Administration
---

Dgraph administration covers the operational tasks needed to manage, monitor, and maintain your Dgraph cluster.

## Core Administration Tasks

**[Admin Tasks](admin-tasks/)** - Administrative operations including data export, cluster shutdown, database deletion, and upgrade procedures. Also covers basic security configuration like IP whitelisting and authentication tokens.


**[View Cluster State](admin-tasks/view-cluster-state)** - View cluster state, group membership, and predicate distribution (sharding) information.

## Security & Access Control

**[Security Configuration](/admin/security/)** - TLS configuration, port usage, and network security settings.

**[User Management and Access Control](/admin/admin-tasks/user-management-access-control.md)** - manage users, groups, and configure access control rules to protect your data.

## Monitoring & Observability

**[Observability](/admin/observability/)** - Monitoring with Prometheus/Grafana, metrics collection, distributed tracing, and log format documentation.

**[Troubleshooting](troubleshooting)** - Common issues, OOM handling, file descriptor limits, and cluster setup verification.

## Configuration

**[Data Compression](data-compression)** - Configure disk compression algorithms (Snappy, Zstandard) for Alpha data storage.