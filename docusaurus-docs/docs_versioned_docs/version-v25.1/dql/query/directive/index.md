---
title: Directives
---

Directives in Dgraph Query Language (DQL) are special annotations that modify how queries are executed or how results are formatted. They are prefixed with the `@` symbol and can be applied to query blocks or predicates to change their behavior.

Directives provide powerful control over:

- **Filtering**: Apply conditions to filter nodes in query results
- **Response structure**: Format and organize query results
- **Graph traversal**: Control how the graph is explored
- **Pattern matching**: Filter results based on complete query structure
- **Aggregation**: Group and aggregate data

## Available Directives

- **[@filter](/dql/query/directive/filter)**: Applies additional filtering conditions to nodes in query blocks using functions and boolean operators.

- **[@normalize](/dql/query/directive/normalize-directive)**: Flattens the response structure by removing nesting and returning only aliased predicates.

- **[@cascade](/dql/query/directive/cascade-directive)**: Filters out nodes that don't match all predicates specified in the query at any nested level, enabling pattern matching behavior.

- **[@recurse](/dql/query/directive/recurse-query)**: Performs recursive graph traversal, following relationships to explore paths of variable depth.

- **[@ignorereflex](/dql/query/directive/ignorereflex-directive)**: Ignores reflexive edges (edges that point back to the same node) during graph traversal.

- **[@groupby](/dql/query/directive/groupby)**: Groups query results based on specified predicates and allows aggregation functions to be applied to each group.

Directives can be combined in a single query to achieve complex querying and result formatting requirements.

