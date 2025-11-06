---
title: Dgraph Glossary
description: Dgraph terms
---

:::note
*This is a glossary of Dgraph terms*

### Alpha ###
A Dgraph cluster consists of [Zero](#zero) and Alpha nodes. Alpha nodes host relationships (also known as predicates) and indexes. Dgraph scales horizontally by adding more Alphas.

### Badger ###
Badger is a fast, open-source key-value database written in pure Go that provides the storage layer for Dgraph.
More at [Badger documentation](https://dgraph.io/docs/badger)

### DQL ###
Dgraph Query Language is Dgraph's proprietary language to insert, update, delete and query data. It is based on GraphQL, but is more expressive. (See also: [GraphQL](#graphql))

### Edge ###
In the mental picture of a graph: bubbles connected by lines ; the bubbles are nodes, the lines are edges.
In Dgraph terminology edges are [relationships](#relationship) i.e an information about the relation between two nodes.

### Facet ###
A facet represents a property of a [relationship](#relationship).

### Graph ###
A graph is a simple structure that maps relations between objects. In Dgraph terminology, the objects are [nodes](#node) and the connections between them are [relationships](#relationship).

### GraphQL ###
[GraphQL](https://graphql.org/) is a declarative language for querying data used by application developers to get the data they need using GraphQL APIs. GraphQL is an open standard with a robust ecosystem.  Dgraph supports the deployment of a GraphQL data model (GraphQL schema) and automatically exposes a GraphQL API endpoint accepting GraphQL queries.

### gRPC ###
[gRPC](https://grpc.io/) is a high performance Remote Procedure Call (RPC) framework used by Dgraph to interface with clients. Dgraph has official gRPC clients for go, C#, Java, JavaScript and Python. Applications written in those language can perform mutations and queries inside transactions using Dgraph clients.

### Lambda ###
A Lambda Resolver (Lambda for short) is a GraphQL resolver supported within Dgraph. A Lambda is a user-defined JavaScript function that performs custom actions over the GraphQL types, interfaces, queries, and mutations. Dgraph Lambdas are unrelated to AWS Lambdas.

### Mutation ###
A mutation is a request to modify the database. Mutations include insert, update, or delete operations. A Mutation can be combined with a query to form an [Upsert](#upsert).

### Node ###
Conceptually, a node is "a thing" or an object of the business domain. For every node, Dgraph stores and maintains a universal identifier [UID](#uid), a list of properties, and the [relationships](#relationship) the node has with other nodes.

The term "node" is also used in software architecture to reference a physical computer or a virtual machine running a module of Dgraph in a cluster. See [Aplha node](#alpha) and [Zero node](#zero).

### Predicate ###
In [RDF](#rdf) terminology, a predicate is the smallest piece of information about an object. A predicate can hold a literal value or can describe a relation to another entity :
- when we store that an entity name is "Alice". The predicate is ``name`` and predicate value is the string "Alice". It becomes a node property.
- when we store that Alice knows Bob, we may use a predicate ``knows`` with the node representing Alice. The value of this predicate would be the [uid](#uid) of the node representing Bob. In that case, ``knows`` is a [relationship](#relationship).

### RATEL ###
Ratel is an open source GUI tool for data visualization and cluster management that’s designed to work with Dgraph and DQL. See also: [Ratel Overview](/ratel).

### RDF ###
RDF 1.1 is a Semantic Web Standard for data interchange. It allows us to make statements about resources. The format of these statements is simple and in the form of `<subject> <predicate> <object>`.
Dgraph supports the RDF format to create, import and export data. Note that Dgraph also supports the JSON format.


### Relationship ###
A relationship is  a named, directed link relating one [node](#node) to another. It is the Dgraph term similar to [edge](#edge) and [predicate](#predicate). In Dgraph a relationship may itself have properties representing information about the relation, such as weight, cost, timeframe, or type. In Dgraph the properties of a relationship are called [facets](#facet).

### Sharding ###
Sharding is a database architecture pattern to achieve horizontal scale by distributing data among many servers. Dgraph shards data per relationship, so all data for one relationship form a single shard, and are stored on one (group of) servers, an approach referred to as 'predicate-based sharding'.

### Triple ###
Because RDF statements consist of three elements: `<subject> <predicate> <object>`, they are called triples. A triple represents a single atomic statement about a node. The object in an RDF triple can be a literal value or can point to another node. See [DQL RDF Syntax](/dgraph-overview/dql/dql-rdf) for more details.
- when we store that a node name is "Alice". The predicate is ``name`` and predicate value is the string "Alice". The string becomes a node property.
- when we store that Alice knows Bob, we may use a predicate ``knows`` with the node representing Alice. The value of this predicate would be the [uid](#uid) of the node representing Bob. In that case, ``knows`` is a [relationship](#relationship).


### UID ###
A UID is the Universal Identifier of a node. `uid` is a reserved property holding the UID value for every node. UIDs can either be generated by Dgraph when creating nodes, or can be set explicitly.


### Upsert ###
An upsert operation combines a Query with a [Mutation](#mutation). Typically, a node is searched for, and then depending on if it is found or not, a new node is created with associated predicates or the exixting node relationships are updated. Upsert operations are important to implement uniqueness of predicates.

### Zero ###
Dgraph consists of Zero and [Alpha](#alpha) nodes. Zero nodes control the Dgraph database cluster. It assigns Alpha nodes to groups, re-balances data between groups, handles transaction timestamp and UID assignment.
:::
