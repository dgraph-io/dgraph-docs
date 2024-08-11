+++
title = "Directives"
weight = 4
[menu.main]
  identifier = "directives"
  parent = "gqlschema"
+++

The list of all directives supported by Dgraph.

### @auth

`@auth` allows you to define how to apply authorization rules on the queries/mutation for a type.

Reference: [Auth directive]({{< relref "auth.md" >}})

### @cascade

`@cascade` allows you to filter out certain nodes within a query.

Reference: [Cascade](/graphql/queries/cascade)

### @custom

`@custom` directive is used to define custom queries, mutations and fields.

Reference: [Custom directive]({{< relref "graphql/custom/directive.md" >}})

### @deprecated

The `@deprecated` directive lets you mark the schema definition of a field or `enum` value as deprecated, and also lets you provide an optional reason for the deprecation.

Reference: [Deprecation]({{< relref "deprecated.md" >}})

### @dgraph

`@dgraph` directive tells us how to map fields within a type to existing predicates inside Dgraph.

Reference: [@dgraph directive]({{< relref "directive-dgraph" >}})

### @embedding

`@embedding` directive designates one or more fields as vector embeddings.

Reference: [@embedding directive]({{< relref "embedding" >}})

### @generate

The `@generate` directive is used to specify which GraphQL APIs are generated for a type.

Reference: [Generate directive]({{< relref "generate.md" >}})

### @hasInverse

`@hasInverse` is used to setup up two way edges such that adding a edge in
one direction automatically adds the one in the inverse direction.

Reference: [Linking nodes in the graph]({{< relref "graph-links.md" >}})

### @id

`@id` directive is used to annotate a field which represents a unique identifier coming from outside
 of Dgraph.

Reference: [Identity](({{< relref "ids.md" >}})

### @include

The `@include` directive can be used to include a field based on the value of an `if` argument.

Reference: [Include directive]({{< relref "skip-include.md" >}})

### @lambda

The `@lambda` directive allows you to call custom JavaScript resolvers. The `@lambda` queries, mutations, and fields are resolved through the lambda functions implemented on a given lambda server.

Reference: [Lambda directive]({{< relref "lambda-overview.md" >}})

### @remote

`@remote` directive is used to annotate types for which data is not stored in Dgraph. These types
are typically used with custom queries and mutations.

Reference: [Remote directive]({{< relref "directive.md#remote-types" >}})

### @remoteResponse

The `@remoteResponse` directive allows you to annotate the fields of a `@remote` type in order to map a custom query's JSON key response to a GraphQL field.

Reference: [Remote directive]({{< relref "directive.md##remote-response" >}})

### @search

`@search` allows you to perform filtering on a field while querying for nodes.

Reference: [Search]({{< relref "search.md" >}})

### @secret

`@secret` directive is used to store secret information, it gets encrypted and then stored in Dgraph.

Reference: [Password Type]({{< relref "types.md#password-type" >}})

### @skip

The `@skip` directive can be used to fetch a field based on the value of a user-defined GraphQL variable.

Reference: [Skip directive]({{< relref "skip-include.md" >}})

### @withSubscription

`@withSubscription` directive when applied on a type, generates subscription queries for it.

Reference: [Subscriptions]({{< relref "subscriptions.md" >}})

### @lambdaOnMutate

The `@lambdaOnMutate` directive allows you to listen to mutation events(`add`/`update`/`delete`). Depending on the defined events and the occurrence of a mutation event, `@lambdaOnMutate` triggers the appropriate lambda function implemented on a given lambda server.

Reference: [LambdaOnMutate directive]({{< relref "webhook.md" >}})

<style>
  ul.contents {
    display: none;
  }
</style>
