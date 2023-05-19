+++
title = "Dgraph Cloud Overview"
weight = 1
[menu.main]
    parent = "cloud"
+++

## Dgraph

Designed from day one to be distributed for scale and speed, **Dgraph** is the native Graph database with native GraphQL support. It is open-source, scalable, distributed, highly-available, and lightning fast.

Dgraph is different from other graph databases in a number of ways, including:

- **Distributed Scale**: &emsp; *Built from day 1 to be distributed, to handle larger data sets.*

- **GraphQL Support**: &emsp; *GraphQL is built in to make data access simple and standards-compliant. Unlike most GraphQL solutions, no resolvers are needed - Dgraph resolves queries automatically through graph navigation.*

- **Fully Transactional and ACID Compliant**: &emsp; *Dgraph satisfies demanding OLTP workloads that require frequent inserts and updates.*

- **Language support & Text Search**: &emsp; *Full-text searching is included and strings can be expressed in multiple languages*

- **Gelocation data and geo querie**: &emsp; *Dgraph can store Points and Shapes and queries can use near, within, contains, intersects geo functions*

More details at [Dgraph Database Overview]({{< relref "dgraph-overview">}})

## Dgraph Cloud 

Dgraph Cloud gives you the power of Dgraph database including performance, high-availability, horizontally-scalability and the support of GraphQL for rapid application development in a hosted and fully-managed environment. Dgraph Cloud lets you focus on building apps, not managing infrastructure.

### Dgraph Cloud Cluster Types

 - **Shared Instance**: Dgraph Cloud with [shared instances](https://cloud.dgraph.io/pricing?type=shared) is a fast and easy way to get started with GraphQL, and does not require any graph database knowledge to start and run. Shared instances run in a common database using Dgraph multi-tenancy. Your data is protected but you share resources and will have limited scale.

- **Dedicated instances** run on their own dedicated hardware to ensure consistent performance. This option extends the capabilities of the lower-cost shared instances to support enterprise, production workloads, and includes a high availability option.


## Key features

| Feature        | Notes     |
| :------------- | :------------- |
| Production-ready | Dgraph Cloud is  built to meet the needs of your business as it grows with built-in authorization, encryption at rest, TLS, incremental backups, and more. |
| Scale and expand your app without rebuilding your backend | Dgraph Cloud stores and distributes data to optimize the execution of GraphQL traversals, joins, and retrievals. Dgraph natively parses and executes GraphQL, achieving great performance and the ability to scale horizontally up to terabytes of data. |
| A high-performance, graph-first database | Dgraph Cloud runs Dgraph database, which is built to support the needs of modern apps with lightning-fast queries at any depth. |
| Custom logic | Use JavaScript to add programmatic custom logic on the backend, adding power to your apps without sacrificing client-side performance. |
| Power your app with native GraphQL support | Dgraph is built for graph data, so you don’t need to configure and maintain a cumbersome GraphQL layer over a traditional relational database. |
| Evolve your schema without downtime | When it comes time to deploy a new schema, you can do that in seconds, not hours. |
| GraphQL-based authorization and management | GraphQL is used throughout Dgraph Cloud, so you don’t need to use another tool or learn another syntax to handle user authorization or database administration tasks such as schema changes and data exports. |
| Work with the Open Source ecosystem | Because Dgraph is open-source, your app relies on a codebase that you can contribute to, not an opaque “black box”. |



## Next steps


To learn more about how Dgraph Cloud makes it easier to develop apps, create a
trial account at [Dgraph Cloud](https://cloud.dgraph.io) and try the [Introduction to GraphQL](https://dgraph.io/tour/graphqlintro/2/) tutorial to define a GraphQL schema, insert and query data in just a few minutes.

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


You might also be interested in:

- [Dgraph GraphQL Schema Reference]({{< relref "graphql/schema" >}}), which lists all the types and directives supported by Dgraph
- [Dgraph GraphQL API Reference]({{< relref "graphql-clients" >}}), which serves as a guide to using your new `/graphql` endpoint
