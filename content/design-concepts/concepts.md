+++
date = "2017-03-20T22:25:17+11:00"
title = "Concepts"
weight = 3
[menu.main]
    parent = "design-concepts"
+++








## Dgraph Ratel GUI
Dgraph provides the `Ratel` GUI tool for DQL querying and basic graph visualization. Ratel does not support GraphQL queries, since there are many mature tools and every user or company is likely to have their own preferred tools for GraphQL development.




## Lambdas
Dgraph Lambdas are JavaScript functions that can be used during query or mutation processing to extend GraphQL or DQL queries and mutations. Lambdas are not related at all to AWS Lambdas. They are functions that run in an (optional) node.js server that is included in the Dgraph Cloud offering. 

## ACLs
Dgraph Access Control Lists (ACLs) are sets of permissions for which `Relationships` a user may access. Recall that Dgraph is "predicate based" so all data is stored in and is implicit in relationships. This allows relationship-based controls to be very powerful in restricting a graph based on roles (RBAC).

Note that the Dgraph multi-tenancy feature relies on ACLs to ensure each tenant can only see their own data in one server.

Using ACLs requires a client to authenticate (log in) differently and specify credentials that will drive which relationships are visible in their view of the graph database.

## Namespace or Tenant
A Dgraph `Namespace` (aka Tenant) is a logically separate database within a Dgraph cluster. A Dgraph cluster can host many Namespaces (and this is how the Dgraph "shared" cloud offering works). Each Tenant logs into their own namespace using their own credentials, and sees only their own data. 

There is no mechanism to query in a way that combines data from two namespaces, which simplifies and enforces security in use cases where this is the requirement. An API layer or client would have to pull data from multiple namespaces using different authenticated queries if data needed to be combined.

