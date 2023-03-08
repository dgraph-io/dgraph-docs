+++
title = "ABAC rules"
description = "Dgraph support Attribute Based Access Control (ABAC) on GraphQL API operations: you can specify which data a user can query, add, update or delete for each type of your GraphQL schema based on JWT claims, using the ``@auth`` directive and graph traversal queries."
weight = 5
[menu.main]
    parent = "gql-auth"
+++

Dgraph support Attribute Based Access Control (ABAC) on GraphQL API operations: you can specify which data a user can query, add, update or delete for each type of your GraphQL schema based on JWT claims, using the ``@auth`` directive and graph traversal queries.


To implement graph traversal rule on GraphQL API operations  :
1. Ensure your have configured the GraphQL schema to [Handle JWT tokens]({{< relref "jwt.md">}}) using ``# Dgraph.Authorization``   
  This step is important to be able to use the [JWT claims]({{< relref "graphql/security/_index.md#jwt-claims" >}})
2. Annotate the Types in the GraphQL schema with the `@auth` directive and specify conditions to be met for `query`, `add`, `update` or `delete` operations.
3. Deploy the GraphQL schema either with a [schema update]({{< relref "graphql/admin.md#using-updategqlschema-to-add-or-modify-a-schema" >}}) or via the Cloud console's [Schema](https://cloud.dgraph.io/_/schema) page.


A graph traversal rule is expressed as GraphQL query on the type on which the @auth directive applies.

For example, a rule on ``Contact`` type can only use a ``queryContact`` query :

```graphql
type Contact @auth(
  query: { rule: "query { queryContact(filter: { isPublic: true }) { id } }" },
  add: ...
  update: ...
  delete: ...
) {
  <type definition>
  ...
}
```

You can use triple quotation marks. In that case the query can be defined on multiple lines.

The following schema is also valid:
```graphql
type Contact @auth(
  query: { rule: """query { 
    queryContact(filter: { isPublic: true }) { 
        id 
    } 
    } """ 
}) {
  <type definition>
  ...
}
```

The rules are expressed as GraphQL queries, so they can also have a name and parameters:
```graphql
type Todo @auth(
    query: { rule: """
        query ($USER: String!) { 
            queryTodo(filter: { owner: { eq: $USER } } ) { 
                id 
            } 
        }"""
    }
){
    id: ID!
    text: String! @search(by: [term])
    owner: String! @search(by: [hash])
}
```

The parameters are replaced at runtime by the corresponding ``claims`` found in the JWT token. In the previous case, the query will be executed with the value of the `USER` claim.

When a user sends a request on `/graphql` endpoint for a `get<Type>` or `query<Type>` operation, Dgraph executes the query specified in the @auth directive of the `Type` to build a list of "authorized" UIDs. Dgraph returns only the data matching both the requested data and the "authorized" list. That means that the client can apply any filter condition, the result will be the intersection of the data matching the filter and the "authorized" data.  

The same logic applies for update<Type> and delete<Type>: only the data matching the @auth query are affected.
```graphql
type Todo @auth(
    delete: { or: [ 
        { rule:  """query ($USER: String!) { 
            queryTodo(filter: { owner: { eq: $USER } } ) { 
                __typename 
            } 
          } """ 
        }, # you are the author graph query
        { rule:  "{$ROLE: { eq: \"ADMIN\" } }" }
    ]}
)
```

In the context of @auth directive, Dgraph executes the @auth query differently that a normal query : if the query has nested blocks, all levels must match existing data. Dgraph internally applies a `@cascade` directive, making the directive more like a **pattern matching** condition. 

For example, in the cases of `Todo`, the access will depend not on a value in the todo, but on checking which owner it's linked to.
This means our auth rule must make a step further into the graph to check who the owner is :

```graphql
type User {
	username: String! @id
	todos: [Todo]
}

type Todo @auth(
    query: { rule: """
        query ($USER: String!) {
            queryTodo {
                owner(filter: { username: { eq: $USER } } ) {
                    __typename
                }
            }
        }"""
    }
){
	id: ID!
	text: String!
	owner: User
}
```

The @auth query rule will only return ``Todos`` having an owner matching the condition: the owner ``username`` must be equal the the JWT claim ``USER``.

All blocks must return some data for the query to succeed. You may want to use the field `__typename` in the most inner block to ensure a data match at this level.


### rules combination

Rules can be combined with the logical connectives ``and``, ``or`` and ``not``.
A permission can be a mixture of graph traversals and role based rules.

### `@auth` on Interfaces

The rules provided inside the `@auth` directive on an interface will be applied as an `AND` rule to those on the implementing types.

A type inherits the `@auth` rules of all the implemented interfaces. The final authorization rule is an `AND` of the type's `@auth` rule and of all the implemented interfaces.

### claims

Rules may use claims from the namespace specified by the [# Dgraph.Authorization]({{< relref "jwt.md">}}) or claims present at the root level of the JWT payload.

### error handling

When deploying the schema, Dgraph tests if you are using valid queries in your @auth directive.

For example, using ``queryFilm`` for a rule on a type ``Actor`` will lead to an error:
```
resolving updateGQLSchema failed because Type Actor: @auth: expected only queryActor rules,but found queryFilm
```