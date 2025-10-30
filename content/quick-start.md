+++
title = "Quick Start"
type = "docs"
weight = 2
[menu.main]
  name = "Quick Start"
  identifier = "dql-quick-start"
  parent = ""
  
+++

In this Dgraph quick start guide we walk through creating a graph, inserting
data, and querying the graph using [DQL]({{< relref "dgraph-glossary.md#dql" >}}).

This guide helps you to understand how to:

- Create a new Dgraph graph
- Connect your graph to the Ratel web client
- Add data using mutations
- Query the graph using DQL
- Update the graph schema to support more advanced queries

## Run Dgraph and connect the Ratel web UI

The recommended way to get started with Dgraph for local development is by using
the official Dgraph Docker image.

In this section we'll create a new graph, then we'll connect our new graph to
[Ratel]({{< relref "dgraph-glossary.md#ratel" >}}), the web-based UI for Dgraph.

### Run Dgraph with Docker

The [`dgraph/standalone`](https://hub.docker.com/r/dgraph/standalone) Docker image has everything needed to run Dgraph locally.

Ensure you have [Docker installed](https://www.docker.com/), then run the following command to start a local Dgraph instance:

```bash
docker run --rm -it -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
```

This will create a local Dgraph instance and expose the ports necessary to connect to Dgraph via HTTP and gRPC. Specifically:

* `docker run` - initiates a new Docker container
* `--rm` - automatically removes the container when it exits, helping with cleanup
* `-it` - uses interactive mode to show output of the container
* `-p 8080:8080` - maps port 8080 from the host machine to port 8080 in the Docker container to allow Dgraph HTTP connections
* `-p 9080:9080` - maps port 9080 from the host machine to port 9080 in the Docker container to allow Dgraph gRPC connections
* `dgraph/standalone:latest` - specifies the Docker image to use, this is the official Dgraph image with latest tag

### Connect Ratel

Ratel is a web-based UI dashboard for interacting with Dgraph using Dgraph's query language, [DQL]({{< relref "dgraph-glossary.md#dql" >}})

Run Ratel locally by running the `dgraph/ratel` container with the following command:

```bash
docker run --rm -it -p 8000:8000 dgraph/ratel:latest
```

This will start Ratel. Open your web browser and navigate to `http://localhost:8000`, then enter `http://localhost:8080` for the "Dgraph Conn String". This will allow Ratel to connect to our local Dgraph instance and execute DQL queries.

![Setting up Ratel](/images/dgraph/quickstart/ratel-docker-connection.png)

Now select **Connect** to verify the connection and then select **Continue** to access the Ratel console.

![Setting up Ratel local connection](/images/dgraph/quickstart/ratel-docker-overview.png)

Now we're ready to add data to our graph.

## Add data to the graph with a mutation

Graph databases like Dgraph use a data model called the **property graph**,
which consists of [**nodes**]({{< relref "dgraph-glossary.md#node" >}}),
[**relationships**]({{< relref "dgraph-glossary.md#relationship" >}}) that connect nodes, and key-value
pair **properties** that describe nodes and relationships.

With Dgraph, we use **triples** to describe each piece of our graph, which when
combined together make up our property graph. Triples are composed of a subject,
predicate, and object.

```text
<subject> <predicate> <object> .
```

The subject always refers to a [node]({{< relref "dgraph-glossary.md#node" >}}),
[predicates]({{< relref "dgraph-glossary.md#predicate" >}}) can be a relationship or property, and the
object can be a node or property value. You can read more about triples in the
[RDF section of the docs]({{< relref "dql-rdf.md" >}}), but for now let's move on to
creating data in Dgraph using triples.

Let's create data about movies, characters, and their genres. Here's the
property graph representation of the data we'll create:

![Movie and actor data model](/images/dgraph/quickstart/data-model.png)

### Add mutation in Ratel

The create, update, and delete operations in Dgraph are called mutations.

In the Ratel **Console** page, select the **Mutate** tab, then paste the
following mutation:

```dql
{
    set {

        _:scifi <dgraph.type> "Genre" .
        _:scifi <Genre.name> "Sci-Fi" .

        _:starwars <dgraph.type> "Movie" .
        _:starwars <Movie.title> "Star Wars: Episode IV - A New Hope" .
        _:starwars <Movie.release_date> "1977-05-25"^^<xs:dateTime> .


        _:startrek <dgraph.type> "Movie" .
        _:startrek <Movie.title> "Star Trek: The Motion Picture" .
        _:startrek <Movie.release_date> "1979-12-07"^^<xs:dateTime> .

        _:george <dgraph.type> "Person" .
        _:george <Person.name> "George Lucas" .

        _:luke <dgraph.type> "Character" .
        _:luke <Character.name> "Luke Skywalker" .

        _:leia <dgraph.type> "Character" .
        _:leia <Character.name> "Princess Leia" .

        _:han <dgraph.type> "Character" .
        _:han <Character.name> "Han Solo" .

        _:starwars <Movie.genre> _:scifi .
        _:startrek <Movie.genre> _:scifi .

        _:starwars <Movie.director> _:george .

        _:starwars <Movie.character> _:luke .
        _:starwars <Movie.character> _:leia .
        _:starwars <Movie.character> _:han .

    }
}
```

The preceding DQL mutation uses
[N-Quad RDF format]({{< relref "dql-rdf.md#n-quads-format" >}}) to define the triples that
make up the property graph we want to create.

### View mutation results

Select **Run** to execute the mutation. In the JSON tab we can see the result of
this mutation.

```json
      {
        "data": {
          "code": "Success",
          "message": "Done",
          "queries": null,
          "uids": {
            "george": "0x4",
            "han": "0x7",
            "leia": "0x6",
            "luke": "0x5",
            "scifi": "0x1",
            "startrek": "0x3",
            "starwars": "0x2"
          }
        }
      }
```

Dgraph displays the universal identifiers ([UID]({{< relref "dgraph-glossary.md#uid" >}})) of the
nodes that were created.

## Query the graph

### Query for all movies

In the **Console** page, select the **Query** tab and run this query:

```dql
      {
        movies(func: type(Movie)) {
          Movie.title
          Movie.genre {
            Genre.name
          }
          Movie.director {
            Person.name
          }
          Movie.character {
            Character.name
          }
        }
      }
```

This query searches for all `Movie` nodes as the start of the traversal using
the `type(Movie)` function to define the starting point of our query traversal,
then finds any genres, directors, and characters connected to each movie.

### View results in JSON and graph visualization

In Ratel's JSON tab we can view the results of this query as JSON:

```json
      {
        "data": {
          "movies": [
            {
              "Movie.title": "Star Wars: Episode IV - A New Hope",
              "Movie.genre": [
                {
                  "Genre.name": "Sci-Fi"
                }
              ],
              "Movie.director": [
                {
                  "Person.name": "George Lucas"
                }
              ],
              "Movie.character": [
                {
                  "Character.name": "Luke Skywalker"
                },
                {
                  "Character.name": "Princess Leia"
                },
                {
                  "Character.name": "Han Solo"
                }
              ]
            },
            {
              "Movie.title": "Star Trek: The Motion Picture",
              "Movie.genre": [
                {
                  "Genre.name": "Sci-Fi"
                }
              ]
            }
          ]
        }
      }
```

In the response panel, Select **Graph** to view a graph visualization of the
results of our query:

![Query result graph visualization](/images/dgraph/quickstart/query-result-1.png)

## Update the graph schema and query using an index

The previous query used the `type()` function to find the starting point of our
graph traversal. We can use more complex functions to filter by string
comparison operator, and others, however to use these functions we must first
update the graph schema to create an index on the predicates we want to use in
these functions.

The [function documentation]({{< relref "functions.md" >}}) specifies which kind of
index is needed for each function.

We'll use Ratel to alter the schema to add indexes on some of the data so
queries can use term matching, filtering, and sorting.

### Create an index for movie title

In Ratel's **Schema** page, select **Predicates**. Here we can see all the
predicates used in the graph. A [predicate]({{< relref "dgraph-glossary.md#predicate" >}}) is
Dgraph's internal representation of a node, property, or relationship.

Select the `Movie.title` predicate. Ratel displays details about the predicate
type and indexes.

Change the type to **string** then select **index** and select **term** for the
`Movie.title` predicate, then select **Update** to apply the index.

![Adding an index for movie title](/images/dgraph/quickstart/schema-title.png)

### Create an index for movie release date

Next, we'll create an index for the `Movie.release_date` predicate.

Select the `Movie.release_date` predicate. Change the type to **dateTime**.
Select **index** and choose **year** for the index tokenizer. Click **Update**
to apply the index on the `release-date` predicate.

![Adding an index for movie release date](/images/dgraph/quickstart/schema-date.png)

### Query using indexes

Now let's find all movies with the term "Star" in their title and released
before 1979.

In the **Console** page select the **Query** tab and run this query:

```dql
      {
        movieSearch(func: allofterms(Movie.title, "Star"), orderasc: Movie.release_date) @filter(lt(Movie.release_date, "1979")) {
          Movie.title
          Movie.release_date
          Movie.director {
          Person.name
          }
          Movie.character (orderasc: Character.name) {
          Character.name
          }
        }
      }
```

We can see the JSON result in the JSON tab:

```json
      {
        "data": {
          "movieSearch": [
            {
              "Movie.title": "Star Wars: Episode IV - A New Hope",
              "Movie.release_date": "1977-05-25T00:00:00Z",
              "Movie.director": [
                {
                  "Person.name": "George Lucas"
                }
              ],
              "Movie.character": [
                {
                  "Character.name": "Han Solo"
                },
                {
                  "Character.name": "Luke Skywalker"
                },
                {
                  "Character.name": "Princess Leia"
                }
              ]
            }
          ]
        }
      }
```

And also view the graph visualization of the result in the Graph tab:

![Graph visualization of query result](/images/dgraph/quickstart/query-result-2.png)

Try changing the release date and the search terms conditions to see Dgraph
search and filtering in action.

## Reverse relationship query

### Add reverse relationship

In the previous queries we traversed from the movie node to its connected genre
node, but what if we want to find all movies connected to a genre node? In order
to traverse from a genre node to a movie node we need to explicitly define the
`Movie.genre` predicate as a reverse relationship.

To define a reverse relationship for the `Movie.genre` predicate we'll return to
the Schema page in Ratel, select the `Movie.genre` predicate and toggle the
**reverse** checkbox. Then select **Update** to apply this schema change.

![Define a reverse relationship in the graph schema](/images/dgraph/quickstart/schema-reverse.png)

### Query using the reverse relationship

In a DQL query the `~` operator is used to specify a reverse relationship. To
traverse from a genre node to a movie node we use the syntax `~Movie.genre`.

In this query we find all movies connected to the "Sci-Fi" genre:

```dql
      {
        genreSearch(func: type(Genre)) {
          Genre.name
          movies: ~Movie.genre {
            Movie.title
          }
        }
      }
```

Note that we can also alias the field name to "movies" in our result JSON using
the syntax `movies: ~Movie.genre`.

```json
      {
        "data": {
          "genreSearch": [
            {
              "Genre.name": "Sci-Fi",
              "movies": [
                {
                  "Movie.title": "Star Wars: Episode IV - A New Hope"
                },
                {
                  "Movie.title": "Star Trek: The Motion Picture"
                }
              ]
            }
          ]
        }
      }
```

In this quick start we created a new graph instance using Dgraph, added data,
queried the graph, visualized the results, and updated the schema of our graph.

## Where to go from here

- Learn more about using [DQL]({{< relref "dql-query.md" >}}) to query your graph.
- Go to [Clients](/clients) to see how to communicate with Dgraph
  from your app.
