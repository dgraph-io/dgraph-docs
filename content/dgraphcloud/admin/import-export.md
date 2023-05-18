+++
title = "Importing and Exporting data from Dgraph Cloud"
weight = 4   
[menu.main]
    parent = "cloud-admin"
+++

## Exporting and Importing Data in Dgraph Cloud

You can export your data as an Administator from one Dgraph Cloud backend, and then import this data back into another Dgraph instance or Dgraph Cloud backend. For more information about how to export data in Dgraph Cloud, see [Export data]({{< relref "howto/exportdata/export-data-cloud.md" >}}). You can also export data from Dgraph Cloud programatically using the Dgraph Cloud API. For more information, see [Cloud API documentation]({{< relref "dgraphcloud/cloud-api/backup.md" >}}).

To import data to Dgraph Cloud, see [live loader]({{< relref "howto/importdata/live-loader.md" >}}).

## Exporting Data with Multi-Tenancy feature enabled in Dgraph Cloud

{{% notice "note" %}}
With Multi-Tenancy feature enabled, for any GraphQL request you need to provide the `accessJWT` for the specific user in the `X-Dgraph-AccessToken` header.
{{% /notice %}}

You can trigger two types of exports:
* cluster-wide export: this is an export of the entire backend (including all namespaces). This request can be only triggered by the [*Guardian of Galaxy*](https://dgraph.io/docs/enterprise-features/multitenancy/#guardians-of-the-galaxy) users.
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
3. Once done, you can now send the following GraqhQL mutation to get the `signedUrls` from where you can download your export files:
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

