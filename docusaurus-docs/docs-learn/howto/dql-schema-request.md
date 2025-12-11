---
title: Query Dgraph types
---


You can retrieve the Dgraph schema containing the list of predicates types and node types by:
- issuing a query on /query endpoint using the [HTTP Client](/clients/raw-http#query-current-dql-schema)
- issuing a query using any [DQL client library](/clients)
- using [Ratel UI](/ratel/schema)
- using the Cloud console through the [DQL Schema](https://cloud.dgraph.io/_/schema?tab=dqlschema) tab of the Schema section.


When using a query, the request body is 
```
schema {}
```

:::note Unlike regular queries, the schema query is not surrounded
by curly braces. Also, schema queries and regular queries cannot be combined.
:::

You can query for particular schema fields in the query body.

```
schema {
  type
  index
  reverse
  tokenizer
  list
  count
  upsert
  lang
}
```

You can also query for particular predicates:

```
schema(pred: [name, friend]) {
  type
  index
  reverse
  tokenizer
  list
  count
  upsert
  lang
}
```

:::note If ACL is enabled, then the schema query returns only the
predicates for which the logged-in ACL user has read access. :::

Types can also be queried. Below are some example queries.

```
schema(type: Movie) {}
schema(type: [Person, Animal]) {}
```

Note that type queries do not contain anything between the curly braces. The
output will be the entire definition of the requested types.
