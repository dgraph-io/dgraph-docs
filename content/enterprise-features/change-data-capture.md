+++
title = "Change Data Capture"
description = "With a Dgraph enterprise license, you can use Dgraph's change data capture (CDC) capabilities to track data changes over time."
weight = 2
[menu.main]
    parent = "enterprise-features"
+++

With a Dgraph [enterprise license]({{< relref "enterprise-features/license.md" >}}),
you can use change data capture (CDC) to track data changes over time, including
mutations and drops (deletes) in your database. Dgraph's CDC implementation lets
you use Kafka or a local file as a *sink* to store the CDC updates streamed by
Dgraph Alpha leader nodes. 

When CDC is enabled, Dgraph streams all mutations except those that update
password fields, along with any drop events. Live Loader events are tracked by
CDC, but Bulk Loader events aren't.

### Enable CDC

To enable CDC, start Dgraph Alpha with the `--cdc` command, as in the following
command example:

```bash
dgraph alpha --cdc "kafka=kafka-hostname; sasl-user=tstark; sasl-password=m3Ta11ic"
```

## CDC command reference

The `--cdc` option includes several sub-options that you can use to configure
CDC when running the `dgraph alpha` command



# DRAFTY: FROM PR:

Flag: cdc and various sub-options for change data capture are.

- file=/path/to/directory where audit logs will be stored
- kafka=host1,host2 to define comma separated list of host.
- sasl-user=username to define sasl username for kafka.
- sasl-password=password to define sasl password for kafka.
- ca-cert=/path/to/ca/crt/file to define ca cert for tls encryption.
- client-cert=/path/to/client/cert/file to define the client certificate for tls encryption.
- client-key=/path/to/client/key/file to define the client key for tls encryption.

Test Cases Verified:

- Sink Fails and comes back up. Pending events are sent to the sink
- Sink fails and then leader fails. Then sink comes up and events are reaching to the sink
- Waiting txns are getting sent and pending events are getting cleared with time.
- Aborted txns are getting cleared
- In case of leadership changes, old events are not being sent.
- for live loader we are getting all events,
- For bulk loader no events.

Sample events for file-based sink looks like this:

```json
{ "key": "0", "value": {"meta":{"commit_ts":5},"type":"mutation","event":{"operation":"set","uid":2,"attr":"counter.val","value":1,"value_type":"int"}}}
```

# DRAFTY: FROM DISCUSS:

The leader of each group will be streaming out CDC updates. Later on, once we have namespaces(from multi tenancy), we will make it listen to updates accordingly.

We have made raft logs readable for CDC. Hence each raft entry would be read and sent as CDC event if necessary. This ensures all the guarantees we needed for CDC.

Solution:

* CDC will be managed via config flags.
* CDC job will read the raft logs and decide which events to send based on the type of operation.
* Initially only Kafka will be provided as a sink. All alpha nodes are required to specify with the Kafka sink config, for CDC to work efficiently.
* Events will be sent out via leader node only.
* Events will be sent to Kafka topics named as dgraph-cdc. Later with multi-tenancy, events will be distributed based on namespaces over the partitions.

Handling Drop operations:

There are 4 kinds of drop operations:

    Drop All
    Drop Data
    Drop Attribute
    Drop Type

Drop Event will be sent for each of these cases.

Sample a DROP ALL event would look like this:

```json
{"meta":{"commit_ts":13},"type":"drop","event":{"operation":"all"}}
```

Mutation Events

There will be 2 kinds of events; Set and Delete that we will be emitting. Other DBs do support another operation Update that would be costly for us to support because of extra lookup needed for that. We don’t intend to support that.

Raft entries will have information about Predicate, EntityId, Value and DataType. Information extracted from these entries would go into Set and Delete field of JSON below.

A Set mutation event updating counter.val to 10 would look like this:

```json
{"meta":{"commit_ts":29},"type":"mutation","event":{"operation":"set","uid":3,"attr":"counter.val","value":10,"value_type":"int"}}
```

Similarly, a sample Delete mutation event of removing all values for predicate Author.name for a node with uid=7 would look like this:

```json
{"meta":{"commit_ts":44},"type":"mutation","event":{"operation":"del","uid":7,"attr":"Author.name","value":"_STAR_ALL","value_type":"default"}}
```

Integration With Sink Clients

Initially, only two sink clients will be available i.e. Kafka and File.

    Kafka will adhere to the TLS encryption as well as sasl authentication. All the CDC events will be generated over the default topic and events will be distributed based on namespace over the partitions.
    File-based sinks are just dumping events into a file. This is generally useful in the case of testing.

Important things to note

    If the sink is failing or down, clients will not lose events. But it will lead to an increase in the raft files because CDC jobs read the raft logs and since no events are getting published, raft files are not getting cleared. Hence it becomes necessary to manage the cluster properly in case of failure events.
    In case of node crashes or leadership changes there might be duplicated events but no loss of events.
    In the case of live loader, there will be events for each predicate.
    In the case of an old cluster, CDC events will be sent from the last raft index available.
    In the case of bulk loader, there will be no events.
    Value for password fields will not be sent out in CDC events.

Limitations

    CDC is not supported in case of ludicrous mode. We are working on fixing this. We will update the timelines for that later.
    Schema updates will not available over CDC at this moment. We are working on fixing this. We will update the timelines for that later.

Important: This is an enterprise feature.
