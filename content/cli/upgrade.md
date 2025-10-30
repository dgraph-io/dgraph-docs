+++
title = "dgraph upgrade"
weight = 3
type = "docs"
[menu.main]
    parent = "cli"
+++

The `dgraph upgrade` command helps you upgrade from an earlier Dgraph release to a newer release by migrating ACL data and performing other version-specific migrations.

## Overview

This tool is designed specifically for upgrading ACL (Access Control List) data structures when moving between major Dgraph versions. It handles schema changes and data migrations required for backward compatibility.

{{% notice "note" %}}
This tool is supported only for mainstream release versions of Dgraph, not for beta releases.
{{% /notice %}}

## Usage

```bash
dgraph upgrade [flags]
```

## Key Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-a, --alpha` | Dgraph Alpha gRPC server address | `"127.0.0.1:9080"` |
| `--acl` | Upgrade ACL from v1.2.2 to >=v20.03.0 | `false` |
| `-f, --from` | The version string from which to upgrade (e.g., v1.2.2) | |
| `-t, --to` | The version string till which to upgrade (e.g., v20.03.0) | |
| `-u, --user` | Username of ACL user | |
| `-p, --password` | Password of ACL user | |
| `-d, --deleteOld` | Delete the older ACL types/predicates | `true` |
| `--dry-run` | Perform a dry-run of the upgrade without making changes | `false` |

## When to Use

Use the upgrade command when:
- Upgrading from v1.2.2 to v20.03.0 or later (ACL schema changes)
- Migrating between versions with incompatible ACL structures
- You need to validate upgrade feasibility before applying changes

## Examples

### Dry Run to Check Compatibility

Before performing an actual upgrade, do a dry run to validate:

```bash
dgraph upgrade --acl \
  --alpha localhost:9080 \
  --from v1.2.2 \
  --to v20.03.0 \
  --user groot \
  --password password \
  --dry-run
```

### Upgrade ACL from v1.2.2 to v20.03.0

```bash
dgraph upgrade --acl \
  --alpha localhost:9080 \
  --from v1.2.2 \
  --to v20.03.0 \
  --user groot \
  --password password
```

### Upgrade with Credentials

```bash
dgraph upgrade --acl \
  --alpha myhost.example.com:9080 \
  --from v1.2.2 \
  --to v21.03.0 \
  --user admin \
  --password mySecurePassword
```

### Keep Old ACL Types

If you want to preserve old ACL types/predicates during upgrade:

```bash
dgraph upgrade --acl \
  --alpha localhost:9080 \
  --from v1.2.2 \
  --to v20.03.0 \
  --user groot \
  --password password \
  --deleteOld=false
```

## Full Reference

```shell
This tool is supported only for the mainstream release versions of Dgraph, not for the beta releases.
Usage:
 dgraph upgrade [flags]

Flags:
     --acl               upgrade ACL from v1.2.2 to >=v20.03.0
 -a, --alpha string      Dgraph Alpha gRPC server address (default "127.0.0.1:9080")
 -d, --deleteOld         Delete the older ACL types/predicates (default true)
     --dry-run           dry-run the upgrade
 -f, --from string       The version string from which to upgrade, e.g.: v1.2.2
 -h, --help              help for upgrade
 -p, --password string   Password of ACL user
 -t, --to string         The version string till which to upgrade, e.g.: v20.03.0
 -u, --user string       Username of ACL user

Use "dgraph upgrade [command] --help" for more information about a command.
```

## Upgrade Process

The upgrade tool performs the following steps:

1. **Connects to Alpha**: Establishes connection to the specified Alpha node
2. **Authenticates**: Logs in with provided user credentials
3. **Validates Versions**: Checks source and target version compatibility
4. **Analyzes Schema**: Examines current ACL schema structure
5. **Migrates Data**: Transforms ACL data to new format (if not dry-run)
6. **Cleans Up**: Removes old ACL types/predicates (if `--deleteOld=true`)

## Prerequisites

Before running the upgrade:

1. **Backup Your Data**: Always create a full backup before upgrading
2. **Stop Write Operations**: Ensure no ACL modifications are happening
3. **Access Credentials**: Have guardian/admin user credentials ready
4. **Network Access**: Ensure connectivity to the Alpha node
5. **Review Release Notes**: Check version-specific migration requirements

## Best Practices

### Planning the Upgrade

1. **Read Release Notes**: Review breaking changes between versions
2. **Test in Staging**: Run upgrade on a staging environment first
3. **Use Dry Run**: Always perform a dry-run before actual upgrade
4. **Schedule Downtime**: Plan for maintenance window if needed

### During the Upgrade

```bash
# Step 1: Backup
dgraph live backup --alpha localhost:9080

# Step 2: Dry run
dgraph upgrade --acl \
  --alpha localhost:9080 \
  --from v1.2.2 \
  --to v20.03.0 \
  --user groot \
  --password password \
  --dry-run

# Step 3: If dry run succeeds, perform actual upgrade
dgraph upgrade --acl \
  --alpha localhost:9080 \
  --from v1.2.2 \
  --to v20.03.0 \
  --user groot \
  --password password

# Step 4: Verify
# Test ACL functionality after upgrade
```

### After the Upgrade

1. **Verify ACL Functionality**: Test user authentication and permissions
2. **Check Logs**: Review Alpha logs for any warnings or errors
3. **Test Applications**: Ensure client applications work correctly
4. **Document Changes**: Note any configuration changes made

## Common Upgrade Paths

### v1.2.2 → v20.03.0+

Major ACL schema changes were introduced in v20.03.0:

```bash
dgraph upgrade --acl \
  --alpha localhost:9080 \
  --from v1.2.2 \
  --to v20.03.0 \
  --user groot \
  --password password
```

### v20.x → v21.03+

If upgrading from v20.x to v21.03, check if ACL migration is needed:

```bash
dgraph upgrade --acl \
  --alpha localhost:9080 \
  --from v20.11.0 \
  --to v21.03.0 \
  --user groot \
  --password password \
  --dry-run
```

## Troubleshooting

### Authentication Failures

If you encounter authentication errors:
- Verify user credentials are correct
- Ensure ACL is enabled on the cluster
- Check that the user has sufficient permissions

### Connection Issues

If unable to connect to Alpha:
- Verify Alpha is running: `curl http://localhost:8080/health`
- Check network connectivity
- Verify the gRPC port (9080) is accessible

### Migration Errors

If the upgrade fails:
1. Restore from backup
2. Review error messages in Alpha logs
3. Check for version compatibility issues
4. Try with `--deleteOld=false` if cleanup is causing issues

## Version-Specific Notes

### ACL Changes in v20.03.0

- New predicate structure for permissions
- Group-based permission model
- Guardian user privileges expanded

### Changes in v21.03.0

- Superflag introduction
- Configuration file format changes
- Namespace support added

## Limitations

- Only supports mainstream releases (not beta versions)
- Primarily designed for ACL migrations
- Requires guardian/admin user credentials
- Cannot downgrade versions (one-way migration)

## See Also

- [Access Control Lists]({{< relref "../../enterprise-features/access-control-lists.md" >}}) - ACL documentation
- [Binary Backups]({{< relref "../../enterprise-features/binary-backups.md" >}}) - Backup before upgrading
- [Release Notes]({{< relref "../../releases" >}}) - Version-specific changes
- [Migration Guide]({{< relref "../../migration" >}}) - Data migration strategies

