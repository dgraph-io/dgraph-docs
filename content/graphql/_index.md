+++
title = "GraphQL API"
description = "Generate a GraphQL API and a graph backend from a single GraphQL schema."
type = "graphql"
weight = 10


[menu.graphql]
  identifier = "graphql"

+++

Dgraph lets you generate a GraphQL API and a graph backend from a single [GraphQL schema](/graphql/schema/), no resolvers or custom queries are needed. Dgraph automatically generates the GraphQL operations for [queries](/graphql/queries/) and [mutations](/graphql/mutations/) 

GraphQL developers can [get started](/graphql/quick-start/) in minutes, and need not concern themselves with the powerful graph database running in the background.

Dgraph extends the [GraphQL specifications](https://spec.graphql.org/) with [directives](/graphql/schema/directives/) and allows you to customize the behavior of GraphQL operations using [custom resolvers](/graphql/custom/) or to write you own resolver logic with [Lambda resolvers](/graphql/lambda-overview/).

Dgraph also supports 
- [GraphQL subscriptions](/graphql/subscriptions/) with the `@withSubscription` directive: a client application can execute a subscription query and receive real-time updates when the subscription query result is updated.
- [Apollo federation](/graphql/federation/) : you can create a gateway GraphQL service that includes the Dgraph GraphQL API and other GraphQL services.

Refer to the following pages for more details: