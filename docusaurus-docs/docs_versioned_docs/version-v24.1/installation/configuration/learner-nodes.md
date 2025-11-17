---
title: Learner Nodes
description: Deploy read-only replica instances for low-latency best-effort queries in remote geographic regions
---
:::note
**Enterprise Feature**: Learner nodes require a Dgraph Enterprise license. See [License](../../admin/enterprise-features/license) for details.
:::

Learner nodes are read-only replica instances that serve best-effort queries with zero latency overhead. Use learner nodes to provide low-latency access for clients in remote geographic regions distant from your main Dgraph cluster.

A learner node receives all updates from its Alpha group leader without participating in Raft elections. It can accept read and write operations, but write operations are forwarded to the Alpha group leader and incur network latency to the main cluster.

## Best-Effort Queries

Best-effort queries use eventual consistency and return data available on the learner node at a timestamp that may not be the latest. They do not contact Zero nodes to get the latest timestamp, providing instant responses for geographically distributed clients.

You can also send strict consistency queries to a learner node, but these incur additional latency as they must reach the Zero leader. At least one Alpha leader must be available for the learner node to serve normal queries.

## Setup

Start all nodes (Dgraph Zero leader and Dgraph Alpha leader) with the `--my` flag so they are accessible to the learner node. Then start an Alpha instance as a learner node:

```sh
dgraph alpha --raft="learner=true; group=N" --my <learner-node-ip-address>:5080
```

This creates a replica that receives updates from group "N" leader without participating in Raft elections.

:::note
You must specify the `--my` flag for Dgraph Zero, the Dgraph Alpha leader, and the learner node. Omitting it results in an error: `Error during SubscribeForUpdates`.
:::
