+++
title = "Dgraph CLI"
weight = 14
type = "docs"
[menu.main]
    identifier = "cli"
+++

The Dgraph command-line interface (CLI) provides comprehensive tools for deploying and managing Dgraph in self-managed environments. Whether you're running Dgraph on on-premises infrastructure or cloud platforms (AWS, GCP, Azure), the CLI gives you complete control over your deployment.

## CLI Structure

The Dgraph CLI is built around the root `dgraph` command and its subcommands. Many commands support their own subcommands, creating a hierarchical structure. For example, `dgraph acl` requires you to specify a subcommand like `add`, `del`, `info`, or `mod`.

## Available Commands

The Dgraph CLI includes the following command groups:

### Core Commands
- [**`dgraph alpha`**]({{< relref "alpha.md" >}}) - Run Dgraph Alpha database nodes
- [**`dgraph zero`**]({{< relref "zero.md" >}}) - Run Dgraph Zero management nodes

### Data Loading Commands
- [**`dgraph bulk`**]({{< relref "bulk.md" >}}) - Bulk load data with the Bulk Loader
- [**`dgraph live`**]({{< relref "live.md" >}}) - Load data with the Live Loader
- [**`dgraph restore`**]({{< relref "restore.md" >}}) - Restore backups from Enterprise Edition

### Security Commands
- [**`dgraph acl`**]({{< relref "acl.md" >}}) - Manage Access Control Lists (ACL)
- [**`dgraph audit`**]({{< relref "audit.md" >}}) - Decrypt audit files
- [**`dgraph cert`**]({{< relref "cert.md" >}}) - Manage TLS certificates

### Debug Commands
- [**`dgraph debug`**]({{< relref "debug.md" >}}) - Debug Dgraph instances
- [**`dgraph debuginfo`**]({{< relref "debuginfo.md" >}}) - Generate debug information

### Utility Commands
- [**`dgraph completion`**]({{< relref "completion.md" >}}) - Generate shell completion scripts
- [**`dgraph conv`**]({{< relref "conv.md" >}}) - Convert geographic files to RDF
- [**`dgraph decrypt`**]({{< relref "decrypt.md" >}}) - Decrypt exported files
- [**`dgraph export_backup`**]({{< relref "export_backup.md" >}}) - Export binary backups
- [**`dgraph increment`**]({{< relref "increment.md" >}}) - Test with transactional counter
- [**`dgraph lsbackup`**]({{< relref "lsbackup.md" >}}) - List backup information
- [**`dgraph migrate`**]({{< relref "migrate.md" >}}) - Migrate from MySQL to Dgraph
- [**`dgraph upgrade`**]({{< relref "upgrade.md" >}}) - Upgrade Dgraph versions

## Configuration

Dgraph provides flexible configuration options:

- **[Superflags]({{< relref "superflags.md" >}})** - Learn about compound flags for complex commands
- **[Configuration Guide]({{< relref "config.md" >}})** - Configure using flags, environment variables, or config files

## Getting Help

You can view help for any command using the `--help` flag:

```bash
dgraph --help                  # Show all available commands
dgraph alpha --help            # Show alpha-specific options
dgraph acl add --help          # Show help for acl add subcommand
```


