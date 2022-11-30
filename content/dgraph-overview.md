+++
title = "Dgraph Database Overview"
description = "Introduction to Dgraph Database. Dgraph is a horizontally scalable and distributed GraphQL database that you can run on-premises, in your cloud infrastructure, or fully-managed (hosted)."
[menu.main]
    name = "Dgraph Overview"
    identifier = "overview"
    weight = 2
+++
# <span style="color:red">WORK IN PROGRESS</span>
## Dgraph


Designed from the ground up to be run in production, **Dgraph** is the native GraphQL database with a graph backend. It is open-source, scalable, distributed, highly available and lightning fast.

## Hosting options

### Basic architecture
Dgraph cluster consists of different nodes (Zero, Alpha), and each node serves a
different purpose.

- **Dgraph Zero** controls the Dgraph cluster, assigns servers to a group,
and re-balances data between server groups.

- **Dgraph Alpha** hosts predicates and indexes. Predicates are either the properties
associated with a node or the relationship between two nodes. Indexes are the tokenizers
that can be associated with the predicates to enable filtering using appropriate functions.

- **Ratel** serves the UI to run queries, mutations & altering schema.

You need at least one Dgraph Zero and one Dgraph Alpha to get started.
## Who is using Dgraph & How
Dgraph is a horizontally scalable and distributed GraphQL database with a graph
backend. Dgraph is built for the heavy transactional workloads required to
power modern apps and websites, but it isn’t limited to only these types of
applications. Whether you are looking to power the backend of your app, create
elastic search for your website, or build a new database purely for data
analysis, Dgraph is up to the task. In fact, it is in production today in
the following real-world scenarios:

* [Data unification](https://dgraph.io/capventis)
* Customer 360
* Social media sites
* Content Management Systems
* Ecommerce stores
* [Entity resolution](https://dgraph.io/blog/post/introducing-entity-resolution/)
* HR management applications
* Master data management
* Product recommendation engines
* Real-time chat applications

To learn more about how organizations are using Dgraph, see
[Dgraph Case Studies](https://dgraph.io/case-studies).

## Edges

Typical data format is RDF [N-Quad](https://www.w3.org/TR/n-quads/) which is:

* `Subject, Predicate, Object, Label`, aka
* `Entity, Attribute, Other Entity / Value, Label`

Both the terminologies get used interchangeably in our code. Dgraph considers edges to be directional,
i.e. from `Subject -> Object`. This is the direction that the queries would be run.

{{% notice "tip" %}}Dgraph can automatically generate a reverse edge. If the user wants to run
queries in that direction, they would need to define the [reverse edge]({{< relref "query-language/schema.md#reverse-edges" >}})
as part of the schema.{{% /notice %}}


## Dgraph database and Dgraph Cloud

You can run Dgraph database in a variety of ways:

* Fully-managed (hosted): Dgraph Cloud provides Dgraph as a fully-managed cloud
service. Dgraph Cloud [Shared Instances](https://dgraph.io/graphql) (formerly called *Slash GraphQL*)
give you the power of Dgraph in a low-cost hosted service running on a shared cluster.
Dgraph Cloud [Dedicated Instances](https://dgraph.io/cloud) provide an enterprise-grade
service that runs on dedicated cluster instances. To learn more, see [Fully-Managed Dgraph](#fully-managed-dgraph).
* Self-managed: You can use [Dgraph](https://dgraph.io/dgraph) on-premises, hosted on your own physical
infrastructure. You can also run Dgraph in your AWS, GCP, or Azure cloud
infrastructure.

{{% notice "note" %}}
The documentation provided on [this Dgraph Docs site](https://dgraph.io/docs)
is applicable to self-managed instances of Dgraph, and also largely applicable
to Dgraph Cloud (except for content in the [Deploy and Manage]({{< relref "/deploy/overview" >}}) section). To learn more about Dgraph Cloud, see
[Dgraph cloud services docs](https://dgraph.io/docs/cloud).
{{% /notice %}}

## Dgraph Cloud

Dgraph Cloud with [shared instances](https://dgraph.io/graphql) is a
fully-managed GraphQL database service that lets you focus on building apps, not
managing infrastructure. Dgraph Cloud is built from the ground up to support
GraphQL, and uses a graph database structure down to its lowest layers. So it
integrates seamlessly with your existing ecosystem of GraphQL tools.

Dgraph Cloud gives you the power of Dgraph database in a hosted environment,
providing the flexibility and performance of a horizontally-scalable and distributed
GraphQL database with a graph backend, so you don’t need to configure and manage
VMs, servers, firewalls, and HTTP endpoints to power your modern apps and websites.
Dgraph Cloud with shared instances runs on a shared cluster so we can offer it
at a low price. To learn more about Dgraph Cloud, see [Dgraph Cloud Overview](https://dgraph.io/docs/cloud/introduction).

Dgraph Cloud with [dedicated instances](https://dgraph.io/cloud) extends the
capabilities of the lower-cost shared instances offering to meet the heavy workloads
and other needs of enterprise customers. With Dgraph Cloud, you get dedicated cluster
instances, high availability, and the option to run Dgraph in your own virtual
private cloud (VPC) or bring your own Kubernetes (BYOK) environment.

## Get started






## Dgraph and GraphQL

Because Dgraph is a native GraphQL database, queries across sparse data sets run
efficiently. As a native GraphQL database, Dgraph doesn’t have a relational
database running in the background, so your data has the ability to grow and
change with your app, without the need to add new tables. And when it comes time
to deploy a new schema, you can do that in seconds, not hours.

To learn more about Dgraph's GraphQL implementation,
see [GraphQL Overview]({{< relref "/graphql/overview" >}}). If you are a SQL
user, see:
[Dgraph for SQL Users](https://dgraph.io/learn/courses/datamodel/sql-to-dgraph/overview/introduction/).

## What's next
- get familiar with some terms in our [Glossary](/dgraph-glossary)
- GraphQL tutorial
