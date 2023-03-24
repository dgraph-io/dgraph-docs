+++
title = "Overview"
weight = 1
[menu.main]
    parent = "cloud-api"
    identifier = "cloud-api-overview"
+++

Dgraph Cloud now includes an API so you can programmatically launch and manage your Cloud backups.

The majority of these APIs use `https://cerebro.cloud.dgraph.io/graphql` as the primary endpoint, and will require you to log in with a username and password. Please see [Authentication]({{< relref "authentication.md" >}}) for instructions on generating a JWT token.

### Commands

Please see the following topics:

* [Authentication]({{< relref "authentication.md" >}}) describes how to authenticate with the Dgraph Cloud API.
* [Backend]({{< relref "backend.md" >}}) lists commands related to backend.
* [Backup]({{< relref "backup.md" >}}) lists commands related to backup.
* [Lambda]({{< relref "lambda.md" >}}) lists commands related to Lambda.
* [Schema]({{< relref "schema.md" >}}) lists commands related to schema.

## Understanding Headers used across the APIs

Dgraph Cloud has two layers of security: Dgraph Cloud Authentication and Dgraph Access Control Lists Authentication. The following section introduces the usage of the headers involved in the authentication process. These include the `Dg-Auth`, `X-Auth-Token`,  `Authorization`, and `X-Dgraph-AccessToken` headers.

### Dgraph Cloud Authentication
The `Dg-Auth` or `X-Auth-Token` headers are for Dgraph Cloud’s API key authentication (where you pass in any API key you would generate from the ["API Keys" tab](https://cloud.dgraph.io/_/settings?tab=api-keys) on the Settings page). The API key passed can be one of two kinds: Admin API key or Client API key. The tokens generated from the admin API grant access to the `/admin` or `/admin/slash` endpoints to perform schema alterations and similar operations. The tokens generated via the Client API key provides access to the `/graphql` endpoint to run GraphQL queries and mutations.

Dgraph Cloud also offers the Dgraph Cloud API, hosted at [this endpoint](https://cerebro.cloud.dgraph.io/graphql), that helps to automate tasks such as deployment of a lambda. In order to use this API, users need to pass an `Authorization` header. In order to generate this header, the user must first [Authenticate]({{< relref "authentication" >}}) and generate a token. The token is then set in `Authorization` header as a Bearer token (e.g. `Bearer {token}`). 

{{% notice "note" %}}
The `Dg-Auth`, `X-Auth-Token` and the `Authorization` headers are relevant to all types of backends, including Free, Shared, and Dedicated Backends.
{{% /notice %}}

### Dgraph Access Control Lists Authentication
The `X-Dgraph-AccessToken` header is used for accessing backends using Dgraph’s Access Control Lists or the Multitenancy feature. This lets you pass in an access JWT generated via a login mutation for a Dgraph user from the access control list permissions and/or log into a specific namespace with multi-tenancy. The Login mutation relevant for ACL is documented [here](https://dgraph.io/docs/enterprise-features/access-control-lists/#logging-in).

If you’re using ACLs or multitenancy, then you’ll need to set the `X-Dgraph-AccessToken` with a JWT token to access your backend.

{{% notice "note" %}}
The `X-Dgraph-AccessToken` header is relevant only for the Dedicated backends. Users with Free or Shared backends can ignore this header.
{{% /notice %}}
