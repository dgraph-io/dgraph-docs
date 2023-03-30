+++
date = "2017-03-27:12:00:00Z"
title = "Discovery"
weight = 30
[menu.main]
    parent = "design-concepts"
+++

## New Servers and Discovery
Dgraph clusters will detect new machines allocated to the [cluster]({{< relref "deploy/cluster-setup.md" >}}),
establish connections, and transfer data to the new server based on the group the new machine is in.
