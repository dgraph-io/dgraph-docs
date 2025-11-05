+++
date = "2017-03-20T22:25:17+11:00"
title = "Dgraph Administration"
weight = 1
type = "docs"
[menu.main]
    parent = "admin"
+++

Dgraph Alpha exposes various administrative endpoints over HTTP and GraphQL for operations like data export and cluster shutdown.

For security configuration including authentication, IP whitelisting, and token-based access control, see [Admin Endpoint Security]({{< relref "security/admin-endpoint-security.md" >}}).

## Restrict Mutation Operations

By default, you can perform mutation operations for any predicate.
If the predicate in mutation doesn't exist in the schema,
the predicate gets added to the schema with an appropriate
[Dgraph Type]({{< relref "dql-schema.md" >}}).

You can use `--limit "mutations=disallow"` to disable all mutations,
which is set to `allow` by default.

```sh
dgraph alpha --limit "mutations=disallow;"
```

Enforce a strict schema by setting `--limit "mutations=strict`.
This mode allows mutations only on predicates already in the schema.
Before performing a mutation on a predicate that doesn't exist in the schema,
you need to perform an alter operation with that predicate and its schema type.

```sh
dgraph alpha --limit "mutations=strict; mutations-nquad=1000000"
```

## Secure Alter Operations

Alter operations allow clients to apply schema updates and drop predicates from the database. By default, all clients are allowed to perform alter operations.

You can secure alter operations using token authentication. See [Admin Endpoint Security]({{< relref "security/admin-endpoint-security.md#securing-alter-operations" >}}) for detailed configuration instructions.

For enterprise-grade access control, see [Access Control Lists]({{< relref "enterprise-features/access-control-lists.md" >}}).

## Export database

As an `Administrator` you might want to export data from Dgraph to:

* backup your data
* move the data to another Dgraph instance
* share your data

For more information about exporting your database, see [Export data]({{< relref "export-data.md" >}})

## Shut down database

A clean exit of a single Dgraph node is initiated by running the following GraphQL mutation on /admin endpoint.
{{% notice "warning" %}}This won't work if called from outside the server where Dgraph is running.
You can specify a list or range of whitelisted IP addresses from which shutdown or other admin operations
can be initiated using the `--security` superflag's `whitelist` option on `dgraph alpha`.
{{% /notice %}}

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

## Delete database

To drop all data, you could send a `DropAll` request via `/alter` endpoint.

Alternatively, you could:

* [Shutdown Dgraph]({{< relref "#shut-down-database" >}}) and wait for all writes to complete,
* Delete (maybe do an export first) the `p` and `w` directories, then
* Restart Dgraph.

## Upgrade database

Doing periodic exports is always a good idea. This is particularly useful if you wish to upgrade Dgraph or reconfigure the sharding of a cluster. The following are the right steps to safely export and restart.

1. Start an [export]({{< relref "#export-database">}})
2. Ensure it is successful
3. [Shutdown Dgraph]({{< relref "#shut-down-database" >}}) and wait for all writes to complete
4. Start a new Dgraph cluster using new data directories (this can be done by passing empty directories to the options `-p` and `-w` for Alphas and `-w` for Zeros)
5. Reload the data via [bulk loader]({{< relref "bulk-loader.md" >}})
6. Verify the correctness of the new Dgraph cluster. If all looks good, you can delete the old directories (export serves as an insurance)

These steps are necessary because Dgraph's underlying data format could have changed, and reloading the export avoids encoding incompatibilities.

Blue-green deployment is a common approach to minimize downtime during the upgrade process.
This approach involves switching your application to read-only mode. To make sure that no mutations are executed during the maintenance window you can
do a rolling restart of all your Alpha using the option `--mutations disallow` when you restart the Alpha nodes. This will ensure the cluster is in read-only mode.

At this point your application can still read from the old cluster and you can perform the steps 4. and 5. described above.
When the new cluster (that uses the upgraded version of Dgraph) is up and running, you can point your application to it, and shutdown the old cluster.

### Enterprise Upgrade Notes

For enterprise customers, specific upgrade procedures may be required depending on your Dgraph version. The general upgrade process uses [binary backups]({{< relref "enterprise-features/binary-backups.md">}}) for data migration:

1. Use binary backup to export data from the old cluster
2. Ensure the backup is successful
3. [Shutdown Dgraph]({{< relref "#shut-down-database" >}}) and wait for all writes to complete
4. Upgrade the `dgraph` binary to the target version
5. Restore from the backups using the upgraded `dgraph` binary
6. Start a new Dgraph cluster using the restored data directories
7. Run any required upgrade commands using `dgraph upgrade` if needed

{{% notice "note" %}}
For specific version-to-version upgrade instructions, consult the release notes for your target Dgraph version. Always test upgrades in a non-production environment first.
{{% /notice %}}

