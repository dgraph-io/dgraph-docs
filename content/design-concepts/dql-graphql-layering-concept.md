
TODO: add query layering in addition to schema layering

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