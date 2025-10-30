+++
title = "@filter"
type = "docs"
weight = 2
[menu.main]
  parent = "dql-directives"
+++

The `@filter` directive allows you to apply additional filtering conditions to nodes in a query block. Filters use [functions]({{< relref "functions.md" >}}) to test node attributes or relationships and can be applied to both root query blocks and nested blocks.

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

Nested blocks may also specify criteria on the relationships attributes using [filtering on facets]({{< relref "../facets.md#filtering-on-facets" >}}).

## Filter Functions

Filters use the same [functions]({{< relref "../functions.md" >}}) that are available for root criteria. These functions can test:

- **String attributes**: term matching, regular expressions, fuzzy matching, full-text search
- **Attribute values**: equality, inequalities, ranges
- **Node properties**: predicate existence, UID, relationships, node type
- **Relationship counts**: equality and inequality comparisons
- **Geolocation attributes**: proximity, containment, intersection

Common functions include:

- String matching: [allofterms]({{< relref "../functions.md#allofterms" >}}), [anyofterms]({{< relref "../functions.md#anyofterms" >}}), [regexp]({{< relref "../functions.md#regular-expressions" >}}), [match]({{< relref "../functions.md#fuzzy-matching" >}}), [alloftext]({{< relref "../functions.md#full-text-search" >}})
- Value comparisons: [eq]({{< relref "../functions.md#equal-to" >}}), [le, lt, ge, gt]({{< relref "../functions.md#less-than-less-than-or-equal-to-greater-than-and-greater-than-or-equal-to" >}}), [between]({{< relref "../functions.md#between" >}})
- Node tests: [has]({{< relref "../functions.md#has" >}}), [uid]({{< relref "../functions.md#uid" >}}), [uid_in]({{< relref "../functions.md#uid_in" >}}), `type()`
- Geolocation: [near]({{< relref "../functions.md#near" >}}), [within]({{< relref "../functions.md#within" >}}), [contains]({{< relref "../functions.md#contains" >}}), [intersects]({{< relref "../functions.md#intersects" >}})

Variables may be used as function parameters in filters. See [query variables]({{< relref "variables.md#query-variables" >}}) and [value variables]({{< relref "variables.md#value-variables" >}}) for more information.

Filters can also be combined with directives like [@cascade]({{< relref "cascade-directive.md" >}}) to create pattern matching queries where only nodes matching the complete query structure are returned.

## Connecting Filters

Within `@filter` multiple functions can be used with boolean operators AND, OR, and NOT.

### AND, OR and NOT

Connectives `AND`, `OR` and `NOT` join filters and can be built into arbitrarily complex filters, such as `(NOT A OR B) AND (C AND NOT (D OR E))`.  Note that, `NOT` binds more tightly than `AND` which binds more tightly than `OR`.

Query Example: All Steven Spielberg movies that contain either both "indiana" and "jones" OR both "jurassic" and "park".

{{< runnable >}}
{
  me(func: eq(name@en, "Steven Spielberg")) @filter(has(director.film)) {
    name@en
    director.film @filter(allofterms(name@en, "jones indiana") OR allofterms(name@en, "jurassic park"))  {
      uid
      name@en
    }
  }
}
{{< /runnable >}}

