---
title: Query Language
description: Dgraph Query Language (DQL) is Dgraph's proprietary language to add, modify, delete and fetch data.
---

Dgraph Query Language (DQL) is Dgraph's proprietary language to add, modify, delete and fetch data. It provides a powerful and expressive way to work with graph data, allowing you to traverse relationships, filter nodes, and retrieve complex graph structures.

## Essential Concepts

Before diving into DQL, it's important to understand how Dgraph structures data:

**Nodes** represent entities or "things" in your domain—like a person, a movie, or a company. Each node has a unique identifier ([UID](/dgraph-glossary#uid)) that Dgraph assigns.

**Predicates** are the smallest unit of information in Dgraph. They describe facts about nodes and come in two forms:
- **Attributes**: Store literal values (strings, numbers, dates) directly on a node. For example, a `name` predicate with value "Alice" is an attribute.
- **Relationships**: Connect one node to another node. For example, a `knows` predicate linking Alice's node to Bob's node is a relationship.

Dgraph stores data as facts using predicates. Each fact follows the pattern: `<node> <predicate> <value>`, where the value can be either a literal (for attributes) or another node's UID (for relationships).

**Facets** are metadata that can be attached to any predicate—both attributes and relationships. They provide additional context about the predicate itself, such as when a relationship was established, the confidence level of an attribute, or any other property about the fact. Learn more about [facets](/design-concepts/facets-concept).

For detailed definitions, see the [Dgraph Glossary](/dgraph-glossary) and [design concepts](/design-concepts/relationships-concept).

---



