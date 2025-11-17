---
title: Multi-Tenancy
description: Enable multiple tenants to share a Dgraph cluster using logically separated namespaces
---

Multi-tenancy enables multiple tenants to coexist in the same Dgraph cluster using `uint64` namespaces. Each tenant operates in its own namespace with logical data separation—data is stored in the same `p` directory but is not accessible across namespaces.

:::note
**Enterprise Feature**: Multi-tenancy requires [Access Control Lists](access-control-lists) (ACL) to be enabled. See [License](license) for details.
:::

Multi-tenancy builds upon ACL and scopes ACL policies to individual tenants. Access controls are applied per tenant to specific predicates or all predicates within that tenant. Tenants are logically separated; each client must authenticate within a tenant and can only access data as allowed by the tenant's ACL rules.

The default namespace (`0x00`) is called a `galaxy`. [Guardians of the Galaxy](#guardians-of-the-galaxy) are super-admins with special privileges to create or delete namespaces and reset passwords across namespaces. Each namespace has a guardian group with root access to that namespace. Users belong to a single namespace; to access multiple namespaces, create separate user accounts for each.

:::tip
For multi-tenant environments, consider setting a query timeout using `--limit query-limit=500ms` when starting Dgraph Alpha.
:::

## Access Control Roles

### Guardians of the Galaxy
Super Admins of namespace `0x00`

- Create and delete namespaces
- Reset passwords across namespaces
- Query and mutate the default namespace (`0x00`)
- Trigger cluster-wide backups and exports
- Export all namespaces or specific namespaces

### Guardians of a Namespace
- Create users and groups within the namespace
- Assign users to groups and predicates to groups
- Export the namespace
- Drop data within the namespace
- Query and mutate within the namespace

**Normal Users**:
- Login into a namespace
- Query and mutate within the namespace as permitted by ACL rules

:::note
Guardians of the Galaxy cannot read across tenants. They are used only for database administration operations such as exporting data of all tenants.
:::

## Namespace Operations

### Create a Namespace

Only [Guardians of the Galaxy](#guardians-of-the-galaxy) can create namespaces. Send the JWT access token in the `X-Dgraph-AccessToken` header:

```graphql
mutation {
  addNamespace(input: {password: "mypass"}) {
    namespaceId
    message
  }
}
```

This creates a namespace, automatically creates a guardian group for that namespace, and creates a `groot` user with the specified password (default is `password`) in the guardian group. Use these credentials to login and perform operations like [`addUser`](access-control-lists#create-a-regular-user).

### List Namespaces

Only [Guardians of the Galaxy](#guardians-of-the-galaxy) can list active namespaces using the GraphQL `state` query:

```graphql
query {
  state {
    namespaces
  }
}
```

Response:

```json
{
  "data": {
    "state": {
      "namespaces": [2, 1, 0]
    }
  }
}
```

### Delete a Namespace

Only [Guardians of the Galaxy](#guardians-of-the-galaxy) can delete namespaces. Send the JWT access token in the `X-Dgraph-AccessToken` header:

```graphql
mutation {
  deleteNamespace(input: {namespaceId: 123}) {
    namespaceId
    message
  }
}
```

### Reset Passwords

Only [Guardians of the Galaxy](#guardians-of-the-galaxy) can reset passwords across namespaces:

```graphql
mutation {
  resetPassword(input: {userId: "groot", password: "newpassword", namespace: 100}) {
    userId
    message
  }
}
```

## Drop Operations

The `drop all` operation can only be triggered by a [Guardian of the Galaxy](#guardians-of-the-galaxy) and deletes data and schema across all namespaces. All other drop operations run at namespace level. Guardians of a namespace can trigger `drop data` within their namespace, which deletes all data but retains the schema.

For example, to drop data within a namespace:

```bash
curl 'http://localhost:8080/alter' \
  -H 'X-Dgraph-AccessToken: <your-access-token>' \
  --data-raw '{"drop_op":"DATA"}'
```

For information about other drop operations, see [Alter the database](../../clients/raw-http#alter-the-dql-schema).

## Backups and Exports

Backups are cluster-wide only and can only be triggered by a [Guardian of the Galaxy](#guardians-of-the-galaxy). Exports can be generated cluster-wide or at namespace level.

[Initial import](../../migration/bulk-loader) and [Live import](../../migration/live-loader) tools support multi-tenancy.


### Exports

Exports generate `.rdf` or `.json` files and schemas that include namespace information. If a Guardian of the Galaxy exports the whole cluster, a single folder contains export data of all namespaces in a single file with a single schema.

Namespace-specific exports contain the namespace value in the generated `.rdf` file:

```rdf
<0x01> "name" "ibrahim" <0x12> .     -> belongs to namespace 0x12
<0x01> "name" "ibrahim" <0x0> .      -> belongs to namespace 0x00
```

**Export a specific namespace** (Guardian of the Galaxy):

```graphql
mutation {
  export(input: {format: "rdf", namespace: 1234}) {
    response {
      message
    }
  }
}
```

**Export current namespace** (Guardian of a Namespace - no namespace parameter needed):

```graphql
mutation {
  export(input: {format: "rdf"}) {
    response {
      message
    }
  }
}
```

**Export all namespaces** (Guardian of the Galaxy only):

```graphql
mutation {
  export(input: {format: "rdf", namespace: -1}) {
    response {
      message
    }
  }
}
```
