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


### Delete data
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

### Update data
The upsert block allows performing queries and mutations in a single request. The upsert
block contains one query block and one or more than one mutation blocks. Variables defined
in the query block can be used in the mutation blocks using the `uid` and `val` function.

In general, the structure of the upsert block is as follows:

```
upsert {
  query <query block>
  [fragment <fragment block>]
  mutation <mutation block 1>
  [mutation <mutation block 2>]
  ...
}
```

Execution of an upsert block also returns the response of the query executed on the state
of the database *before mutation was executed*. To get the latest result, we should commit
the mutation and execute another query.

#### `uid` Function

The `uid` function allows extracting UIDs from variables defined in the query block.
There are two possible outcomes based on the results of executing the query block:

* If the variable is empty i.e. no node matched the query, the `uid` function returns a new UID in case of a `set` operation and is thus treated similar to a blank node. On the other hand, for `delete/del` operation, it returns no UID, and thus the operation becomes a no-op and is silently ignored. A blank node gets the same UID across all the mutation blocks.
* If the variable stores one or more than one UIDs, the `uid` function returns all the UIDs stored in the variable. In this case, the operation is performed on all the UIDs returned, one at a time.

#### `val` Function

The `val` function allows extracting values from value variables. Value variables store
a mapping from UIDs to their corresponding values. Hence, `val(v)` is replaced by the value
stored in the mapping for the UID (Subject) in the N-Quad. If the variable `v` has no value
for a given UID, the mutation is silently ignored. The `val` function can be used with the
result of aggregate variables as well, in which case, all the UIDs in the mutation would
be updated with the aggregate value.

#### Example of `uid` Function

Consider an example with the following schema:

```sh
curl localhost:8080/alter -X POST -d $'
  name: string @index(term) .
  email: string @index(exact, trigram) @upsert .
  age: int @index(int) .' | jq
```

Now, let's say we want to create a new user with `email` and `name` information.
We also want to make sure that one email has exactly one corresponding user in
the database. To achieve this, we need to first query whether a user exists
in the database with the given email. If a user exists, we use its UID
to update the `name` information. If the user doesn't exist, we create
a new user and update the `email` and `name` information.

We can do this using the upsert block as follows:

```sh
curl -H "Content-Type: application/rdf" -X POST localhost:8080/mutate?commitNow=true -d $'
upsert {
  query {
    q(func: eq(email, "user@company1.io")) {
      v as uid
      name
    }
  }

  mutation {
    set {
      uid(v) <name> "first last" .
      uid(v) <email> "user@company1.io" .
    }
  }
}' | jq
```

Result:

```json
{
  "data": {
    "q": [],
    "code": "Success",
    "message": "Done",
    "uids": {
      "uid(v)": "0x1"
    }
  },
  "extensions": {...}
}
```

The query part of the upsert block stores the UID of the user with the provided email
in the variable `v`. The mutation part then extracts the UID from variable `v`, and
stores the `name` and `email` information in the database. If the user exists,
the information is updated. If the user doesn't exist, `uid(v)` is treated
as a blank node and a new user is created as explained above.

If we run the same mutation again, the data would just be overwritten, and no new uid is
created. Note that the `uids` map is empty in the result when the mutation is executed
again and the `data` map (key `q`) contains the uid that was created in the previous upsert.

```json
{
  "data": {
    "q": [
      {
        "uid": "0x1",
        "name": "first last"
      }
    ],
    "code": "Success",
    "message": "Done",
    "uids": {}
  },
  "extensions": {...}
}
```

We can achieve the same result using `json` dataset as follows:

```sh
curl -H "Content-Type: application/json" -X POST localhost:8080/mutate?commitNow=true -d '
{
  "query": "{ q(func: eq(email, \"user@company1.io\")) {v as uid, name} }",
  "set": {
    "uid": "uid(v)",
    "name": "first last",
    "email": "user@company1.io"
  }
}' | jq
```

Now, we want to add the `age` information for the same user having the same email
`user@company1.io`. We can use the upsert block to do the same as follows:

```sh
curl -H "Content-Type: application/rdf" -X POST localhost:8080/mutate?commitNow=true -d $'
upsert {
  query {
    q(func: eq(email, "user@company1.io")) {
      v as uid
    }
  }

  mutation {
    set {
      uid(v) <age> "28" .
    }
  }
}' | jq
```

Result:

```json
{
  "data": {
    "q": [
      {
        "uid": "0x1"
      }
    ],
    "code": "Success",
    "message": "Done",
    "uids": {}
  },
  "extensions": {...}
}
```

Here, the query block queries for a user with `email` as `user@company1.io`. It stores
the `uid` of the user in variable `v`. The mutation block then updates the `age` of the
user by extracting the uid from the variable `v` using `uid` function.

We can achieve the same result using `json` dataset as follows:

```sh
curl -H "Content-Type: application/json" -X POST localhost:8080/mutate?commitNow=true -d $'
{
  "query": "{ q(func: eq(email, \\"user@company1.io\\")) {v as uid} }",
  "set":{
    "uid": "uid(v)",
    "age": "28"
  }
}' | jq
```

If we want to execute the mutation only when the user exists, we could use
[Conditional Upsert]({{< relref "mutations/conditional-upsert.md" >}}).

#### Example of `val` Function

Let's say we want to migrate the predicate `age` to `other`. We can do this using the
following mutation:

```sh
curl -H "Content-Type: application/rdf" -X POST localhost:8080/mutate?commitNow=true -d $'
upsert {
  query {
    v as var(func: has(age)) {
      a as age
    }
  }

  mutation {
    # we copy the values from the old predicate
    set {
      uid(v) <other> val(a) .
    }

    # and we delete the old predicate
    delete {
      uid(v) <age> * .
    }
  }
}' | jq
```

Result:

```json
{
  "data": {
    "code": "Success",
    "message": "Done",
    "uids": {}
  },
  "extensions": {...}
}
```

Here, variable `a` will store a mapping from all the UIDs to their `age`. The mutation
block then stores the corresponding value of `age` for each UID in the `other` predicate
and deletes the `age` predicate.

We can achieve the same result using `json` dataset as follows:

```sh
curl -H "Content-Type: application/json" -X POST localhost:8080/mutate?commitNow=true -d $'{
  "query": "{ v as var(func: regexp(email, /.*@company1.io$/)) }",
  "delete": {
    "uid": "uid(v)",
    "age": null
  },
  "set": {
    "uid": "uid(v)",
    "other": "val(a)"
  }
}' | jq
```

### Bulk Delete

Let's say we want to delete all the users of `company1` from the database. This can be
achieved in just one query using the upsert block as follows:

```sh
curl -H "Content-Type: application/rdf" -X POST localhost:8080/mutate?commitNow=true -d $'
upsert {
  query {
    v as var(func: regexp(email, /.*@company1.io$/))
  }

  mutation {
    delete {
      uid(v) <name> * .
      uid(v) <email> * .
      uid(v) <age> * .
    }
  }
}' | jq
```

We can achieve the same result using `json` dataset as follows:

```sh
curl -H "Content-Type: application/json" -X POST localhost:8080/mutate?commitNow=true -d '{
  "query": "{ v as var(func: regexp(email, /.*@company1.io$/)) }",
  "delete": {
    "uid": "uid(v)",
    "name": null,
    "email": null,
    "age": null
  }
}' | jq

### Comments
Anything on a line following a `#` is a comment
