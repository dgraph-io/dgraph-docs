---
title: Update Dgraph types
---

You modify Dgraph types (node types and predicates types) by 
- issuing a request to the ``/alter`` endpoint using the [HTTP Client](/clients/raw-http#alter-the-dql-schema)
- using an ``alter`` operation of any [DQL client library](/clients).
- using [Ratel UI](/ratel/schema)



### Notes about predicate type change

If data is already stored, existing values are not checked to conform to the updated predicate type.  

On query, Dgraph tries to convert existing values to the new predicate type and ignores any that fail conversion.

If data exists and new indexes are specified, any old index not in the updated schema is dropped. New indexes are created.




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

### Notes

If executed before the indexing finishes, queries that require the new indices will fail with an error
notifying that a given predicate is not indexed or doesn't have reverse edges.

In a multi-node cluster, it is possible that the alphas will finish computing indexes at different times. Alphas may return different schema in such a case until all the indexes are done computing on all the Alphas.

You can check the background indexing status using the [Health](/admin/dgraph-alpha#health-check) query on the `/admin` endpoint.


An alter operation will fail if one is already in progress with an error
`schema is already being modified. Please retry`.


Dgraph will report the indexes in the schema only when the indexes are done computing.  


## Deleting a node type

Type definitions can be deleted using the Alter endpoint. 

Below is an example deleting the type `Person` using the Go client:
```go
err := c.Alter(context.Background(), &api.Operation{
                DropOp: api.Operation_TYPE,
                DropValue: "Person"})
```


