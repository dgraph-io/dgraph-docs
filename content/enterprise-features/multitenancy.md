+++
date = "2017-03-20T22:25:17+11:00"
title = "Multi-Tenancy"
weight = 9
[menu.main]
    parent = "enterprise-features"
+++

Multi-tenancy is an enterprise-only feature that allows various tenants to co-exist in the same Dgraph
cluster using `uint64` namespaces. With multi-tenancy, each tenant can only log into their own
namespace and operate in their own namespace.

{{% notice "note" %}}
Multi-tenancy is an enterprise feature and needs [Access Control Lists]({{< relref "access-control-lists.md" >}}) (ACL) enabled to work.
{{% /notice %}}

## Overview

Multi-tenancy is built upon [Access Control Lists]({{< relref "access-control-lists.md" >}}) (ACL), 
and enables multiple tenants to share a Dgraph cluster using unique namespaces.
The tenants are logically separated, and their data lies in the same `p` directory.
Each namespace has a group guardian, which has root access to that namespace.

The default namespace is called a `galaxy`. [Guardians of the Galaxy](#guardians-of-the-galaxy) get
special access to create or delete namespaces and change passwords of
users of other namespaces.

{{% notice "note" %}}
Dgraph provides a timeout limit per query that's configurable using the `--limit` superflag's `query-limit` option.
There's no time limit for queries by default, but you can override it when running Dgraph Alpha.
For multi-tenant environments a suggested `query-limit` value is 500ms. 
{{% /notice %}}

## FAQ

- How access controls and policies are handled among different tenants?

    In previous versions of Dgraph, the [Access Control Lists]({{< relref "access-control-lists.md" >}}) (ACL) feature
    offered a unified control solution across the entire database.
    With the new multi-tenancy feature, the ACL policies are now scoped down to individual tenants in the database.

{{% notice "note" %}}
Only super-admins ([Guardians of the galaxy](#guardians-of-the-galaxy)) have access across tenants.
The super admin is used only for database administration operations, such as exporting data of all tenants. _Guardian_ of the _Galaxy_ group cannot read across tenants.
{{% /notice %}}

- What's the ACL granularity in a multi-tenancy environment? Is it per tenant?

    The access controls are applied per tenant at a predicate level.
    For example, the user `John Smith` belonging to the group `Data Approvers` may only have read-only access to predicates,
    while user `Jane Doe`, who belongs to the group `Data Editors`, can be given access to modify predicates.
    All of these ACL constraints have to be configured for each tenant. 

- Are tenants a physical separation or a logical one?

    Tenants are a logical separation. In this example, data needs to be written twice for 2 different tenants.
    Each client must authenticate within a tenant, and can only modify data within the tenant as allowed by the configured ACLs.

- Can data be copied from one tenant to the other?

    Yes, but not by breaking any ACL or tenancy constraints.
    This can be done by exporting data from one tenant and importing data to another.

## Namespace

A multi-tenancy Namespace acts as a logical silo, so data stored in one namespace is not accessible from another namespace.
Each namespace has a group guardian (with root access to that namespace), and a unique `uint64` identifier. 
Users are members of a single namespace, and cross-namespace queries are not allowed.

{{% notice "note" %}}
If a user wants to access multiple namespaces, the user needs to be created separately for each namespace.
{{% /notice %}}

The default namespace (`0x00`) is called a `galaxy`. A [Guardian of the Galaxy](#guardians-of-the-galaxy) has
special access to create or delete namespaces and change passwords of
users of other namespaces.

## Access Control Lists

Multi-tenancy defines certain ACL roles for the shared cluster:

- [Guardians of the Galaxy](#guardians-of-the-galaxy) (Super Admins) 
- Guardians of the Namespace
  - They can create users and groups inside their own namespace
  - They can assign users to groups inside their own namespace
  - They can assign predicates to groups inside their own namespace
  - They can add users to groups inside the namespace
  - They can export their namespace 
  - They can query and mutate in their namespace
  - They can't query or mutate across namespaces
- Normal users
  - They can login into a namespace
  - They can query in their namespace
  - They can mutate in their namespace
  - They can't query or mutate across namespaces

### Guardians of the Galaxy

A _Guardian of the Galaxy_ is a Super Admin of the default namespace (`0x00`).

As a super-admin, a _Guardian of the Galaxy_ can: 
- [Create](#create-a-namespace) and [delete](#delete-a-namespace) namespaces
- Reset the passwords
- Query and mutate the default namespace (`0x00`)
- Trigger cluster-wide [backups](#backups) (no namespace-specific backup)
- Trigger cluster-wide or namespace-specific [exports](#exports) (exports contain information about the namespace)

For example, if the user `rocket` is part of the _Guardians of the Galaxy_ group (namespace `0x00`),
he can only read/write on namespace `0x00`.

## Create a Namespace

Only members of the [Guardians of the Galaxy](#guardians-of-the-galaxy) group can create a namespace.
A namespace can be created by calling `/admin` with the `addNamespace` mutation,
and will return the assigned number for the new namespace.

{{% notice "note" %}}
To create a namespace, the _Guardian_ must send the JWT access token in the `X-Dgraph-AccessToken` header.
{{% /notice %}}

For example, to create a new namespace:

```graphql
mutation {
 addNamespace
  {
    namespaceId
    message
  }
}
```

## List Namespaces

Only members of the [Guardians of the Galaxy](#guardians-of-the-galaxy) group can list active namespaces.
You can check available namespaces using the `/state` endpoint.

For example, if you have a multi-tenant cluster with multiple namespaces, as a _Guardian of the Galaxy_ you can query `state` from GraphQL:

```graphql
query{
  state {
    groups {
      tablets{
        predicate
      }
    }
  }
}
```

In the response, each predicate will have a namespace prefix.
In this way administrators can identify which namespaces are available and active.
E.g., for predicate `2-dgraph.type`, `2` is the namespace.

```json
{
  "data": {
    "state": {
      "groups": [
        {
          "tablets": [
            {
              "predicate": "1-dgraph.password"
            },
            {
              "predicate": "2-dgraph.user.group"
            },
            {
              "predicate": "2-dgraph.xid"
            },
            {
              "predicate": "4-dgraph.rule.predicate"
            },
            {
              "predicate": "3-dgraph.password"
            },
            {
              "predicate": "3-dgraph.user.group"
            },
            {
              "predicate": "5-dgraph.type"
            },
            {
              "predicate": "3-dgraph.acl.rule"
            },
            {
              "predicate": "6-dgraph.graphql.xid"
            },
            {
              "predicate": "5-dgraph.graphql.xid"
            },
            {
              "predicate": "2-dgraph.password"
            },
            {
              "predicate": "0-dgraph.password"
            },
            {
              "predicate": "5-dgraph.rule.predicate"
            },
            {
              "predicate": "6-dgraph.type"
            },
            {
              "predicate": "4-dgraph.xid"
            },
            {
              "predicate": "0-dgraph.rule.permission"
            },
            {
              "predicate": "5-dgraph.xid"
            },
            {
              "predicate": "1-dgraph.graphql.xid"
            },
            {
              "predicate": "0-dgraph.drop.op"
            },
            {
              "predicate": "4-dgraph.drop.op"
            },
            {
              "predicate": "3-dgraph.graphql.xid"
            },
            {
              "predicate": "5-dgraph.acl.rule"
            },
            {
              "predicate": "6-dgraph.rule.permission"
            },
            {
              "predicate": "2-dgraph.drop.op"
            },
            {
              "predicate": "5-dgraph.user.group"
            },
            {
              "predicate": "5-dgraph.drop.op"
            },
            {
              "predicate": "1-dgraph.user.group"
            },
            {
              "predicate": "1-dgraph.xid"
            },
            {
              "predicate": "5-dgraph.graphql.p_query"
            },
            {
              "predicate": "6-dgraph.rule.predicate"
            },
            {
              "predicate": "4-dgraph.graphql.schema"
            },
            {
              "predicate": "4-dgraph.rule.permission"
            },
            {
              "predicate": "2-dgraph.graphql.p_query"
            },
            {
              "predicate": "2-dgraph.graphql.xid"
            },
            {
              "predicate": "5-dgraph.rule.permission"
            },
            {
              "predicate": "0-dgraph.user.group"
            },
            {
              "predicate": "0-dgraph.xid"
            },
            {
              "predicate": "6-dgraph.drop.op"
            },
            {
              "predicate": "0-dgraph.graphql.schema"
            },
            {
              "predicate": "0-dgraph.acl.rule"
            },
            {
              "predicate": "3-dgraph.type"
            },
            {
              "predicate": "3-dgraph.rule.permission"
            },
            {
              "predicate": "1-dgraph.drop.op"
            },
            {
              "predicate": "6-dgraph.graphql.p_query"
            },
            {
              "predicate": "3-dgraph.rule.predicate"
            },
            {
              "predicate": "1-dgraph.graphql.p_query"
            },
            {
              "predicate": "1-dgraph.rule.predicate"
            },
            {
              "predicate": "1-dgraph.graphql.schema"
            },
            {
              "predicate": "6-dgraph.user.group"
            },
            {
              "predicate": "5-dgraph.graphql.schema"
            },
            {
              "predicate": "1-dgraph.rule.permission"
            },
            {
              "predicate": "2-dgraph.acl.rule"
            },
            {
              "predicate": "1-dgraph.acl.rule"
            },
            {
              "predicate": "4-dgraph.user.group"
            },
            {
              "predicate": "3-dgraph.graphql.schema"
            },
            {
              "predicate": "3-dgraph.drop.op"
            },
            {
              "predicate": "4-dgraph.password"
            },
            {
              "predicate": "6-dgraph.graphql.schema"
            },
            {
              "predicate": "5-dgraph.password"
            },
            {
              "predicate": "3-dgraph.xid"
            },
            {
              "predicate": "4-dgraph.graphql.p_query"
            },
            {
              "predicate": "0-dgraph.graphql.p_query"
            },
            {
              "predicate": "2-dgraph.rule.predicate"
            },
            {
              "predicate": "0-dgraph.rule.predicate"
            },
            {
              "predicate": "6-dgraph.acl.rule"
            },
            {
              "predicate": "4-dgraph.graphql.xid"
            },
            {
              "predicate": "2-dgraph.rule.permission"
            },
            {
              "predicate": "0-dgraph.graphql.xid"
            },
            {
              "predicate": "1-dgraph.type"
            },
            {
              "predicate": "3-dgraph.graphql.p_query"
            },
            {
              "predicate": "2-dgraph.graphql.schema"
            },
            {
              "predicate": "6-dgraph.password"
            },
            {
              "predicate": "4-dgraph.type"
            },
            {
              "predicate": "6-dgraph.xid"
            },
            {
              "predicate": "0-dgraph.type"
            },
            {
              "predicate": "4-dgraph.acl.rule"
            },
            {
              "predicate": "2-dgraph.type"
            }
          ]
        }
      ]
    }
  }
}
```

## Delete a Namespace

Only members of the [Guardians of the Galaxy](#guardians-of-the-galaxy) group can delete a namespace.
A namespace can be dropped by calling `/admin` with the `deleteNamespace` mutation.

{{% notice "note" %}}
To delete a namespace, the _Guardian_ must send the JWT access token in the `X-Dgraph-AccessToken` header.
{{% /notice %}}

For example, to drop the namespace `123`:

```graphql
mutation {
  deleteNamespace(input: {namespaceId: 123})
  {
    namespaceId
    message
  }
}
```

{{% notice "note" %}}
Members of `namespace-guardians` can't delete namespaces, they can only perform queries and mutations.
{{% /notice %}}

## Reset passwords

Only members of the _Guardians of the Galaxy_ can reset passwords across namespaces.
A password can be reset by calling `/admin` with the `resetPassword` mutation.

For example, to reset the password for user `groot` from the namespace `100`:

```graphql
mutation {
  resetPassword(input: {userId: "groot", password:"newpassword", namespace: 100}) {
    userId
    message
  }
}
```

## Drop operations

The `drop all` and `drop data` operations can only be triggered by a [Guardian of the Galaxy](#guardians-of-the-galaxy).
They're executed at cluster level and delete data across namespaces.
All other `drop` operations run at namespace level and are namespace specific.

{{% notice "note" %}}
`drop all` and `drop data` operations are executed at cluster level and will delete across namespaces. The `drop data` operation will delete all the data but will keep the schema only.
{{% /notice %}}

## Backups

Backups are currently cluster-wide only, but [exports](#exports) can be created by namespace.
Only a [Guardian of the Galaxy](#guardians-of-the-galaxy) can trigger a backup.

### Bulk Loader

[Bulk loader]({{< relref "bulk-loader.md" >}}) can be used to load the data in bulk.
By default, Bulk loader preserves the namespace in the data and schema files.
If there's no namespace information available, it loads the data into the default namespace.

Please refer to the [Bulk loader documentation]({{< relref "bulk-loader.md#multi-tenancy-enterprise-feature" >}}) for examples and additional information.

### Live Loader

Since multi-tenancy works with ACL enabled, when using the [Live loader]({{< relref "live-loader.md" >}}),
you must provide the login credentials using the `--creds` flag.
By default, Live loader loads the data into the user's namespace.
[Guardians of the Galaxy](#guardians-of-the-galaxy) can load the data into multiple namespaces.

Please refer to the [Live loader documentation]({{< relref "live-loader.md#multi-tenancy-enterprise-feature" >}}) for examples and additional information.

{{% notice "note" %}}
The Live loader requires that the `namespace` from the data and schema files exist before loading the data.
{{% /notice %}}

{{% notice "tip" %}}
[Live loader](#live-loader) supports loading data into specific namespaces.
{{% /notice %}}

## Exports

Exports can be generated cluster-wide or at namespace level.
These exported sets of `.rdf` or `.json` files and schemas include the multi-tenancy namespace information.

If a _Guardian of the Galaxy_ exports the whole cluster, a single folder containing the export data of all the namespaces in a single `.rdf` or `.json` file and a single schema will be generated.

{{% notice "note" %}}
Guardians of a Namespace can trigger an Export for their namespace.
{{% /notice %}}

A namespace-specific export will contain the namespace value in the generated `.rdf` file: 

```rdf
<0x01> "name" "ibrahim" <0x12> .     -> this belongs to namespace 0x12
<0x01> "name" "ibrahim" <0x0> .      -> this belongs to namespace 0x00
```

For example, when the _Guardian of the Galaxy_ user is used to export the namespace `0x1234` to a folder in the export directory (by default this directory is `export`):

```graphql
mutation {
  export(input: {format: "rdf", namespace: 1234}) {
    response {
      message
    }
  }
}
```
When using the _Guardian of the Namespace_, there's no need to specify the namespace in the GraphQL mutation, as they can only export within their own namespace:

```graphql
mutation {
  export(input: {format: "rdf") {
    response {
      message
    }
  }
}
```

To export all the namespaces: (this is only valid for _Guardians of the Galaxy_)

```graphql
mutation {
  export(input: {format: "rdf", namespace: -1}) {
    response {
      message
    }
  }
}
```
