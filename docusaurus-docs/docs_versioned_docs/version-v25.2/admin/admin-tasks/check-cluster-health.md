---
title: Check Cluster Health
---

You can check the health of your Dgraph cluster using HTTP endpoints or the GraphQL Admin API.

## HTTP Endpoints

Alpha exposes HTTP endpoints on port `8080` for monitoring and administration:

**`/health?all`** - Returns information about the health of all servers in the cluster.

The `/health` endpoint provides basic cluster health status. Use `/health?all` to get detailed information about all nodes.

## GraphQL Admin API

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


