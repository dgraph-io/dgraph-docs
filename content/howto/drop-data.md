+++
date = ""
title = "Drop all data"
weight = 1
[menu.main]
    parent = "tasks"
+++

## On-Premise
### Drop data and schema

The `/alter` endpoint is used to create or change the schema. Here, the
predicate `name` is the name of an account. It's indexed so that we can look up
accounts based on their name.

```sh
$ curl -X POST localhost:8080/alter -d \
'name: string @index(term) .
type Person {
   name
}'
```

If all goes well, the response should be `{"code":"Success","message":"Done"}`.

Other operations can be performed via the `/alter` endpoint as well. A specific
predicate or the entire database can be dropped.

To drop the predicate `name`:

```sh
$ curl -X POST localhost:8080/alter -d '{"drop_attr": "name"}'
```

To drop the type `Film`:
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_op": "TYPE", "drop_value": "Film"}'
```

To drop all data and schema:
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_all": true}'
```

To drop all data only (keep schema):
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_op": "DATA"}'
```
## on cloud

It is possible to drop all data from your Dgraph Cloud backend, and start afresh while retaining the same endpoint. Be careful, as this operation is not reversible, and all data will be lost. It is highly recommended that you [export](/admin/import-export) your data before you drop your data.

In order to drop all data while retaining the schema, click the <kbd>Drop Data</kbd> button under the [Schema](https://cloud.dgraph.io/_/schema) tab in the sidebar.

*![Drop Data](/images/drop-data.png)*


### Dropping Data Programmatically

In order to do this, call the `dropData` mutation on `/admin/slash`. As an example, if your GraphQL endpoint is `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/graphql`, then the admin endpoint for schema will be at `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/admin/slash`.

Please note that this endpoint requires [Authentication](/admin/authentication).

Please see the following curl as an example.

```
curl 'https://<your-backend>/admin/slash' \
  -H 'X-Auth-Token: <your-token>' \
  -H 'Content-Type: application/graphql' \
  --data-binary 'mutation { dropData(allData: true) { response { code message } } }'
```

If you would like to drop the schema along with the data, then you can set the `allDataAndSchema` flag.

```
curl 'https://<your-backend>/admin/slash' \
  -H 'X-Auth-Token: <your-token>' \
  -H 'Content-Type: application/graphql' \
  --data-binary 'mutation { dropData(allDataAndSchema: true) { response { code message } } }'
```
