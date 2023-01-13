+++
title = "Dgraph Database Overview"
description = "Introduction to Dgraph Database. Dgraph is a horizontally scalable and distributed graph database that supports GraphQL natively. You can run Dgraph on-premise, in your cloud infrastructure, or as a service fully-managed by Dgraph."
[menu.main]
    name = "Dgraph Overview"
    identifier = "overview"
    weight = 2
+++
## Dgraph

Designed from the ground up to be distributed for scale and speed, **Dgraph** is the native Graph database with native GraphQL support. It is open-source, scalable, distributed, highly-available, and lightning fast.

Dgraph is different from other graph databases in a number of ways, including:

- **Distributed Scale**: &emsp; *Built from day 1 to be distributed, to handle larger data sets.*

- **GraphQL Support**: &emsp; *GraphQL is built in to make data access simple and standards-compliant. Unlike most GraphQL solutions, no resolvers are needed - Dgraph resolves queries automatically through graph navigation.*

- **True Free Open Source Software (FOSS)**: &emsp; *Dgraph is free to use, and [available on github](https://github.com/dgraph-io/dgraph).*

- **Fully Transactional and ACID Compliant**: &emsp; *Dgraph satisfies demanding OLTP workloads that require frequent inserts and updates.*

- **Text Search**: &emsp; *Full-text searching is included.*
## Who is using Dgraph & How
Dgraph is a graph database with some special differentiators. Any graph database is better when relationships and connections really matter. For example, when querying across links in a social network, or detecting networks of interconnected fraudsters in a fraud application - these are natural graph use cases.

Dgraph particularly excels when teams need simplicity and elegance to start fast, or anticipate large data sets and loads down the road.

To get a sample of the kinds of things that are natural with Dgraph, consider the following real-world scenarios 
(and click the embedded links):

* [Data unification](https://dgraph.io/case-studies/factset/)
* [Customer 360](https://dgraph.io/capventis)
* [Fraud detection](https://www.youtube.com/watch?v=rAuDfb1dhl0) <!-- Knights Analytics Dgraph Day video -->
* Ecommerce stores
* [Entity resolution](https://dgraph.io/blog/post/introducing-entity-resolution/)
* [HR management applications](https://www.idgconnect.com/article/3615990/why-graphs-will-form-the-basis-for-a-new-hr-industry.html)
* [Entity Resolution and Master data management (MDM)](https://dgraph.io/blog/post/introducing-entity-resolution/)
* Product recommendation engines
* Real-time chat applications
* [Logistics](https://dgraph.io/case-studies/ke-holdings/)

To learn more about how organizations are using Dgraph, read more
[Dgraph Case Studies](https://dgraph.io/case-studies).

## Dgraph and GraphQL
In Dgraph, GraphQL is not an afterghtough or an add-on; it is core to the product. GraphQL developers can get started in minutes, and need not concern themselves with the powerful graph database running in the background.

The difference with Dgraph is that no resolvers or custom queries are needed. Simply update a GraphQL schema, and all apis are ready to go. The "resolvers" are transparently implemented by simply following graph relationships from node to node and node to field, and with native graph performance.

For complex queries that the GraphQL specification does not support, Dgraph provides an extension of pure GraphQL called "DQL." With GraphQL simple use cases remain simple, and with DQL extensions complex cases become possible.

<!-- TODO: too long. move this part below to GraphQL page 
   Our GraphQL feature allows GraphQL users to get started immediately - simply define a schema and Dgraph automatically builds out CRUD and query APIs. Dgraph works as a standards-compliant GraphQL server, so many web and app developers may not know (or care) that Dgraph is a powerful graph database as well.

   As a native GraphQL database, Dgraph doesn’t have a relational database running in the background, or complex resolvers to map between database and GraphQL schemas. We often call this "single-schema development." The big time savings is that there are no GraphQL resolvers or custom queries needed to get started. All GraphQL fields are "resolved" simply by following our graph database edges to required fields. With single-schema development, you can change your GraphQL schema, insert data, and call your new APIs in seconds, not hours.

   To learn more about Dgraph's GraphQL implementation, see this [GraphQL Overview]({{< relref "/graphql/overview" >}}). If you are a SQL user, check out:

   [Dgraph for SQL Users](https://dgraph.io/learn/courses/datamodel/sql-to-dgraph/overview/introduction/). 
   
   Read more about the motivations for GraphQL and how Facebook still uses it to provide generic yet efficient data access in [the original annoucement of the spec from Facebook](https://engineering.fb.com/2015/09/14/core-data/graphql-a-data-query-language/).
-->
## The Graph Model - Nodes, Relationships and Values

Dgraph is fundamentally a [**property-graph database**](https://www.dataversity.net/what-is-a-property-graph/) because it stores nodes and relations and can also store sets of properties, called "facets," on any relationship to add qualifying data or metadata to them.

<!-- TODO move this to some JSON format page

**Dgraph JSON input example with a facet:**

    {
      "name": "Bob",
      "Address": {
       "street": "123 Main St."
      },
      "Address|since": "2022-02-22"
    }

This JSON structure succinctly represents rich data:
- **Nodes**: A Person node and Address node are included
- **Relation**: The Person node is related to the Address node via an "Address" directed relationship
- **Values**: the person's name is "Bob" and the Address street component is "123 Main St."
- **Facet** metadata: the Address relation is qualified with a property specifying the Address relationship started on February 20, 2022.
-->

Dgraph supports [JSON]({{< relref "mutations/json-mutation-format" >}}) data as both a return structure and an insert/update format. In Dgraph JSON nesting represents relations among nodes, so `{"Person": {"Address": "123 Main St." }}` efficiently and intuitively represents a Person node, an Address node, and a relation between them. 

In addition, Dgraph supports [RDF triples]({{< relref "mutations/triples/" >}}) as an input and outpup format. 

Dgraph relationships are directed (or from a node to a value), so it is recommended to define a [reverse edge]({{< relref "query-language/schema.md#reverse-edges" >}})
as part of a schema if fast graph query in both directions is needed.
## App teams and data teams work together seamlessly
Dgraph allows a particularly smoooth interaction among data teams or experts and data consumers. GraphQL's flexibility empowers data consumers to get exactly the data they want, in the format they want it, at the speed they need, without writing custom REST APIs or understanding a new graph query language.

Database experts can focus on the data, schema and indexes, without maintaining a sprawling set of REST APIs, views, or optimized queries tailored to each data consumer or app.

## Hosting options
Dgraph is typically deployed as a service in the cloud (Graph as a Service) - [click here to get started in minutes](https://cloud.dgraph.io/). This is the fastest and easiest way to get started with Dgraph, and is recommended since it includes hosting, security, monitoring, support, and upgrades, from the Dgraph team.

- **Managed**: Our **Dgraph Cloud** offering provides the flexibility and performance of a horizontally-scalable and distributed graph database with native GraphQL services out of the box, so you don’t need to configure and manage VMs, pods, containers, servers, firewalls, monitoring, load balancers, API gateways, or HTTP endpoints to power a modern data infrastructure.

   To learn more about Dgraph Cloud, see the [Dgraph Cloud Overview](https://dgraph.io/docs/cloud/introduction).

- **Self-hosted**: For organizations who require or prefer to **keep data on premise,** or in their own cloud-based servers, dgraph can also be downloaded and installed as a docker image, or as a binary to install directly on a Linux machine.

### Dgraph Cloud Cluster Types

 - **Shared Instance**: Dgraph Cloud with [shared instances](https://dgraph.io/graphql) is a
fully-managed graph database service that lets you focus on building apps, not
managing infrastructure. This is a fast and easy way to get started with GraphQL, and does not require any graph database knowledge to start and run. 

    Shared instances run in a common database using Dgraph multi-tenancy. Your data is protected but you share resources and will have limited scale.

    Try [[this ]](https://dgraph.io/tour/graphqlintro/2/) to define a GraphQL schema, insert and query data in just a few minutes. 

- **Dedicated instances** run on their own dedicated hardware to ensure consistent performance. This option extends the capabilities of the lower-cost shared instances to support enterprise, production workloads, and includes a high availability option.

Dgraph's cloud offering is currently available in AWS and Google Cloud (GCP), with an Azure version coming soon.
## Internal architecture
Dgraph scales to larger data sizes than other graph databases because it is designed from the groud up to be distributed. Therefore Dgraph runs as a cluster of server nodes which communicate to form a single logical data store. There are two main types of processes (nodes) running: Zeros and Alphas.

- **Dgraph Zero** server nodes hold metadata for the Dgraph cluster, coordinate distributed transactions, and re-balance data among server groups.

- **Dgraph Alpha** server nodes store the graph data and indices. Unlike non-distributed graph databases, Dgraph alphas store and index "predicates" which represent the relations among data elements. This unique indexing approach allows Dgraph to perform a database query with depth N in only N network hops, making it faster and more scalable for distributed (sharded) data sets.

In addition, people use common tools to define schemas, load data, and query the database:

- **GraphQL IDEs**: A number of GraphQL IDEs are available to update GraphQL schemas and run GraphQL updates and queries. [One of these IDEs is GrahpiQL](https://github.com/graphql/graphiql)

- **Ratel** is a Dgraph UI that runs DQL queries, mutations & allows schema editing. 

- **Dgraph lambdas**: A Dgraph lambdas is an optional node.js server that the alpha nodes connect to to execute data functions written in JavaScript during query processing. This is useful to implement custom triggers or custom GraphQL resolvers.

### Scale, replication and sharding
Every cluster will have at least one Dgraph Zero node and one Dgraph Alpha node. Then databases are expanded in two ways.

- **High Availability Replication**: For high-availability, Dgraph runs with three zeros and three alphas instead of one of each. This configuration is recommended for the scale and reliability required by most production applications. Having three servers both triples the capacity of the overall cluster, and also provides redundancy.

- **Sharding**: When data sizes approach or exceed 1 TB, Dgraph databases are typically sharded so that full data replicas are not kept on any single alpha node. With sharding, data is distributed across many nodes (or node groups) to achieve higher scale. Sharding and high-availability combine when desired to provide massive scale and ideal reliability.

**Self-healing**: In Dgraph's cloud offering, Kubernetes is used to automatically detect, restart and heal any cluster (HA, sharded, both or neither) to keep things running smoothly and at full capacity.

## What's Next

- **Get Started** with a [free database instance](https://cloud.dgraph.io) 
- get familiar with some terms in our [Glossary](/dgraph-glossary)
- Take the [Dgraph tour](https://dgraph.io/tour/)
- Go through some [tutorials]({{< relref "tutorials" >}})
