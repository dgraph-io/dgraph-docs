+++
title = "@embedding"
weight = 1
[menu.main]
    parent = "directives"
+++

`@embedding` allows you to create HNSW index on vector embeddings. The embeddings can be defined on one or more predicates of a type and they are generated using suitable machine learning models.

This directive cannot be used independently. It must be used in conjunction with `@search` directive. For more information see: [@search]({{< relref "search.md" >}}).