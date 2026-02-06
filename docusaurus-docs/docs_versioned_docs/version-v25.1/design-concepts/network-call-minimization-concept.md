---
title: Network Call Minimization
---

Compared to RAM or SSD access, network calls are slow, so Dgraph is built from the ground up to minimize them. For graph databases which store sub-graphs on different shards, this is difficult or impossible, but predicate-based (relationship-based) sharding allows fast distributed query with Dgraph.

See [How Dgraph Minmizes Network Calls](minimizing-network-calls) for more details.
