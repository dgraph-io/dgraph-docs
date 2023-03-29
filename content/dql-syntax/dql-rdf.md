+++
title = "RDF"
[menu.main]
  name = "RDF"
  identifier = "dql-rdf"
  parent = "dql-syntax"
  weight = 3
+++
Dgrpah supports Resource Description Framework (RDF) when creating, importing and exporting data.

[RDF 1.1](https://www.w3.org/RDF/) is a Semantic Web Standard for data interchange defined by the W3C. It expresses statements about resources. The format of these statements is simple and in the form of triples.


A triple has the form
```
<subject> <predicate> <object> .
```

In RDF terminology, each triple represents one fact about a node. 

In Dgraph, the <subject> of a triple is always a node, and must be a numeric UID.  The <object> of a triple may be another node or a literal value:
```
<0x01> <name> "Alice" .
<0x01> <knows> <0x02> .
```
The first triple specifies that a node has a name property of “Alice”. The subject is the UID of the first node, the predicate is `name`, and the object is the literal value string: `"Alice"`. 
The second triple specifies that Alice knows Bob. The subject is again the UID of a node (the "alice" node), the predicate is `knows`, and the object of this triple is the uid of the other node (the "bob" node). When the object is a UID, the triple represents a relationship in Dgraph.

Each triple representation in RDF ends with a period.  

### Blank nodes in mutations
When creating nodes in Dgraph, you often let Dgraph assign the node [UID]({{< relref "dgraph-glossary.md#uid" >}}) by specifing a blank node starting with "_:". All references to the same blank node, such as `_:identifier123`, will identify the same node within a mutation. Dgraph creates a UID identifying each blank node.
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
Dgraph understands standard RDF types specified in RDF using the `^^` separator.  For example
```
<0x01> <age> "32"^^<xs:int> .
<0x01> <birthdate> "1985-06-08"^^<xs:dateTime> .
```

The supported [RDF datatypes](https://www.w3.org/TR/rdf11-concepts/#section-Datatypes) and the corresponding internal Dgraph type are as follows.

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

Dgraph is more expressive than RDF in that it allows properties to be stored on every relation. These properties are called Facets in Dgraph, and dgraph allows an extension to RDF where facet values are incuded in any triple.
####  Creating a list with facets

The following set operation uses a sequence of RDF statements with additional facet information:
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
{{% notice "tip" %}}Dgraph can automatically generate a reverse relation. If the user wants to run
queries in that direction, they would define the [reverse relationship]({{< relref "predicate-types.md#reverse-edges" >}})
## N-quads format
While most RDF data uses only triples (with three parts) an optional fourth part is allowed. This fourth component in RDF is called a graph label, and in Dgraph it must be the UID of the namespace that the data should go into as described in [Multi-tenancy]({{< relref "cloud-multitenancy" >}}).  

## Processing RDF to comply with Dgraph syntax for subjects

While it is valid RDF to specify subjects that are IRI strings, Dgraph requires a numeric UID or a blank node as the subject. If a string IRI is required, Dgraph support them via [xid properties]({{< relref "external-ids-upsert-block" >}}). When importing RDF from another source that does not use numeric UID subjects, it will be required to replace arbitrary subject IRIs with blank node IRIs.

Typically this is done simply by prepending "_:" to the start of the original IRI. So a triple such as:

```<http://abc.org/schema/foo#item1> <http://abc.org/hasRelation> "somevalue"^^xs:string```

may be rewritten as 

```<_:http://abc.org/schema/foo#item1> <http://abc.org/hasRelation> "somevalue"^^xs:string```

Dgraph will create a consistent UID for all references to the uniquely-named blank node. To maintain this uniqueness over multiple data loads, use the [dgraph live]({{< relref "dgraph-glossary.md#uid" >}}) utility with the xid option, or use specific UIDs such as the hash of the IRI in the source RDF directly.

