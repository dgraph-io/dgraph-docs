+++
title = "Index of Directives in GraphQL"
description = "The list of all directives supported by Dgraph's GraphQL implementation. Full details linked within for all directives available with GraphQL."
weight = 11
[menu.main]
  name = "Directives"
  identifier = "directives"
  parent = "graphql"
+++

The list of all directives supported by Dgraph.

### @auth

`@auth` allows you to define how to apply authorization rules on the queries/mutation for a type.

Reference: [Auth directive](/docs/graphql/authorization/directive)

### @cascade

`@cascade` allows you to filter out certain nodes within a query.

Reference: [Cascade](/docs/graphql/queries/cascade)

### @custom

`@custom` directive is used to define custom queries, mutations and fields.

Reference: [Custom directive](/docs/graphql/custom/directive)

### @deprecated

The `@deprecated` directive lets you mark the schema definition of a field or `enum` value as deprecated, and also lets you provide an optional reason for the deprecation.

Reference: [Deprecation]({{< relref "graphql/schema/deprecated.md" >}})

### @dgraph

`@dgraph` directive tells us how to map fields within a type to existing predicates inside Dgraph.

Reference: [GraphQL on Existing Dgraph]({{< relref "graphql/dgraph/index.md" >}})

### @generate

The `@generate` directive is used to specify which GraphQL APIs are generated for a type.

Reference: [Generate directive](/docs/graphql/schema/generate)

### @hasInverse

`@hasInverse` is used to setup up two way edges such that adding a edge in
one direction automically adds the one in the inverse direction.

Reference: [Linking nodes in the graph](/docs/graphql/schema/graph-links)

### @id

`@id` directive is used to annotate a field which represents a unique identifier coming from outside
 of Dgraph.

Reference: [Identity](/docs/graphql/schema/ids)

### @include

The `@include` directive can be used to include a field based on the value of an `if` argument.

Reference: [Include directive](/docs/graphql/queries/skip-include)

### @lambda

The `@lambda` directive allows you to call custom JavaScript resolvers. The `@lambda` queries, mutations, and fields are resolved through the lambda functions implemented on a given lambda server.

Reference: [Lambda directive](/docs/graphql/lambda/overview)

### @remote

`@remote` directive is used to annotate types for which data is not stored in Dgraph. These types
are typically used with custom queries and mutations.

Reference: [Remote directive](/docs/graphql/custom/directive/#remote-types)

### @remoteResponse

The `@remoteResponse` directive allows you to annotate the fields of a `@remote` type in order to map a custom query's JSON key response to a GraphQL field.

Reference: [Remote directive](/docs/graphql/custom/directive/#remote-response)

### @search

`@search` allows you to perform filtering on a field while querying for nodes.

Reference: [Search](/docs/graphql/schema/search)

### @secret

`@secret` directive is used to store secret information, it gets encrypted and then stored in Dgraph.

Reference: [Password Type](/docs/graphql/schema/types/#password-type)

### @skip

The `@skip` directive can be used to fetch a field based on the value of a user-defined GraphQL variable.

Reference: [Skip directive](/docs/graphql/queries/skip-include)

### @withSubscription

`@withSubscription` directive when applied on a type, generates subsciption queries for it.

Reference: [Subscriptions](/docs/graphql/subscriptions)

### @lambdaOnMutate

The `@lambdaOnMutate` directive allows you to listen to mutation events(`add`/`update`/`delete`). Depending on the defined events and the occurrence of a mutation event, `@lambdaOnMutate` triggers the appropriate lambda function implemented on a given lambda server.

Reference: [LambdaOnMutate directive](/docs/graphql/lambda/webhook)
