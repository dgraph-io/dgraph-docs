+++
title = "Dgraph Cloud Overview"
weight = 1
[menu.main]
    parent = "cloud"
+++

Dgraph Cloud, powered by Dgraph database, is a fully-managed GraphQL database
service that lets you focus on building apps, not managing infrastructure. Dgraph
Cloud is built from the ground up to support GraphQL, and uses a graph database
structure down to its lowest layers. So, it integrates seamlessly with your
existing ecosystem of GraphQL tools.

Dgraph Cloud gives you the power of Dgraph database in a hosted environment,
providing the flexibility and performance of a horizontally-scalable and
distributed GraphQL database with a graph backend. With Dgraph Cloud, you
don’t need to configure and manage VMs, servers, firewalls, and HTTP endpoints
to power your modern apps and websites.

Dgraph Cloud is available in several pricing tiers:

* **Free**: This tier is suitable for hobbyist use and evaluation, but has significant bandwidth limitations.
* **Shared Instances** (formerly *Slash GraphQL*): Backends in this tier run on a shared server cluster to provide a graph database service at a low price.
* **Dedicated Instances**: Backends in this tier run on dedicated server clusters to meet the heavy workloads and other needs of enterprise customers. This tier also provides high availability and the option to run Dgraph in your own virtual private cloud (VPC) or bring your own Kubernetes (BYOK) environment.

To learn more about pricing for each tier, see the [Dgraph Pricing Page](https://dgraph.io/pricing).
To learn more about Dgraph database, see [Dgraph Database Overview]{{< relref "dgraph-overview.md">}}).

{{% notice "tip" %}}
You can check which Dgraph database release version is running on your Dgraph Cloud backend in [Dgraph Cloud Settings](https://cloud.dgraph.io/_/settings).
{{% /notice %}}

## Key features

| Feature        | Notes     |
| :------------- | :------------- |
| Production-ready | Dgraph Cloud is great for small app developers but is also built to meet the needs of your business as it grows with built-in authorization, encryption at rest, TLS, incremental backups, and more. |
| Scale and expand your app without rebuilding your backend | Dgraph Cloud stores and distributes data to optimize the execution of GraphQL traversals, joins, and retrievals. Dgraph natively parses and executes GraphQL, achieving great performance and the ability to scale horizontally up to terabytes of data. |
| A high-performance, graph-first database | Dgraph Cloud runs Dgraph database, which is built to support the needs of modern apps with lightning-fast queries at any depth. |
| Custom logic | Use JavaScript to add programmatic custom logic on the backend, adding power to your apps without sacrificing client-side performance. |
| Power your app with native GraphQL support | Dgraph is built for graph data, so you don’t need to configure and maintain a cumbersome GraphQL layer over a traditional relational database. |
| Evolve your schema without downtime | When it comes time to deploy a new schema, you can do that in seconds, not hours. |
| GraphQL-based authorization and management | GraphQL is used throughout Dgraph Cloud, so you don’t need to use another tool or learn another syntax to handle user authorization or database administration tasks such as schema changes and data exports. |
| Work with the Open Source ecosystem | Because Dgraph is open-source, your app relies on a codebase that you can contribute to, not an opaque “black box”. |

## Architecture

Dgraph Cloud runs Dgraph database in a fully-managed service, so you don't need
to manage servers or VM. Dgraph Cloud provides a truly distributed database that shards and
replicates data across cluster nodes, providing a scalable and production-ready
database solution for your app.

Behind the scenes, Dgraph Cloud instances run as as clusters of Dgraph Zero and
Dgraph Alpha server nodes.

*  Dgraph Zero nodes control the cluster. This includes storing information
   about the cluster and moving data between Dgraph Alpha nodes to re-balance
   based on transactional workloads.
*  Dgraph Alpha nodes serve data to clients, and also provide administrator
   endpoints.

To learn more about the Dgraph clusters that power Dgraph Cloud, see
[Understanding Dgraph Cluster]({{< relref "cluster-setup.md#understanding-dgraph-cluster" >}}).

## Next steps

To learn more about how Dgraph Cloud makes it easier to develop apps, create a
trial account and [try Dgraph Cloud](https://cloud.dgraph.io) for yourself.

## Recommended Reading

Please see the following topics to learn more about how to use Dgraph Cloud:

- The [Quick Start]({{< relref "cloud-quick-start" >}}) will help you get started with a Dgraph Cloud Schema, starting with a multi tenant to-do app
- [Administering your Backend]({{< relref "admin/_index.md" >}}) covers topics such as how to programmatically set your schema, and import or export your data
  - [Authentication]({{< relref "admin/authentication" >}}) will guide you in creating a API token. Since all admin APIs require an auth token, this is a good place to start.
  - [Schema]({{< relref "admin/schema" >}}) describes how to programmatically query and update your GraphQL schema.
  - [Import and Exporting Data]({{< relref "admin/import-export" >}}) is a guide for exporting your data from a Dgraph Cloud backend, and how to import it into another cluster
  - [Dropping Data]({{< relref "admin/drop-data" >}}) will guide you through dropping all data from your Dgraph Cloud backend.
  - [Switching Schema Modes]({{< relref "admin/schema-modes" >}}) will guide you through changing Dgraph Cloud schema mode.
- [Dgraph Cloud API]({{< relref "cloud-api/overview" >}}) Dgraph Cloud now includes a API so you can programmatically manage your backends
- [Schema]({{< relref "cloud-api/schema" >}}) lists commands related to schema.
- [Advanced Queries With DQL]({{< relref "advanced-queries" >}}) covers interacting with your database using the gRPC endpoint.

You might also be interested in:

- [Dgraph GraphQL Schema Reference]({{< relref "graphql/schema" >}}), which lists all the types and directives supported by Dgraph
- [Dgraph GraphQL API Reference]({{< relref "graphql/api" >}}), which serves as a guide to using your new `/graphql` endpoint
