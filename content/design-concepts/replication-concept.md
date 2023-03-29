
## High Availability and Replication
Each Highly-Available (HA) group will be served by at least 3 servers (or two if one is temporarily unavailable). In the case of a machine
failure, other servers serving the same group still handle the load for data in the group.

In addition, Dgraph `Learner Nodes` hold replicas of data, but this replication is to suupport read replicas, typically in a different geography from the master cluster. This replication is independent of HA replication.