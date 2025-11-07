---
title: "@filter"
---
import RunnableCodeBlock from '@site/src/components/RunnableCodeBlock';



The `@filter` directive allows you to apply additional filtering conditions to nodes in a query block. Filters use [functions](/dql/query/functions) to test node attributes or relationships and can be applied to both root query blocks and nested blocks.

## Using @filter

### In Query Blocks

A query block may have a combination of filters to apply to the root nodes. The `@filter` directive appears after the `func:` criteria and before the opening curly bracket:

```graphql
{
  me(func: eq(name@en, "Steven Spielberg")) @filter(has(director.film)) {
    name@en
    director.film {
      name@en
    }
  }
}
```

### In Nested Blocks

For relationships to fetch, nested blocks may specify filters to apply on the related nodes:

```graphql
{
  director(func: eq(name@en, "Steven Spielberg")) {
    name@en
    director.film @filter(allofterms(name@en, "indiana jones")) {
      uid
      name@en
    }
  }
}
```

Nested blocks may also specify criteria on the relationships attributes using [filtering on facets](/dql/query/facets#filtering-on-facets).

## Filter Functions

Filters use the same [functions](/dql/query/functions) that are available for root criteria. These functions can test:

- **String attributes**: term matching, regular expressions, fuzzy matching, full-text search
- **Attribute values**: equality, inequalities, ranges
- **Node properties**: predicate existence, UID, relationships, node type
- **Relationship counts**: equality and inequality comparisons
- **Geolocation attributes**: proximity, containment, intersection

Common functions include:

- String matching: [allofterms](/dql/query/functions#allofterms), [anyofterms](/dql/query/functions#anyofterms), [regexp](/dql/query/functions#regular-expressions), [match](/dql/query/functions#fuzzy-matching), [alloftext](/dql/query/functions#full-text-search)
- Value comparisons: [eq](/dql/query/functions#equal-to), [le, lt, ge, gt](/dql/query/functions#less-than-less-than-or-equal-to-greater-than-and-greater-than-or-equal-to), [between](/dql/query/functions#between)
- Node tests: [has](/dql/query/functions#has), [uid](/dql/query/functions#uid), [uid_in](/dql/query/functions#uid_in), `type()`
- Geolocation: [near](/dql/query/functions#near), [within](/dql/query/functions#within), [contains](/dql/query/functions#contains), [intersects](/dql/query/functions#intersects)

Variables may be used as function parameters in filters. See [query variables](/dql/query/variables#query-variables) and [value variables](/dql/query/variables#value-variables) for more information.

Filters can also be combined with directives like [@cascade](/dql/query/directive/cascade-directive) to create pattern matching queries where only nodes matching the complete query structure are returned.

## Connecting Filters

Within `@filter` multiple functions can be used with boolean operators AND, OR, and NOT.

### AND, OR and NOT

Connectives `AND`, `OR` and `NOT` join filters and can be built into arbitrarily complex filters, such as `(NOT A OR B) AND (C AND NOT (D OR E))`.  Note that, `NOT` binds more tightly than `AND` which binds more tightly than `OR`.

Query Example: All Steven Spielberg movies that contain either both "indiana" and "jones" OR both "jurassic" and "park".

<RunnableCodeBlock>

```dql
{
  me(func: eq(name@en, "Steven Spielberg")) @filter(has(director.film)) {
    name@en
    director.film @filter(allofterms(name@en, "jones indiana") OR allofterms(name@en, "jurassic park"))  {
      uid
      name@en
    }
  }
}
```

</RunnableCodeBlock>

