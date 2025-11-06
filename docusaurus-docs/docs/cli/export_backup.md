---
title: dgraph export_backup
---

#### `dgraph export_backup`

This command is used to convert a [binary backup](/dgraph-overview/admin/enterprise-features/binary-backups)
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


