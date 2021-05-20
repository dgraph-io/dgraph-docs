+++
date = "2017-03-20T22:25:17+11:00"
title = "Cascade Directive"
weight = 15
[menu.main]
    parent = "query-language"
+++

With the `@cascade` directive, nodes that don't have all predicates specified in the query are removed. This can be useful in cases where some filter was applied or if nodes might not have all listed predicates.


Query Example: Harry Potter movies, with each actor and characters played.  With `@cascade`, any character not played by an actor called Warwick is removed, as is any Harry Potter movie without any actors called Warwick.  Without `@cascade`, every character is returned, but only those played by actors called Warwick also have the actor name.
{{< runnable >}}
{
  HP(func: allofterms(name@en, "Harry Potter")) @cascade {
    name@en
    starring{
        performance.character {
          name@en
        }
        performance.actor @filter(allofterms(name@en, "Warwick")){
            name@en
         }
    }
  }
}
{{< /runnable >}}

You can apply `@cascade` on inner query blocks as well.
{{< runnable >}}
{
  HP(func: allofterms(name@en, "Harry Potter")) {
    name@en
    genre {
      name@en
    }
    starring @cascade {
        performance.character {
          name@en
        }
        performance.actor @filter(allofterms(name@en, "Warwick")){
            name@en
         }
    }
  }
}
{{< /runnable >}}

## Parameterized `@cascade`

The `@cascade` directive can optionally take a list of fields as an argument.
This changes the default behavior, considering only the supplied fields as mandatory instead of all the fields for a type.
Listed fields are automatically cascaded as a required argument to nested selection sets.

{{% notice "tip" %}}
The rule with `@cascade(predicate)` is that the predicate needs to be in the query at the same level `@cascade` is.
{{% /notice %}}

In the example below, `name` is supplied in the `fields` argument. For an author to be in the query response, it must have a `name`, and if it has a `country` subfield, then that subfield must also have `name`.

{{< runnable >}}
{
    queryAuthor(func: allofterms(name@en, "Harry Potter")) @cascade(name) {
        reputation
        name
        country{
           Id
           name
        }
    }
}
{{< /runnable >}}

The query below only return those `posts` which have a non-null `text` field.

{{< runnable >}}
{
    queryAuthor(func: allofterms(name@en, "Harry Potter")) {
        reputation
        name
        posts @cascade(text) {
           title
           text
        }
    }
}
{{< /runnable >}}

### Nesting and parameterized cascade

The cascading nature of field selection is overwritten by a nested `@cascade`.

For example, the query below ensures that an author has the `reputation` and `name` fields, and, if it has a `posts` subfield, then that subfield must have a `text` field.

{{< runnable >}}
{
    queryAuthor(func: allofterms(name@en, "Harry Potter")) @cascade(reputation, name) {
        reputation
        name
        dob
        posts @cascade(text) {
            title
            text
        }
    }
}
{{< /runnable >}}
