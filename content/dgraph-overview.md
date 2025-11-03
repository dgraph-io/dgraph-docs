+++
title = "Overview"
type = "docs"
description = "Introduction to Dgraph Database. Dgraph is a horizontally scalable and distributed graph database that supports GraphQL natively. You can run Dgraph on-premise, in your cloud infrastructure, or as a service fully-managed by Dgraph."
aliases = ["/about"]
[menu.main]
    name = "Overview"
    identifier = "overview"
    weight = 2
+++

Dgraph is a distributed graph database designed for modern applications that need to work with highly connected data. It provides a scalable foundation for storing and querying complex relationships between entities.

## Understanding the Graph Model

At its core, Dgraph stores data as a graph composed of **nodes** and **relationships**. Nodes represent entities in your data (like users, products, or locations), while relationships connect these nodes to show how they relate to each other (like "follows", "purchased", or "located_in").

Each node is identified by a unique identifier (UID) and can have multiple **attributes** that describe its properties. For example, a person node might have attributes like name, age, and email. Attributes can store various data types including strings, integers, floats, dates, and geographic coordinates.

## Data Formats

Dgraph is flexible in how you provide data to it. You can save data in two formats:

**RDF (Resource Description Format)** uses a triple-based structure with subject-predicate-object statements:
```
<0x1> <name> "Alice" .
<0x1> <age> "30" .
<0x1> <friend> <0x2> .
```

**JSON** provides a more familiar structure for developers:
```json
{
  "uid": "0x1",
  "name": "Alice",
  "age": 30,
  "friend": {
    "uid": "0x2"
  }
}
```

Both formats are stored internally as graph structures, allowing you to choose the format that best fits your workflow.

## Schema and Types

While Dgraph can operate in a schema-less manner (you can add any predicate to any node at any time), defining a schema provides important benefits. The schema tells Dgraph about your predicates—their data types and which indexes to use.
Indexes are required to use certain query functions.

## Distributed Architecture

Dgraph is built from the ground up as a distributed system. Data is automatically sharded across multiple nodes in a cluster, allowing you to scale horizontally as your graph grows. The distributed architecture enables Dgraph to handle graphs with billions of nodes and triples while maintaining low-latency query performance.

Each Dgraph cluster consists of multiple server groups (shards) that work together to store and query your data. Queries are automatically distributed across the relevant shards and results are aggregated, making the distributed nature transparent to your application. This architecture provides both horizontal scalability and high availability.

For detailed information about Dgraph's distributed architecture, clustering, and replication, see the [Architecture documentation]({{< relref "dgraph-architecture">}}).

## Enterprise-Grade Features

Dgraph includes production-ready features for running mission-critical applications:

**High Availability**: Configure multiple replicas within each server group to ensure your database remains available even when individual nodes fail. Automatic failover maintains service continuity without manual intervention.

**Backup and Restore**: Create full and incremental backups of your graph data. Backups can be stored locally or in cloud storage, and point-in-time recovery allows you to restore your database to any previous state.

**Monitoring and Observability**: Built-in metrics and integration with monitoring tools like Prometheus and Grafana provide visibility into cluster health, query performance, and resource utilization.

**Access Control**: Fine-grained access control lists (ACLs) allow you to manage user permissions at the predicate level, ensuring data security in multi-tenant environments.

**Encryption**: Support for encryption at rest and in transit protects your data throughout its lifecycle.

These features make Dgraph suitable for production deployments requiring reliability, security, and operational excellence.

## Querying Dgraph Query Language (DQL)

Dgraph uses **DQL**, a query language inspired by GraphQL but extended with graph-specific capabilities. Queries in Dgraph allow you to traverse the graph, following relationships from node to node to retrieve connected data in a single request.

A typical query starts at one or more nodes and traverses relationships to gather related information:
```graphql
{
  person(func: eq(name, "Alice")) {
    name
    age
    friend {
      name
      friend {
        name
      }
    }
  }
}
```

This traverses from Alice to her friends, and then to her friends' friends, returning the nested structure in one query.

## Graph Traversals and Filtering

Dgraph excels at traversing complex relationships. You can filter at any level of traversal, aggregate data, sort results, and paginate through large result sets. The query language supports recursive queries for exploring paths of variable length, filtering by regular expressions, geographic proximity, and full-text search.

Variables and value aggregation allow you to build sophisticated queries that analyze patterns across your graph, such as finding the most connected nodes or calculating metrics across relationships.

## Mutations

Data modifications in Dgraph are called **mutations**. You can add new nodes, update existing attributes, create or remove relationships, and delete nodes. Mutations can be submitted in either RDF or JSON format, and multiple operations can be batched together in a single transaction for consistency.

## Transactions and Consistency

Dgraph provides ACID transactions, ensuring that your data remains consistent even under concurrent access. Transactions can span multiple queries and mutations, and Dgraph handles conflicts automatically to maintain data integrity across your distributed cluster.

## Getting Started

Working with Dgraph typically involves:
1. Defining your schema (optional but recommended)
2. Loading your data through mutations
3. Querying the graph to retrieve and analyze connected information
4. Iterating on your schema and queries as your application evolves

The graph model naturally represents connected data, making it straightforward to model domains like social networks, recommendation systems, knowledge graphs, access control systems, and any application where relationships between entities matter as much as the entities themselves.


## What's Next

- Get familiar with some terms in our [Glossary](/dgraph-glossary)
- Go through some [tutorials]({{<relref "learn">}})










