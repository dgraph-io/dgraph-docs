+++
title = "Ratel Overview"
description = "Ratel is a tool for data visualization and cluster management that's designed from the ground-up to work with Dgraph. Clone and build Ratel to get started."
[menu.main]
    parent = "ratel"
    weight = 1
+++

Ratel is a tool for data visualization and cluster management that's designed
from the ground-up to work with Dgraph and [DQL]({{< relref "/query-language" >}}). You can use it for the following types of tasks:

* Connect to a backend and manage cluster settings (see [Connection]({{< relref "/ratel/connection" >}}))
* Run DQL queries and mutations, and see results (see [Console]({{< relref "/ratel/console" >}}))
* Update or replace your DQL schema, and drop data (see [Schema]({{< relref "/ratel/schema" >}}))
* Get information on cluster nodes and remove nodes (see [Cluster]({{< relref "/ratel/cluster" >}}))
* Backup your server if you are using self-managed Dgraph (see [Backup]({{< relref "/ratel/backups" >}}))

To get started with Ratel, use it online with the [Dgraph Ratel Dashboard](https://play.dgraph.io) or clone and build Ratel using the [instructions
from the Ratel repository on GitHub](https://github.com/dgraph-io/ratel/blob/master/INSTRUCTIONS.md).