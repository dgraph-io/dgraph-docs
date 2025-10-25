+++
date = "2020-31-08T19:35:35+11:00"
title = "Ratel UI"
description = "Ratel is a web-based tool for data visualization and cluster management designed to work with Dgraph and DQL."
type = "ratel"
weight = 1

[menu.main]
  identifier = "ratel"
  weight = 30

[menu.ratel]
  url = "/ratel/"
  identifier = "ratel"
  weight = 1
+++

Ratel is a web-based tool for data visualization and cluster management designed to work with Dgraph and DQL. You can use it for:

* **[Connect to backend]({{< relref "connection" >}})**: Manage cluster settings and connections
* **[Run DQL queries]({{< relref "console" >}})**: Execute queries and mutations with result visualization
* **[Manage schema]({{< relref "schema" >}})**: Update or replace DQL schemas and drop data
* **[Monitor cluster]({{< relref "cluster" >}})**: View cluster nodes and manage node operations
* **[Backup operations]({{< relref "backups" >}})**: Create and restore database backups

## Getting Started

Clone and build Ratel using the [instructions from the Ratel repository on GitHub](https://github.com/dgraph-io/ratel/blob/master/INSTRUCTIONS.md).
