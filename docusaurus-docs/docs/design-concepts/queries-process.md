---
title: Query Process
---


To understand how query execution works, look at an example.

```
{
    me(func: uid(0x1)) {
      rel_A
      rel_B {
        rel_B1
        rel_B2
      }
      rel_C {
        rel_C1
        rel_C2 {
          rel_C2_1
      }
      }
  }
}

```

Let's assume we have 3 Alpha instances, and instance id=2 receives this query. These are the steps:

* This query specifies the exact UID list (one UID) to start with, so there is no root query clause.
* Retreive posting lists using keys = `0x1::rel_A`, `0x1::rel_B`, and `0x1::rel_C`.
   * At worst, these predicates could belong to 3 different groups if the DB is sharded, so this would incur at most 3 network calls.
* The above posting lists would include three lists of UIDs or values.
   * The UID results (id1, id2, ..., idn) for `rel_B` are converted into queries for `id1::rel_B1` `id2::rel_B1`, etc., and for `id1::rel_B2` `id2::rel_B2`, etc.
   * Similarly, results for rel_C will be used to get the next set of UIDs from posting list keys like `id::rel_C1` and `id::rel_C2`.
* This process continues recursively for `rel_C2_1` as well, and as deep as any query requires.

More complex queries may do filtering operations, or intersections and unions of UIDs, but this recursive walk to execute a number of (often parallel) `Tasks` to retrieve UIDs characterizes Dgraph querying.

If the query was run via HTTP interface `/query`, the resulting subgraph then gets converted into JSON for
replying back to the client. If the query was run via [gRPC](https://www.grpc.io/) interface using
the language [clients](/dgraph-overview/clients/), the subgraph gets converted to
[protocol buffer](https://developers.google.com/protocol-buffers/) format and similarly returned to the client.
