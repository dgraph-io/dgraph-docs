+++
title = "Authorization tips"
description = "Given an authentication mechanism and a signed JSON Web Token (JWT), the @auth directive tells Dgraph how to apply authorization."
weight = 7
[menu.main]
    parent = "gql-auth"
+++

## Public Data

Many apps have data that can be accessed by anyone, logged in or not.  That also works nicely with Dgraph auth rules.  

For example, in Twitter, StackOverflow, etc. you can see authors and posts without being signed it - but you'd need to be signed in to add a post.  With Dgraph auth rules, if a type doesn't have, for example, a `query` auth rule or the auth rule doesn't depend on a JWT value, then the data can be accessed without a signed JWT.

For example, the todo app might allow anyone, logged in or not, to view any author, but not make any mutations unless logged in as the author or an admin.  That would be achieved by rules like the following.

```graphql
type User @auth(
    # no query rule
    add: { rule:  "{$ROLE: { eq: \"ADMIN\" } }" },
    update: ...
    delete: ...
) {
    username: String! @id
    todos: [Todo]
}
```

Maybe some todos can be marked as public and users you aren't logged in can see those.

```graphql
type Todo @auth(
    query: { or: [
        # you are the author 
        { rule: ... },
        # or, the todo is marked as public
        { rule: """query { 
            queryTodo(filter: { isPublic: { eq: true } } ) { 
                id 
            } 
        }"""}
    ]}
) { 
    ...
    isPublic: Boolean
}

```

Because the rule doesn't depend on a JWT value, it can be successfully evaluated for users who aren't logged in.

Ensuring that requests are from an authenticated JWT, and no further restrictions, can be done by arranging the JWT to contain a value like `"isAuthenticated": "true"`.  For example,


```graphql
type User @auth(
    query: { rule:  "{$isAuthenticated: { eq: \"true\" } }" },
) {
    username: String! @id
    todos: [Todo]
}
```

specifies that only authenticated users can query other users.

### blocking an operation of everyone

If the `ROLE` claim isn't present in a JWT, any rule that relies on `ROLE` simply evaluates to false.

You can also simply disallow some queries and mutations by using a condition on a non-existing claim:

If you know that your JWTs never contain the claim `DENIED`, then a rule such as

```graphql
type User @auth(
    delete: { rule:  "{$DENIED: { eq: \"DENIED\" } }"}
) { 
    ...
}
```
will block the delete operation for everyone.