+++
title = "Apollo Federation"
description = "Dgraph now supports Apollo federation so that you can create a gateway GraphQL service that includes the Dgraph GraphQL API and other GraphQL services."
weight = 14
[menu.main]
  name = "Apollo Federation"
  identifier = "federation"
  parent = "graphql"
+++

Dgraph supports [Apollo federation](https://www.apollographql.com/docs/federation/) starting in release version 21.03. This lets you create a gateway GraphQL service that includes the Dgraph GraphQL API and other GraphQL services.

## Support for Apollo federation directives

The current implementation supports the following five directives: `@key`, `@extends`, `@external`, `@provides`, and `@requires`.

### `@key` directive
This directive takes one field argument inside it: the `@key` field. There are few limitations on how to use `@key` directives:

- Users can define the @key directive only once for a type
- Support for multiple key fields is not currently available.
- Since the @key field acts as a foreign key to resolve entities from the service where it is extended, the field provided as an argument inside the @key directive should be of ID type or have the @id directive on it.

For example -

```graphql
type User @key(fields: "id") {
   id: ID!
  name: String
}
```

### `@extends` directive
This directive is provided to give support for extended definitions. Suppose the above defined `User` type is defined in some other service. Users can extend it in Dgraph's GraphQL service by using this directive. 

```graphql
type User @key(fields: "id") @extends{
  id: String! @id @external
  products: [Product]
}
```
The same is also achievable with the `extend` keyword, i.e., user has the choice to choose between `extend type User ...` or `type User @extends ...`.

### `@external` directive
This directive is used when the given field is not stored in this service. It can only be used on extended type definitions. As it is used above on the `id` field of `User` type.

### `@provides` directive
This directive is used on a field that tells the gateway to return a specific fieldSet from the base type while fetching the field. 

For example -

```graphql
type Review @key(fields: "id") {
  product: Product @provides(fields: "name price")
}

extend type Product @key(fields: "upc") {
  upc: String @external
  name: String @external
  price: Int @external
}
```

While fetching `Review.product` from the `review` service, and if the `name` or `price` is also queried, the gateway will fetch these from the `review` service itself, meaning that it also resolves these fields, even though both fields are `@external`.

### `@requires` directive
This directive is used on a field to annotate the fieldSet of the base type. It is used to develop a query plan where the required fields may not be needed by the client, but the service may need additional information from other services. 

For example -

```graphql
extend type User @key(fields: "id") {
  id: ID! @external
  email: String @external
  reviews: [Review] @requires(fields: "email")
}
```

When the gateway fetches `user.reviews` from the `review` service, the gateway will get `user.email` from the `User` service and provide it as an argument to the `_entities` query.

Using `@requires` alone on a field doesn't make much sense. In cases, where you feel the need to use `@requires`, you would want some custom logic on that field too. You can achieve that using `@lambda` or `@custom(http: {...})` directives.

Here's an example -

1. Schema:
```graphql
extend type User @key(fields: "id") {
  id: ID! @external
  email: String @external
  reviews: [Review] @requires(fields: "email") @lambda
}
```
2. Lambda Script:
```js
// returns a list of reviews for a user
async function userReviews({parent, graphql}) {
  let reviews = [];
  // find the reviews for a user using the email and return them.
  // Even though the email has been declared `@external`, it will be available as `parent.email` as it is mentioned in `@requires`.
  return reviews
}
self.addGraphQLResolvers({
  "User.reviews": userReviews
})
```

## Generated queries and mutations

In this section, you will see what all queries and mutations will be available to individual service and to the Apollo gateway. 

Let's take the below schema as an example -

```graphql
type Mission @key(fields: "id") {
    id: ID!
    crew: [Astronaut]
    designation: String!
    startDate: String
    endDate: String
}

type Astronaut @key(fields: "id") @extends {
    id: ID! @external
    missions: [Mission]
}
```

The queries and mutations which are exposed to the gateway are -

```graphql
type Query {
	getMission(id: ID!): Mission
	queryMission(filter: MissionFilter, order: MissionOrder, first: Int, offset: Int): [Mission]
	aggregateMission(filter: MissionFilter): MissionAggregateResult
}

type Mutation {
	addMission(input: [AddMissionInput!]!): AddMissionPayload
	updateMission(input: UpdateMissionInput!): UpdateMissionPayload
	deleteMission(filter: MissionFilter!): DeleteMissionPayload
	addAstronaut(input: [AddAstronautInput!]!): AddAstronautPayload
	updateAstronaut(input: UpdateAstronautInput!): UpdateAstronautPayload
	deleteAstronaut(filter: AstronautFilter!): DeleteAstronautPayload
}
```

The queries for `Astronaut` are not exposed to the gateway since it will be resolved through the `_entities` resolver. Although these queries will be available on the Dgraph GraphQL API endpoint.

## Mutation for `extended` types
If you want to add an object of `Astronaut` type which is extended in this service.
The mutation `addAstronaut` takes `AddAstronautInput` which is generated as -

```graphql
input AddAstronautInput {
	id: ID!
	missions: [MissionRef]
}
```

Even though the `id` field is of `ID` type which should be ideally generated internally by Dgraph. In this case, it should be provided as input since currently federated mutations aren't supported. The user should provide the value of `id` same as the value present in the GraphQL service where the type  `Astronaut` is defined.

For example, let's take that the type `Astronaut` is defined in some other service `AstronautService` as -

```graphql
type Astronaut @key(fields: "id") {
    id: ID! 
    name: String!
}
```

When adding an object of type `Astronaut`, first it should be added into `AstronautService` service and then the `addAstronaut` mutation should be called with value of `id` provided as an argument which must be equal to the value in `AstronautService` service.
