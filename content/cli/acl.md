+++
title = "dgraph acl"
weight = 3
type = "docs"
[menu.main]
    parent = "cli"
+++

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

