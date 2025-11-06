---
title: Dgraph CLI Reference
---

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

This command lets you manage [TLS certificates](/dgraph-overview/admin/security/tls-configuration).
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

