+++
date = "2017-03-27:12:00:00Z"
title = "Group (concept)"
weight = 80
[menu.main]
    parent = "design-concepts"
+++

A group is a set of 1 or 3 or more servers that work together and have a single `leader` in the sense defined by the RAFT protocol.
## Alpha Group
An Alpha `Group` in Dgraph is a shard of data, and may or may not be highly-available (HA). An HA group typically has three Dgraph instances (servers or K8s pods), and a non-HA group is a single instance. Every Alpha instance belongs to one group, and each group is responsible for serving a
particular set of tablets (relations). In an HA configuration, the three or more instances in a single group replicate the same data to every instance to ensure redundancy of data.

In a sharded Dgraph cluster, tablets are automatically assigned to each group, and dynamically relocated as sizes change to keep the groups balanced. Predicates can also be moved manually if desired.

In a future version, if a tablet gets too big, it will be split among two groups, but currently data is balanced by moving each tablet to one group only.

To avoid confusion, remember that you may have many Dgraph alpha instances due to either sharding, or due to HA configuration. If you have both sharding and HA, you will have 3*N groups:

   config    | Non-HA            |   HA
-------------|-------------------|--------
Non-sharded  | 1 alpha total     |  3 alphas total
Sharded      | 1 alpha per group |  3*N alphas for N groups

## Zero Group
Group Zero is a lightweight server or group of servers which helps control the overall cluster. It manages timestamps and UIDs, determines when data should be rebalanced among shards, and other functions. The servers in this group are generally called "Zeros."