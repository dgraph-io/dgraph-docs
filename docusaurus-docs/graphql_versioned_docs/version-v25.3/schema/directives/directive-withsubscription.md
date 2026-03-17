---
title: "@withSubscription"

---


The `@withSubscription` directive enables **subscription** operation on a GraphQL type.

A subscription notifies your client with changes to back-end data using the WebSocket protocol.
Subscriptions are useful to get low-latency, real-time updates. 

To enable subscriptions on any type add the `@withSubscription` directive to the schema as part of the type definition, as in the following example:

```graphql
type Todo @withSubscription {
  id: ID!
  title: String!
  description: String!
  completed: Boolean!
}
```

Refer to [GraphQL Subscriptions](/graphql/subscriptions) to learn how to use subscriptions in you client application.

