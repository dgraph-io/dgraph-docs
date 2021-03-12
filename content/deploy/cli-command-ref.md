+++
title = "Dgraph CLI Command Reference"
weight = 20
[menu.main]
    parent = "deploy"
+++

The Dgraph command-line interface (CLI) is used to deploy and manage Dgraph. You
use it in self-managed deployment scenarios; such as running Dgraph on on-premises
servers hosted on your physical infrastructure, or running Dgraph in the cloud
on your AWS, GCP, or Azure infrastructure. 

Dgraph has a root command used throughout the Dgraph CLI: `dgraph`. This root
command is supported by multiple commands (such as `alpha` or `update`), some of
which also contain commands. For example, the `acl` command requires you to
specify one of the following commands: `add`, `del`, `info` or `mod`. You specify
settings for commands using flags. 

## Dgraph CLI flag updates in release 21.03

Some flags are deprecated and replaced in release v21.03. In previous Dgraph
releases, multiple related flags are used in a command, causing some commands to
be very long. Starting in release v21.03, compound flags are  used for the most
complex subcommands (`alpha`, `backup`, `bulk`,`debug`, `live` and
`zero`). Compound flags contain one or more options that let you define multiple
settings in a semicolon-delimited list. The general syntax for compound flags
is as follows: `--<flagname> option-a=value; option-b=value`


For example, the following command that is valid in release 20.11 is no longer
valid starting in release 21.03:

```ssh
dgraph alpha --ludicrous_mode=true ludicrous_concurrency=16
```

Instead, you would express this command as follows starting in release 21.03:

```ssh
dgraph alpha --ludicrous enabled=true; concurrency=16;
```

The following table maps Dgraph CLI flags from release 20.11 and earlier that
have been replaced by compound flags in release v21.03. Any flags not shown here
are unchanged from release 21.03.

<!-- TBD alphabetize by compound flag -->
| Old Flag | Old Type | New Flag and Options | New Type | Applies To |
|---------:|:---------|---------:|:---------|:----:|
| | | **`--badger`** | | | |
| `max_retries` | int | `max-retries` | int |`alpha`|
| `badger.compression` | string | `compression` | string | `alpha`, `bulk`, `backup`|
| | | (new) [`goroutines`]({{< relref "troubleshooting.md" >}}) | int |`alpha`, `bulk`, `backup`|
| `badger.cache_mb` | string | `cache-mb` | string |`bulk`|
| `badger.cache_percentage` | string | `cache-percentage` | string |`bulk`|
| | | **`--acl`** | | |
| `acl_secret_file` | string | `secret-file` | string |`alpha`|
| `acl_access_ttl` | time.Duration | `access-ttl` | [string](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) |`alpha`|
| `acl_refresh_ttl` | time.Duration | `refresh-ttl` | [string](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) |`alpha`|
| | | **`--limit`** | | |
| `mutations` | string | `mutations` | string |`alpha`|
| | | **`--ludicrous`** | | |
| `ludicrous_mode` | bool | `enabled` | bool |`alpha`|
| `ludicrous_concurrency` | int | `concurrency` | int |`alpha`|
| | | **`--graphql`** | | 
| `graphql_introspection` | bool | `introspection` | bool |`alpha`|
| `graphql_debug` | bool | `debug` | bool |`alpha`|
| `graphql_extensions` | bool | `extensions` | bool |`alpha`|
| `graphql_poll_interval` | time.Duration | `poll-interval` | [string](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) |`alpha`|
| `graphql_lambda_url` | string | `lambda-url` | string |`alpha`|
| | | **`--raft`** | |
| `pending_proposals` | int | `pending-proposals` | int |`alpha`|
| `idx` | int | `idx` | int |`alpha`, `zero`|
| `group` | int | `group` | int |`alpha`|
| `learner` | bool | `learner` | bool | `alpha`, `zero`|
| `snapshot-after` | int | `snapshot-after` | bool |`alpha`|
| | | **`--security`** | | 
| `auth_token` | string | `token` | string |`alpha`|
| `whitelist` | string | `whitelist` | string |`alpha`|
| | | **`--limit`** | | 
| `query_edge_limit` | uint64 | `query-edge` | uint64 |`alpha`|
| `normalize_node_limit` | int | `normalize-node` | int |`alpha`|
| `mutations_nquad_limit` | int | `mutations-nquad` | int |`alpha`|
| | | **`--telemetry`** | |
| `telemetry` | bool | `reports` | bool |`alpha` and `zero`|
| `enable_sentry` | bool | `sentry` | bool |`alpha` and `zero`|
| | | **`--tls`** | |
| `tls_cacert` | string | `ca-cert` | string |`alpha`, `zero`, `bulk`, `backup`, `live`|
| `tls_use_system_ca` | bool | `use-system-ca` | bool |`alpha`, `zero`, `bulk`, `backup`, `live`|
| `tls_server_name` | string | `server-name` | string |`alpha`, `zero`, `bulk`, `backup`, `live`|
| `tls_client_auth` | string | `client-auth-type` | string |`alpha`, `zero`|
| `tls_node_cert` | string | `server-cert` | string |`alpha` and `zero`|
| `tls_node_key` | string | `server-key` | string |`alpha` and `zero`|
| `tls_internal_port_enabled` | bool | `internal-port` | bool | `alpha`, `zero`, `bulk`, `backup`, `live`|
| `tls_cert` | string | `client-cert` | string |`alpha`, `zero`, `bulk`, `backup`, `live`|
| `tls_key` | string | `client-key` | string |`alpha`, `zero`, `bulk`, `backup`, `live`|
| | | **`--trace`** | |
| `trace` | float64 | `ratio` | float64 |`alpha`, `zero`|
| `jaeger.collector` | string | `jaeger` | string | `alpha`, `zero`|
| `datadog.collector` | string | `datadog` | string | `alpha`, `zero`|
| | | **`--vault`** | |
| `vault_addr` | string | `addr` | string | `alpha`, `bulk`, `backup`, `live`, `debug`|
| `vault_roleid_file` | string | `role-id-file` | string | `alpha`, `bulk`, `backup`, `live`, `debug`|
| `vault_secretid_file` | string | `secret-id-file` | string |`alpha`, `bulk`, `backup`, `live`, `debug`|
| `vault_path` | string | `path` | string | `alpha`, `bulk`, `backup`, `live`, `debug`|
| `vault_field` | string | `field` | string |`alpha`, `bulk`, `backup`, `live`, `debug`|
| `vault_format` | string | `format` | string | `alpha`, `bulk`, `backup`, `live`, `debug`|

<!--
## Dgraph CLI commands

The Dgraph CLI includes the following commands (subcommands of `dgraph`). 
CLI help for these commands is replicated inline below for your reference, or you
can find help by calling these commands with the `--help` flag.

| Command    | Notes                    | Learn More |
|------------|--------------------------|------------|
|[`acl`](#name-command)| Notes | []() |
|[`name`](#name-command)|  |
|[`name`](#name-command)|  |
|[`name`](#name-command)|  |
|[`name`](#name-command)|  |
|[`name`](#name-command)|  |
|[`name`](#name-command)|  |
-->