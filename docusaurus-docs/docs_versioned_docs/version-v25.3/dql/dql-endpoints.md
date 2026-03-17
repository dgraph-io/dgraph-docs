---
title: Endpoints
---

Dgraph Alpha exposes endpoints for querying, mutating, and managing the database. You can interact with Dgraph using HTTP on port 8080 (plus optional port offset) or gRPC on port 9080 (plus optional port offset). Port offsets can be configured when starting Dgraph Alpha. If you're using a load balancer or reverse proxy, check your [architecture configuration](../installation/dgraph-architecture) to determine the actual endpoint addresses.

## HTTP Endpoints

Dgraph Alpha exposes the following HTTP endpoints on port `8080`:

### `/query`

Execute DQL queries.

- **Method**: `POST`
- **Content-Type**: `application/dql` or `application/json`
- **Query Parameters**:
  - `ro=true`: Execute as read-only transaction
  - `be=true`: Execute as best-effort query
  - `respFormat=rdf`: Return results in RDF format (default is JSON)

### `/mutate`

Execute DQL mutations (add, modify, or delete data).

- **Method**: `POST`
- **Content-Type**: `application/rdf` or `application/json`
- **Query Parameters**:
  - `startTs=<timestamp>`: Execute as part of an existing transaction
  - `commitNow=true`: Commit the transaction immediately after mutation

### `/commit`

Commit or abort a transaction.

- **Method**: `POST`
- **Query Parameters**:
  - `startTs=<timestamp>`: Transaction start timestamp
  - `abort=true`: Abort the transaction instead of committing

### `/alter`

Modify the DQL schema (add predicates, types, indexes, or drop schema elements).

- **Method**: `POST`
- **Content-Type**: `text/plain` (DQL schema format)

For detailed information on request/response formats, authentication, and examples, see [Raw HTTP](../clients/raw-http).

## gRPC Methods

Dgraph Alpha exposes the following gRPC methods on port `9080`:

### `Query`

Execute DQL queries. By default, returns results in JSON format. To get RDF format results, set `resp_format` to `RespFormat.RDF` in the request.

### `Mutate`

Execute DQL mutations (add, modify, or delete data).

### `Commit`

Commit or abort a transaction.

### `Alter`

Modify the DQL schema (add predicates, types, indexes, or drop schema elements).

### Protocol Buffer Definitions

The gRPC service definitions and message types are defined in the [api.proto](https://github.com/dgraph-io/dgo/blob/master/protos/api.proto) file. Refer to this file for complete method signatures, request/response message structures, and field definitions.

For detailed information on using gRPC methods, see the [Go client](../clients/go) documentation, which provides comprehensive examples of gRPC usage.

## Payload Format

The rest of the DQL documentation describes the payload format in DQL syntax. The payload content (queries, mutations, schema definitions) is the same whether you use HTTP or gRPC—only the transport protocol differs.

- **HTTP**: Send DQL payloads as request bodies with appropriate `Content-Type` headers
- **gRPC**: Send DQL payloads as protocol buffer messages

## Additional Services

In addition to DQL endpoints, Dgraph Alpha also exposes administrative services on the same ports:

For details on administrative endpoints and operations, see the [Administration](../admin/index.md) section.

