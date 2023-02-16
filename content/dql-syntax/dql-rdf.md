+++
title = "RDF"
[menu.main]
  name = "RDF"
  identifier = "dql-rdf"
  parent = "dql-syntax"
  weight = 3
+++
Along with JSON, Dgraph supports RDF format to create,  delete, import and export data.

RDF 1.1 is a Semantic Web Standards for data interchange. It expresses statements about resources. The format of these statements is simple and in the form of triples.


A triple has the form
```
<subject> <predicate> <object> .
```

In RDF terminology, a predicate is the smallest piece of information about an object. A predicate can hold a literal value or can describe a relation to another entity :

```
<0x01> <name> "Alice" .
<0x01> <knows> <0x02> .
```
when we store that an entity name is “Alice”. The predicate is `name` and predicate value is the string `"Alice"`. It becomes a node property.
when we store that Alice knows Bob, we may use a predicate `knows` with the node representing Alice. The value of this predicate would be the uid of the node representing Bob. In that case, knows is a relationship.

Each triple ends with a period.  

The subject of a triple is always a node in the graph, while the object may be a node or a value (a literal).


### Blank nodes in mutations
When creating nodes in Dgraph, you should let Dgraph assign a [UID]({{< relref "dgraph-glossary.md#uid" >}}).

However you need to reference the node in the mutation.

Blank nodes in mutations, written `_:identifier`, identify nodes within a mutation. Dgraph creates a UID identifying each blank node.
### Language for string values
Languages are written using `@lang`. For example
```
<0x01> <name> "Adelaide"@en .
<0x01> <name> "Аделаида"@ru .
<0x01> <name> "Adélaïde"@fr .
<0x01> <dgraph.type> "Person" .
```
See also [how language strings are handled in queries]({{< relref "query-language/graphql-fundamentals.md#language-support" >}}).

### Types
You can specify literals type with the standard `^^` separator.  For example
```
<0x01> <age> "32"^^<xs:int> .
<0x01> <birthdate> "1985-06-08"^^<xs:dateTime> .
```

The supported [RDF datatypes](https://www.w3.org/TR/rdf11-concepts/#section-Datatypes) and the corresponding internal type in which the data is stored are as follows.

| Storage Type                                                    | Dgraph type     |
| -------------                                                   | :------------:   |
| &#60;xs:string&#62;                                             | `string`         |
| &#60;xs:dateTime&#62;                                           | `dateTime`       |
| &#60;xs:date&#62;                                               | `datetime`       |
| &#60;xs:int&#62;                                                | `int`            |
| &#60;xs:integer&#62;                                            | `int`            |
| &#60;xs:boolean&#62;                                            | `bool`           |
| &#60;xs:double&#62;                                             | `float`          |
| &#60;xs:float&#62;                                              | `float`          |
| &#60;geo:geojson&#62;                                           | `geo`            |
| &#60;xs:password&#62;                                           | `password`       |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#string&#62;           | `string`         |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#dateTime&#62;         | `dateTime`       |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#date&#62;             | `dateTime`       |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#int&#62;              | `int`            |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#positiveInteger&#62;  | `int`            |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#integer&#62;          | `int`            |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#boolean&#62;          | `bool`           |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#double&#62;           | `float`          |
| &#60;http&#58;//www.w3.org/2001/XMLSchema#float&#62;            | `float`          |




### Facets
####  Creating a list with facets

```sh
{
  set {
    _:Julian <name> "Julian" .
    _:Julian <nickname> "Jay-Jay" (kind="first") .
    _:Julian <nickname> "Jules" (kind="official") .
    _:Julian <nickname> "JB" (kind="CS-GO") .
  }
}
```

```graphql
{
  q(func: eq(name,"Julian")){
    name
    nickname @facets
  }
}
```
Result:
```JSON
{
  "data": {
    "q": [
      {
        "name": "Julian",
        "nickname|kind": {
          "0": "first",
          "1": "official",
          "2": "CS-GO"
        },
        "nickname": [
          "Jay-Jay",
          "Jules",
          "JB"
        ]
      }
    ]
  }
}
```
