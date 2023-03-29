+++
title = "GraphQL and DQL schemas"
weight = 1
[menu.main]
  name = "GraphQL and DQL schemas"
  identifier = "graphql-dql-schema"
  parent = "graphql-dql"
+++

The first step in mastering DQL in the context of GraphQL API is probably to understand the fundamental difference between GraphQL schema and DQL schema.

### In GraphQL, the schema is a central notion.
GraphQL is a strongly typed language. Contrary to REST which is organized in terms of endpoints, GraphQL APIs are organized in terms of types and fields. The type system is used to define the schema, which is a contract between client and server.
GraphQL uses types to ensure Apps only ask for what’s possible and provide clear and helpful errors.

In the [GraphQL Quick start]({{<relref "quick-start" >}}), we have used a schema to generate a GraphQL API:
 ```graphql
type Product {
    productID: ID!
    name: String @search(by: [term])
    reviews: [Review] @hasInverse(field: about)
}

type Customer {
    username: String! @id @search(by: [hash, regexp])
    reviews: [Review] @hasInverse(field: by)
}

type Review {
    id: ID!
    about: Product!
    by: Customer!
    comment: String @search(by: [fulltext])
    rating: Int @search
}
```

The API and the engine logic are generated from the schema defining the types of objects we are dealing with, the fields, and the relationships in the form of fields referencing other types.


### In DQL, the schema is just an optional helper 

On the Dgraph custer which has a [schema mode]({{<relref "schema-modes">}}) set to ``flexible`` (which is the default behavior) you can run a mutation without declaring any schema.

For example, you can run the following mutation:
```graphql
{
  set {
    <_:jedi1> <character_name> "Luke Skywalker" .
    <_:leia> <character_name> "Leia" .
    <_:sith1> <character_name> "Anakin" (aka="Darth Vador",villain=true).
    <_:sith1> <has_for_child> <_:jedi1> .
    <_:sith1> <has_for_child> <_:leia> .
  } 
}
```
This mutation using the [RDF]({{< relref "dql-rdf">}}) notation, could be read as:

- There is a first `thing`, that we refer to as `jedi1`, having a `character name` “Luke Skywalker”, 
- There is anothe `thing`, that we refer to as `leia`, having a `character name` “Leia”, 
- There is a thing that we refer to as `sith1`, having a `character name` “Anakin”. The `character_name` has a characteristic `aka` equal to “Darth Vador” and `villain` equal true.
- The thing referred to as `sith1` has a relation `has_for_child` with the thing referred to as `jedi1`.
- The thing referred to as `sith1` has a relation `has_for_child` with the thing referred to as `leia`.

We can see those simple lines as a list of facts. They represent a certain information and knowledge. 

You can retrieve information from Dgraph using a DQL query:
```graphql
{
   characters(func:has(character_name)) {
      character_name @facets
      has_for_child { character_name }
       
  }
     
}
```
Run this query in Ratel and you'll get the following response (in JSON):
```json
{
  "data": {
    "characters": [
      {
        "character_name": "Luke Skywalker"
      },
      {
        "character_name": "Leia"
      },
      {
        "character_name|aka": "Darth Vador",
        "character_name|vilain": true,
        "character_name": "Anakin",
        "has_for_child": [
          {
            "character_name": "Luke Skywalker"
          },
          {
            "character_name": "Leia"
          }
        ]
      }
    ]
  }
...
```


Dgraph handles data as a network of nodes with materialized links between them.
One way to inject information into Dgraph is to simply describe facts in the form of RDF triples and to send a mutation request. 

#### DQL Schema: predicates and types
Dgraph maintains a list of all predicates names and types in the Dgraph schema.
When we execute the previous mutation, Dgraph adds the predicates “character_name” and “has_for_child” because we have saved facts using those predicates.

{{% notice "note" %}} In ``strict`` [mode]({{<relref "schema-modes">}}), you must declare the predicates (update a DQL schema) before you can run a mutation using those predicates.
{{% /notice  %}}

If you do a search with the function "eq" on the predicate "character_name", you will notice that Dgraph will complain that the predicate is not indexed.

The DQL schema is the way to specify predcicates types and cardinality (if it is a list or not),  to instruct Dgraph how to index predicates, and to declare if Dgraph needs to maitain different languages for a string predicate.

DQL schema can be seen as meta-data about predicates.

**What about Types?**

As mentioned you can add "facts" about a node at any moment. This is a key feature allowing Dgraph to be used as a flexible knowledge graph.

There are two use cases where actually knowing the list of potential predicates of a node is necessary:
- deleting all the information about a node : this is the `delete { <uid> * * . }` mutation.
- showing all the predicates without knowing their names : this is the ``expand(_all_)`` feature of DQL.

The DQL type system is only used in those 2 use cases.
A DQL type is just a list of predicates associated with a type name.
A node is given a type by setting the ``dgraph.type`` predicate. ``dgraph.type`` is an array of strings, so a node may be given many types.

When executing the `delete all predicates` mutation or the `expand all` query, Dgraph will check if the node has a ``dgraph.type`` predicate. If so, the engine is using the declared type to find the list of predicates and apply the delete or the expand on all of them.s


{{% notice "note" %}} DQL types is only declarative. In DQL, you can always add a fact to a node using a predicate that is not declared in the type associated with the node. And you can always add node without a ``dgraph.type`` predicate that is without a type.
{{% /notice  %}}


### Schema mapping

When deploying a GraphQL Schema, Dgraph will generates DQL predicates and types for the graph backend.
In order to distinguish a field ``name`` from a type ``Person`` from the field ``name`` of different type (they may have different indexes), Dgraph is using a dotted notation for the DQL schema.

For example, deploying the following GraphQL Schema
```graphql
type Person {
  id: ID
  name: String!
  friends: [Person]
}
```

will lead the the declaration of 3 predicates in the DQL Schema:

- ``Person.id default``
- ``Person.name string``
- ``Person.friends [uid]``

and one DQL type
```
type Person {
   Person.name
   Person.friends
}
```

Once again, the DQL type is just a declaration of the list of predicates that one can expect to be present in a node of having ``dgraph.type`` equal ``Person``.

The default mapping can be customized by using the [@dgraph directive]({{< relref "directive-dgraph" >}}).


#### GraphQL ID type and Dgraph `uid`
Person.id is not part of the Person DQL type: internally Dgraph is using ``uid`` predicate as unique identifier for every node in the graph. Dgraph returns the value of ``uid`` when a GraphQL field of type ID is requested.

#### @search directive and predicate indexes

`@search` directive tells Dgraph what search to build into your GraphQL API. 
```graphql 
type Person {
    name: String @search(by: [hash])
    ...
```
Is simply translated into a prediate index specification in the Dgraph schema:
```
Person.name: string @index(hash) .
```

#### Constraints
DQL does not have 'non nullable' constraint ``!`` nor 'unique' constraint. Constraints on the graph are handled by correctly using ``upsert`` operation in DQL.

#### DQL queries
You can use DQL to query the data generated by the GraphQL API operations.
For example the GraphQL Query
```graphql
query {
  queryPerson {
    id
    name
    friends {
      id
      name
    }
  }
}
```
can be executed in DQL 
```graphql
{
  queryPerson(func: type(Person)) {
    id: uid
    name: Person.name
    friends: Person.friends {
      id: uid
      name: Person.name
    }
  }
}
```

Note that in this query, we are using ``aliases`` such as ``name: Person.name`` to name the predicates in the JSON response,as they are declared in the GraphQL schema.

#### GraphQL Interface
DQL does not have the concept of interfaces. 

Considering the  following GraphQL schema :
```graphql
interface Location {
  id: ID!
  geoloc: Point
}

type Property implements Location {
  price: Float
}
```
The predicates and types generated for a ``Property`` are:


```graphql 
Location.geoloc: geo .
Location.name: string .
Property.price: float .
type Property {
	Location.name
	Location.geoloc
	Property.price
}
```

### Consequences
The fact that the GraphQL API backend is a graph in Dgraph, implies that you can use Dgraph DQL on the data that is also served by the GraphQL API operations.

In particular, you can 
- use Dgraph DQL mutations but also Dgraph's [import tools]({{< relref "importdata">}}) to populate the graph after you have deployed a GraphQL Schema. See [GraphQL data loading]({{<relref "graphql-data-loading.md">}})
- use DQL to query the graph in the context of authorization rules and custom resolvers.
- add knowledge to your graph such as meta-data, score, annotations, ...,  but also relationships or relationships attributes (facets) that could be the result of similarity computation, threat detection a.s.o. The added data could be hidden from your GraphQL API clients but be available to logic written with DQL clients.
- break things using DQL: DQL is powerful and is bypassing constraints expressed in the GraphQL schema. You can for example delete a node predicate that is mandatory in the GraphQL API! Hopefully there are ways to secure who can read/write/delete predicates. ( see the [ACL]({{<relref "access-control-lists">}})) section.
- fix things using DQL: this is especially useful when doing GraphQL Schema updates which require some [data migrations]({{<relref "graphql-data-migration.md">}}). 



