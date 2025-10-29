+++
date = "2017-03-20T22:25:17+11:00"
title = "Self-managed cluster"
weight = 9
type = "docs"
aliases = ["/deploy/overview"]
[menu.main]
  identifier = "deploy"
+++

You can deploy and manage Dgraph database in a variety of self-managed deployment scenarios.


A Dgraph cluster consists of the following:

* **Dgraph Alpha database server nodes**: The Dgraph Alpha server nodes in your deployment host and serve data. These nodes also host an `/admin` HTTP and GRPC endpoint that can
be used for data and node administration tasks such as backup, export, draining,
and shutdown.
* **Dgraph Zero management server nodes**: The Dgraph Zero nodes in your deployment control
the nodes in your Dgraph cluster. Dgraph Zero automatically moves data between different Dgraph Alpha instances based on the volume of data served by each Alpha instance.

You need at least one node of each type to run Dgraph. You need three nodes of
each type to run Dgraph in a high-availability (HA) cluster configuration. To
learn more about 2-node and 6-node deployment options, see the [Production Checklist]({{< relref "installation/production-checklist.md" >}}).

