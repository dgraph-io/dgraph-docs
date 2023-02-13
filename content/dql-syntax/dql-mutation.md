+++
title = "DQL mutation"
[menu.main]
  name = "DQL mutation"
  identifier = "dql-mutation"
  parent = "dql-syntax"
  weight = 2
+++

Dgraph Query Language (DQL) is Dgraph's proprietary language to add, modify, delete and fetch data.

Fetching data is done through [DQL Queries]({{< relref "dql-query.md" >}}). Adding, modifying or deleting data is done through ***DQL Mutations***.

This overview explains the structure of DQL Mutations and provides links to the appropriate DQL reference documentation.


DQL mutations support JSON or [RDF]({{< relref "dql-rdf.md" >}}) format.

### Add data
In DQL, you add data using a set mutation, identified by the `set` keyword.
{{% tabs %}} {{< tab "JSON" >}}
```dql
   {
   "set": [
     {
       "name":"Star Wars: Episode IV - A New Hope",
       "release_date": "1977-05-25",
       "director": {
         "name": "George Lucas",
         "dgraph.type": "Person"
       },
       "starring" : [
         {
           "name": "Luke Skywalker"
         },
         {
           "name": "Princess Leia"
         },
         {
           "name": "Han Solo"
         }
       ]
     },
     {
       "name":"Star Trek: The Motion Picture",
       "release_date": "1979-12-07"
     }
   ]
 }  
```
{{% /tab %}}
{{< tab "RDF" >}}
```
{
  set {
    # triples in here
    _:n1 <name> "Star Wars: Episode IV - A New Hope" .
    _:n1 <release_date>  "1977-05-25" .
    _:n1 <director> _:n2 .
    _:n2 <name> "George Lucas" .

  }
}
```

triples are in [RDF]({{< relref "dql-rdf.md" >}}) format.

####  Node reference
A mutation can include a blank nodes as an identifier for the subject or object, or a known UID.
```
{
  set {
    # triples in here
    <0x632ea2> <release_date>  "1977-05-25" .
  }
}
```
will add the `release_date` information to the node identified by UID `0x632ea2`.

####  language support
```
{
  set {
    # triples in here
    <0x632ea2> <name>  "Star Wars, épisode IV : Un nouvel espoir"@fr .
  }
}
```

{{% /tab %}}
{{% /tabs %}}


### delete data
A delete mutation, identified by the `delete` keyword, removes
[triples](/mutations/triples) from the store.

For example, if the store contained the following:
```RDF
<0xf11168064b01135b> <name> "Lewis Carrol"
<0xf11168064b01135b> <died> "1998"
<0xf11168064b01135b> <dgraph.type> "Person" .
```

Then, the following delete mutation deletes the specified erroneous data, and
removes it from any indexes:

```sh
{
  delete {
     <0xf11168064b01135b> <died> "1998" .
  }
}
```

#### Wildcard delete

In many cases you will need to delete multiple types of data for a predicate.
For a particular node `N`, all data for predicate `P` (and all corresponding
indexing) is removed with the pattern `S P *`.

```sh
{
  delete {
     <0xf11168064b01135b> <author.of> * .
  }
}
```

The pattern `S * *` deletes all the known edges out of a node, any reverse edges
corresponding to the removed edges, and any indexing for the removed data.

{{% notice "note" %}} For mutations that fit the `S * *` pattern, only
predicates that are among the types associated with a given node (using
`dgraph.type`) are deleted. Any predicates that don't match one of the
node's types will remain after an `S * *` delete mutation.{{% /notice %}}

```sh
{
  delete {
     <0xf11168064b01135b> * * .
  }
}
```

If the node `S` in the delete pattern `S * *` has only a few predicates with a
type defined by `dgraph.type`, then only those triples with typed predicates are
deleted. A node that contains untyped predicates will still exist after a
`S * *` delete mutation.

{{% notice "note" %}} The patterns `* P O` and `* * O` are not supported because
it's inefficient to store and find all the incoming edges. {{% /notice %}}

#### Deletion of non-list predicates

Deleting the value of a non-list predicate (i.e a 1-to-1 relationship) can be
done in two ways.

* Using the [wildcard delete](#wildcard-delete) (star notation)
 mentioned in the last section.
* Setting the object to a specific value. If the value passed is not the
current value, the mutation will succeed but will have no effect. If the value
passed is the current value, the mutation will succeed and will delete the
non-list predicate.

For language-tagged values, the following special syntax is supported:

```
{
  delete {
    <0x12345> <name@es> * .
  }
}
```

In this example, the value of the `name` field that is tagged with the language
tag `es` is deleted. Other tagged values are left untouched.



### Comments
Anything on a line following a `#` is a comment
