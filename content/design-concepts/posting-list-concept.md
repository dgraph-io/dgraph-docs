## Posting Lists and Tablets
Posting lists and tablets are internal storage mechanisms and are generally hidden from users or developers, but logs, core product code, blog posts and discussions about Dgraph may use the terms "posting list" and "tablet."

Posting lists are a form of inverted index. Posting lists correspond closely to the RDF concept of a graph, where the entire graph is a collection of triples, ``<subject> <predicate> <object>``. In this view, a posting list is a list of all triples that share a ``<subject>+<predicate>`` pair.

(Note that in Dgraph docs, we typically use the term "relationship" rather than predicate, but here we will refer to predicates explicitly.) 

The posting lists are grouped by predicate into `tablets`. A tablet therefore has all data for a predicate, for all subject UIDs.

Tablets are the basis for data shards in Dgraph. In the near future, Dgraph may split a single tablet into two shards, but currently every data shard is a single predicate. Every server then hosts and stores a set of tablets. Dgraph will move or allocate different tablets to different servers to achieve balance across a sharded cluster.


### Example
If we're storing friendship relationships among four people, we may have four posting lists represented by the four tables below:

Node    | Attribute| Value
------- |----------|--------
person1 | friend   | person2
person1 | friend   | person4

&nbsp;

Node    | Attribute| Value
------- |----------|--------
person2 | friend   | person1

&nbsp;

Node    | Attribute| Value
------- |----------|--------
person3 | friend   | person2
person3 | friend   | person4

&nbsp;

Node    | Attribute| Value
------- |----------|--------
person4 | friend   | person2
person4 | friend   | person1
person4 | friend   | person3

&nbsp;

The corrsponding posting lists would be something like:

```
person1UID+friend->[person2UID, person4UID]
person2UID+friend->[person1UID]
person3UID+friend->[person2UID, person4UID]
person4UID+friend->[person1UID, person2UID, person3UID]
```
&nbsp;

Similarly, a posting list will also hold all literal value properties for every node. E.g. consider the names of people in these three tables:

Node    | Attribute| Value
------- |----------|--------
person1 | name     | "James"
person1 | name     | "Jimmy"
person1 | name     | "Jim"

&nbsp;

Node    | Attribute| Value
------- |----------|--------
person2 | name     | "Rajiv"

&nbsp;

Node    | Attribute| Value
------- |----------|--------
person3 | name     | "Rachel"

&nbsp;
The posting lists would look like:
```
person1UID+name->["James", "Jimmy", "Jim"]
person2UID+friend->["Rajiv"]
person3UID+friend->["Rachel"]
```
&nbsp;

Note that person4 has no name attribute specified, so that posting list would not exist.

In these examples, two predicates (relations) are defined, and therefore two tablets will exist.

The tablet for the `friend` predicate will hold all posting lists for all "friend" relationships in the entire graph. The tablet for the `name` property will hold all posting lists for `name` in the graph. 

If other types such as Pets or Cities also have a name property, their data will be in the same tablet as the Person names.

### Performance implications

A key advantage of grouping data into predicate-based shards is that we have all the data to do one join in one `tablet` on one server/shard. This means, one RPC to
the machine serving that `tablet` will be adequate, as documented in [How Dgraph Minmizes Network Calls]({{< relref "minimizing-network-calls" >}}).

Posting lists are the unit of data access and caching in Dgraph. The underlying key-value store stores and retrieves posting lists as a unit. Queries that access larger posting lists will use more cache and may incur more disk access for un-cached posting lists.
