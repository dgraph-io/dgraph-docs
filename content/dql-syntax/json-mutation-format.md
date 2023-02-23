+++
date = "2017-03-20T22:25:17+11:00"
title = "JSON Mutation Format"
weight = 10
[menu.main]
  parent = "dql-syntax"
  weight = 4
+++
Dgraph supports [Mutations]({{< relref "dql-mutation.md" >}}) in JSON or [RDF]({{< relref "dql-rdf.md" >}}) format.
When using JSON format Dgraph creates nodes and relationships from the JSON structure and handles the assignation of UIDs to nodes.

## Specifying node UIDs

For example, if you run the following mutation 

```dql
   {
   "set": [
     {
      "name": "diggy",
      "dgraph.type": "Mascot"
     }
   ]
 }  
```
You will see that Dgraph responds with 
{{< highlight json "linenos=false,hl_lines=7 " >}}
{
  "data": {
    "code": "Success",
    "message": "Done",
    "queries": null,
    "uids": {
      "dg.3162278161.22055": "0xfffd8d72745f0650"
    }
  }
{{< / highlight >}}

Meaning that Dgraph has created one node from the JSON. It has used the identifier `dg.3162278161.22055` during the transaction. And the final UID value for this node is `0xfffd8d72745f0650`.

You can control the identifier name by specifying a `uid` field in your JSON data and using the notation : 
``` "uid" : "_:<your-identifier>" ```


In the following mutation we are using two JSON objects but as they are refering to the same identifier, Dgraph creates only one node :

```dql
   {
   "set": [
     {
      "uid": "_:diggy",
      "name": "diggy",
      "dgraph.type": "Mascot"
     },
     {
      "uid": "_:diggy",
      "specie": "badger"
     }
   ]
 }  
```

Running this mutation, you can see that Dgraph returns the UID of the created node with the `diggy` identifier :

{{< highlight json "linenos=false,hl_lines=7 " >}}
{
  "data": {
    "code": "Success",
    "message": "Done",
    "queries": null,
    "uids": {
      "diggy": "0xfffd8d72745f0691"
    }
{{< / highlight >}}

Note that the `specie` field is added to the node already created with `name` and `dgraph.type` information.

### Referencing existing nodes

You can use the `"uid"` field to reference an existing node. To do so, you must specify the UID value of the node.


For example:
```dql
   {
   "set": [
     {
      "uid": "0xfffd8d72745f0650",
      "specie": "badger"
     }
   ]
 }  
```

Will add the specie information to the node we have created earlier.


## Language support

To set a string value for a specific lnguage, append the language tag to the field name.
Assuming that `specie` predicate has the @lang directive, the JSON mutation
```dql
   {
   "set": [
     {
      "uid": "_:diggy",
      "name": "diggy",
      "dgraph.type": "Mascot",
      "specie@en" : "badger",
      "specie@fr" : "blaireau"
     }
   ]
 }  
```
Will set the `specie` string predficate in two english and in french.


## Geolocation support

Geo-location data must be specified using keys `type` and `coordinates` in the JSON document. 
The supported types are `Point`, `Polygon`, or `MultiPolygon` . 

```dql
 {
   "set": [
     {
      "name": "diggy",
      "dgraph.type": "Mascot",
      "home" : {
          "type": "Point",
          "coordinates": [-122.475537, 37.769229 ]
       }
     }
   ]
 }    
```





## Relationships

Relationships are simply created from the nested structure of JSON.

For example:
```dql
 {
   "set": [
     {
      "uid": "_:diggy",
      "name": "diggy",
      "dgraph.type": "Mascot",
      "food" : [
        {
          "uid":"_:f1",
          "name": "earthworms"
        },
        {
          "uid":"_:f2",
          "name": "apples"
        }]
     }
   ]
 }

```

Will result in the creation of three nodes and the `food` predicate will be a relationship.

{{< highlight json "linenos=false,hl_lines=6-7 " >}}
{
  "data": {
    "code": "Success",
    "message": "Done",
    "queries": null,
    "uids": {
      "diggy": "0xfffd8d72745f06d7",
      "f1": "0xfffd8d72745f06d8",
      "f2": "0xfffd8d72745f06d9"
    }
    ...
{{< / highlight >}}



You can use references to existing nodes at any level of your nested JSON.




## Forbidden values

The string values `uid(...)`, `val(...)`are not accepted:  



## Deleting literal values

To delete node predicates, specify the UID of the node you are changing and set  
the predicates to delete to the JSON value `null`.

For example, to remove the predicate `name` from node  `0xfffd8d72745f0691` :
```dql
{
   "delete": [
     {
      "uid": "0xfffd8d72745f0691",
      "name": null
     }
   ]
}
```

## Deleting relationship

A relationhsip can be defined with a cardinality of 1 or many (list).
Setting a relationship to `null` removes all the relationships.

```JSON
{
  "uid": "0xfffd8d72745f06d7",
  "food": null
}
```


To delete a single relationhsip in a list, you must specify the target node of the relationship.

```dql
{
   "delete": [
      {
      "uid": "0xfffd8d72745f06d7",
      "food": {
          "uid": "0xfffd8d72745f06d9"
        }
      }
   ]
}

```

deletes only one `food` relationship.


To delete all predicates of a given node :
- make sure the node has a `dgraph.type` predicate 
- the type is defined by the [Dgraph type system]({{< relref "type-system.md" >}})
- run a delete mutation specifying only the uid field :


```JSON
{
   "delete": [
      {
        "uid": "0x123"
      }
   ]
}
```

## Facets

Facets can be created by using the `|` character to separate the predicate
and facet key in a JSON object field name. This is the same encoding schema
used to show facets in query results. E.g.
```JSON
{
  "name": "Carol",
  "name|initial": "C",
  "dgraph.type": "Person",
  "friend": {
    "name": "Daryl",
    "friend|close": "yes",
    "dgraph.type": "Person"
  }
}
```

Facets do not contain type information but Dgraph will try to guess a type from
the input. If the value of a facet can be parsed to a number, it will be
converted to either a float or an int. If it can be parsed as a Boolean, it will
be stored as a Boolean. If the value is a string, it will be stored as a
datetime if the string matches one of the time formats that Dgraph recognizes
(YYYY, MM-YYYY, DD-MM-YYYY, RFC339, etc.) and as a double-quoted string
otherwise. If you do not want to risk the chance of your facet data being
misinterpreted as a time value, it is best to store numeric data as either an
int or a float.

## Deleting Facets

To delete a Facet, overwrite it :  when you run a mutation for the same entity without a facet, the existing facet will be deleted automatically.





## Handling arrays 

To create a predicate as a list of string:

```JSON
{
   "set": [
    {
      "testList": [
        "Grape",
        "Apple",
        "Strawberry",
        "Banana",
        "watermelon"
      ]
    }
   ]
}
```

Assuming `0x06` is the UID of the node created.

To remove one value from the list :

```JSON
{
  "delete": {
    "uid": "0x6", #UID of the list.
    "testList": "Apple"
  }
}
```

To remove multiple multiple values:
```JSON
{
  "delete": {
    "uid": "0x6",
    "testList": [
          "Strawberry",
          "Banana",
          "watermelon"
        ]
  }
}
```

To add a value :

```JSON
{
   "uid": "0x6", #UID of the list.
   "testList": "Pineapple"
}
```

## Facets in List
Schema:
```sh
<name>: string @index(exact).
<nickname>: [string] .
```
To create a List-type predicate you need to specify all value in a single list. Facets for all
predicate values should be specified together. It is done in map format with index of predicate
values inside list being map key and their respective facets value as map values. Predicate values
which does not have facets values will be missing from facets map. E.g.
```JSON
{
  "set": [
    {
      "uid": "_:Julian",
      "name": "Julian",
      "nickname": ["Jay-Jay", "Jules", "JB"],
      "nickname|kind": {
        "0": "first",
        "1": "official",
        "2": "CS-GO"
      }
    }
  ]
}
```
Above you see that we have three values ​​to enter the list with their respective facets.
You can run this query to check the list with facets:
```graphql
{
   q(func: eq(name,"Julian")) {
    uid
    nickname @facets
   }
}
```
Later, if you want to add more values ​​with facets, just do the same procedure, but this time instead of using Blank-node you must use the actual node's UID.
```JSON
{
  "set": [
    {
      "uid": "0x3",
      "nickname|kind": "Internet",
      "nickname": "@JJ"
    }
  ]
}
```
And the final result is:
```JSON
{
  "data": {
    "q": [
      {
        "uid": "0x3",
        "nickname|kind": {
          "0": "first",
          "1": "Internet",
          "2": "official",
          "3": "CS-GO"
        },
        "nickname": [
          "Jay-Jay",
          "@JJ",
          "Jules",
          "JB"
        ]
      }
    ]
  }
}
```


