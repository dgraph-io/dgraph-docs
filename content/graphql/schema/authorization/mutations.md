+++
title = "Mutations and GraphQL Authorization"
description = "Mutations with authorization work like queries. But mutations involve a state change in the database, so you need to understand when the rules are applied."
weight = 3
[menu.main]
    name = "Mutations"
    parent = "authorization"
+++

Mutations with authorization work like queries. But because mutations involve a state change in the database,  it's important to understand when the authorization rules are applied and what they mean.

## Add

Rules for `add` authorization state that the rule must hold of nodes created by the mutation data once committed to the database.

For example, a rule such as the following:

```graphql
type Todo @auth(
    add: { rule: """
        query ($USER: String!) { 
            queryTodo {
                owner(filter: { username: { eq: $USER } } ) { 
                    username
                } 
            } 
        }"""
    }
){
    id: ID!
    text: String!
    owner: User
}
type User {
    username: String! @id
    todos: [Todo]
}
```

... states that if you add a new to-do list item, then that new to-do must satisfy the `add` rule, in this case saying that you can only add to-do list items with yourself as the author.

## Delete

Delete rules filter the nodes that can be deleted. A user can only ever delete a subset of the nodes that the `delete` rules allow.  

For example, the following rule states that a user can delete a to-do list item if they own it, or they have the `ADMIN` role:

```graphql
type Todo @auth(
    delete: { or: [ 
        { rule: """
            query ($USER: String!) { 
                queryTodo {
                    owner(filter: { username: { eq: $USER } } ) { 
                        username
                    } 
                } 
            }"""
        },
        { rule:  "{$ROLE: { eq: \"ADMIN\" } }"}
    ]}
){
    id: ID!
    text: String! @search(by: [term])
    owner: User
}

type User {
    username: String! @id
    todos: [Todo]
}
```

So with these types of rules, a mutation like the following performs differently
depending on which user is running it:
* For most users, the following mutation deletes the posts that contain the
  term "graphql" and are owned by the user who runs the mutation, but doesn't
  affect any other user's to-do list items
* For an admin user, the following mutation deletes any posts that contain the
  term "graphql", regardless of which user owns these posts

```graphql
mutation {
    deleteTodo(filter: { text: { anyofterms: "graphql" } }) {
        numUids    
    }
}
```

When adding data, what matters is the resulting state of the database, when deleting,
what matters is the the state before the delete occurs.

## Update

Updates have both a before and after state that can be important for authorization.  

For example, consider a rule stating that you can only update your own to-do list items. If evaluated in the database before the mutation (like the delete rules) it would prevent you from updating anyone else's to-do list items, but does it stop you from updating your own to-do items to have a different `owner`. If evaluated in the database after the mutation occurs, like for add rules, it would prevent setting the `owner` to another user, but would not prevent editing other's posts.

Currently, Dgraph evaluates `update` rules _before_ the mutation.

## Update and add mutations

Update mutations can also insert new data. For example, you might allow a mutation that runs an update mutation to add a new to-do list item:

```graphql
mutation {
    updateUser(input: {
        filter: { username: { eq: "aUser" }},
        set: { todos: [ { text: "do this new todo"} ] }
    }) {
        ...
    }
}
```

Because a mutation updates a user's to-do list by inserting a new to-do list item, it
would have to satisfy the rules to update the author _and_ the rules to add a
to-do list item. If either fail, the mutation has no effect.

---