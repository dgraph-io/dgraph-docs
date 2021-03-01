+++
date = "2017-03-20T22:25:17+11:00"
title = "Multi-Tenancy"
weight = 3
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
  - They can add users to groups inside the namespace
  - They can remove users from groups inside the namespace
  - They can export their namespace
- Normal users
  - They can login into a namespace
  - They can query in their namespace
  - They can mutate in their namespace
  - They can't query or mutate across namespaces

### Guardians of the Galaxy

A _Guardian of the Galaxy_ is a Super Admin of the default namespace (`0x00`).

As a super-admin, a _Guardian of the Galaxy_ can: 
- [Create](#create-a-namespace) and [delete](#delete-a-namespace) namespaces
- Add new users and guardians to any namespace
- Reset the passwords
- Query and mutate the default namespace (`0x00`)
- Trigger cluster-wide [backups](#backups) (no namespace-specific backup)
- Trigger cluster-wide or namespace-specific [exports](#exports) (exports contain information about the namespace)

For example, if the user `rocket` is part of the _Guardians of the Galaxy_ group (namespace `0x00`),
he can only read/write on namespace `0x00`, but he can create new namespaces and add users to them.

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

## Delete a Namespace

Only members of the [Guardians of the Galaxy](#guardians-of-the-galaxy) group can delete a namespace.
A namespace can be dropped by calling `/admin` with the `deleteNamespace` mutation.

{{% notice "note" %}}
To delete a namespace, the _Guardian_ must send the JWT access token in the `X-Dgraph-AccessToken` header.
{{% /notice %}}

For example, to drop the namespace `0x123`:

```graphql
mutation {
  deleteNamespace(input: {namespaceId: 0x123})
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
`drop all` and `drop data` operations are executed at cluster level and will delete across namespaces.
{{% /notice %}}

## Backups

Backups are currently cluster-wide only, but [exports](#exports) can be created by namespace.
Only a [Guardian of the Galaxy](#guardians-of-the-galaxy) can trigger a backup.

{{% notice "tip" %}}
[Live loader](#live-loader) supports loading data into specific namespaces.
{{% /notice %}}

### Bulk Loader

[Bulk loader]({{< relref "bulk-loader.md" >}}) can be used to load the data in bulk.
By default, Bulk loader preserves the namespace in the data and schema files.
If the namespace information is missing it loads it into default namespace.

Using `--force-namespace` flag one can load all the data into specified namespace.
The namespace information from the data and schema file will be ignored.

For example, to force the bulk data loading into namespace `123`:

```sh
dgraph bulk -s /tmp/data/1million.schema -f /tmp/data/1million.rdf.gz --force-namespace 123
```

### Live Loader

Since multi-tenancy works with ACL enabled, when using the [Live loader]({{< relref "live-loader.md" >}}),
you must provide the login credentials using the `--creds` flag.
By default, Live loader loads the data into the user's namespace.

[Guardians of the Galaxy](#guardians-of-the-galaxy) can load the data into multiple namespaces. Using `--force-namespace`, a _Guardian_ can load the data into the namespace specified in the data and schema files.

For example:

```sh
dgraph live -s /tmp/data/1million.schema -f /tmp/data/1million.rdf.gz --creds="user=groot;password=password;namespace=0" --force-namespace -1
```

A _Guardian of the Galaxy_ can also load data into a specific namespace. For example, to force the data loading into namespace `123`:

```sh
dgraph live -s /tmp/data/1million.schema -f /tmp/data/1million.rdf.gz --creds="user=groot;password=password;namespace=0" --force-namespace 123
```

## Exports

Exports can be generated cluster-wide or at namespace level.
The export function creates a new folder for each namespace, and each folder contains the exported `.rdf` and schema file.
These exported sets of `.rdf` files and schemas include the multi-tenancy namespace information.

If a _Guardian of the Galaxy_ exports the whole cluster, a single folder containing the export data of all the namespaces in a single `.rdf` file and a single schema will be generated.

{{% notice "note" %}}
Guardians of a Namespace can trigger an Export for their namespace.
{{% /notice %}}

A namespace-specific export will contain the namespace value in the generated `.rdf` file: 

```rdf
<0x01> "name" "ibrahim" <0x12> .     -> this belongs to namespace 0x12
<0x01> "name" "ibrahim" <0x0> .      -> this belongs to namespace 0x00
```

For example, to export the namespace `0x1234` to a folder in the export directory (by default this directory is `export`):

```graphql
mutation {
  export(input: {format: "rdf", namespace: 0x1234}) {
    response {
      message
    }
  }
}
```

To export all the namespaces: (this is only valid for _Guardians of the Galaxy_)

```graphql
mutation {
  export(input: {format: "rdf"}) {
    response {
      message
    }
  }
}
```

{{% notice "note" %}}
For _Guardians of the Galaxy_, if you don't define a namespace it will export data for every namespace.
{{% /notice %}}
