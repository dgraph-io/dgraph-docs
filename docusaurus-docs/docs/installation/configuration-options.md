---
title: Installation Configuration Options
description: Key configuration options to consider when installing Dgraph
---

This guide lists important configuration options you should consider when installing Dgraph. Each option links to detailed documentation in the Administration section.

:::tip
For a comprehensive production setup checklist, see the [Production Checklist](production-checklist).
:::

## Security Configuration

### TLS/SSL Encryption

Enable TLS to secure communications between Dgraph nodes and clients over HTTP and gRPC ports.

**Consider enabling TLS if:**
- Your cluster handles sensitive data
- Dgraph nodes communicate over untrusted networks
- You need to meet compliance requirements
- You're deploying in a production environment

**Configuration:**
- Generate certificates using `dgraph cert`
- Configure TLS using the `--tls` superflag on Alpha and Zero nodes
- Supports encryption for external ports (client connections) and internal ports (inter-node communication)
- Supports mutual TLS (mTLS) for client authentication

**Learn more:** [TLS Configuration](/admin/security/tls-configuration)

### Access Control Lists (ACL)

Enable ACL to control access to your data with user authentication and authorization.

**Consider enabling ACL if:**
- Multiple users or applications access your database
- You need fine-grained access control to predicates
- You're using multi-tenancy features
- You need to audit who accessed what data

**Configuration:**
- Generate an HMAC secret file (32 bytes)
- Configure ACL using the `--acl` superflag on Alpha nodes
- Set up users and permissions after enabling ACL

**Learn more:** [Access Control Lists](/admin/enterprise-features/access-control-lists)

### Encryption at Rest

Encrypt data stored on disk to protect sensitive information.

**Consider enabling encryption at rest if:**
- You store sensitive or regulated data (PII, financial data, etc.)
- You need to meet compliance requirements (GDPR, HIPAA, etc.)
- Your storage may be accessed by unauthorized parties

**Configuration:**
- Generate an encryption key file (16, 24, or 32 bytes)
- Configure using the `--encryption` superflag on Alpha nodes
- Can use local file or Hashicorp Vault for key storage

**Learn more:** [Encryption at Rest](/admin/enterprise-features/encryption-at-rest)

### Network Security

Configure firewall rules and network access controls.

**Configuration:**
- Review required ports in [Ports Usage](/admin/security/ports-usage)
- Configure firewall rules to restrict access
- Use IP whitelisting with the `--security` superflag
- Consider placing Zero nodes in private networks

**Learn more:** [Ports Usage](/admin/security/ports-usage), [Admin Endpoint Security](/admin/security/admin-endpoint-security)

## Enterprise Features

### Change Data Capture (CDC)

Enable CDC to track and stream data changes to external systems like Kafka.

**Consider enabling CDC if:**
- You need to replicate data to other systems
- You're building event-driven architectures
- You need to track all data changes for compliance
- You're integrating with data pipelines

**Configuration:**
- Configure using the `--cdc` superflag on Alpha nodes
- Choose between Kafka sink or local file sink
- Configure TLS and authentication for Kafka connections

**Learn more:** [Change Data Capture](/admin/enterprise-features/change-data-capture)

### Binary Backups

Set up automated backup policies for disaster recovery.

**Consider configuring backups if:**
- You're running in production
- You need point-in-time recovery
- You have compliance requirements for data retention
- You want to enable incremental backups

**Configuration:**
- Configure backup schedules using the backup API
- Enable encrypted backups if using encryption at rest
- Set up backup storage (local, S3, GCS, Azure Blob, MinIO)
- Configure full and incremental backup policies

**Learn more:** [Binary Backups](/admin/enterprise-features/binary-backups)

### Multi-Tenancy

Enable multi-tenancy to isolate data by namespace for multiple tenants.

**Consider enabling multi-tenancy if:**
- You're building a SaaS application
- You need to isolate data for different customers
- You want to share infrastructure across multiple tenants
- You need namespace-level access control

**Configuration:**
- Multi-tenancy works with ACL enabled
- Create namespaces and assign users to namespaces
- Configure namespace-specific permissions

**Learn more:** [Multi-Tenancy](/admin/enterprise-features/multitenancy)

### Learner Nodes

Configure learner nodes for read scaling without affecting cluster consensus.

**Consider using learner nodes if:**
- You need additional read capacity
- You want to scale reads without increasing write quorum requirements
- You're running analytics workloads that don't need real-time consistency

**Learn more:** [Learner Nodes](/admin/enterprise-features/learner-nodes)

## Observability Configuration

### Metrics and Monitoring

Configure metrics collection and monitoring for your cluster.

**Consider setting up monitoring if:**
- You're running in production
- You need to track performance and health
- You want to set up alerts for issues
- You need capacity planning data

**Configuration:**
- Dgraph exposes metrics on `/debug/prometheus_metrics`
- Set up Prometheus to scrape metrics
- Configure Grafana dashboards for visualization
- Set up alerting rules

**Learn more:** [Metrics](/admin/observability/metrics), [Monitoring](/admin/observability/monitoring)

### Distributed Tracing

Enable distributed tracing to debug performance issues and understand request flows.

**Consider enabling tracing if:**
- You're debugging performance issues
- You need to understand query execution paths
- You want to identify bottlenecks in your cluster
- You're running complex multi-node queries

**Configuration:**
- Configure using the `--trace` superflag
- Set trace sampling ratio (default: 1%)
- Send traces to Jaeger or use built-in zPages
- Configure Jaeger collector endpoint

**Learn more:** [Tracing](/admin/observability/tracing)

### Audit Logging

Enable audit logging to track all requests for compliance and security.

**Consider enabling audit logging if:**
- You need to meet compliance requirements
- You want to track all database access
- You need to investigate security incidents
- You're required to maintain audit trails

**Configuration:**
- Configure audit log file location and size
- Set retention policies
- Review audit log format and content

**Learn more:** [Audit Logging](/admin/observability/audit-logs)

### Log Configuration

Configure logging levels and formats for better debugging.

**Configuration:**
- Adjust log verbosity levels
- Configure log output format
- Set up log rotation policies

**Learn more:** [Log Format](/admin/observability/log-format)

## Performance and Storage

### Data Compression

Enable compression to reduce storage requirements.

**Consider enabling compression if:**
- You have large datasets
- Storage costs are a concern
- You want to improve I/O performance
- Network bandwidth is limited

**Configuration:**
- Configure compression using Badger options
- Choose compression algorithm (zstd, snappy)
- Balance between compression ratio and CPU usage

**Learn more:** [Data Compression](/admin/data-compression)

### Storage Configuration

Configure storage settings for optimal performance.

**Configuration:**
- Use SSDs (not HDDs) for production
- Ensure sufficient IOPS (1000+ minimum, 3000+ recommended)
- Configure appropriate disk sizes (250GB-750GB for Alpha)
- Use ext4 filesystem on Linux
- Avoid shared storage (NFS, CIFS, CEPH)

**Learn more:** [Production Checklist](production-checklist#disk)

## Network Configuration

### Port Configuration

Understand and configure Dgraph ports for your network setup.

**Key ports:**
- **8080**: HTTP endpoint for Alpha (queries, mutations)
- **9080**: gRPC endpoint for Alpha (client connections)
- **6080**: HTTP endpoint for Zero (admin operations)
- **5080**: gRPC endpoint for Zero (internal cluster communication)
- **7080**: Internal gRPC for Alpha (Raft consensus)

**Configuration:**
- Configure firewall rules for required ports
- Use load balancers for client connections
- Restrict admin ports (6080) to internal networks
- Consider custom ports if defaults conflict

**Learn more:** [Ports Usage](/admin/security/ports-usage)

## High Availability Configuration

### Cluster Setup

Configure your cluster for high availability and fault tolerance.

**Configuration:**
- Run at least 3 Zero nodes for HA
- Run at least 3 Alpha nodes per group for HA
- Distribute nodes across availability zones
- Configure proper Raft replication settings

**Learn more:** [High Availability Cluster Setup](ha-cluster), [Deployment Patterns](deployment-patterns)

## Additional Considerations

### Lambda Server

Configure Lambda server for custom business logic.

**Consider using Lambda if:**
- You need custom query logic
- You want to integrate with external services
- You need server-side data transformations

**Learn more:** [Lambda Server](lambda-server)

### Configuration Methods

Dgraph supports multiple configuration methods:

- **Command-line flags**: Direct flags when starting nodes
- **Configuration files**: YAML or JSON config files
- **Environment variables**: Set via `DGRAPH_ALPHA_*` or `DGRAPH_ZERO_*` prefixes
- **Superflags**: Compound flags for complex configurations

**Learn more:** [Configuration Options](/cli/config), [Superflags](/cli/superflags)

## Next Steps

After configuring your installation:

1. Review the [Production Checklist](production-checklist) for additional requirements
2. Set up [monitoring and observability](/admin/observability)
3. Configure [backup policies](/admin/enterprise-features/binary-backups)
4. Test your configuration in a staging environment
5. Review [troubleshooting guide](/admin/troubleshooting) for common issues

