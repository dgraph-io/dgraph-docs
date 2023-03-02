+++
date = "2017-03-20T22:25:17+11:00"
title = "Predicate types"
weight = 3
[menu.main]
    parent = "dql"
+++

A predicate is the smallest piece of information about an object. A predicate can hold a literal value or can describe a relation to another entity :
- when we store that an entity name is "Alice". The predicate is ``name`` and predicate value is the string "Alice".
- when we store that Alice knows Bob, we may use a predicate ``knows`` with the node representing Alice. The value of this predicate would be the [uid]{{<relref "dgraph-glossary.md#uid">}}) of the node representing Bob. In that case, ``knows`` is a [relationship](#relationship).


Dgraph maintains a list of all predicates names and their type in the Dgraph schema.

A predicate type is either created
- by an alter operation (See [Update Dgraph types]({{<relref "update-dgraph-types.md">}}) )
or
- during a mutation :
  If a predicate type isn't specified, then the type is inferred from the first mutation.
  If the mutation is using [RDF format]({{<relref "#rdf-types" >}}) with an RDF type, Dgraph uses this information to infer the predicate type.


If no type can be inferred, the predicate type is set to  `default`.


## Scalar Types

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

## UID Type

The `uid` type denotes a relationship; internally each node is identified by it's UID which is a `uint64`.


## Predicate name rules

Any alphanumeric combination of a predicate name is permitted.
Dgraph also supports [Internationalized Resource Identifiers](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) (IRIs).
You can read more in [Predicates i18n](#predicates-i18n).

### Allowed special characters

Single special characters are not accepted, which includes the special characters from IRIs.
They have to be prefixed/suffixed with alphanumeric characters.

```
][&*()_-+=!#$%
```

*Note: You are not restricted to use @ suffix, but the suffix character gets ignored.*

### Forbidden special characters

The special characters below are not accepted.

```
^}|{`\~
```


## Predicates i18n

If your predicate is a URI or has language-specific characters, then enclose
it with angle brackets `<>` when executing the schema mutation.

{{% notice "note" %}}Dgraph supports [Internationalized Resource Identifiers](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) (IRIs) for predicate names and values.{{% /notice  %}}

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


## Upsert directive


To use [upsert operations]({{<relref "howto/upserts.md">}}) on a predicate, specify the `@upsert` directive in the schema.

When committing transactions involving predicates with the `@upsert` directive, Dgraph checks index keys for conflicts, helping to enforce uniqueness constraints when running concurrent upserts.

This is how you specify the upsert directive for a predicate.
```
email: string @index(exact) @upsert .
```

## Noconflict directive

The NoConflict directive prevents conflict detection at the predicate level. This is an experimental feature and not a
recommended directive but exists to help avoid conflicts for predicates that don't have high
correctness requirements. This can cause data loss, especially when used for predicates with count
index.

This is how you specify the `@noconflict` directive for a predicate.
```
email: string @index(exact) @noconflict .
```

## RDF Types

Dgraph supports a number of [RDF]({{< relref "dql-rdf.md" >}}) types.

As well as implying a schema type for a first mutation, an RDF type can override a schema type for storage.

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



## Password type

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
