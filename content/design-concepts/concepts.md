+++
date = "2017-03-20T22:25:17+11:00"
title = "Concepts"
weight = 3
[menu.main]
    parent = "design-concepts"
+++

## Relationships

Dgraph stores `relationships` among `entities` to represent graph structures, and also stores literal properties of `entities`. 

This makes it easy for Dgraph to ingest the RDF [N-Quad](https://www.w3.org/TR/n-quads/) format, where each line represents

* `Node, RelationName, Node, Label` or
* `Node, RelationName, ValueLiteral, Label`

The first represents relations among entities (nodes in graph terminology) and the second represents the relationship of a Node to all it's named attributes.

Often, the optional `Label` is omitted, and therefore the N-Quad data is also referred to as "triples." When it is included, it represents which `Tenant` or `Namespace` the data lives in within Dgraph.

In our product (the code or the GUI, and also in older documentation) you may see other terminology such as

Edge instead of Relationship
Predicate instead of Relationship
Entity or Vertex instead of Node

Similarly in the RDF spec you'll see 
Subject and Object instead of Node
Predicate instead of Relationship.

This is unavoidable, since graph databases, RDF, and graph theory have separate origins that do not all share terminology.

{{% notice "tip" %}}Dgraph can automatically generate a reverse relation. If the user wants to run
queries in that direction, they would need to define the [reverse relationship]({{< relref "predicate-types.md#reverse-edges" >}})


For `Relationships`, the subject and object are represented as 64-bit numeric UIDs and the relationship name itself links them: <subjectUID> <relationshipName> <objectUID>.

For literal attributes of a `Node`, the subject must still (and always) be a numeric UID, but the Object will be a primitive value. These can be thought of as <subjectUID> <relationshipName> <value>, where value is not a 64-bit UID, and is instead a: string, float, int, dateTime, geopoint, or boolean.

## Posting Lists and Tablets
Dgraph groups all relationships of a given type together into one data structure called a `tablet`. E.g. in a database of people who are friends with one another, and have first names and last names, the three relations might be: "friend", "firstName", and "lastName". The full set of data for each relation is called a `tablet` and is also a shard in a Dgraph sharded database, because Dgraph shards based on relationships.

Conceptually, a posting list contains all the `Relationships` of one kind corresponding to one `Node`, in the following format:

```
RelationshipName::NodeUID -> sorted list of other Node UIDs // Everything in uint64 representation.
```
Note the composite key "RelationshipName::NodeUID emphasizing that a posting list is the related data for one Node, within one Relationship.

E.g., if we're storing a list of friends, we may have three posting lists:

Node  | Attribute| ValueId
------- |----------|--------
Me      | friend   | person0
Me      | friend   | person1
Me      | friend   | person2
Me      | friend   | person3

Node  | Attribute| ValueId
------- |----------|--------
person1 | friend   | person2
person1 | friend   | Me

Node  | Attribute| ValueId
------- |----------|--------
person2 | friend   | person3

One structure for the (directional) friends of each person.

The tablet for the relation `friend` holds all posting lists for all "friend" relationships in the entire graph. Three in this example. Seeking for `Me` in this tablet would retrieve the single posting list of my friends, namely `[person0, person1, person2, person3]`.

The main advantage of having such a structure is that we have all the data to do one join in one
`tablet` on one server/shard. This means, one RPC to
the machine serving that `Tablet` will be adequate, as documented in [How Dgraph Minmizes Network Calls]({{< relref "minimizing-network-calls" >}}).

Implementation wise, a `Posting List` is a list of `Postings`, and each Posting is either one related Node or one literal value. 

##  Badger
[Badger](https://github.com/dgraph-io/badger) is a key-value store developed and maintained by Dgraph. It is also open source, and it is the backing store for Dgraph data. 

It is largely transparent to users that Dgraph uses Badger to store data internally. Badger is packaged into the Dgraph binary, and is the persistence layer. However, various configuration settings and log messages may reference Badger, such as cache sizes.

Badger values are `Posting Lists` and indexes. Badger Keys are formed by concatenating <RelationshipName>+<NodeUID>.


## Group
A `Group` in Dgraph is a shard of data, and may or may not be highly-available (HA). An HA group typically has three Dgraph instances (servers or K8s pods), and a non-HA group is a single instance. Every Alpha instance belongs to one group, and each group is responsible for serving a
particular set of tablets (relations). In an HA configuration, the three or more instances in a single group replicate the same data to every instance to ensure redundancy of data.

In a sharded Dgraph cluster, tablets are automatically assigned to each group, and dynamically relocated as sizes change to keep the groups balanced. Predicates can also be moved manually if desired.

In a future version, if a tablet gets too big, it will be split among two groups, but currently data is balanced by moving each tablet to one group only.

To avoid confusion, remember that you may have many Dgraph alpha instances due to either sharding, or due to HA configuration. If you have both sharding and HA, you will have 3*N groups:

   config    | Non-HA            |   HA
-------------|-------------------|--------
Non-sharded  | 1 alpha total     |  3 alphas total
Sharded      | 1 alpha per group |  3*N alphas for N groups


## High Availability and Replication
Each Highly-Available (HA) group will be served by at least 3 servers (or two if one is temporarily unavailable). In the case of a machine
failure, other servers serving the same group still handle the load for data in the group.

In addition, Dgraph `Learner Nodes` hold replicas of data, but this replication is to suupport read replicas, typically in a different geography from the master cluster. This replication is independent of HA replication.

## New Servers and Discovery
Dgraph clusters will detect new machines allocated to the [cluster]({{< relref "deploy/cluster-setup.md" >}}),
establish connections, and transfer data to the new server based on the group the new machine is in.

## Write Ahead Logs (WAL) and Memtables
Per the MVCC approach, transactions write data to a `Write-Ahead Log` to ensure it is durably stored. Soon after commit, data is also updated in the `memtables` which are buffers holding all new data. The `memtables` are mutable, unlike the SST files written to disk which hold most data. Once full, memtables are flushed to disk and become SST files. See Log Compaction for more details on this process.

In the event of a system crash, the persistent data in the Write Ahead Logs is replayed to rebiuld the memtables and restore the full state from before the crash.

## Transactions and Mutations

Borrowing from GraphQL, Dgraph calls writes to the database `Mutations`. As noted elsewhere (MVCC, LSM Trees and Write Ahead Log sections) writes are written persistently to the Write Ahead Log, and ephemerally to a memtable. 

Data is queried from the combination of persistent SST files and ephemeral memtable data structures. The mutations therefore always go into the memtables first (though are also written durably to the WAL). The memtables are the "Level 0" overlay on top of the immutable SST files, to use LSM Tree terminology.

In addition to being written to `Write Ahead Logs`, a mutation also gets stored in memory as an
overlay over immutable `Posting list` in a mutation layer. This mutation layer allows us to iterate
over `Posting`s as though they're sorted, without requiring re-creating the posting list.


## Queries

Let's understand how query execution works, by looking at an example.

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
the language [clients]({{< relref "clients/_index.md" >}}), the subgraph gets converted to
[protocol buffer](https://developers.google.com/protocol-buffers/) format and similarly returned to the client.

## Network Calls
Compared to RAM or SSD access, network calls are slow, so Dgraph is built from the ground up to minimize them. For graph databases which store sub-graphs on different shards, this is difficult or impossible, but predicate-based (relationship-based) sharding allows fast distributed query with Dgraph.

See [How Dgraph Minmizes Network Calls]({{< relref "minimizing-network-calls" >}}) for more details.

## Workers and Worker Pools
Dgraph maintains a fixed set of worker processes that retrieve and execute queries in parallel as they are sent over HTTP or gRPC. Dgraph also parallelizes Tasks within a query execution, to maximize parallelism and more fully utilize system resources. Dgraph is written in the go language, which supports high numbers of parallel goroutines, enabling this approach without creating massive numbers of OS threads which would be slower.


## Protocol Buffers
All data in Dgraph that is stored or transmitted among the Dgraph instances (servers) is converted into space-optimized byte arrays using [Protocol Buffers](https://developers.google.com/protocol-buffers/). Protocol Buffers are a standard, optimized technology to speed up network communications.

## DQL
DQL is the "Dgraph Query Language" and is based on GraphQL. It is neither a superset nor subset of GraphQL, but is generally more powerful than GraphQL. DQL coexists nicely with GraphQL so many users perform most access using GraphQL and only "drop down" into DQL when there is a particular query mechanism needed that is not supported in the GraphQL spec. E.g. @recurse query operations are only in DQL. Other customers simply use DQL. DQL supports both queries and mutations, as well as hybrid "upsert" operations.

## GraphQL
 `GraphQL` is a query and update standard defined at [GraphQL.org](https://graphql.org/). `GraphQL` is natively supported by Dgraph, without requiring additional servers, data mappings or resolvers. Typically, "resolving" a data field in GraphQL simply corresponds to walking that relationship in Dgraph.
 
 Dgraph also auto-generates access functions for any `GraphQL Schema`, allowing users to get up and running in minutes with Dgraph + a GraphQL schema. The APIs are auto-generated.

GraphQL is internally converted to the (similar-but-different) `DQL` query language before being executed. We can think of GraphQL as "sitting on top" of DQL.

## Dgraph Schemas
Dgraph natively supports GraphQL, including `GraphQL Schema`s. GraphQL schemas "sit on top of" DQL schemas, in the sense that when a GraphQL schema is added to Dgraph, a corresponding `DQL Schema` is automatically created.

For example, if you add GraphQL Schema fragment
```
type Task {
  id: ID!
  title: String! @search(by: [fulltext])
  completed: Boolean! @search
  user: User!
}
```
to Dgraph, the following DQL schema relationships (predicates) will be auto generated:
```
Task.title
Task.completed
Task.user
```
and the DQL notion of a uid (which all entities in Dgraph have) will be mapped to the GraphQL ID! property.

This provides an ability to query GraphQL data using DQL, by using the qualified relationship names of the form <Type>.<property> from DQL.

## Dgraph Clients
Dgraph provides [client libraries]({{< relref "clients/_index.md" >}}) for many languages. These clients send DQL queries, and perform useful functions such as logging in, in idomatic ways in each language.

Note that Dgraph does not force or insist on any particular GraphQL client. Any GraphQL client, GUI, tool, or library will work well with Dgraph, and it is the users' choice which to choose. Dgraph only provides clients for the proprietary DQL query language.

However, Dgraph's cloud console does support basic GraphQL querying, so this is something of a tool. We recommend using a mature GraphQL console instead, as they are more mature. Dgraph's GraphQL GUI function is for quick start and convenience.

## Dgraph Ratel GUI
Dgraph provides the `Ratel` GUI tool for DQL querying and basic graph visualization. Ratel does not support GraphQL queries, since there are many mature tools and every user or company is likely to have their own preferred tools for GraphQL development.

## Facets
Dgraph allows a set of properties to be associated with any `Relationship`. E.g. if there is a "worksFor" relationships between Node "Bob" and Node "Google", this relationship may have facet values of "since": 2002-05-05 and "position": "Engineer".

Facets can always be replaced by adding a new Node representing the relationship and storing the facet data as attriubutes of the new Node.

## Indexing and Tokenizers
Typically, Dgraph query access is optimized for forward access. When other access is needed, an index may speed up queries. Indexes are large structures that hold all values for some Relation (vs `Posting Lists`, which are typically smaller, per-Node structures).

Tokenizers are simply small algorithms that create the indexed values from some Node property. E.g. if a Book Node has a Title attribute, an you add a "term" index, each word (term) in the text will be indexed. The term "Tokenizer" makes the most sense for this index type.

Similary if the Book has a publicationDateTime you can add a day or year index. The "tokenizer" here extracts the value to be indexed, which may be the day or hour of the dateTime, or only the year.

## Lambdas
Dgraph Lambdas are JavaScript functions that can be used during query or mutation processing to extend GraphQL or DQL queries and mutations. Lambdas are not related at all to AWS Lambdas. They are functions that run in an (optional) node.js server that is included in the Dgraph Cloud offering. 

## ACLs
Dgraph Access Control Lists (ACLs) are sets of permissions for which `Relationships` a user may access. Recall that Dgraph is "predicate based" so all data is stored in and is implicit in relationships. This allows relationship-based controls to be very powerful in restricting a graph based on roles (RBAC).

Note that the Dgraph multi-tenancy feature relies on ACLs to ensure each tenant can only see their own data in one server.

Using ACLs requires a client to authenticate (log in) differently and specify credentials that will drive which relationships are visible in their view of the graph database.

## Namespace or Tenant
A Dgraph `Namespace` (aka Tenant) is a logically separate database within a Dgraph cluster. A Dgraph cluster can host many Namespaces (and this is how the Dgraph "shared" cloud offering works). Each Tenant logs into their own namespace using their own credentials, and sees only their own data. 

There is no mechanism to query in a way that combines data from two namespaces, which simplifies and enforces security in use cases where this is the requirement. An API layer or client would have to pull data from multiple namespaces using different authenticated queries if data needed to be combined.

