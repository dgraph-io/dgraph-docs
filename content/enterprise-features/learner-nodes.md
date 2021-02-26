+++
date = "2017-03-20T22:25:17+11:00"
title = "Learner Nodes"
weight = 3
[menu.main]
    parent = "enterprise-features"
+++

A Learner node is an enterprise-only feature that allows a user to spin-up a read-only replica instance across the world without paying a latency cost. 
When enabled, a Dgraph cluster using learner nodes can serve best-effort queries faster.

The `learner` nodes can still accept `write` operations. The node would forward them over to the leader and do the writing just like a typical Alpha node. It would just be slower depending on the latency between the Alpha node and the learner node.

{{% notice "note" %}}
A `learner` node instance can forward `/admin` operations and perform both `read`/`write` operations,
but writing will incur in network call latency to the main cluster.
{{% /notice %}}


## Set up a Learner node

The learner node feature works at the Dgraph Alpha group level.
To use it, first you need to set up an Alpha instance as a `learner` node.
Once the learner instance is up, this replica can be used to run best-effort queries with zero latency overhead.

To spin up a `learner` node, start an Alpha instance with:

```sh
dgraph alpha --raft="learner=true; group=N"
```

This would make the new Alpha instance to get all the updates from the group `N` leader without participating in the Raft elections.

{{% notice "note" %}}
Since it's an Enterprise feature, a `learner` node won't be able to connect to a Dgraph Zero until the Zero server has a valid license.
{{% /notice %}}

## Best-effort Queries

Regular queries use the strict consistency model, and any write operation to the cluster anywhere would be read immediately.

Best-effort queries apply the eventual consistency model. A write to the cluster will be seen eventually to the node.
In regular conditions, the eventual consistency is usually achieved quickly.

A best-effort query to a `learner` node returns any data that is already available in that learner node.
The response is still a valid snapshot of data, but at a timestamp which is not the latest one.

You can still send typical `read` queries (strict consistency) to a `learner` node.
They would just incur an extra latency cost due to having to reach out the Zero leader.

{{% notice "note" %}}
Best-effort queries won't be forwarded to a Zero node to get the latest timestamp.
{{% /notice %}}

## Use-case examples

### Geographic distribution

Consider this scenario: 
- you want to achieve low latency for clients in a remote geographical region, distant from your Dgraph cluster.

You can solve it by using a `learner` node to run best-effort queries.
This read replica instance could be across distant geographies and you can use best-effort queries to get instant responses.

Since a `learner` node supports read and write operations, users in the remote location can do everything with this replica node,
as if they were working the full cluster.


### Datacenter to Datacenter

Another use case example is using a `learner` node for Data-Center to Data-Center replication.

Let's take for example this DC scenario:
- A Dgraph cluster in the US-west.
- A `learner` read replica for each group in the US-east.

In case the US-west Datacenter goes down, you could quickly bring up a new cluster in the US-east using the `learner` node data available.


### Zero downtime upgrades

Assume that you want to upgrade your cluster to the latest Dgraph version, with zero downtime even with breaking changes.

You can easily solve this with a `learner` node setup:
- Bring up a `learner` node with the new Dgraph version.
- Once it catches up, make the main cluster read-only (allow any last writes to catch up).
- Bring a new cluster around the `learner` node (the `learner` needs to restart for this).
- Redirect the traffic to the new cluster.
- Turn off the old cluster.
