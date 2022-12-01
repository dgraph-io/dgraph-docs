+++
title = "DQL Quickstart"
aliases = ["/get-started-old"]
[menu.main]
  name = "DQL quickstart"
  identifier = "get-started"
  parent = "dql"
  weight = 2
+++

This is a quickstart guide to run Dgraph. For an interactive walkthrough, take the [tour](https://dgraph.io/tour/).

{{% notice "note" %}}
[DQL](https://dgraph.io/docs/main/query-language/#graphql) is a powerful query language of Dgraph,
which is a variation of [GraphQL](https://graphql.org/), a query language created by Facebook.
For GraphQL quickstart information see, [dgraph.io/graphql](https://dgraph.io/graphql). This guide is not recommended for production environment.
{{% /notice %}}

This guide helps you:

* Obtain a basic understanding of DQL principles
* Alter a schema that represents the structure of the data set
* Run an instance of Dgraph Server that lets you execute queries against your schema


## Step 1: Run Dgraph

The easiest way to get Dgraph up and running is using the `dgraph/standalone` docker image.
Follow the Docker [install instructions](https://docs.docker.com/install) to install
Docker if you don't have it already.

1. Create a folder to store Dgraph data outside of the container, as follows:

   ```sh
    mkdir -p ~/dgraph
   ``` 
1. Start a standalone instance of Dgraph in Docker:

    ```sh
    docker run --rm -it -p "8080:8080" -p "9080:9080" -v ~/dgraph:/dgraph "dgraph/standalone:{{< version >}}"
    ```
    This starts a single container with **Dgraph Alpha** and **Dgraph Zero**. The Dgraph data required for this quickstart is located in a folder named *dgraph* of your *home directory*.
  
1. Access **Ratel** at https://play.dgraph.io. It allows browser-based queries, mutations and visualizations.

1. To connect Ratel with your Dgraph cluster add `http://localhost:8080` in the **Dgraph server URL** field of
   the **Dgraph Server Connection** dialog in Ratel. To learn more about using Ratel, see [Connection]({{< relref "ratel/connection.md">}}).

1. Click **Connect**.

### Step 2: Run Mutation

Changing the data stored in Dgraph is a mutation. Dgraph supports mutation for two kinds of data: RDF and JSON. 
The dataset on which you can run in the mutation is a movie graph and entities of the type directors, actors, genres, or movies. Store the data in the graph using the RDF mutation that stores information about the first three releases of the the ''Star Wars''series and one of the ''Star Trek'' movies.

To store data in Dgraph, in the **Console** page, click **Mutate** tab and paste the following:
   
   ```dql
  {
   set {
    _:luke <name> "Luke Skywalker" .
    _:luke <dgraph.type> "Person" .
    _:leia <name> "Princess Leia" .
    _:leia <dgraph.type> "Person" .
    _:han <name> "Han Solo" .
    _:han <dgraph.type> "Person" .
    _:lucas <name> "George Lucas" .
    _:lucas <dgraph.type> "Person" .
    _:irvin <name> "Irvin Kernshner" .
    _:irvin <dgraph.type> "Person" .
    _:richard <name> "Richard Marquand" .
    _:richard <dgraph.type> "Person" .

    _:sw1 <name> "Star Wars: Episode IV - A New Hope" .
    _:sw1 <release_date> "1977-05-25" .
    _:sw1 <revenue> "775000000" .
    _:sw1 <running_time> "121" .
    _:sw1 <starring> _:luke .
    _:sw1 <starring> _:leia .
    _:sw1 <starring> _:han .
    _:sw1 <director> _:lucas .
    _:sw1 <dgraph.type> "Film" .

    _:sw2 <name> "Star Wars: Episode V - The Empire Strikes Back" .
    _:sw2 <release_date> "1980-05-21" .
    _:sw2 <revenue> "534000000" .
    _:sw2 <running_time> "124" .
    _:sw2 <starring> _:luke .
    _:sw2 <starring> _:leia .
    _:sw2 <starring> _:han .
    _:sw2 <director> _:irvin .
    _:sw2 <dgraph.type> "Film" .

    _:sw3 <name> "Star Wars: Episode VI - Return of the Jedi" .
    _:sw3 <release_date> "1983-05-25" .
    _:sw3 <revenue> "572000000" .
    _:sw3 <running_time> "131" .
    _:sw3 <starring> _:luke .
    _:sw3 <starring> _:leia .
    _:sw3 <starring> _:han .
    _:sw3 <director> _:richard .
    _:sw3 <dgraph.type> "Film" .

    _:st1 <name> "Star Trek: The Motion Picture" .
    _:st1 <release_date> "1979-12-07" .
    _:st1 <revenue> "139000000" .
    _:st1 <running_time> "132" .
    _:st1 <dgraph.type> "Film" .
   }
  }  
   ```

### Step 3: Alter Schema

Alter the schema to add indexes on some of the data so queries can use term matching, filtering and sorting.
In the **Schema** page, click **Bulk Edit**, and paste the schema, and click **Apply Schema**.

```dql
name: string @index(term) .
release_date: datetime @index(year) .
revenue: float .
running_time: int .
starring: [uid] .
director: [uid] .

type Person {
  name
}

type Film {
  name
  release_date
  revenue
  running_time
  starring
  director
}
```
### Step 4: Run Queries

To Get all movies, in the **Console** page, click **Query** tab and run this query: 
```dql
{
 me(func: has(starring)) {
   name
  }
}
```
The query lists all movies that have a `starring` edge.

A Graph output appears:

{{% load-img "/images/deploy/query1.png" "graph of query1" %}}

To get all "Star Wars" movies released after "1980" in the **Console** page click **Query** tab and run this query:

```dql
{
  me(func: allofterms(name, "Star Wars"), orderasc: release_date) @filter(ge(release_date, "1980")) {
    name
    release_date
    revenue
    running_time
    director {
     name
    }
    starring (orderasc: name) {
     name
    }
  }
}
```

A Graph output appears:

{{% load-img "/images/deploy/query2.png" "graph of query2" %}}

In these four steps, we set up Dgraph, added some data, set a schema and queried that data .

## Where to go from here

- Go to [Clients]({{< relref "clients/_index.md" >}}) to see how to
communicate with Dgraph from your application.
- Take the [Tour](https://dgraph.io/tour/) for a guided tour of how to write queries in Dgraph.
- A wider range of queries can also be found in the
[Query Language]({{< relref "query-language/_index.md" >}}) reference.
- See [Deploy]({{< relref "deploy/_index.md" >}}) if you wish to run Dgraph
  in a cluster.

## Need Help

* Please use [discuss.dgraph.io](https://discuss.dgraph.io) for questions, issues,
feature requests, and discussions.
