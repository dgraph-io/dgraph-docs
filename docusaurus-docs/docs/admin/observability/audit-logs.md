---
title: Audit Logging
description: Track and audit all requests (queries and mutations) with Dgraph audit logging.
---

:::note
**Enterprise Feature**: Audit logging requires a Dgraph Enterprise license. See [License](/dgraph-overview/admin/enterprise-features/license) for details.
:::

Audit logging tracks all requests (queries and mutations) sent to your Dgraph cluster. When enabled, audit logs record the following information for each request:

* **Endpoint** - The API endpoint used for the request
* **User Name** - The logged-in user (if ACL is enabled)
* **Server address** - The Dgraph server host address
* **Client address** - The client host address
* **Request Body** - The request payload (truncated at 4KB)
* **Timestamp** - When the request was received
* **Namespace** - The namespace ID (for multi-tenant clusters)
* **Query Parameters** - Any query parameters provided
* **Response status** - The HTTP/gRPC response status

## Audit Log Scope

Audit logging captures most queries and mutations sent to Dgraph Alpha and Dgraph Zero nodes.

### Logged Requests

* HTTP requests sent to Dgraph Zero's port 6080 and Dgraph Alpha's port 8080 (except health/monitoring endpoints)
* gRPC requests sent to Dgraph Zero's port 5080 and Dgraph Alpha's port 9080 (except internal cluster endpoints)

### Excluded Requests

The following requests are not logged:

* Response payloads (only requests are logged)
* HTTP requests to `/health`, `/state`, and `/jemalloc` endpoints
* gRPC requests to Raft endpoints (internal cluster consensus)
* gRPC requests to health check endpoints (`Check` and `Watch`)
* gRPC requests to Dgraph Zero stream endpoints (`StreamMembership`, `UpdateMembership`, `Oracle`, `Timestamps`, `ShouldServe`, `Connect`)

## Audit Log Files

Audit logs are written in JSON format. Dgraph uses a rolling-file policy:

* The current log file is used until it reaches a configurable size (default: 100MB)
* When the size limit is reached, Dgraph creates a new current log file
* Older audit log files are retained for a configurable number of days (default: 10 days)


### Example Audit Log Entry

For this GraphQL query:

```graphql
{
  q(func: has(actor.film)){
    count(uid)
  }
}
```

The corresponding audit log entry is:

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

## Configuration

Enable audit logging on Dgraph Alpha or Dgraph Zero nodes using the `--audit` flag with semicolon-separated options.

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `output=<path>` | Directory path for storing audit logs | Required |
| `size=<MB>` | Maximum size per log file in MB | 100 |
| `days=<N>` | Number of days to retain log files | 10 |
| `compress=true` | Enable compression for older log files | false |
| `encrypt-file=<path>` | Path to encryption key file for log encryption | disabled |

### Enable Audit Logging

The simplest configuration specifies only the output directory:

```bash
dgraph alpha --audit output=audit-log-dir
```

### Customize Log File Size and Retention

Configure larger log files and extended retention:

```bash
dgraph alpha --audit "output=audit-log-dir;size=200;days=15"
```

This sets log files to 200 MB and retains them for 15 days.

### Enable Compression

Compress older audit logs to reduce storage space:

```bash
dgraph alpha --audit "output=audit-log-dir;compress=true"
```

### Enable Encryption

Encrypt audit logs to protect sensitive information in logged requests:

```bash
dgraph alpha --audit "output=audit-log-dir;compress=true;encrypt-file=/path/to/encrypt/key/file"
```

### Decrypt Audit Logs

Decrypt encrypted audit logs using the `dgraph audit decrypt` command:

```bash
dgraph audit decrypt \
  --encryption_key_file=/path/encrypt/key/file \
  --in /path/to/encrypted/log/file \
  --out /path/to/output/file
```

## Related Documentation

For general logging and log format information, see [Log Format](/dgraph-overview/admin/observability/log-format).
