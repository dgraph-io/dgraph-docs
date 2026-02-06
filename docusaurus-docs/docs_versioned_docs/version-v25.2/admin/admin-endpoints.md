---
title: Admin Endpoints
---

The [Admin Tasks](./admin-tasks/index.md) section provides detailed guides for common administrative operations, but this page provides an exhaustive list of all administrative endpoints available in Dgraph. 

Dgraph provides administrative endpoints on both Alpha and Zero nodes.

## Alpha HTTP Endpoints (port 8080)

Dgraph Alpha exposes the following HTTP endpoints on port `8080` (plus optional port offset):

- **`/admin/config/cache_mb`** - Configure cache size
- **`/admin/draining`** - Drain connections from a node
- **`/admin/shutdown`** - Shutdown a single Alpha node
- **`/alter`** - Apply schema updates and drop predicates
- **`/login`** - Authenticate ACL users
- **`/health`** - Health status
- **`/health?all`** - Health status of all servers in the cluster
- **`/state`** - Returns information about the nodes that are part of the cluster. This includes information about the size of predicates and which groups they belong to.

## Zero HTTP Endpoints (port 6080)

Dgraph Zero exposes the following HTTP endpoints on port `6080` (plus optional port offset):

### GET Endpoints

- **`/assign?what=uids&num=100`** - Allocates a range of UIDs specified by the `num` argument, and returns a JSON map containing the `startId` and `endId` that defines the range of UIDs (inclusive). This UID range can be safely assigned externally to new nodes during data ingestion.
- **`/assign?what=timestamps&num=100`** - Requests timestamps from Zero. This is useful to "fast forward" the state of the Zero node when starting from a postings directory that already has commits higher than Zero's leased timestamp.
- **`/removeNode?id=3&group=2`** - Removes a dead Zero or Alpha node. When a replica node goes offline and can't be recovered, you can remove it and add a new node to the quorum. To remove dead Zero nodes, pass `group=0` and the id of the Zero node to this endpoint.

:::note
Before using the `/removeNode` endpoint, ensure that the node is down and ensure that it doesn't come back up ever again. Do not use the same `idx` of a node that was removed earlier.
:::

- **`/moveTablet?tablet=name&group=2`** - Moves a tablet to a group. Zero already rebalances shards every 8 mins, but this endpoint can be used to force move a tablet.

### POST Endpoints

- **`/enterpriseLicense`** - Applies an enterprise license to the cluster by supplying it as part of the body.

## Alpha GraphQL Admin Endpoints (port 8080)

**`/admin`** - GraphQL endpoint for cluster management operations

The GraphQL Admin API provides an alternative way to perform the same administrative tasks available through HTTP endpoints. Many operations that can be done via HTTP endpoints (such as export, backup, shutdown, draining, etc.) can also be performed using GraphQL queries and mutations. The GraphQL interface offers a more structured and type-safe approach to administrative operations.

#### Queries

- **`getGQLSchema`** - Get the current GraphQL schema
- **`health`** - Get health status
- **`state`** - Get cluster state
- **`config`** - Get node configuration
- **`task`** - Get task information
- **`getUser`** - Get a user by name
- **`getGroup`** - Get a group by name
- **`getCurrentUser`** - Get the currently logged in user
- **`queryUser`** - Query users with filters
- **`queryGroup`** - Query groups with filters
- **`listBackups`** - Get information about backups at a given location

#### Mutations

- **`updateGQLSchema`** - Update the Dgraph cluster to serve the input schema. This may change the GraphQL schema, the types and predicates in the Dgraph schema, and cause indexes to be recomputed.
- **`export`** - Start an export of all data in the cluster. Export format should be 'rdf' (the default if no format is given), or 'json'.
- **`draining`** - Set (or unset) the cluster draining mode. In draining mode no further requests are served.
- **`shutdown`** - Shutdown this node.
- **`config`** - Alter the node's config.
- **`removeNode`** - Remove a node from the cluster.
- **`moveTablet`** - Move a predicate from one group to another.
- **`assign`** - Lease UIDs, Timestamps or Namespace IDs in advance.
- **`backup`** - Start a binary backup.
- **`restore`** - Start restoring a binary backup.
- **`restoreTenant`** - Restore given tenant into namespace 0 of the cluster.
- **`login`** - Login to Dgraph. Successful login results in a JWT that can be used in future requests. If login is not successful an error is returned.
- **`addUser`** - Add a user. When linking to groups: if the group doesn't exist it is created; if the group exists, the new user is linked to the existing group. It's possible to both create new groups and link to existing groups in the one mutation. Dgraph ensures that usernames are unique, hence attempting to add an existing user results in an error.
- **`addGroup`** - Add a new group and (optionally) set the rules for the group.
- **`updateUser`** - Update users, their passwords and groups. As with AddUser, when linking to groups: if the group doesn't exist it is created; if the group exists, the new user is linked to the existing group. If the filter doesn't match any users, the mutation has no effect.
- **`updateGroup`** - Add or remove rules for groups. If the filter doesn't match any groups, the mutation has no effect.
- **`deleteGroup`** - Delete a group.
- **`deleteUser`** - Delete a user.
- **`addNamespace`** - Add a new namespace.
- **`deleteNamespace`** - Delete a namespace.
- **`resetPassword`** - Reset password can only be used by the Guardians of the galaxy to reset password of any user in any namespace.


For security configuration including authentication, IP whitelisting, and token-based access control, see [Admin Endpoint Security](./security/admin-endpoint-security).
