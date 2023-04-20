+++
date = "2017-03-20T22:25:17+11:00"
title = "Query Dgraph types"
weight = 14
[menu.main]
    parent = "howto"
+++


The list of predicates and node types is retrieved using a query on the `/query` endpoint. 

```
schema {}
```

{{% notice "note" %}} Unlike regular queries, the schema query is not surrounded
by curly braces. Also, schema queries and regular queries cannot be combined.
{{% /notice %}}

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

{{% notice "note" %}} If ACL is enabled, then the schema query returns only the
predicates for which the logged-in ACL user has read access. {{% /notice %}}

Types can also be queried. Below are some example queries.

```
schema(type: Movie) {}
schema(type: [Person, Animal]) {}
```

Note that type queries do not contain anything between the curly braces. The
output will be the entire definition of the requested types.
