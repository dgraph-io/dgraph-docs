---
title: dgraph zero
---

The `dgraph zero` command runs Dgraph Zero management nodes, which control the cluster and coordinate data distribution.

## Overview

A Dgraph Zero instance manages the Dgraph cluster. Typically, a single Zero instance is sufficient for the cluster; however, one can run multiple Zero instances to achieve high-availability.

## Usage

```bash
dgraph zero [flags]
```

## Key Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--my` | Address:port of this server for cluster communication | |
| `--peer` | Address of another dgraphzero server | |
| `-o, --port_offset` | Value added to all listening port numbers [Grpc=5080, HTTP=6080] | `0` |
| `-w, --wal` | Directory storing WAL | `"zw"` |
| `--replicas` | How many Dgraph Alpha replicas to run per data shard group | `1` |
| `--rebalance_interval` | Interval for trying a predicate move | `8m0s` |
| `--enterprise_license` | Path to the enterprise license file | |

## Superflags

Zero uses several [superflags](superflags) for advanced configuration:

- `--audit` - Audit logging configuration
- `--limit` - UID lease and admin endpoint settings
- `--raft` - Raft consensus options
- `--telemetry` - Telemetry and crash reporting
- `--tls` - TLS configuration
- `--trace` - Distributed tracing

## Full Reference

```shell
A Dgraph Zero instance manages the Dgraph cluster.  Typically, a single Zero
instance is sufficient for the cluster; however, one can run multiple Zero
instances to achieve high-availability.

Usage:
  dgraph zero [flags]

Flags:
      --audit string                  Audit options
                                          compress=false; Enables the compression of old audit logs.
                                          days=10; The number of days audit logs will be preserved.
                                          encrypt-file=; The path to the key file to be used for audit log encryption.
                                          output=; [stdout, /path/to/dir] This specifies where audit logs should be output to.
                                      			"stdout" is for standard output. You can also specify the directory where audit logs
                                      			will be saved. When stdout is specified as output other fields will be ignored.
                                          size=100; The audit log max size in MB after which it will be rolled over.
                                       (default "compress=false; days=10; size=100; dir=; output=; encrypt-file=;")
      --enterprise_license string     Path to the enterprise license file.
  -h, --help                          help for zero
      --limit string                  Limit options
                                          disable-admin-http=false; Turn on/off the administrative endpoints exposed over Zero's HTTP port.
                                          refill-interval=30s; The interval after which the tokens for UID lease are replenished.
                                          uid-lease=0; The maximum number of UIDs that can be leased by namespace (except default namespace)
                                      			in an interval specified by refill-interval. Set it to 0 to remove limiting.
                                       (default "uid-lease=0; refill-interval=30s; disable-admin-http=false;")
      --my string                     addr:port of this server, so other Dgraph servers can talk to this.
      --peer string                   Address of another dgraphzero server.
  -o, --port_offset int               Value added to all listening port numbers. [Grpc=5080, HTTP=6080]
      --raft string                   Raft options
                                          idx=1; Provides an optional Raft ID that this Alpha would use to join Raft groups.
                                          learner=false; Make this Zero a "learner" node. In learner mode, this Zero will not participate in Raft elections. This can be used to achieve a read-only replica.
                                       (default "idx=1; learner=false;")
      --rebalance_interval duration   Interval for trying a predicate move. (default 8m0s)
      --replicas int                  How many Dgraph Alpha replicas to run per data shard group. The count includes the original shard. (default 1)
      --survive string                Choose between "process" or "filesystem".
                                          If set to "process", there would be no data loss in case of process crash, but the behavior would be nondeterministic in case of filesystem crash.
                                          If set to "filesystem", blocking sync would be called after every write, hence guaranteeing no data loss in case of hard reboot.
                                          Most users should be OK with choosing "process". (default "process")
      --telemetry string              Telemetry (diagnostic) options
                                          reports=true; Send anonymous telemetry data to Dgraph devs.
                                          sentry=true; Send crash events to Sentry.
                                       (default "reports=true; sentry=true;")
      --tls string                    TLS Server options
                                          ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                          client-auth-type=VERIFYIFGIVEN; The TLS client authentication method.
                                          client-cert=; (Optional) The client Cert file which is needed to connect as a client with the other nodes in the cluster.
                                          client-key=; (Optional) The private client Key file which is needed to connect as a client with the other nodes in the cluster.
                                          internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                          server-cert=; The server Cert file which is needed to initiate the server in the cluster.
                                          server-key=; The server Key file which is needed to initiate the server in the cluster.
                                          use-system-ca=true; Includes System CA into CA Certs.
                                       (default "use-system-ca=true; client-auth-type=VERIFYIFGIVEN; internal-port=false;")
      --trace string                  Trace options
                                          datadog=; URL of Datadog to send OpenCensus traces. As of now, the trace exporter does not support annotation logs and discards them.
                                          jaeger=; URL of Jaeger to send OpenCensus traces.
                                          ratio=0.01; The ratio of queries to trace.
                                       (default "ratio=0.01; jaeger=; datadog=;")
  -w, --wal string                    Directory storing WAL. (default "zw")

Use "dgraph zero [command] --help" for more information about a command.
```


