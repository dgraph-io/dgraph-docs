+++
date = "2017-03-27:12:00:00Z"
title = "Network Call Minimization"
weight = 120
[menu.main]
    parent = "design-concepts"
+++
## Network Call Minimization
Compared to RAM or SSD access, network calls are slow, so Dgraph is built from the ground up to minimize them. For graph databases which store sub-graphs on different shards, this is difficult or impossible, but predicate-based (relationship-based) sharding allows fast distributed query with Dgraph.

See [How Dgraph Minmizes Network Calls]({{< relref "minimizing-network-calls" >}}) for more details.
