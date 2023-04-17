+++
title = "Importing and Exporting data from Dgraph Cloud"
weight = 4   
[menu.main]
    parent = "cloud-admin"
+++

You can export your data from one Dgraph Cloud backend, and then import this data back into another Dgraph instance or Dgraph Cloud Backend.

## Exporting Data

You can export your data using JSON format. To do this, call the `export` mutation on `/admin/slash`. As an example, if your GraphQL endpoint is at `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/graphql`, then the `/admin` endpoint for the schema is at `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/admin/slash`.

{{% notice "note" %}}
The `/admin/slash` endpoint requires [Authentication]({{<relref "authentication">}}).
{{% /notice %}}

The following is an example of a GraphQL mutation to export data to JSON.

```graphql
mutation {
  export {
    response { code message }
    exportId
    taskId
  }
}
```
Make sure to keep your `exportId` and `taskId` safe as you will need them for getting the signed URLs in order to download your export files. These URLs will be returned in the `signedUrls` output field and **they expire after 48 hours**.

Export will usually return 3 files:
* `g01.gql_schema.gz`: The GraphQL schema file. This file can be re-imported via the [Schema APIs](/admin/schema)
* `g01.json.gz`: the data from your instance, which can be imported via live loader
* `g01.schema.gz`: This file is the internal Dgraph schema. If you have set up your backend with a GraphQL schema, then you should be able to ignore this file.

The following is an example of GraphQL query to check the status of the export and get the signed URLs for downloading your export files.

```graphql
query {
  exportStatus (
    exportId:"<paste-your-exportId>"
    taskId: "<paste-your-taskId>"
  ){
    kind
    lastUpdated
    signedUrls
    status
  }
}
```
## Exporting Data with Multi-Tenancy feature enabled

{{% notice "note" %}}
With Multi-Tenancy feature enabled, for any GraphQL request you will need to provide the `accessJWT` for the specific user in the `X-Dgraph-AccessToken` header.
{{% /notice %}}

You can trigger two types of exports:
* cluster-wide export: this is an export of the entire backend (including all namespaces). This request can be only triggered by the [*Guardian of Galaxy*]({{<relref "/enterprise-features/multitenancy.md#guardians-of-the-galaxy">}}) users.
* namespace-specific export: this is an export of a specific namespace. This request can be triggered by the *Guardian of Galaxy* users and by the *Guardian of Namespace* users.

### Cluster-wide Exports

This can only be done by the *Guardian of Galaxy* users (AKA Super Admin), the steps are:

1. Get the `accessJWT` token for the *Guardian of Galaxy* user. Send the following GraphQL mutation to the `/admin` endpoint:
```graphql
mutation login($userId: String, $password: String, $namespace: Int) {
  login(userId: $userId, password: $password, namespace: $namespace) {
    response {
      accessJWT
      refreshJWT
    }
  }
}
```
Your variables should be referring to the *Guardian of Galaxy* user:
```json
{
	"userId": "groot",
	"password": "password",
	"namespace": 0
}
```
2. Once obtained the `accessJWT` token you need to pass it in `X-Dgraph-AccessToken` Header and only then you can send the following GraphQL mutation to `/admin/slash` endpoint:
```graphql
mutation {
  export (namespace: -1) {
    response { code message }
    exportId
    taskId
  }
}
```
3. Once done, you can now send the following GraphQL mutation to get the `signedUrls` from where you can download your export files:
```graphql
query {
  exportStatus (
    exportId:"<paste-your-exportId>"
    taskId: "<paste-your-taskId>"
  ){
    kind
    lastUpdated
    signedUrls
    status
  }
}
```

### Namespace-specific Exports

Namespace-specific exports can be triggered by the *Guardian of Galaxy* users. In this case you can follow the same steps for the cluster-wide exports and replace the namespace value from `-1` to the namespace you want to export. It's important that you get the `accessJWT` token for the *Guardian of Galaxy* user and pass it in the `X-Dgraph-AccessToken` header.

E.g. if you want to export the namespace `0x123` your GraphQL request sent to the `/admin/slash` endpoint would look like:
```graphql
mutation {
  export (namespace: 123) {
    response { code message }
    exportId
    taskId
  }
}
```
You can also trigger namespace-specific export using the *Guardian of Namespace* users, in this case there is no need to specify any namespace in the GraphQL request as these users can only export their own namespace. It's important that you get the `accessJWT` token for the *Guardian of Namespace* user and pass it in the `X-Dgraph-AccessToken` header.

The GraphQL request sent to the `/admin/slash` endpoint would be:
```graphql
mutation {
  export {
    response { code message }
    exportId
    taskId
  }
}
```

## Importing data with Live Loader

It is possible to import data into a Dgraph Cloud backend using [live loader]({{<relref "live-loader.md">}}). 
