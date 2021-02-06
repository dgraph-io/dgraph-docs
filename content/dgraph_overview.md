+++
title = "Dgraph Database Overview"
description = "Dgraph is a horizontally scalable and distributed GraphQL database that you can run on-prem, in your cloud infrastructure, or fully-managed. Learn Dgraph and GraphQL terms from our glossary."
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

* HR management applications
* Social media sites
* Ecommerce stores
* Content Management Systems
* Product recommendation engines
* Real-time chat applications 

## Dgraph database and Dgraph cloud services

You can run Dgraph database in a variety of ways:

* Self-managed: You can use Dgraph on-premises, hosted on your own physical
infrastructure. You can also run Dgraph in your AWS, GCP, or Azure cloud
infrastructure.
* Fully-managed (hosted): You can use Dgraph as a fully-managed cloud service.
 Slash GraphQL gives you the power of Dgraph in a hosted service. Dgraph Cloud
extends Slash GraphQL to meet the needs of enterprises. 

**Note**: The documentation provided on this site (dgraph.io/docs) is applicable to
self-managed instances of Dgraph, and also largely applicable to Slash GraphQL 
and Dgraph Cloud (except for content about managing server clusters in the
[Deploy](/deploy) section).

### Get started with self-managed Dgraph

To run Dgraph on your own server, see [instructions for single-node setup](/deploy/single-host-setup/)
or [instructions for cluster setup](/deploy/multi-host-setup/).

{{% notice "tip" %}}
Dgraph Labs recommends running Dgraph on Linux for production use.
{{% /notice %}}

### Get started with hosted Dgraph

You can [get started using Slash GraphQL today](https://slash.dgraph.io) with a free trial.
To use Dgraph Cloud, visit the [Dgraph Pricing Page](https://dgraph.io/pricing) to
get an estimate or contact us.

## Dgraph and GraphQL

Because Dgraph is a native GraphQL database, queries across sparse data sets run
efficiently. As a native GraphQL database, Dgraph doesn’t have a relational
database running in the background, so your data has the ability to grow and
change with your app, without the need to add new tables. And when it comes time
to deploy a new schema, you can do that in seconds, not hours.

To learn more about Dgraph's GraphQL implementation, see [GraphQL Overview](/graphql/overview/).

## Fully-Managed Dgraph

Slash GraphQL is a fully-managed GraphQL database service that lets you focus on
building apps, not managing infrastructure. Slash is built from the ground up to
support GraphQL, and uses a graph database structure down to its lowest layers.
So it integrates seamlessly with your existing ecosystem of GraphQL tools.

Slash GraphQL gives you the power of Dgraph database in a hosted environment, giving you
the flexibility and performance of a horizontally-scalable and distributed
GraphQL database with a graph backend, so you don’t need to configure and manage
VMs, servers, firewalls, and HTTP endpoints to power your modern apps and websites.

To learn more about Slash GraphQL, see [Slash GraphQL Overview](https://dgraph.io/learn/courses/resources/overviews-and-glossary/overview/slash-overview/).

Dgraph Cloud extends Slash GraphQL to meet the needs of enterprise customers with dedicated instances, high availability, and the choice of running in your own cloud VPC.

## Glossary of Dgraph and GraphQL terms

| Term            |Definition	                                                   |Learn More                  |
|-----------------|--------------------------------------------------------------|----------------------------|
|Badger | A fast, open-source key-value database written in pure Go that provides the disk layer for Dgraph database.|[Badger documentation](https://dgraph.io/docs/badger/)|
|data node| A basic unit of data representing an entity in a graph database. Nodes are connected by *edges* and have predicates (or *fields*) that contain node data.||
|Dgraph Alpha| A server node that serves data to clients of Dgraph database, and also provides administrator endpoints.|[Dgraph Alpha documentation](https://dgraph.io/docs/master/deploy/dgraph-alpha/)|
|Dgraph database| A horizontally-scalable and distributed GraphQL database with a graph backend.	|[Dgraph documentation](https://dgraph.io/docs/master/)|
|Dgraph Query Language (DQL)|	A query language that extends and modifies GraphQL to support deep queries for modern apps. Formerly known as *GraphQL+-*.	|[DQL documentation](https://dgraph.io/docs/master/dql/)|
|Dgraph Zero| A server node that controls a Dgraph database cluster. |[Dgraph Zero documentation](https://dgraph.io/docs/master/deploy/dgraph-alpha/)|
|edge|	A relationship between two data nodes in a graph database.	| |
|field|	See *predicate*.	| |
|GraphQL|	An open-source query language for APIs and a runtime for fulfilling those queries. |[Dgraph GraphQL documentation](https://dgraph.io/docs/master/graphql/overview/)|
|object|	See *data node*.	| |
|server node|	A server that makes up part of a server cluster. See *Dgraph Alpha* and *Dgraph Zero*. |[Dgraph Cluster Setup documentation](https://dgraph.io/docs/master/deploy/cluster-setup/) |
|predicate|	A property of a data node in a graph database; also a discrete piece of information available to request in a graph database.	| |
|Slash GraphQL|	A fully-managed GraphQL database service powered by Dgraph database.	|[Slash GraphQL documentation](https://dgraph.io/docs/slash-graphql/) |
