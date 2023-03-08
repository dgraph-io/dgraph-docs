+++
title = "RBAC rules"
description = "Dgraph support Role Based Access Control (RBAC) on GraphQL API operations."
weight = 4
[menu.main]
    parent = "gql-auth"
+++

Dgraph support Role Based Access Control (RBAC) on GraphQL API operations: you can specify who can invoke query, add, update and delete operations on each type of your GraphQL schema based on JWT claims, using the ``@auth`` directive.


To implement Role Based Access Control on GraphQL API operations  :
1. Ensure your have configured the GraphQL schema to [Handle JWT tokens]({{< relref "jwt.md">}}) using ``# Dgraph.Authorization``   
  This step is important to be able to use the [JWT claims]({{< relref "graphql/security/_index.md#jwt-claims" >}})
2. Annotate the Types in the GraphQL schema with the `@auth` directive and specify conditions to be met for `query`, `add`, `update` or `delete` operations.
3. Deploy the GraphQL schema either with a [schema update]({{< relref "graphql/admin.md#using-updategqlschema-to-add-or-modify-a-schema" >}}) or via the Cloud console's [Schema](https://cloud.dgraph.io/_/schema) page.



The generic format of RBAC rule is as follow
```graphql
type User @auth(
    query: { rule:  "{$<claim>: { eq: \"<value>\" } }" },
    add: { rule:  "{$<claim>: { in: [\"<value1>\",...] } }" },
    update: ...
    delete: ...
)
```

Where `<claim>` is a [JWT claim]({{< relref "graphql/security/_index.md#jwt-claims" >}}) from the JWT token payload.

You can use ``eq`` or ``in`` function to test the value of any claim.


For example the following schema has a @auth directive specifying that a delete operation on a User object can only be done in the connected user has a 'ROLE' claim in the JWT token with the value "ADMIN" :
```graphql
type User @auth( 
     delete: { rule: "{$ROLE: { eq: \"ADMIN\" } }"} 
    ) { 
    username: String! 
    @id todos: [Todo] 
}
```

## rules combination

Rules can be combined with the logical connectives ``and``, ``or`` and ``not``.
A permission can be a mixture of graph traversals and role based rules.

In the todo app, you can express, for example, that you can delete a `Todo` if you are the author, or are the site admin.

```graphql
type Todo @auth(
    delete: { or: [ 
        { rule:  "query ($USER: String!) { ... }" }, # you are the author graph query
        { rule:  "{$ROLE: { eq: \"ADMIN\" } }" }
    ]}
)
```


## claims

Rules may use claims from the namespace specified by the [# Dgraph.Authorization]({{< relref "jwt.md">}}) or claims present at the root level of the JWT payload.

For example, given the following JWT payload

```json
{
   "https://xyz.io/jwt/claims": [
      "ROLE": "ADMIN"
   ],
  "USERROLE": "user1",
  "email": "random@example.com"
}
```

The authorization rules can use ``$ROLE`` (if `https://xyz.io/jwt/claims` is declared as the namespace to use ) and also ``$USEROLE`` or ``$email``.

In cases where the same claim is present in the namespace and at the root level, the claim value in the namespacetakes precedence.

## `@auth` on Interfaces

The rules provided inside the `@auth` directive on an interface will be applied as an `AND` rule to those on the implementing types.

A type inherits the `@auth` rules of all the implemented interfaces. The final authorization rule is an `AND` of the type's `@auth` rule and of all the implemented interfaces.



