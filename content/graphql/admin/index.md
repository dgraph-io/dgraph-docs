+++
title = "Administrative API on GraphQL"
description = "This documentation presents the Admin API and explains how to run a Dgraph database with GraphQL."
weight = 12
[menu.main]
  name = "Administrative API"
  identifier = "graphql-admin"
  parent = "graphql"
+++

This article presents the Admin API and explains how to run a Dgraph database with GraphQL.

## Running Dgraph with GraphQL

The simplest way to start with Dgraph GraphQL is to run the all-in-one Docker image.

```
docker run -it -p 8080:8080 dgraph/standalone:master
```

That brings up GraphQL at `localhost:8080/graphql` and `localhost:8080/admin`, but is intended for quickstart and doesn't persist data.

## Advanced options

Once you've tried out Dgraph GraphQL, you'll need to move past the `dgraph/standalone` and run and deploy Dgraph instances.

Dgraph is a distributed graph database.  It can scale to huge data and shard that data across a cluster of Dgraph instances.  GraphQL is built into Dgraph in its Alpha nodes. To learn how to manage and deploy a Dgraph cluster, check our [deployment guide](https://dgraph.io/docs/deploy/).

GraphQL schema introspection is enabled by default, but you can disable it by
setting the `--graphql` superflag's `introspection` option to false (`--graphql introspection=false`) when
starting the Dgraph Alpha nodes in your cluster.

## Dgraph's schema

Dgraph's GraphQL runs in Dgraph and presents a GraphQL schema where the queries and mutations are executed in the Dgraph cluster.  So the GraphQL schema is backed by Dgraph's schema.

{{% notice "warning" %}}
this means that if you have a Dgraph instance and change its GraphQL schema, the schema of the underlying Dgraph will also be changed!
{{% /notice %}}

## Endpoints

When you start Dgraph with GraphQL, two GraphQL endpoints are served.

### /graphql

At `/graphql` you'll find the GraphQL API for the types you've added.  That's what your app would access and is the GraphQL entry point to Dgraph.  If you need to know more about this, see the [quick start](https://dgraph.io/docs/graphql/quick-start/) and [schema docs](https://dgraph.io/docs/graphql/schema/).

### /admin

At `/admin` you'll find an admin API for administering your GraphQL instance.  The admin API is a GraphQL API that serves POST and GET as well as compressed data, much like the `/graphql` endpoint.

Here are the important types, queries, and mutations from the `admin` schema.

```graphql
	"""
	The Int64 scalar type represents a signed 64‐bit numeric non‐fractional value.
	Int64 can represent values in range [-(2^63),(2^63 - 1)].
	"""
	scalar Int64

	"""
	The UInt64 scalar type represents an unsigned 64‐bit numeric non‐fractional value.
	UInt64 can represent values in range [0,(2^64 - 1)].
	"""
	scalar UInt64

	"""
	The DateTime scalar type represents date and time as a string in RFC3339 format.
	For example: "1985-04-12T23:20:50.52Z" represents 20 minutes and 50.52 seconds after the 23rd hour of April 12th, 1985 in UTC.
	"""
	scalar DateTime

	"""
	Data about the GraphQL schema being served by Dgraph.
	"""
	type GQLSchema @dgraph(type: "dgraph.graphql") {
		id: ID!

		"""
		Input schema (GraphQL types) that was used in the latest schema update.
		"""
		schema: String!  @dgraph(pred: "dgraph.graphql.schema")

		"""
		The GraphQL schema that was generated from the 'schema' field.
		This is the schema that is being served by Dgraph at /graphql.
		"""
		generatedSchema: String!
	}

	type Cors @dgraph(type: "dgraph.cors"){
		acceptedOrigins: [String]
	}

	"""
	A NodeState is the state of an individual node in the Dgraph cluster.
	"""
	type NodeState {

		"""
		Node type : either 'alpha' or 'zero'.
		"""
		instance: String

		"""
		Address of the node.
		"""
		address: String

		"""
		Node health status : either 'healthy' or 'unhealthy'.
		"""
		status: String

		"""
		The group this node belongs to in the Dgraph cluster.
		See : https://dgraph.io/docs/deploy/#cluster-setup.
		"""
		group: String

		"""
		Version of the Dgraph binary.
		"""
		version: String

		"""
		Time in nanoseconds since the node started.
		"""
		uptime: Int64

		"""
		Time in Unix epoch time that the node was last contacted by another Zero or Alpha node.
		"""
		lastEcho: Int64

		"""
		List of ongoing operations in the background.
		"""
		ongoing: [String]

		"""
		List of predicates for which indexes are built in the background.
		"""
		indexing: [String]

		"""
		List of Enterprise Features that are enabled.
		"""
		ee_features: [String]
	}

	type MembershipState {
		counter: UInt64
		groups: [ClusterGroup]
		zeros: [Member]
		maxUID: UInt64
		maxNsID: UInt64
		maxTxnTs: UInt64
		maxRaftId: UInt64
		removed: [Member]
		cid: String
		license: License
		"""
		Contains list of namespaces. Note that this is not stored in proto's MembershipState and
		computed at the time of query.
		"""
		namespaces: [UInt64]
	}

	type ClusterGroup {
		id: UInt64
		members: [Member]
		tablets: [Tablet]
		snapshotTs: UInt64
		checksum: UInt64
	}

	type Member {
		id: UInt64
		groupId: UInt64
		addr: String
		leader: Boolean
		amDead: Boolean
		lastUpdate: UInt64
		clusterInfoOnly: Boolean
		forceGroupId: Boolean
	}

	type Tablet {
		groupId: UInt64
		predicate: String
		force: Boolean
		space: Int
		remove: Boolean
		readOnly: Boolean
		moveTs: UInt64
	}

	type License {
		user: String
		maxNodes: UInt64
		expiryTs: Int64
		enabled: Boolean
	}

	directive @dgraph(type: String, pred: String) on OBJECT | INTERFACE | FIELD_DEFINITION
	directive @id on FIELD_DEFINITION
	directive @secret(field: String!, pred: String) on OBJECT | INTERFACE

	type UpdateGQLSchemaPayload {
		gqlSchema: GQLSchema
	}

	input UpdateGQLSchemaInput {
		set: GQLSchemaPatch!
	}

	input GQLSchemaPatch {
		schema: String!
	}

	input ExportInput {
		"""
		Data format for the export, e.g. "rdf" or "json" (default: "rdf")
		"""
		format: String
		"""
		Namespace for the export in multi-tenant cluster. Users from guardians of galaxy can export
		all namespaces by passing a negative value or specific namespaceId to export that namespace.
		"""
		namespace: Int

		"""
		Destination for the export: e.g. Minio or S3 bucket or /absolute/path
		"""
		destination: String

		"""
		Access key credential for the destination.
		"""
		accessKey: String

		"""
		Secret key credential for the destination.
		"""
		secretKey: String

		"""
		AWS session token, if required.
		"""
		sessionToken: String

		"""
		Set to true to allow backing up to S3 or Minio bucket that requires no credentials.
		"""
		anonymous: Boolean
	}

	input TaskInput {
		id: String!
	}
	type Response {
		code: String
		message: String
	}

	type ExportPayload {
		response: Response
		taskId: String
	}

	type DrainingPayload {
		response: Response
	}

	type ShutdownPayload {
		response: Response
	}

	type TaskPayload {
		kind: TaskKind
		status: TaskStatus
		lastUpdated: DateTime
	}
	enum TaskStatus {
		Queued
		Running
		Failed
		Success
		Unknown
	}
	enum TaskKind {
		Backup
		Export
		Unknown
	}
	input ConfigInput {
		"""
		Estimated memory the caches can take. Actual usage by the process would be
		more than specified here. The caches will be updated according to the
		cache_percentage flag.
		"""
		cacheMb: Float

		"""
		True value of logRequest enables logging of all the requests coming to alphas.
		False value of logRequest disables above.
		"""
		logRequest: Boolean
	}

	type ConfigPayload {
		response: Response
	}

	type Config {
		cacheMb: Float
	}
	input RemoveNodeInput {
		"""
		ID of the node to be removed.
		"""
		nodeId: UInt64!
		"""
		ID of the group from which the node is to be removed.
		"""
		groupId: UInt64!
	}
	type RemoveNodePayload {
		response: Response
	}
	input MoveTabletInput {
		"""
		Namespace in which the predicate exists.
		"""
		namespace: UInt64
		"""
		Name of the predicate to move.
		"""
		tablet: String!
		"""
		ID of the destination group where the predicate is to be moved.
		"""
		groupId: UInt64!
	}
	type MoveTabletPayload {
		response: Response
	}
	enum AssignKind {
		UID
		TIMESTAMP
		NAMESPACE_ID
	}
	input AssignInput {
		"""
		Choose what to assign: UID, TIMESTAMP or NAMESPACE_ID.
		"""
		what: AssignKind!
		"""
		How many to assign.
		"""
		num: UInt64!
	}
	type AssignedIds {
		"""
		The first UID, TIMESTAMP or NAMESPACE_ID assigned.
		"""
		startId: UInt64
		"""
		The last UID, TIMESTAMP or NAMESPACE_ID assigned.
		"""
		endId: UInt64
		"""
		TIMESTAMP for read-only transactions.
		"""
		readOnly: UInt64
	}
	type AssignPayload {
		response: AssignedIds
	}

	input BackupInput {
		"""
		Destination for the backup: e.g. Minio or S3 bucket.
		"""
		destination: String!
		"""
		Access key credential for the destination.
		"""
		accessKey: String
		"""
		Secret key credential for the destination.
		"""
		secretKey: String
		"""
		AWS session token, if required.
		"""
		sessionToken: String
		"""
		Set to true to allow backing up to S3 or Minio bucket that requires no credentials.
		"""
		anonymous: Boolean
		"""
		Force a full backup instead of an incremental backup.
		"""
		forceFull: Boolean
	}
	type BackupPayload {
		response: Response
		taskId: String
	}
	input RestoreInput {
		"""
		Destination for the backup: e.g. Minio or S3 bucket.
		"""
		location: String!
		"""
		Backup ID of the backup series to restore. This ID is included in the manifest.json file.
		If missing, it defaults to the latest series.
		"""
		backupId: String
		"""
		Number of the backup within the backup series to be restored. Backups with a greater value
		will be ignored. If the value is zero or missing, the entire series will be restored.
		"""
		backupNum: Int
		"""
		Path to the key file needed to decrypt the backup. This file should be accessible
		by all alphas in the group. The backup will be written using the encryption key
		with which the cluster was started, which might be different than this key.
		"""
		encryptionKeyFile: String
		"""
		Vault server address where the key is stored. This server must be accessible
		by all alphas in the group. Default "http://localhost:8200".
		"""
		vaultAddr: String
		"""
		Path to the Vault RoleID file.
		"""
		vaultRoleIDFile: String
		"""
		Path to the Vault SecretID file.
		"""
		vaultSecretIDFile: String
		"""
		Vault kv store path where the key lives. Default "secret/data/dgraph".
		"""
		vaultPath: String
		"""
		Vault kv store field whose value is the key. Default "enc_key".
		"""
		vaultField: String
		"""
		Vault kv store field's format. Must be "base64" or "raw". Default "base64".
		"""
		vaultFormat: String
		"""
		Access key credential for the destination.
		"""
		accessKey: String
		"""
		Secret key credential for the destination.
		"""
		secretKey: String
		"""
		AWS session token, if required.
		"""
		sessionToken: String
		"""
		Set to true to allow backing up to S3 or Minio bucket that requires no credentials.
		"""
		anonymous: Boolean
	}
	type RestorePayload {
		"""
		A short string indicating whether the restore operation was successfully scheduled.
		"""
		code: String
		"""
		Includes the error message if the operation failed.
		"""
		message: String
	}
	input ListBackupsInput {
		"""
		Destination for the backup: e.g. Minio or S3 bucket.
		"""
		location: String!
		"""
		Access key credential for the destination.
		"""
		accessKey: String
		"""
		Secret key credential for the destination.
		"""
		secretKey: String
		"""
		AWS session token, if required.
		"""
		sessionToken: String
		"""
		Whether the destination doesn't require credentials (e.g. S3 public bucket).
		"""
		anonymous: Boolean
	}
	type BackupGroup {
		"""
		The ID of the cluster group.
		"""
		groupId: UInt64
		"""
		List of predicates assigned to the group.
		"""
		predicates: [String]
	}
	type Manifest {
		"""
		Unique ID for the backup series.
		"""
		backupId: String
		"""
		Number of this backup within the backup series. The full backup always has a value of one.
		"""
		backupNum: UInt64
		"""
		Whether this backup was encrypted.
		"""
		encrypted: Boolean
		"""
		List of groups and the predicates they store in this backup.
		"""
		groups: [BackupGroup]
		"""
		Path to the manifest file.
		"""
		path: String
		"""
		The timestamp at which this backup was taken. The next incremental backup will
		start from this timestamp.
		"""
		since: UInt64
		"""
		The type of backup, either full or incremental.
		"""
		type: String
	}
	type LoginResponse {
		"""
		JWT token that should be used in future requests after this login.
		"""
		accessJWT: String
		"""
		Refresh token that can be used to re-login after accessJWT expires.
		"""
		refreshJWT: String
	}
	type LoginPayload {
		response: LoginResponse
	}
	type User @dgraph(type: "dgraph.type.User") @secret(field: "password", pred: "dgraph.password") {
		"""
		Username for the user.  Dgraph ensures that usernames are unique.
		"""
		name: String! @id @dgraph(pred: "dgraph.xid")
		groups: [Group] @dgraph(pred: "dgraph.user.group")
	}
	type Group @dgraph(type: "dgraph.type.Group") {
		"""
		Name of the group.  Dgraph ensures uniqueness of group names.
		"""
		name: String! @id @dgraph(pred: "dgraph.xid")
		users: [User] @dgraph(pred: "~dgraph.user.group")
		rules: [Rule] @dgraph(pred: "dgraph.acl.rule")
	}
	type Rule @dgraph(type: "dgraph.type.Rule") {
		"""
		Predicate to which the rule applies.
		"""
		predicate: String! @dgraph(pred: "dgraph.rule.predicate")
		"""
		Permissions that apply for the rule.  Represented following the UNIX file permission
		convention. That is, 4 (binary 100) represents READ, 2 (binary 010) represents WRITE,
		and 1 (binary 001) represents MODIFY (the permission to change a predicate’s schema).
		The options are:
		* 1 (binary 001) : MODIFY
		* 2 (010) : WRITE
		* 3 (011) : WRITE+MODIFY
		* 4 (100) : READ
		* 5 (101) : READ+MODIFY
		* 6 (110) : READ+WRITE
		* 7 (111) : READ+WRITE+MODIFY
		Permission 0, which is equal to no permission for a predicate, blocks all read,
		write and modify operations.
		"""
		permission: Int! @dgraph(pred: "dgraph.rule.permission")
	}
	input StringHashFilter {
		eq: String
	}
	enum UserOrderable {
		name
	}
	enum GroupOrderable {
		name
	}
	input AddUserInput {
		name: String!
		password: String!
		groups: [GroupRef]
	}
	input AddGroupInput {
		name: String!
		rules: [RuleRef]
	}
	input UserRef {
		name: String!
	}
	input GroupRef {
		name: String!
	}
	input RuleRef {
		"""
		Predicate to which the rule applies.
		"""
		predicate: String!
		"""
		Permissions that apply for the rule.  Represented following the UNIX file permission
		convention. That is, 4 (binary 100) represents READ, 2 (binary 010) represents WRITE,
		and 1 (binary 001) represents MODIFY (the permission to change a predicate’s schema).
		The options are:
		* 1 (binary 001) : MODIFY
		* 2 (010) : WRITE
		* 3 (011) : WRITE+MODIFY
		* 4 (100) : READ
		* 5 (101) : READ+MODIFY
		* 6 (110) : READ+WRITE
		* 7 (111) : READ+WRITE+MODIFY
		Permission 0, which is equal to no permission for a predicate, blocks all read,
		write and modify operations.
		"""
		permission: Int!
	}
	input UserFilter {
		name: StringHashFilter
		and: UserFilter
		or: UserFilter
		not: UserFilter
	}
	input UserOrder {
		asc: UserOrderable
		desc: UserOrderable
		then: UserOrder
	}
	input GroupOrder {
		asc: GroupOrderable
		desc: GroupOrderable
		then: GroupOrder
	}
	input UserPatch {
		password: String
		groups: [GroupRef]
	}
	input UpdateUserInput {
		filter: UserFilter!
		set: UserPatch
		remove: UserPatch
	}
	input GroupFilter {
		name: StringHashFilter
		and: UserFilter
		or: UserFilter
		not: UserFilter
	}
	input SetGroupPatch {
		rules: [RuleRef!]!
	}
	input RemoveGroupPatch {
		rules: [String!]!
	}
	input UpdateGroupInput {
		filter: GroupFilter!
		set: SetGroupPatch
		remove: RemoveGroupPatch
	}
	type AddUserPayload {
		user: [User]
	}
	type AddGroupPayload {
		group: [Group]
	}
	type DeleteUserPayload {
		msg: String
		numUids: Int
	}
	type DeleteGroupPayload {
		msg: String
		numUids: Int
	}
	input AddNamespaceInput {
		password: String
	}
	input DeleteNamespaceInput {
		namespaceId: Int!
	}
	type NamespacePayload {
		namespaceId: UInt64
		message: String
	}
	input ResetPasswordInput {
		userId: String!
		password: String!
		namespace: Int!
	}
	type ResetPasswordPayload {
		userId: String
		message: String
		namespace: UInt64
	}
	input EnterpriseLicenseInput {
		"""
		The contents of license file as a String.
		"""
		license: String!
	}
	type EnterpriseLicensePayload {
		response: Response
	}

	type Query {
		getGQLSchema: GQLSchema
		health: [NodeState]
		state: MembershipState
		config: Config
		task(input: TaskInput!): TaskPayload

		getUser(name: String!): User
		getGroup(name: String!): Group
		"""
		Get the currently logged in user.
		"""
		getCurrentUser: User
		queryUser(filter: UserFilter, order: UserOrder, first: Int, offset: Int): [User]
		queryGroup(filter: GroupFilter, order: GroupOrder, first: Int, offset: Int): [Group]
		"""
		Get the information about the backups at a given location.
		"""
		listBackups(input: ListBackupsInput!) : [Manifest]
	}
	type Mutation {

		"""
		Update the Dgraph cluster to serve the input schema.  This may change the GraphQL
		schema, the types and predicates in the Dgraph schema, and cause indexes to be recomputed.
		"""
		updateGQLSchema(input: UpdateGQLSchemaInput!) : UpdateGQLSchemaPayload

		"""
		Starts an export of all data in the cluster.  Export format should be 'rdf' (the default
		if no format is given), or 'json'.
		See : https://dgraph.io/docs/deploy/#export-database
		"""
		export(input: ExportInput!): ExportPayload

		"""
		Set (or unset) the cluster draining mode.  In draining mode no further requests are served.
		"""
		draining(enable: Boolean): DrainingPayload

		"""
		Shutdown this node.
		"""
		shutdown: ShutdownPayload

		"""
		Alter the node's config.
		"""
		config(input: ConfigInput!): ConfigPayload
		"""
		Remove a node from the cluster.
		"""
		removeNode(input: RemoveNodeInput!): RemoveNodePayload
		"""
		Move a predicate from one group to another.
		"""
		moveTablet(input: MoveTabletInput!): MoveTabletPayload
		"""
		Lease UIDs, Timestamps or Namespace IDs in advance.
		"""
		assign(input: AssignInput!): AssignPayload

		"""
		Start a binary backup.  See : https://dgraph.io/docs/enterprise-features/#binary-backups
		"""
		backup(input: BackupInput!) : BackupPayload
		"""
		Start restoring a binary backup.  See :
			https://dgraph.io/docs/enterprise-features/#binary-backups
		"""
		restore(input: RestoreInput!) : RestorePayload
		"""
		Login to Dgraph.  Successful login results in a JWT that can be used in future requests.
		If login is not successful an error is returned.
		"""
		login(userId: String, password: String, namespace: Int, refreshToken: String): LoginPayload
		"""
		Add a user.  When linking to groups: if the group doesn't exist it is created; if the group
		exists, the new user is linked to the existing group.  It's possible to both create new
		groups and link to existing groups in the one mutation.
		Dgraph ensures that usernames are unique, hence attempting to add an existing user results
		in an error.
		"""
		addUser(input: [AddUserInput!]!): AddUserPayload
		"""
		Add a new group and (optionally) set the rules for the group.
		"""
		addGroup(input: [AddGroupInput!]!): AddGroupPayload
		"""
		Update users, their passwords and groups.  As with AddUser, when linking to groups: if the
		group doesn't exist it is created; if the group exists, the new user is linked to the existing
		group.  If the filter doesn't match any users, the mutation has no effect.
		"""
		updateUser(input: UpdateUserInput!): AddUserPayload
		"""
		Add or remove rules for groups. If the filter doesn't match any groups,
		the mutation has no effect.
		"""
		updateGroup(input: UpdateGroupInput!): AddGroupPayload
		deleteGroup(filter: GroupFilter!): DeleteGroupPayload
		deleteUser(filter: UserFilter!): DeleteUserPayload
		"""
		Add a new namespace.
		"""
		addNamespace(input: AddNamespaceInput): NamespacePayload
		"""
		Delete a namespace.
		"""
		deleteNamespace(input: DeleteNamespaceInput!): NamespacePayload
		"""
		Reset password can only be used by the Guardians of the galaxy to reset password of
		any user in any namespace.
		"""
		resetPassword(input: ResetPasswordInput!): ResetPasswordPayload
		"""
		Apply enterprise license.
		"""
		enterpriseLicense(input: EnterpriseLicenseInput!): EnterpriseLicensePayload
	}
```

You'll notice that the `/admin` schema is very much the same as the schemas generated by Dgraph GraphQL.

* The `health` query lets you know if everything is connected and if there's a schema currently being served at `/graphql`.
* The `state`  query returns the current state of the cluster and group membership information. For more information about `state` see [here](https://dgraph.io/docs/deploy/dgraph-zero/#more-about-state-endpoint).
* The `config` query returns the configuration options of the cluster set at the time of starting it.
* The `getGQLSchema` query gets the current GraphQL schema served at `/graphql`, or returns null if there's no such schema.
* The `updateGQLSchema` mutation allows you to change the schema currently served at `/graphql`.

## Enterprise features

Enterprise Features like ACL, Backups and Restore are also available using the GraphQL API at `/admin` endpoint.

* [ACL](https://dgraph.io/docs/enterprise-features/access-control-lists/#using-graphql-admin-api)
* [Backups](https://dgraph.io/docs/enterprise-features/binary-backups/#create-a-backup)
* [Restore](https://dgraph.io/docs/enterprise-features/binary-backups/#restore-from-backup)

## First start

On first starting with a blank database:

* There's no schema served at `/graphql`.
* Querying the `/admin` endpoint for `getGQLSchema` returns `"getGQLSchema": null`.
* Querying the `/admin` endpoint for `health` lets you know that no schema has been added.

## Validating a schema

You can validate a GraphQL schema before adding it to your database by sending
your schema definition in an HTTP POST request to the to the
`/admin/schema/validate` endpoint, as shown in the following example:

Request header:

```ssh
path: /admin/schema/validate
method: POST
```

Request body:

```graphql
type Person {
	name: String
}
```

This endpoint returns a JSON response that indicates if the schema is valid or
not, and provides an error if isn't valid. In this case, the schema is valid,
so the JSON response includes the following message: `Schema is valid`.

## Modifying a schema

There are two ways you can modify a GraphQL schema:
- Using `/admin/schema`
- Using the `updateGQLSchema` mutation on `/admin`

{{% notice "tip" %}}
While modifying the GraphQL schema, if you get errors like `errIndexingInProgress`, `another operation is already running` or `server is not ready`, please wait a moment and then retry the schema update.
{{% /notice %}}

### Using `/admin/schema`

The `/admin/schema` endpoint provides a simplified method to add and update schemas.

To create a schema you only need to call the `/admin/schema` endpoint with the required schema definition. For example:

```graphql
type Person {
	name: String
}
```

If you have the schema definition stored in a `schema.graphql` file, you can use `curl` like this:
```
curl -X POST localhost:8080/admin/schema --data-binary '@schema.graphql'
```

On successful execution, the `/admin/schema` endpoint will give you a JSON response with a success code.

### Using `updateGQLSchema` to add or modify a schema

Another option to add or modify a GraphQL schema is the `updateGQLSchema` mutation.

For example, to create a schema using `updateGQLSchema`, run this mutation on the `/admin` endpoint:

```graphql
mutation {
  updateGQLSchema(
    input: { set: { schema: "type Person { name: String }"}})
  {
    gqlSchema {
      schema
      generatedSchema
    }
  }
}
```

### Adding CORS

You can add CORS Origins by specifying `# Dgraph.Allow-Origin` at the end of the GraphQL schema using a schema update. For example:

```graphql
# Dgraph.Allow-Origin "https://example.com" 
# Dgraph.Allow-Origin "https://www.exmaple.com"
```

## Initial schema

Regardless of the method used to upload the GraphQL schema, on a black database, adding this schema

```graphql
type Person {
	name: String
}
```

would cause the following:

* The `/graphql` endpoint would refresh and serve the GraphQL schema generated from type `type Person { name: String }`: that's Dgraph type `Person` and predicate `Person.name: string .` (see [this article](https://dgraph.io/docs/graphql/dgraph) on how to customize the generated schema)
* The schema of the underlying Dgraph instance would be altered to allow for the new `Person` type and `name` predicate.
* The `/admin` endpoint for `health` would return that a schema is being served.
* The mutation would return `"schema": "type Person { name: String }"` and the generated GraphQL schema for `generatedSchema` (this is the schema served at `/graphql`).
* Querying the `/admin` endpoint for `getGQLSchema` would return the new schema.

## Migrating a schema

Given an instance serving the GraphQL schema from the previous section, updating the schema to the following

```graphql
type Person {
    name: String @search(by: [regexp])
    dob: DateTime
}
```

would change the GraphQL definition of `Person` and result in the following:

* The `/graphql` endpoint would refresh and serve the GraphQL schema generated from the new type.
* The schema of the underlying Dgraph instance would be altered to allow for `dob` (predicate `Person.dob: datetime .` is added, and `Person.name` becomes `Person.name: string @index(regexp).`) and indexes are rebuilt to allow the regexp search.
* The `health` is unchanged.
* Querying the `/admin` endpoint for `getGQLSchema` would return the updated schema.

## Removing indexes from a schema

Adding a schema through GraphQL doesn't remove existing data (it only removes indexes).

For example, starting from the schema in the previous section and modifying it with the initial schema

```graphql
type Person {
	name: String
}
```

would have the following effects:

* The `/graphql` endpoint would refresh to serve the schema built from this type.
* Thus, field `dob` would no longer be accessible, and there would be no search available on `name`.
* The search index on `name` in Dgraph would be removed.
* The predicate `dob` in Dgraph would be left untouched (the predicate remains and no data is deleted).
