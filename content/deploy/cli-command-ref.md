+++
title = "Dgraph CLI Command Reference"
weight = 20
[menu.main]
    parent = "deploy"
+++

The Dgraph command-line interface (CLI) is used to deploy and manage Dgraph. You
use it in self-managed deployment scenarios such as running Dgraph on on-premises
servers hosted on your physical infrastructure, or running Dgraph on your AWS,
GCP, or Azure cloud infrastructure. 

The Dgraph CLI consists of a variety of commands (such as `alpha` or `upgrade`),
some of which are grouped together (such as `acl add` and `acl info`). You specify
settings for these commands using flags. Some flags have been deprecated and replaced
in release 21.03.

## Dgraph CLI flag updates in 21.03

In previous Dgraph releases, multiple related flags are used in a command,
causing some commands to be very long. Starting in release 21.03, fewer flags are 
used for the most complex commands (`alpha`, `backup`, `bulk`,`debug`, `live` and
`zero`). Instead, many of these flags contain one or more options that let you 
define multiple settings in a semicolon-delimited list that's encapsulated in 
double-quotes. So, the general syntax for flags that contain options is as follows: 

`--<flagname> "option-a=value; option-b=value"`

For example, the following command that is valid in release 20.11 is no longer
valid starting in release 21.03:

```bash
dgraph alpha --ludicrous_mode=true ludicrous_concurrency=16
```

Instead, you would express this command as follows starting in release 21.03:

```bash
dgraph alpha --ludicrous "enabled=true; concurrency=16;"
```

The following table maps Dgraph CLI flags from release 20.11 and earlier to new
flags used starting in release 21.03; any flags not shown here are unchanged from
release 21.03.

| Old Flag | Old Type | New Flag and Options | New Type | Applies To |
|---------:|:---------|---------:|:---------|:----:|
| | | **`--badger`** | | | |
| `badger.compression` | string | `compression` | string | `alpha`, `bulk`, `backup`|
| | | (new) `goroutines` | int |`alpha`, `bulk`, `backup`|
| `badger.cache_mb` | string | `cache-mb` | string |`bulk`|
| `badger.cache_percentage` | string | `cache-percentage` | string |`bulk`|
| | | **`--acl`** | | |
| `acl_secret_file` | string | `secret-file` | string |`alpha`|
| `acl_access_ttl` | time.Duration | `access-ttl` | [string](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) |`alpha`|
| `acl_refresh_ttl` | time.Duration | `refresh-ttl` | [string](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) |`alpha`|
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
| | | **`--tls`** | |
| `tls_cacert` | string | `ca-cert` | string |`alpha`, `zero`, `bulk`, `backup`, `live`|
| `tls_use_system_ca` | bool | `use-system-ca` | bool |`alpha`, `zero`, `bulk`, `backup`, `live`|
| `tls_server_name` | string | `server-name` | string |`alpha`, `zero`, `bulk`, `backup`, `live`|
| `tls_client_auth` | string | `client-auth-type` | string |`alpha`, `zero`|
| `tls_node_cert` | string | `server-cert` | string |`alpha`, `zero`|
| `tls_node_key` | string | `server-key` | string |`alpha`, `zero`|
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
