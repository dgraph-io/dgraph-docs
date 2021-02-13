+++
title = "Dgraph Database Overview"
description = "Introduction to Dgraph Database. Dgraph is a horizontally scalable and distributed GraphQL database that you can run on-premises, in your cloud infrastructure, or fully-managed (hosted). Learn Dgraph and GraphQL terms from our glossary."
[menu.main]
    name = "Dgraph Overview"
    identifier = "overview"
    weight = 2
+++

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


## Dgraph database and Dgraph cloud services

You can run Dgraph database in a variety of ways:

* Self-managed: You can use [Dgraph](https://dgraph.io/dgraph) on-premises, hosted on your own physical
infrastructure. You can also run Dgraph in your AWS, GCP, or Azure cloud
infrastructure.
* Fully-managed (hosted): You can use Dgraph as a fully-managed cloud service.
[Slash GraphQL](https://dgraph.io/graphql) gives you the power of Dgraph in a
hosted service running on a shared cluster. [Dgraph Cloud](https://dgraph.io/cloud)
extends Slash GraphQL to meet the needs of enterprises, and provides dedicated
clusters. To learn more, see [Fully-Managed Dgraph](#fully-managed-dgraph).

{{% notice "note" %}}
The documentation provided on [this Dgraph Docs site](https://dgraph.io/docs)
is applicable to self-managed instances of Dgraph, and also largely applicable
to Slash GraphQL and Dgraph Cloud (except for content in the [Deploy and Manage]({{< relref "/deploy" >}}) section). To learn more about Slash GraphQL and Dgraph Cloud, see
[Dgraph cloud services docs](https://dgraph.io/docs/slash-graphql).
{{% /notice %}}

### Get started with self-managed Dgraph

To run Dgraph on your own server, see [instructions for single-node setup]({{< relref "/deploy/single-host-setup" >}})
or [instructions for cluster setup]({{< relref "/deploy/multi-host-setup" >}}).

{{% notice "tip" %}}
Dgraph Labs recommends running Dgraph on Linux for production use.
{{% /notice %}}

### Get started with fully-managed Dgraph

You can [get started using Slash GraphQL today](https://slash.dgraph.io) with a
free trial. To use Dgraph Cloud, visit our [Pricing Page](https://dgraph.io/pricing) or 
[Pricing Calculator](https://slash.dgraph.io/pricing-calculator/) to get an
estimate, or [contact us](https://dgraph.io/connect).

## Dgraph and GraphQL

Because Dgraph is a native GraphQL database, queries across sparse data sets run
efficiently. As a native GraphQL database, Dgraph doesn’t have a relational
database running in the background, so your data has the ability to grow and
change with your app, without the need to add new tables. And when it comes time
to deploy a new schema, you can do that in seconds, not hours.

To learn more about Dgraph's GraphQL implementation, 
see [GraphQL Overview]({{< relref "/graphql/overview" >}}). If you are a SQL
user who is interested in learning about Dgraph and GraphQL, see:
[Dgraph for SQL Users](https://dgraph.io/learn/courses/datamodel/sql-to-dgraph/overview/introduction/).

## Fully-Managed Dgraph

[Slash GraphQL](https://dgraph.io/graphql) is a fully-managed GraphQL database
service that lets you focus on building apps, not managing infrastructure. Slash
is built from the ground up to support GraphQL, and uses a graph database
structure down to its lowest layers. So it integrates seamlessly with your
existing ecosystem of GraphQL tools.

Slash GraphQL gives you the power of Dgraph database in a hosted environment, providing
the flexibility and performance of a horizontally-scalable and distributed
GraphQL database with a graph backend, so you don’t need to configure and manage
VMs, servers, firewalls, and HTTP endpoints to power your modern apps and websites.
Slash GraphQL runs on a shared cluster so we can offer it at a low price.

To learn more about Slash GraphQL, see [Slash GraphQL Overview](https://dgraph.io/learn/courses/resources/overviews-and-glossary/overview/slash-overview/).

[Dgraph Cloud](https://dgraph.io/cloud) extends the capabilities of Slash
GraphQL to meet the heavy workloads and other needs of enterprise customers.
With Dgraph Cloud, you get dedicated cluster instances, high availability, and
the choice of running in your own virtual private cloud (VPC). You can also run
Dgraph Cloud in a bring your own Kubernetes (BYOK) environment.


## Glossary of Dgraph and GraphQL terms

| Term            |Definition	                                                   |Learn More                  |
|-----------------|--------------------------------------------------------------|----------------------------|
|Badger | A fast, open-source key-value database written in pure Go that provides the disk layer for Dgraph database.|[Badger documentation](https://dgraph.io/docs/badger)|
|data node| A basic unit of data representing an entity in a graph database. Nodes are connected by *edges* and have predicates (or *fields*) that contain node data.||
|Dgraph Alpha| A server node that serves data to clients of Dgraph database, and also provides administrator endpoints.|[Dgraph Alpha documentation]({{< relref "/deploy/dgraph-alpha" >}})|
|Dgraph database| A horizontally-scalable and distributed GraphQL database with a graph backend.	||
|Dgraph Query Language (DQL)|	A query language that extends and modifies GraphQL to support deep queries for modern apps. Formerly known as *GraphQL+-*.	|[DQL documentation]({{< relref "/dql" >}})|
|Dgraph Zero| A server node that controls a Dgraph database cluster. |[Dgraph Zero documentation]({{< relref "/deploy/dgraph-zero" >}})|
|edge|	A relationship between two data nodes in a graph database.	| |
|field|	See *predicate*.	| |
|GraphQL|	An open-source query language for APIs and a runtime for fulfilling those queries. |[Dgraph GraphQL documentation]({{< relref "/graphql/overview" >}})|
|object|	See *data node*.	| |
|server node|	A server that makes up part of a server cluster. See *Dgraph Alpha* and *Dgraph Zero*. |[Dgraph Cluster Setup documentation]({{< relref "/deploy/cluster-setup" >}}) |
|predicate|	A property of a data node in a graph database; also a discrete piece of information available to request in a graph database.	| |
|Slash GraphQL|	A fully-managed GraphQL database service powered by Dgraph database.	|[Slash GraphQL documentation]({{< relref "/slash-graphql" >}}) |

