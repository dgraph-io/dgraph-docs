+++
title = "GraphQL API"
description = "Generate a GraphQL API and a graph backend from a single GraphQL schema."
weight = 10

[menu.main]
  identifier = "graphql"

+++

Dgraph lets you generate a GraphQL API and a graph backend from a single [GraphQL schema]({{< relref "schema/_index.md">}}), no resolvers or custom queries are needed. Dgraph automatically generates the GraphQL operations for [queries]({{< relref "queries/_index.md">}}) and [mutations]({{< relref "mutations/_index.md">}}) 

GraphQL developers can [get started]({{< relref "quick-start/index.md">}}) in minutes, and need not concern themselves with the powerful graph database running in the background.

Dgraph extends the [GraphQL specifications](https://spec.graphql.org/) with [directives]({{< relref "schema/directives/_index.md">}}) and allows you to customize the behavior of GraphQL operations using [custom resolvers]({{< relref "custom-overview.md">}}) or to write you own resolver logic with [Lambda resolvers]({{< relref "lambda-overview.md">}}).

Dgraph also supports 
- [GraphQL subscriptions]({{< relref "subscriptions/index.md">}}) with the `@withSubscription` directive: a client application can execute a subscription query and receive real-time updates when the subscription query result is updated.
- [Apollo federation]({{< relref "federation/index.md" >}}) : you can create a gateway GraphQL service that includes the Dgraph GraphQL API and other GraphQL services.

Refer to the following pages for more details: