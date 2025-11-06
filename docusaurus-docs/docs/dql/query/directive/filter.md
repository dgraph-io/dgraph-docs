---
title: "@filter"
---
import RunnableCodeBlock from '@site/src/components/RunnableCodeBlock';



The `@filter` directive allows you to apply additional filtering conditions to nodes in a query block. Filters use [functions](/dgraph-overview/dql/query/functions) to test node attributes or relationships and can be applied to both root query blocks and nested blocks.

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

Nested blocks may also specify criteria on the relationships attributes using [filtering on facets](../facets#filtering-on-facets).

## Filter Functions

Filters use the same [functions](../functions) that are available for root criteria. These functions can test:

- **String attributes**: term matching, regular expressions, fuzzy matching, full-text search
- **Attribute values**: equality, inequalities, ranges
- **Node properties**: predicate existence, UID, relationships, node type
- **Relationship counts**: equality and inequality comparisons
- **Geolocation attributes**: proximity, containment, intersection

Common functions include:

- String matching: [allofterms](../functions#allofterms), [anyofterms](../functions#anyofterms), [regexp](../functions#regular-expressions), [match](../functions#fuzzy-matching), [alloftext](../functions#full-text-search)
- Value comparisons: [eq](../functions#equal-to), [le, lt, ge, gt](../functions#less-than-less-than-or-equal-to-greater-than-and-greater-than-or-equal-to), [between](../functions#between)
- Node tests: [has](../functions#has), [uid](../functions#uid), [uid_in](../functions#uid_in), `type()`
- Geolocation: [near](../functions#near), [within](../functions#within), [contains](../functions#contains), [intersects](../functions#intersects)

Variables may be used as function parameters in filters. See [query variables](/dgraph-overview/variables#query-variables) and [value variables](/dgraph-overview/variables#value-variables) for more information.

Filters can also be combined with directives like [@cascade](/dgraph-overview/dql/query/directive/cascade-directive) to create pattern matching queries where only nodes matching the complete query structure are returned.

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

