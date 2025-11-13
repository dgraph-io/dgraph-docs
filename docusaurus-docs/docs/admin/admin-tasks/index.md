---
title: Admin Tasks
---

Dgraph Alpha exposes various administrative endpoints over HTTP and GraphQL for operations like data export, cluster shutdown, and database management.

For security configuration including authentication, IP whitelisting, and token-based access control, see [Admin Endpoint Security](../security/admin-endpoint-security).

## Admin Endpoints

Dgraph Alpha provides the following administrative endpoints:

### HTTP Endpoints

- **`/admin`** - GraphQL endpoint for cluster management operations
- **`/admin/config/cache_mb`** - Configure cache size
- **`/admin/draining`** - Drain connections from a node
- **`/admin/shutdown`** - Shutdown a single Alpha node
- **`/admin/schema`** - Schema management
- **`/admin/schema/validate`** - Validate schema
- **`/alter`** - Apply schema updates and drop predicates
- **`/login`** - Authenticate ACL users

 By default, the `/admin` endpoint is only accessible from the same machine as the Alpha server. For detailed information about endpoint security and authentication, see [Admin Endpoint Security](../security/admin-endpoint-security).

## Admin Tasks

The following administrative tasks are available:

### Data Management

- **[Restrict Mutation Operations](restrict-mutation-operations)** - Control mutation permissions and enforce strict schema validation
- **[Secure Alter Operations](secure-alter-operations)** - Protect schema updates and predicate drops with authentication
- **[Export Database](export-database)** - Export data from Dgraph for backup, migration, or sharing
- **[Delete Database](delete-database)** - Drop all data from the database

### Cluster Management

- **[Check Cluster Health](check-cluster-health)** - Monitor cluster health using HTTP endpoints or GraphQL Admin API
- **[Shut Down Database](shut-down-database)** - Perform a clean shutdown of a Dgraph node
- **[Upgrade Database](upgrade-database)** - Safely upgrade Dgraph version and migrate data
