+++
title = "Order and Pagination in GraphQL"
description = "Every type with fields whose types can be ordered gets ordering built into the query and any list fields of that type."
weight = 7
[menu.main]
    name = "Order and Pagination"
    parent = "graphql-queries"
+++

Every type with fields whose types can be ordered (`Int`, `Float`, `String`, `DateTime`) gets
ordering built into the query and any list fields of that type. Every query and list field
gets pagination with `first` and `offset` and ordering with `order` parameter.

The `order` parameter is not required for pagination.

For example, find the most recent 5 posts.

```graphql
queryPost(order: { desc: datePublished }, first: 5) { ... }
```

Skip the first five recent posts and then get the next 10.

```graphql
queryPost(order: { desc: datePublished }, offset: 5, first: 10) { ... }
```

It's also possible to give multiple orders.  For example, sort by date and within each
date order the posts by number of likes.

```graphql
queryPost(order: { desc: datePublished, then: { desc: numLikes } }, first: 5) { ... }
```
