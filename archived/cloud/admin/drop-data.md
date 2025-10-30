+++
title = "Dropping Data from your Backend"
weight = 5   
[menu.main]
    parent = "cloud-admin"
+++

It is possible to drop all data from your Dgraph Cloud backend, and start afresh while retaining the same endpoint. Be careful, as this operation is not reversible, and all data will be lost. It is highly recommended that you [export]({{<relref "cloud/admin/import-export">}}) your data before you drop your data.

In order to drop all data while retaining the schema, click the <kbd>Drop Data</kbd> button under the [Schema](https://cloud.dgraph.io/_/schema) tab in the sidebar.

![Drop Data](/images/drop-data.png)

### Dropping Data Programmatically

In order to do this, call the `dropData` mutation on `/admin/slash`. As an example, if your GraphQL endpoint is `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/graphql`, then the admin endpoint for schema will be at `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/admin/slash`.

Please note that this endpoint requires [Authentication]({{<relref "cloud/admin/authentication">}}).

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
