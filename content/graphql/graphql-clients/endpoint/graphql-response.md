+++
title = "HTTP Response"
description = "Get the structure for GraphQL requests and responses, how to enable compression for them, and configuration options for extensions."
weight = 3
[menu.main]
    parent = "graphql-endpoint"
    identifier = "graphql-response"
    name = "HTTP Response"
+++

<div class="api">


### Responses
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


#### "data" field

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

#### "errors" field

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
#### Error propagation
Before returning query and mutation results, Dgraph uses the types in the schema to apply GraphQL [value completion](https://graphql.github.io/graphql-spec/June2018/#sec-Value-Completion) and [error handling](https://graphql.github.io/graphql-spec/June2018/#sec-Errors-and-Non-Nullability).  That is, `null` values for non-nullable fields, e.g. `String!`, cause error propagation to parent fields.  

In short, the GraphQL value completion and error propagation mean the following.

* Fields marked as nullable (i.e. without `!`) can return `null` in the json response.
* For fields marked as non-nullable (i.e. with `!`) Dgraph never returns null for that field.
* If an instance of type has a non-nullable field that has evaluated to null, the whole instance results in null.
* Reducing an object to null might cause further error propagation.  For example, querying for a post that has an author with a null name results in null: the null name (`name: String!`) causes the author to result in null, and a null author causes the post (`author: Author!`) to result in null.
* Error propagation for lists with nullable elements, e.g. `friends [Author]`, can result in nulls inside the result list.
* Error propagation for lists with non-nullable elements results in null for `friends [Author!]` and would cause further error propagation for `friends [Author!]!`.

Note that, a query that results in no values for a list will always return the empty list `[]`, not `null`, regardless of the nullability.  For example, given a schema for an author with `posts: [Post!]!`, if an author has not posted anything and we queried for that author, the result for the posts field would be `posts: []`.  

A list can, however, result in null due to GraphQL error propagation.  For example, if the definition is `posts: [Post!]`, and we queried for an author who has a list of posts.  If one of those posts happened to have a null title (title is non-nullable `title: String!`), then that post would evaluate to null, the `posts` list can't contain nulls and so the list reduces to null.

#### "extensions" field

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
</div>




