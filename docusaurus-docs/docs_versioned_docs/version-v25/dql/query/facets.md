---
title: Querying Facets
---

This page covers how to query and filter using facets in DQL. For an introduction to what facets are and how to create them, see [Facets in Schema](../dql-schema#facets-edge-attributes).

## Sample Data

The examples on this page use this data:

```rdf
# Schema
name: string @index(exact, term) .
rated: [uid] @reverse @count .

# Data
_:alice <name> "Alice" .
_:alice <dgraph.type> "Person" .
_:alice <mobile> "040123456" (since=2006-01-02T15:04:05) .
_:alice <car> "MA0123" (since=2006-02-02T13:01:09, first=true) .

_:bob <name> "Bob" .
_:bob <dgraph.type> "Person" .
_:bob <car> "MA0134" (since=2006-02-02T13:01:09) .

_:charlie <name> "Charlie" .
_:charlie <dgraph.type> "Person" .

_:alice <friend> _:bob (close=true, relative=false) .
_:alice <friend> _:charlie (close=false, relative=true) .
_:alice <friend> _:dave (close=true, relative=true) .

_:movie1 <name> "Movie 1" .
_:movie1 <dgraph.type> "Movie" .

_:alice <rated> _:movie1 (rating=3) .
_:bob <rated> _:movie1 (rating=5) .
_:charlie <rated> _:movie1 (rating=2) .
```

## Querying Facets

### Query Specific Facets

Use `@facets(facet-name)` to retrieve specific facet values:

```dql
{
  data(func: eq(name, "Alice")) {
    name
    mobile @facets(since)
    car @facets(since)
  }
}
```

Facets appear in the response at the same level as the edge, with keys like `edge|facet`.

### Query All Facets

Use `@facets` without arguments to retrieve all facets on an edge:

```dql
{
  data(func: eq(name, "Alice")) {
    name
    mobile @facets
    car @facets
  }
}
```

### Facets on UID Predicates

For relationship edges, facets appear with the child node:

```dql
{
  data(func: eq(name, "Alice")) {
    name
    friend @facets(close) {
      name
    }
  }
}
```

The `close` facet appears with key `friend|close` alongside each friend's data.

### Using Aliases

Assign custom names to facet results:

```dql
{
  data(func: eq(name, "Alice")) {
    name
    car @facets(car_since: since)
    friend @facets(close_friend: close) {
      name
    }
  }
}
```

:::note
`orderasc` and `orderdesc` are reserved and cannot be used as aliases.
:::

## Filtering on Facets

Filter edges based on facet values using `@facets(condition)`:

### Basic Filter

```dql
{
  data(func: eq(name, "Alice")) {
    friend @facets(eq(close, true)) {
      name
    }
  }
}
```

### Filter and Return Facets

Combine filtering with facet retrieval:

```dql
{
  data(func: eq(name, "Alice")) {
    friend @facets(eq(close, true)) @facets(relative) {
      name
    }
  }
}
```

### Compound Filters

Use `AND`, `OR`, and `NOT` to combine conditions:

```dql
{
  data(func: eq(name, "Alice")) {
    friend @facets(eq(close, true) AND eq(relative, true)) {
      name
    }
  }
}
```

## Sorting by Facets

Sort results by facet values on UID edges:

```dql
{
  me(func: anyofterms(name, "Alice Bob Charlie")) {
    name
    rated @facets(orderdesc: rating) {
      name
    }
  }
}
```

## Facets with Variables

### Assign Facets to Variables

Store facet values in variables for use elsewhere in the query:

```dql
{
  var(func: eq(name, "Alice")) {
    friend @facets(a as close, b as relative)
  }

  close_friends(func: uid(a)) {
    name
    val(a)
  }

  relatives(func: uid(b)) {
    name
    val(b)
  }
}
```

### Variable Propagation

Numeric facets (`int`, `float`) propagate through queries. When multiple paths reach the same node, values are summed:

```dql
{
  var(func: anyofterms(name, "Alice Bob Charlie")) {
    num_raters as math(1)
    rated @facets(r as rating) {
      total_rating as math(r)
      average_rating as math(total_rating / num_raters)
    }
  }
  
  data(func: uid(total_rating)) {
    name
    val(total_rating)
    val(average_rating)
  }
}
```

## Aggregating Facets

Facet values in variables can be aggregated:

```dql
{
  data(func: eq(name, "Alice")) {
    name
    rated @facets(r as rating) {
      name
    }
    avg(val(r))
  }
}
```

:::warning
When a query reaches nodes through multiple paths, facet values are summed. This affects aggregations:

```dql
# This does NOT calculate individual averages correctly
{
  data(func: anyofterms(name, "Alice Bob")) {
    name
    rated @facets(r as rating) {
      name
    }
    avg(val(r))  # Incorrect: r contains summed values
  }
}
```

Calculate per-user averages with separate variable mappings:

```dql
{
  var(func: has(rated)) {
    num_rated as math(1)
    rated @facets(r as rating) {
      avg_rating as math(r / num_rated)
    }
  }

  data(func: uid(avg_rating)) {
    name
    val(avg_rating)
  }
}
```
:::

## Internationalized Facet Keys

Facet keys can use language-specific characters. When querying, enclose them in angle brackets:

**Mutation:**
```rdf
_:person1 <name> "Daniel" (वंश="स्पेनी", ancestry="Español") .
```

**Query:**
```dql
{
  q(func: has(name)) {
    name @facets(<वंश>)
  }
}
```

See [Predicates i18n](../dql-schema#predicates-i18n) for more on internationalization.
