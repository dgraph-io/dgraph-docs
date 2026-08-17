---
title: "GraphQL data migration"

---



When deploying a new version of your GraphQL Schema, Dgraph will update the underlying DQL Schema but will not alter the data.

As explained in [GraphQL and DQL Schemas](/graphql/graphql-dql/graphql-dql-schema) overview, Dgraph has no constraints at the database level and any node with predicates is valid. 

You may face with several data GraphQL API and data discrepancies.

### unused fields
For example, let's assume that you have deployed the following schema:
```graphql
type TestDataMigration {
  id: ID!
  someInfo: String!
  someOtherInfo: String
}
```

Then you create a `TestDataMigration`  with `someOtherInfo` value.

Then you update the Schema and remove the field.
```graphql
type TestDataMigration {
  id: ID!
  someInfo: String!
}
```

The data you have previously created is still in the graph database !

Moreover if you delete the `TestDataMigration` object using its `id`, the GraphQL API delete operation will be successful.

If you followed the [GraphQL - DQL Schema mapping](/graphql/graphql-dql/graphql-dql-schema), you understand that Dgraph has used the list the known list of predicates (id, someInfo) and removed them. In fact, Dgraph also removed the `dgraph.type` predicate and so this `TestDataMigration` node is not visible anymore to the GraphQL API.

The point is that a node with this `uid` exists and has a predicate `someOtherInfo`. This is because this data has been created initially and nothing in the process of deploying a new version and then using a delete operation by ID instructed Dgraph to delete this predicate.

You end up with a node without type (i.e without a `dgraph.type` predicate) and with an old predicate value which is 'invisible' to your GraphQL API!

When doing a GraphQL schema deployement, you must take care of the data cleaning and data migration.
The good news is that DQL offers you the tools to identify (search) potential issues and to correct the data (mutations).

In the previous case, you can alter the database and completely delete the predicate or you can write an 'upsert' DQL query that will search the nodes of interest and delete the unused predicate for those nodes.

### new non-nullable field
Another obvious example appears if you deploy a new version containing a new non-nullable field for an existing type. The existing 'nodes' of the same type in the graph do not have this predicate. A Gra[hQL query reaching those nodes will return a list of errors. You can easily write an 'upsert' DQL mutation to find all node of this type not having the new predicate and update them with a default value.

