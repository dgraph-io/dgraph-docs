+++
date = "2017-03-20T22:25:17+11:00"
title = "Update Dgraph types"
weight = 15
[menu.main]
    parent = "howto"
+++


## Adding or Modifying Dgraph types

You modify Dgraph types (node types and predicates types) using the /alter endpoint in Raw HTTP or the alter operation of a client library.
### HTTP API

You can specify the flag `runInBackground` to `true` to run
index computation in the background.

```sh
curl localhost:8080/alter?runInBackground=true -XPOST -d $'
    name: string @index(fulltext, term) .
    age: int @index(int) @upsert .
    friend: [uid] @count @reverse .
' | python -m json.tool | less
```

### Grpc API

You can set `RunInBackground` field to `true` of the `api.Operation`
struct before passing it to the `Alter` function.

```go
op := &api.Operation{}
op.Schema = `
  name: string @index(fulltext, term) .
  age: int @index(int) @upsert .
  friend: [uid] @count @reverse .
`
op.RunInBackground = true
err = dg.Alter(context.Background(), op)
```



If no data has been stored for the predicates, a schema mutation sets up an empty schema ready to receive triples.

If data is already stored before the mutation, existing values are not checked to conform to the new schema.  

On query, Dgraph tries to convert existing values to the new schema types, ignoring any that fail conversion.

If data exists and new indices are specified in a schema mutation, any index not in the updated list is dropped and a new index is created for every new tokenizer specified.




## Indexes in Background

Indexes may take long time to compute depending upon the size of the data.

Indexes can be computed in the background and thus indexing may still be running after an Alter operation returns.

To run index computation in the background set the flag `runInBackground` to `true` .

```sh
curl localhost:8080/alter?runInBackground=true -XPOST -d $'
    name: string @index(fulltext, term) .
    age: int @index(int) @upsert .
    friend: [uid] @count @reverse .
' | python -m json.tool | less
```

```go
op := &api.Operation{}
op.Schema = `
  name: string @index(fulltext, term) .
  age: int @index(int) @upsert .
  friend: [uid] @count @reverse .
`
op.RunInBackground = true
err = dg.Alter(context.Background(), op)
```

{{% notice "note" %}}If executed before the indexing finishes, queries that require the new indices will fail with an error
notifying that a given predicate is not indexed or doesn't have reverse edges.{{% /notice  %}}

You can check the background indexing status using the [Health](https://dgraph.io/docs/main/deploy/dgraph-alpha/#querying-health) query on the `/admin` endpoint.


{{% notice "note" %}}An alter operation will also fail if one is already in progress with an error
`schema is already being modified. Please retry`.{{% /notice  %}}

For example, let's say we execute an Alter operation with the following schema:

Dgraph reports 

Dgraph will report the indexes in the schema only when the indexes are done computing.  

In a multi-node cluster, it is possible that the alphas will finish computing indexes at different times. Alphas may return different schema in such a case until all the indexes are done computing on all the Alphas.



