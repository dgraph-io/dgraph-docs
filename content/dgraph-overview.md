+++
title = "Dgraph Database Overview"
description = "Introduction to Dgraph Database. Dgraph is a horizontally scalable and distributed graph database that supports GraphQL natively. You can run Dgraph on-premise, in your cloud infrastructure, or as a service fully-managed by Dgraph."
[menu.main]
    name = "Dgraph Overview"
    identifier = "overview"
    weight = 2
+++
# <span style="color:red">WORK IN PROGRESS</span>
## Dgraph


Designed from the ground up to be distributed for scale and speed, **Dgraph** is the native Graph database with native GraphQL support. It is open-source, scalable, distributed, highly-available and lightning fast.

Dgraph is different from other graph databases in a number of ways

| | |
|:----|:----|
| **Distributed Scale**   |  Built from day 1 to be distributed, to handle larger data sets |
| **GraphQL Support** |  GraphQL is built in to make data access simple and standards-compliant. Unlike most GraphQL solutions, no resolvers are needed - Dgraph resolves queries automatically through graph navigation |
| **True Free Open Source Software (FOSS)**  | Dgraph is free to use, and [available on github](https://github.com/dgraph-io/dgraph) |
| **Fully Transactional and ACID Compliant** | Satisfy demanding OLTP workloads that require frequent inserts and updates  |
| **Full Text Search**  | Full-text searching is included in query options |
## Who is using Dgraph & How
Dgraph is a horizontally scalable and distributed graph database with native GraphQL support. Querying across links in a social netowrk, or detecting networks of interconnected fraudsters in a fraud application are natural graph use cases.

Graph databases are ideal when relationships and connections really matter. In SQL or most NoSQL platforms relationships are slow to query and inconvenient to model, requiring join tables and extra primary and foreign keys. Dgraph is the best graph database when ease-of-use or massive scale are key.


To get a sample of production use of Dgraph you can dig into the following real-world scenarios:

* [Data unification](https://dgraph.io/case-studies/factset/)
* [Customer 360](https://dgraph.io/capventis)
* [Fraud detection](https://www.youtube.com/watch?v=rAuDfb1dhl0)
* Content Management Systems
* Ecommerce stores
* [Entity resolution](https://dgraph.io/blog/post/introducing-entity-resolution/)
* HR management applications
* Master data management (MDM)
* Product recommendation engines
* Real-time chat applications
* [Logistics] (https://dgraph.io/case-studies/ke-holdings/)

To learn more about how organizations are using Dgraph, read more
[Dgraph Case Studies](https://dgraph.io/case-studies).

## GraphQL in Dgraph
In Dgraph, GraphQL is not an afterghtough or an add-on; it is core to the product. GraphQL allows developers to get started immediately - simply define a schema and Dgraph automatically builds out CRUD and query APIs. Dgraph works as a standards-compliant GraphQL server, so many web and app developers may not know (or care) that Dgraph is a powerful graph database as well.

The big time savings is that there are no resolvers needed to get started. All GraphQL fields are "resolved" simply by following a graph database edge to the required field. 

For some custom queries that the GraphQL specification cannot support, Dgraph provides an extension of pure GraphQL called "DQL." Between the two languages, all data is easily and efficiently updated and accessed.

## Database expert use vs GraphQL app developer use
Dgraph is ideal for both graph database experts and users who prefer to be insulated from graph database details by using GraphQL. 

### Database experts
Database experts using graph databases need a simple languge to query networked or interconnected data, and expect those qeries to scale well. These users work on systems such as data fabrics or data hubs which combine data from many sources, or innovative systems pushing the boundaries beyond what SQL and other slow-joining technologies can do.

### GraphQL users
GraphQL users may still be database experts, but are focused on providing easy, fast and flexible access to data. GraphQL allows people to specify the "shape" and "extent" of data to retreive from a database as a JSON-like skeleton. Then Dgraph does the rest of the work. By specifying the data in the request, GraphQL developers get only the data they need and want, without writing custom REST services, or worrying about over- and under-fetching. 

Read more about the motivations for GraphQL in [the original annoucement of the spec from Facebook](https://engineering.fb.com/2015/09/14/core-data/graphql-a-data-query-language/).
## Hosting options
Dgraph provides a "Graph as a Service" severless database. [Click here to get started in minutes](https://cloud.dgraph.io/). This is the fastest and easiest way to get started with Dgraph, and is recommended since it includes hosting, monitoring and provisioning from the Dgraph team.

For organizations who require or prefer to keep data on premise, or in cloud-based Ubuntu servers they provision themselves, dgraph can also be downloaded and installed on any Ubuntu Linux machine or image.

### Internal architecture
Dgraph scales to greater data sizes than other graph databases becuase it is designed from the groud up to be distributed. Therefore Dgraph runs as a cluster of server nodes which communicate to form a single logical data store. There are two types of processes (nodes) running: Zeros and Alphas.

(Terminology note: The word "node" is ambiguous and can refer to a server in a network of collaborating servers that form a databse, or to a piece of data in a graph database. We will use "server node" for servers and "data node" for data element here.)

- **Dgraph Zero** server nodes control the Dgraph cluster, assign servers to a group, coordinate distributed transactions,
and re-balance data among server groups.

- **Dgraph Alpha** server nodes stores the graph data. Unlike non-distributed graph databases, Dgraph alphas store and index "predicates" which represent the relations among data nodes. Predicates are either the properties
associated with a data node or the relationship between two nodes. Indexes speed up certain queries.

- **GraphQL IDEs** a number of GraphQL IDEs are available to update GraphQL schemas and run GraphQL updates and queries. [One of these IDEs is GrahpiQL](https://github.com/graphql/graphiql)

- **Ratel** a Dgraph UI that runs DQL queries, mutations & allows schema editing. 


You need at least one Dgraph Zero and one Dgraph Alpha to get started.


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
