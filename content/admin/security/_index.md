+++
title = "Security"
weight = 4
type = "docs"
[menu.main]
  identifier = "security"
  parent = "admin"
+++

Dgraph security configuration covers authentication, network security, and access control for your cluster.

## Security Configuration

**[Admin Endpoint Security]({{< relref "admin-endpoint-security.md" >}})** - Authentication layers for admin endpoints, IP whitelisting, and token-based authentication.

**[Ports Usage]({{< relref "ports-usage.md" >}})** - Understanding Dgraph's port configuration and network security requirements.

**[TLS Configuration]({{< relref "tls-configuration.md" >}})** - Encrypting communications between Dgraph nodes and clients using TLS/mTLS.

## Enterprise Security Features

For advanced security features, see [Enterprise Features]({{< relref "../../enterprise-features" >}}):

- [Access Control Lists (ACL)]({{< relref "../../enterprise-features/access-control-lists.md" >}}) - Fine-grained access control
- [Audit Logging]({{< relref "../../enterprise-features/audit-logs.md" >}}) - Track and audit all requests
- [Encryption at Rest]({{< relref "../../enterprise-features/encryption-at-rest.md" >}}) - Encrypt data on disk