+++
date = "2017-03-20T22:25:17+11:00"
title = "Upsert"
type = "docs"

[menu.main]
    parent = "dql"
    weight = 7
+++

Upsert-style operations are operations where:

1. A node is searched for, and then
2. Depending on if it is found or not, either:
    - Updating some of its attributes, or
    - Creating a new node with those attributes.

The upsert has to be an atomic operation such that either a new node is
created, or an existing node is modified. It's not allowed that two concurrent
upserts both create a new node.

There are many examples where upserts are useful. Most examples involve the
creation of a 1 to 1 mapping between two different entities. E.g. associating
email addresses with user accounts.

Upserts are common in both traditional RDBMSs and newer NoSQL databases.
Dgraph is no exception.

## Upsert Procedure

In Dgraph, upsert-style behavior can be implemented by users on top of
transactions. The steps are as follows:

1. Create a new transaction.

2. Query for the node. This will usually be as simple as `{ q(func: eq(email,
   "bob@example.com")) { uid }}`. If a `uid` result is returned, then that's the
`uid` for the existing node. If no results are returned, then the user account
doesn't exist.

3. In the case where the user account doesn't exist, then a new node has to be
   created. This is done in the usual way by making a mutation (inside the
transaction), e.g.  the RDF `_:newAccount <email> "bob@example.com" .`. The
`uid` assigned can be accessed by looking up the blank node name `newAccount`
in the `Assigned` object returned from the mutation.

4. Now that you have the `uid` of the account (either new or existing), you can
   modify the account (using additional mutations) or perform queries on it in
whichever way you wish.

## Upserts in DQL and GraphQL

You can also use the `Upsert Block` in DQL to achieve the upsert procedure in a single
 mutation. The request will contain both the query and the mutation as explained
[here]({{< relref "dql-mutation.md#Update data with upsert block" >}}).

In GraphQL, you can use the `upsert` input variable in an `add` mutation, as explained [here]({{< relref "graphql/mutations/upsert.md">}}).

## Conflicts

Upsert operations are intended to be run concurrently, as per the needs of the
application. As such, it's possible that two concurrently running operations
could try to add the same node at the same time. For example, both try to add a
user with the same email address. If they do, then one of the transactions will
fail with an error indicating that the transaction was aborted.

If this happens, the transaction is rolled back and it's up to the user's
application logic to retry the whole operation. The transaction has to be
retried in its entirety, all the way from creating a new transaction.

The choice of index placed on the predicate is important for performance.
**Hash is almost always the best choice of index for equality checking.**

{{% notice "note" %}}
It's the _index_ that typically causes upsert conflicts to occur. The index is
stored as many key/value pairs, where each key is a combination of the
predicate name and some function of the predicate value (e.g. its hash for the
hash index). If two transactions modify the same key concurrently, then one
will fail.
{{% /notice %}}

The upsert block contains one query block and mutation blocks. Variables defined
in the query block can be used in the mutation blocks using the `uid` and `val` function.

The `uid` function allows extracting UIDs from variables defined in the query block.
There are two possible outcomes based on the results of executing the query block:

* If the variable is empty i.e. no node matched the query, the `uid` function returns a new UID in case of a `set` operation and is thus treated similar to a blank node. On the other hand, for `delete/del` operation, it returns no UID, and thus the operation becomes a no-op and is silently ignored. A blank node gets the same UID across all the mutation blocks.
* If the variable stores one or more than one UIDs, the `uid` function returns all the UIDs stored in the variable. In this case, the operation is performed on all the UIDs returned, one at a time.


## Example of `uid` Function

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
[Conditional Upsert]({{< relref "dql-mutation.md#conditional-upsert" >}}).



## Bulk Delete Example

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
```
## val function
Variables defined in the query block can be used in the mutation blocks using the `uid` and `val` function.


The `val` function allows extracting values from value variables. Value variables store
a mapping from UIDs to their corresponding values. Hence, `val(v)` is replaced by the value
stored in the mapping for the UID (Subject) in the N-Quad. If the variable `v` has no value
for a given UID, the mutation is silently ignored. The `val` function can be used with the
result of aggregate variables as well, in which case, all the UIDs in the mutation would
be updated with the aggregate value.


### Example of `val` Function

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
## External ids
The upsert block makes managing external IDs easy.

Set the schema.
```
xid: string @index(exact) .
<http://schema.org/name>: string @index(exact) .
<http://schema.org/type>: [uid] @reverse .
```

Set the type first of all.
```
{
  set {
    _:blank <xid> "http://schema.org/Person" .
    _:blank <dgraph.type> "ExternalType" .
  }
}
```

Now you can create a new person and attach its type using the upsert block.
```
   upsert {
      query {
        var(func: eq(xid, "http://schema.org/Person")) {
          Type as uid
        }
        var(func: eq(<http://schema.org/name>, "Robin Wright")) {
          Person as uid
        }
      }
      mutation {
          set {
           uid(Person) <xid> "https://www.themoviedb.org/person/32-robin-wright" .
           uid(Person) <http://schema.org/type> uid(Type) .
           uid(Person) <http://schema.org/name> "Robin Wright" .
           uid(Person) <dgraph.type> "Person" .
          }
      }
    }
```

You can also delete a person and detach the relation between Type and Person Node. It's the same as above, but you use the keyword "delete" instead of "set". "`http://schema.org/Person`" will remain but "`Robin Wright`" will be deleted.

```
   upsert {
      query {
        var(func: eq(xid, "http://schema.org/Person")) {
          Type as uid
        }
        var(func: eq(<http://schema.org/name>, "Robin Wright")) {
          Person as uid
        }
      }
      mutation {
          delete {
           uid(Person) <xid> "https://www.themoviedb.org/person/32-robin-wright" .
           uid(Person) <http://schema.org/type> uid(Type) .
           uid(Person) <http://schema.org/name> "Robin Wright" .
           uid(Person) <dgraph.type> "Person" .
          }
      }
    }
```

Query by user.
```
{
  q(func: eq(<http://schema.org/name>, "Robin Wright")) {
    uid
    xid
    <http://schema.org/name>
    <http://schema.org/type> {
      uid
      xid
    }
  }
}
```