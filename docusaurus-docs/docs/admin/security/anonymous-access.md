---
title: Anonymous Access
description: Use the --security anonymous option to decide what a caller with no verified credential can do on Dgraph Alpha and Zero.
---

:::info Unreleased feature
The `anonymous` option of the `--security` superflag is not yet part of a released version of Dgraph. This page describes the behavior that ships with it. On a release that predates it, Dgraph Alpha and Dgraph Zero refuse to start if you set it. See [Upgrades and mixed versions](#upgrades-and-mixed-versions).
:::

The `anonymous` option of the `--security` superflag sets what a caller with no verified credential can do. You choose one of three postures: `full`, `data`, or `none`. The default is `full`, which keeps the behavior of every earlier release.

```sh
# Anonymous callers can query and mutate, but cannot administer the cluster
dgraph alpha --security "token=<authtokenstring>; anonymous=data"
```

This page is a reference and an explanation. It covers why the option exists, exactly what each posture allows, how a caller becomes identified, and how to move a running cluster to a closed posture.

## Why this option exists

Three settings protect the privileged operations on Dgraph Alpha:

| Setting | Question it answers | Behavior when you leave it unset |
|---------|--------------------|----------------------------------|
| `--security "whitelist=..."` | Where did the request come from? | Only loopback callers pass. Every other address is rejected. |
| `--security "token=..."` | Does the caller know the shared secret? | No token is required from anyone. |
| `--acl "secret-file=..."` | Which user is this, and what may they do? | Guardian checks succeed for everyone. |

Each setting passes when its own feature is unconfigured. The protection you get is whatever you configured, rather than the combination of all three.

The default is safe because the empty whitelist admits loopback only. The risk appears when you widen the whitelist. The whitelist checks the network location of a request and carries no credential. If you set `whitelist=0.0.0.0/0` and configure neither a token nor ACL, then any caller that can reach the port can back up, restore, export, or shut down your cluster without presenting any credential at all.

The `anonymous` option makes that decision explicit. It answers a fourth question: what may a caller do when nothing has identified them?

:::tip
`whitelist=0.0.0.0/0` is common in containers and quickstart setups, because the Docker host reaches a published port from a non-loopback address. If you run Dgraph that way, read [Choose a posture](#choose-a-posture).
:::

## Postures

| Posture | Anonymous callers can | Anonymous callers cannot | When to use it |
|---------|----------------------|--------------------------|----------------|
| `full` (default) | Do whatever the whitelist, token, and ACL settings allow. | Nothing changes from earlier releases. | Existing clusters, and clusters that rely on network isolation alone. |
| `data` | Run queries, mutations, and commits. Log in. Read `/health`. | Perform any administrative operation, no matter what the whitelist allows. | Clusters that serve application traffic without credentials but must protect the control plane. |
| `none` | Log in, call `CheckVersion`, and read the health and readiness endpoints. | Run queries, mutations, or commits, or perform any administrative operation. | Clusters where every client authenticates. |

The value is not case-sensitive. Alpha and Zero refuse to start on any other value:

```text
--security "anonymous=closed" is not a valid value; it must be one of full, data, or none
```

## What counts as an identified caller

A request is identified when it presents a credential that Dgraph verifies. A request that presents no credential, or one that fails verification, is anonymous.

| Credential | How to send it over HTTP | How to send it over gRPC | Identifies the caller when |
|------------|--------------------------|--------------------------|----------------------------|
| ACL access JWT | `X-Dgraph-AccessToken` header | `accessJwt` metadata key | ACL is enabled and the JWT is valid and unexpired |
| `--security` auth token | `X-Dgraph-AuthToken` header | `auth-token` metadata key | A token is configured and the value matches it |

A few rules follow from this table:

* **A token identifies a caller only when you configure one.** If you set `anonymous=data` without a token or ACL, no request can ever be identified, so no one can administer the cluster. Dgraph logs a warning at startup when it detects this. See [Startup warnings](#startup-warnings).
* **The source IP never identifies a caller.** Loopback and whitelisted addresses count as anonymous under `data` and `none`.
* **When a request carries both credentials, the ACL user wins.** The ACL JWT identifies a person, while the token identifies a client service.
* **An identity does not bypass the other settings.** The posture decides whether an anonymous caller is turned away. It does not grant anything. An identified caller still has to pass the whitelist, token, and ACL checks that applied before.

:::note
With ACL enabled, a caller who presents only the `--security` token is identified, but ACL rules still decide what they may do. The token does not grant administrative authority on an ACL cluster. Use the credentials of a Guardian user for administration.
:::

## What each posture allows

This table lists the operations the posture affects. "Unchanged" means the operation follows the whitelist, token, and ACL rules exactly as it did before the `anonymous` option existed.

### Data operations

| Operation | HTTP | gRPC | `full` | `data` | `none` |
|-----------|------|------|--------|--------|--------|
| Query | `/query` | `Query`, `RunDQL` | Unchanged | Unchanged | Requires identity |
| Mutation | `/mutate` | `Query` with mutations, `RunDQL` | Unchanged | Unchanged | Requires identity |
| Commit or abort | `/commit` | `CommitOrAbort` | Unchanged | Unchanged | Requires identity |
| GraphQL queries and mutations | `/graphql` | | Unchanged | Unchanged | Requires identity |
| Schema change (no drop) | `/alter` | `Alter` | Unchanged | Unchanged | Unchanged |

Schema changes keep their existing rule under every posture. `/alter` has always required a whitelisted address and, when one is configured, the token.

### Administrative operations

Every operation in this table requires an identified caller under `data` and `none`.

| Operation | Where | `full` |
|-----------|-------|--------|
| Drop all data | `/alter` with `drop_all`, gRPC `Alter` | Unchanged |
| Create, drop, or list namespaces | gRPC `CreateNamespace`, `DropNamespace`, `ListNamespaces`; `/admin` `addNamespace`, `deleteNamespace` | Unchanged |
| Lease UIDs | gRPC `AllocateIDs` | Unchanged |
| Act in another namespace | Galaxy-wide loads, such as `dgraph live --force-namespace` | Unchanged |
| Read cluster state | `/state`, `/health?all`, `/admin` `state` | Unchanged |
| Backups | `/admin` `backup`, `restore`, `restoreTenant`, `listBackups` | Unchanged |
| Exports | `/admin` `export` | Unchanged |
| Cluster control | `/admin` `shutdown`, `draining`, `removeNode`, `moveTablet`, `assign`, `config`; `/admin/shutdown`, `/admin/draining`, `/admin/config/cache_mb` | Unchanged |
| GraphQL schema | `/admin/schema`, `/admin` `updateGQLSchema`, `getGQLSchema` | Unchanged |
| Password reset | `/admin` `resetPassword` | Unchanged |
| External snapshot import | gRPC `UpdateExtSnapshotStreamingState`, `StreamExtSnapshot` | Unchanged |

### Operations that stay open

The posture never blocks these operations. They are how a client obtains a credential, or how infrastructure checks that a node is alive.

They keep the rules that applied before. In particular, `/login` still requires a whitelisted address and, when you configure one, the token. On a cluster with a token, send `X-Dgraph-AuthToken` along with the login request.

| Operation | Where |
|-----------|-------|
| Log in | `/login`, gRPC `Login`, `/admin` `login` |
| Version check | gRPC `CheckVersion` |
| Health | `/health` (without `?all`), gRPC `grpc.health.v1.Health` |
| GraphQL readiness | `/probe/graphql` |

:::caution
`/state` and `/health?all` are administrative under `data` and `none`. If your monitoring, readiness probes, or test tooling read `/state` without a credential, they start receiving `Unauthenticated` errors. Point them at `/health`, or send the token.
:::

## Choose a posture

Use the scenario that matches your deployment.

**You run Dgraph on a single host and only administer it from that host.**
Keep `full`. The empty whitelist already limits administrative operations to loopback.

**You widened the whitelist so other hosts or containers can reach Alpha, and you have no ACL.**
Set a token and move to `data`. Application traffic keeps working without credentials, and administration requires the token.

```sh
dgraph alpha --security "whitelist=0.0.0.0/0; token=<authtokenstring>; anonymous=data"
```

**You run ACL and every application already logs in.**
Move to `none`. Anonymous requests can no longer read or write data, even predicates that no ACL rule covers.

```sh
dgraph alpha --acl "secret-file=/dgraph/acl/hmac_secret" --security "anonymous=none"
```

**You run a multi-tenant cluster.**
Use `data` or `none` together with ACL. The posture stops an anonymous caller from reaching namespace lifecycle operations, while ACL continues to decide what each tenant's users may do.

## Examples

The examples use a token named `s3cr3t`. Use a long random value in production, for example the output of `openssl rand -hex 32`.

### Protect the control plane with a token

Start Alpha with an open whitelist, a token, and the `data` posture:

```sh
dgraph alpha --security "whitelist=0.0.0.0/0; token=s3cr3t; anonymous=data"
```

Queries and mutations work without a credential:

```sh
curl -s -H 'Content-Type: application/dql' localhost:8080/query \
  -d '{ q(func: has(name)) { name } }'
```

```json
{"data":{"q":[]},"extensions":{...}}
```

Reading cluster state without the token is refused:

```sh
curl -s localhost:8080/state
```

```json
{"errors":[{"message":"rpc error: code = Unauthenticated desc = the tenant-admin capability requires an identified caller, and this request presented no credential that verified. This cluster runs with --security \"anonymous=data\". Present the --security auth token, or log in with ACL."}]}
```

The same request with the token succeeds:

```sh
curl -s -H 'X-Dgraph-AuthToken: s3cr3t' localhost:8080/state
```

### Administer through the GraphQL admin endpoint

Send the token in the `X-Dgraph-AuthToken` header on `/admin` requests:

```sh
curl -s localhost:8080/admin \
  -H 'Content-Type: application/json' \
  -H 'X-Dgraph-AuthToken: s3cr3t' \
  -d '{"query":"mutation { export(input: {format: \"rdf\"}) { response { code message } } }"}'
```

Without the header, the mutation fails before it runs:

```json
{"errors":[{"message":"Invalid X-Dgraph-AuthToken","extensions":{"code":"ErrorUnauthorized"}}]}
```

### Require a credential for everything

Under `none`, an anonymous query is refused:

```sh
dgraph alpha --security "token=s3cr3t; anonymous=none"

curl -s -H 'Content-Type: application/dql' localhost:8080/query \
  -d '{ q(func: has(name)) { name } }'
```

```json
{"errors":[{"message":"rpc error: code = Unauthenticated desc = query requires an identified caller, and this request presented no credential that verified. This cluster runs with --security \"anonymous=none\". Present the --security auth token, or log in with ACL."}]}
```

Health checks keep working, so readiness probes are unaffected:

```sh
curl -s localhost:8080/health
```

### Send the token from a gRPC client

Over gRPC, put the token in the `auth-token` metadata key. In Go:

```go
import "google.golang.org/grpc/metadata"

ctx = metadata.AppendToOutgoingContext(ctx, "auth-token", "s3cr3t")
resp, err := client.Alter(ctx, op)
```

### Configure the option in a config file

The option is part of the `security` superflag in a YAML config file:

```yaml
security:
  token: s3cr3t
  whitelist: 10.0.0.0/8
  anonymous: data
```

Or as an environment variable:

```sh
export DGRAPH_ALPHA_SECURITY="whitelist=10.0.0.0/8; token=s3cr3t; anonymous=data"
dgraph alpha
```

## Dgraph Zero

Zero reads the same `--security` superflag. On Zero, `anonymous` controls its administrative HTTP endpoints on port `6080`.

| Endpoint | `full` | `data` or `none` |
|----------|--------|------------------|
| `/removeNode`, `/moveTablet` | Token, or a whitelisted address. Loopback only by default. | Token required. A whitelisted address is not enough. |
| `/state`, `/assign` | Open until you configure a token or whitelist. | Token required. |
| `/health` | Open | Open |

Zero has no ACL, so under `data` or `none` the token is the only credential it accepts. Configure one, or no caller can reach Zero's administrative endpoints, including from loopback.

```sh
dgraph zero --security "token=s3cr3t; anonymous=data"

# Refused, even from the Zero host itself
curl -s localhost:6080/state

# Allowed
curl -s -H 'X-Dgraph-AuthToken: s3cr3t' localhost:6080/state
```

:::tip
Set the same posture on Alpha and Zero. A cluster where only Alpha is closed still exposes Zero's control plane to anything inside Zero's whitelist.
:::

## Startup warnings

Alpha checks your `--security` settings at startup and logs a warning that begins with `SECURITY:` when they combine badly.

| Configuration | Warning | What to do |
|---------------|---------|------------|
| `full`, a widened whitelist, and neither a token nor ACL | Privileged operations are reachable from the whitelist range without any credential. | Set a token or enable ACL, and narrow the whitelist. Consider `anonymous=data`. |
| `data` or `none`, and neither a token nor ACL | No request can be identified, so the cluster cannot be administered, including from loopback. | Set a token or enable ACL. |

Zero logs the second warning when you set `data` or `none` without a token.

## Move a cluster to a closed posture

Follow these steps to move an existing cluster from `full` to `data` without an interruption.

1. **Upgrade every Alpha and Zero** to a release that supports the `anonymous` option. A node on an older release refuses to start with it.
2. **Choose a credential.** Set a token on every Alpha and Zero with `--security "token=..."`, or enable ACL. Restart the nodes.
3. **Update your tooling.** Send the token from every script, dashboard, and probe that performs administrative operations or reads `/state`. Leave the posture at `full` while you do this, so nothing breaks yet.
4. **Check the tools that load data.** `dgraph live` leases UIDs through an administrative operation. See [Known limitations](#known-limitations) before you continue.
5. **Set `anonymous=data`** on every Zero, then every Alpha, and restart them one at a time.
6. **Confirm the result.** An anonymous request to `/state` returns `Unauthenticated`, a request with the token succeeds, and the startup log has no `SECURITY:` warnings.

To return to the previous behavior, set `anonymous=full` and restart.

## Known limitations

* **`dgraph live` with only `--auth_token` cannot load data under `data` or `none`.** The loader leases UIDs through the `AllocateIDs` operation, and it does not send the token on that request. The request is refused and the loader retries without making progress. Use ACL credentials instead, which the loader does send:

  ```sh
  dgraph live -f data.rdf -s data.schema -a localhost:9080 -z localhost:5080 \
    --creds "user=groot;password=password;namespace=0"
  ```

  On a cluster without ACL, keep `anonymous=full` while you run the live loader.

* **`dgraph increment` and `dgraph import` have no `--auth_token` option.** Use ACL credentials with them on a closed cluster.

* **`dgraph bulk` is not affected.** It talks only to Zero's gRPC port, which the posture does not govern.

## Upgrades and mixed versions

Dgraph rejects any superflag option it does not recognize, so that a typo fails at startup instead of being silently ignored. An Alpha or Zero from a release that predates the `anonymous` option exits when it sees the option:

```text
superflag: found invalid options: anonymous=data.
valid options: token=; whitelist=;
```

Upgrade every node before you set the option. This applies to config files and environment variables too, because they feed the same superflag.

## Default value and future releases

The default is `full` so that upgrading changes nothing for an existing cluster. A future major release is planned to change the default to `data`. To prepare, set a token or enable ACL now, and set `anonymous=data` explicitly to confirm your tooling works with it.

## See also

* [Admin Endpoint Security](admin-endpoint-security) explains the whitelist and token options.
* [Superflags](../../cli/superflags#security-superflag) lists every `--security` option.
* [Enable ACL](../../installation/configuration/enable-acl) sets up user-based access control.
* [Ports Usage](ports-usage) describes which ports to expose to which networks.
