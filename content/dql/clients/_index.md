+++
date = "2023-03-23T22:25:17+11:00"
title = "Client Libraries"
description = "Dgraph client libraries in various programming languages."
weight = 7
aliases = ["/clients"]
[menu.main]
  identifier = "clients"
  parent = "dql"
+++

Dgraph client libraries allow you to run DQL transactions, queries and mutations in various programming languages.

If you are interested in clients for GraphQL endpoint, please refer to [GraphQL clients]({{< relref "graphql-clients">}}) section.


Go, python, Java, C# and JavaScript clients are using **[gRPC](http://www.grpc.io/):** protocol and [Protocol
  Buffers](https://developers.google.com/protocol-buffers) (the proto file
used by Dgraph is located at
[api.proto](https://github.com/dgraph-io/dgo/blob/master/protos/api.proto)).

A JavaScript client  using **HTTP:** is also available.


It's possible to interface with Dgraph directly via gRPC or HTTP. However, if a
client library exists for your language, that will be an easier option.

{{% notice "tip" %}}
For multi-node setups, predicates are assigned to the group that first sees that
predicate. Dgraph also automatically moves predicate data to different groups in
order to balance predicate distribution. This occurs automatically every 10
minutes. It's possible for clients to aid this process by communicating with all
Dgraph instances. For the Go client, this means passing in one
`*grpc.ClientConn` per Dgraph instance, or routing traffic through a load balancer.
Mutations will be made in a round robin
fashion, resulting in a semi-random initial predicate distribution.
{{% /notice %}}

### GraphQL Clients
Dgraph does not force or insist on any particular GraphQL client. Any GraphQL client, GUI, tool, or library will work well with Dgraph, and it is the users' choice which to choose. Dgraph only provides clients for the proprietary DQL query language. GraphQL clients are available for free from many organizations.

There is however, a basic GraphQL web-based tool included in the [Dgraph cloud GUI](https://cloud.dgraph.io) for convenience.
### Transactions

Dgraph clients perform mutations and queries using transactions. A
transaction bounds a sequence of queries and mutations that are committed by
Dgraph as a single unit: that is, on commit, either all the changes are accepted
by Dgraph or none are.

A transaction always sees the database state at the moment it began, plus any
changes it makes --- changes from concurrent transactions aren't visible.

On commit, Dgraph will abort a transaction, rather than committing changes, when
a conflicting, concurrently running transaction has already been committed.  Two
transactions conflict when both transactions:

- write values to the same scalar predicate of the same node (e.g both
  attempting to set a particular node's `address` predicate); or
- write to a singular `uid` predicate of the same node (changes to `[uid]` predicates can be concurrently written); or
- write a value that conflicts on an index for a predicate with `@upsert` set in the schema (see [upserts]({{< relref "howto/upserts.md">}})).

When a transaction is aborted, all its changes are discarded.  Transactions can be manually aborted.


### In this section
