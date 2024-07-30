+++
title = "@embedding"
weight = 1
[menu.main]
    parent = "directives"
+++


A Float array can be used as a vector using `@embedding` directive. It denotes a vector of floating point numbers, i.e an ordered array of float32. 

The embeddings can be defined on one or more predicates of a type and they are generated using suitable machine learning models.

This directive is used in conjunction with `@search` directive to declare the HNSW index. For more information see: [@search](/graphql/schema/directives/search/#vector-embedding) directive for vector embeddings.