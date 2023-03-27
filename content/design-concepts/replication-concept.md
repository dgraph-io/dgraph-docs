+++
date = "2017-03-27:12:00:00Z"
title = "High Availability Replication (concept)"
weight = 170
[menu.main]
    parent = "design-concepts"
+++
## High Availability and Replication
Each Highly-Available (HA) group will be served by at least 3 servers (or two if one is temporarily unavailable). In the case of an alpha instance
failure, other servers in the same group still handle the load for data in that group. In case of a zero instance failure, the remaining two zeros will continue to hand out timestamps and perform other zero functions.

In addition, Dgraph `Learner Nodes` hold replicas of data, but this replication is to suupport read replicas, typically in a different geography from the master cluster. This replication is implemented the same way as HA replication, but the learner nodes do not participate in quorum, and do not take over from failed nodes to provide high availability.