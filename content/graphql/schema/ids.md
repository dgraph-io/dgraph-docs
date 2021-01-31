+++
title = "IDs"
description = "There are two types of identity built into Dgraph. Those are accessed using the ID scalar type and the @id directive."
weight = 3
[menu.main]
    parent = "schema"
+++

There are two types of identity built into Dgraph. Those are accessed using the `ID` scalar type and the `@id` directive.

### The ID type

In Dgraph, every node has a unique 64-bit identifier that you can expose in GraphQL using the `ID` type. `ID`s are auto-generated, immutable and never reused. Each type can have at most one `ID` field.

The `ID` type works great for things that you'll want to refer to via an id, but don't need to set the identifier externally.  Examples are things like posts, comments, tweets, etc. 

For example, you might set the following type in a schema.

```graphql
type Post {
    id: ID!
    ...
}
```

In a single page app, you'll want to render the page for `http://.../posts/0x123` when a user clicks to view the post with id `0x123`.  Your app can then use a `getPost(id: "0x123") { ... }` GraphQL query to fetch the data to generate the page.

For input and output, `ID`s are treated as strings.

You'll also be able to update and delete posts by id.

### The @id directive

For some types, you'll need a unique identifier set from outside Dgraph.  A common example is a username.

The `@id` directive tells Dgraph to keep values of that field unique and to use them as identifiers.

For example, you might set the following type in a schema.

```graphql
type User {
    username: String! @id
    ...
}
```

Dgraph will then require a unique username when creating a new user --- it'll generate the input type for `addUser` with `username: String!` so you can't make an add mutation without setting a username, and when processing the mutation, Dgraph will ensure that the username isn't already set for another node of the `User` type.

Identities created with `@id` are reusable - if you delete an existing user, you can reuse the username.

Fields with the `@id` directive must have the type `String!`.

As with `ID` types, Dgraph will generate queries and mutations so you'll also be able to query, update and delete by the field with the @id directive.

In a single page app, you'll want to render the page for `http://.../user/foobar` when a user clicks to view author bio page for user `foobar`.  Your app can then use a `getUser(username: "foobar") { ... }` GraphQL query to fetch the data to generate the page.

### Combining ID and @id directive

You may use both the ID scalar and the @id directive on another field definition to have both a unique identifier and a generated id.

For example, you might set the following type in a schema.

```graphql
type User {
    id: ID!
    username: String! @id
    ...
}
```

Dgraph will still require a unique username when creating a new user. This schema provides the benefits of both of the previous examples above. Your app can then use the `getUser(...) { ... }` query providing either the id or the username.

When your app needs to reference a specific `User` for reference by edge in another mutation, it may then use either the `id` or the `username` field.

### More to come

We are currently considering allowing types other than `String` with `@id`, see [here](https://discuss.dgraph.io/t/id-with-type-int/10402)

We are currently considering expanding uniqueness to include composite ids and multiple unique fields (e.g. [this](https://discuss.dgraph.io/t/support-multiple-unique-fields-in-dgraph-graphql/8512) issue).
