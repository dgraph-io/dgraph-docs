---
title: dgraph live
---

#### `dgraph live`

This command is used to load live data with the Dgraph [Live Loader](../migration/live-loader) tool.
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


