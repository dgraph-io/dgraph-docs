+++
date = "2017-03-20T22:25:17+11:00"
title = "Query Dgraph types"
type = "docs"
weight = 14
[menu.main]
    parent = "howto"
+++


You can retrieve the Dgraph schema containing the list of predicates types and node types by:
- issuing a query on /query endpoint using the [HTTP Client]({{< relref "raw-http#query-current-dql-schema">}})
- issuing a query using any [DQL client library]({{< relref "dql/clients">}})
- using [Ratel UI]({{< relref "ratel/schema">}})
- using the Cloud console through the [DQL Schema](https://cloud.dgraph.io/_/schema?tab=dqlschema) tab of the Schema section.


When using a query, the request body is 
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
