---
title: "GraphQL on Existing Dgraph"

---

### How to use GraphQL on an existing Dgraph instance

In the case where you have an existing Dgraph instance which has been created using a DQL Schema (and populated with Dgraph import tools) and you want to expose some or all of the data using a GraphQL API, you can use the [@dgraph directive](/graphql/schema/directives/directive-dgraph/) to customize how Dgraph maps GraphQL type names and fields names to DQL types and predicates.



### Language support in GraphQL

In your GraphQL schema, you need to define a field for each language that you want to use. 
In addition, you also need to apply the `@dgraph(pred: "...")` directive on that field, with the `pred` argument set to point to the correct DQL predicate with a language tag for the language that you want to use it for.
Dgraph will automatically add a `@lang` directive in the DQL schema for the corresponding predicate.

:::tip
By default, the DQL predicate for a GraphQL field is generated as `Typename.FieldName`.
:::

For example:

```graphql
type Person {
     name: String   # Person.name is the auto-generated DQL predicate for this GraphQL field, unless overridden using @dgraph(pred: "...")
     nameHi: String @dgraph(pred:"Person.name@hi") # this field exposes the value for the language tag `@hi` for the DQL predicate `Person.name` to GraphQL
     nameEn: String @dgraph(pred:"Person.name@en")
     nameHi_En:  String @dgraph(pred:"Person.name@hi:en") # this field uses multiple language tags: `@hi` and `@en`
     nameHi_En_untag:  String @dgraph(pred:"Person.name@hi:en:.") # as this uses `.`, it will give untagged values if there is no value for `@hi` or `@en`
  }
```

If a GraphQL field uses more than one language tag, then it won't be part of any mutation input. Like, in the above example the fields `nameHi_En` and `nameHi_En_untag` can't be given as an input to any mutation. Only the fields which use one or no language can be given in a mutation input, like `name`, `nameHi`, and `nameEn`.

All the fields can be queried, irrespective of whether they use one language or more.

:::note
GraphQL won’t be able to query `Person.name@*` type of language tags because of the structural requirements of GraphQL.
:::


