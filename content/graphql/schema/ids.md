+++
title = "IDs in GraphQL"
description = "Dgraph database provides two types of identifiers: the ID scalar type and the @id directive."
weight = 3
[menu.main]
    name = "IDs"
    parent = "schema"
+++

Dgraph provides two types of built-in identifiers: the `ID` scalar type and the `@id` directive.

* The `ID` scalar type is used when you don't need to set an identifier outside of Dgraph.
* The `@id` directive is used for external identifiers, such as email addresses.

## The `ID` type

In Dgraph, every node has a unique 64-bit identifier that you can expose in GraphQL using the `ID` type. An `ID` is auto-generated, immutable and never reused. Each type can have at most one `ID` field.

The `ID` type works great when you need to use an identifier on nodes and don't need to set that identifier externally (for example, posts and comments).

For example, you might set the following type in a schema:

```graphql
type Post {
    id: ID!
    ...
}
```

In a single-page app, you could generate the page for `http://.../posts/0x123` when a user clicks to view the post with `ID` 0x123. Your app can then use a `getPost(id: "0x123") { ... }` GraphQL query to fetch the data used to generate the page.

For input and output, `ID`s are treated as strings.

You can also update and delete posts by `ID`.

## The `@id` directive

For some types, you'll need a unique identifier set from outside Dgraph.  A common example is a username.

The `@id` directive tells Dgraph to keep that field's values unique and use them as identifiers.

For example, you might set the following type in a schema:

```graphql
type User {
    username: String! @id
    ...
}
```

Dgraph requires a unique username when creating a new user. It generates the input type for `addUser` with `username: String!`, so you can't make an add mutation without setting a username; and when processing the mutation, Dgraph will ensure that the username isn't already set for another node of the `User` type.

In a single-page app, you could render the page for `http://.../user/Erik` when a user clicks to view the author bio page for that user. Your app can then use a `getUser(username: "Erik") { ... }` GraphQL query to fetch the data and generate the page.

Identities created with `@id` are reusable. If you delete an existing user, you can reuse the username.

Fields with the `@id` directive must have the type `String!`.

As with `ID` types, Dgraph generates queries and mutations so you can query, update, and delete data in nodes, using the fields with the `@id` directive as references.

It's possible to use the `@id` directive on more than one field in a type. For example, you can define a type like the following:

```graphql
type Book {
    name: String! @id
    isbn: String! @id
    genre: String!
    ...
}
```

You can then use multiple `@id` fields in arguments to `get` queries, and while searching, these fields will be combined with the `AND` operator, resulting in a Boolean `AND` operation. For example, for the above schema, you can send a `getBook` query like the following:

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

### `@id` and interfaces

By default, if used in an interface, the `@id` directive will ensure field uniqueness for each implementing type separately.
In this case, the `@id` field in the interface won't be unique for the interface but for each of its implementing types.
This allows two different types implementing the same interface to have the same value for the inherited `@id` field. 

There are scenarios where this behavior might not be desired, and you may want to constrain the `@id` field to be unique across all the implementing types. In that case, you can set the `interface` argument of the `@id` directive to `true`, and Dgraph will ensure that the field has unique values across all the implementing types of an interface.

For example:

```graphql
interface Item {
  refID: Int! @id(interface: true) # if there is a Book with refID = 1, then there can't be a chair with that refID.
  itemID: Int! @id # If there is a Book with itemID = 1, there can still be a Chair with the same itemID.
}

type Book implements Item { ... }
type Chair implements Item { ... }
```

In the above example, `itemID` won't be present as an argument to the `getItem` query as it might return more than one `Item`.

{{% notice "note" %}}
`get` queries generated for an interface will have only the `@id(interface: true)` fields as arguments.
{{% /notice %}}

## Combining `ID` and `@id`

You can use both the `ID` type and the `@id` directive on another field definition to have both a unique identifier and a generated identifier.

For example, you might define the following type in a schema:

```graphql
type User {
    id: ID!
    username: String! @id
    ...
}
```

With this schema, Dgraph requires a unique `username` when creating a new user. This schema provides the benefits of both of the previous examples above. Your app can then use the `getUser(...) { ... }` query to provide either the Dgraph-generated `id` or the externally-generated `username`.

{{% notice "note" %}}
If in a type there are multiple `@id` fields, then in a `get` query these arguments will be optional. If in a type there's only one field defined with either `@id` or `ID`, then that will be a required field in the `get` query's arguments.
{{% /notice %}}

<!--
### More to come

We are currently considering allowing types other than `String` with `@id`, see [here](https://discuss.dgraph.io/t/id-with-type-int/10402)

We are currently considering expanding uniqueness to include composite ids and multiple unique fields (e.g. [this](https://discuss.dgraph.io/t/support-multiple-unique-fields-in-dgraph-graphql/8512) issue).
-->
