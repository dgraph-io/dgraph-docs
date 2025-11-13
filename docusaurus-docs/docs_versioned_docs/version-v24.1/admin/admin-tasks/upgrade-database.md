---
title: Upgrade Database
---

Doing periodic exports is always a good idea. This is particularly useful if you wish to upgrade Dgraph or reconfigure the sharding of a cluster. The following are the right steps to safely export and restart.

1. Start an [export](export-database)
2. Ensure it is successful
3. [Shutdown Dgraph](shut-down-database) and wait for all writes to complete
4. Start a new Dgraph cluster using new data directories (this can be done by passing empty directories to the options `-p` and `-w` for Alphas and `-w` for Zeros)
5. Reload the data via [bulk loader](../../migration/bulk-loader)
6. Verify the correctness of the new Dgraph cluster. If all looks good, you can delete the old directories (export serves as an insurance)

These steps are necessary because Dgraph's underlying data format could have changed, and reloading the export avoids encoding incompatibilities.

## Blue-Green Deployment

Blue-green deployment is a common approach to minimize downtime during the upgrade process.
This approach involves switching your application to read-only mode. To make sure that no mutations are executed during the maintenance window you can
do a rolling restart of all your Alpha using the option `--mutations disallow` when you restart the Alpha nodes. This will ensure the cluster is in read-only mode.

At this point your application can still read from the old cluster and you can perform the steps 4. and 5. described above.
When the new cluster (that uses the upgraded version of Dgraph) is up and running, you can point your application to it, and shutdown the old cluster.

## Enterprise Upgrade Notes

For enterprise customers, specific upgrade procedures may be required depending on your Dgraph version. The general upgrade process uses [binary backups](../enterprise-features/binary-backups) for data migration:

1. Use binary backup to export data from the old cluster
2. Ensure the backup is successful
3. [Shutdown Dgraph](shut-down-database) and wait for all writes to complete
4. Upgrade the `dgraph` binary to the target version
5. Restore from the backups using the upgraded `dgraph` binary
6. Start a new Dgraph cluster using the restored data directories
7. Run any required upgrade commands using `dgraph upgrade` if needed

:::note
For specific version-to-version upgrade instructions, consult the release notes for your target Dgraph version. Always test upgrades in a non-production environment first.
:::

## Related Topics

- [Export Database](export-database) - Export data before upgrade
- [Shut Down Database](shut-down-database) - Clean shutdown during upgrade
- [Binary Backups](../enterprise-features/binary-backups) - Enterprise backup solution for upgrades
- [Restrict Mutation Operations](restrict-mutation-operations) - Put cluster in read-only mode during upgrade

