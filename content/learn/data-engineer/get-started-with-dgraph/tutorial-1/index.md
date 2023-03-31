+++
title = "Get Started with Dgraph - Introduction"
type = "learn"
[menu.learn]
  name = "Introduction"
  identifier = "tutorials-intro"
  parent = "learn-data-engineer-getstarted"
  weight = 1
+++
**Welcome to getting started with Dgraph.**

[Dgraph](https://dgraph.io) is an open-source, transactional, distributed, native Graph Database. Here is the first tutorial of the get started series on using Dgraph.

In this tutorial, we'll learn about:

- Running Dgraph using the `dgraph/standalone` docker image.
- Running the following basic operations using Dgraph's UI Ratel,
 - Creating a node.
 - Creating an edge between two nodes.
 - Querying for the nodes.

Our use case will represent a person named "Ann", age 28, who "follows" in social media, a person named "Ben", age 31.

You can see the accompanying video below.

{{< youtube u73ovhDCPQQ >}}

---

## Running Dgraph

Running the `dgraph/standalone` docker image is the quickest way to get started with Dgraph.
This standalone image is meant for quickstart purposes only.
It is not recommended for production environments.

Ensure that [Docker](https://docs.docker.com/install/) is installed and running on your machine.

Now, it's just a matter of running the following command, and you have Dgraph up and running.

```sh
docker run --rm -it -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
```

### Nodes and Relationships

The mental picture of the use case may be a graph where we have 2 nodes representing the 2 persons and an relationship representing the fact that "Ann" follows "Ben" :


{{<figure class="medium image" src="/images/tutorials/1/gs-1.png" title="A simple graph" alt="A simple graph">}}

Dgraph is using those very same concepts, making it simple to store and manipulate your data.

We will then create two nodes, one representing the information we know about `Ann` and one holding the information about `Ben`.

What we know is the `name` and the `age` of those persons.

We also know that Ann follows Jessica. This will also be stored as a relationship between the two nodes.

### Using Ratel
Launch Ratel image

```sh
docker run --rm -d -p 8000:8000 - dgraph/ratel:latest
```


Just visit [http://localhost:8000](http://localhost:8000) from your browser, and you will be able to access it.

{{% load-img "/images/tutorials/1/gs-2.png" "ratel-1" %}}

We'll be using the Console tab of Ratel.

{{% load-img "/images/tutorials/1/gs-3.png" "ratel-2" %}}

### Mutations using Ratel

The create, update, and delete operations in Dgraph are called mutations.


In Ratel console, select the `Mutate` tab and paste the following mutation into the text area.

```json
{
  "set": [
    {
      "name": "Ann",
      "age": 28,
      "follows": {
        "name": "Ben",
        "age": 31
      }
    }
  ]
}
```

The query above creates an entity and saves the predicates `name` and `age` with the corresponding values.

It also creates a predicate 'follows' for that entity but the value is not a literal (string, int, float, bool).

So Dgraph also creates a second entity that is the object of this predicate. This second entity has itself some predicates (`name` and `age`).


Let's execute this mutation. Click Run!

{{% load-img "/images/tutorials/1/mutate-example.gif" "Query-gif" %}}

You can see in the response that two UIDs (Universal IDentifiers) have been created.
The two values in the `"uids"` field of the response correspond
to the two entities created for "Ann" and "Ben".

### Querying using the has function

Now, let's run a query to visualize the graph which we just created.
We'll be using Dgraph's `has` function.
The expression `has(name)` returns all the entities with a predicate `name` associated with them.

```sh
{
  people(func: has(name)) {
    name
    age
  }
}
```

Go to the `Query` tab this time and type in the query above.
Then, click `Run` on the top right of the screen.

{{% load-img "/images/tutorials/1/query-1.png" "query-1" %}}

Ratel renders a graph visualization of the result.

Just click on any of them, notice that the nodes are assigned UIDs,
matching the ones, we saw in the mutation's response.

You can also view the JSON results in the JSON tab on the right.

{{% load-img "/images/tutorials/1/query-2.png" "query-2" %}}

#### Understanding the query

{{% load-img "/images/tutorials/1/explain-query-2.JPG" "Illustration with explanation" %}}

The first part of the query is the user-defined function name.
In our query, we have named it as `people`. However, you could use any other name.

The `func` parameter has to be associated with a built-in function of Dgraph.
Dgraph offers a variety of built-in functions. The `has` function is one of them.
Check out the [query language guide](https://dgraph.io/docs/query-language) to know more about other built-in functions in Dgraph.

The inner fields of the query are similar to the column names in a SQL select statement or to a GraphQL query!

You can easily specify which predicates you want to get back.

```graphql
{
  people(func: has(name)) {
    name
  }
}
```

Similarly, you can use the `has` function to find all entities with the `age` predicate.

```graphql
{
  people(func: has(age)) {
    name
  }
}
```

### Flexible schema

Dgraph doesn't enforce a structure or a schema. Instead, you can start entering
your data immediately and add constraints as needed.

Let's look at this mutation.

```json
{
  "set": [
    {
      "name": "Balaji",
      "age": 23,
      "country": "India"
    },
    {
      "name": "Daniel",
      "age": 25,
      "city": "San Diego"
    }
  ]
}
```

We are creating two entities, while the first entity has predicates `name`, `age`, and `country`,
the second one has `name`, `age`, and `city`.

Schemas are not needed initially. Dgraph creates
new predicates as they appear in your mutations.
This flexibility can be beneficial, but if you prefer to force your
mutations to follow a given schema there are options available that
we will explore in an next tutorial.

## Wrapping up

In this tutorial, we learned the basics of Dgraph, including how to
run the database, add new entities and predicates, and query them
back.


Check out our next tutorial of the getting started series [here]({{< relref "tutorial-2/index.md" >}}).

## Need Help

* Please use [discuss.dgraph.io](https://discuss.dgraph.io) for questions, feature requests, bugs, and discussions.
