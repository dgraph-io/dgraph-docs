+++
title = "Use DQL in GraphQL"
weight = 3
type = "graphql"
[menu.graphql]
  name = "Use DQL in GraphQL"
  identifier = "graphql-dql-use"
  parent = "graphql-dql"
+++



Dgraph Query Language ([DQL](/dql/)) can be used to extend GraphQL API capabilities when writing:

- [custom DQL resolvers]({{<relref "custom-dql">}})
- [subscriptions on DQL queries](/graphql/schema/directives/directive-withsubscription/#subscriptions-to-custom-dql)



When writing custom DQL query resolvers, you must understand the [GraphQL - DQL schema mapping]({{<relref "graphql-dql-schema">}}) to use proper aliases inside DQL queries to map them to the GraphQL response. 



