+++
date = "2017-03-20T22:25:17+11:00"
title = "Admin Endpoint Security"
weight = 2
type = "docs"
[menu.main]
  parent = "security"
+++

Dgraph Alpha exposes various administrative endpoints over HTTP and GraphQL for operations like data export and cluster shutdown. All admin endpoints are protected by three layers of authentication.

## Authentication Layers

Admin endpoints require authentication through three layers:

1. **IP Whitelisting** - Use the `--security` superflag's `whitelist` option on Dgraph Alpha to whitelist IP addresses other than localhost.
2. **Token Authentication** - If Dgraph Alpha is started with the `--security` superflag's `token` option, you must pass the token as an `X-Dgraph-AuthToken` header when making HTTP requests.
3. **ACL Guardian Access** - If ACL is enabled, you must pass the ACL-JWT of a Guardian user using the `X-Dgraph-AccessToken` header when making HTTP requests.

## Admin Endpoints

An admin endpoint is any HTTP endpoint which provides admin functionality. Admin endpoints usually start with the `/admin` path. The current list of admin endpoints includes:

* `/admin`
* `/admin/config/cache_mb`
* `/admin/draining`
* `/admin/shutdown`
* `/admin/schema`
* `/admin/schema/validate`
* `/alter`
* `/login`

### Special Endpoints

There are exceptions to the general authentication rule:

* **`/login`**: This endpoint logs-in an ACL user and provides them with a JWT. Only IP Whitelisting and token authentication checks are performed for this endpoint.
* **`/admin`**: This GraphQL endpoint provides queries/mutations corresponding to the HTTP admin endpoints. All queries/mutations on `/admin` have all three layers of authentication, except for `login (mutation)`, which has the same behavior as the HTTP `/login` endpoint.

## IP Whitelisting

By default, admin operations can only be initiated from the machine on which the Dgraph Alpha runs.

You can use the `--security` superflag's `whitelist` option to specify a comma-separated whitelist of IP addresses, IP ranges, CIDR ranges, or hostnames for hosts from which admin operations can be initiated.

**Examples:**

```sh
# Allow localhost only
dgraph alpha --security whitelist=127.0.0.1 ...

# Allow IP range and specific IP
dgraph alpha --security whitelist=172.17.0.0:172.20.0.0,192.168.1.1 ...

# Allow CIDR ranges
dgraph alpha --security whitelist=172.17.0.0/16,192.168.1.1/32 ...

# Allow hostnames
dgraph alpha --security whitelist=admin-bastion,host.docker.internal ...

# Allow all IPs (not recommended for production)
dgraph alpha --security whitelist=0.0.0.0/0 ...
```

For detailed network security configuration including TLS and port usage, see [Ports Usage]({{< relref "ports-usage.md" >}}) and [TLS Configuration]({{< relref "tls-configuration.md" >}}).

## Token Authentication

Token authentication provides a simple way to secure admin endpoints without full ACL. This is sometimes called "poor-man's auth" and is useful for basic protection.

### Setting Up Token Authentication

Specify the auth token with the `--security` superflag's `token` option for each Dgraph Alpha in the cluster:

```sh
dgraph alpha --security token=<authtokenstring>
```

### Using Token Authentication

Clients must include the same auth token in the `X-Dgraph-AuthToken` header when making admin requests:

```sh
# Without token - will be denied
curl -s localhost:8080/alter -d '{ "drop_all": true }'
# Permission denied. No token provided.

# With wrong token - will be denied
curl -s -H 'X-Dgraph-AuthToken: <wrongsecret>' localhost:8080/alter -d '{ "drop_all": true }'
# Permission denied. Incorrect token.

# With correct token - will succeed
curl -H 'X-Dgraph-AuthToken: <authtokenstring>' localhost:8080/alter -d '{ "drop_all": true }'
# Success. Token matches.
```

{{% notice "note" %}}
To fully secure admin operations in the cluster, the authentication token must be set for every Alpha node.
{{% /notice %}}

## Securing Alter Operations

Alter operations allow clients to apply schema updates and drop predicates from the database. By default, all clients are allowed to perform alter operations, which can be a security risk.

You can configure Dgraph to only allow alter operations when the client provides a specific token. This prevents clients from making unintended or accidental schema updates or predicate drops.

See the [Token Authentication](#token-authentication) section above for setup instructions. Once configured, all alter operations require the `X-Dgraph-AuthToken` header.

For enterprise-grade access control, see [Access Control Lists]({{< relref "../../enterprise-features/access-control-lists.md" >}}).

