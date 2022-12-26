+++
title = "DQL Overview"
aliases = ["/dql-overview"]
[menu.main]
  name = "DQL Overview"
  identifier = "dql-overview"
  parent = "dql"
  weight = 1
+++

Dgraph Query Language is Dgraph's proprietary language to insert, update, delete and query data.

## Queries

A DQL query finds nodes based on search criteria, matches patterns in a graph and returns a graph as a result.

A query is composed of nested blocks, starting with a query root.  The root finds the initial set of nodes against which the following graph matching and filtering is applied.

{{% notice "note" %}}See more about Queries in [Queries design concept]({{< relref "design-concepts/concepts.md#queries" >}}) {{% /notice %}}

### Error Codes

When running a DQL query you might get an error message from the `/query` endpoint.
Here we will be focusing on the error `"code"` returned in the JSON error object.

You can usually get two types of error codes:
- [`ErrorInvalidRequest`](#errorinvalidrequest): this error can be either a bad request (`400`) or an internal server error (`500`).
- [`Error`](#error): this is an internal server error (`500`)

For example, if you submit a query with a syntax error, you'll get:

```json
{
  "errors": [
    {
      "message": "while lexing {\nq(func: has(\"test)){\nuid\n}\n} at line 2 column 12: Unexpected end of input.",
      "extensions": {
        "code": "ErrorInvalidRequest"
      }
    }
  ],
  "data": null
}
```
The error `"code"` value is returned with the query response.
In this case, it's a syntax error and the error `code` is `ErrorInvalidRequest`.

##### `Error`

This is a rare code to get and it's always an internal server error (`500`).
This can happen when JSON marsharling is failing (it's returned when the system tries to marshal a Go struct to JSON)

##### `ErrorInvalidRequest`

This is the most common error code that you can get from the `/query` endpoint. This error can be either a bad request (`400`) or an internal server error (`500`).

For example, you can get this error:
- If the query parameter is not being parsed correctly. The query parameter could be:
  - `debug`
  - `timeout`
  - `startTs`
  - `be` (best effort)
  - `ro` (read-only)
  - If the value of these query parameters is incorrect you would get this error code. This is basically a bad request (`400`)
- If the header's `Content-Type` value is not parsed correctly. The only allowed content types in the header are:
  - `application/json`
  - `application/dql`
  - `application/graphql+-` (deprecated)
  - Anything else will be wrongly parsed and end up in a bad request (`400`)
- Query timeout (deadline exceeded). This is an internal server error (`500`)
- Any error in query processing like:
  - syntax error - bad request (`400`)
  - health failing (server not healthy) - internal server error (`500`)
  - Alpha not able to reach zero because of network issue - internal server error (`500`)
  - ACL error (user not found or user does not have privileges) - unauthenticated/unauthorized request (`401` or `403`)
  - if you set `be=true` and `ro=false` - bad request (`400`)
  - any error related to JSON formatting the response - internal server error (`500`)

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
