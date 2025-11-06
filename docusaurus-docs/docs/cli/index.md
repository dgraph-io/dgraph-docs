---
title: Dgraph CLI
---

The Dgraph command-line interface (CLI) provides comprehensive tools for deploying and managing Dgraph in self-managed environments. Whether you're running Dgraph on on-premises infrastructure or cloud platforms (AWS, GCP, Azure), the CLI gives you complete control over your deployment.

## CLI Structure

The Dgraph CLI is built around the root `dgraph` command and its subcommands. Many commands support their own subcommands, creating a hierarchical structure. For example, `dgraph acl` requires you to specify a subcommand like `add`, `del`, `info`, or `mod`.

## Available Commands

The Dgraph CLI includes the following command groups:

### Core Commands
- [**`dgraph alpha`**](/dgraph-overview/cli/alpha) - Run Dgraph Alpha database nodes
- [**`dgraph zero`**](/dgraph-overview/cli/zero) - Run Dgraph Zero management nodes

### Data Loading Commands
- [**`dgraph bulk`**](/dgraph-overview/cli/bulk) - Bulk load data with the Bulk Loader
- [**`dgraph live`**](/dgraph-overview/cli/live) - Load data with the Live Loader
- [**`dgraph restore`**](/dgraph-overview/cli/restore) - Restore backups from Enterprise Edition

### Security Commands
- [**`dgraph acl`**](/dgraph-overview/cli/acl) - Manage Access Control Lists (ACL)
- [**`dgraph audit`**](/dgraph-overview/cli/audit) - Decrypt audit files
- [**`dgraph cert`**](/dgraph-overview/cli/cert) - Manage TLS certificates

### Debug Commands
- [**`dgraph debug`**](/dgraph-overview/dql/query/debug) - Debug Dgraph instances
- [**`dgraph debuginfo`**](/dgraph-overview/cli/debuginfo) - Generate debug information

### Utility Commands
- [**`dgraph completion`**](/dgraph-overview/cli/completion) - Generate shell completion scripts
- [**`dgraph conv`**](/dgraph-overview/cli/conv) - Convert geographic files to RDF
- [**`dgraph decrypt`**](/dgraph-overview/cli/decrypt) - Decrypt exported files
- [**`dgraph export_backup`**](/dgraph-overview/cli/export_backup) - Export binary backups
- [**`dgraph increment`**](/dgraph-overview/cli/increment) - Test with transactional counter
- [**`dgraph lsbackup`**](/dgraph-overview/admin/enterprise-features/lsbackup) - List backup information
- [**`dgraph migrate`**](/dgraph-overview/cli/migrate) - Migrate from MySQL to Dgraph
- [**`dgraph upgrade`**](/dgraph-overview/cli/upgrade) - Upgrade Dgraph versions

## Configuration

Dgraph provides flexible configuration options:

- **[Superflags](/dgraph-overview/cli/superflags)** - Learn about compound flags for complex commands
- **[Configuration Guide](/dgraph-overview/cli/config)** - Configure using flags, environment variables, or config files

## Getting Help

You can view help for any command using the `--help` flag:

```bash
dgraph --help                  # Show all available commands
dgraph alpha --help            # Show alpha-specific options
dgraph acl add --help          # Show help for acl add subcommand
```


