---
title: Dgraph Alpha API Reference
---

Dgraph Alpha is the data plane that stores graph data and serves queries. This reference documents Alpha's HTTP and GraphQL endpoints for health monitoring and basic operations.

For architectural overview, see [Architecture](../installation/dgraph-architecture). For comprehensive admin operations like backup, export, and shutdown, see [Dgraph Administration](dgraph-administration).

## Configuration

By default, Alpha listens on `localhost` for admin actions (the loopback address only accessible from the same machine). Use the `--bindall=true` option to bind to `0.0.0.0` and allow external connections.

:::tipSet max file descriptors to a high value like 10000 if you are going to load a lot of data.:::

## HTTP Endpoints

Alpha exposes HTTP endpoints on port `8080` for monitoring and administration:

### Health Check

**`/health?all`** - Returns information about the health of all servers in the cluster.

The `/health` endpoint provides basic cluster health status. Use `/health?all` to get detailed information about all nodes.

## GraphQL Admin API

The `/admin` GraphQL endpoint provides comprehensive cluster management capabilities.

### Querying Cluster Health

You can query the `/admin` GraphQL endpoint to get detailed health information about all servers in the cluster:

```graphql
query {
  health {
    instance
    address
    version
    status
    lastEcho
    group
    uptime
    ongoing
    indexing
  }
}
```

**Response Example:**

```json
{
  "data": {
    "health": [
      {
        "instance": "zero",
        "address": "localhost:5080",
        "version": "v2.0.0-rc1",
        "status": "healthy",
        "lastEcho": 1582827418,
        "group": "0",
        "uptime": 1504
      },
      {
        "instance": "alpha",
        "address": "localhost:7080",
        "version": "v2.0.0-rc1",
        "status": "healthy",
        "lastEcho": 1582827418,
        "group": "1",
        "uptime": 1505,
        "ongoing": ["opIndexing"],
        "indexing": ["name", "age"]
      }
    ]
  }
}
```

**Response Fields:**

- **`instance`**: Name of the instance. Either `alpha` or `zero`.
- **`status`**: Health status of the instance. Either `healthy` or `unhealthy`.
- **`version`**: Version of Dgraph running the Alpha or Zero server.
- **`uptime`**: Time in nanoseconds since the Alpha or Zero server is up and running.
- **`address`**: IP_ADDRESS:PORT of the instance.
- **`group`**: Group assigned based on the replication factor.
- **`lastEcho`**: Last time, in Unix epoch, when the instance was contacted by another Alpha or Zero server.
- **`ongoing`**: List of ongoing operations in the background.
- **`indexing`**: List of predicates for which indexes are built in the background.

:::note
The same information (except `ongoing` and `indexing`) is available from the `/health` and `/health?all` HTTP endpoints.
:::

## Additional Admin Operations

For comprehensive administrative operations including:
- Backup and restore
- Data export
- Cluster shutdown and draining
- Schema management
- Security and authentication

See [Dgraph Administration](dgraph-administration).
