---
title: Python
---

[![PyPI](https://img.shields.io/pypi/v/pydgraph)](https://pypi.org/project/pydgraph/)

The official Dgraph Python client communicates with the server using [gRPC](https://grpc.io/).

## Installation

```sh
pip install pydgraph
```

## Supported Versions

| Dgraph version | pydgraph version |
| -------------- | ---------------- |
| dgraph 21.03.X | pydgraph 21.03.X |
| dgraph 23.0.X  | pydgraph 23.0.X  |
| dgraph 24.X.Y  | pydgraph 24.X.Y  |
| dgraph 25.X.Y  | pydgraph 25.X.Y  |

## Quick Start

### Using Connection Strings (v25+)

The simplest way to connect is using a connection string:

```python
import pydgraph

client = pydgraph.open("dgraph://localhost:9080")
```

With ACL authentication:

```python
client = pydgraph.open("dgraph://groot:password@localhost:9080")
```

### Running Queries and Mutations

```python
import pydgraph
import json

# Create client
client = pydgraph.open("dgraph://localhost:9080")

# Set schema
op = pydgraph.Operation(schema='name: string @index(exact) .')
client.alter(op)

# Run a mutation
txn = client.txn()
try:
    txn.mutate(set_obj={'name': 'Alice'}, commit_now=True)
finally:
    txn.discard()

# Run a query
query = '{ alice(func: eq(name, "Alice")) { name } }'
res = client.txn(read_only=True).query(query)
print(json.loads(res.json))

# Clean up
client.close()
```

## Multi-tenancy

In multi-tenant environments, use `login_into_namespace()` to authenticate to a specific namespace:

```python
client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)

# Login to namespace 123
client.login_into_namespace("groot", "password", "123")
```

Once logged in, the client can perform all operations allowed for that user in the specified namespace.

## Handling aborted transactions

When a commit aborts, the client raises `pydgraph.AbortedError`. In addition to
the full server message, the error exposes the [abort reason](/clients#abort-reasons)
as a typed `pydgraph.AbortReason`, so you can branch on *why* the commit aborted:

```python
import pydgraph

txn = client.txn()
try:
    txn.mutate(set_obj={"name": "Alice"})
    txn.commit()
except pydgraph.AbortedError as e:
    if e.reason in (pydgraph.AbortReason.CONFLICT, pydgraph.AbortReason.STALE_STARTTS):
        # Safe to retry with a fresh transaction.
        ...
    elif e.reason == pydgraph.AbortReason.PREDICATE_MOVE:
        # A predicate is being moved between groups; retry after a short backoff.
        ...
    else:  # pydgraph.AbortReason.UNKNOWN
        # No category reported. Fall back to the message, which still explains
        # what happened. Reached against an older server, and also when a
        # current server declines to categorize a cause.
        ...
    print("commit aborted:", e)
finally:
    txn.discard()
```

`AbortedError.reason` is `pydgraph.AbortReason.UNKNOWN` whenever the server
reports no category, so the code above works unchanged against older Dgraph
servers — and also against current ones, which deliberately leave some causes
uncategorized rather than implying the wrong remedy (see
[abort reasons](/clients#abort-reasons)). Always keep the `UNKNOWN` branch; the
message still carries the explanation. An unrecognized category also degrades to
`UNKNOWN`, so a newer server can add categories without breaking this code.

## Documentation

For complete API documentation, examples, and advanced usage:

- **[GitHub Repository](https://github.com/dgraph-io/pydgraph)** — Full README with all APIs and examples
- **[PyPI Package](https://pypi.org/project/pydgraph/)** — Package information and releases

The GitHub README covers:
- Connection strings and client creation
- Transactions (read-only, best-effort)
- Mutations (JSON and RDF formats)
- Queries with variables
- Upserts and conditional upserts
- Async/await support
- TLS configuration
- And more
