+++
title = "Deployment and Management Overview"
description = "Deploy and manage Dgraph database in your physical or cloud infrastructure."
weight = 1
[menu.main]
    parent = "deploy"
+++

You can deploy and manage Dgraph database in a variety of self-managed deployment scenarios, including:

* Running Dgraph on your on-premises infrastructure (bare-metal physical servers)
* Running Dgraph on your cloud infrastructure (AWS, GCP and Azure)

This section focuses exclusively on deployment and management for these self-managed
scenarios. To learn about fully-managed options that let you focus on
building apps and websites, rather than managing infrastructure, see the 
[Dgraph cloud services docs](https://dgraph.io/docs/cloud/), or 
[Try Dgraph Cloud](https://cloud.dgraph.io/).

A Dgraph cluster consists of the following:

* **Dgraph Alpha database server nodes**: The Dgraph Alpha server nodes in your deployment host and serve data. These nodes also host an `/admin` HTTP and GRPC endpoint that can
be used for data and node administration tasks such as backup, export, draining,
and shutdown.
* **Dgraph Zero management server nodes**: The Dgraph Zero nodes in your deployment control
the nodes in your Dgraph cluster. Dgraph Zero automatically moves data between different Dgraph Alpha instances based on the volume of data served by each Alpha instance.

You need at least one node of each type to run Dgraph. You need three nodes of
each type to run Dgraph in a high-availability (HA) cluster configuration. To
learn more about 2-node and 6-node deployment options, see the [Production Checklist]({{< relref "deploy/production-checklist.md" >}}).
