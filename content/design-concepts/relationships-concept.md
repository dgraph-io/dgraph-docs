
## Relationships

Dgraph stores `relationships` among `entities` to represent graph structures, and also stores literal properties of `entities`. 

This makes it easy for Dgraph to ingest the RDF [N-Quad](https://www.w3.org/TR/n-quads/) format, where each line represents

* `Node, RelationName, Node, Label` or
* `Node, RelationName, ValueLiteral, Label`

The first represents relations among entities (nodes in graph terminology) and the second represents the relationship of a Node to all it's named attributes.

Often, the optional `Label` is omitted, and therefore the N-Quad data is also referred to as "triples." When it is included, it represents which `Tenant` or `Namespace` the data lives in within Dgraph.

In our product (the code or the GUI, and also in older documentation) you may see other terminology such as

Edge instead of Relationship
Predicate instead of Relationship
Entity or Vertex instead of Node

Similarly in the RDF spec you'll see 
Subject and Object instead of Node
Predicate instead of Relationship.

This is unavoidable, since graph databases, RDF, and graph theory have separate origins that do not all share terminology.

{{% notice "tip" %}}Dgraph can automatically generate a reverse relation. If the user wants to run
queries in that direction, they would need to define the [reverse relationship]({{< relref "predicate-types.md#reverse-edges" >}})


For `Relationships`, the subject and object are represented as 64-bit numeric UIDs and the relationship name itself links them: <subjectUID> <relationshipName> <objectUID>.

For literal attributes of a `Node`, the subject must still (and always) be a numeric UID, but the Object will be a primitive value. These can be thought of as <subjectUID> <relationshipName> <value>, where value is not a 64-bit UID, and is instead a: string, float, int, dateTime, geopoint, or boolean.
