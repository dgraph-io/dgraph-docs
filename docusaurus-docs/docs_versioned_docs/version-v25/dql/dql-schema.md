---
title: Schema
---

The Dgraph schema defines [predicate types](#predicate-types) and [node types](#node-types).

**Example schema:**

```dql
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

## Predicate Types

Predicates are declared in the Dgraph schema with their type, cardinality, indexes, and language support.

A predicate is created either:
- By altering the schema (see [Update Dgraph types](../admin/admin-tasks/update-dgraph-types/))
- During a mutation, if the cluster's **schema mode** is `flexible` and the predicate doesn't exist

When a predicate type isn't declared:
- The type is inferred from the first mutation
- [RDF type annotations](dql-rdf) are used if present
- Otherwise, the type defaults to `default`

A predicate holds either a literal value ([scalar type](#scalar-types)) or a relationship ([UID type](#uid-type)).

### Scalar Types

| Dgraph Type | Go Type | Notes |
|-------------|---------|-------|
| `default` | string | Default when type cannot be inferred |
| `int` | int64 | |
| `float` | float | |
| `bigfloat` | big.Float| from math/big |
| `string` | string | |
| `bool` | bool | |
| `dateTime` | time.Time | RFC3339 format (e.g., `2006-01-02T15:04:05.999999999+10:00`) |
| `geo` | [go-geom](https://github.com/twpayne/go-geom) | Geographic data |
| `password` | string | Encrypted with bcrypt |

:::note
Dgraph requires RFC 3339 format for `dateTime`, which differs from ISO 8601. Convert values before sending to Dgraph.
:::

### Vector Type

The `float32vector` type stores an ordered array of 32-bit floats, typically used for ML embeddings.

When [indexed](predicate-indexing), vectors enable similarity search using the [similar_to](query/functions#vector-similarity-search) function.

### UID Type

The `uid` type represents a relationship to another node. Internally, each node is identified by a `uint64` UID.

### Predicate Naming

Predicate names can be any alphanumeric combination. Dgraph also supports [Internationalized Resource Identifiers](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) (IRIs) — see [Predicates i18n](#predicates-i18n).

:::note
Names starting with `dgraph.` are reserved for internal use.
:::

**Allowed special characters** (when prefixed/suffixed with alphanumerics):
```
][&*()_-+=!#$%
```

**Not allowed:**
```
^}|{`\~
```

:::tip
The `@` suffix is allowed but ignored.
:::

### Predicates i18n

For predicate names with language-specific characters or URIs, enclose them in angle brackets `<>`:

```dql
<职业>: string @index(exact) .
<年龄>: int @index(int) .
<地点>: geo @index(geo) .
<公司>: string @index(fulltext) @lang .
```

Use the `@lang` directive for proper full-text tokenization:

**Mutation:**
```dql
{
  set {
    _:a <公司> "Dgraph Labs Inc"@en .
    _:b <公司> "夏新科技有限责任公司"@zh .
    _:a <dgraph.type> "Company" .
  }
}
```

**Query:**
```dql
{
  q(func: alloftext(<公司>@zh, "夏新科技有限责任公司")) {
    uid
    <公司>@.
  }
}
```

### Schema Directives

#### `@unique`

Ensures all values of a predicate are distinct. Requires an index.

```dql
email: string @unique @index(exact) .
```

| Data Type | Required Index |
|-----------|----------------|
| `string` | `hash` or `exact` |
| `int` | `int` |

Dgraph automatically adds `@upsert` when `@unique` is specified.

#### `@upsert`

Enables [upsert operations](upserts) with conflict detection on index keys:

```dql
email: string @index(exact) @upsert .
```

#### `@noconflict`

Disables conflict detection for a predicate. Use with caution.

```dql
counter: int @noconflict .
```

:::warning
This is experimental and can cause data loss, especially with count indexes.
:::

### Password Type

Passwords are stored encrypted and can only be verified, not queried directly.

**Schema:**
```dql
pass: password .
```

**Set password:**
```dql
{
  set {
    <0x123> <name> "Password Example" .
    <0x123> <pass> "ThePassword" .
  }
}
```

**Verify password:**
```dql
{
  check(func: uid(0x123)) {
    name
    checkpwd(pass, "ThePassword")
  }
}
```

**Response:**
```json
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

Use an alias for cleaner output:

```dql
{
  check(func: uid(0x123)) {
    name
    secret: checkpwd(pass, "ThePassword")
  }
}
```

### RDF Type Inference

When a mutation includes an RDF type that differs from the schema type, Dgraph checks convertibility and stores in the RDF type's corresponding Dgraph type. Query results return the schema type.

**Example** (no schema defined for `age`):

```dql
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
- Sets schema type to `int` (from first triple)
- Converts `"13"` to `int`
- Stores `"14"` as `string` (convertible to `int`)
- Throws error for `"14.5"` triples (not convertible to `int`)

## Predicate Indexing

Indexes enable [filtering functions](query/functions) in queries. See [Predicate Indexing](predicate-indexing/) for details.

## Facets (Edge Attributes)

Facets are **key-value pairs attached to predicates** rather than nodes. They add properties to attributes and relationships.

### When to Use Facets

Facets are ideal for relationship metadata:
- `friend` edge with `since` timestamp
- `rated` edge with `rating` score
- `member_of` edge with `role`

:::note
Facets cannot be indexed or used in root query functions.
:::

### Facet Types

| Type | Description |
|------|-------------|
| `string` | Text value |
| `bool` | `true` or `false` |
| `int` | 32-bit signed integer |
| `float` | 64-bit floating point |
| `bigfloat` | big.Float from math/big |
| `dateTime` | RFC3339 timestamp |

### Facets Are Not in Schema

Facets are defined inline during mutations — not declared in the schema:

```rdf
_:alice <friend> _:bob (close=true, since=2020-01-01T00:00:00) .
_:alice <car> "MA0123" (since=2006-02-02T13:01:09, first=true) .
```

Dgraph infers facet types from values.

For querying facets, see [Facets in Queries](query/facets).

## Node Types

Node types declare which predicates a node can have. They are optional.

### Defining Node Types

```dql
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

- All predicates in a type must be defined in the schema
- Different types can share predicates

### Reverse Predicates

Include reverse edges using the `~` prefix:

```dql
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

:::tip
Enclose predicates with special characters in angle brackets `<>`.
:::

### Assigning Types to Nodes

Set the `dgraph.type` predicate (supports multiple types):

```dql
{
  set {
    _:a <name> "Garfield" .
    _:a <dgraph.type> "Pet" .
    _:a <dgraph.type> "Animal" .
  }
}
```

:::note
DQL types are declarative only — Dgraph doesn't enforce them. You can:
- Add nodes without `dgraph.type`
- Add predicates not declared in the node's type
:::

### When Node Types Matter

Node types are required for:
- **Delete all predicates**: `delete { <uid> * * . }` uses the type to find predicates
- **Expand all**: [expand(_all_)](query/expand-predicates) uses the type to list predicates
- **Type filtering**: The [type()](query/functions#type) function in queries

:::warning
`delete { <uid> * * . }` only deletes predicates declared in the type. Predicates added outside the type definition remain.
:::
