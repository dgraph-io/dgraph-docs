+++
title = "Change Data Capture"
description = "With a Dgraph enterprise license, you can use Dgraph's change data capture (CDC) capabilities to track data changes over time."
weight = 5
[menu.main]
    parent = "enterprise-features"
+++

With a Dgraph [enterprise license]({{< relref "enterprise-features/license.md" >}}),
you can use change data capture (CDC) to track data changes over time; including
mutations and drops in your database. Dgraph's CDC implementation lets you use
Kafka or a local file as a *sink* to store CDC updates streamed by Dgraph Alpha
leader nodes. 

When CDC is enabled, Dgraph streams events for all `set` and `delete` mutations,
except those that affect password fields; along with any drop  events. Live
Loader events are recorded by CDC, but Bulk Loader events aren't.

CDC events are based on changes to Raft logs. So, if the sink is not reachable
by the Alpha leader node, then Raft logs expand as events are collected on
that node until the sink is available again. You should enable CDC on all Dgraph
Alpha nodes to avoid interruptions in the stream of CDC events.

## Enable CDC with Kafka sink

Kafka records CDC events under the `dgraph-cdc` topic. To enable CDC and sink
events to Kafka, start Dgraph Alpha with the `--cdc` command and the sub-options
shown below, as follows:

```bash
dgraph alpha --cdc "kafka=kafka-hostname:port; sasl-user=tstark; sasl-password=m3Ta11ic"
```

If you use Kafka on the localhost without SASL authentication, you can just 
specify the hostname and port used by Kafka, as follows:

```bash
dgraph alpha --cdc "localhost:9092"
```

## Enable CDC with file sink

To enable CDC and sink results to a local unencrypted file, start Dgraph Alpha
with the `--cdc` command and the sub-option shown below, as follows:

```bash
dgraph alpha --cdc "file=local-file-path"
```

## CDC command reference

The `--cdc` option includes several sub-options that you can use to configure
CDC when running the `dgraph alpha` command:

| Sub-option       | Example `dgraph alpha` command option     | Notes                                                                |
|------------------|-------------------------------------------|----------------------------------------------------------------------|
|  `ca-cert`       | `--cdc "ca-cert=/cert-dir/ca.crt"`        | Path and filename of the CA root certificate used for TLS encryption |
|  `client-cert`   | `--cdc "client-cert=/c-certs/client.crt"` | Path and filename of the client certificate used for TLS encryption  |
|  `client-key`    | `--cdc "client-cert=/c-certs/client.key"` | Path and filename of the client certificate private key              |
|  `file`          | `--cdc "file=/sink-dir/cdc-file"`         | Path and filename of a local file sink (alternative to Kafka sink)   |
|  `kafka`         | `--cdc "kafka=kafka-hostname; sasl-user=tstark; sasl-password=m3Ta11ic"` | Hostname(s) of the Kafka hosts. May require authentication using the `sasl-user` and `sasl-password` sub-options. |
|  `sasl-user`     | `--cdc "kafka=kafka-hostname; sasl-user=tstark; sasl-password=m3Ta11ic"` | SASL username for Kafka. Requires the `kafka` and `sasl-password` sub-options. |
|  `sasl-password` | `--cdc "kafka=kafka-hostname; sasl-user=tstark; sasl-password=m3Ta11ic"` | SASL password for Kafka. Requires the `kafka` and `sasl-username` sub-options. |

## CDC data format


CDC events are in JSON format. Most CDC events look like the following example:

```json
{ "key": "0", "value": {"meta":{"commit_ts":5},"type":"mutation","event":{"operation":"set","uid":2,"attr":"counter.val","value":1,"value_type":"int"}}}
```

The `Meta.Commit_Ts` value (shown above as `"meta":{"commit_ts":5}`) will increase
with each CDC event, so you can use this value to find duplicate events if those 
occur due to Raft leadership changes in your Dgraph Alpha group.

### Mutation event examples

A set mutation event updating `counter.val` to 10 would look like the following:

```json
{"meta":{"commit_ts":29},"type":"mutation","event":{"operation":"set","uid":3,"attr":"counter.val","value":10,"value_type":"int"}}
```

Similarly, a delete mutation event that removes all values for the `Author.name`
field for a specified node would look like the following:

```json
{"meta":{"commit_ts":44},"type":"mutation","event":{"operation":"del","uid":7,"attr":"Author.name","value":"_STAR_ALL","value_type":"default"}}
```

### Drop event examples

CDC drop events look like the following example event for "drop all":

```json
{"meta":{"commit_ts":13},"type":"drop","event":{"operation":"all"}}
```

The `operation` field specifies which drop operation (`attribute`, `type`,
specified `data`, or `all` data) is tracked by the CDC event.

## CDC and multi-tenancy

When you enable CDC in a [multi-tenant environment]({{< relref "multitenancy.md" >}}),
CDC events streamed to Kafka are distributed by the Kafka client. It distributes
events between the available Kafka partitions based on their multi-tenancy
namespace.

## Known limitations

CDC has the following known limitations:

* CDC events do not track old values that are updated or removed by mutation or
  drop operations; only new values are tracked
* CDC is not currently supported when Dgraph is in Ludicrous mode
* CDC does not currently track schema updates
* You can only configure or enable CDC when starting Alpha nodes using the
 `dgraph alpha` command
* If a node crashes or the leadership of a Raft group changes, CDC might have
  duplicate events, but no data loss
