+++
title = "Raw HTTP"
description = "Get the structure for GraphQL requests and responses, how to enable compression for them, and configuration options for extensions."
weight = 2
[menu.main]
    parent = "api"
    identifier = "graphql-http"
    name = "Raw HTTP"
+++

GraphQL requests can be sent via HTTP POST or HTTP GET requests.

## Endpoint
<TO DO>



## Requests

### Headers


<div class="tablenoheaders">

| Header | Value |
|:------|:------|
| Content-Type | `application/graphql` or `application/json` |
| Content-Encoding  | optional  `gzip` |
| Accept-Encoding  |  optional  `gzip` |
</div>
To use data compression for requests and POST gzip-compressed data:
- set HTTP header `Content-Encoding` to `gzip`. 

To use data compression for responses:
- set the HTTP header `Accept-Encoding` to `gzip`.

### Payload format
POST requests sent with the Content-Type header `application/graphql` must have a POST body content as a GraphQL query string. For example, the following is a valid POST body for a query:

```graphql
query {
  getTask(id: "0x3") {
    id
    title
    completed
    user {
      username
      name
    }
  }
}
```

POST requests sent with the Content-Type header `application/json` must have a POST body in the following JSON format:

```json
{
  "query": "...",
  "operationName": "...",
  "variables": { "var": "val", ... }
}
```

GET requests must be sent in the following format. The query, variables, and operation are sent as URL-encoded query parameters in the URL.

```
http://localhost:8080/graphql?query={...}&variables={...}&operation=...
```

I- `query` is mandatory
- `variables` is only required if the query contains GraphQL variables.
- `operationName` is only required if there are multiple operations in the query; in which case, operations must also be named.

### Variables

Variables simplify GraphQL queries and mutations by letting you pass data separately. A GraphQL request can be split into two sections: one for the query or mutation, and another for variables.

Variables can be declared after the `query` or `mutation` and are passed like arguments to a function and begin with `$`.

#### Query Example

```graphql
query post($filter: PostFilter) {
	queryPost(filter: $filter) {
		title
		text
		author {
			name
		}
	}
}
```

**Variables**

```graphql
{
	"filter": {
		"title": {
			"eq": "First Post"
		}
	}
}
```

**Result**

```graphql
{
	"data": {
		"queryPost": [{
			"title": "First Post",
			"text": "Hello world!",
			"author": [{
				"name": "A.N. Author"
			}]
		}]
	}
}
```

#### Mutation Example

```graphql
mutation addAuthor($author: AddAuthorInput!) {
	addAuthor(input: [$author]) {
		author {
			name
			posts {
				title
				text
			}
		}
	}
}
```

**Variables**

```graphql
{
	"author": {
		"name": "A.N. Author",
		"dob": "2000-01-01",
		"posts": [{
			"title": "First Post",
			"text": "Hello world!"
		}]
	}
}
```

**Result**

```graphql
{
	"data": {
		"addAuthor": {
			"author": [{
				"name": "A.N. Author",
				"posts": [{
					"title": "First Post",
					"text": "Hello world!"
				}]
			}]
		}
	}
}
```

### Fragments
A GraphQL fragment is a reusable unit of logic that can be shared between multiple queries and mutations.
Here, we declare a `postData` fragment that can be used with any `Post` object:

```graphql
fragment postData on Post {
  id
  title
  text
  author {
    username
    displayName
  }
}
```

The fragment has a subset of the fields from its associated type. In the above example, the `Post` type must declare all the fields present in the `postData` fragment for it be valid.

We can include the `postData` fragment in any number of queries and mutations as shown below.
```graphql
query allPosts {
  queryPost(order: { desc: title }) {
    ...postData
  }
}
mutation addPost($post: AddPostInput!) {
  addPost(input: [$post]) {
    post {
      ...postData
    }
  }
}
```

The above request is equivalent to:
```graphql
query allPosts {
  queryPost(order: { desc: title }) {
    id
    title
    text
    author {
      username
      displayName
    }
  }
}

mutation addPost($post: AddPostInput!) {
  addPost(input: [$post]) {
    post {
      id
      title
      text
      author {
        username
        displayName
      }
    }
  }
}
```

**Example**

```graphql
fragment postData on Post {
  id
  title
  text
  author {
    username
    displayName
  }
}
mutation addPost($post: AddPostInput!) {
  addPost(input: [$post]) {
    post {
      ...postData
    }
  }
}
```

**Variable**

```graphql
{
	"post": {
    "text": "Hello World",
		"title": "First Blog post",
		"author": [{
			"username": "arijit_ad",
			"displayName": "Arijit Das"
		}]
	}
}
```

**Result**

```graphql
{
  "addPost": {
    "post": [
      {
        "id": "0x27e0",
        "title": "First Blog post",
        "text": "Hello World",
        "author": [
          {
            "username": "arijit_ad",
            "displayName": "Arijit Das"
          }
        ]
      }
    ]
  }
}
```

### Using fragments with interfaces

It is possible to define fragments on interfaces.
Here's an example of a query that includes in-line fragments:

**Schema**

```graphql
interface Employee {
    ename: String!
}
interface Character {
    id: ID!
    name: String! @search(by: [exact])
}
type Human implements Character & Employee {
    totalCredits: Float
}
type Droid implements Character {
    primaryFunction: String
}
```

**Query**

```graphql
query allCharacters {
  queryCharacter {
    name
    __typename
    ... on Human {
      totalCredits
    }
    ... on Droid {
      primaryFunction
    }
  }
}
```

The `allCharacters` query returns a list of `Character` objects. Since `Human` and `Droid` implements the `Character` interface, the fields in the result would be returned according to the type of object.

**Result**

```graphql
{
  "data": {
    "queryCharacter": [
      {
        "name": "Human1",
        "__typename": "Human",
        "totalCredits": 200.23
      },
      {
        "name": "Human2",
        "__typename": "Human",
        "totalCredits": 2.23
      },
      {
        "name": "Droid1",
        "__typename": "Droid",
        "primaryFunction": "Code"
      },
      {
        "name": "Droid2",
        "__typename": "Droid",
        "primaryFunction": "Automate"
      }
    ]
  }
}
```

## Responses
All responses, including errors, always return HTTP 200 OK status codes.

The response is a JSON map including the fields `"data"`, `"errors"`, or `"extensions"` following the GraphQL specification. They follow the following formats.

Successful queries are in the following format:

```json
{
  "data": { ... },
  "extensions": { ... }
}
```

Queries that have errors are in the following format.

```json
{
  "errors": [ ... ],
}
```


### "data" field

The "data" field contains the result of your GraphQL request. The response has exactly the same shape as the result. For example, notice that for the following query, the response includes the data in the exact shape as the query.

Query:

```graphql
query {
  getTask(id: "0x3") {
    id
    title
    completed
    user {
      username
      name
    }
  }
}
```

Response:

```json
{
  "data": {
    "getTask": {
      "id": "0x3",
      "title": "GraphQL docs example",
      "completed": true,
      "user": {
        "username": "dgraphlabs",
        "name": "Dgraph Labs"
      }
    }
  }
}
```

### "errors" field

The "errors" field is a JSON list where each entry has a `"message"` field that describes the error and optionally has a `"locations"` array to list the specific line and column number of the request that points to the error described. For example, here's a possible error for the following query, where `getTask` needs to have an `id` specified as input:

Query:
```graphql
query {
  getTask() {
    id
  }
}
```

Response:
```json
{
  "errors": [
    {
      "message": "Field \"getTask\" argument \"id\" of type \"ID!\" is required but not provided.",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ]
    }
  ]
}
```

### "extensions" field

The "extensions" field contains extra metadata for the request with metrics and trace information for the request.

- `"touched_uids"`: The number of nodes that were touched to satisfy the request. This is a good metric to gauge the complexity of the query.
- `"tracing"`: Displays performance tracing data in [Apollo Tracing][apollo-tracing] format. This includes the duration of the whole query and the duration of each operation.

[apollo-tracing]: https://github.com/apollographql/apollo-tracing

Here's an example of a query response with the extensions field:

```json
{
  "data": {
    "getTask": {
      "id": "0x3",
      "title": "GraphQL docs example",
      "completed": true,
      "user": {
        "username": "dgraphlabs",
        "name": "Dgraph Labs"
      }
    }
  },
  "extensions": {
    "touched_uids": 9,
    "tracing": {
      "version": 1,
      "startTime": "2020-07-29T05:54:27.784837196Z",
      "endTime": "2020-07-29T05:54:27.787239465Z",
      "duration": 2402299,
      "execution": {
        "resolvers": [
          {
            "path": [
              "getTask"
            ],
            "parentType": "Query",
            "fieldName": "getTask",
            "returnType": "Task",
            "startOffset": 122073,
            "duration": 2255955,
            "dgraph": [
              {
                "label": "query",
                "startOffset": 171684,
                "duration": 2154290
              }
            ]
          }
        ]
      }
    }
  }
}
```

**Turn off extensions**

To turn off extensions set the
`--graphql` superflag's `extensions` option to false (`--graphql extensions=false`)
when running Dgraph Alpha.





