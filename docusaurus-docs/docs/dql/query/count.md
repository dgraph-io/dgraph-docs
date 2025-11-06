---
title: Count
---
import RunnableCodeBlock from '@site/src/components/RunnableCodeBlock';



Syntax Examples:

* `count(predicate)`
* `count(uid)`

The form `count(predicate)` counts how many `predicate` edges lead out of a node.

The form `count(uid)` counts the number of UIDs matched in the enclosing block.

Query Example: The number of films acted in by each actor with `Orlando` in their name.

<RunnableCodeBlock>

```dql
{
  me(func: allofterms(name@en, "Orlando")) @filter(has(actor.film)) {
    name@en
    count(actor.film)
  }
}
```

</RunnableCodeBlock>

Count can be used at root and [aliased](/dgraph-overview/dql/query/alias).

Query Example: Count of directors who have directed more than five films.  When used at the query root, the [count index](/dgraph-overview/predicate-indexing#count-index) is required.

<RunnableCodeBlock>

```dql
{
  directors(func: gt(count(director.film), 5)) {
    totalDirectors : count(uid)
  }
}
```

</RunnableCodeBlock>


Count can be assigned to a [value variable](/dgraph-overview/variables#value-variables).

Query Example: The actors of Ang Lee's "Eat Drink Man Woman" ordered by the number of movies acted in.

<RunnableCodeBlock>

```dql
{
  var(func: allofterms(name@en, "eat drink man woman")) {
    starring {
      actors as performance.actor {
        totalRoles as count(actor.film)
      }
    }
  }

  edmw(func: uid(actors), orderdesc: val(totalRoles)) {
    name@en
    name@zh
    totalRoles : val(totalRoles)
  }
}
```

</RunnableCodeBlock>
