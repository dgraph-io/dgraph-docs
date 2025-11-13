---
title: Read only and Strict mode
---

You can control mutation operations using the `--limit` flag with the `mutations` parameter. There are three modes available: `allow`, `disallow`, and `strict`.

## Mutation Modes

### Allow (Default)

The default mode is `allow`. In this mode:
- Users can read and mutate data
- Mutations can be performed on predicates that don't exist in the DQL schema
- If a predicate in a mutation doesn't exist in the schema, it gets automatically added to the schema with an appropriate [Dgraph Type](../../dql/dql-schema)

No configuration is needed as this is the default behavior.

### Disallow

The `disallow` mode disables all mutation operations. This makes the database read-only.

```sh
dgraph alpha --limit "mutations=disallow;"
```

### Strict

The `strict` mode enforces schema validation for mutations:
- Mutations are only allowed on predicates that are already declared in the schema
- Before performing a mutation on a predicate that doesn't exist in the schema, you must first perform an alter operation to add that predicate and its schema type

```sh
dgraph alpha --limit "mutations=strict"
```

## Related Topics

- [Secure Alter Operations](secure-alter-operations) - Protect schema updates with authentication
- [Admin Endpoint Security](../security/admin-endpoint-security) - Configure authentication for admin operations

