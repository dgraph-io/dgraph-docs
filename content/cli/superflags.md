+++
title = "Superflags"
weight = 1
type = "docs"
[menu.main]
    parent = "cli"
+++

Dgraph uses *superflags* for complex commands: `alpha`, `backup`, `bulk`, `debug`, `live` and `zero`. Superflags are compound flags that contain one or more options, allowing you to define multiple related settings in a single, semicolon-delimited list.

## Syntax

The general syntax for superflags is:

```bash
--<super-flag-name> option-a=value; option-b=value
```

Semicolons are required between superflag options, but a semicolon after the last option is optional.

{{% notice "note" %}}
You should encapsulate the options for a superflag in double-quotes (`"`) if any of those option values include spaces. You can also use quotes to improve readability:
`--<super-flag-name> "option-a=value; option-b=value"`
{{% /notice %}}

## Available Superflags

* `--acl`
* `--badger`
* `--cache`
* `--encryption`
* `--graphql`
* `--limit`
* `--raft`
* `--security`
* `--telemetry`
* `--tls`
* `--trace`
* `--vault`

## ACL Superflag

The `--acl` superflag configures [Access Control List]({{< relref "../../enterprise-features/access-control-lists.md" >}}) settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `secret-file` | string | `alpha` | File that stores the HMAC secret used for signing the JWT |
| `access-ttl` | [duration](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) | `alpha` | TTL for the access JWT |
| `refresh-ttl` | [duration](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) | `alpha` | TTL for the refresh JWT |

## Badger Superflag

The `--badger` superflag configures [Badger](https://dgraph.io/docs/badger) database options:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `compression` | string | `alpha`, `bulk`, `backup` | Specifies the compression level and algorithm |
| `numgoroutines` | int | `alpha`, `bulk`, `backup` | Number of Go routines used by Dgraph |

{{% notice "note" %}}
The `--badger` superflag allows you to set many advanced [Badger options](https://pkg.go.dev/github.com/dgraph-io/badger/v3#Options), including:
`dir`, `valuedir`, `syncwrites`, `numversionstokeep`, `readonly`, `inmemory`, `metricsenabled`, `memtablesize`,
`basetablesize`, `baselevelsize`, `levelsizemultiplier`, `tablesizemultiplier`, `maxlevels`, `vlogpercentile`,
`valuethreshold`, `nummemtables`, `blocksize`, `bloomfalsepositive`, `blockcachesize`, `indexcachesize`, `numlevelzerotables`,
`numlevelzerotablesstall`, `valuelogfilesize`, `valuelogmaxentries`, `numcompactors`, `compactl0onclose`, `lmaxcompaction`,
`zstdcompressionlevel`, `verifyvaluechecksum`, `encryptionkeyrotationduration`, `bypasslockguard`, `checksumverificationmode`,
`detectconflicts`, `namespaceoffset`.
{{% /notice %}}

## Cache Superflag

The `--cache` superflag configures cache settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `size-mb` | string | `alpha` | Total size of cache (in MB) per shard in the reducer |
| `percentage` | string | `alpha` | Cache percentages for block cache and index cache |

## Encryption Superflag

The `--encryption` superflag configures encryption settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `key-file` | string | `alpha`, `bulk`, `live`, `restore`, `debug`, `decrypt`, `export_backup` | The file that stores the symmetric key |

## GraphQL Superflag

The `--graphql` superflag configures GraphQL settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `introspection` | bool | `alpha` | Enables GraphQL schema introspection |
| `debug` | bool | `alpha` | Enables debug mode in GraphQL |
| `extensions` | bool | `alpha` | Enables extensions in GraphQL response body |
| `poll-interval` | [duration](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) | `alpha` | The polling interval for GraphQL subscriptions |
| `lambda-url` | string | `alpha` | The URL of a lambda server that implements custom GraphQL JavaScript resolvers |

## Limit Superflag

The `--limit` superflag configures limit settings for Dgraph Alpha:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `txn-abort-after` | string | `alpha` | Abort any pending transactions older than this duration |
| `disable-admin-http` | string | `zero` | Turn on/off the administrative endpoints |
| `max-retries` | int | `alpha` | Maximum number of retries |
| `mutations` | string | `alpha` | Mutation mode: `allow`, `disallow`, or `strict` |
| `query-edge` | uint64 | `alpha` | Maximum number of edges that can be returned in a query |
| `normalize-node` | int | `alpha` | Maximum number of nodes that can be returned in a query that uses the normalize directive |
| `mutations-nquad` | int | `alpha` | Maximum number of nquads that can be inserted in a mutation request |
| `max-pending-queries` | int | `alpha` | Maximum number of concurrently processing requests allowed before requests are rejected with 429 Too Many Requests |

## Raft Superflag

The `--raft` superflag configures [Raft]({{< relref "../../design-concepts/raft.md" >}}) consensus settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `pending-proposals` | int | `alpha` | Maximum number of pending mutation proposals; useful for rate limiting |
| `idx` | int | `alpha`, `zero` | Provides an optional Raft ID that an Alpha node can use to join Raft groups |
| `group` | int | `alpha` | Provides an optional Raft group ID that an Alpha node can use to request group membership from a Zero node |
| `learner` | bool | `alpha`, `zero` | Make this Alpha a learner node (used for read-only replicas) |
| `snapshot-after-duration` | duration | `alpha` | Frequency at which Raft snapshots are created |
| `snapshot-after-entries` | int | `alpha` | Create a new Raft snapshot after the specified number of Raft entries |

## Security Superflag

The `--security` superflag configures security settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `token` | string | `alpha` | Authentication token |
| `whitelist` | string | `alpha` | A comma separated list of IP addresses, IP ranges, CIDR blocks, or hostnames for administration |

## Telemetry Superflag

The `--telemetry` superflag configures telemetry settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `reports` | bool | `alpha`, `zero` | Sends anonymous telemetry data to Dgraph |
| `sentry` | bool | `alpha`, `zero` | Enable sending crash events to Sentry |

## TLS Superflag

The `--tls` superflag configures [TLS]({{< relref "tls-configuration.md" >}}) settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `ca-cert` | string | `alpha`, `zero`, `bulk`, `backup`, `live` | The CA cert file used to verify server certificates |
| `use-system-ca` | bool | `alpha`, `zero`, `bulk`, `backup`, `live` | Include System CA with Dgraph Root CA |
| `server-name` | string | `alpha`, `zero`, `bulk`, `backup`, `live` | Server name, used for validating the server's TLS host name |
| `client-auth-type` | string | `alpha`, `zero` | TLS client authentication used to validate client connections from external ports |
| `server-cert` | string | `alpha`, `zero` | Path and filename of the node certificate (for example, `node.crt`) |
| `server-key` | string | `alpha`, `zero` | Path and filename of the node certificate private key (for example, `node.key`) |
| `internal-port` | bool | `alpha`, `zero`, `bulk`, `backup`, `live` | Makes internal ports (by default, 5080 and 7080) use the REQUIREANDVERIFY setting |
| `client-cert` | string | `alpha`, `zero`, `bulk`, `backup`, `live` | User cert file provided by the client to the Alpha node |
| `client-key` | string | `alpha`, `zero`, `bulk`, `backup`, `live` | User private key file provided by the client to the Alpha node |

## Trace Superflag

The `--trace` superflag configures [tracing]({{< relref "tracing.md" >}}) settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `ratio` | float64 | `alpha`, `zero` | The ratio of queries to trace |
| `jaeger` | string | `alpha`, `zero` | URL of Jaeger to send OpenCensus traces |
| `datadog` | string | `alpha`, `zero` | URL of Datadog to send OpenCensus traces |

## Vault Superflag

The `--vault` superflag configures Vault integration settings:

| Option | Type | Applies to | Description |
|--------|------|------------|-------------|
| `addr` | string | `alpha`, `bulk`, `backup`, `live`, `debug` | Vault server address, formatted as `http://ip-address:port` |
| `role-id-file` | string | `alpha`, `bulk`, `backup`, `live`, `debug` | File containing Vault `role-id` used for AppRole authentication |
| `secret-id-file` | string | `alpha`, `bulk`, `backup`, `live`, `debug` | File containing Vault `secret-id` used for AppRole authentication |
| `path` | string | `alpha`, `bulk`, `backup`, `live`, `debug` | Vault key=value store path (example: `secret/data/dgraph` for kv-v2, `kv/dgraph` for kv-v1) |
| `field` | string | `alpha`, `bulk`, `backup`, `live`, `debug` | Vault key=value store field whose value is the base64 encoded encryption key |
| `format` | string | `alpha`, `bulk`, `backup`, `live`, `debug` | Vault field format (`raw` or `base64`) |

## Using Superflags

To learn more about each superflag and its options, see the `--help` output of the specific Dgraph CLI commands, or refer to the individual command documentation pages.

