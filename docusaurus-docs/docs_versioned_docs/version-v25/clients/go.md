---
title: Go
---

[![GoDoc](https://pkg.go.dev/badge/github.com/dgraph-io/dgo)](https://pkg.go.dev/github.com/dgraph-io/dgo/v250)

The official Dgraph Go client communicates with the server using [gRPC](https://grpc.io/).

## Installation

```sh
go get github.com/dgraph-io/dgo/v250
```

## Supported Versions

| Dgraph version | dgo version | Import path                     |
| -------------- | ----------- | ------------------------------- |
| dgraph 23.X.Y  | dgo 230.X.Y | `github.com/dgraph-io/dgo/v230` |
| dgraph 24.X.Y  | dgo 240.X.Y | `github.com/dgraph-io/dgo/v240` |
| dgraph 25.X.Y  | dgo 250.X.Y | `github.com/dgraph-io/dgo/v250` |

## Quick Start

### Using Connection Strings (v25+)

The simplest way to connect is using a connection string:

```go
client, err := dgo.Open("dgraph://localhost:9080")
if err != nil {
    log.Fatal(err)
}
defer client.Close()
```

With ACL authentication:

```go
client, err := dgo.Open("dgraph://groot:password@localhost:9080")
```


### Running Queries and Mutations

```go
// Set schema
err := client.SetSchema(ctx, `name: string @index(exact) .`)

// Run a mutation
resp, err := client.RunDQL(ctx, `{
  set {
    _:alice <name> "Alice" .
  }
}`)

// Run a query
resp, err := client.RunDQL(ctx, `{
  alice(func: eq(name, "Alice")) {
    name
  }
}`)
fmt.Printf("%s\n", resp.Json)
```

## Multi-tenancy

In multi-tenant environments, use `LoginIntoNamespace()` to authenticate to a specific namespace:

```go
conn, err := grpc.Dial("127.0.0.1:9080", grpc.WithInsecure())
if err != nil {
    log.Fatal(err)
}
dc := dgo.NewDgraphClient(api.NewDgraphClient(conn))
ctx := context.Background()

// Login to namespace 123
if err := dc.LoginIntoNamespace(ctx, "groot", "password", 123); err != nil {
    log.Fatal(err)
}
```

Once logged in, the client can perform all operations allowed for that user in the specified namespace.

## Documentation

For complete API documentation, examples, and advanced usage:

- **[GitHub Repository](https://github.com/dgraph-io/dgo)** — Full README with all APIs and examples
- **[GoDoc Reference](https://pkg.go.dev/github.com/dgraph-io/dgo/v250)** — Complete API documentation

The GitHub README covers:
- Connection strings and advanced client creation
- Transactions (read-only, best-effort)
- Mutations (JSON and RDF formats)
- Queries with variables
- Upserts and conditional upserts
- Namespace management
- And more
