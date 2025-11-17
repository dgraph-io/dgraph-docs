---
title: Change Data Capture
description: Stream database mutations and drop events to Kafka or local file sinks
---

:::note
**Enterprise Feature**: Change Data Capture requires a Dgraph Enterprise license. See [License](../../admin/enterprise-features/license) for details.
:::

Change Data Capture (CDC) streams database mutations and drop events to external sinks (Kafka or local files). CDC tracks all `set` and `delete` mutations except those affecting password fields, along with all drop events. Live Loader events are recorded; Bulk Loader events are not.

CDC events are based on Raft log changes. If the sink is unreachable by the Alpha leader, Raft logs expand as events accumulate until the sink becomes available. Enable CDC on all Alpha nodes to avoid interruptions in the event stream.

## Enable CDC with Kafka

Kafka records CDC events under the `dgraph-cdc` topic. Create the topic before events are sent to the broker.

Start Dgraph Alpha with the `--cdc` option:

```bash
dgraph alpha --cdc "kafka=kafka-hostname:port; sasl-user=tstark; sasl-password=m3Ta11ic"
```

For localhost Kafka without SASL authentication:

```bash
dgraph alpha --cdc "localhost:9092"
```

For TLS-enabled Kafka clusters, the `ca-cert` option is required. The certificate can be self-signed.

## Enable CDC with File Sink

To stream CDC events to a local unencrypted file, start Dgraph Alpha with:

```bash
dgraph alpha --cdc "file=local-file-path"
```

## Command Reference

The `--cdc` option supports the following sub-options:

| Sub-option       | Example `dgraph alpha` command option     | Notes                                                                |
|------------------|-------------------------------------------|----------------------------------------------------------------------|
|  `tls`           | `--tls=false`                             | boolean flag to enable/disable TLS while connecting to Kafka.        |
|  `ca-cert`       | `--cdc "ca-cert=/cert-dir/ca.crt"`        | Path and filename of the CA root certificate used for TLS encryption, if not specified, Dgraph uses system certs if `tls=true` |
|  `client-cert`   | `--cdc "client-cert=/c-certs/client.crt"` | Path and filename of the client certificate used for TLS encryption  |
|  `client-key`    | `--cdc "client-cert=/c-certs/client.key"` | Path and filename of the client certificate private key              |
|  `file`          | `--cdc "file=/sink-dir/cdc-file"`         | Path and filename of a local file sink (alternative to Kafka sink)   |
|  `kafka`         | `--cdc "kafka=kafka-hostname; sasl-user=tstark; sasl-password=m3Ta11ic"` | Hostname(s) of the Kafka hosts. May require authentication using the `sasl-user` and `sasl-password` sub-options |
|  `sasl-user`     | `--cdc "kafka=kafka-hostname; sasl-user=tstark; sasl-password=m3Ta11ic"` | SASL username for Kafka. Requires the `kafka` and `sasl-password` sub-options |
|  `sasl-password` | `--cdc "kafka=kafka-hostname; sasl-user=tstark; sasl-password=m3Ta11ic"` | SASL password for Kafka. Requires the `kafka` and `sasl-username` sub-options |
|  `sasl-mechanism` | `--cdc "kafka=kafka-hostname; sasl-mechanism=PLAIN"` | The SASL mechanism for Kafka (PLAIN, SCRAM-SHA-256 or SCRAM-SHA-512). The default is PLAIN |

## Data Format

CDC events are in JSON format. Example:

```json
{ "key": "0", "value": {"meta":{"commit_ts":5},"type":"mutation","event":{"operation":"set","uid":2,"attr":"counter.val","value":1,"value_type":"int"}}}
```

The `meta.commit_ts` value increases with each CDC event. Use this value to identify duplicate events that may occur due to Raft leadership changes.

### Mutation Events

**Set mutation:**

```json
{"meta":{"commit_ts":29},"type":"mutation","event":{"operation":"set","uid":3,"attr":"counter.val","value":10,"value_type":"int"}}
```

**Delete mutation:**

```json
{"meta":{"commit_ts":44},"type":"mutation","event":{"operation":"del","uid":7,"attr":"Author.name","value":"_STAR_ALL","value_type":"default"}}
```

### Drop Events

**Drop all:**

```json
{"meta":{"commit_ts":13},"type":"drop","event":{"operation":"all"}}
```

The `operation` field specifies the drop operation: `attribute`, `type`, `data`, or `all`.

## Multi-Tenancy

In multi-tenants environment, CDC events streamed to Kafka are distributed across Kafka partitions by the Kafka client based on the multi-tenancy namespace.

## Limitations

- CDC events track only new values, not old values updated or removed by mutations or drop operations
- Schema updates are not tracked
- CDC can only be configured when starting Alpha nodes with the `dgraph alpha` command
- Node crashes or Raft leadership changes may result in duplicate events, but no data loss
