## Posting Lists and Tablets
Dgraph groups all relationships of a given type together into one data structure called a `tablet`. E.g. in a database of people who are friends with one another, and have first names and last names, the three relations might be: "friend", "firstName", and "lastName". The full set of data for each relation is called a `tablet` and is also a shard in a Dgraph sharded database, because Dgraph shards based on relationships.

Conceptually, a posting list contains all the `Relationships` of one kind corresponding to one `Node`, in the following format:

```
RelationshipName::NodeUID -> sorted list of other Node UIDs // Everything in uint64 representation.
```
Note the composite key "RelationshipName::NodeUID emphasizing that a posting list is the related data for one Node, within one Relationship.

E.g., if we're storing a list of friends, we may have three posting lists:

Node  | Attribute| ValueId
------- |----------|--------
Me      | friend   | person0
Me      | friend   | person1
Me      | friend   | person2
Me      | friend   | person3

Node  | Attribute| ValueId
------- |----------|--------
person1 | friend   | person2
person1 | friend   | Me

Node  | Attribute| ValueId
------- |----------|--------
person2 | friend   | person3

One structure for the (directional) friends of each person.

The tablet for the relation `friend` holds all posting lists for all "friend" relationships in the entire graph. Three in this example. Seeking for `Me` in this tablet would retrieve the single posting list of my friends, namely `[person0, person1, person2, person3]`.

The main advantage of having such a structure is that we have all the data to do one join in one
`tablet` on one server/shard. This means, one RPC to
the machine serving that `Tablet` will be adequate, as documented in [How Dgraph Minmizes Network Calls]({{< relref "minimizing-network-calls" >}}).

Implementation wise, a `Posting List` is a list of `Postings`, and each Posting is either one related Node or one literal value. 
