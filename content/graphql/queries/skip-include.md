+++
title = "@skip and @include Directives in GraphQL"
description = "@skip and @include directives can be applied to query fields. They let you skip or include a field based on the value of the if argument."
weight = 9
[menu.main]
    name = "@skip and @include Directives"
    parent = "graphql-queries"
+++

`@skip` and `@include` directives can be applied to query fields.
They allow you to skip or include a field based on the value of the `if` argument
that is passed to the directive.

## @skip

In the query below, we fetch posts and decide whether to fetch the title for them or not
based on the `skipTitle` GraphQL variable.

GraphQL query

```graphql
query ($skipTitle: Boolean!) {
  queryPost {
    id
    title @skip(if: $skipTitle)
    text
  }
}
```

GraphQL variables
```json
{
    "skipTitle": true
}
```

## @include

Similarly, the `@include` directive can be used to include a field based on the value of
the `if` argument. The query below would only include the authors for a post if `includeAuthor`
GraphQL variable has value true.

GraphQL Query
```graphql
query ($includeAuthor: Boolean!) {
  queryPost {
    id
    title
    text
    author @include(if: $includeAuthor) {
        id
        name
    }
  }
}
```

GraphQL variables
```json
{
    "includeAuthor": false
}
```
