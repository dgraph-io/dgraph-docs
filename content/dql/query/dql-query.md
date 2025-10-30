+++
title = "Query Structure"
type = "docs"
weight = 2
[menu.main]
  name = "Query Structure"
  identifier = "dql-query"
  parent = "query-language"
+++

Fetching data with Dgraph Query Language (DQL), is done through **DQL Queries**. Adding, modifying or deleting data is done through [DQL Mutations]({{< relref "dql-mutation.md" >}}).

This overview explains the structure of DQL Queries and provides links to the appropriate DQL reference documentation.

### DQL query structure
DQL is **declarative**, which means that queries return a response back in a similar shape to the query. It gives the client application the control of what it gets: the request return exactly what you ask for, nothing less and nothing more. In this, DQL is similar to GraphQL from which it is inspired.

A DQL query finds nodes based on search criteria, matches patterns in the graph and returns the node attributes, relationships specified in the query.

A DQL query has
- an optional parameterization, ie a name and a list of parameters
- an opening curly bracket
- at least one [query block]({{< relref "#query-block" >}}), but can contain many blocks
- optional var blocks
- a closing curly bracket

{{<figure  src="/images/dql-syntax/query-syntax-1.png"  alt="DQL Query with parameterization">}}


### Query parameterization
**Parameters**
* must  have a name starting with a `$` symbol.
* must have a type `int`, `float`, `bool` or `string`.
* may have a default value. In the example below, `$age` has a default value of `95`
* may be mandatory by suffixing the type with a `!`. Mandatory parameters can't have a default value.

Parameters can be used in the query where a string, float, int or bool value are needed.

You can also use a variable holding ``uids`` by using a string variable and by providing the value as a quoted list in square brackets:  
`query title($uidsParam: string = "[0x1, 0x2, 0x3]") { ... }`.



**Error handling**
When submitting a query using parameters, Dgraph responds with errors if
* A parameter value is not parsable to the given type.
* The query is using a parameter that is not declared.
* A mandatory parameter is not provided


The query parameterization is optional. If you don't use parameters you can omit it and send only the query blocks.

{{<figure  src="/images/dql-syntax/query-syntax-2.png"  alt="DQL Query without parameters">}}
{{% notice "note" %}}The current documentation is usually using example of queries without parameters. {{% /notice %}}

If you execute this query in our [Movies demo database]({{< relref "running-examples.md" >}}) you can see that Dgraph will return a JSON structure similar to the request :
{{<figure  src="/images/dql-syntax/query-syntax-3.png"  alt="DQL response structure">}}

### Query block

A query block specifies information to retrieve from Dgraph.

A query block
- must have name
- must have a node criteria defined by the keyword ``func:``
- may have ordering and pagination information
- may have a combination of filters (to apply to the root nodes)
- must provide the list of attributes and relationships to fetch for each node matching the root nodes.

Refer to [pagination]({{< relref "pagination.md" >}}), [ordering]({{< relref "sorting.md" >}}), [connecting filters]({{< relref "filter.md#connecting-filters" >}}) for more information.

For each relationships to fetch, the query is using a nested block.

A nested block
- may specify filters to apply on the related nodes
- may specify criteria on the relationships attributes using [filtering on facets]({{< relref "facets.md#filtering-on-facets" >}}))
- provides the list of relationship attributes ([facets]({{< relref "facets.md" >}}))) to fetch.
- provides the list of attributes and relationships to fetch for the related nodes.

A nested block may contain another nested block, and such at any level.

### Multiple query blocks
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

### Escape characters in predicate names
 If your predicate has special characters, wrap it with angular brackets `< >` in the query. 
 
 E.g.
 `<https://myschema.org#name>
 `

### Formatting options
Dgraph returns the attributes and relationships that you specified in the query. You can specify an alternate name for the result by using [aliases]({{< relref "alias.md" >}}).

You can flatten the response structure at any level using [@normalize]({{< relref "normalize-directive.md" >}}) directive.

Entering the list of all the attributes you want to fetch could be fastidious for large queries or repeating blocks : you may take advantage of [fragments]({{< relref "fragments.md" >}}) and the [expand function]({{< relref "expand-predicates.md" >}}).

### Node criteria (used by root function or by filter)

Root criteria and filters are using [functions]({{< relref "functions.md" >}}) applied to nodes attributes or variables.

Dgraph offers functions for
- testing string attributes
  - term matching : [allofterms]({{< relref "functions.md#allofterms" >}}), [anyofterms]({{< relref "functions.md#anyofterms" >}})
  - regular Expression : [regexp]({{< relref "functions.md#regular-expressions" >}})
  - fuzzy match : [match]({{< relref "functions.md#fuzzy-matching" >}})
  - full-text search : [alloftext]({{< relref "functions.md#full-text-search" >}})
- testing attribute value
  - equality : [eq]({{< relref "functions.md#equal-to" >}})
  - inequalities : [le,lt,ge,gt]({{< relref "functions.md#less-than-less-than-or-equal-to-greater-than-and-greater-than-or-equal-to" >}})
  - range : [between]({{< relref "functions.md#between" >}})
- testing if a node
  - has a particular predicate (an attribute or a relation) : [has]({{< relref "functions.md#has" >}})
  - has a given UID : [uid]({{< relref "functions.md#uid" >}})
  - has a relationship to a given node : [uid_in]({{< relref "functions.md#uid_in" >}})
  - is of a given type : type()
- testing the number of node relationships
  - equality : [eq]({{< relref "functions.md#equal-to" >}})
  - inequalities : [le,lt,ge,gt]({{< relref "functions.md#less-than-less-than-or-equal-to-greater-than-and-greater-than-or-equal-to" >}})
- testing geolocation attributes
  - if geo location is within distance : [near]({{< relref "functions.md#near" >}})
  - if geo location lies within a given area : [within]({{< relref "functions.md#within" >}})
  - if geo area contains a given location : [contains]({{< relref "functions.md#contains" >}})
  - if geo area intersects a given are : [intersects]({{< relref "functions.md#intersects" >}})


### Var block

  Variable blocks (`var` blocks) start with the keyword `var` instead of a block name.

  var blocks are not reflected in the query result. They are used to compute [query-variables]({{< relref "variables.md#query-variables" >}}) which are lists of node UIDs, or [value-variables]({{< relref "variables.md#value-variables" >}}) which are maps from node UIDs to the corresponding scalar values.

  Note that query-variables and value-variables can also be computed in query blocks. In that case, the query block is used to fetch and return data, and to define some variables which must be used in other blocks of the same query.

  Variables may be used as functions parameters in filters or root criteria in other blocks.

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

### Summarizing functions

When dealing with array attributes or with relationships to many node, the query may use summary functions [count]({{< relref "count.md" >}}) , [min]({{< relref "aggregation.md#min" >}}), [max]({{< relref "aggregation.md#max" >}}), [avg]({{< relref "aggregation.md#sum-and-avg" >}}) or [sum]({{< relref "aggregation.md#sum-and-avg" >}}).

The query may also contain [mathematical functions]({{< relref "variables.md#math-on-value-variables" >}}) on value variables.

Summary functions can be used in conjunction with [@grouby]({{< relref "groupby.md" >}}) directive to create aggregated value variables.

The query may contain **anonymous block** to return computed values. **Anonymous block** don't have a root criteria as they are not used to search for nodes but only to returned computed values.

### Graph traversal

When you specify nested blocks and filters you basically describe a way to traverse the graph.

[@recurse]({{< relref "recurse-query.md" >}}) and [@ignorereflex]({{< relref "ignorereflex-directive.md" >}}) are  directives used to optionally configure the graph traversal.

### Pattern matching
Queries with nested blocks with filters may be turned into pattern matching using [@cascade]({{< relref "cascade-directive.md" >}}) directive : nodes that don’t have all attributes and all relationships specified in the query at any sub level are not considered in the result. So only nodes "matching" the complete query structure are returned.

### Graph algorithms
The query can ask for the shortest path between a source (from) node and destination (to) node using the [shortest]({{< relref "kshortest-path-queries.md" >}}) query block.

### Comments
Anything on a line following a `#` is a comment
