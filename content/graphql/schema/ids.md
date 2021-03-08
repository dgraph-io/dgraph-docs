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

In a single page app, you'll want to render the page for `http://.../posts/0x123` when a user clicks to view the post with id `0x123`.  You app can then use a `getPost(id: "0x123") { ... }` GraphQL query to fetch the data to generate the page.

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

Identities created with `@id` are reusable - if you delete an existing user, you can reuse the username. But like `ID` types, fields declared with `@id` are also immutable.

Fields with the `@id` directive must have the type `String!`.

As with `ID` types, Dgraph generates queries and mutations so you can query, update and delete data in nodes, using the fields with the `@id` directive as references.

It's possible to use the `@id` directive on more than one field in a type. For example, you can define a type like the following:

```graphql
type Book {
    name: String! @id
    isbn: String! @id
    genre: String!
    ...
}
```

 You can then perform queries with filters containing multiple `@id` fields; the fields you specify will execute in the manner of an `and` operation. For example, for the above schema, you can send a `getBook` query like the following:

```graphql
query {
  getBook(name: "The Metamorphosis", isbn: "9871165072") {
    name
    genre
    ...
  }
}
```

This will yield a positive response if both the `name` **and** `isbn` match any data in the database.

{{% notice "note" %}}
If there are multiple fields with `@id`’s  in a type then all of them will be nullable. If a type has a single field defined with either `@id` or `ID` then that will be non-nullable. 
{{% /notice %}}


### More to come

We are currently considering allowing types other than `String` with `@id`; see [here](https://discuss.dgraph.io/t/id-with-type-int/10402) for more information.