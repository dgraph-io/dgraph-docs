+++
title = "dgraph restore"
weight = 3
type = "docs"
[menu.main]
    parent = "cli"
+++

#### `dgraph restore`

This command loads objects from available backups. The following replicates the
help listing shown when you run `dgraph restore --help`:

```shell
Restore loads objects created with the backup feature in Dgraph Enterprise Edition (EE).

Backups taken using the GraphQL API can be restored using CLI restore
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

