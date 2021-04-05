+++
date = "2017-03-20T22:25:17+11:00"
title = "Audit Logging"
description = "With an Enterprise license, Dgraph can generate audit logs that let you track and audit all requests (queries and mutations)."
weight = 2
[menu.main]
    parent = "enterprise-features"
+++

As a database administrator, you count on being able to audit access to your
database. With a Dgraph 
[enterprise license]({{< relref "enterprise-features/license.md" >}}), you can
enable audit logging so that all requests are tracked and available for use in
security audits. When audit logging is enabled, the following information is
recorded about the queries and mutations (requests) sent to your database:

* Endpoint
* Logged-in User Name
* Server host address
* Client Host address
* Request Body (truncated at 4KB)
* Timestamp
* Namespace
* Query Parameters (if provided)
* Response status

## Audit log scope

Most queries and mutations sent to Dgraph Alpha and Dgraph Zero are logged.
Specifically, the following are logged:

* HTTP requests sent over Dgraph Zero's 6080 port and Dgraph Alpha's 8080 port (except as noted below)
* GRPC requests sent over Dgraph Zero's 5080 port and Dgraph Alpha's 9080 port (except the Raft, health and Dgraph Zero stream endpoints noted below)

The following are not logged:

* Responses to queries and mutations
* HTTP requests to `/health`, `/state` and `/jemalloc` endpoints
* GRPC requests to Raft endpoints (see [RAFT]({{< relref "design-concepts/raft.md" >}}))
* GRPC requests to health endpoints (`Check` and `Watch`)
* GRPC requests to Dgraph Zero stream endpoints (`StreamMembership`, `UpdateMembership`, `Oracle`, `Timestamps`, `ShouldServe` and `Connect`)
<!-- We don't have any docs to link to for the endpoints described in the last two bullets. TBD fix this so we are't referencing something not described elsewhere -->

## Audit log files

All audit logs are in JSON format. Dgraph has a "rolling-file" policy for audit
logs, where the current log file is used until it reaches a configurable size
(default: 100MB), and then is replaced by another current audit log file. Older
audit log files are retained for a configurable number of days (default: 10 days).


For example, by sending this query:

```graphql
{
  q(func: has(actor.film)){
    count(uid)
  }
}
```

You'll get the following JSON audit log entry:

```json
{
   "ts":"2021-03-22T15:03:19.165Z",
   "endpoint":"/query",
   "level":"AUDIT",
   "user":"",
   "namespace":0,
   "server":"localhost:7080",
   "client":"[::1]:60118",
   "req_type":"Http",
   "req_body":"{\"query\":\"{\\n  q(func: has(actor.film)){\\n    count(uid)\\n  }\\n}\",\"variables\":{}}",
   "query_param":{
      "timeout":[
         "20s"
      ]
   },
   "status":"OK"
}
```

## Enable audit logging

You can enable audit logging on a Dgraph Alpha or Dgraph Zero node by using the
`--audit` flag to specify semicolon-separated options for audit logging. When
you enable audit logging, a few options are available for you to configure:

* `compress=true` tells Dgraph to use compression on older audit log files
* `days=20` tells Dgraph to retain older audit logs for 20 days, rather than the
default of 10 days
* `output=/path/to/audit/logs` tells Dgraph which path to use for storing audit logs
* `encrypt-file=/encryption/key/path` tells Dgraph to encrypt older log files
 with the specified key
* `size=200` tells Dgraph to store audit logs in 200 MB files,  rather than the
default of 100 MB files

You can see how to use these options in the example commands below.

## Example commands

The commands in this section show you how to enable and configure audit logging.

### Enable audit logging

In the simplest scenario, you can enable audit logging by simply specifying the 
directory to store audit logs on a Dgraph Alpha node:

```bash
dgraph alpha --audit output=audit-log-dir
```

You could extend this command a bit to specify larger log files (200 MB, instead
of 100 MB) and retain them for longer (15 days instead of 10 days):

```bash
dgraph alpha --audit output=audit-log-dir;size=200;days=15
```

### Enable audit logging with compression

In many cases you will want to compress older audit logs to save storage space.
You can do this with a command like the following:

```bash
dgraph alpha --audit output=audit-log-dir;compress=true
```

### Enable audit logging with encryption

You can also enable encryption of audit logs to protect sensitive information that
might exist in logged requests. You can do this, along with compression, with a
command like the following:

```bash
dgraph alpha --audit output=audit-log-dir;compress=true;encrypt-file=/path/to/encrypt/key/file
```

### Decrypt audit logs

To decrypt encrypted audit logs, you can use the `dgraph audit decrypt` command,
as follows:

```bash
dgraph audit decrypt --encryption key-file=/path/encrypt/key/file --in /path/to/encrypted/log/file --out /path/to/output/file
```

## Next steps

To learn more about the logging features of Dgraph, see [Logging]({{< relref "deploy/log-format.md" >}}).