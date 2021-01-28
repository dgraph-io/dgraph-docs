+++
title = "Update Mutations"
description = "Update mutations let you to update existing objects of a particular type. With update mutations, you can filter nodes and set and remove any field belonging to a type."
weight = 3
[menu.main]
    parent = "graphql-mutations"
    name = "Update"
+++

Update mutations let you update existing objects of a particular type. With update mutations, you can filter nodes and set or remove any field belonging to a type.

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

Dgraph automatically generates input and return types in the schema for the update mutation. Update mutations take `filter` as an input to select specific objects. You can specify `set` and `remove` operations on fields belonging to the filtered objects. It returns the state of the objects after updating.

{{% notice "note" %}}
Executing an empty `remove {}` statement is equivalent to `remove *` and will delete everything for the predicate in the specified filter.
{{% /notice %}}

```graphql
updatePost(input: UpdatePostInput!): UpdatePostPayload

input UpdatePostInput {
	filter: PostFilter!
	set: PostPatch
	remove: PostPatch
}

type UpdatePostPayload {
	post(filter: PostFilter, order: PostOrder, first: Int, offset: Int): [Post]
	numUids: Int
}
```

### Set

For example, an update `set` mutation using variables:

```graphql
mutation updatePost($patch: UpdatePostInput!) {
  updatePost(input: $patch) {
    post {
      postID
      title
      text
    }
  }
}
```
Variables:
```json
{ "patch":
  { "filter": {
      "postID": ["0x123", "0x124"]
    },
    "set": {
      "text": "updated text"
    }
  }
}
```

### Remove

For example an update `remove` mutation using variables:

```graphql
mutation updatePost($patch: UpdatePostInput!) {
  updatePost(input: $patch) {
    post {
      postID
      title
      text
    }
  }
}
```
Variables:
```json
{ "patch":
  { "filter": {
      "postID": ["0x123", "0x124"]
    },
    "remove": {
      "text": "delete this text"
    }
  }
}
```

### Examples

You can refer to the following [link](https://github.com/dgraph-io/dgraph/blob/master/graphql/resolve/update_mutation_test.yaml) for more examples.
