---
title: Client Libraries
description: Dgraph client libraries in various programming languages.
---

Dgraph client libraries allow you to run DQL transactions, queries and mutations in various programming languages.

If you are interested in clients for GraphQL endpoint, please refer to [GraphQL clients](/graphql/graphql-clients) section.


Go, python, Java, C# and JavaScript clients are using **[gRPC](http://www.grpc.io/):** protocol and [Protocol
  Buffers](https://developers.google.com/protocol-buffers) (the proto file
used by Dgraph is located at
[api.proto](https://github.com/dgraph-io/dgo/blob/master/protos/api.proto)).

A JavaScript client  using **HTTP:** is also available.


It's possible to interface with Dgraph directly via gRPC or HTTP. However, if a
client library exists for your language, that will be an easier option.

:::tip
For multi-node setups, predicates are assigned to the group that first sees that
predicate. Dgraph also automatically moves predicate data to different groups in
order to balance predicate distribution. This occurs automatically every 10
minutes. It's possible for clients to aid this process by communicating with all
Dgraph instances. For the Go client, this means passing in one
`*grpc.ClientConn` per Dgraph instance, or routing traffic through a load balancer.
Mutations will be made in a round robin
fashion, resulting in a semi-random initial predicate distribution.
:::


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
- write a value that conflicts on an index for a predicate with `@upsert` set in the schema (see [upserts](/dql/upserts)).

When a transaction is aborted, all its changes are discarded.  Transactions can be manually aborted.

#### Abort reasons

A write-write conflict is not the only reason a commit can abort. When Dgraph
aborts a commit it reports a *category* describing why, so clients can decide
how to react (for example, retry immediately versus back off). The category is
carried as a `"<code>: <detail>"` prefix on the gRPC `ABORTED` status message
(and on the HTTP error message), where `<code>` is one of:

- `conflict` — a write-write conflict with another concurrent transaction, as
  described above. Retrying the transaction typically succeeds.
- `stale-startts` — the transaction's start timestamp is older than the oldest
  timestamp the server can still validate against. That happens after a Zero
  leader change, and also when Zero trims its conflict map at a snapshot, which
  is not a leader change. Retrying with a fresh transaction succeeds.
- `predicate-move` — a predicate the transaction wrote is being moved between
  groups so commits on it are blocked, or it finished moving while the
  transaction was open. Retrying once the move completes succeeds.

The full message reads `<code>: Transaction has been aborted. Please retry. <detail>`.
Every abort message, with or without a category, contains
`Transaction has been aborted. Please retry`, as it did before categories existed.

:::note[Not every abort has a category]
Some aborts carry **no** prefix, and that is deliberate. Where the server cannot
map a cause onto one of the categories above, it sends the explanation without a
code rather than borrowing one that would imply the wrong remedy. Clients report
those as `UNKNOWN`.

That covers aborts from **older servers**, which do not categorize at all, and
also causes a **current** server declines to categorize — for example a
transaction already aborted out of band by a schema change or the
idle-transaction reaper, a cancelled or timed-out request, or a predicate no
group currently serves. `UNKNOWN` therefore does not mean your server is out of
date. The description still explains what happened; only the machine-readable
category is absent.
:::

:::tip[Detect aborts by status code, not message text]
Treat the gRPC `ABORTED` status code (or the HTTP error response) as the signal
that a commit aborted, and the message as detail only. Message text differs per
category and is not a stable contract — it may be reworded or extended between
releases. The official clients all branch on the status code, and an
unrecognized or absent prefix degrades to `UNKNOWN`, so a newer server can add
categories without breaking an older client.
:::

#### What a `conflict` can and cannot tell you

A conflict does not name a predicate or UID, and cannot: conflict keys are
one-way fingerprints by the time the server compares them, so the specific key
is unrecoverable.

This matters when tuning a schema, because the culprit is not necessarily the
data you wrote directly. Writing one triple can write several keys, and any of
them can collide:

- the **data** key you set;
- an **index** key, if the predicate is indexed;
- a **count** key, if the predicate has `@count`.

`@upsert` changes the rule rather than adding a key: the UID is excluded from
the comparison, so **any** two transactions writing the same value conflict, not
just two writing the same node. That is how uniqueness is enforced, and it is a
common source of surprising conflicts in upsert-heavy ingest.

Reverse edges (`@reverse`) never cause conflicts, and predicates marked
`@noconflict` are excluded from conflict detection entirely.

The official [Go](/clients/go), [Java](/clients/java) and [Python](/clients/python)
clients parse this category into a typed value; see those pages for the API.


### In this section
