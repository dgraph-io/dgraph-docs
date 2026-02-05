---
title: dgraph alpha
---

The `dgraph alpha` command runs Dgraph Alpha database nodes, which store data and serve queries in your deployment.

## Overview

A Dgraph Alpha instance stores the data. Each Dgraph Alpha is responsible for storing and serving one data group. If multiple Alphas serve the same group, they form a Raft group and provide synchronous replication.

## Usage

```bash
dgraph alpha [flags]
```

## Key Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-p, --postings` | Directory to store posting lists | `"p"` |
| `-w, --wal` | Directory to store raft write-ahead logs | `"w"` |
| `--tmp` | Directory to store temporary buffers | `"t"` |
| `-z, --zero` | Comma separated list of Dgraph Zero addresses | `"localhost:5080"` |
| `--my` | Address:port of this server for cluster communication | |
| `-o, --port_offset` | Value added to all listening port numbers [Internal=7080, HTTP=8080, Grpc=9080] | `0` |
| `--export` | Folder in which to store exports | `"export"` |
| `--custom_tokenizers` | Comma separated list of tokenizer plugins for custom indices | |

## Superflags

Alpha uses several [superflags](superflags) for advanced configuration:

- `--acl` - Access Control List settings (Enterprise)
- `--audit` - Audit logging configuration
- `--badger` - Badger database options
- `--cache` - Cache configuration
- `--cdc` - Change Data Capture options
- `--encryption` - Encryption at rest (Enterprise)
- `--graphql` - GraphQL settings
- `--limit` - Query and mutation limits
- `--raft` - Raft consensus options
- `--security` - Security settings (token, whitelist)
- `--telemetry` - Telemetry and crash reporting
- `--tls` - TLS configuration
- `--trace` - Distributed tracing
- `--vault` - HashiCorp Vault integration

## Full Reference

```shell
A Dgraph Alpha instance stores the data. Each Dgraph Alpha is responsible for
storing and serving one data group. If multiple Alphas serve the same group,
they form a Raft group and provide synchronous replication.

Usage:
  dgraph alpha [flags]

Flags:
      --acl string                 [Enterprise Feature] ACL options
                                       access-ttl=6h; The TTL for the access JWT.
                                       refresh-ttl=30d; The TTL for the refresh JWT.
                                       secret-file=; The file that stores the HMAC secret, which is used for signing the JWT and should have at least 32 ASCII characters. Required to enable ACLs.
                                    (default "access-ttl=6h; refresh-ttl=30d; secret-file=;")
      --audit string               Audit options
                                       compress=false; Enables the compression of old audit logs.
                                       days=10; The number of days audit logs will be preserved.
                                       encrypt-file=; The path to the key file to be used for audit log encryption.
                                       output=; [stdout, /path/to/dir] This specifies where audit logs should be output to.
                                   			"stdout" is for standard output. You can also specify the directory where audit logs
                                   			will be saved. When stdout is specified as output other fields will be ignored.
                                       size=100; The audit log max size in MB after which it will be rolled over.
                                    (default "compress=false; days=10; size=100; dir=; output=; encrypt-file=;")
      --badger string              Badger options
                                       compression=snappy; [none, zstd:level, snappy] Specifies the compression algorithm and
                                   			compression level (if applicable) for the postings directory."none" would disable
                                   			compression, while "zstd:1" would set zstd compression at level 1.
                                       numgoroutines=8; The number of goroutines to use in badger.Stream.
                                       max-retries=-1; Commits to disk will give up after these number of retries to prevent locking the worker in a failed state. Use -1 to retry infinitely.
                                    (default "compression=snappy; numgoroutines=8; max-retries=-1;")
      --cache string               Cache options
                                       percentage=0,65,35; Cache percentages summing up to 100 for various caches (FORMAT: PostingListCache,PstoreBlockCache,PstoreIndexCache)
                                       size-mb=1024; Total size of cache (in MB) to be used in Dgraph.
                                    (default "size-mb=1024; percentage=0,65,35;")
      --cdc string                 Change Data Capture options
                                       ca-cert=; The path to CA cert file for TLS encryption.
                                       client-cert=; The path to client cert file for TLS encryption.
                                       client-key=; The path to client key file for TLS encryption.
                                       file=; The path where audit logs will be stored.
                                       kafka=; A comma separated list of Kafka hosts.
                                       sasl-password=; The SASL password for Kafka.
                                       sasl-user=; The SASL username for Kafka.
                                    (default "file=; kafka=; sasl_user=; sasl_password=; ca_cert=; client_cert=; client_key=;")
      --custom_tokenizers string   Comma separated list of tokenizer plugins for custom indices.
      --encryption string          [Enterprise Feature] Encryption At Rest options
                                       key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                                    (default "key-file=;")
      --export string              Folder in which to store exports. (default "export")
      --graphql string             GraphQL options
                                       debug=false; Enables debug mode in GraphQL. This returns auth errors to clients, and we do not recommend turning it on for production.
                                       extensions=true; Enables extensions in GraphQL response body.
                                       introspection=true; Enables GraphQL schema introspection.
                                       lambda-url=; The URL of a lambda server that implements custom GraphQL Javascript resolvers.
                                       poll-interval=1s; The polling interval for GraphQL subscription.
                                    (default "introspection=true; debug=false; extensions=true; poll-interval=1s; lambda-url=;")
  -h, --help                       help for alpha
      --limit string               Limit options
                                       disallow-drop=false; Set disallow-drop to true to block drop-all and drop-data operation. It still allows dropping attributes and types.
                                       mutations-nquad=1000000; The maximum number of nquads that can be inserted in a mutation request.
                                       mutations=allow; [allow, disallow, strict] The mutations mode to use.
                                       normalize-node=10000; The maximum number of nodes that can be returned in a query that uses the normalize directive.
                                       query-edge=1000000; The maximum number of edges that can be returned in a query. This applies to shortest path and recursive queries.
                                       query-timeout=0ms; Maximum time after which a query execution will fail. If set to 0, the timeout is infinite.
                                       txn-abort-after=5m; Abort any pending transactions older than this duration. The liveness of a transaction is determined by its last mutation.
                                       max-pending-queries=10000; Number of maximum pending queries before we reject them as too many requests.
                                    (default "mutations=allow; query-edge=1000000; normalize-node=10000; mutations-nquad=1000000; disallow-drop=false; query-timeout=0ms; txn-abort-after=5m; max-pending-queries=10000")
      --my string                  addr:port of this server, so other Dgraph servers can talk to this.
  -o, --port_offset int            Value added to all listening port numbers. [Internal=7080, HTTP=8080, Grpc=9080]
  -p, --postings string            Directory to store posting lists. (default "p")
      --raft string                Raft options
                                       group=; Provides an optional Raft Group ID that this Alpha would indicate to Zero to join.
                                       idx=; Provides an optional Raft ID that this Alpha would use to join Raft groups.
                                       learner=false; Make this Alpha a "learner" node. In learner mode, this Alpha will not participate in Raft elections. This can be used to achieve a read-only replica.
                                       pending-proposals=256; Number of pending mutation proposals. Useful for rate limiting.
                                       snapshot-after-duration=30m; Frequency at which we should create a new raft snapshots. Set to 0 to disable duration based snapshot.
                                       snapshot-after-entries=10000; Create a new Raft snapshot after N number of Raft entries. The lower this number, the more frequent snapshot creation will be. Snapshots are created only if both snapshot-after-duration and snapshot-after-entries threshold are crossed.
                                    (default "learner=false; snapshot-after-entries=10000; snapshot-after-duration=30m; pending-proposals=256; idx=; group=;")
      --security string            Security options
                                       token=; If set, all Admin requests to Dgraph will need to have this token. The token can be passed as follows: for HTTP requests, in the X-Dgraph-AuthToken header. For Grpc, in auth-token key in the context.
                                       whitelist=; A comma separated list of IP addresses, IP ranges, CIDR blocks, or hostnames you wish to whitelist for performing admin actions (i.e., --security "whitelist=144.142.126.254,127.0.0.1:127.0.0.3,192.168.0.0/16,host.docker.internal").
                                    (default "token=; whitelist=;")
      --survive string             Choose between "process" or "filesystem".
                                       If set to "process", there would be no data loss in case of process crash, but the behavior would be nondeterministic in case of filesystem crash.
                                       If set to "filesystem", blocking sync would be called after every write, hence guaranteeing no data loss in case of hard reboot.
                                       Most users should be OK with choosing "process". (default "process")
      --telemetry string           Telemetry (diagnostic) options
                                       reports=true; Send anonymous telemetry data to Dgraph devs.
                                       sentry=true; Send crash events to Sentry.
                                    (default "reports=true; sentry=true;")
      --tls string                 TLS Server options
                                       ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                       client-auth-type=VERIFYIFGIVEN; The TLS client authentication method.
                                       client-cert=; (Optional) The client Cert file which is needed to connect as a client with the other nodes in the cluster.
                                       client-key=; (Optional) The private client Key file which is needed to connect as a client with the other nodes in the cluster.
                                       internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                       server-cert=; The server Cert file which is needed to initiate the server in the cluster.
                                       server-key=; The server Key file which is needed to initiate the server in the cluster.
                                       use-system-ca=true; Includes System CA into CA Certs.
                                    (default "use-system-ca=true; client-auth-type=VERIFYIFGIVEN; internal-port=false;")
      --tmp string                 Directory to store temporary buffers. (default "t")
      --trace string               Trace options
                                       datadog=; URL of Datadog to send OpenCensus traces. As of now, the trace exporter does not support annotation logs and discards them.
                                       jaeger=; URL of Jaeger to send OpenCensus traces.
                                       ratio=0.01; The ratio of queries to trace.
                                    (default "ratio=0.01; jaeger=; datadog=;")
      --vault string               Vault options
                                       acl-field=; Vault field containing ACL key.
                                       acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                       addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                       enc-field=; Vault field containing encryption key.
                                       enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                       path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                       role-id-file=; Vault RoleID file, used for AppRole authentication.
                                       secret-id-file=; Vault SecretID file, used for AppRole authentication.
                                    (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")
  -w, --wal string                 Directory to store raft write-ahead logs. (default "w")
  -z, --zero string                Comma separated list of Dgraph Zero addresses of the form IP_ADDRESS:PORT. (default "localhost:5080")

Use "dgraph alpha [command] --help" for more information about a command.
```



