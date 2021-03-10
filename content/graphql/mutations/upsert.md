+++
title = "Upsert Mutations"
description = "Upsert mutations allow you to perform `add` or `update` operations based on whether a particular ID exists in the database"
weight = 2
[menu.main]
    parent = "graphql-mutations"
    name = "Upsert"
+++

Upsert mutations allow you to perform `add` or `update` operations based on whether a particular `ID` exists in the database. The IDs must be external IDs, defined using the `@id` directive in the schema.

For example, to demonstrate how upserts work in GraphQL, take the following schema:

**Schema**
```graphql
type Author {
	id: String! @id
	name: String! @search(by: [hash])
	posts: [Post] @hasInverse(field: author)
}

type Post {
	postID: String! @id
	title: String! @search(by: [term, fulltext])
	text: String @search(by: [fulltext, term])
	author: Author!
}
```

Dgraph automatically generates input and return types in the schema for the `add` mutation, as shown below:

```graphql
addPost(input: [AddPostInput!]!, upsert: Boolean): AddPostPayload

input AddPostInput {
  postID: String!
  title: String!
  text: String
  author: AuthorRef!
}
```

Suppose you want to update the `text` field of a post with the ID `mm2`. But you also want to create a new post with that ID in case it doesn't already exist. To do this, you use the `addPost` mutation, but with an additional input variable `upsert`.  

This is a `Boolean` variable. Setting it to `true` will result in an upsert operation.

It will perform an `update` mutation and carry out the changes you specify in your request if the particular ID exists. Otherwise, it will fall back to a default `add` operation and create a new `Post` with that ID and the details you provide.

Setting `upsert` to `false` is the same as using a plain `add` operation—it'll either fail or succeed, depending on whether the ID exists or not.

**Example**: Add mutation with `upsert` true:

```graphql
mutation($post: [AddPostInput!]!) {
  addPost(input: $post, upsert: true) {
    post {
      postID
      title
      text
      author {
        id
      }
    }
  }
}
```

With variables:

```json
{
	"post": 
  {
		"postID": "mm2",
		"title": "Second Post",
		"text": "This is my second post, and updated with some new information.",
		"author": {
			"id": "micky"
		}
	}
}
```

If a post with the ID `mm2` exists, it will update the post with the new details. Otherwise, it'll create a new `Post` with that ID and the values you provided. In either case, you'll get the following response back:

```graphql
"data": {
    "addPost": {
      "post": [
        {
          "postID": "mm2",
          "title": "Second Post",
          "text": "This is my second post, and updated with some new information.",
          "author": {
            "id": "micky"
          }
        }
      ]
    }
  }
```

{{% notice "note" %}}
* The default value of `uspert` will be `false`, for backward compatibility.
* The current behavior of `Add` and `Update` mutations is such that they do not update deep level nodes. So Add mutations with `upsert` set to `true` will only update values at the root level. 
{{% /notice %}}

## Examples
You can refer to the following [link](https://github.com/dgraph-io/dgraph/blob/master/graphql/resolve/add_mutation_test.yaml) for more examples.