
+++
date = "2017-03-27:12:00:00Z"
title = "Relationships"
type = "docs"
weight = 165
[menu.main]
    parent = "design-concepts"
    identifier = "concept-relationships"
+++


Dgraph stores `relationships` among `nodes` to represent graph structures, and also stores literal properties of `nodes`. 

This makes it easy for Dgraph to ingest the RDF [N-Quad](https://www.w3.org/TR/n-quads/) format, where each line represents

* `Node, RelationName, Node, Label` or
* `Node, RelationName, ValueLiteral, Label`

The first represents relations among entities (nodes in graph terminology) and the second represents the relationship of a Node to all it's named attributes.

Often, the optional `Label` is omitted, and therefore the N-Quad data is also referred to as "triples." When it is included, it represents which `Tenant` or `Namespace` the data lives in within Dgraph.

{{% notice "tip" %}}Dgraph can automatically generate a reverse relation. If the user wants to run
queries in that direction, they would need to define the [reverse relationship]({{< relref "dql-schema.md#reverse-edges" >}})
{{% /notice %}}

For `Relationships`, the subject and object are represented as 64-bit numeric UIDs and the relationship name itself links them: <subjectUID> <relationshipName> <objectUID>.

For literal attributes of a `Node`, the subject must still (and always) be a numeric UID, but the Object will be a primitive value. These can be thought of as <subjectUID> <relationshipName> <value>, where value is not a 64-bit UID, and is instead a: string, float, int, dateTime, geopoint, or boolean.
