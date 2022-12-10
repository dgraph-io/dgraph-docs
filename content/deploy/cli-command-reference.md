+++
title = "Dgraph CLI Reference"
weight = 20
[menu.main]
    parent = "deploy"
+++


You can use the Dgraph command-line interface (CLI) to deploy and manage Dgraph.
You use it in self-managed deployment scenarios; such as running Dgraph on
on-premises servers hosted on your physical infrastructure, or running Dgraph in
the cloud on your AWS, GCP, or Azure infrastructure. 

Dgraph has a root command used throughout its CLI: `dgraph`. The `dgraph` command
is supported by multiple subcommands (such as `alpha` or `update`), some of which
are also supported by their own subcommands. For example, the `dgraph acl`
command requires you to specify one of its subcommands: `add`, `del`, `info` or
`mod`. As with other CLIs, you provide command options using flags like `--help`
or `--telemetry`. 

{{% notice "tip" %}}
The term *command* is used instead of *subcommand* throughout this document, 
except when clarifying relationships in the CLI command hierarchy. The
term *command* is also used for combinations of commands and their subcommands,
such as `dgraph alpha debug`. 
{{% /notice %}}

## Dgraph CLI superflags in release v21.03

Some flags are deprecated and replaced in release v21.03. In previous Dgraph
releases, multiple related flags are often used in a command, causing some 
commands to be very long. Starting in release v21.03, Dgraph uses *superflags* 
for some flags used by the most complex commands: `alpha`, `backup`, `bulk`,
`debug`, `live` and `zero`. Superflags are compound flags: they contain one or
more options that let you define multiple settings in a semicolon-delimited list.
Semicolons are required between superflag options, but a semicolon after the last
superflag option is optional.

The general syntax for superflags is as follows: `--<super-flag-name> option-a=value; option-b=value`

{{% notice "note" %}}
You should encapsulate the options for a superflag in double-quotes (`"`) if any
of those option values include spaces. You can also encapsulate options in
double-quotes to improve readability. So, you can also use the following
syntax for superflags: `--<super-flag-name> "option-a=value; option-b=value"`.
{{% /notice %}}

Release v21.03 includes the following superflags:
* `--acl`
* `--badger`
* `--cache`
* `--encryption`
* `--graphql`
* `--limit`
* `--ludicrous`
* `--raft`
* `--security`
* `--telemetry`
* `--tls`
* `--trace`
* `--vault`

For example, the following command that is valid in release v20.11 is no longer
valid starting in release v21.03:

```sh
dgraph alpha --ludicrous_mode=true ludicrous_concurrency=16
```

Instead, you can express this command as follows starting in release v21.03:

```sh

dgraph alpha --ludicrous enabled=true; concurrency=16;
```

The following table maps Dgraph CLI flags from release v20.11 and earlier that
have been replaced by superflags (and their options) in release v21.03. Any flags
not shown here are unchanged in release v21.03. 

### ACL superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--acl`** | | | [Access Control List]({{< relref "enterprise-features/access-control-lists.md" >}}) superflag |
| `--acl_secret_file` | string | `secret-file` | string |`alpha`| File that stores the HMAC secret that is used for signing the JWT |
| `--acl_access_ttl` | time.Duration | `access-ttl` | [string](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) |`alpha`| TTL for the access JWT |
| `--acl_refresh_ttl` | time.Duration | `refresh-ttl` | [string](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) |`alpha`| The TTL for the refresh JWT |

### Badger superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--badger`** | | |  [Badger](https://dgraph.io/docs/badger) superflag |
| `--badger.compression` | string | `compression` | string | `alpha`, `bulk`, `backup`| Specifies the compression level and algorithm |
||| (new) [`numgoroutines`]({{< relref "troubleshooting.md" >}}) | int |`alpha`, `bulk`, `backup`| Number of Go routines used by Dgraph |

{{% notice "note" %}}
The `--badger` superflag allows you to set many advanced [Badger options](https://pkg.go.dev/github.com/dgraph-io/badger/v3#Options), including:
`dir`, `valuedir`, `syncwrites`, `numversionstokeep`, `readonly`, `inmemory`, `metricsenabled`, `memtablesize`,
`basetablesize`, `baselevelsize`, `levelsizemultiplier`, `tablesizemultiplier`, `maxlevels`, `vlogpercentile`,
`valuethreshold`, `nummemtables`, `blocksize`, `bloomfalsepositive`, `blockcachesize`, `indexcachesize`, `numlevelzerotables`,
`numlevelzerotablesstall`, `valuelogfilesize`, `valuelogmaxentries`, `numcompactors`, `compactl0onclose`, `lmaxcompaction`,
`zstdcompressionlevel`, `verifyvaluechecksum`, `encryptionkeyrotationduration`, `bypasslockguard`, `checksumverificationmode`,
`detectconflicts`, `namespaceoffset`.
{{% /notice %}}

### Cache superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--cache`** | | |  Cache superflag |
| `cache_mb` | string | `size-mb` | string |`alpha`| Total size of cache (in MB) per shard in the reducer |
| `cache_percentage` | string | `percentage` | string |`alpha`| Cache percentages for block cache and index cache |

### Encryption superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--encryption`** | | |  Encryption superflag |
| `--encryption_key_file` | string | `key-file` | string |`alpha`, `bulk`, `live`, `restore`, `debug`, `decrypt`, `export_backup` | The file that stores the symmetric key |

### GraphQL superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--graphql`** | | | [GraphQL]({{< relref "graphql/overview.md" >}}) superflag  |
| `--graphql_introspection` | bool | `introspection` | bool |`alpha`| Enables GraphQL schema introspection |
| `--graphql_debug` | bool | `debug` | bool |`alpha`| Enables debug mode in GraphQL |
| `--graphql_extensions` | bool | `extensions` | bool |`alpha`| Enables extensions in GraphQL response body |
| `--graphql_poll_interval` | time.Duration | `poll-interval` | [string](https://github.com/dgraph-io/ristretto/blob/master/z/flags.go#L80-L98) |`alpha`| The polling interval for GraphQL subscriptions | 
| `--graphql_lambda_url` | string | `lambda-url` | string |`alpha`| The URL of a lambda server that implements custom GraphQL JavaScript resolvers |

### Limit superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--limit`** | | | Limit-setting superflag for Dgraph Alpha  |
| `--abort_older_than` | string | `txn-abort-after` | string |`alpha`| Abort any pending transactions older than this duration |
| `--disable_admin_http` | string | `disable-admin-http` | string |`zero`| Turn on/off the administrative endpoints |
| `--max_retries` | int | `max-retries` | int |`alpha`| Maximum number of retries |
| `--mutations` | string | `mutations` | string |`alpha`| Mutation mode: `allow`, `disallow`, or `strict` |
| `--query_edge_limit` | uint64 | `query-edge` | uint64 |`alpha`| Maximum number of edges that can be returned in a query |
| `--normalize_node_limit` | int | `normalize-node` | int |`alpha`| Maximum number of nodes that can be returned in a query that uses the normalize directive |
| `--mutations_nquad_limit` | int | `mutations-nquad` | int |`alpha`| Maximum number of nquads that can be inserted in a mutation request |

### Ludicrous mode superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--ludicrous`** | | | [Ludicrous Mode]({{< relref "deploy/ludicrous-mode.md" >}}) superflag  |
| `--ludicrous_mode` | bool | `enabled` | bool |`alpha`| Enables Ludicrous mode |
| `--ludicrous_concurrency` | int | `concurrency` | int |`alpha`| Number of concurrent threads to use in Ludicrous mode |

### Raft superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--raft`** | | | [Raft]({{< relref "design-concepts/raft.md" >}}) superflag  |
| `--pending_proposals` | int | `pending-proposals` | int |`alpha`|  Maximum number of pending mutation proposals; useful for rate limiting |
| `--idx` | int | `idx` | int |`alpha`, `zero`| Provides an optional Raft ID that an Alpha node can use to join Raft groups |
| `--group` | int | `group` | int |`alpha`| Provides an optional Raft group ID that an Alpha node can use to request group membership from a Zero node |
|  |  | (new)`learner` | bool | `alpha`, `zero`| Make this Alpha a learner node (used for read-only replicas) |
| | | (new)`snapshot-after-duration` | int |`alpha`|  Frequency at which Raft snapshots are created |
| `--snapshot-after` | int | `snapshot-after-entries` | int |`alpha`|  Create a new Raft snapshot after the specified number of Raft entries |

### Security superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--security`** | | | Security superflag |
| `--auth_token` | string | `token` | string |`alpha`| Authentication token |
| `--whitelist` | string | `whitelist` | string |`alpha`| A comma separated list of IP addresses, IP ranges, CIDR blocks, or hostnames for administration |
| | | **`--telemetry`** | | | Telemetry superflag  |
| `--telemetry` | bool | `reports` | bool |`alpha` and `zero`| Sends anonymous telemetry data to Dgraph |
| `--enable_sentry` | bool | `sentry` | bool |`alpha` and `zero`| Enable sending crash events to Sentry |

### TLS superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--tls`** | | | [TLS]({{< relref "deploy/tls-configuration.md" >}}) superflag  |
| `--tls_cacert` | string | `ca-cert` | string |`alpha`, `zero`, `bulk`, `backup`, `live`| The CA cert file used to verify server certificates |
| `--tls_use_system_ca` | bool | `use-system-ca` | bool |`alpha`, `zero`, `bulk`, `backup`, `live`| Include System CA with Dgraph Root CA |
| `--tls_server_name` | string | `server-name` | string |`alpha`, `zero`, `bulk`, `backup`, `live`| Server name, used for validating the server’s TLS host name |
| `--tls_client_auth` | string | `client-auth-type` | string |`alpha`, `zero`| TLS client authentication used to validate client connections from external ports |
| `--tls_node_cert` | string | `server-cert` | string |`alpha` and `zero`|  Path and filename of the node certificate (for example, `node.crt`) |
| `--tls_node_key` | string | `server-key` | string |`alpha` and `zero`| Path and filename of the node certificate private key (for example, `node.key`) |
| `--tls_internal_port_enabled` | bool | `internal-port` | bool | `alpha`, `zero`, `bulk`, `backup`, `live`| Makes internal ports (by default, 5080 and 7080) use the REQUIREANDVERIFY setting. |
| `--tls_cert` | string | `client-cert` | string |`alpha`, `zero`, `bulk`, `backup`, `live`| User cert file provided by the client to the Alpha node |
| `--tls_key` | string | `client-key` | string |`alpha`, `zero`, `bulk`, `backup`, `live`| User private key file provided by the client to the Alpha node |

### Trace superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--trace`** | | | [Tracing]({{< relref "deploy/tracing.md" >}}) superflag  |
| `--trace` | float64 | `ratio` | float64 |`alpha`, `zero`| The ratio of queries to trace |
| `--jaeger.collector` | string | `jaeger` | string | `alpha`, `zero`| URL of Jaeger to send OpenCensus traces |
| `--datadog.collector` | string | `datadog` | string | `alpha`, `zero`| URL of Datadog to send OpenCensus traces

### Vault superflag

| Old flag | Old type | New superflag and options | New type | Applies to | Notes |
|---------:|:---------|---------:|:---------|:----:|:----:|
| | | **`--vault`** | | | Vault superflag  |
| `--vault_addr` | string | `addr` | string | `alpha`, `bulk`, `backup`, `live`, `debug`| Vault server address, formatted as of `http://ip-address:port` |
| `--vault_roleid_file` | string | `role-id-file` | string | `alpha`, `bulk`, `backup`, `live`, `debug`| File containing Vault `role-id` used for AppRole authentication |
| `--vault_secretid_file` | string | `secret-id-file` | string |`alpha`, `bulk`, `backup`, `live`, `debug`| File containing Vault `secret-id` used for AppRole authentication |
| `--vault_path` | string | `path` | string | `alpha`, `bulk`, `backup`, `live`, `debug`| Vault key=value store path (example: `secret/data/dgraph` for kv-v2, `kv/dgraph` for kv-v1) |
| `--vault_field` | string | `field` | string |`alpha`, `bulk`, `backup`, `live`, `debug`| Vault key=value store field whose value is the base64 encoded encryption key |
| `--vault_format` | string | `format` | string | `alpha`, `bulk`, `backup`, `live`, `debug`| Vault field format (`raw` or `base64`) |

To learn more about each superflag and its options, see the `--help` output of
the Dgraph CLI commands listed in the following section.

## Dgraph CLI command help listing

The Dgraph CLI includes the root `dgraph` command and its subcommands. The CLI
help for these commands is replicated inline below for your reference, or you
can find help by calling these commands (or their subcommands) using the `--help`
flag.

{{% notice "note" %}}
Although many of the commands listed below have subcommands, only `dgraph` and
subcommands of `dgraph` are included in this listing. 
{{% /notice %}}

The Dgraph CLI has several commands, which are organized into the following groups:

* [Dgraph core](#dgraph-core-commands)
* [Data loading](#data-loading-commands)
* [Dgraph security](#dgraph-security-commands)
* [Dgraph debug](#dgraph-debug-commands)
* [Dgraph tools](#dgraph-tools-commands)

The commands in these groups are shown in the following table:

|Group             | Command                        | Note                         | 
|------------------|--------------------------------|------------------------------|
| (root)           | [`dgraph`](#dgraph-root-command) | Root command for Dgraph CLI  |          
| Dgraph core      | [`alpha`](#dgraph-alpha) | Dgraph Alpha database node commands |
| Dgraph core      | [`zero`](#dgraph-zero) | Dgraph Zero management node commands |
| Data loading     | [`bulk`](#dgraph-bulk) | Dgraph [Bulk Loader]({{< relref "deploy/fast-data-loading/bulk-loader.md" >}}) commands     |
| Data loading     | [`live`](#dgraph-live) | Dgraph [Live Loader]({{< relref "deploy/fast-data-loading/live-loader.md" >}}) commands     |
| Data loading     | [`restore`](#dgraph-restore) | Command used to restore backups created using Dgraph Enterprise Edition     |
| Dgraph security  | [`acl`](#dgraph-acl) | Dgraph [Access Control List (ACL)]({{< relref "enterprise-features/access-control-lists.md" >}}) commands |
| Dgraph security  | [`audit`](#dgraph-audit) | Decrypt audit files     |
| Dgraph security  | [`cert`](#dgraph-cert) | Configure TLS and manage TLS certificates     |
| Dgraph debug     | [`debug`](#dgraph-debug)    | Used to debug issues with Dgraph     |
| Dgraph debug     | [`debuginfo`](#dgraph-debuginfo)    | Generates information about the current node for use in debugging issues with Dgraph clusters   |
| Dgraph tools     | [`completion`](#dgraph-completion)    | Generates shell completion scripts for `bash` and `zsh`     |
| Dgraph tools     | [`conv`](#dgraph-conv)    | Converts geographic files into RDF so that they can be consumed by Dgraph    |
| Dgraph tools     | [`decrypt`](#dgraph-decrypt)    | Decrypts an export file created by an encrypted Dgraph cluster     |
| Dgraph tools     | [`export_backup`](#dgraph-export_backup)    | Converts a binary backup created using Dgraph Enterprise Edition into an exported folder.      |
| Dgraph tools     | [`increment`](#dgraph-increment)    | Increments a counter transactionally to confirm that a Dgraph Alpha node can handle query and mutation requests |
| Dgraph tools     | [`lsbackup`](#dgraph-lsbackup)    | Lists information on backups in a given location   |
| Dgraph tools     | [`migrate`](#dgraph-migrate)    | Migrates data from a MySQL database to Dgraph |
| Dgraph tools     | [`raftmigrate`](#dgraph-raftmigrate)    | Dgraph Raft migration tool     |
| Dgraph tools     | [`upgrade`](#dgraph-upgrade)    | Upgrades Dgraph to a newer version     |

### `dgraph` root command

This command is the root for all commands in the Dgraph CLI. Key information from
the help listing for `dgraph --help` is shown below:

```shell
Usage:
  dgraph [command] 

Generic:             
 help          Help about any command        
 version       Prints the dgraph version details 

Available Commands:

Dgraph Core:   
  alpha         Run Dgraph Alpha database server                   
  zero          Run Dgraph Zero management server 

Data Loading:     
  bulk          Run Dgraph Bulk Loader          
  live          Run Dgraph Live Loader    
  restore       Restore backup from Dgraph Enterprise Edition   

Dgraph Security:  
  acl           Run the Dgraph Enterprise Edition ACL tool  
  audit         Dgraph audit tool  
  cert          Dgraph TLS certificate management                

Dgraph Debug:         
  debug         Debug Dgraph instance 
  debuginfo     Generate debug information on the current node            

Dgraph Tools:       
  completion    Generates shell completion scripts for bash or zsh 
  conv          Dgraph Geo file converter   
  decrypt       Run the Dgraph decryption tool 
  export_backup Export data inside single full or incremental backup  
  increment     Increment a counter transactionally  
  lsbackup      List info on backups in a given location 
  migrate       Run the Dgraph migration tool from a MySQL database to Dgraph 
  raftmigrate   Run the Raft migration tool  
  upgrade       Run the Dgraph upgrade tool  

Flags:
      --alsologtostderr                  log to standard error as well as files
      --bindall                          Use 0.0.0.0 instead of localhost to bind to all addresses on local machine. (default true)
      --block_rate int                   Block profiling rate. Must be used along with block profile_mode
      --config string                    Configuration file. Takes precedence over default values, but is overridden to values set with environment variables and flags.
      --cwd string                       Change working directory to the path specified. The parent must exist.
      --expose_trace                     Allow trace endpoint to be accessible from remote
  -h, --help                             help for dgraph
      --log_backtrace_at traceLocation   when logging hits line file:N, emit a stack trace (default :0)
      --log_dir string                   If non-empty, write log files in this directory
      --logtostderr                      log to standard error instead of files
      --profile_mode string              Enable profiling mode, one of [cpu, mem, mutex, block]
  -v, --v Level                          log level for V logs
      --vmodule moduleSpec               comma-separated list of pattern=N settings for file-filtered logging

```

### Dgraph core commands

Dgraph core commands provide core deployment and management functionality
for the Dgraph Alpha database nodes and Dgraph Zero management nodes in your
deployment.

#### `dgraph alpha`

This command is used to configure and run the Dgraph Alpha database nodes in
your deployment. The following replicates the help listing for `dgraph alpha --help`:


```shell
A Dgraph Alpha instance stores the data. Each Dgraph Alpha is responsible for
storing and serving one data group. If multiple Alphas serve the same group,
they form a Raft group and provide synchronous replication.
 
Usage:
  dgraph alpha [flags] 

Flags:
      --acl string                 [Enterprise Feature] ACL options
                                       access-ttl=6h; The TTL for the access JWT.
                                       refresh-ttl=30d; The TTL for the refresh JWT.
                                       secret-file=; The file that stores the HMAC secret, which is used for signing the JWT and should have at least 32 ASCII characters. Required to enable ACLs.
                                    (default "access-ttl=6h; refresh-ttl=30d; secret-file=;")
      --audit string               Audit options
                                       compress=false; Enables the compression of old audit logs.
                                       days=10; The number of days audit logs will be preserved.
                                       encrypt-file=; The path to the key file to be used for audit log encryption.
                                       output=; [stdout, /path/to/dir] This specifies where audit logs should be output to.
                                   			"stdout" is for standard output. You can also specify the directory where audit logs
                                   			will be saved. When stdout is specified as output other fields will be ignored.
                                       size=100; The audit log max size in MB after which it will be rolled over.
                                    (default "compress=false; days=10; size=100; dir=; output=; encrypt-file=;")
      --badger string              Badger options
                                       compression=snappy; [none, zstd:level, snappy] Specifies the compression algorithm and
                                   			compression level (if applicable) for the postings directory."none" would disable
                                   			compression, while "zstd:1" would set zstd compression at level 1.
                                       goroutines=8; The number of goroutines to use in badger.Stream.
                                       max-retries=-1; Commits to disk will give up after these number of retries to prevent locking the worker in a failed state. Use -1 to retry infinitely.
                                    (default "compression=snappy; goroutines=8; max-retries=-1;")
      --cache string               Cache options
                                       percentage=0,65,35; Cache percentages summing up to 100 for various caches (FORMAT: PostingListCache,PstoreBlockCache,PstoreIndexCache)
                                       size-mb=1024; Total size of cache (in MB) to be used in Dgraph.
                                    (default "size-mb=1024; percentage=0,65,35;")
      --cdc string                 Change Data Capture options
                                       ca-cert=; The path to CA cert file for TLS encryption.
                                       client-cert=; The path to client cert file for TLS encryption.
                                       client-key=; The path to client key file for TLS encryption.
                                       file=; The path where audit logs will be stored.
                                       kafka=; A comma separated list of Kafka hosts.
                                       sasl-password=; The SASL password for Kafka.
                                       sasl-user=; The SASL username for Kafka.
                                    (default "file=; kafka=; sasl_user=; sasl_password=; ca_cert=; client_cert=; client_key=;")
      --custom_tokenizers string   Comma separated list of tokenizer plugins for custom indices.
      --encryption string          [Enterprise Feature] Encryption At Rest options
                                       key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                                    (default "key-file=;")
      --export string              Folder in which to store exports. (default "export")
      --graphql string             GraphQL options
                                       debug=false; Enables debug mode in GraphQL. This returns auth errors to clients, and we do not recommend turning it on for production.
                                       extensions=true; Enables extensions in GraphQL response body.
                                       introspection=true; Enables GraphQL schema introspection.
                                       lambda-url=; The URL of a lambda server that implements custom GraphQL Javascript resolvers.
                                       poll-interval=1s; The polling interval for GraphQL subscription.
                                    (default "introspection=true; debug=false; extensions=true; poll-interval=1s; lambda-url=;")
  -h, --help                       help for alpha
      --limit string               Limit options
                                       disallow-drop=false; Set disallow-drop to true to block drop-all and drop-data operation. It still allows dropping attributes and types.
                                       mutations-nquad=1000000; The maximum number of nquads that can be inserted in a mutation request.
                                       mutations=allow; [allow, disallow, strict] The mutations mode to use.
                                       normalize-node=10000; The maximum number of nodes that can be returned in a query that uses the normalize directive.
                                       query-edge=1000000; The maximum number of edges that can be returned in a query. This applies to shortest path and recursive queries.
                                       query-timeout=0ms; Maximum time after which a query execution will fail. If set to 0, the timeout is infinite.
                                       txn-abort-after=5m; Abort any pending transactions older than this duration. The liveness of a transaction is determined by its last mutation.
                                    (default "mutations=allow; query-edge=1000000; normalize-node=10000; mutations-nquad=1000000; disallow-drop=false; query-timeout=0ms; txn-abort-after=5m;")
      --ludicrous string           Ludicrous options
                                       concurrency=2000; The number of concurrent threads to use in Ludicrous mode.
                                       enabled=false; Set enabled to true to run Dgraph in Ludicrous mode.
                                    (default "enabled=false; concurrency=2000;")
      --my string                  addr:port of this server, so other Dgraph servers can talk to this.
  -o, --port_offset int            Value added to all listening port numbers. [Internal=7080, HTTP=8080, Grpc=9080]
  -p, --postings string            Directory to store posting lists. (default "p")
      --raft string                Raft options
                                       group=; Provides an optional Raft Group ID that this Alpha would indicate to Zero to join.
                                       idx=; Provides an optional Raft ID that this Alpha would use to join Raft groups.
                                       learner=false; Make this Alpha a "learner" node. In learner mode, this Alpha will not participate in Raft elections. This can be used to achieve a read-only replica.
                                       pending-proposals=256; Number of pending mutation proposals. Useful for rate limiting.
                                       snapshot-after-duration=30m; Frequency at which we should create a new raft snapshots. Set to 0 to disable duration based snapshot.
                                       snapshot-after-entries=10000; Create a new Raft snapshot after N number of Raft entries. The lower this number, the more frequent snapshot creation will be. Snapshots are created only if both snapshot-after-duration and snapshot-after-entries threshold are crossed.
                                    (default "learner=false; snapshot-after-entries=10000; snapshot-after-duration=30m; pending-proposals=256; idx=; group=;")
      --security string            Security options
                                       token=; If set, all Admin requests to Dgraph will need to have this token. The token can be passed as follows: for HTTP requests, in the X-Dgraph-AuthToken header. For Grpc, in auth-token key in the context.
                                       whitelist=; A comma separated list of IP addresses, IP ranges, CIDR blocks, or hostnames you wish to whitelist for performing admin actions (i.e., --security "whitelist=144.142.126.254,127.0.0.1:127.0.0.3,192.168.0.0/16,host.docker.internal").
                                    (default "token=; whitelist=;")
      --survive string             Choose between "process" or "filesystem".
                                       If set to "process", there would be no data loss in case of process crash, but the behavior would be indeterministic in case of filesystem crash.
                                       If set to "filesystem", blocking sync would be called after every write, hence guaranteeing no data loss in case of hard reboot.
                                       Most users should be OK with choosing "process". (default "process")
      --telemetry string           Telemetry (diagnostic) options
                                       reports=true; Send anonymous telemetry data to Dgraph devs.
                                       sentry=true; Send crash events to Sentry.
                                    (default "reports=true; sentry=true;")
      --tls string                 TLS Server options
                                       ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                       client-auth-type=VERIFYIFGIVEN; The TLS client authentication method.
                                       client-cert=; (Optional) The client Cert file which is needed to connect as a client with the other nodes in the cluster.
                                       client-key=; (Optional) The private client Key file which is needed to connect as a client with the other nodes in the cluster.
                                       internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                       server-cert=; The server Cert file which is needed to initiate the server in the cluster.
                                       server-key=; The server Key file which is needed to initiate the server in the cluster.
                                       use-system-ca=true; Includes System CA into CA Certs.
                                    (default "use-system-ca=true; client-auth-type=VERIFYIFGIVEN; internal-port=false;")
      --tmp string                 Directory to store temporary buffers. (default "t")
      --trace string               Trace options
                                       datadog=; URL of Datadog to send OpenCensus traces. As of now, the trace exporter does not support annotation logs and discards them.
                                       jaeger=; URL of Jaeger to send OpenCensus traces.
                                       ratio=0.01; The ratio of queries to trace.
                                    (default "ratio=0.01; jaeger=; datadog=;")
      --vault string               Vault options
                                       acl-field=; Vault field containing ACL key.
                                       acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                       addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                       enc-field=; Vault field containing encryption key.
                                       enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                       path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                       role-id-file=; Vault RoleID file, used for AppRole authentication.
                                       secret-id-file=; Vault SecretID file, used for AppRole authentication.
                                    (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")
  -w, --wal string                 Directory to store raft write-ahead logs. (default "w")
  -z, --zero string                Comma separated list of Dgraph Zero addresses of the form IP_ADDRESS:PORT. (default "localhost:5080")

Use "dgraph alpha [command] --help" for more information about a command.
```

#### `dgraph zero`

This command is used to configure and run the Dgraph Zero management nodes in
your deployment. The following replicates the help listing shown when you run
`dgraph zero --help`:

```shell
A Dgraph Zero instance manages the Dgraph cluster.  Typically, a single Zero
instance is sufficient for the cluster; however, one can run multiple Zero
instances to achieve high-availability.
 
Usage:
  dgraph zero [flags] 

Flags:
      --audit string                  Audit options
                                          compress=false; Enables the compression of old audit logs.
                                          days=10; The number of days audit logs will be preserved.
                                          encrypt-file=; The path to the key file to be used for audit log encryption.
                                          output=; [stdout, /path/to/dir] This specifies where audit logs should be output to.
                                      			"stdout" is for standard output. You can also specify the directory where audit logs 
                                      			will be saved. When stdout is specified as output other fields will be ignored.
                                          size=100; The audit log max size in MB after which it will be rolled over.
                                       (default "compress=false; days=10; size=100; dir=; output=; encrypt-file=;")
      --enterprise_license string     Path to the enterprise license file.
  -h, --help                          help for zero
      --limit string                  Limit options
                                          disable-admin-http=false; Turn on/off the administrative endpoints exposed over Zero's HTTP port.
                                          refill-interval=30s; The interval after which the tokens for UID lease are replenished.
                                          uid-lease=0; The maximum number of UIDs that can be leased by namespace (except default namespace)
                                      			in an interval specified by refill-interval. Set it to 0 to remove limiting.
                                       (default "uid-lease=0; refill-interval=30s; disable-admin-http=false;")
      --my string                     addr:port of this server, so other Dgraph servers can talk to this.
      --peer string                   Address of another dgraphzero server.
  -o, --port_offset int               Value added to all listening port numbers. [Grpc=5080, HTTP=6080]
      --raft string                   Raft options
                                          idx=1; Provides an optional Raft ID that this Alpha would use to join Raft groups.
                                          learner=false; Make this Zero a "learner" node. In learner mode, this Zero will not participate in Raft elections. This can be used to achieve a read-only replica.
                                       (default "idx=1; learner=false;")
      --rebalance_interval duration   Interval for trying a predicate move. (default 8m0s)
      --replicas int                  How many Dgraph Alpha replicas to run per data shard group. The count includes the original shard. (default 1)
      --survive string                Choose between "process" or "filesystem".
                                          If set to "process", there would be no data loss in case of process crash, but the behavior would be indeterministic in case of filesystem crash.
                                          If set to "filesystem", blocking sync would be called after every write, hence guaranteeing no data loss in case of hard reboot.
                                          Most users should be OK with choosing "process". (default "process")
      --telemetry string              Telemetry (diagnostic) options
                                          reports=true; Send anonymous telemetry data to Dgraph devs.
                                          sentry=true; Send crash events to Sentry.
                                       (default "reports=true; sentry=true;")
      --tls string                    TLS Server options
                                          ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                          client-auth-type=VERIFYIFGIVEN; The TLS client authentication method.
                                          client-cert=; (Optional) The client Cert file which is needed to connect as a client with the other nodes in the cluster.
                                          client-key=; (Optional) The private client Key file which is needed to connect as a client with the other nodes in the cluster.
                                          internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                          server-cert=; The server Cert file which is needed to initiate the server in the cluster.
                                          server-key=; The server Key file which is needed to initiate the server in the cluster.
                                          use-system-ca=true; Includes System CA into CA Certs.
                                       (default "use-system-ca=true; client-auth-type=VERIFYIFGIVEN; internal-port=false;")
      --trace string                  Trace options
                                          datadog=; URL of Datadog to send OpenCensus traces. As of now, the trace exporter does not support annotation logs and discards them.
                                          jaeger=; URL of Jaeger to send OpenCensus traces.
                                          ratio=0.01; The ratio of queries to trace.
                                       (default "ratio=0.01; jaeger=; datadog=;")
  -w, --wal string                    Directory storing WAL. (default "zw")

Use "dgraph zero [command] --help" for more information about a command.
```

### Data loading commands

#### `dgraph bulk`

This command is used to bulk load data with the Dgraph
[Bulk Loader]({{< relref "deploy/fast-data-loading/bulk-loader.md"  >}}) tool.
The following replicates the help listing shown when you run `dgraph bulk --help`:

```shell
 Run Dgraph Bulk Loader 
Usage:
  dgraph bulk [flags] 

Flags:
      --badger string              Badger options (Refer to badger documentation for all possible options)
                                       compression=snappy; Specifies the compression algorithm and compression level (if applicable) for the postings directory. "none" would disable compression, while "zstd:1" would set zstd compression at level 1.
                                       numgoroutines=8; The number of goroutines to use in badger.Stream.
                                    (default "compression=snappy; numgoroutines=8;")
      --cleanup_tmp                Clean up the tmp directory after the loader finishes. Setting this to false allows the bulk loader can be re-run while skipping the map phase. (default true)
      --custom_tokenizers string   Comma separated list of tokenizer plugins
      --encrypted                  Flag to indicate whether schema and data files are encrypted. Must be specified with --encryption or vault option(s).
      --encrypted_out              Flag to indicate whether to encrypt the output. Must be specified with --encryption or vault option(s).
      --encryption string          [Enterprise Feature] Encryption At Rest options
                                       key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                                    (default "key-file=;")
  -f, --files string               Location of *.rdf(.gz) or *.json(.gz) file(s) to load.
      --force-namespace uint       Namespace onto which to load the data. If not set, will preserve the namespace. (default 18446744073709551615)
      --format string              Specify file format (rdf or json) instead of getting it from filename.
  -g, --graphql_schema string      Location of the GraphQL schema file.
  -h, --help                       help for bulk
      --http string                Address to serve http (pprof). (default "localhost:8080")
      --ignore_errors              ignore line parsing errors in rdf files
      --map_shards int             Number of map output shards. Must be greater than or equal to the number of reduce shards. Increasing allows more evenly sized reduce shards, at the expense of increased memory usage. (default 1)
      --mapoutput_mb int           The estimated size of each map file output. Increasing this increases memory usage. (default 2048)
      --new_uids                   Ignore UIDs in load files and assign new ones.
  -j, --num_go_routines int        Number of worker threads to use. MORE THREADS LEAD TO HIGHER RAM USAGE. (default 1)
      --out string                 Location to write the final dgraph data directories. (default "./out")
      --partition_mb int           Pick a partition key every N megabytes of data. (default 4)
      --reduce_shards int          Number of reduce shards. This determines the number of dgraph instances in the final cluster. Increasing this potentially decreases the reduce stage runtime by using more parallelism, but increases memory usage. (default 1)
      --reducers int               Number of reducers to run concurrently. Increasing this can improve performance, and must be less than or equal to the number of reduce shards. (default 1)
      --replace_out                Replace out directory and its contents if it exists.
  -s, --schema string              Location of schema file.
      --skip_map_phase             Skip the map phase (assumes that map output files already exist).
      --store_xids                 Generate an xid edge for each node.
      --tls string                 TLS Client options
                                       ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                       client-cert=; (Optional) The Cert file provided by the client to the server.
                                       client-key=; (Optional) The private Key file provided by the clients to the server.
                                       internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                       server-name=; Used to verify the server hostname.
                                       use-system-ca=true; Includes System CA into CA Certs.
                                    (default "use-system-ca=true; internal-port=false;")
      --tmp string                 Temp directory used to use for on-disk scratch space. Requires free space proportional to the size of the RDF file and the amount of indexing used. (default "tmp")
      --vault string               Vault options
                                       acl-field=; Vault field containing ACL key.
                                       acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                       addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                       enc-field=; Vault field containing encryption key.
                                       enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                       path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                       role-id-file=; Vault RoleID file, used for AppRole authentication.
                                       secret-id-file=; Vault SecretID file, used for AppRole authentication.
                                    (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")
      --version                    Prints the version of Dgraph Bulk Loader.
      --xidmap string              Directory to store xid to uid mapping
  -z, --zero string                gRPC address for Dgraph zero (default "localhost:5080")

Use "dgraph bulk [command] --help" for more information about a command.
```

#### `dgraph live`

This command is used to load live data with the Dgraph [Live Loader]({{< relref "deploy/fast-data-loading/live-loader.md" >}}) tool.
The following replicates the help listing shown when you run `dgraph live --help`:

```shell
 Run Dgraph Live Loader 
Usage:
  dgraph live [flags] 

Flags:
  -a, --alpha string                 Comma-separated list of Dgraph alpha gRPC server addresses (default "127.0.0.1:9080")
  -t, --auth_token string            The auth token passed to the server for Alter operation of the schema file. If used with --slash_grpc_endpoint, then this should be set to the API token issuedby Slash GraphQL
  -b, --batch int                    Number of N-Quads to send as part of a mutation. (default 1000)
  -m, --bufferSize string            Buffer for each thread (default "100")
  -c, --conc int                     Number of concurrent requests to make to Dgraph (default 10)
      --creds string                 Various login credentials if login is required.
                                     	user defines the username to login.
                                     	password defines the password of the user.
                                     	namespace defines the namespace to log into.
                                     	Sample flag could look like --creds user=username;password=mypass;namespace=2
      --encryption string            [Enterprise Feature] Encryption At Rest options
                                         key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                                      (default "key-file=;")
  -f, --files string                 Location of *.rdf(.gz) or *.json(.gz) file(s) to load
      --force-namespace int          Namespace onto which to load the data.Only guardian of galaxy should use this for loading data into multiple namespaces or somespecific namespace. Setting it to negative value will preserve the namespace.
      --format string                Specify file format (rdf or json) instead of getting it from filename
  -h, --help                         help for live
      --http string                  Address to serve http (pprof). (default "localhost:6060")
      --ludicrous                    Run live loader in ludicrous mode (Should only be done when alpha is under ludicrous mode)
      --new_uids                     Ignore UIDs in load files and assign new ones.
  -s, --schema string                Location of schema file
      --slash_grpc_endpoint string   Path to Slash GraphQL GRPC endpoint. If --slash_grpc_endpoint is set, all other TLS options and connection options will beignored
      --tls string                   TLS Client options
                                         ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                         client-cert=; (Optional) The Cert file provided by the client to the server.
                                         client-key=; (Optional) The private Key file provided by the clients to the server.
                                         internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                         server-name=; Used to verify the server hostname.
                                         use-system-ca=true; Includes System CA into CA Certs.
                                      (default "use-system-ca=true; internal-port=false;")
      --tmp string                   Directory to store temporary buffers. (default "t")
  -U, --upsertPredicate string       run in upsertPredicate mode. the value would be used to store blank nodes as an xid
  -C, --use_compression              Enable compression on connection to alpha server
      --vault string                 Vault options
                                         acl-field=; Vault field containing ACL key.
                                         acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                         addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                         enc-field=; Vault field containing encryption key.
                                         enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                         path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                         role-id-file=; Vault RoleID file, used for AppRole authentication.
                                         secret-id-file=; Vault SecretID file, used for AppRole authentication.
                                      (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")
      --verbose                      Run the live loader in verbose mode
  -x, --xidmap string                Directory to store xid to uid mapping
  -z, --zero string                  Dgraph zero gRPC server address (default "127.0.0.1:5080")

Use "dgraph live [command] --help" for more information about a command.
```


#### `dgraph restore`

This command loads objects from available backups. The following replicates the
help listing shown when you run `dgraph restore --help`:

```shell
Restore loads objects created with the backup feature in Dgraph Enterprise Edition (EE).

Backups are originated from HTTP at /admin/backup, then can be restored using CLI restore
command. Restore is intended to be used with new Dgraph clusters in offline state.

The --location flag indicates a source URI with Dgraph backup objects. This URI supports all
the schemes used for backup.

Source URI formats:
  [scheme]://[host]/[path]?[args]
  [scheme]:///[path]?[args]
  /[path]?[args] (only for local or NFS)

Source URI parts:
  scheme - service handler, one of: "s3", "minio", "file"
    host - remote address. ex: "dgraph.s3.amazonaws.com"
    path - directory, bucket or container at target. ex: "/dgraph/backups/"
    args - specific arguments that are ok to appear in logs.

The --posting flag sets the posting list parent dir to store the loaded backup files.

Using the --zero flag will use a Dgraph Zero address to update the start timestamp using
the restored version. Otherwise, the timestamp must be manually updated through Zero's HTTP
'assign' command.

Dgraph backup creates a unique backup object for each node group, and restore will create
a posting directory 'p' matching the backup group ID. Such that a backup file
named '.../r32-g2.backup' will be loaded to posting dir 'p2'.

Usage examples:

# Restore from local dir or NFS mount:
$ dgraph restore -p . -l /var/backups/dgraph

# Restore from S3:
$ dgraph restore -p /var/db/dgraph -l s3://s3.us-west-2.amazonaws.com/srfrog/dgraph

# Restore from dir and update Ts:
$ dgraph restore -p . -l /var/backups/dgraph -z localhost:5080

		 
Usage:
  dgraph restore [flags] 

Flags:
      --backup_id string    The ID of the backup series to restore. If empty, it will restore the latest series.
  -b, --badger string       Badger options
                                compression=snappy; Specifies the compression algorithm and compression level (if applicable) for the postings directory. "none" would disable compression, while "zstd:1" would set zstd compression at level 1.
                                goroutines=; The number of goroutines to use in badger.Stream.
                             (default "compression=snappy; numgoroutines=8;")
      --encryption string   [Enterprise Feature] Encryption At Rest options
                                key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                             (default "key-file=;")
      --force_zero          If false, no connection to a zero in the cluster will be required. Keep in mind this requires you to manually update the timestamp and max uid when you start the cluster. The correct values are printed near the end of this command's output. (default true)
  -h, --help                help for restore
  -l, --location string     Sets the source location URI (required).
  -p, --postings string     Directory where posting lists are stored (required).
      --tls string          TLS Client options
                                ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                client-cert=; (Optional) The Cert file provided by the client to the server.
                                client-key=; (Optional) The private Key file provided by the clients to the server.
                                internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                server-name=; Used to verify the server hostname.
                                use-system-ca=true; Includes System CA into CA Certs.
                             (default "use-system-ca=true; internal-port=false;")
      --vault string        Vault options
                                acl-field=; Vault field containing ACL key.
                                acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                enc-field=; Vault field containing encryption key.
                                enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                role-id-file=; Vault RoleID file, used for AppRole authentication.
                                secret-id-file=; Vault SecretID file, used for AppRole authentication.
                             (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")
  -z, --zero string         gRPC address for Dgraph zero. ex: localhost:5080

Use "dgraph restore [command] --help" for more information about a command.
```


### Dgraph security commands

Dgraph security commands let you manage access control lists (ACLs), manage
certificates, and audit database usage.

#### `dgraph acl`

This command runs the Dgraph Enterprise Edition ACL tool. The following replicates
the help listing shown when you run `dgraph acl --help`:

```shell
Run the Dgraph Enterprise Edition ACL tool 
Usage:
 dgraph acl [command] 

Available Commands: 
 add         Run Dgraph acl tool to add a user or group
 del         Run Dgraph acl tool to delete a user or group
 info        Show info about a user or group
 mod         Run Dgraph acl tool to modify a user's password, a user's group list, or agroup's predicate permissions

Flags:
 -a, --alpha string            Dgraph Alpha gRPC server address (default "127.0.0.1:9080")
     --guardian-creds string   Login credentials for the guardian
                                 user defines the username to login.
                                 password defines the password of the user.
                                 namespace defines the namespace to log into.
                                 Sample flag could look like --guardian-creds user=username;password=mypass;namespace=2
 -h, --help                    help for acl
     --tls string              TLS Client options
                                   ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                   client-cert=; (Optional) The Cert file provided by the client to the server.
                                   client-key=; (Optional) The private Key file provided by the clients to the server.
                                   internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                   server-name=; Used to verify the server hostname.
                                   use-system-ca=true; Includes System CA into CA Certs.
                                (default "use-system-ca=true; internal-port=false;")

Use "dgraph acl [command] --help" for more information about a command.
```

#### `dgraph audit`

This command decrypts audit files. These files are created using the `--audit`
when you run the `dgraph alpha` command. The following replicates the help listing
shown when you run `dgraph audit --help`:

```shell
Dgraph audit tool 
Usage:
 dgraph audit [command] 

Available Commands: 
 decrypt     Run Dgraph Audit tool to decrypt audit files

Flags:
 -h, --help   help for audit

Use "dgraph audit [command] --help" for more information about a command.
```

#### `dgraph cert`

This command lets you manage [TLS certificates]({{< relref "deploy/tls-configuration.md" >}}).
The following replicates the help listing shown when you run `dgraph cert --help`:

```shell
Dgraph TLS certificate management 
Usage:
 dgraph cert [flags]
 dgraph cert [command] 

Available Commands: 
 ls          lists certificates and keys

Flags:
 -k, --ca-key string           path to the CA private key (default "ca.key")
 -c, --client string           create cert/key pair for a client name
 -d, --dir string              directory containing TLS certs and keys (default "tls")
     --duration int            duration of cert validity in days (default 365)
 -e, --elliptic-curve string   ECDSA curve for private key. Values are: "P224", "P256", "P384", "P521".
     --force                   overwrite any existing key and cert
 -h, --help                    help for cert
 -r, --keysize int             RSA key bit size for creating new keys (default 2048)
 -n, --nodes strings           creates cert/key pair for nodes
     --verify                  verify certs against root CA when creating (default true)

Use "dgraph cert [command] --help" for more information about a command.
```

### Dgraph debug commands

Dgraph debug commands provide support for debugging issues with Dgraph deployments.
To learn more, see [Using the Debug Tool]({{< relref "howto/using-debug-tool.md" >}}).

#### `dgraph debug`

This command is used to debug issues with a Dgraph database instance. The
following replicates the help listing shown when you run `dgraph debug --help`:

```shell
 Debug Dgraph instance 
Usage:
  dgraph debug [flags] 

Flags:
      --at uint             Set read timestamp for all txns. (default 18446744073709551615)
      --encryption string   [Enterprise Feature] Encryption At Rest options
                                key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                             (default "key-file=;")
  -h, --help                help for debug
      --histogram           Show a histogram of the key and value sizes.
  -y, --history             Show all versions of a key.
      --item                Output item meta as well. Set to false for diffs. (default true)
      --jepsen string       Disect Jepsen output. Can be linear/binary.
  -l, --lookup string       Hex of key to lookup.
      --nokeys              Ignore key_. Only consider amount when calculating total.
  -p, --postings string     Directory where posting lists are stored.
  -r, --pred string         Only output specified predicate.
      --prefix string       Uses a hex prefix.
  -o, --readonly            Open in read only mode. (default true)
      --rollup string       Hex of key to rollup.
  -s, --snap string         Set snapshot term,index,readts to this. Value must be comma-separated list containing the value for these vars in that order.
  -t, --truncate uint       Remove data from Raft entries until but not including this index.
      --vals                Output values along with keys.
      --vault string        Vault options
                                acl-field=; Vault field containing ACL key.
                                acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                enc-field=; Vault field containing encryption key.
                                enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                role-id-file=; Vault RoleID file, used for AppRole authentication.
                                secret-id-file=; Vault SecretID file, used for AppRole authentication.
                             (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")
  -w, --wal string          Directory where Raft write-ahead logs are stored.

Use "dgraph debug [command] --help" for more information about a command.
```

#### `dgraph debuginfo`

This command generates information about the current node that is useful for debugging. 
The following replicates the help listing shown when you run `dgraph debuginfo --help`:

```shell
Generate debug information on the current node 
Usage:
 dgraph debuginfo [flags] 

Flags:
 -a, --alpha string       Address of running dgraph alpha. (default "localhost:8080")
 -x, --archive            Whether to archive the generated report (default true)
 -d, --directory string   Directory to write the debug info into.
 -h, --help               help for debuginfo
 -p, --profiles strings   List of pprof profiles to dump in the report. (default [goroutine,heap,threadcreate,block,mutex,profile,trace])
 -s, --seconds uint32     Duration for time-based profile collection. (default 15)
 -z, --zero string        Address of running dgraph zero.

Use "dgraph debuginfo [command] --help" for more information about a command.
```

### Dgraph tools commands

Dgraph tools provide a variety of tools to make it easier for you to deploy and
manage Dgraph.

#### `dgraph completion`

This command generates shell completion scripts for `bash` and `zsh` CLIs. The
following replicates the help listing shown when you run `dgraph completion --help`:

```shell
Generates shell completion scripts for bash or zsh 
Usage:
 dgraph completion [command] 

Available Commands: 
 bash        bash shell completion
 zsh         zsh shell completion

Flags:
 -h, --help   help for completion

Use "dgraph completion [command] --help" for more information about a command.
```

#### `dgraph conv`

This command runs the Dgraph geographic file converter, which converts geographic
files into RDF so that they can be consumed by Dgraph. The following replicates
the help listing shown when you run `dgraph conv --help`:

```shell
Dgraph Geo file converter 
Usage:
 dgraph conv [flags] 

Flags:
     --geo string       Location of geo file to convert
     --geopred string   Predicate to use to store geometries (default "loc")
 -h, --help             help for conv
     --out string       Location of output rdf.gz file (default "output.rdf.gz")

Use "dgraph conv [command] --help" for more information about a command.
```

#### `dgraph decrypt`

This command lets you decrypt an export file created by an encrypted Dgraph
cluster. The following replicates the help listing shown when you run
`dgraph decrypt --help`:

```shell
 A tool to decrypt an export file created by an encrypted Dgraph cluster 
Usage:
  dgraph decrypt [flags] 

Flags:
      --encryption string   [Enterprise Feature] Encryption At Rest options
                                key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                             (default "key-file=;")
  -f, --file string         Path to file to decrypt.
  -h, --help                help for decrypt
  -o, --out string          Path to the decrypted file.
      --vault string        Vault options
                                acl-field=; Vault field containing ACL key.
                                acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                enc-field=; Vault field containing encryption key.
                                enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                role-id-file=; Vault RoleID file, used for AppRole authentication.
                                secret-id-file=; Vault SecretID file, used for AppRole authentication.
                             (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")

Use "dgraph decrypt [command] --help" for more information about a command.
```

#### `dgraph export_backup`

This command is used to convert a [binary backup]({{< relref "enterprise-features/binary-backups.md" >}})
created using Dgraph Enterprise Edition into an exported folder. The following
replicates key information from the help listing shown when you run `dgraph export_backup --help`:

```shell
 Export data inside single full or incremental backup 
Usage:
  dgraph export_backup [flags] 

Flags:
  -d, --destination string   The folder to which export the backups.
      --encryption string    [Enterprise Feature] Encryption At Rest options
                                 key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                              (default "key-file=;")
  -f, --format string        The format of the export output. Accepts a value of either rdf or json (default "rdf")
  -h, --help                 help for export_backup
  -l, --location string      Sets the location of the backup. Both file URIs and s3 are supported.
                             		This command will take care of all the full + incremental backups present in the location.
      --upgrade              If true, retrieve the CORS from DB and append at the end of GraphQL schema.
                             		It also deletes the deprecated types and predicates.
                             		Use this option when exporting a backup of 20.11 for loading onto 21.03.
      --vault string         Vault options
                                 acl-field=; Vault field containing ACL key.
                                 acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                 addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                 enc-field=; Vault field containing encryption key.
                                 enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                 path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                 role-id-file=; Vault RoleID file, used for AppRole authentication.
                                 secret-id-file=; Vault SecretID file, used for AppRole authentication.
                              (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")

Use "dgraph export_backup [command] --help" for more information about a command. 
```

#### `dgraph increment`

This command increments a counter transactionally, so that you can confirm that
an Alpha node is able to handle both query and mutation requests. To learn more,
see [Using the Increment Tool]({{< relref "howto/using-increment-tool.md" >}}). 
The following replicates the help listing shown when you run `dgraph increment --help`:

```shell
Increment a counter transactionally 
Usage:
 dgraph increment [flags] 

Flags:
     --alpha string    Address of Dgraph Alpha. (default "localhost:9080")
     --be              Best-effort. Read counter value without retrieving timestamp from Zero.
     --creds string    Various login credentials if login is required.
                         user defines the username to login.
                         password defines the password of the user.
                         namespace defines the namespace to log into.
                         Sample flag could look like --creds user=username;password=mypass;namespace=2
 -h, --help            help for increment
     --jaeger string   Send opencensus traces to Jaeger.
     --num int         How many times to run. (default 1)
     --pred string     Predicate to use for storing the counter. (default "counter.val")
     --retries int     How many times to retry setting up the connection. (default 10)
     --ro              Read-only. Read the counter value without updating it.
     --tls string      TLS Client options
                           ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                           client-cert=; (Optional) The Cert file provided by the client to the server.
                           client-key=; (Optional) The private Key file provided by the clients to the server.
                           internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                           server-name=; Used to verify the server hostname.
                           use-system-ca=true; Includes System CA into CA Certs.
                        (default "use-system-ca=true; internal-port=false;")
     --wait duration   How long to wait.

Use "dgraph increment [command] --help" for more information about a command.
```

#### `dgraph lsbackup`

This command lists information on backups in a given location for Dgraph Enterprise
Edition. To learn more, see [Backup List Tool]({{< relref "enterprise-features/lsbackup.md" >}}).
The following replicates the help listing shown when you run `dgraph lsbackup --help`:

```shell
List info on backups in a given location 
Usage:
 dgraph lsbackup [flags] 

Flags:
 -h, --help              help for lsbackup
 -l, --location string   Sets the source location URI (required).
     --verbose           Outputs additional info in backup list.

Use "dgraph lsbackup [command] --help" for more information about a command.
```

#### `dgraph migrate`

This command runs the Dgraph [migration tool]({{< relref "migration/migrate-tool.md" >}})
to move data from a MySQL database to Dgraph. The following replicates the help
listing shown when you run `dgraph migrate --help`:

```shell
Run the Dgraph migration tool from a MySQL database to Dgraph 
Usage:
 dgraph migrate [flags] 

Flags:
     --db string              The database to import
 -h, --help                   help for migrate
     --host string            The hostname or IP address of the database server. (default "localhost")
 -o, --output_data string     The data output file (default "sql.rdf")
 -s, --output_schema string   The schema output file (default "schema.txt")
     --password string        The password used for logging in
     --port string            The port of the database server. (default "3306")
 -q, --quiet                  Enable quiet mode to suppress the warning logs
 -p, --separator string       The separator for constructing predicate names (default ".")
     --tables string          The comma separated list of tables to import, an empty string means importing all tables in the database
     --user string            The user for logging in

Use "dgraph migrate [command] --help" for more information about a command.
```

#### `dgraph raftmigrate`

This command runs the Dgraph Raft migration tool.<!-- TBD need to say more about this --> 
The following replicates the help listing shown when you run `dgraph raftmigrate --help`:

```shell
Run the Raft migration tool 
Usage:
 dgraph raftmigrate [flags] 

Flags:
     --encryption_key_file string   The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively). Enterprise feature.
 -h, --help                         help for raftmigrate
     --new-dir string               Path to the new (z)w directory.
     --old-dir string               Path to the old (z)w directory.
     --vault string                 Vault options
                                        addr=http://localhost:8200; Vault server address in the form of http://ip:port
                                        field=enc_key; Vault kv store field whose value is the base64 encoded encryption key.
                                        format=base64; Vault field format: raw or base64.
                                        path=secret/data/dgraph; Vault kv store path. e.g. secret/data/dgraph for kv-v2, kv/dgraph for kv-v1.
                                        role-id-file=; File containing Vault role-id used for approle auth.
                                        secret-id-file=; File containing Vault secret-id used for approle auth.
                                     (default "addr=http://localhost:8200; path=secret/data/dgraph; field=enc_key; format=base64; role-id-file=; secret-id-file=;")

Use "dgraph raftmigrate [command] --help" for more information about a command.
```

#### `dgraph upgrade`

This command helps you to upgrade from an earlier Dgraph release to a newer release. 
The following replicates the help listing shown when you run `dgraph upgrade --help`:

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
