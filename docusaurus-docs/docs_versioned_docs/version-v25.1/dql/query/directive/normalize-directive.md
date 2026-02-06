---
title: "@normalize"
---
import RunnableCodeBlock from '@site/src/components/RunnableCodeBlock';



With the `@normalize` directive, only aliased predicates are returned and the result is flattened to remove nesting.

Query Example: Film name, country and first two actors (by UID order) of every Steven Spielberg movie, without `initial_release_date` because no alias is given and flattened by `@normalize`
<RunnableCodeBlock>

```dql
{
  director(func:allofterms(name@en, "steven spielberg")) @normalize {
    director: name@en
    director.film {
      film: name@en
      initial_release_date
      starring(first: 2) {
        performance.actor {
          actor: name@en
        }
        performance.character {
          character: name@en
        }
      }
      country {
        country: name@en
      }
    }
  }
}
```

</RunnableCodeBlock>

You can also apply `@normalize` on nested query blocks. It will work similarly but only flatten the result of the nested query block where `@normalize` has been applied. `@normalize` will return a list irrespective of the type of attribute on which it is applied.
<RunnableCodeBlock>

```dql
{
  director(func:allofterms(name@en, "steven spielberg")) {
    director: name@en
    director.film {
      film: name@en
      initial_release_date
      starring(first: 2) @normalize {
        performance.actor {
          actor: name@en
        }
        performance.character {
          character: name@en
        }
      }
      country {
        country: name@en
      }
    }
  }
}
```

</RunnableCodeBlock>