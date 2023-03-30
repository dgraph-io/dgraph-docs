+++
date = "2017-03-27:12:00:00Z"
title = "High Availability Replication"
weight = 85
[menu.main]
    parent = "design-concepts"
+++
## High Availability and Replication
Each Highly-Available (HA) group will be served by at least 3 instances (or two if one is temporarily unavailable). In the case of an alpha instance
failure, other alpha instances in the same group still handle the load for data in that group. In case of a zero instance failure, the remaining two zeros in the zero group will continue to hand out timestamps and perform other zero functions.

In addition, Dgraph `Learner Nodes` are alpha instances that hold replicas of data, but this replication is to suupport read replicas, often in a different geography from the master cluster. This replication is implemented the same way as HA replication, but the learner nodes do not participate in quorum, and do not take over from failed nodes to provide high availability.