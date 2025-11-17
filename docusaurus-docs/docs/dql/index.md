---
title: Query Language
description: Dgraph Query Language (DQL) is Dgraph's proprietary language to add, modify, delete and fetch data.
---

Dgraph Query Language (DQL) is Dgraph's proprietary language to add, modify, delete and fetch data. It provides a powerful and expressive way to work with graph data, allowing you to traverse relationships, filter nodes, and retrieve complex graph structures.

## Essential Concepts

### Nodes, Predicates, and Facets
Before diving into DQL, it's important to understand how Dgraph structures data:

**Nodes** represent entities or "things" in your domain—like a person, a movie, or a company. Each node has a unique identifier ([UID](../dgraph-glossary#uid)) that Dgraph assigns.

**Predicates** are the smallest unit of information in Dgraph. They describe facts about nodes and come in two forms:
- **Attributes**: Store literal values (strings, numbers, dates) directly on a node. For example, a `name` predicate with value "Alice" is an attribute.
- **Relationships**: Connect one node to another node. For example, a `knows` predicate linking Alice's node to Bob's node is a relationship.

Dgraph stores data as facts using predicates. Each fact follows the pattern: `<node> <predicate> <value>`, where the value can be either a literal (for attributes) or another node's UID (for relationships).

**Facets** are metadata that can be attached to any predicate—both attributes and relationships. They provide additional context about the predicate itself, such as when a relationship was established, the confidence level of an attribute, or any other property about the fact. Learn more about [facets](../design-concepts/facets-concept).


### Transactions

Dgraph supports transactions to ensure data consistency and atomicity. A transaction groups multiple operations (queries and mutations) into a single atomic unit.

#### Transaction Lifecycle

1. **Start a transaction**: When you execute a query or mutation, Dgraph automatically starts a new transaction and assigns it a unique transaction ID (also called `start_ts` or start timestamp).

2. **Execute operations**: Within a transaction, you can perform multiple queries and mutations. All operations in the same transaction use the same transaction ID to ensure they see a consistent view of the data.

3. **Commit or rollback**: 
   - **Commit**: Makes all changes in the transaction permanent. After committing, the changes are visible to other transactions.
   - **Rollback (abort)**: Discards all changes in the transaction. The database returns to its state before the transaction started.

#### Transaction Contents

A transaction can contain:
- **Queries**: Read data from the database
- **Mutations**: Add, modify, or delete data

You can perform multiple queries and mutations within a single transaction before committing. This allows you to read data, make decisions based on that data, and then apply mutations—all while maintaining consistency.

#### Read-Only Transactions

**Read-only** transactions are optimized for read operations and cannot contain mutations. They are useful to increase read speed because they can circumvent the usual consensus protocol. Attempting to perform a mutation in a read-only transaction will result in an error.

Read-only queries can optionally be set as **best-effort**. Using this flag asks the Dgraph Alpha to try to get timestamps from memory on a best-effort basis to reduce the number of outbound requests to Zero. This may yield improved latencies in read-bound workloads where linearizable reads are not strictly needed.

For more details, see [Transactions](../design-concepts/transactions-concept)..



