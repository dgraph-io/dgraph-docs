+++
date = "2017-03-20T22:25:17+11:00"
title = "Dgraph types schema"
type = "docs"
weight = 3
aliases = ["/dql/type-system","dql/predicate-types"]
[menu.main]
    identifier = "dql-schema"
    parent = "dql"
+++

Here is an example of Dgraph types schema:
```
name: string @index(term) .
release_date: datetime @index(year) .
revenue: float .
running_time: int .
starring: [uid] .
director: [uid] .
description: string .

description_vector: float32vector @index(hnsw(metric:"cosine")) .

type Person {
  name
}

type Film {
  name
  release_date
  revenue
  running_time
  starring
  director
  description
  description_vector
}
```

The schema contains information about [predicate types](#predicate-types) and [node types](#node-types).


A [predicate]({{< relref "dgraph-glossary.md#Predicate">}}) is the smallest piece of information about an object. A predicate can hold a literal value or a relation to another entity :
- when we store that an entity name is "Alice". The predicate is ``name`` and predicate value is the string "Alice".
- when we store that Alice knows Bob, we may use a predicate ``knows`` with the node representing Alice. The value of this predicate would be the [uid]({{<relref "dgraph-glossary.md#uid">}}) of the node representing Bob. In that case, ``knows`` is a [relationship](#relationship).


Dgraph maintains a list of all predicates names and their type in the **Dgraph types schema**.



## Predicates declaration

The Dgraph Cluster **schema mode** defines if the Dgraph types must be declared before allowing mutations or not:
- In ``strict`` mode, you must declare the predicates before you can run a mutation using those predicates.
- In ``flexible`` mode (which is the default behavior), you can run a mutation without declaring the predicate in the DQL Schema.


{{% notice "note" %}}
When you deploy a [GraphQL API schema]({{< relref "graphql">}}), Dgraph generates all the underlying Dgraph types. 

Refer to [GraphQL and DQL schemas]({{< relref "graphql-dql-schema">}}) in the [GraphQL - DQL interoperability]({{< relref "graphql-dql">}}) section for use cases using both approaches.
{{% /notice %}}

For example, you can run the following mutation (using the [RDF](/dql/dql-syntax/dql-rdf/) notation):
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
In ``strict`` mode, the mutation will return an error if the predicates are not present in the Dgraph types schema.

In ``flexible`` mode, Dgraph will execute the mutation and adds the predicates “character_name” and “has_for_child” to the Dgraph types.


## Predicate types

All predicate types used in a Dgraph cluster are declared in the Dgraph schema.

The Dgraph types schema is the way to specify predicates types and cardinality (if it is a list or not), to instruct Dgraph how to index predicates, and to declare if Dgraph needs to maintain different languages for a string predicate.

A predicate type is either created
- by altering the Dgraph types schema (See [Update Dgraph types](/howto/update-dgraph-types/) )
or
- during a mutation, if the Dgraph Cluster **schema mode** is ``flexible`` and the predicate used is not yet declared.

  If a predicate type isn't declared in the schema, then the type is inferred from the first mutation and added to the schema.

  If the mutation is using [RDF format]({{<relref "#rdf-types" >}}) with an RDF type, Dgraph uses this information to infer the predicate type.

  If no type can be inferred, the predicate type is set to  `default`.

A predicate can hold a literal value ([Scalar type](#scalar-types)) or a relation to another entity ([UID type](#uid-type)).

### Scalar Types

For all triples with a predicate of scalar types the object is a literal.

| Dgraph Type | Go type |
| ------------|:--------|
|  `default`  | string  |
|  `int`      | int64   |
|  `float`    | float   |
|  `string`   | string  |
|  `bool`     | bool    |
|  `dateTime` | time.Time (RFC3339 format [Optional timezone] eg: 2006-01-02T15:04:05.999999999+10:00 or 2006-01-02T15:04:05.999999999)    |
|  `geo`      | [go-geom](https://github.com/twpayne/go-geom)    |
|  `password` | string (encrypted) |


{{% notice "note" %}}Dgraph supports date and time formats for `dateTime` scalar type only if they
are RFC 3339 compatible which is different from ISO 8601(as defined in the RDF spec). You should
convert your values to RFC 3339 format before sending them to Dgraph.{{% /notice  %}}

### Vector Type

The `float32vector` type denotes a vector of floating point numbers, i.e an ordered array of float32.  A node type can contain more than one vector predicate.

Vectors are normaly used to store embeddings obtained from other information through an ML model. When a `float32vector` is [indexed](/dql/predicate-indexing/), the DQL [similar_to](/dql/dql-syntax/functions/#vector-similarity-search) function can be used for similarity search.




### UID Type

The `uid` type denotes a relationship; internally each node is identified by it's UID which is a `uint64`.


### Predicate name rules

Any alphanumeric combination of a predicate name is permitted.
Dgraph also supports [Internationalized Resource Identifiers](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) (IRIs).
You can read more in [Predicates i18n](#predicates-i18n).

{{% notice "note" %}}You can't define type names starting with `dgraph.`, it is reserved as the
namespace for Dgraph's internal types/predicates. For example, defining `dgraph.Student` as a
type is invalid.{{% /notice  %}}

### Special characters

Following characters are accepted if prefixed/suffixed with alphanumeric characters.

```
][&*()_-+=!#$%
```

*Note: You are not restricted to use @ suffix, but the suffix character gets ignored.*


The special characters below are not accepted.

```
^}|{`\~
```


### Predicates i18n
Dgraph supports [Internationalized Resource Identifiers](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) (IRIs) for predicate names and values.

If your predicate is a URI or has language-specific characters, then enclose
it with angle brackets `<>` when executing the schema mutation.

Schema syntax:
```
<职业>: string @index(exact) .
<年龄>: int @index(int) .
<地点>: geo @index(geo) .
<公司>: string .
```

This syntax allows for internationalized predicate names, but full-text indexing still defaults to English.
To use the right tokenizer for your language, you need to use the `@lang` directive and enter values using your
language tag.

Schema:
```
<公司>: string @index(fulltext) @lang .
```
Mutation:
```
{
  set {
    _:a <公司> "Dgraph Labs Inc"@en .
    _:b <公司> "夏新科技有限责任公司"@zh .
    _:a <dgraph.type> "Company" .
  }
}
```
Query:
```
{
  q(func: alloftext(<公司>@zh, "夏新科技有限责任公司")) {
    uid
    <公司>@.
  }
}
```

### Unique Directive


The unique constraint enables us to guarantee that all values of a predicate are distinct. To implement the @unique
directive for a predicate, you should define it in the schema and create an index on the predicate based on its type.
If a user does not add the proper index to the predicate, then Dgraph will return an error. 

Dgraph will automatically include the @upsert directive for the predicate. To enforce this uniqueness constraint,
a predicate must have an index, as explained below. Currently, we only support the @unique directive on newly created
predicates with the data types string and integer.

| Data Type    | Index |
| -------- | ------- |
| string  | hash, exact    |
| int | int     |

This is how you define the unique directive for a predicate.

```
email: string @unique @index(exact)  .
```

### Upsert directive


To use [upsert operations](/howto/upserts/) on a predicate, specify the `@upsert` directive in the schema.

When committing transactions involving predicates with the `@upsert` directive, Dgraph checks index keys for conflicts, helping to enforce uniqueness constraints when running concurrent upserts.

This is how you specify the upsert directive for a predicate.
```
email: string @index(exact) @upsert .
```

### Noconflict directive

The NoConflict directive prevents conflict detection at the predicate level. This is an experimental feature and not a
recommended directive but exists to help avoid conflicts for predicates that don't have high
correctness requirements. This can cause data loss, especially when used for predicates with count
index.

This is how you specify the `@noconflict` directive for a predicate.
```
email: string @index(exact) @noconflict .
```

### Predicate types from RDF Types

As well as implying a schema type for a first mutation, an RDF type can override a schema type for storage.
Dgraph supports a number of [RDF](/dql/dql-syntax/dql-rdf/) types.

If a predicate has a schema type and a mutation has an RDF type with a different underlying Dgraph type, the convertibility to schema type is checked, and an error is thrown if they are incompatible, but the value is stored in the RDF type's corresponding Dgraph type.  Query results are always returned in schema type.

For example, if no schema is set for the `age` predicate.  Given the mutation
```
{
 set {
  _:a <age> "15"^^<xs:int> .
  _:b <age> "13" .
  _:c <age> "14"^^<xs:string> .
  _:d <age> "14.5"^^<xs:string> .
  _:e <age> "14.5" .
 }
}
```
Dgraph:

* sets the schema type to `int`, as implied by the first triple,
* converts `"13"` to `int` on storage,
* checks `"14"` can be converted to `int`, but stores as `string`,
* throws an error for the remaining two triples, because `"14.5"` can't be converted to `int`.

### Password type

A password for an entity is set with setting the schema for the attribute to be of type `password`.  Passwords cannot be queried directly, only checked for a match using the `checkpwd` function.
The passwords are encrypted using [bcrypt](https://en.wikipedia.org/wiki/Bcrypt).

For example: to set a password, first set schema, then the password:
```
pass: password .
```

```
{
  set {
    <0x123> <name> "Password Example" .
    <0x123> <pass> "ThePassword" .
  }
}
```

to check a password:
```
{
  check(func: uid(0x123)) {
    name
    checkpwd(pass, "ThePassword")
  }
}
```

output:
```
{
  "data": {
    "check": [
      {
        "name": "Password Example",
        "checkpwd(pass)": true
      }
    ]
  }
}
```

You can also use alias with password type.

```
{
  check(func: uid(0x123)) {
    name
    secret: checkpwd(pass, "ThePassword")
  }
}
```

output:
```
{
  "data": {
    "check": [
      {
        "name": "Password Example",
        "secret": true
      }
    ]
  }
}
```
## Predicate indexing

The schema is also used to set [predicates indexes](/dql/predicate-indexing/) which are required to apply [filtering functions](/dql/dql-syntax/functions/) in DQL queries.

## Node types
Node types are declared along with [predicate types](#predicate-types) in the Dgraph types schema.

Node types are optional.

### Node type definition

Node type declares the list of predicates that could be present in a Node of this type. Node type are defined using the following syntax:

```
name: string @index(term) .
dob: datetime .
home_address: string .
friends: [uid] .

type Student {
  name
  dob
  home_address
  friends
}
```

{{% notice "note" %}}All predicates used in a type must be defined in the Dgraph types schema itself.{{%/ notice  %}}

{{% notice "tips" %}}Different node types can use the same predicates.{{%/ notice  %}}

### Reverse predicates
Reverse predicates can also be included inside a type definition. For example, the following schema, declares that a node of type Child may have a ``~children`` inverse relationhsip. .

```
children: [uid] @reverse .
name: string @index(term) .
type Parent {
  name
  children
}
type Child {
  name
  <~children>
}
```
{{% notice "tip" %}}
Predicates with special caracter are enclosed with angle brackets `<>`
{{% /notice  %}}

### Node type attribution
A node is given a type by setting the ``dgraph.type`` predicate value to the type name. 

A node may be given many types, ``dgraph.type`` is an array of strings.

{{% notice "note" %}} DQL types is only declarative are not enforced by Dgraph. In DQL, 
- you can always add node without a ``dgraph.type`` predicate, that is without a type.
- you can always add a predicate to a node that is not declared in the predicate list of the node type. 
{{% /notice  %}}

Here's an example of mutation to set the types of a node:

```
{
  set {
    _:a <name> "Garfield" .
    _:a <dgraph.type> "Pet" .
    _:a <dgraph.type> "Animal" .
  }
}
```

### When to use node types

Node types are optional, but there are two use cases where actually knowing the list of potential predicates of a node is necessary:
- deleting all the information about a node: this is the `delete { <uid> * * . }` mutation.
- retrieving all the predicates of a given node: this is done using the [expand(_all_)](/dql/dql-syntax/expand-predicates/) feature of DQL.

The Dgraph node types are used in those 2 use cases: when executing the `delete all predicates` mutation or the `expand all` query, Dgraph will check if the node has a ``dgraph.type`` predicate. If so, the engine is using the declared type to find the list of predicates and apply the delete or the expand on all of them.

When nodes have a type (i.e have a `dgraph.type` predicate), then you can use the function [type()](/dql/dql-syntax/dql-query/#node-criteria-used-by-root-function-or-by-filter) in queries.

{{% notice "warning" %}}
`delete { <uid> * * . }` will only delete the predicates declared in the type. You may have added other predicates by running DQL mutation on this node: the node may still exist after the operation if it holds predicates not declared in the node type. `<>`
{{% /notice  %}}












