---
title: Sorting
---
import RunnableCodeBlock from '@site/src/components/RunnableCodeBlock';



Syntax Examples:

* `q(func: ..., orderasc: predicate)`
* `q(func: ..., orderdesc: val(varName))`
* `predicate (orderdesc: predicate) { ... }`
* `predicate @filter(...) (orderasc: N) { ... }`
* `q(func: ..., orderasc: predicate1, orderdesc: predicate2)`

Sortable Types: `int`, `float`, `String`, `dateTime`, `default`

Results can be sorted in ascending order (`orderasc`) or descending order (`orderdesc`) by a predicate or variable.

For sorting on predicates with [sortable indices](/dgraph-overview/predicate-indexing#sortable-indices), Dgraph sorts on the values and with the index in parallel and returns whichever result is computed first.

:::note
Dgraph returns `null` values at the end of the results, irrespective of their sort. This behavior is consistent across indexed and non-indexed sorts.
:::

:::tip
Sorted queries retrieve up to 1000 results by default. This can be changed with [first](/dgraph-overview/pagination#first).
:::


Query Example: French director Jean-Pierre Jeunet's movies sorted by release date.

<RunnableCodeBlock>

```dql
{
  me(func: allofterms(name@en, "Jean-Pierre Jeunet")) {
    name@fr
    director.film(orderasc: initial_release_date) {
      name@fr
      name@en
      initial_release_date
    }
  }
}
```

</RunnableCodeBlock>

Sorting can be performed at root and on value variables.

Query Example: All genres sorted alphabetically and the five movies in each genre with the most genres.

<RunnableCodeBlock>

```dql
{
  genres as var(func: has(~genre)) {
    ~genre {
      numGenres as count(genre)
    }
  }

  genres(func: uid(genres), orderasc: name@en) {
    name@en
    ~genre (orderdesc: val(numGenres), first: 5) {
      name@en
      genres : val(numGenres)
    }
  }
}
```

</RunnableCodeBlock>

Sorting can also be performed by multiple predicates as shown below. If the values are equal for the
first predicate, then they are sorted by the second predicate and so on.

Query Example: Find all nodes which have type Person, sort them by their first_name and among those
that have the same first_name sort them by last_name in descending order.

```
{
  me(func: type("Person"), orderasc: first_name, orderdesc: last_name) {
    first_name
    last_name
  }
}
```
