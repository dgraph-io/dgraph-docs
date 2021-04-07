+++
title = "Schema Migration"
description = "This document describes all the things that you need to take care while doing a schema update or migration."
weight = 1
[menu.main]
    parent = "schema"
    identifier = "schema-migration"
+++

In every app's development lifecycle, there's a point where the underlying schema doesn't fit the requirements and must be changed for good.
That requires a migration for both schema and the underlying data.
This article will guide you through common migration scenarios you can encounter with Dgraph and help you avoid any pitfalls around them.

These are the most common scenarios that can occur:
* Renaming a type
* Renaming a field
* Changing a field's type
* Adding `@id` to an existing field

{{% notice "note" %}}
As long as you can avoid migration, avoid it. 
Because there can be scenarios where you might need to update downstream clients, which can be hard.
So, its always best to try out things first, once you are confident enough, then only push them to 
production.
{{% /notice %}}

### Renaming a type

Let's say you had the following schema:

```graphql
type User {
    id: ID!
    name: String
}
```

and you had your application working fine with it. Now, you feel that the name `AppUser` would be
more sensible than the name `User` because `User` seems a bit generic to you. Then you are in a 
situation where you need migration.

This can be handled in a couple of ways:
1. Migrate all the data for type `User` to use the new name `AppUser`. OR,
2. Just use the [`@dgraph(type: ...)`](/graphql/dgraph) directive to maintain backward compatibility 
   with the existing data.

Depending on your use-case, you might find option 1 or 2 better for you. For example, if you 
have accumulated very little data for the `User` type till now, then you might want to go with 
option #1. But, if you have an active application with a very large dataset then updating the 
node of each user may not be a thing you might want to commit to, as that can require some 
maintenance downtime. So, option #2 could be a better choice in such conditions.

Option #2 makes your new schema compatible with your existing data. Here's an example:

```graphql
type AppUser @dgraph(type: "User") {
    id: ID!
    name: String
}
```

So, no downtime required. Migration is done by just updating your schema. Fast, easy, and simple.

Note that, irrespective of what option you choose for migration on Dgraph side, you will still 
need to migrate your GraphQL clients to use the new name in queries/mutations. For example, the 
query `getUser` would now be renamed to `getAppUser`. So, your downstream clients need to update 
that bit in the code.

### Renaming a field

Just like renaming a type, let's say you had the following working schema:

```graphql
type User {
    id: ID!
    name: String
    phone: String
}
```

and now you figured that it would be better to call `phone` as `tel`. You need migration.

You have the same two choices as before:
1. Migrate all the data for the field `phone` to use the new name `tel`. OR,
2. Just use the [`@dgraph(pred: ...)`](/graphql/dgraph) directive to maintain backward compatibility
   with the existing data.
   
Here's an example if you want to go with option #2:

```graphql
type User {
    id: ID!
    name: String
    tel: String @dgraph(pred: "User.phone")
}
```

Again, note that, irrespective of what option you choose for migration on Dgraph side, you will 
still need to migrate your GraphQL clients to use the new name in queries/mutations. For example,
the following query:

```graphql
query {
    getUser(id: "0x05") {
        name
        phone
    }
}
```

would now have to be changed to:

```graphql
query {
    getUser(id: "0x05") {
        name
        tel
    }
}
```

So, your downstream clients need to update that bit in the code.

### Changing a field's type

There can be multiple scenarios in this category:
* List -> Single item
* `String` -> `Int`
* Any other combination you can imagine

It is strictly advisable that you figure out a solid schema before going in production, so that 
you don't have to deal with such cases later. Nevertheless, if you ended up in such a situation, you
have to migrate your data to fit the new schema. There is no easy way around here.

An example scenario is, if you initially had this schema:

```graphql
type Todo {
    id: ID!
    task: String
    owner: Owner
}  

type Owner {
    name: String! @id
    todo: [Todo] @hasInverse(field:"owner")
}
```

and later you decided that you want an owner to have only one todo at a time. So, you want to 
make your schema look like this:

```graphql
type Todo {
    id: ID!
    task: String
    owner: Owner
}  

type Owner {
    name: String! @id
    todo: Todo @hasInverse(field:"owner")
}
```

If you try updating your schema, you may end up getting an error like this:

```txt
resolving updateGQLSchema failed because succeeded in saving GraphQL schema but failed to alter Dgraph schema - GraphQL layer may exhibit unexpected behavior, reapplying the old GraphQL schema may prevent any issues: Schema change not allowed from [uid] => uid without deleting pred: owner.todo
```

That is a red flag. As the error message says, you should revert to the old schema to make your 
clients work correctly. In such cases, you should have migrated your data to fit the new schema
_before_ applying the new schema. The steps for such a data migration varies from case to case, 
and so can't all be listed down here, but you need to migrate your data first, is all you need 
to keep in mind while making such changes.

### Adding `@id` to an existing field

Let's say you had the following schema:

```graphql
type User {
    id: ID!
    username: String
}
```

and now you think that `username` must be unique for every user. So, you change the schema to this:

```graphql
type User {
    id: ID!
    username: String! @id
}
```

Now, here's the catch: with the old schema, it was possible that there could have existed 
multiple users with the username `Alice`. If that was true, then the queries would break in such 
cases. Like, if you run this query after the schema change:

```graphql
query {
    getUser(username: "Alice") {
        id
    }
}
```

Then it might error out saying:

```txt
A list was returned, but GraphQL was expecting just one item. This indicates an internal error - probably a mismatch between the GraphQL and Dgraph/remote schemas. The value was resolved as null (which may trigger GraphQL error propagation) and as much other data as possible returned.
```

So, while making such a schema change, you need to make sure that the underlying data really 
honors the uniqueness constraint on the username field. If not, you need to do a data migration 
to honor such constraints.
