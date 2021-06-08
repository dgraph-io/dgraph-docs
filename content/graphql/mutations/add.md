+++
title = "Add Mutations in GraphQL"
description = "Add mutations allows you to add new objects of a particular type. Dgraph automatically generates input and return types in the schema for the add mutation"
weight = 2
[menu.main]
    parent = "graphql-mutations"
    name = "Add"
+++

Add mutations allow you to add new objects of a particular type.

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

Dgraph automatically generates input and return types in the schema for the `add` mutation, 
as shown below:
```graphql
addPost(input: [AddPostInput!]!): AddPostPayload

input AddPostInput {
	title: String!
	text: String
	datePublished: DateTime
}

type AddPostPayload {
	post(filter: PostFilter, order: PostOrder, first: Int, offset: Int): [Post]
	numUids: Int
}
```

**Example**: Add mutation on single type with embedded value
```graphql
mutation {
  addAuthor(input: [{ name: "A.N. Author", posts: []}]) {
    author {
      id
      name
    }
  }
}
```

**Example**: Add mutation on single type using variables
```graphql
mutation addAuthor($author: [AddAuthorInput!]!) {
  addAuthor(input: $author) {
    author {
      id
      name
    }
  }
}
```
Variables:
```json
{ "author":
  { "name": "A.N. Author",
    "dob": "2000-01-01",
    "posts": []
  }
}
```

{{% notice "note" %}}
You can convert an `add` mutation to an `upsert` mutation by setting the value of the input variable `upsert` to `true`. For more information, see [Upsert Mutations](/graphql/mutations/upsert).
{{% /notice %}}

## Examples

You can refer to the following [link](https://github.com/dgraph-io/dgraph/blob/master/graphql/resolve/add_mutation_test.yaml) for more examples.
