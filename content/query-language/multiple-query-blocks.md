+++
date = "2017-03-20T22:25:17+11:00"
title = "Multiple Query Blocks"
weight = 8
[menu.main]
    parent = "query-language"
+++

Inside a single query, multiple query blocks are allowed.  The result is all blocks with corresponding block names.

Multiple query blocks are executed in parallel.

The blocks need not be related in any way.

Query Example: All of Angelina Jolie's films, with genres, and Peter Jackson's films since 2008.

{{< runnable >}}
{
 AngelinaInfo(func:allofterms(name@en, "angelina jolie")) {
  name@en
   actor.film {
    performance.film {
      genre {
        name@en
      }
    }
   }
  }

 DirectorInfo(func: eq(name@en, "Peter Jackson")) {
    name@en
    director.film @filter(ge(initial_release_date, "2008"))  {
        Release_date: initial_release_date
        Name: name@en
    }
  }
}
{{< /runnable >}}


If queries contain some overlap in answers, the result sets are still independent.

Query Example: The movies Mackenzie Crook has acted in and the movies Jack Davenport has acted in.  The results sets overlap because both have acted in the Pirates of the Caribbean movies, but the results are independent and both contain the full answers sets.

{{< runnable >}}
{
  Mackenzie(func:allofterms(name@en, "Mackenzie Crook")) {
    name@en
    actor.film {
      performance.film {
        uid
        name@en
      }
      performance.character {
        name@en
      }
    }
  }

  Jack(func:allofterms(name@en, "Jack Davenport")) {
    name@en
    actor.film {
      performance.film {
        uid
        name@en
      }
      performance.character {
        name@en
      }
    }
  }
}
{{< /runnable >}}


## Var Blocks

Var blocks start with the keyword `var` and are not returned in the query results.

Query Example: Angelina Jolie's movies ordered by genre.

{{< runnable >}}
{
  var(func:allofterms(name@en, "angelina jolie")) {
    name@en
    actor.film {
      A AS performance.film {
        B AS genre
      }
    }
  }

  films(func: uid(B), orderasc: name@en) {
    name@en
    ~genre @filter(uid(A)) {
      name@en
    }
  }
}
{{< /runnable >}}

## Multiple Var Blocks

Multiple `var` blocks are also supported within a single query operation. Variables
from one `var` block can be used in any of the following blocks but not within the
same block.

Query Example: Movies containing both Angelina Jolie and Morgan Freeman sorted by name.

{{< runnable >}}
{
  var(func:allofterms(name@en, "angelina jolie")) {
    name@en
    actor.film {
      A AS performance.film
    }
  }
  var(func:allofterms(name@en, "morgan freeman")) {
    name@en
    actor.film {
      B as performance.film @filter(uid(A))
    }
  }
  
  films(func: uid(B), orderasc: name@en) {
    name@en
  }
}
{{< /runnable >}}

{{% notice "note" %}}
This same results could have been obtained by logically combining both both var blocks
in the films block.
```
{
  var(func:allofterms(name@en, "angelina jolie")) {
    name@en
    actor.film {
      A AS performance.film
    }
  }
  var(func:allofterms(name@en, "morgan freeman")) {
    name@en
    actor.film {
      B as performance.film
    }
  }
  films(func: uid(A,B), orderasc: name@en) @filter(uid(A) AND uid(B)) {
    name@en
  }
}
```
The root `uid` function unions the uids from var `A` and `B` hence the need for the filter
to intersect the uids from var `A` and `B`.
{{% /notice %}}
