---
title: "@dgraph"

---


The `@dgraph` directive customizes the name of the types and predicates generated in Dgraph when deploying a GraphQL Schema.

* `type <type> @dgraph(type: "TypeNameToUseInDgraph")` controls what Dgraph type is used for a GraphQL type.
* `field: SomeType @dgraph(pred: "DgraphPredicate")` controls what Dgraph predicate is mapped to a GraphQL field.

For example, if you have existing types that don't match GraphQL requirements, you can create a schema like the following.

```graphql
type Person @dgraph(type: "Human-Person") {
    name: String @search(by: [hash]) @dgraph(pred: "name")
    age: Int
}

type Movie @dgraph(type: "film") {
    name: String @search(by: [term]) @dgraph(pred: "film.name")
}
```

Which maps to the Dgraph schema:

```graphql
type Human-Person {
    name
    Person.age
}

type film {
    film.name
}

name string @index(hash) .
Person.age: int .
film.name string @index(term) .
```

You might also have the situation where you have used `name` for both movie names and people's names.  In this case you can map fields in two different GraphQL types to the one Dgraph predicate.

```graphql
type Person {
    name: String @dgraph(pred: "name")
    ...
}

type Movie {
    name: String @dgraph(pred: "name")
    ...
}
```

:::note
In Dgraph's current GraphQL implementation, if two fields are mapped to the same Dgraph predicate, both should have the same `@search` directive.
:::