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

A multi-tenancy Namespace acts as a logical silo. Each namespace has a group guardian (with root access to that namespace),
and a unique `uint64` identifier. The data stored in one namespace will not be accessible by another namespace.
Each user is part of a single namespace, and cross-namespace queries are not allowed.
A user can be part of multiple namespaces, but the user has to be created separately for each namespace.

The default namespace (`0x00`) is called a `galaxy`. A [Guardian of the Galaxy](#guardians-of-the-galaxy) has
special access to create or delete namespaces and change passwords of
users of other namespaces.

## Access Control Lists

Multi-tenancy defines certain ACL roles for the shared cluster:

- [Guardians of the Galaxy](#guardians-of-the-galaxy) (Super Admins) 
- Guardians of the Namespace
  - They can add users to groups inside the namespace
  - They can remove users from groups inside the namespace
- Normal users
  - They can login into a namespace
  - They can query in their namespace
  - They can mutate in their namespace
  - They can export their namespace
  - They cannot query or mutate across namespaces

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

A namespace can only be created by a member of the [Guardians of the Galaxy](#guardians-of-the-galaxy) (`dgraph-guardians`) group.
A namespace can be created by calling `/alter` with payload `{"create_namespace": "<name>"}`,
and will return the assigned number for the new namespace.

For example, to create a namespace `foo`:

```sh
$ curl -X POST localhost:8080/alter -d '{"create_namespace": "foo"}'
```

## Delete a Namespace

A namespace can only be deleted by a member of the [Guardians of the Galaxy](#guardians-of-the-galaxy) (`dgraph-guardians`) group.
A namespace can be dropped by calling `/alter` with payload `{"drop_namespace": "<name>"}`.  

For example, to drop the namespace `foo`:

```sh
$ curl -X POST localhost:8080/alter -d '{"drop_namespace": "foo"}'
```

{{% notice "note" %}}
Members of `namespace-guardians` cannot delete a namespace, they can only perform queries and mutations.
{{% /notice %}}

## Backups

Backups are currently cluster-wide only, but [exports](#exports) can be created by namespace.

{{% notice "tip" %}}
[Live loader]({{< relref "live-loader.md" >}}) supports loading data into specific namespaces.
{{% /notice %}}

## Exports

Exports can be generated cluster-wide or at namespace level.
The export function creates a new folder for each namespace, and each folder contains the exported `.rdf` and schema file.

A namespace-specific export will contain the namespace value in the generated `.rdf` file: 

```rdf
0x01 "name" "ibrahim" 0x12 .     -> this goes to namespace 0x12
0x01 "name" "ibrahim" .          -> this goes to namespace 0x00
```

For example, to export the namespace `foo` to a folder `foo` in the export directory (by default this directory is `export`):

```graphql
mutation {
  export(input: {format: "json", namespace:"foo"}) {
    response {
      message
      code
    }
  }
}
```

To export all the namespaces:

```graphql
mutation {
    export(input: {format: "json", namespace:"*"})
}
```
{{% notice "tip" %}}
The `namespace` parameter can be a regex which allows exporting multiple namespaces.
{{% /notice %}}
