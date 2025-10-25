+++
date = "2017-03-27:12:00:00Z"
title = "DQL and GraphQL"
type = "docs"
weight = 50
[menu.main]
    parent = "design-concepts"
+++

## Dgraph Schemas
Dgraph natively supports GraphQL, including `GraphQL Schema`s. GraphQL schemas "sit on top of" DQL schemas, in the sense that when a GraphQL schema is added to Dgraph, a corresponding `DQL Schema` is automatically created.

Refer to [GraphQL-DQL interoperability]({{<relref "graphql-dql">}}) section for details.

## Dgraph Queries, Mutations and Upserts
Similarly, GraphQL mutations are implemented on top of DQL in the sense that a GraphQL query is converted internally into a DQL query, which is then executed. This translation is not particularly complex, since DQL is based on GraphQL, with some syntax changes and some extensions.

This is generally transaparent to all callers, however users should be aware that
1) Anything done in GraphQL can also be done in DQL if needed. Some small exceptions include the enforcement of non-null constraints and other checks done before Dgraph transpiles GraphQL to DQL and executes it.
2) Some logging including Request Logging and OpenTrace (Jaeger) tracing may show DQL converted from the GraphQL.
