+++
date = "2017-03-20T22:25:17+11:00"
title = "Config"
weight = 3
[menu.main]
    parent = "deploy"
+++

{{% notice "tip" %}}
For a single server setup, recommended for new users, please see [Get Started]({{< relref "get-started/index.md" >}}) page.
{{% /notice %}}

You can see the list of available subcommands with `dgraph --help`.  You can view the full set of configuration options for a given subcommand with `dgraph <subcommand> --help` (for example, `dgraph zero --help`).

You can configure options in multiple ways, which are listed below from highest precedence to lowest precedence:


- Using command line flags (as described in the help output).
- Using environment variables.
- Using a configuration file.

If no configuration for an option is used, then the default value as described
in the `--help` output applies.

You can use multiple configuration methods at the same time, so a core
set of options could be set in a config file, and instance specific options
could be set using environment vars or flags.

## Command line flags

Dgraph has *global flags* that apply to all subcommands and flags specific to a subcommand. Below is an example of using command line flags with `dgraph alpha`.

```bash
dgraph alpha --my=alpha.example.com:7080 --zero=zero.example.com:5080 \
  --badger.compression "zstd:1" \
  --block_rate "10" \
  --jaeger.collector "http://jaeger:14268" \
  --tls_cacert "/dgraph/tls/node.crt" \
  --tls_cert "/dgraph/tls/client.dgraphuser.crt" \
  --tls_client_auth "REQUIREANDVERIFY" \
  --tls_internal_port_enabled \
  --tls_key "/dgraph/tls/client.dgraphuser.key" \
  --tls_node_cert "/dgraph/tls/node.crt" \
  --tls_node_key "/dgraph/tls/node.key" \
  --tls_use_system_ca \
  --whitelist "10.0.0.0/8,172.0.0.0/8,192.168.0.0/16"
```

## Environment variables

The environment variable names mirror the flag names as seen in the `--help`
output. They are the concatenation of `DGRAPH`, the subcommand invoked
(`ALPHA`, `ZERO`, `LIVE`, or `BULK`), and then the name of the flag (in
uppercase). For example, instead of using `dgraph alpha --block_rate 10`, you
could use `DGRAPH_ALPHA_BLOCK_RATE=10 dgraph alpha`.

{{% notice "tip" %}}
For command line flags with the dot `.` notation, you can use underscore `_` in the environment variable name.  Thus `dgraph zero --jaeger.collector` becomes `DGRAPH_ZERO_JAEGER_COLLECTOR`.
{{% /notice %}}

Below is an example of environment variables for `dgraph alpha`:

```bash
DGRAPH_ALPHA_BADGER_COMPRESSION="zstd:1"
DGRAPH_ALPHA_BLOCK_RATE="10"
DGRAPH_ALPHA_CLIENT_AUTH="VERIFYIFGIVEN"
DGRAPH_ALPHA_JAEGER_COLLECTOR="http://jaeger:14268"
DGRAPH_ALPHA_TLS_CACERT="/dgraph/tls/ca.crt"
DGRAPH_ALPHA_TLS_CERT="/dgraph/tls/client.dgraphuser.crt"
DGRAPH_ALPHA_TLS_INTERNAL_PORT_ENABLED="true"
DGRAPH_ALPHA_TLS_KEY="/dgraph/tls/client.dgraphuser.key"
DGRAPH_ALPHA_TLS_NODE_CERT="/dgraph/tls/node.crt"
DGRAPH_ALPHA_TLS_NODE_KEY="/dgraph/tls/node.key"
DGRAPH_ALPHA_TLS_USE_SYSTEM_CA="true"
DGRAPH_ALPHA_WHITELIST="10.0.0.0/8,172.0.0.0/8,192.168.0.0/16"
```

## Configuration file

A configuration file can be specified using the `--config` flag, or an environment variable, such as `dgraph alpha --config my_config.json` or `DGRAPH_ALPHA_CONFIG=my_config.json dgraph alpha`.

The config consists of a set of key/value pairs, where the keys mirror the flag names.

Dgraph supports several configuration file formats that it detects based on file extensions ([`.json`](https://www.json.org/json-en.html), [`.toml`](https://toml.io/en/), [`.yml`](https://yaml.org/) or [`.yaml`](https://yaml.org/), [`.hcl`](https://github.com/hashicorp/hcl), and [`.properties`](https://en.wikipedia.org/wiki/.properties)).

{{% notice "tip" %}}
For command-line flags with the dot (`.`) notation, you can use the full name as the key (such as `jaeger.collector`), or represent them hierarchically where the key (`jaeger`) points to a hash. For flags in snake case or using underscore (`_`) notation (such as `tls_cacert`), you cannot represent them hierarchically.  See language-specific examples below for further information.
{{% /notice %}}

### JSON config file

Example JSON config file (`config.json`):

```json
{
  "block_rate": 10,
  "badger": {
    "compression": "zstd:1",
  },
  "jaeger": {
    "collector": "http://jaeger:14268",
  },
  "tls_cacert": "/dgraph/tls/node.crt",
  "tls_cert": "/dgraph/tls/client.dgraphuser.crt",
  "tls_client_auth": "REQUIREANDVERIFY",
  "tls_internal_port_enabled": true,
  "tls_key": "/dgraph/tls/client.dgraphuser.key",
  "tls_node_cert": "/dgraph/tls/node.crt",
  "tls_node_key": "/dgraph/tls/node.key",
  "tls_use_system_ca": true,
  "whitelist": "10.0.0.0/8,172.0.0.0/8,192.168.0.0/16"
}
```

### TOML config file


Example TOML config file (`config.toml`):

```toml
block_rate = 10
tls_cacert = '/dgraph/tls/node.crt'
tls_cert = '/dgraph/tls/client.dgraphuser.crt'
tls_client_auth = 'REQUIREANDVERIFY'
tls_internal_port_enabled = true
tls_key = '/dgraph/tls/client.dgraphuser.key'
tls_node_cert = '/dgraph/tls/node.crt'
tls_node_key = '/dgraph/tls/node.key'
tls_use_system_ca = true
whitelist = '10.0.0.0/8,172.0.0.0/8,192.168.0.0/16'

[badger]
compression = 'zstd:1'

[jaeger]
collector = 'http://jaeger:14268'
```

### YAML config file

Example YAML config file (`config.yml`):

```yaml
badger:
  compression: zstd:1
block_rate: 10
jaeger:
  collector: http://jaeger:14268
tls_cacert: /dgraph/tls/node.crt
tls_cert: /dgraph/tls/client.dgraphuser.crt
tls_client_auth: REQUIREANDVERIFY
tls_internal_port_enabled: true
tls_key: /dgraph/tls/client.dgraphuser.key
tls_node_cert: /dgraph/tls/node.crt
tls_node_key: /dgraph/tls/node.key
tls_use_system_ca: true
whitelist: 10.0.0.0/8,172.0.0.0/8,192.168.0.0/16
```

### HCL config file

Example HCL config file (`config.hcl`):

{{% notice "note" %}}
Though that HCL language itself supports hierarchical key to hash, this currently does not work.  Instead you will have to use the full flag name with the dot `.` included.
{{% /notice %}}

```hcl
badger.compression        = "zstd:1"
block_rate                = 10
jaeger.collector          = "http://jaeger:14268"
tls_cacert                = "/dgraph/tls/node.crt"
tls_cert                  = "/dgraph/tls/client.dgraphuser.crt"
tls_client_auth           = "REQUIREANDVERIFY"
tls_internal_port_enabled = true
tls_key                   = "/dgraph/tls/client.dgraphuser.key"
tls_node_cert             = "/dgraph/tls/node.crt"
tls_node_key              = "/dgraph/tls/node.key"
tls_use_system_ca         = true
whitelist                 = "10.0.0.0/8,172.0.0.0/8,192.168.0.0/16"
```

### Java properties config file

Example Java properties config file (`config.properties`):

```properties
badger.compression=zstd:1
block_rate=10
jaeger.collector=http://jaeger:14268
tls_cacert=/dgraph/tls/node.crt
tls_cert=/dgraph/tls/client.dgraphuser.crt
tls_client_auth=REQUIREANDVERIFY
tls_internal_port_enabled=true
tls_key=/dgraph/tls/client.dgraphuser.key
tls_node_cert=/dgraph/tls/node.crt
tls_node_key=/dgraph/tls/node.key
tls_use_system_ca=true
whitelist=10.0.0.0/8,172.0.0.0/8,192.168.0.0/16
```
