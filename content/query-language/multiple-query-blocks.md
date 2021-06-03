+++
date = "2017-03-20T22:25:17+11:00"
title = "Multiple Query Blocks with DQL"
description = "With Dgraph Query Language (DQL), you can include multiple query blocks in a single query, and have those query blocks execute in parallel."
weight = 8
[menu.main]
    name = "Multiple Query Blocks"
    parent = "query-language"
+++

Inside a single query, multiple query blocks are allowed, and each block can 
have a name. Multiple query blocks are executed in parallel, and they don't
need to be related in any way.

Query Example: _"All of Angelina Jolie's films, with genres, and Peter Jackson's films since 2008"_

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

Query Example: _"The movies Mackenzie Crook has acted in and the movies Jack Davenport has acted in"_

The results sets overlap because both have acted in the _Pirates of the Caribbean_
movies, but the results are independent and both contain the full answers sets.

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


## Variable (`var`) blocks

Variable blocks (`var` blocks) start with the keyword `var` and are not returned
in the query results, but do affect the contents of query results.

Query Example: _"Angelina Jolie's movies ordered by genre"_

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

## Multiple `var` blocks

You can also use multiple `var` blocks within a single query operation. You can
use variables from one `var` block in any of the subsequent blocks, but not
within the same block.

Query Example: _"Movies containing both Angelina Jolie and Morgan Freeman sorted by name"_

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


### Combining multiple `var` blocks

You could get the same query results by logically combining both both `var` blocks
in the films block, as follows:
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
The root `uid` function unions the `uid`s from `var` `A` and `B`, so you need a
filter to intersect the `uid`s from `var` `A` and `B`.

