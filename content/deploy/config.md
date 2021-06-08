+++
date = "2017-03-20T22:25:17+11:00"
title = "Configuration"
description = "In this guide, we explain how to configure options in multiple ways, including: using command line flags, using environment variables, and using a configuration file."
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

Dgraph has *global flags* that apply to all subcommands and flags specific to a subcommand.

Some flags have been deprecated and replaced in release `v21.03`, and flags for several commands (`alpha`, `backup`, `bulk`,`debug`, `live`, and `zero`) now have superflags. Superflags are compound flags that contain
one or more options that let you define multiple settings in a semicolon-delimited
list. The general syntax for superflags is as follows: `--<flagname> option-a=value-a; option-b=value-b`.

The following example shows how to use superflags when running the `dgraph alpha` command.

```bash
dgraph alpha --my=alpha.example.com:7080 --zero=zero.example.com:5080 \
  --badger "compression=zstd:1" \
  --block_rate "10" \
  --trace "jaeger=http://jaeger:14268" \
  --tls "ca-cert=/dgraph/tls/ca.crt;client-auth-type=REQUIREANDVERIFY;server-cert=/dgraph/tls/node.crt;server-key=/dgraph/tls/node.key;use-system-ca=true;internal-port=true;client-cert=/dgraph/tls/client.dgraphuser.crt;client-key=/dgraph/tls/client.dgraphuser.key"
  --security "whitelist=10.0.0.0/8,172.0.0.0/8,192.168.0.0/16"
```

## Environment variables

The environment variable names for Dgraph mirror the flag names shown in the Dgraph CLI `--help` output. These environment variable names are formed the concatenation of `DGRAPH`, the subcommand invoked (`ALPHA`, `ZERO`, `LIVE`, or `BULK`), and then the name of the flag (in uppercase). For example, instead running a command like `dgraph alpha --block_rate 10`, you could set the following environment variable: `DGRAPH_ALPHA_BLOCK_RATE=10 dgraph alpha`.

So, the environment variable syntax for a superflag (`--<superflag-name> option-a=value; option-b=value`) is `<SUPERFLAG-NAME>="option-a=value;option-b=value"`.

The following is an example of environment variables for `dgraph alpha`:

```bash
DGRAPH_ALPHA_BADGER="compression=zstd:1"
DGRAPH_ALPHA_BLOCK_RATE="10"
DGRAPH_ALPHA_TRACE="jaeger=http://jaeger:14268"
DGRAPH_ALPHA_TLS="ca-cert=/dgraph/tls/ca.crt;client-auth-type=REQUIREANDVERIFY;server-cert=/dgraph/tls/node.crt;server-key=/dgraph/tls/node.key;use-system-ca=true;internal-port=true;client-cert=/dgraph/tls/client.dgraphuser.crt;client-key=/dgraph/tls/client.dgraphuser.key"
DGRAPH_ALPHA_SECURITY="whitelist=10.0.0.0/8,172.0.0.0/8,192.168.0.0/16"
```

## Configuration file

You can specify a configuration file using the Dgraph CLI with the `--config` flag (for example,
`dgraph alpha --config my_config.json`), or using an environment variable, (for example, `DGRAPH_ALPHA_CONFIG=my_config.json dgraph alpha`).

Dgraph supports configuration file formats that it detects based on file extensions ([`.json`](https://www.json.org/json-en.html), [`.yml`](https://yaml.org/) or [`.yaml`](https://yaml.org/)).  In these files, the name of the superflag is used as a key that points to a hash. The hash consists of `key: value` pairs that correspond to the superflag's list of `option=value` pairs.


{{% notice "note" %}}
The formats [`.toml`](https://toml.io/en/), [`.hcl`](https://github.com/hashicorp/hcl), and [`.properties`](https://en.wikipedia.org/wiki/.properties) are not supported in release `v21.03.0`.
{{% /notice %}}

{{% notice "tip" %}}
When representing the superflag options in the hash, you can use either *kebab-case* or *snake_case* for names of the keys.
{{% /notice %}}

### JSON config file

In JSON, you can represent a superflag and its options (`--<superflag-name>
option-a=value;option-b=value`) as follows:

```json
{
  "<superflag-name>": {
    "option-a": "value",
    "opton-b": "value"
  }
}
```

The following example JSON config file (`config.json`) using *kebab-case*:

```json
{
  "badger": { "compression": "zstd:1" },
  "trace": { "jaeger": "http://jaeger:14268" },
  "security": { "whitelist": "10.0.0.0/8,172.0.0.0/8,192.168.0.0/16" },
  "tls": {
    "ca-cert": "/dgraph/tls/ca.crt",
    "client-auth-type": "REQUIREANDVERIFY",
    "server-cert": "/dgraph/tls/node.crt",
    "server-key": "/dgraph/tls/node.key",
    "use-system-ca": true,
    "internal-port": true,
    "client-cert": "/dgraph/tls/client.dgraphuser.crt",
    "client-key": "/dgraph/tls/client.dgraphuser.key"
  }
}
```

The following example JSON config file (`config.json`) using *snake_case*:

```json
{
  "badger": { "compression": "zstd:1" },
  "trace": { "jaeger": "http://jaeger:14268" },
  "security": { "whitelist": "10.0.0.0/8,172.0.0.0/8,192.168.0.0/16" },
  "tls": {
    "ca_cert": "/dgraph/tls/ca.crt",
    "client_auth_type": "REQUIREANDVERIFY",
    "server_cert": "/dgraph/tls/node.crt",
    "server_key": "/dgraph/tls/node.key",
    "use_system_ca": true,
    "internal_port": true,
    "client_cert": "/dgraph/tls/client.dgraphuser.crt",
    "client_key": "/dgraph/tls/client.dgraphuser.key"
  }
}
```


### YAML config file

In YAML, you can represent a superflag and its options (`--<superflag-name>
option-a=value;option-b=value`) as follows:

```yaml
<superflag-name>:
 option-a: value
 opton-b: value
```

The following example YAML config file (`config.yml`) uses *kebab-case*:

```yaml
badger:
  compression: zstd:1
trace:
  jaeger: http://jaeger:14268
security:
  whitelist: 10.0.0.0/8,172.0.0.0/8,192.168.0.0/16
tls:
  ca-cert: /dgraph/tls/ca.crt
  client-auth-type: REQUIREANDVERIFY
  server-cert: /dgraph/tls/node.crt
  server-key: /dgraph/tls/node.key
  use-system-ca: true
  internal-port: true
  client-cert: /dgraph/tls/client.dgraphuser.crt
  client-key: /dgraph/tls/client.dgraphuser.key
```

The following example YAML config file (`config.yml`) uses *snake_case*:

```yaml
badger:
  compression: zstd:1
trace:
  jaeger: http://jaeger:14268
security:
  whitelist: 10.0.0.0/8,172.0.0.0/8,192.168.0.0/16
tls:
  ca_cert: /dgraph/tls/ca.crt
  client_auth_type: REQUIREANDVERIFY
  server_cert: /dgraph/tls/node.crt
  server_key: /dgraph/tls/node.key
  use_system_ca: true
  internal_port: true
  client_cert: /dgraph/tls/client.dgraphuser.crt
  client_key: /dgraph/tls/client.dgraphuser.key
```
