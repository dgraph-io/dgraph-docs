---
title: Fragments
---

The `fragment` keyword lets you define new fragments that can be referenced
in a query, per the [Fragments section of the GraphQL specification](http://spec.graphql.org/June2018/#sec-Language.Fragments).
Fragments allow for the reuse of common repeated selections of fields, reducing
duplicated text in the DQL documents. Fragments can be nested inside fragments,
but no cycles are allowed in such cases. For example:

```sh
curl -H "Content-Type: application/dql" localhost:8080/query -XPOST -d $'
query {
  debug(func: uid(1)) {
    name@en
    ...TestFrag
  }
}
fragment TestFrag {
  initial_release_date
  ...TestFragB
}
fragment TestFragB {
  country
}' | python -m json.tool | less
```

:::note
GraphQL+- has been renamed to Dgraph Query Language (DQL). While `application/dql`
is the preferred value for the `Content-Type` header, we will continue to support
`Content-Type: application/graphql+-` to avoid making breaking changes.
:::
