+++
title = "Dgraph Database Overview"
description = "Introduction to Dgraph Database. Dgraph is a horizontally scalable and distributed GraphQL database that you can run on-premises, in your cloud infrastructure, or fully-managed (hosted). Learn Dgraph and GraphQL terms from our glossary."
[menu.main]
    name = "Dgraph Overview"
    identifier = "overview"
    weight = 2
+++

{{% notice "tip" %}}
Dgraph Cloud currently runs release v20.11. To see docs for that release, select
**v20.11** from the drop-down on this page, or [click here](https://dgraph.io/docs/v20.11/dgraph-overview/).
{{% /notice %}}

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


## Dgraph database and Dgraph Cloud

You can run Dgraph database in a variety of ways:

* Self-managed: You can use [Dgraph](https://dgraph.io/dgraph) on-premises, hosted on your own physical
infrastructure. You can also run Dgraph in your AWS, GCP, or Azure cloud
infrastructure.
* Fully-managed (hosted): Dgraph Cloud provides Dgraph as a fully-managed cloud
service. Dgraph Cloud [Shared Instances](https://dgraph.io/graphql) (formerly called *Slash GraphQL*)
give you the power of Dgraph in a low-cost hosted service running on a shared cluster.
Dgraph Cloud [Dedicated Instances](https://dgraph.io/cloud) provide an enterprise-grade
service that runs on dedicated cluster instances. To learn more, see [Fully-Managed Dgraph](#fully-managed-dgraph).

{{% notice "note" %}}
The documentation provided on [this Dgraph Docs site](https://dgraph.io/docs)
is applicable to self-managed instances of Dgraph, and also largely applicable
to Dgraph Cloud (except for content in the [Deploy and Manage]({{< relref "/deploy/overview" >}}) section). To learn more about Dgraph Cloud and Dgraph Cloud, see
[Dgraph cloud services docs](https://dgraph.io/docs/cloud).
{{% /notice %}}

### Get started with self-managed Dgraph

To run Dgraph on your own server, see [instructions for single-node setup]({{< relref "/deploy/single-host-setup" >}})
or [instructions for cluster setup]({{< relref "/deploy/multi-host-setup" >}}).

{{% notice "note" %}}
Dgraph is designed to run on Linux. As of release v21.03, Dgraph no longer
supports installation on Windows or macOS. We recommend using the standalone
Docker image to try out Dgraph on Windows or macOS.
{{% /notice %}}

#### To run Dgraph using the standalone Docker image

1. Download docker: https://www.docker.com/
2. Create a folder to store Dgraph data outside of the container, as follows: `mkdir -p ~/dgraph`
3. Get the Docker standalone image, as follows: `docker pull dgraph/standalone`
4. Run the Dgraph Docker standalone image, as follows:

```sh
  docker run -it -p 5080:5080 -p 6080:6080 -p 8080:8080 -p 9080:9080 -p 8000:8000 -v ~/dgraph:/dgraph --name dgraph dgraph/standalone:v21.03.0
```  

{{% notice "tip" %}}
To run the Docker standalone image for another version of Dgraph, change `v21.03.0`
in the command shown above to the version number for a previous release, such as `v20.11.0`.
{{% /notice %}}

After following these steps, Dgraph Alpha now runs and listens for HTTP requests
on port 8080, and Ratel listens on port 8000.

### Get started with fully-managed Dgraph

You can [get started with Dgraph Cloud](https://cloud.dgraph.io) today with a
free trial. To use Dgraph Cloud, visit our [Pricing Page](https://dgraph.io/pricing) or 
[Pricing Calculator](https://cloud.dgraph.io/pricing-calculator/) to get an
estimate, or [contact us](https://dgraph.io/connect).

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

## Fully-Managed Dgraph

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

## Glossary of Dgraph and GraphQL terms

| Term            |Definition	                                                   |Learn More                  |
|-----------------|--------------------------------------------------------------|----------------------------|
|Dgraph Cloud|	A fully-managed GraphQL database service powered by Dgraph database.	|[Dgraph Cloud documentation](https://dgraph.io/docs/cloud) |
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
|superflag|	A Dgraph CLI flag that contains one or more options used to specify command settings. |[Dgraph Cluster Setup documentation]({{< relref "/deploy/cli-command-reference" >}}) |
|predicate|	A property of a data node in a graph database; also a discrete piece of information available to request in a graph database.	| |
