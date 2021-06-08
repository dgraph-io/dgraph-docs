+++
title = "Delete Mutations in GraphQL"
description = "In this guide we explain how to use delete mutations in GraphQL, allowing you to delete objects of a particular type. Also included is the schema used in GraphQL examples."
weight = 4
[menu.main]
    parent = "graphql-mutations"
    name = "Delete"
    identifier = "graphql-delete"
+++

Delete Mutations allow you to delete objects of a particular type.

We use the following schema to demonstrate some examples.

**Schema**:
```graphql
type Author {
	id: ID!
	name: String! @search(by: [hash])
	dob: DateTime
	posts: [Post]
}

type Post {
	postID: ID!
	title: String! @search(by: [term, fulltext])
	text: String @search(by: [fulltext, term])
	datePublished: DateTime
}
```

Dgraph automatically generates input and return types in the schema for the `delete` mutation.
Delete mutations take `filter` as an input to select specific objects and returns the state of the objects before deletion.
```graphql
deleteAuthor(filter: AuthorFilter!): DeleteAuthorPayload

type DeleteAuthorPayload {
	author(filter: AuthorFilter, order: AuthorOrder, first: Int, offset: Int): [Author]
	msg: String
	numUids: Int
}
```

**Example**: Delete mutation using variables
```graphql
mutation deleteAuthor($filter: AuthorFilter!) {
  deleteAuthor(filter: $filter) {
    msg
    author {
      name
      dob
    }
  }
}
```
Variables:
```json
{ "filter":
  { "name": { "eq": "A.N. Author" } }
}
```

## Examples

You can refer to the following [link](https://github.com/dgraph-io/dgraph/blob/master/graphql/resolve/delete_mutation_test.yaml) for more examples.
