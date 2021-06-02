+++
title = "And, Or and Not"
description = "Every GraphQL search filter can use AND, OR and NOT operators."
weight = 5
[menu.main]
    parent = "graphql-queries"
    name = "And, Or and Not"
+++

Every GraphQL search filter can use `and`, `or` and `not` operators.

GraphQL syntax uses infix notation, so: "a and b" is `a, and: { b }`, "a or b or c" is `a, or: { b, or: c }`, and "not" is a prefix (`not:`).

Example: Posts that do not have "GraphQL" in the title.

```graphql
queryPost(filter: { not: { title: { allofterms: "GraphQL"} } } ) { ... }
```

Example: Posts that have "GraphQL" or "Dgraph" in the title.

```graphql
queryPost(filter: {
  title: { allofterms: "GraphQL"},
  or: { title: { allofterms: "Dgraph" } }
} ) { ... }
```

Example: Posts that have "GraphQL" and "Dgraph" in the title.

```graphql
queryPost(filter: {
  title: { allofterms: "GraphQL"},
  and: { title: { allofterms: "Dgraph" } }
} ) { ... }
```

The "and" operator is implicit for a single filter object, if the fields don't overlap.  For example, above the `and` is required because `title` is in both filters, whereas below, `and` is not required.

```graphql
queryPost(filter: {
  title: { allofterms: "GraphQL" },
  datePublished: { ge: "2020-06-15" }
} ) { ... }
```

Example: Posts that have "GraphQL" in the title, or have the tag "GraphQL" and mention "Dgraph" in the title

```graphql
queryPost(filter: {
  title: { allofterms: "GraphQL"},
  or: { title: { allofterms: "Dgraph" }, tags: { eq: "GraphQL" } }
} ) { ... }
```

The `and` and `or` filter both accept a list of filters. Per the GraphQL specification, non-list filters are coerced into a list. This provides backwards compatibility while allowing for more complex filters.

Example: Query for posts that have `GraphQL` in the title but that lack the `GraphQL` tag, or that have `Dgraph` in the title but lack the `Dgraph` tag.

```graphql
queryPost(filter: {
  or: [
    { and: [{ title: { allofterms: "GraphQL" } }, { not: { tags: { eq: "GraphQL" } } }] }
    { and: [{ title: { allofterms: "Dgraph" } }, { not: { tags: { eq: "Dgraph" } } }] }
  ]
} ) { ... }
```

{{% notice "note" %}}
Nested logic with the same `and`/`or` conjunction can be simplified into a single list.
```
queryPost(filter: {
  or: [
    { or: [ { foo: { eq: "A" } }, { bar: { eq: "B" } } ] },
    { or: [ { baz: { eq: "C" } }, { quz: { eq: "D" } } ] }
  ]
} ) { ... }
```
Can be simplified into
```
queryPost(filter: {
  or: [
    { foo: { eq: "A" } }, 
    { bar: { eq: "B" } },
    { baz: { eq: "C" } }, 
    { quz: { eq: "D" } }
  ]
} ) { ... }
```
{{% /notice %}}
