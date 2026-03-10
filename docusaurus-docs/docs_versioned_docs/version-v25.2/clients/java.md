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
