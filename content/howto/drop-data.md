+++
date = ""
title = "Drop all data"
[menu.main]
    parent = "howto"
+++


It is possible to drop all data from your Dgraph Cloud backend, and start afresh while retaining the same endpoint.

Be careful, as this operation is not reversible, and all data will be lost. It is highly recommended that you [export](/admin/import-export) your data before you drop your data.

### Dropping data from the Cloud UI
In order to drop all data while retaining the schema :
- access the [Schema](https://cloud.dgraph.io/_/schema) panel
- click the <kbd>Drop Data</kbd> button at the bottom of the schema.
- select the options and confirm.

*![Drop Data](/images/drop-data.png)*


### Dropping Data Programmatically

You can drop data by invoking the `dropData` mutation on `/admin/slash` endpoint.

As an example, if your GraphQL endpoint is `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/graphql`, then the admin endpoint for schema will be at `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/admin/slash`.

This endpoint requires [Authentication]({{<relref "dgraphcloud/admin/authentication">}}).

Here is curl example.

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

## On-Premise
### Drop data and schema

The `/alter` endpoint is used to drop data.

To drop all data and schema:
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_all": true}'
```

To drop all data only (keep schema):
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_op": "DATA"}'
```
The `/alter` endpoint can also be used to drop a specific property or all nodes of a specific type.

To drop property `name`:

```sh
$ curl -X POST localhost:8080/alter -d '{"drop_attr": "name"}'
```

To drop the type `Film`:
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_op": "TYPE", "drop_value": "Film"}'
```
