---
title: Java
---

[![Maven Central](https://img.shields.io/maven-central/v/io.dgraph/dgraph4j)](https://search.maven.org/artifact/io.dgraph/dgraph4j)

The official Dgraph Java client communicates with the server using [gRPC](https://grpc.io/).

## Installation

Via Gradle:

```groovy
implementation 'io.dgraph:dgraph4j:25.0.0'
```

Via Maven:

```xml
<dependency>
  <groupId>io.dgraph</groupId>
  <artifactId>dgraph4j</artifactId>
  <version>25.0.0</version>
</dependency>
```

## Supported Versions

| Dgraph version | dgraph4j version  | Java version |
| -------------- | ----------------- | ------------ |
| dgraph 24.X.Y  | dgraph4j 24.X.Y   | 11           |
| dgraph 25.X.Y  | dgraph4j 25.X.Y   | 11           |

## Quick Start

### Using Connection Strings (v25+)

The simplest way to connect is using a connection string:

```java
DgraphClient client = DgraphClient.open("dgraph://localhost:9080");
```

With ACL authentication:

```java
DgraphClient client = DgraphClient.open("dgraph://groot:password@localhost:9080");
```

### Running Queries and Mutations

```java
// Set schema
client.setSchema("name: string @index(exact) .");

// Run a DQL mutation
client.runDQL("{set { _:alice <name> \"Alice\" . }}");

// Run a query
Response response = client.runDQL(
    "{ alice(func: eq(name, \"Alice\")) { name } }");
System.out.println(response.getJson().toStringUtf8());

// Clean up
client.shutdown();
```

## Multi-tenancy

In multi-tenant environments, use `loginIntoNamespace()` to authenticate to a specific namespace:

```java
ManagedChannel channel = ManagedChannelBuilder
    .forAddress("localhost", 9080)
    .usePlaintext().build();
DgraphClient client = new DgraphClient(DgraphGrpc.newStub(channel));

// Login to namespace 123
client.loginIntoNamespace("groot", "password", 123);
```

Once logged in, the client can perform all operations allowed for that user in the specified namespace.

## Handling aborted transactions

When a commit aborts, the client throws a `TxnConflictException`. In addition to
the full server message, the exception exposes the [abort reason](/clients#abort-reasons)
as a typed `TxnConflictException.AbortReason`, so you can branch on *why* the
commit aborted:

```java
import io.dgraph.TxnConflictException;
import io.dgraph.TxnConflictException.AbortReason;

Transaction txn = client.newTransaction();
try {
    // ... mutations ...
    txn.commit();
} catch (TxnConflictException e) {
    switch (e.getReason()) {
        case CONFLICT:
        case STALE_STARTTS:
            // Safe to retry with a fresh transaction.
            break;
        case PREDICATE_MOVE:
            // A predicate is being moved between groups; retry after a short backoff.
            break;
        case UNKNOWN:
            // No category reported. Fall back to the message, which still explains
            // what happened. Reached against an older server, and also when a
            // current server declines to categorize a cause.
            break;
    }
    System.err.println("commit aborted: " + e.getMessage());
} finally {
    txn.discard();
}
```

`getReason()` returns `AbortReason.UNKNOWN` whenever the server reports no
category, so the code above works unchanged against older Dgraph servers — and
also against current ones, which deliberately leave some causes uncategorized
rather than implying the wrong remedy (see
[abort reasons](/clients#abort-reasons)). Always keep an `UNKNOWN` branch;
`getMessage()` still carries the explanation. An unrecognized category also
degrades to `UNKNOWN`, so a newer server can add categories without breaking
this code.

`isRetryable()` remains available for code that only needs the retry/no-retry
distinction.

## Documentation

For complete API documentation, examples, and advanced usage:

- **[GitHub Repository](https://github.com/dgraph-io/dgraph4j)** — Full README with all APIs and examples
- **[Maven Central](https://search.maven.org/artifact/io.dgraph/dgraph4j)** — Package information and releases

The GitHub README covers:
- Connection strings and advanced client creation
- Transactions (read-only, best-effort)
- Mutations (JSON and RDF formats)
- Queries with variables
- Upserts and conditional upserts
- Exception handling and automatic retry
- Namespace management and ID allocation
- TLS configuration
- Async client usage
- And more
