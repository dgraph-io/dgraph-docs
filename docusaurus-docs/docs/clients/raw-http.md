---
title: Raw HTTP
---

Dgraph exposes HTTP endpoints for querying, mutating, and managing the database. Use these endpoints to build clients in languages without gRPC support.

This documentation describes the HTTP API endpoints and request/response formats. Examples use `curl` and [`jq`](https://stedolan.github.io/jq/) to demonstrate the API. For gRPC-based client implementation, see the [Go client](go).

## Alter the DQL Schema

You need to alter the DQL schema to declare predicate types, add predicate search indexes, and declare the predicates expected in entities of specific types.

Update the DQL schema by posting schema data to the `/alter` endpoint:

```sh
curl "localhost:8080/alter" --silent --request POST \
  --data $'
name: string @index(term) .
balance: int .

type User {
  name
  balance
}
' | jq
```

Alternatively, you can post the schema from a file:

```sh
curl "localhost:8080/alter" --silent --request POST \
  --data-binary @schema.dql | jq
```

Where `schema.dql` contains:

```dql
name: string @index(term) .
balance: int .

type User {
  name
  balance
}
```

**Success response:**

```json
{
  "data": {
    "code": "Success",
    "message": "Done"
  }
}
```

**Error response:**

In case of errors, the API will reply with an error message such as:

```json
{
  "errors": [
    {
      "extensions": {
        "code": "Error"
      },
      "message": "line 5 column 18: Invalid ending"
    }
  ]
}
```

:::note
The request will update or create the predicates and types present in the request. It will not modify or delete other schema information that may be present.
:::

## Query Current DQL Schema

Obtain the DQL schema by issuing a DQL query on the `/query` endpoint:

```sh
curl -X POST \
  -H "Content-Type: application/dql" \
  localhost:8080/query -d $'schema {}' | jq
```

:::note
The schema is returned as json document. 

You may need to convert this json to the format used by the `alter` operation.

Check [dgraph_schema_converter] (https://github.com/dgraph-io/dgraph-experimental/blob/main/dql-helper/dgraph_schema_converter.sh) in dgraph-experimental repository.
:::

## Create Data with Mutations

Mutations can be done over HTTP by making a `POST` request to an Alpha's `/mutate` endpoint. Set the `Content-Type` header to `application/rdf` to specify that the mutation is written in RDF format.

### Mutation using RDF format
To create Alice and Bob with initial balances:
```sh
curl -H "Content-Type: application/rdf" -X POST "localhost:8080/mutate?commitNow=true" -d $'
{
  set {
    _:alice <name> "Alice" .
    _:alice <balance> "100" .
    _:alice <dgraph.type> "User" .
    _:bob <name> "Bob" .
    _:bob <balance> "70" .
    _:bob <dgraph.type> "User" .
  }
}
' | jq
```

**Response:**

```json
{
  "data": {
    "code": "Success",
    "message": "Done",
    "uids": {
      "alice": "0x1",
      "bob": "0x2"
    }
  },
  "extensions": {
    "server_latency": {
      "parsing_ns": 50901,
      "processing_ns": 14631082
    },
    "txn": {
      "start_ts": 4,
      "commit_ts": 5
    }
  }
}
```

The response contains `uids` which maps the blank node identifiers (`_:alice`, `_:bob`) to the actual UIDs assigned by Dgraph (`0x1`, `0x2`). These UIDs can be used in subsequent queries and mutations.

:::note
The `commitNow=true` parameter commits the transaction immediately after the mutation. For multi-step transactions, you can omit this parameter and use the `/commit` endpoint separately.
:::

### Mutation using JSON format

The  `mutate` operation also accepts JSON input format:
```sh
curl -H "Content-Type: application/json" \
  -X POST "localhost:8080/mutate?commitNow=true" \
  -d '{
    "set": [
      {
        "uid": "_:alice",
        "name": "Alice",
        "balance": 100,
        "dgraph.type": "User"
      },
      {
        "uid": "_:bob",
        "name": "Bob",
        "balance": 70,
        "dgraph.type": "User"
      }
    ]
  }' | jq
```
Note that
- Content-type is 'application/json'
- The payload is valid json document: the `set` keyword has quotes.

#### UID
`uid` can be omitted in the JSON if you don't have to retrieve the generated UID in the response.


## Query Data

To query the database, use the `/query` endpoint. Set the `Content-Type` header to `application/dql` to ensure that the body of the request is parsed correctly.

To get the balances for both users:

```sh
curl -H "Content-Type: application/dql" -X POST localhost:8080/query -d $'
{
  users(func: anyofterms(name, "Alice Bob")) {
    uid
    name
    balance
  }
}' | jq
```

**Response:**

```json
{
  "data": {
    "users": [
      {
        "uid": "0x1",
        "name": "Alice",
        "balance": "100"
      },
      {
        "uid": "0x2",
        "name": "Bob",
        "balance": "70"
      }
    ]
  },
  "extensions": {
    "server_latency": {
      "parsing_ns": 70494,
      "processing_ns": 697140,
      "encoding_ns": 1560151
    },
    "txn": {
      "start_ts": 6
    }
  }
}
```

Notice that along with the query result under the `data` field, there is additional data in the `extensions -> txn` field. This data includes the transaction start timestamp (`start_ts`), which will need to be used if you want to perform mutations as part of the same transaction.

### Query with RDF Response Format

You can request query results in RDF format by adding the `respFormat=RDF` parameter to the query endpoint:

```sh
curl -H "Content-Type: application/dql" -X POST "localhost:8080/query?respFormat=rdf" -d $'
{
  users(func: anyofterms(name, "Alice Bob")) {
    uid
    name
    balance
  }
}' | jq -r '.data' | sed 's/\\n/\n/g'
```

**Response (RDF format):**

```
<0x1> <name> "Alice" .
<0x1> <balance> "100" .
<0x1> <dgraph.type> "User" .
<0x2> <name> "Bob" .
<0x2> <balance> "70" .
<0x2> <dgraph.type> "User" .
```
### Running Read-Only Queries

You can set the query parameter `ro=true` to `/query` to set it as a [read-only](../dql/index.md#read-only-transactions) query:

```sh
curl -H "Content-Type: application/dql" -X POST "localhost:8080/query?ro=true" -d $'
{
  users(func: anyofterms(name, "Alice Bob")) {
    uid
    name
    balance
  }
}'
```

### Running Best-Effort Queries

You can set the query parameter `be=true` to `/query` to set it as a [best-effort](../dql/index.md#read-only-transactions) query:

```sh
curl -H "Content-Type: application/dql" -X POST "localhost:8080/query?be=true" -d $'
{
  users(func: anyofterms(name, "Alice Bob")) {
    uid
    name
    balance
  }
}'
```
## Transactions

### Transaction State

A client built on top of the HTTP API needs to track three pieces of state for each transaction:

1. **A start timestamp (`start_ts`)**. This uniquely identifies a transaction and doesn't change over the transaction lifecycle.

2. **The set of keys modified by the transaction (`keys`)**. This aids in transaction conflict detection. Every mutation returns a new set of keys. The client must merge them with the existing set.

3. **The set of predicates modified by the transaction (`preds`)**. This aids in predicate move detection. Every mutation returns a new set of predicates. The client must merge them with the existing set.

**For both query and mutation, if the `start_ts` is provided as a path parameter, then the operation is performed as part of the ongoing transaction. Otherwise, a new transaction is initiated.**

### Update Data in a Transaction

To update data within a transaction, first run a query to get the current state and transaction timestamp:

```sh
curl -H "Content-Type: application/dql" -X POST localhost:8080/query -d $'
{
  users(func: anyofterms(name, "Alice Bob")) {
    uid
    name
    balance
  }
}' | jq
```

The response will include a `start_ts` in the `extensions -> txn` field. Use this `start_ts` for subsequent mutations in the same transaction.

Now, if Bob transfers $10 to Alice, update the balances:

```sh
curl -H "Content-Type: application/rdf" -X POST "localhost:8080/mutate?startTs=6" -d $'
{
  set {
    <0x1> <balance> "110" .
    <0x2> <balance> "60" .
  }
}' | jq
```

**Response:**

```json
{
  "data": {
    "code": "Success",
    "message": "Done",
    "uids": {}
  },
  "extensions": {
    "server_latency": {
      "parsing_ns": 50901,
      "processing_ns": 14631082
    },
    "txn": {
      "start_ts": 6,
      "keys": [
        "2ahy9oh4s9csc",
        "3ekeez23q5149"
      ],
      "preds": [
        "1-balance"
      ]
    }
  }
}
```

The result contains `keys` and `preds` which should be added to the transaction state.

### Commit the Transaction

Commit the transaction using the `/commit` endpoint. Provide the `start_ts` you've been using for the transaction along with the list of `keys` and the list of predicates. If you performed multiple mutations in the transaction, the keys and predicates provided during the commit should be the union of all keys and predicates returned in the responses from the `/mutate` endpoint.

The `preds` field is used to abort the transaction in cases where some of the predicates are moved. This field is not required and the `/commit` endpoint also accepts the old format, which was a single array of keys.

```sh
curl -X POST localhost:8080/commit?startTs=6 -d $'
{
  "keys": [
    "2ahy9oh4s9csc",
    "3ekeez23q5149"
  ],
  "preds": [
    "1-balance"
  ]
}' | jq
```

**Response:**

```json
{
  "data": {
    "code": "Success",
    "message": "Done"
  },
  "extensions": {
    "txn": {
      "start_ts": 6,
      "commit_ts": 7
    }
  }
}
```

The transaction is now complete.

If another client were to perform another transaction concurrently affecting the same keys, then it's possible that the transaction would *not* be successful. This is indicated in the response when the commit is attempted:

```json
{
  "errors": [
    {
      "code": "Error",
      "message": "Transaction has been aborted. Please retry."
    }
  ]
}
```

In this case, it should be up to the user of the client to decide if they wish to retry the transaction.

### Abort the Transaction

To abort a transaction, use the same `/commit` endpoint with the `abort=true` parameter while specifying the `startTs` value for the transaction:

```sh
curl -X POST "localhost:8080/commit?startTs=6&abort=true" | jq
```

**Response:**

```json
{
  "code": "Success",
  "message": "Done"
}
```

## Delete Data

### Delete Specific Triples

To delete specific triples (data), use the `delete` block in a mutation:

```sh
curl -H "Content-Type: application/rdf" -X POST localhost:8080/mutate?commitNow=true -d $'
{
  delete {
    <0x1> <balance> * .
  }
}' | jq
```

This deletes all `balance` values for the node with UID `0x1`.

To delete a specific value:

```sh
curl -H "Content-Type: application/rdf" -X POST localhost:8080/mutate?commitNow=true -d $'
{
  delete {
    <0x1> <balance> "110" .
  }
}' | jq
```

### Delete an Entire Node

To delete an entire node and all its predicates, use the `*` wildcard:

```sh
curl -H "Content-Type: application/rdf" -X POST localhost:8080/mutate?commitNow=true -d $'
{
  delete {
    <0x1> * * .
  }
}' | jq
```

This deletes the node with UID `0x1` and all its data.

### Delete Predicate

To delete a predicate from the schema (and all its data), use the `/alter` endpoint with the `@drop` directive:

```sh
curl "localhost:8080/alter" --silent --request POST \
  --data $'balance: int @drop .' | python -m json.tool
```

**Response:**

```json
{
  "data": {
    "code": "Success",
    "message": "Done"
  }
}
```

This removes the `balance` predicate from the schema and deletes all data stored in that predicate across all nodes.

:::warning
Deleting a predicate is a destructive operation that cannot be undone. All data stored in that predicate will be permanently deleted.
:::

### Delete Type

To delete a type from the schema, use the `/alter` endpoint with the `@drop` directive on the type:

```sh
curl "localhost:8080/alter" --silent --request POST \
  --data $'type User @drop .' | python -m json.tool
```

**Response:**

```json
{
  "data": {
    "code": "Success",
    "message": "Done"
  }
}
```

This removes the `User` type from the schema. Note that this does not delete the data nodes themselves, only the type definition. The nodes will still exist but will no longer have the `User` type assigned.

:::note
To delete all nodes of a specific type, you would need to query for all nodes of that type and then delete them individually using the delete mutation syntax shown above.
:::



## Compression via HTTP

Dgraph supports gzip-compressed requests to and from Dgraph Alphas for `/query`, `/mutate`, and `/alter`.

**Compressed requests:** To send compressed requests, set the HTTP request header `Content-Encoding: gzip` along with the gzip-compressed payload.

**Compressed responses:** To receive gzipped responses, set the HTTP request header `Accept-Encoding: gzip` and Alpha will return gzipped responses.

**Example of a compressed request via curl:**

```sh
curl -X POST \
  -H 'Content-Encoding: gzip' \
  -H "Content-Type: application/rdf" \
  localhost:8080/mutate?commitNow=true --data-binary @mutation.gz
```

**Example of a compressed response via curl:**

```sh
curl -X POST \
  -H 'Accept-Encoding: gzip' \
  -H "Content-Type: application/dql" \
  localhost:8080/query -d $'schema {}' | gzip --decompress
```

**Example of a compressed request and response via curl:**

```sh
curl -X POST \
  -H 'Content-Encoding: gzip' \
  -H 'Accept-Encoding: gzip' \
  -H "Content-Type: application/dql" \
  localhost:8080/query --data-binary @query.gz | gzip --decompress
```

:::note
Curl has a `--compressed` option that automatically requests for a compressed response (`Accept-Encoding` header) and decompresses the compressed response:

```sh
curl -X POST --compressed -H "Content-Type: application/dql" localhost:8080/query -d $'schema {}'
```
:::

## Run a Query in JSON Format

The HTTP API also accepts requests in JSON format. For queries you have the keys "query" and "variables". The JSON format is required to set [GraphQL Variables](../dql/query/graphql-variables) with the HTTP API.

This query:

```dql
{
  users(func: anyofterms(name, "Alice Bob")) {
    uid
    name
    balance
  }
}
```

Should be escaped to this:

```sh
curl -H "Content-Type: application/json" localhost:8080/query -XPOST -d '{
  "query": "{\n users(func: anyofterms(name, \"Alice Bob\")) {\n uid\n name\n balance\n }\n }"
}' | python -m json.tool | jq
```
