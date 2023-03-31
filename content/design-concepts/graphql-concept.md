
+++
date = "2017-03-27:12:00:00Z"
title = "GraphQL"
weight = 70
[menu.main]
    parent = "design-concepts"
+++

 `GraphQL` is a query and update standard defined at [GraphQL.org](https://graphql.org/). `GraphQL` is natively supported by Dgraph, without requiring additional servers, data mappings or resolvers. Typically, "resolving" a data field in GraphQL simply corresponds to walking that relationship in Dgraph.

 Dgraph also auto-generates access functions for any `GraphQL Schema`, allowing users to get up and running in minutes with Dgraph + a GraphQL schema. The APIs are auto-generated.

GraphQL is internally converted to the (similar-but-different) `DQL` query language before being executed. We can think of GraphQL as "sitting on top" of DQL.
