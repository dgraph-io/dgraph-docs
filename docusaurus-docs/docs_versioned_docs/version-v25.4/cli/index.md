---
title: Dgraph CLI
---

The Dgraph command-line interface (CLI) provides comprehensive tools for deploying and managing Dgraph in self-managed environments. Whether you're running Dgraph on on-premises infrastructure or cloud platforms (AWS, GCP, Azure), the CLI gives you complete control over your deployment.

## CLI Structure

The Dgraph CLI is built around the root `dgraph` command and its subcommands. Many commands support their own subcommands, creating a hierarchical structure. For example, `dgraph acl` requires you to specify a subcommand like `add`, `del`, `info`, or `mod`.

## Available Commands

The Dgraph CLI includes the following command groups:

### Core Commands
- [**`dgraph alpha`**](alpha) - Run Dgraph Alpha database nodes
- [**`dgraph zero`**](zero) - Run Dgraph Zero management nodes

### Data Loading Commands
- [**`dgraph bulk`**](bulk) - Bulk load data with the Bulk Loader
- [**`dgraph live`**](live) - Load data with the Live Loader
- [**`dgraph restore`**](restore) - Restore backups from Enterprise Edition

### Security Commands
- [**`dgraph acl`**](acl) - Manage Access Control Lists (ACL)
- [**`dgraph audit`**](audit) - Decrypt audit files
- [**`dgraph cert`**](cert) - Manage TLS certificates

### Debug Commands
- [**`dgraph debug`**](../dql/query/debug) - Debug Dgraph instances
- [**`dgraph debuginfo`**](debuginfo) - Generate debug information

### Utility Commands
- [**`dgraph completion`**](completion) - Generate shell completion scripts
- [**`dgraph conv`**](conv) - Convert geographic files to RDF
- [**`dgraph decrypt`**](decrypt) - Decrypt exported files
- [**`dgraph export_backup`**](export_backup) - Export binary backups
- [**`dgraph increment`**](increment) - Test with transactional counter
- [**`dgraph lsbackup`**](lsbackup) - List backup information
- [**`dgraph migrate`**](migrate) - Migrate from MySQL to Dgraph
- [**`dgraph upgrade`**](upgrade) - Upgrade Dgraph versions

## Configuration

Dgraph provides flexible configuration options:

- **[Superflags](superflags)** - Learn about compound flags for complex commands
- **[Configuration Guide](config)** - Configure using flags, environment variables, or config files

## Getting Help

You can view help for any command using the `--help` flag:

```bash
dgraph --help                  # Show all available commands
dgraph alpha --help            # Show alpha-specific options
dgraph acl add --help          # Show help for acl add subcommand
```


