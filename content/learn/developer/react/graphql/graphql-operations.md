+++
title = "GraphQL Operations"
type = "learn"
tutorial = "courses/messageboardapp/react"
pageType = "learn"
description = "Using your schema, Dgraph Cloud generated ways to interact with the graph. In GraphQL, the API can be inspected with introspection queries."
weight = 8
[menu.learn]
  name = "GraphQL Operations"
  parent = "react-app-graphql"
  identifier = "react-app-graphql-operations"
[nav]
  nextpage = "react-graphql-mutations.md"
+++

The schema that you developed and deployed to Dgraph Cloud in the previous
sections was about the types in our domain and the shape of the application data
graph. From that, Dgraph Cloud generated some ways to interact with the graph.
GraphQL supports the following *operations*, which provide different ways to
interact with a graph:

* **queries**: used to find a starting point and traverse a subgraph
* **mutations**: used to change the graph and return a result
* **subscriptions**: used to listen for changes in the graph

In GraphQL, the API can be inspected with special queries called *introspection
queries*. Introspection queries are a type of GraphQL query that provides the
best way to find out what operations you can perform with a GraphQL API.

## Introspection

Many GraphQL tools support introspection and generate documentation to help you
explore an API. There are several tools in the GraphQL ecosystem you can use to
explore an API, including [GraphQL Playground](https://github.com/prisma-labs/graphql-playground),
[Insomnia](https://insomnia.rest/), [GraphiQL](https://github.com/graphql/graphiql),
[Postman](https://www.postman.com/graphql/), and [Altair](https://github.com/imolorhe/altair).

You can also explore your GraphQL API using the API explorer that's included in
the Dgraph Cloud web UI. Navigate to the **GraphQL** tab where you can
access the introspected schema from the "Documentation Explorer" in the right
menu.

*![Dgraph Cloud Schema Explorer](/images/message-board/dgraph-cloud-schema-explorer.png)*

From there, you can click through to the queries and mutations and check out the
API. For example, this API includes mutations to add, update and delete users,
posts and comments.


Next, you'll learn more about the API that Dgraph Cloud created from the
schema by trying out the same kind of queries and mutations you'll use to build
the message board app.
