+++
date = "2017-03-20T22:25:17+11:00"
title = "Learner Nodes"
description = "Learner nodes let you spin-up read-only replica instance to serve best-effort queries faster"
weight = 7
[menu.main]
    parent = "enterprise-features"
+++

A Learner node is an enterprise-only feature that allows a user to spin-up a read-only replica instance across the world without paying a latency cost. 
When enabled, a Dgraph cluster using learner nodes can serve best-effort queries faster.

A "learner node" can still accept write operations. The node forwards them over to the Alpha group leader and does the writing just like a typical Alpha node. It will just be slower, depending on the latency between the Alpha node and the learner node.

{{% notice "note" %}}
A learner node instance can forward `/admin` operations and perform both read and write operations,
but writing will incur in network call latency to the main cluster.
{{% /notice %}}


## Set up a Learner node

The learner node feature works at the Dgraph Alpha group level.
To use it, first you need to set up an Alpha instance as a learner node.
Once the learner instance is up, this replica can be used to run best-effort queries
with zero latency overhead. Because it's an Enterprise feature, a learner node
won't be able to connect to a Dgraph Zero node until the Zero node has a valid
license.

To spin up a learner node, first make sure that you start all the nodes, including the Dgraph Zero
leader and the Dgraph Alpha leader, with the `--my` flag so that these nodes will
be accessible to the learner node. Then, start an Alpha instance as follows:

```sh
dgraph alpha --raft="learner=true; group=N" --my <learner-node-ip-address>:5080
```

This allows the new Alpha instance to get all the updates from the group "N" leader without participating in the Raft elections.

{{% notice "note" %}}
You must specify the `--my` flag to set the IP address and port of Dgraph Zero,
the Dgraph Alpha leader node, and the learner node. If you don't, you will get
an error similar to the following: `Error during SubscribeForUpdates` 
{{% /notice %}}

## Best-effort Queries

Regular queries use the strict consistency model, and any write operation to the cluster anywhere would be read immediately.

Best-effort queries apply the eventual consistency model. A write to the cluster will be seen eventually to the node.
In regular conditions, the eventual consistency is usually achieved quickly.

A best-effort query to a learner node returns any data that is already available in that learner node.
The response is still a valid data snapshot, but at a timestamp which is not the latest one.

{{% notice "note" %}}
Best-effort queries won't be forwarded to a Zero node to get the latest timestamp.
{{% /notice %}}

You can still send typical read queries (strict consistency) to a learner node.
They would just incur an extra latency cost due to having to reach out the Zero leader.

{{% notice "note" %}}
If the learner node needs to serve normal queries, at least one Alpha leader must be available. 
{{% /notice %}}

## Use-case examples

### Geographic distribution

Consider this scenario: 

*You want to achieve low latency for clients in a remote geographical region,
distant from your Dgraph cluster.*

You can address this need by using a learner node to run best-effort queries.
This read-only replica instance can be across distant geographies and you can
use best-effort queries to get instant responses.

Because learner nodes support read and write operations, users in the remote
location can do everything with this learner node, as if they were working with
the full cluster.

<!-- commented until tested (21.07)
### Zero-downtime upgrades

Assume that you want to upgrade your cluster to the latest Dgraph version, with zero downtime even with breaking changes.

You can easily solve this with a learner node setup:
1. Bring up a learner node with the new Dgraph version.
2. Once it catches up, make the main cluster read-only (allow any last writes to catch up).
3. Bring a new cluster around the learner node (the learner needs to restart for this).
4. Redirect the traffic to the new cluster.
5. Turn off the old cluster.
-->
