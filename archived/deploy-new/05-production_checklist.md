+++
title = "Production Checklist"
weight = 5
type = "docs"
[menu.main]
  identifier = "production-checklist"
  parent = "deploy"
+++

This checklist helps ensure your Dgraph deployment is production-ready with high availability, security, and reliability.

---

## Infrastructure Requirements

### ✓ Hardware Specifications

**Minimum per Alpha Node:**
- [ ] **CPU:** 8 cores @ 3.4GHz+
- [ ] **RAM:** 16GB (32GB recommended)
- [ ] **Disk:** 250GB SSD with 3000+ IOPS
- [ ] **Network:** 1Gbps+, <5ms latency between nodes

**Minimum per Zero Node:**
- [ ] **CPU:** 2-4 cores
- [ ] **RAM:** 4GB
- [ ] **Disk:** 200GB SSD with 1000+ IOPS

**Disk Types:**
- [ ] Using SSDs (not HDDs)
- [ ] AWS: gp3, io1, or c5d/i3 instance storage
- [ ] GCP: SSD persistent disks or local SSD
- [ ] Azure: Premium SSD or local SSD

**Filesystem:**
- [ ] Using ext4 filesystem
- [ ] Avoiding shared storage (NFS, CEPH, CIFS)

### ✓ Host Configuration

- [ ] **Not using burstable instances** (no AWS t2/t3)
- [ ] **Dedicated physical hosts** or VMs with guaranteed resources
- [ ] **No CPU throttling** or resource oversubscription
- [ ] **File descriptor limit** set to 1,048,576 (`ulimit -n`)
- [ ] **Operating system:** Linux (Debian, Ubuntu, RHEL, CentOS)

---

## Cluster Topology

### ✓ High Availability Setup

**Zero Cluster:**
- [ ] **3 or 5 Zero nodes** (odd number for consensus)
- [ ] `--replicas=3` flag set on all Zeros
- [ ] Each Zero on a **different physical host**
- [ ] Zeros distributed across **3 availability zones** (if possible)

**Alpha Cluster:**
- [ ] **3 or 5 Alphas per group** (minimum)
- [ ] Total Alphas = `num_groups × replicas`
  - Example: 6 Alphas = 2 groups × 3 replicas
- [ ] Each Alpha on a **different physical host**
- [ ] Alphas distributed across **3 availability zones** (if possible)

**Node Placement:**
- [ ] **Maximum 1 Zero + 1 Alpha per host** (if co-locating)
- [ ] **No more than 1 node per group on same host**
- [ ] Cluster can survive **1 AZ failure** without data loss

### ✓ Network Requirements

- [ ] All nodes can reach each other on internal ports
- [ ] Firewall rules configured per [Ports Usage]({{< relref "security/ports-usage.md" >}})
- [ ] Load balancer (if used) configured for Alpha :9080 (gRPC) and :8080 (HTTP)
- [ ] DNS or static IPs configured for all nodes
- [ ] Network latency <5ms between nodes

---

## Security Configuration

### ✓ TLS Encryption

- [ ] **TLS enabled** for client connections (`--tls` configured)
- [ ] **mTLS enabled** for inter-node communication (`internal-port=true`)
- [ ] CA certificate, node certificates, and keys generated
- [ ] Certificates include all hostnames/IPs in SANs
- [ ] Private keys have proper permissions (chmod 600)
- [ ] Certificate expiration monitoring in place

**Verify with:**
```sh
dgraph cert ls
```

### ✓ Access Control

**IP Whitelisting:**
- [ ] Admin endpoints restricted to trusted IPs
- [ ] `--security whitelist=<trusted-ips>` configured on Alphas
- [ ] Zero admin port (6080) accessible only to ops team

**Admin Token:**
- [ ] `--security token=<secret>` set on Alphas
- [ ] Token stored securely (secrets manager, not in code)

**ACL (Enterprise):**
- [ ] ACL enabled with `--acl` superflag
- [ ] HMAC secret file created with 32+ character secret
- [ ] Default admin (groot) password changed
- [ ] User accounts created with least-privilege access
- [ ] Groups configured for different access levels

### ✓ Data Encryption

**At Rest (Enterprise):**
- [ ] `--encryption key-file=<path>` configured
- [ ] Encryption key is 16, 24, or 32 bytes (AES-128/192/256)
- [ ] Keys stored in secure key management system (Vault, KMS)
- [ ] Key rotation policy documented

**In Transit:**
- [ ] TLS 1.2+ enforced
- [ ] Only strong cipher suites enabled

---

## Data Management

### ✓ Backup Strategy

**Binary Backups (Enterprise):**
- [ ] Automated backup schedule configured
- [ ] **Full backups:** Daily
- [ ] **Incremental backups:** Every 2-4 hours
- [ ] Backups stored in **separate geographic location**
- [ ] Backup retention policy: 30 days minimum
- [ ] Restore procedure tested and documented
- [ ] Backup monitoring/alerting configured

**Export Backups (Open Source):**
- [ ] Regular exports scheduled (if not using Enterprise backups)
- [ ] Exports stored off-cluster
- [ ] Export/import procedure tested

### ✓ Data Durability

- [ ] Persistent volumes configured (not ephemeral)
- [ ] Volumes survive node/container restarts
- [ ] Volume backups enabled at infrastructure level
- [ ] Data directories monitored for disk space

---

## Monitoring and Observability

### ✓ Metrics Collection

- [ ] **Prometheus** scraping `/debug/prometheus_metrics`
- [ ] Scrape interval: 15-30 seconds
- [ ] **Grafana** dashboards imported
- [ ] Metrics retention: 30+ days

**Key Metrics Monitored:**
- [ ] Query latency (p50, p95, p99)
- [ ] Mutation throughput
- [ ] Raft proposal queue size
- [ ] Disk usage per node
- [ ] Memory usage per node
- [ ] Network I/O
- [ ] Cache hit ratio

### ✓ Logging

- [ ] Logs centralized (ELK, Splunk, CloudWatch, etc.)
- [ ] Log retention: 30+ days
- [ ] Log levels appropriate (info in prod)
- [ ] Structured logging enabled

### ✓ Alerting

**Critical Alerts:**
- [ ] Node down (Alpha or Zero)
- [ ] Raft leader election
- [ ] Disk space >80% full
- [ ] Query latency >threshold
- [ ] High error rate (5xx)
- [ ] Certificate expiration (30 days)

**Warning Alerts:**
- [ ] Memory usage >80%
- [ ] CPU usage >80% for >5 mins
- [ ] Backup failures
- [ ] Replication lag

### ✓ Health Checks

- [ ] Load balancer health checks on `/health`
- [ ] `/health?all` checked periodically for cluster status
- [ ] GraphQL health query:
  ```graphql
  query { health { instance status address } }
  ```

### ✓ Distributed Tracing (Optional)

- [ ] Jaeger or Datadog configured
- [ ] Trace sampling configured (`--trace ratio=0.01`)
- [ ] Traces integrated with logs

---

## Performance Tuning

### ✓ Cache Configuration

- [ ] `--cache size-mb` set to 40-50% of node RAM
- [ ] Cache percentages tuned for workload
- [ ] Read-heavy: increase block cache (70%)
- [ ] Filter-heavy: increase index cache (40%)

### ✓ Query Limits

- [ ] `--limit` flags configured appropriately:
  - [ ] `query-edge` limit set
  - [ ] `mutations-nquad` limit set
  - [ ] `query-timeout` set for long-running queries
  - [ ] `max-pending-queries` set to prevent overload

### ✓ Storage Optimization

- [ ] Badger compression enabled (`zstd:1` or higher)
- [ ] Raft snapshot frequency tuned
- [ ] Old Raft logs cleaned up automatically

---

## Operational Readiness

### ✓ Documentation

- [ ] **Runbook** created with common procedures:
  - [ ] Node restart procedure
  - [ ] Failover procedure
  - [ ] Backup/restore procedure
  - [ ] Schema migration procedure
  - [ ] Scaling procedure (add nodes)
  - [ ] Rolling upgrade procedure
- [ ] **Network diagram** with node IPs/ports
- [ ] **Contact list** for on-call team
- [ ] **Escalation policy** documented

### ✓ Automation

- [ ] Infrastructure-as-code (Terraform, CloudFormation, etc.)
- [ ] Config management (Ansible, Chef, Puppet, etc.)
- [ ] Automated deployments (CI/CD pipeline)
- [ ] Automated backups
- [ ] Automated monitoring setup

### ✓ Disaster Recovery

- [ ] **RTO (Recovery Time Objective)** defined
- [ ] **RPO (Recovery Point Objective)** defined
- [ ] DR procedure documented and tested
- [ ] Multi-region failover plan (if applicable)
- [ ] Backup restoration tested quarterly

### ✓ Capacity Planning

- [ ] Current resource utilization monitored
- [ ] Growth projections calculated
- [ ] **Scaling thresholds** defined:
  - [ ] CPU >70%: plan to scale
  - [ ] Memory >70%: plan to scale
  - [ ] Disk >70%: add storage or shard
- [ ] Quarterly capacity reviews scheduled

---

## Pre-Launch Validation

### ✓ Load Testing

- [ ] Load tests performed at expected peak traffic
- [ ] Load tests at 2x expected traffic
- [ ] Query latency <100ms at p95 (or meets SLO)
- [ ] Sustained load test (24 hours) successful
- [ ] No memory leaks observed
- [ ] No disk space growth anomalies

### ✓ Failover Testing

- [ ] Single Alpha failure: cluster stays available
- [ ] Single Zero failure: cluster stays available
- [ ] Network partition: cluster recovers
- [ ] Full AZ failure: cluster survives (if multi-AZ)
- [ ] Leader election works correctly
- [ ] Data consistency verified after failover

### ✓ Backup/Restore Testing

- [ ] Full restore tested from backup
- [ ] Point-in-time recovery tested
- [ ] Restore time documented (meets RTO)
- [ ] Data integrity verified post-restore

### ✓ Security Testing

- [ ] Penetration testing completed
- [ ] TLS configuration verified
- [ ] ACL rules tested
- [ ] Admin endpoints not publicly accessible
- [ ] No secrets in code/config files

---

## Launch Day Checklist

### ✓ Final Verification

- [ ] All monitoring dashboards operational
- [ ] All alerts configured and tested
- [ ] On-call rotation scheduled
- [ ] Runbooks accessible to team
- [ ] Communication plan ready (status page, Slack, etc.)

### ✓ Go/No-Go Criteria

- [ ] All critical alerts green
- [ ] All nodes healthy (`/health?all`)
- [ ] Backup jobs successful in last 24 hours
- [ ] Load tests passed
- [ ] Security audit passed
- [ ] Team trained on operations
- [ ] Rollback plan prepared

---

## Post-Launch

### ✓ First 24 Hours

- [ ] Monitor dashboards continuously
- [ ] Check for unexpected alerts
- [ ] Verify backup jobs run successfully
- [ ] Review application logs for errors
- [ ] Confirm query latency within SLOs

### ✓ First Week

- [ ] Review all monitoring data
- [ ] Tune configuration if needed
- [ ] Document any issues encountered
- [ ] Team retrospective meeting
- [ ] Update runbooks with learnings

### ✓ Ongoing

- [ ] Weekly capacity review
- [ ] Monthly DR drill
- [ ] Quarterly load testing
- [ ] Quarterly certificate renewal check
- [ ] Regular Dgraph version upgrades

---

## Common Pitfalls to Avoid

❌ **Don't:**
- Run without HA (single node in prod)
- Use t2/t3 burstable instances
- Co-locate multiple replicas on same host
- Forget to set file descriptor limits
- Use HDDs instead of SSDs
- Skip TLS configuration
- Forget to change default groot password
- Run without backups
- Ignore monitoring until there's an issue
- Scale to even number of nodes (breaks consensus)

✅ **Do:**
- Plan for failure (expect nodes to go down)
- Test failover scenarios regularly
- Monitor proactively, not reactively
- Document everything
- Automate everything
- Review logs and metrics regularly
- Keep Dgraph updated
- Have a rollback plan

---

## Resources

- [Architecture Overview]({{< relref "architecture.md" >}})
- [Deployment Patterns]({{< relref "deployment-patterns.md" >}})
- [Security Configuration]({{< relref "security" >}})
- [Monitoring Guide]({{< relref "monitoring.md" >}})
- [Administration Guide]({{< relref "admin" >}})

---

**Need Help?**
- [Dgraph Community](https://discuss.dgraph.io/)
- [Enterprise Support](https://dgraph.io/support)
- [Documentation](https://dgraph.io/docs/)
