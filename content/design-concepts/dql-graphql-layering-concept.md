+++
date = "2017-03-27:12:00:00Z"
title = "DQL and GraphQL (concept)"
weight = 50
[menu.main]
    parent = "design-concepts"
+++

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

## Dgraph Queries, Mutations and Upserts
Similarly, GraphQL mutations are implemented on top of DQL in the sense that a GraphQL query is converted internally into a DQL query, which is then executed. This translation is not particularly complex, since DQL is based on GraphQL, with some syntax changes and some extensions. 

This is generally transaparent to all callers, however users should be aware that
1) Anything done in GraphQL can also be done in DQL if needed. Some small exceptions include the enforcement of non-null constraints and other checks done before Dgraph transpiles GraphQL to DQL and executes it.
2) Some logging including Request Logging and OpenTrace (Jaeger) tracing may show DQL converted from the GraphQL.
