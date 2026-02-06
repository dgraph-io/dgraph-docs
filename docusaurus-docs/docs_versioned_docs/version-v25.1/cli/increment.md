---
title: dgraph increment
---

This command increments a counter transactionally, so that you can confirm that
an Alpha node is able to handle both query and mutation requests. To learn more,
see [Using the Increment Tool](/learn/howto/using-increment-tool).
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