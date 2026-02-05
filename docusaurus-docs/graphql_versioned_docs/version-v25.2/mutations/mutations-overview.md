---
title: "Mutations Overview"
description: "Mutations can be used to insert, update, or delete data. Dgraph automatically generates GraphQL mutation for each type that you define in your schema."

---

Mutations allow you to modify server-side data, and it also returns an object based on the operation performed. It can be used to insert, update, or delete data. Dgraph automatically generates GraphQL mutations for each type that you define in your schema. The mutation field returns an object type that allows you to query for nested fields. This can be useful for fetching an object's new state after an add/update, or to get the old state of an object before a delete.

**Example**

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

The following mutations would be generated from the above schema.

```graphql
type Mutation {
	addAuthor(input: [AddAuthorInput!]!): AddAuthorPayload
	updateAuthor(input: UpdateAuthorInput!): UpdateAuthorPayload
	deleteAuthor(filter: AuthorFilter!): DeleteAuthorPayload
	addPost(input: [AddPostInput!]!): AddPostPayload
	updatePost(input: UpdatePostInput!): UpdatePostPayload
	deletePost(filter: PostFilter!): DeletePostPayload
}

type AddAuthorPayload {
	author(filter: AuthorFilter, order: AuthorOrder, first: Int, offset: Int): [Author]
	numUids: Int
}

type AddPostPayload {
	post(filter: PostFilter, order: PostOrder, first: Int, offset: Int): [Post]
	numUids: Int
}

type DeleteAuthorPayload {
	author(filter: AuthorFilter, order: AuthorOrder, first: Int, offset: Int): [Author]
	msg: String
	numUids: Int
}

type DeletePostPayload {
	post(filter: PostFilter, order: PostOrder, first: Int, offset: Int): [Post]
	msg: String
	numUids: Int
}

type UpdateAuthorPayload {
	author(filter: AuthorFilter, order: AuthorOrder, first: Int, offset: Int): [Author]
	numUids: Int
}

type UpdatePostPayload {
	post(filter: PostFilter, order: PostOrder, first: Int, offset: Int): [Post]
	numUids: Int
}
```

## Input objects
Mutations require input data, such as the data, to create a new object or an object's ID to delete. Dgraph auto-generates the input object type for every type in the schema.

```graphql
input AddAuthorInput {
	name: String!
	dob: DateTime
	posts: [PostRef]
}

mutation {
  addAuthor(
    input: {
      name: "A.N. Author",
      lastName: "2000-01-01",
    }
  )
  {
    ...
  }
}
```

## Return fields
Each mutation provides a set of fields that can be returned in the response. Dgraph auto-generates the return payload object type for every type in the schema.

```graphql
type AddAuthorPayload {
	author(filter: AuthorFilter, order: AuthorOrder, first: Int, offset: Int): [Author]
	numUids: Int
}
```

## Multiple fields in mutations
A mutation can contain multiple fields, just like a query. While query fields are executed in parallel, mutation fields run in series, one after the other. This means that if we send two `updateAuthor` mutations in one request, the first is guaranteed to finish before the second begins. This ensures that we don't end up with a race condition with ourselves. If one of the mutations is aborted due error like transaction conflict, we continue performing the next mutations.

**Example**: Mutation on multiple types
```graphql
mutation ($post: AddPostInput!, $author: AddAuthorInput!) {
  addAuthor(input: [$author]) {
    author {
      name
    }
  }
  addPost(input: [$post]) {
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
{
  "author": {
	"name": "A.N. Author",
	"dob": "2000-01-01",
	"posts": []
  },
  "post": {
	"title": "Exciting post",
	"text": "A really good post",
	"author": {
	  "name": "A.N. Author"
	}
  }
}
```

## Union mutations

Mutations can be used to add a node to a `union` field in a type. 

For the following schema, 

```graphql
enum Category {
  Fish
  Amphibian
  Reptile
  Bird
  Mammal
  InVertebrate
}

interface Animal {
  id: ID!
  category: Category @search
}

type Dog implements Animal {
  breed: String @search
}

type Parrot implements Animal {
  repeatsWords: [String]
}

type Human {
  name: String!
  pets: [Animal!]!
}

union HomeMember = Dog | Parrot | Human

type Home {
  id: ID!
  address: String
  members: [HomeMember]
}
```

This is the mutation for adding `members` to the `Home` type:

```graphql
mutation {
  addHome(input: [
        {
          "address": "United Street",
          "members": [
            { "dogRef": { "category": Mammal, "breed": "German Shepherd"} },
            { "parrotRef": { "category": Bird, "repeatsWords": ["squawk"]} },
            { "humanRef": { "name": "Han Solo"} }
          ]
        }
      ]) {
    home {
      address
      members {
        ... on Dog {
          breed
        }
        ... on Parrot {
          repeatsWords
        }
        ... on Human {
          name
        }
      }
    }
  }
}
```

## Vector Embedding mutations

For types with vector embeddings Dgraph automatically generates the add mutation. For this example of add mutation we use the following schema.

```graphql
type User {
    userID: ID!
    name: String!
    name_v: [Float!] @embedding @search(by: ["hnsw(metric: euclidean, exponent: 4)"])
}

mutation {
addUser(input: [
{ name: "iCreate with a Mini iPad", name_v: [0.12, 0.53, 0.9, 0.11, 0.32] },
{ name: "Resistive Touchscreen", name_v: [0.72, 0.89, 0.54, 0.15, 0.26] },
{ name: "Fitness Band", name_v: [0.56, 0.91, 0.93, 0.71, 0.24] },
{ name: "Smart Ring", name_v: [0.38, 0.62, 0.99, 0.44, 0.25] }]) 
  {
    project {
      id
      name
      name_v
    }
  }
}
```

Note: The embeddings are generated outside of Dgraph using any suitable machine learning model.

## Examples

You can refer to the following [link](https://github.com/dgraph-io/dgraph/tree/main/graphql/schema/testdata/schemagen) for more examples.
