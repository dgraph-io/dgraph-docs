+++
title = "DQL Overview"
aliases = ["/dql-overview"]
[menu.main]
  name = "DQL Overview"
  identifier = "dql-overview"
  parent = "dql"
  weight = 1
+++

Dgraph Query Language (DQL) is Dgraph's proprietary language to add, modify, delete and fetch data.

Fetching data is done through **DQL Queries**. Adding, modifying or deleting data is done through **DQL Mutations**.

This overview explains the structure of DQL Queries and mutations.

## DQL query structure
DQL is **declarative**, which means that queries return a response back in a similar shape to the query. It gives the client application the control of what it gets: the request return exactly what you ask for, nothing less and nothing more. In this, DQL is similar to GraphQL from which it is inspired.

A DQL query finds nodes based on search criteria, matches patterns in the graph and returns the node attributes, relationships specified in the query.

A DQL query
- has an optional parameterization, ie a name and a list of parameters
- an opening curly bracket
- query or var blocks with at least one query block
- an closing curly bracket

#### Query parameterization

The query can optionally use variables (parameters). They must be defined using
* `query title($<param name>: <type>[! | ( = "default value")], @param2) { ... }`


##### Variables
* must  have a name starting with a `$` symbol.
* must have a type `int`, `float`, `bool` or `string`.
* may have a default value. In the example below, `$age` has a default value of `95`
* may be mandatory by suffixing the type with a `!`. Mandatory parameters can't have a default value.

Variables can be used in the query where a string, float, int or bool value are needed.

You can also use a variable holding ``uids`` by using a string variable and by providing the value as a quoted list in square brackets:  
`query title($uidsParam: string = "[0x1, 0x2, 0x3]") { ... }`.



##### Variables error handling
When submitting a query using parameters, Dgraph responds with errors if
* A parameter value is not parsable to the given type.
* The query is using a parameter that is not declared.
* A mandatory parameter is not provided



#### Query block

A query block specifies information to retrieve from Dgraph.

A query block
- must have name
- must have a root nodes definition
- may have a combination of node filters (to apply to the root nodes)
- provides the list of attributes and relationships to return for each node matching the root nodes.

For each relationships, the query may specify node filters which apply to the related nodes and use nested block to provide the list of attributes and relationships to return for the related nodes.

A query can use any level of nested blocks.

#### root nodes definition
- must have a root criteria defined by the key word ``func:``
- may have pagination
- may have ordering
- may have filters


##### node criteria (used by root function or by filter)
- text
  - term matching with allofterms(), anyofterms
  - Regular Expressions regexp
  - match,
  - Full-Text Search alloftext
- Inequalities
- presence of an attribute or relation has()
- node ID : uid()
- has a relation to a given node : uid_in()
- type()
- predicate value test : eq,
(func: , first: ,after: | offset:, orderasc: <attribute>,
A query block starts with root criteria defining the initial set of nodes against which the graph matching and filtering is applied.

{{% notice "note" %}}See more about Queries in [Queries design concept]({{< relref "design-concepts/concepts.md#queries" >}}) {{% /notice %}}



## Returning Values

Each query has a name, specified at the query root, and the same name identifies the results.

If an edge is of a value type, the value can be returned by giving the edge name.

Query Example: In the example dataset, edges that link movies to directors and actors, movies have a name, release date and identifiers for a number of well known movie databases.  This query, with name `bladerunner`, and root matching a movie name, returns those values for the early 80's sci-fi classic "Blade Runner".

{{< runnable >}}
{
  bladerunner(func: eq(name@en, "Blade Runner")) {
    uid
    name@en
    initial_release_date
    netflix_id
  }
}
{{< /runnable >}}

The query first searches the graph, using indexes to make the search efficient, for all nodes with a `name` edge equaling "Blade Runner".  For the found node the query then returns the listed outgoing edges.

Every node had a unique 64-bit identifier.  The `uid` edge in the query above returns that identifier.  If the required node is already known, then the function `uid` finds the node.

Query Example: "Blade Runner" movie data found by UID.

{{< runnable >}}
{
  bladerunner(func: uid(0x394c)) {
    uid
    name@en
    initial_release_date
    netflix_id
  }
}
{{< /runnable >}}

A query can match many nodes and return the values for each.

Query Example: All nodes that have either "Blade" or "Runner" in the name.

{{< runnable >}}
{
  bladerunner(func: anyofterms(name@en, "Blade Runner")) {
    uid
    name@en
    initial_release_date
    netflix_id
  }
}
{{< /runnable >}}

Multiple IDs can be specified in a list to the `uid` function.

Query Example:
{{< runnable >}}
{
  movies(func: uid(0xb5849, 0x394c)) {
    uid
    name@en
    initial_release_date
    netflix_id
  }
}
{{< /runnable >}}


{{% notice "note" %}} If your predicate has special characters, then you should wrap it with angular
brackets while asking for it in the query. E.g. `<first:name>`{{% /notice %}}

## Expanding Graph Edges

A query expands edges from node to node by nesting query blocks with `{ }`.

Query Example: The actors and characters played in "Blade Runner".  The query first finds the node with name "Blade Runner", then follows  outgoing `starring` edges to nodes representing an actor's performance as a character.  From there the `performance.actor` and `performance.character` edges are expanded to find the actor names and roles for every actor in the movie.
{{< runnable >}}
{
  brCharacters(func: eq(name@en, "Blade Runner")) {
    name@en
    initial_release_date
    starring {
      performance.actor {
        name@en  # actor name
      }
      performance.character {
        name@en  # character name
      }
    }
  }
}
{{< /runnable >}}


## Comments

Anything on a line following a `#` is a comment

## Applying Filters

The query root finds an initial set of nodes and the query proceeds by returning values and following edges to further nodes - any node reached in the query is found by traversal after the search at root.  The nodes found can be filtered by applying `@filter`, either after the root or at any edge.

Query Example: "Blade Runner" director Ridley Scott's movies released before the year 2000.
{{< runnable >}}
{
  scott(func: eq(name@en, "Ridley Scott")) {
    name@en
    initial_release_date
    director.film @filter(le(initial_release_date, "2000")) {
      name@en
      initial_release_date
    }
  }
}
{{< /runnable >}}

Query Example: Movies with either "Blade" or "Runner" in the title and released before the year 2000.

{{< runnable >}}
{
  bladerunner(func: anyofterms(name@en, "Blade Runner")) @filter(le(initial_release_date, "2000")) {
    uid
    name@en
    initial_release_date
    netflix_id
  }
}
{{< /runnable >}}



## Where to go from here
- Follow the [DQL Quickstart]({{< relref "get-started/index.md" >}}) to run some queries and mutations.
- Take the [Tour](https://dgraph.io/tour/) for a guided tour of how to write queries in Dgraph.
- Go to [Clients]({{< relref "clients/_index.md" >}}) to see how to
communicate with Dgraph from your application.
