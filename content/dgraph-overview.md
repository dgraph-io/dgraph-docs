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

## How does Dgraph work?

Dgraph is not a layer on top of another SQL or No-SQL database such as Postgres or MongoDB.
Instead, Dgraph is a new database built from the ground-up to manage data natively in graphs.
Dgraph reads data from disk, accesses RAM, and talks over the network using HTTP
and gRPC. A single Dgraph database instance consists of multiple entitles,
described below in [Dgraph architecture](#dgraph-architecture), but these three entities work together in a single layer.

### What's behind Dgraph's GraphQL endpoints?

Dgraph is the world's first, and at this time only, service to offer a
specification-compliant GraphQL endpoint without the need for an additional
translation layer in the tech stack. You will not find a hidden layer of GraphQL
resolvers in Dgraph. GraphQL is natively executed within the core of Dgraph itself.

<!-- I'd suggest cutting this section, as this level of detail isn't interesting to those still considering whether to try Dgraph... also, the next section provides enough history

### Brief History and Timeline of Dgraph 


- Oct. 2015: Dgraph's founder, Manish, sends email debating whether to use GraphQL as the query language for a new graph db.
- Dec. 2015: Launched Dgraph [v0.1](https://github.com/dgraph-io/dgraph/tree/c83506478e7650174f39453d3db905fe5cd75a41)
- June 2016: Dgraph's efforts [recognized](https://react-etc.net/entry/dgraph-is-a-next-generation-graph-database-with-graphql-as-the-query-language) to make GraphQL a direct competitor to graph query languages.
- June 2016: Dgraph doesn't follow GraphQL Specification [issue](https://github.com/dgraph-io/dgraph/issues/114) opened.
- June 2016: Dgraph recognizes their fork of the GraphQL spec and coins GraphQL+- (GraphQL Plus Minus)
- Oct. 2016: Featured in [React, etc. Tech Stack](https://react-etc.net/entry/dgraph-has-the-potential-to-become-a-defacto-standard-for-graphql-graph-databases) as having the potential to become a defacto standard for GraphQL powered DBs
- May 2017: [Dgraph introduces Badger](https://dgraph.io/blog/post/badger/) replacing RocksDB in the Dgraph stack.
- May 2017: Dgraph's GraphQL Community [request GraphQL spec compliant query language](https://github.com/dgraph-io/dgraph/issues/933).
- Nov. 2017: Dgraph commits to [reconciling GraphQL+- with GraphQL spec](https://github.com/dgraph-io/dgraph/issues/933#issuecomment-344505456).
- Dec. 2017: Dgraph releases [production-ready graph database v1.0](https://dgraph.io/blog/post/releasing-v1.0/)
- Aug. 2018: Dgraph becomes first GraphQL DB to be Jepsen tested.
- Aug. 2018: Due to complexity nature of GraphQL+-, [spec reconciliation could not be achieved](https://github.com/dgraph-io/dgraph/issues/933#issuecomment-412283699).
- Aug. 2018: Dgraph criticized for being a ["stuck in the middle approach"](https://github.com/dgraph-io/dgraph/issues/933#issuecomment-412351583)
- Feb. 2019: [GraphSchema Tools converter](https://github.com/MichaelJCompton/GraphSchemaTools) built by community member.
- July 2019: Dgraph celebrates [10K Github stargazers](https://dgraph.io/blog/post/10k-github-stars/)!
- Sept. 2019: Dgraph releases [v1.1.0](dgraph.io/blog/post/release-v1.1.0/) with support for types and enterprise feature ACL.
- Sept. 2019: Dgraph [releases Ristretto](https://dgraph.io/blog/post/introducing-ristretto-high-perf-go-cache/) improving Dgraphs core performance
- Oct. 2019: Dgraph [soft releases spec compliant GraphQL endpoint within the core](https://dgraph.io/blog/post/building-native-graphql-database-dgraph/) of the DB after hiring the author of GraphSchema Tools converter.
- Dec. 2019: Dgraph [releases v1.1.1](https://dgraph.io/blog/post/release-v1.1.1/) featuring upsert blocks, facets, and encryption at rest.
- March 2020: Dgraph hits GA with [release v20.03](https://dgraph.io/blog/post/dgraph-graphql-hits-ga/) featuring a new spec complaint GraphQL endpoint (also new CalVer version control)
- July 2020: Dgraph [releases v20.07](https://dgraph.io/blog/post/dgraph-release-shuri/) featuring authentication, custom logic, and subscription support for GraphQL endpoint.
- Sept. 2020: Dgraph [announces Slash GraphQL](https://dgraph.io/blog/post/announcing-slash-graphql/) (later renamed as Dgraph Cloud).
- Oct. 2020: Dgraph [renames GraphQL+- to DQL](https://dgraph.io/blog/post/graphql+-to-dql/) (Dgraph Query Language).
- Dec. 2020: Dgraph [releases v20.11](https://dgraph.io/blog/post/v2011-release/) featuring support for GraphQL interfaces, unions, aggregation queries, geospatial types, and lambda resolvers. Dramatically improves memory management.
- Jan. 2021: Dgraph [named Graph Data Platform Contender](https://dgraph.io/blog/post/dgraph-forrester/) by Forrester
- April 2021: Dgraph [releases v21.03](https://dgraph.io/blog/post/v2103-release/) featuring webhooks, upserts, and Apollo Federation support for GraphQL.

-->

### Dgraph Query Language (DQL)

Dgraph started out as its own proprietary graph database without support for the native GraphQL
endpoint it has today. Early on, Dgraph engineers wanted to use GraphQL, but
realized the official GraphQL specification could not support everything that customers
would need from a database query language. GraphQL was not created to be a
database query language, but it could easily be extended as a database query language.

So, Dgraph Labs forked our language from GraphQL and initially named this
language *GraphQL+-* ("GraphQL, plus or minus"). For simplicity, GraphQL+- has
since been renamed to Dgraph Query Language (DQL).

### Dgraph and GraphQL

Dgraph was developed around DQL, which like GraphQL, uses a schema to classify and
manage data. As Dgraph developed, it drew much attention from the GraphQL community,
 but developers still faced the challenge that
has almost always been present when implementing GraphQL in a tech stack — the need to 
build a layer of GraphQL resolvers for queries, mutations, and subscriptions.
The need for a layer of resolvers required developers to translate GraphQL into DQL,
handling middleware, authorization, and custom business logic. Without a resolving layer,
developers were not able to utilize the spec compliant, GraphQL community tools that continue to be developed.

In response to user feedback, Dgraph Labs decided to add a spec-compliant GraphQL
solution into the core of Dgraph. But unlike other GraphQL solutions, Dgraph's
GraphQL implementation creates a spec-compliant GraphQL API with only developer-provided
GraphQL schema. A developer defines types and fields, and applies directives in a GraphQL schema file
that is provided to their Dgraph database instance. Dgraph then creates
a full-featured CRUD-compliant GraphQL API endpoint, including the queries and mutations
that one would expect when working with data under the provided GraphQL schema.

For more information about when and why to use either DQL or GraphQL and a side-by-side
comparison, please see the [GraphQL vs. DQL](https://dgraph.io/blog/post/graphql-vs-dql/) blog.

### Dgraph architecture

Dgraph is a single layer in your tech stack, but inside the inner workings of a
Dgraph database instance, there are three distinct entities:

- [Badger](https://dgraph.io/badger) - Dgraph's custom-built key-value store
- [Ristretto](https://dgraph.io/ristretto) - Dgraph's custom-built cache
- [Dgraph](https://github.com/dgraph-io/dgraph) - the methods and algorithms used to parse DQL (and now GraphQL) and act accordingly

External to the core Dgraph database instance, you will find tools and communication clients to support Dgraph:

- [Ratel]({{< relref "/ratel/overview" >}}) - a GUI Layer to work directly with DQL. (Ratel does not work with the graphql)
- [DQL Clients]({{< relref "/clients" >}}) written in Go, C#, Java, JavaScript, and Python.

## Dgraph database clusters

Dgraph is designed specifically to distribute data horizontally. You can scale Dgraph and maintain
high availability by sharding data and replicating those shards. Dgraph handles the
mundane tasks of actually sharding and replicating the data, you just need to setup and configure
your Dgraph cluster appropriately. For more information on deloying and managing
Dgraph your self, see [Production Checklist]({{< relref "/deploy/production-checklist" >}})

Dgraph now offers a fully managed service with high availability. This relieves you from all the
stress of deployment and relies upon our team of expert engineers. Continue reading this section
for a quick overview of deployment, or skip to the next section to learn more about Dgraph Cloud,
our fully managed Dgraph database-as-a-service offering 

## Running Dgraph database and Dgraph Cloud

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

Use the instructions in this section to get started using Dgraph Cloud or
self-managed Dgraph today.

### Get started with Dgraph Cloud

You can [get started with Dgraph Cloud](https://cloud.dgraph.io) today with a
free trial. To use Dgraph Cloud, visit our [Pricing Page](https://dgraph.io/pricing) or 
[Pricing Calculator](https://cloud.dgraph.io/pricing-calculator/) to get an
estimate, or [contact us](https://dgraph.io/connect).

{{% notice "tip" %}}
Check which Dgraph release version is running on your Dgraph Cloud backend in [Dgraph Cloud Settings](https://cloud.dgraph.io/_/settings), and then use the version selector on this page to find docs.
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

## Dgraph endpoints

Dgraph exposes a variety of HTTP and gRPC endpoints. The type of Dgraph cluster
node that exposes each endpoint (*Alpha* or *Zero*) is noted with each endpoint description below:

### DQL endpoints

- [`/query`]({{< relref "/query-language/graphql-fundamentals" >}}) - used to make query requests with DQL (Alpha)
- [`/mutate`]({{< relref "/mutations/mutations-using-curl" >}}) - used to send mutations in DQL (Alpha)

### GraphQL endpoints

- [`/graphql`]({{< relref "/graphql/overview" >}}) - used to host the GraphQL API, rewriting GraphQL to DQL (Alpha)
- [`/admin`]({{< relref "/deploy/dgraph-administration" >}}) - used to administer the Dgraph cluster (Alpha)

### Other endpoints

- [`/alter`]({{< relref "/deploy/dgraph-administration" >}}) - used to alter the DQL schema (Alpha)
- [`/health`]({{< relref "/deploy/dgraph-alpha" >}}#querying-health) - used to query the health (Alpha)
- [`/login`]({{< relref "/enterprise-features/access-control-lists" >}}) - used to log-in an ACL user, and provides them with a JWT. (Enterprise Feature)
- [`/state`]({{< relref "/deploy/dgraph-zero" >}}#more-about-the-state-endpoint) - used to view information about the nodes that are part of the cluster. (Zero)
- [`/assign`]({{< relref "/deploy/dgraph-zero" >}}) - used allocate a range of UIDs and request timestamps. (Zero)
- [`/removeNode`]({{< relref "/deploy/dgraph-zero" >}}) - used to remove a dead Zero or Alpha node from a cluster. (Zero)
- [`/moveTablet`]({{< relref "/deploy/dgraph-zero" >}}) - used to force move tablets to a group. (Zero)
- [`/enterpriseLicense`]({{< relref "/" >}}) - used to apply an enterprise license to a cluster. (Zero)

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
