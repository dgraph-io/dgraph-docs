---
title: Shut Down Database
---

A clean exit of a single Dgraph node is initiated by running the following GraphQL mutation on /admin endpoint.

:::warningThis won't work if called from outside the server where Dgraph is running.
You can specify a list or range of whitelisted IP addresses from which shutdown or other admin operations
can be initiated using the `--security` superflag's `whitelist` option on `dgraph alpha`.
:::

```graphql
mutation {
  shutdown {
    response {
      message
      code
    }
  }
}
```

This stops the Alpha on which the command is executed and not the entire cluster.

## Related Topics

- [Admin Endpoint Security](../security/admin-endpoint-security) - Configure IP whitelisting for shutdown operations
- [Upgrade Database](upgrade-database) - Shutdown as part of the upgrade process
- [Delete Database](delete-database) - Shutdown before deleting data

