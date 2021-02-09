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
[Dgraph cloud services docs](https://dgraph.io/docs/slash-graphql/), or 
[Try Slash GraphQL](https://slash.dgraph.io/).

Dgraph runs on two types of server nodes, even when you are doing a proof-of-concept
deployment using a single-host setup:

* Dgraph Alpha database server: The Dgraph Alpha server nodes in your deployment host and serve data. These nodes also host an `/admin` HTTP and GRPC endpoint that can
be used for data and node administration tasks such as backup, export, draining,
and shutdown.
* Dgraph Zero management server: The Dgraph Zero nodes in your deployment control
the nodes in your Dgraph cluster. Dgraph Zero automatically moves data between different Dgraph Alpha instances based on the volume of data served by each Alpha instance.
