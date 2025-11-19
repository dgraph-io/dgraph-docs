---
title: Indexes
---

Filtering on a predicate by applying a [function](query/functions) requires an index.

Indices are defined in the [Dgraph types schema](dql-schema) using `@index` directive.

Here are some examples:
```
name: string @index(term) .
release_date: datetime @index(year) .
description_vector: float32vector @index(hnsw(metric:"cosine")) .
```

When filtering by applying a function, Dgraph uses the index to make the search through a potentially large dataset efficient.

All scalar types can be indexed.

Types `int`, `float`, `bool` and `geo` have only a default index each: with tokenizers named `int`, `float`, `bool` and `geo`.

Types `string` and `dateTime` have a number of indices.

Type `float32vector` supports `hnsw` index.

## String Indices
The indices available for strings are as follows.

| Dgraph function            | Required index / tokenizer             | Notes |
| :-----------------------   | :------------                          | :---  |
| `eq`                       | `hash`, `exact`, `term`, or `fulltext` | The most performant index for `eq` is `hash`. Only use `term` or `fulltext` if you also require term or full-text search. If you're already using `term`, there is no need to use `hash` or `exact` as well. |
| `le`, `ge`, `lt`, `gt`     | `exact`                                | Allows faster sorting.                                   |
| `allofterms`, `anyofterms` | `term`                                 | Allows searching by a term in a sentence.                |
| `alloftext`, `anyoftext`   | `fulltext`                             | Matching with language specific stemming and stopwords.  |
| `regexp`                   | `trigram`                              | Regular expression matching. Can also be used for equality checking. |

:::warning
Incorrect index choice can impose performance penalties and an increased
transaction conflict rate. Use only the minimum number of and simplest indexes
that your application needs.
:::

## Vector Indices

The indices available for `float32vector` are as follows.

| Dgraph function            | Required index / tokenizer             | Notes |
| :-----------------------   | :------------                          | :---  |
| `similar_to`                       | `hnsw` | HNSW index supports parameters `metric` and `exponent`. |



`hnsw` (**Hierarchical Navigable Small World**) index supports the following parameters
- metric : indicate the metric to use to compute vector similarity. One of `cosine`, `euclidean`, and `dotproduct`. Default is `euclidean`.

- exponent : an integer, represented as a string, roughly representing the number of vectors expected in the index in power of 10. The exponent value is used to set "reasonable defaults" for HNSW internal tuning parameters. The default is "3" (10^3 vectors). This is a high-level convenience parameter that acts as a "complexity knob" to scale multiple HNSW parameters simultaneously, namely the `maxlevels`, `efconstruction` and `efsearch`. When you set `exponent: "X"`, Dgraph automatically sets default values for three parameters (only if they're not explicitly specified):
  ```
  maxLevels = X - Number of hierarchical layers
  efConstruction = 50 × X - Size of dynamic candidate list during index construction
  efSearch = 30 × X - Size of dynamic candidate list during search
  ```
- maxLevels : an integer, represented as a string, that controls the maximum number of hierarchical layers in the HNSW. Defaults to the `exponent` parameter. More layers = faster search for large datasets but more memory overhead. Fewer layers = slower search but less memory usage.

- efConstruction : an integer, represented as a string, that controls the size of the candidate list during index construction - higher values create better quality graphs but take longer to build. Defaults to 50 times the value of `maxLevels`.

- efSearch : an integer, represented as a string, that controls the size of the candidate list during search queries - higher values improve recall/accuracy but make searches slower. Defaults to 30 times the value of `maxLevels`.

Here are some examples:
```
simple_vector: float32vector @index(hnsw) .
description_vector: float32vector @index(hnsw(metric:"cosine")) .
large_vector: float32vector @index(hnsw(metric:"euclidean", exponent:"6")) .
larger_vector: float32vector @index(hnsw(metric:"euclidean", maxLevels: "7", efConstruction: "250", efSearch: "80"))
```

## DateTime Indices

The indices available for `dateTime` are as follows.

| Index name / Tokenizer   | Part of date indexed                                      |
| :----------- | :------------------------------------------------------------------ |
| `year`      | index on year (default)                                        |
| `month`       | index on year and month                                         |
| `day`       | index on year, month and day                                      |
| `hour`       | index on year, month, day and hour                               |

The choices of `dateTime` index allow selecting the precision of the index.  Applications, such as the movies examples in these docs, that require searching over dates but have relatively few nodes per year may prefer the `year` tokenizer; applications that are dependent on fine grained date searches, such as real-time sensor readings, may prefer the `hour` index.


All the `dateTime` indices are sortable.


## Sortable Indices

Not all the indices establish a total order among the values that they index. Sortable indices allow inequality functions and sorting.

* Indexes `int` and `float` are sortable.
* `string` index `exact` is sortable.
* All `dateTime` indices are sortable.

For example, given an edge `name` of `string` type, to sort by `name` or perform inequality filtering on names, the `exact` index must have been specified.  In which case a schema query would return at least the following tokenizers.

```
{
  "predicate": "name",
  "type": "string",
  "index": true,
  "tokenizer": [
    "exact"
  ]
}
```

## Count index

For predicates with the `@count` Dgraph indexes the number of edges out of each node.  This enables fast queries of the form:
```
{
  q(func: gt(count(pred), threshold)) {
    ...
  }
}
```

## List Type

Predicate with scalar types can also store a list of values if specified in the schema. The scalar
type needs to be enclosed within `[]` to indicate that its a list type.

```
occupations: [string] .
score: [int] .
```

* A set operation adds to the list of values. The order of the stored values is non-deterministic.
* A delete operation deletes the value from the list.
* Querying for these predicates would return the list in an array.
* Indexes can be applied on predicates which have a list type and you can use [Functions](query/functions) on them.
* Sorting is not allowed using these predicates.
* These lists are like an unordered set. For example: `["e1", "e1", "e2"]` may get stored as `["e2", "e1"]`, i.e., duplicate values will not be stored and order may not be preserved.

## Filtering on list

Dgraph supports filtering based on the list.
Filtering works similarly to how it works on edges and has the same available functions.

For example, `@filter(eq(occupations, "Teacher"))` at the root of the query or the
parent edge will display all the occupations from a list of each node in an array but
will only include nodes which have `Teacher` as one of the occupations. However, filtering
on value edge is not supported.

## Reverse Edges

A graph edge is unidirectional. For node-node edges, sometimes modeling requires reverse edges.  If only some subject-predicate-object triples have a reverse, these must be manually added.  But if a predicate always has a reverse, Dgraph computes the reverse edges if `@reverse` is specified in the schema.

The reverse edge of `anEdge` is `~anEdge`.

For existing data, Dgraph computes all reverse edges.  For data added after the schema mutation, Dgraph computes and stores the reverse edge for each added triple.

```
type Person {
  name
}
type Car {
  regnbr
  owner
}
owner: uid @reverse .
regnbr: string @index(exact) .
name: string @index(exact) .
```

This makes it possible to query Persons and their cars by using:
```
q(func: type(Person)) {
  name
  ~owner { regnbr }
}
```
To get a different key than `~owner` in the result, the query can be written with the wanted label
(`cars` in this case):

```
q(func: type(Person)) {
  name
  cars: ~owner { regnbr }
}
```

This also works if there are multiple "owners" of a `car`:
```
owner [uid] @reverse .
```

In both cases the `owner` edge should be set on the `Car`:
```
_:p1 <name> "Mary" .
_:p1 <dgraph.type> "Person" .
_:c1 <regnbr> "ABC123" .
_:c1 <dgraph.type> "Car" .
_:c1 <owner> _:p1 .
```

## Querying Schema

A schema query queries for the whole schema:

```
schema {}
```

:::note Unlike regular queries, the schema query is not surrounded
by curly braces. Also, schema queries and regular queries cannot be combined.
:::

You can query for particular schema fields in the query body.

```
schema {
  type
  index
  reverse
  tokenizer
  list
  count
  upsert
  lang
}
```

You can also query for particular predicates:

```
schema(pred: [name, friend]) {
  type
  index
  reverse
  tokenizer
  list
  count
  upsert
  lang
}
```

:::note If ACL is enabled, then the schema query returns only the
predicates for which the logged-in ACL user has read access. :::

Types can also be queried. Below are some example queries.

```
schema(type: Movie) {}
schema(type: [Person, Animal]) {}
```

Note that type queries do not contain anything between the curly braces. The
output will be the entire definition of the requested types.
