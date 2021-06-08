+++
date = "2017-03-20T22:25:17+11:00"
title = "Dgraph Administration"
description = "In this guide, we explain Dgraph administration operations, including white-listing, mutation restriction, shutting down / deleting databases, and more."
weight = 1
[menu.main]
    parent = "admin"
+++

Each Dgraph Alpha exposes various administrative (admin) endpoints both over
HTTP and GraphQL, for example endpoints to export data and to perform a clean
shutdown. All such admin endpoints are protected by three layers of authentication:

1. IP White-listing (use the `--security` superflag's `whitelist` option on Dgraph Alpha to whitelist IP addresses other than
   localhost).
2. Poor-man's auth, if Dgraph Alpha is started with the `--security` superflag's `token` option,
   then you should pass the token as an `X-Dgraph-AuthToken` header while
   making the HTTP request.
3. Guardian-only access, if ACL is enabled. In this case you should pass the ACL-JWT
   of a Guardian user using the `X-Dgraph-AccessToken` header while making the
   HTTP request.

An admin endpoint is any HTTP endpoint which provides admin functionality.
Admin endpoints usually start with the `/admin` path. The current list of admin
endpoints includes the following:

* `/admin`
* `/admin/backup`
* `/admin/config/lru_mb`
* `/admin/draining`
* `/admin/export`
* `/admin/shutdown`
* `/admin/schema`
* `/alter`
* `/login`

There are a few exceptions to the general rule described above:

* `/login`: This endpoint logs-in an ACL user, and provides them with a JWT.
  Only IP Whitelisting and Poor-man's auth checks are performed for this endpoint.
* `/admin`: This endpoint provides GraphQL queries/mutations corresponding to
  the HTTP admin endpoints. All of the queries/mutations on `/admin` have all
  three layers of authentication, except for `login (mutation)`, which has the
  same behavior as the above HTTP `/login` endpoint.

## Whitelisting Admin Operations

By default, admin operations can only be initiated from the machine on which the Dgraph Alpha runs.

You can use the `--security` superflag's `whitelist` option to specify a comma-separated whitelist of IP addresses, IP ranges, CIDR ranges, or hostnames for hosts from which admin operations can be initiated.

**IP Address**

```sh
dgraph alpha --security whitelist=127.0.0.1 ...
```
This would allow admin operations from hosts with IP 127.0.0.1 (i.e., localhost only).

**IP Range**
```sh
dgraph alpha --security whitelist=172.17.0.0:172.20.0.0,192.168.1.1 ...
```

This would allow admin operations from hosts with IP between `172.17.0.0` and `172.20.0.0` along with
the server which has IP address as `192.168.1.1`.

**CIDR Range**

```sh
dgraph alpha --security whitelist=172.17.0.0/16,172.18.0.0/15,172.20.0.0/32,192.168.1.1/32 ...
```

This would allow admin operations from hosts that matches the CIDR range `172.17.0.0/16`, `172.18.0.0/15`, `172.20.0.0/32`, or `192.168.1.1/32` (the same range as the IP Range example).

You can set whitelist IP to `0.0.0.0/0` to whitelist all IP addresses.

**Hostname**

```sh
dgraph alpha --security whitelist=admin-bastion,host.docker.internal ...
```

This would allow admin operations from hosts with hostnames `admin-bastion` and `host.docker.internal`.

## Restrict Mutation Operations

By default, you can perform mutation operations for any predicate.
If the predicate in mutation doesn't exist in the schema,
the predicate gets added to the schema with an appropriate
[Dgraph Type]({{< relref "query-language/schema.md" >}}).

You can use `--limit "mutations=disallow"` to disable all mutations,
which is set to `allow` by default.

```sh
dgraph alpha --limit "mutations=disallow;"
```

Enforce a strict schema by setting `--limit "mutations=strict`.
This mode allows mutations only on predicates already in the schema.
Before performing a mutation on a predicate that doesn't exist in the schema,
you need to perform an alter operation with that predicate and its schema type.

```sh
dgraph alpha --limit "mutation=strict; mutations-nquad=1000000"
```

## Secure Alter Operations

Clients can use alter operations to apply schema updates and drop particular or all predicates from the database.
By default, all clients are allowed to perform alter operations.
You can configure Dgraph to only allow alter operations when the client provides a specific token.
You can use this "Simple ACL" token to prevent clients from making unintended or accidental schema updates or predicate drops.

You can specify the auth token with the `--security` superflag's `token` option for each Dgraph Alpha in the cluster.
Clients must include the same auth token to make alter requests.

```sh
$ dgraph alpha --security token=<authtokenstring>
```

```sh
$ curl -s localhost:8080/alter -d '{ "drop_all": true }'
# Permission denied. No token provided.
```

```sh
$ curl -s -H 'X-Dgraph-AuthToken: <wrongsecret>' localhost:8180/alter -d '{ "drop_all": true }'
# Permission denied. Incorrect token.
```

```sh
$ curl -H 'X-Dgraph-AuthToken: <authtokenstring>' localhost:8180/alter -d '{ "drop_all": true }'
# Success. Token matches.
```

{{% notice "note" %}}
To fully secure alter operations in the cluster, the authentication token must be set for every Alpha node.
{{% /notice %}}


## Export Database

An export of all nodes is started by locally executing the following GraphQL mutation on the `/admin` endpoint of an Alpha node (e.g. `localhost:8080/admin`) using any compatible client like Insomnia, GraphQL Playground or GraphiQL.

```graphql
mutation {
  export(input: {}) {
    response {
      message
      code
    }
  }
}
```

{{% notice "note" %}}
Since v21.03, the `export` and `backup` APIs are asynchronous: instead of returning the requested data,
they queue the task and return a `taskId` immediately.
These tasks run in the background, and Dgraph has a worker thread that executes them one at a time.
{{% /notice %}}

{{% notice "warning" %}}By default, this won't work if called from outside the server where the Dgraph Alpha is running.
You can specify a list or range of whitelisted IP addresses to initiate admin operations like export. You can do so using the `--security` superflag's `whitelist` option with the `dgraph alpha` command.
{{% /notice %}}

This triggers an export for all Alpha groups of the cluster. The data is exported from the following Dgraph instances:

1. For the Alpha instance that receives the GET request, the group's export data is stored with this Alpha.
2. For every other group, its group's export data is stored with the Alpha leader of that group.

It is up to the user to retrieve the right export files from the Alphas in the
cluster. Dgraph does not copy all files to the Alpha that initiated the export.
The user must also ensure that there is sufficient space on disk to store the
export.

### Check queued tasks

A new Task API has been added to the `/admin` endpoint. This allows you to check the status of a queued task (either `backup` or `export`).
You can provide the `taskId`, and the response will give you the current task status.

For example:

```bash
query {
    task(input: {id: "0x1234"}) {
        status
        lastUpdated
        kind
    }
}
```

### Configure Dgraph Alpha server nodes

Each Dgraph Alpha leader for a group writes output as a gzipped file to the export
directory specified via the `--export` flag (defaults to an **export** directory). If any of the groups fail, the
entire export process is considered failed and an error is returned.

As an example of configuring data export, you can run this:

```bash
docker run --detach --rm --name dgraph-standalone \
  --publish 8080:8080 \
  --publish 8000:8000 \
  --volume ~/exports:/dgraph/myexports \
  --env "DGRAPH_ALPHA_EXPORT=/dgraph/myexports" \
  dgraph/standalone:{{< version >}}
```

{{% notice "tip" %}}
The export configuration can be configured as an environment variable `DGRAPH_ALPHA_EXPORT`, command line flag `--export`, or in a configuration file with the `export` key.  See [Config]({{< relref "config" >}}) for more information in general about configuring Dgraph.
{{% /notice %}}

### Export data format

By default, Dgraph exports data in RDF format. You can explicitly set the output format with the `format` field. For example:

```graphql
mutation {
  export(input: { format: "rdf" }) {
    response {
      message
      code
    }
  }
}
```


You can specify a different output format using the `format` field. For example:

```graphql
mutation {
  export(input: { format: "json" }) {
    response {
      message
      code
    }
  }
}
```

Currently, `rdf` and `json` are the only formats supported.

### Export to NFS or a file path

{{% notice "note" %}}
This feature was introduced in [v20.11.0](https://github.com/dgraph-io/dgraph/releases/tag/v20.11.0).
{{% /notice %}}

You can override the default folder path by adding the `destination` input field to the directory where you want to export data in the GraphQL mutation request, as follows:

```graphql
mutation {
  export(input: {
    format: "rdf"
    destination: "<absolute-path-to-your-export-dir>"
  }) {
    response {
      message
      code
    }
  }
}
```

### Export to an object store

{{% notice "note" %}}
This feature was introduced in [v20.11.0](https://github.com/dgraph-io/dgraph/releases/tag/v20.11.0).
{{% /notice %}}

You can export to an S3 or MinIO object store by specifying a URL in the `destination` input field.

#### Export to S3

```graphql
mutation {
  export(input: {
    destination: "s3://s3.<region>.amazonaws.com/<bucket-name>"
    accessKey: "<aws-access-key-id>"
    secretKey: "<aws-secret-access-key>"
  }) {
    response {
      message
      code
    }
  }
}
```

{{% notice "note" %}}
The Dgraph URL used for S3 is different than the AWS CLI tools with the `aws s3` command, which uses a shortened format: `s3://<bucket-name>`.
{{% /notice %}}


#### Export to MinIO

```graphql
mutation {
  export(input: {
    destination: "minio://<address>:9000/<bucket-name>"
    accessKey: "<minio-access-key>"
    secretKey: "<minio-secret-key>"
  }) {
    response {
      message
      code
    }
  }
}
```

#### Export to a MinIO gateway

You can use MinIO as a gateway to other object stores, such as [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/) or [Google Cloud Storage](https://cloud.google.com/storage).  You can use the above MinIO GraphQL mutation with MinIO configured as a gateway.

##### Azure Blob Storage

You can use [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/) through the [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html).  You need to configure a [storage account](https://docs.microsoft.com/azure/storage/common/storage-account-overview) and a Blob [container](https://docs.microsoft.com/azure/storage/blobs/storage-blobs-introduction#containers) to organize the blobs. The name of the blob container is what you use for `<bucket-name>` when specifying the `destination` in the GraphQL mutation.

For MinIO configuration, you will need to [retrieve storage accounts keys](https://docs.microsoft.com/azure/storage/common/storage-account-keys-manage). The [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html) will use `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` to correspond to Azure Storage Account `AccountName` and `AccountKey`.

Once you have the `AccountName` and `AccountKey`, you can access Azure Blob Storage locally using one of these methods:

*  Using [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html) with the MinIO Binary
   ```bash
   export MINIO_ACCESS_KEY="<AccountName>"
   export MINIO_SECRET_KEY="<AccountKey>"
   minio gateway azure
   ```
*  Using [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html) with Docker
   ```bash
   docker run --detach --rm --name gateway \
    --publish 9000:9000 \
    --env MINIO_ACCESS_KEY="<AccountName>" \
    --env MINIO_SECRET_KEY="<AccountKey>" \
    minio/minio gateway azure
   ```
 * Using [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html) with the [MinIO Helm chart](https://github.com/minio/charts) for Kubernetes:
   ```bash
   helm repo add minio https://helm.min.io/
   helm install my-gateway minio/minio \
     --set accessKey="<AccountName>",secretKey="<AccountKey>" \
     --set azuregateway.enabled=true
   ```

##### Google Cloud Storage

You can use [Google Cloud Storage](https://cloud.google.com/storage) through the [MinIO GCS Gateway](https://docs.min.io/docs/minio-gateway-for-gcs.html).  You will need to create [storage buckets](https://cloud.google.com/storage/docs/creating-buckets), create a Service Account key for GCS and get a credentials file.  See [Create a Service Account key](https://github.com/minio/minio/blob/master/docs/gateway/gcs.md#11-create-a-service-account-ey-for-gcs-and-get-the-credentials-file) for further information.

Once you have a `credentials.json`, you can access GCS locally using one of these methods:

*  Using [MinIO GCS Gateway](https://docs.min.io/docs/minio-gateway-for-gcs.html) with the MinIO Binary
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   export MINIO_ACCESS_KEY="<minio-access-key>"
   export MINIO_SECRET_KEY="<minio-secret-key>"
   minio gateway gcs "<project-id>"
   ```
*  Using [MinIO GCS Gateway](https://docs.min.io/docs/minio-gateway-for-gcs.html) with Docker
   ```bash
   docker run --detach --rm --name gateway \
     --publish 9000:9000  \
     --volume "</path/to/credentials.json>":/credentials.json \
     --env GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
     --env MINIO_ACCESS_KEY="<minio-access-key>" \
     --env MINIO_SECRET_KEY="<minio-secret-key>" \
     minio/minio gateway gcs "<project-id>"
   ```
*  Using [MinIO GCS Gateway](https://docs.min.io/docs/minio-gateway-for-gcs.html) with the [MinIO Helm chart](https://github.com/minio/charts) for Kubernetes:
   ```bash
   ## create MinIO Helm config
   cat <<-EOF > myvalues.yaml
   accessKey: <minio-access-key>
   secretKey: <minio-secret-key>

   gcsgateway:
     enabled: true
     projectId: <project-id>
     gcsKeyJson: |
   $(IFS='\n'; while read -r LINE; do printf '    %s\n' "$LINE"; done < "</path/to/credentials.json>")
   EOF

   ## deploy MinIO GCS Gateway
   helm repo add minio https://helm.min.io/
   helm install my-gateway minio/minio \
     --values myvalues.yaml
   ```

#### Disable HTTPS for exports to S3 and Minio

By default, Dgraph assumes the destination bucket is using HTTPS. If that is not the case, the export will fail. To export to a bucket using HTTP (insecure), set the query parameter `secure=false` with the destination endpoint in the destination field:

```graphql
mutation {
  export(input: {
    destination: "minio://<address>:9000/<bucket-name>?secure=false"
    accessKey: "<minio-access-key>"
    secretKey: "<minio-secret-key>"
  }) {
    response {
      message
      code
    }
  }
}
```

#### Use anonymous credentials

If exporting to S3 or MinIO where credentials are not required, you can set `anonymous` to true.

```graphql
mutation {
  export(input: {
    destination: "s3://s3.<region>.amazonaws.com/<bucket-name>"
    anonymous: true
  }) {
    response {
      message
      code
    }
  }
}
```

### Encrypt exports

Export is available wherever an Alpha is running. To encrypt an export, the Alpha must be configured with the `--encryption key-file=value`.

{{% notice "note" %}}
The `--encryption key-file` was used for [Encryption at Rest]({{< relref "enterprise-features/encryption-at-rest" >}}) and will now also be used for encrypted exports.
{{% /notice %}}

### Use `curl` to trigger an export

This is an example of how you can use `curl` to trigger an export.

  1. Create GraphQL file for the desired mutation:
     ```bash
     cat <<-EOF > export.graphql
     mutation {
       export(input: {
         destination: "s3://s3.<region>.amazonaws.com/<bucket-name>"
         accessKey: "<aws-access-key-id>"
         secretKey: "<aws-secret-access-key>"
       }) {
         response {
           message
           code
         }
       }
     }
     EOF
     ```
  2. Trigger an export with `curl`
     ```bash
     curl http://localhost:8080/admin --silent --request POST \
       --header "Content-Type: application/graphql" \
       --upload-file export.graphql
     ```


## Shut down database

A clean exit of a single Dgraph node is initiated by running the following GraphQL mutation on /admin endpoint.
{{% notice "warning" %}}This won't work if called from outside the server where Dgraph is running.
You can specify a list or range of whitelisted IP addresses from which shutdown or other admin operations
can be initiated using the `--security` superflag's `whitelist` option on `dgraph alpha`.
{{% /notice %}}

```graphql
mutation {
  shutdown {
    response {
      message
      code
    }
  }
}
```

This stops the Alpha on which the command is executed and not the entire cluster.

## Delete database

Individual triples, patterns of triples and predicates can be deleted as described in the [DQL docs]({{< relref "mutations/delete.md" >}}).

To drop all data, you could send a `DropAll` request via `/alter` endpoint.

Alternatively, you could:

* [Shutdown Dgraph]({{< relref "#shut-down-database" >}}) and wait for all writes to complete,
* Delete (maybe do an export first) the `p` and `w` directories, then
* Restart Dgraph.

## Upgrade database

Doing periodic exports is always a good idea. This is particularly useful if you wish to upgrade Dgraph or reconfigure the sharding of a cluster. The following are the right steps to safely export and restart.

1. Start an [export]({{< relref "#export-database">}})
2. Ensure it is successful
3. [Shutdown Dgraph]({{< relref "#shut-down-database" >}}) and wait for all writes to complete
4. Start a new Dgraph cluster using new data directories (this can be done by passing empty directories to the options `-p` and `-w` for Alphas and `-w` for Zeros)
5. Reload the data via [bulk loader]({{< relref "deploy/fast-data-loading/bulk-loader.md" >}})
6. Verify the correctness of the new Dgraph cluster. If all looks good, you can delete the old directories (export serves as an insurance)

These steps are necessary because Dgraph's underlying data format could have changed, and reloading the export avoids encoding incompatibilities.

Blue-green deployment is a common approach to minimize downtime during the upgrade process.
This approach involves switching your application to read-only mode. To make sure that no mutations are executed during the maintenance window you can
do a rolling restart of all your Alpha using the option `--mutations disallow` when you restart the Alpha nodes. This will ensure the cluster is in read-only mode.

At this point your application can still read from the old cluster and you can perform the steps 4. and 5. described above.
When the new cluster (that uses the upgraded version of Dgraph) is up and running, you can point your application to it, and shutdown the old cluster.

### Upgrade from v1.2.2 to v20.03.0 for Enterprise customers

<!-- TODO: Redirect(s) -->
1. Use [binary backup]({{< relref "enterprise-features/binary-backups.md">}}) to export data from old cluster
2. Ensure it is successful
3. [Shutdown Dgraph]({{< relref "#shut-down-database" >}}) and wait for all writes to complete
4. Upgrade `dgraph` binary to `v20.03.0`
5. [Restore]({{< relref "enterprise-features/binary-backups.md#restore-from-backup">}}) from the backups using upgraded `dgraph` binary
6. Start a new Dgraph cluster using the restored data directories
7. Upgrade ACL data using the following command:

```sh
dgraph upgrade --acl -a localhost:9080 -u groot -p password
```

### Upgrade from v20.03.0 to v20.07.0 for Enterprise customers

1. Use [binary backup]({{< relref "enterprise-features/binary-backups.md">}}) to export data from old cluster
2. Ensure it is successful
3. [Shutdown Dgraph]({{< relref "#shut-down-database" >}}) and wait for all writes to complete
4. Upgrade `dgraph` binary to `v20.07.0`
5. [Restore]({{< relref "enterprise-features/binary-backups.md#restore-from-backup">}}) from the backups using upgraded `dgraph` binary
6. Start a new Dgraph cluster using the restored data directories
7. Upgrade ACL data using the following command:
    ```sh
    dgraph upgrade --acl -a localhost:9080 -u groot -p password -f v20.03.0 -t v20.07.0
    ```
    This is required because previously the type-names `User`, `Group` and `Rule` were used by ACL.
    They have now been renamed as `dgraph.type.User`, `dgraph.type.Group` and `dgraph.type.Rule`, to
    keep them in Dgraph's internal namespace. This upgrade just changes the type-names for the ACL
    nodes to the new type-names.

    You can use `--dry-run` option in `dgraph upgrade` command to see a dry run of what the upgrade
    command will do.
8. If you have types or predicates in your schema whose names start with `dgraph.`, then
you would need to manually alter schema to change their names to something else which isn't
prefixed with `dgraph.`, and also do mutations to change the value of `dgraph.type` edge to the
new type name and copy data from old predicate name to new predicate name for all the nodes which
are affected. Then, you can drop the old types and predicates from DB.

{{% notice "note" %}}
If you are upgrading from v1.0, please make sure you follow the schema migration steps described in [this section]({{< relref "/migration/migrate-dgraph-1-1.md" >}}).
{{% /notice %}}

### Upgrade from v20.11.0 to v21.03.0 for Enterprise customers

1. Use [binary backup]({{< relref "enterprise-features/binary-backups.md">}}) to export data from the old cluster
2. Ensure it is successful
3. [Shutdown Dgraph]({{< relref "#shut-down-database" >}}) and wait for all writes to complete
4. Upgrade `dgraph` binary to `v21.03.0`
5. [Restore]({{< relref "enterprise-features/binary-backups.md#restore-from-backup">}}) from the backups using the upgraded `dgraph` binary
6. Start a new Dgraph cluster using the restored data directories
7. Upgrade the CORS and persisted queries. To upgrade an ACL cluster use:
    ```sh
    dgraph upgrade --from v20.11.0 --to v21.03.0 --user groot --password password --alpha http://localhost:9080 --alpha-http http://localhost:8080 --deleteOld
    ```
    To upgrade a non-ACL cluster use:
    ```sh
    dgraph upgrade --from v20.11.0 --to v21.03.0 --alpha http://localhost:9080 --alpha-http http://localhost:8080 --deleteOld
    ```
    This is required because previously CORS information was stored in `dgraph.cors` predicate which has
    now been moved to be a part of the GraphQL schema. Also, the format of persisted queries has changed.
    Some of the internal deprecated predicates will be removed by this change.

    You can use `--dry-run` option in `dgraph upgrade` command to see a dry run of what the upgrade
    command will do.

{{% notice "note" %}}
The above steps are valid for migration from a cluster in `v20.11` to a single-tenant cluster in `v21.03`, 
as backup and restore are cluster-wide operations and a single namespace cannot be restored in a multi-tenant cluster.
{{% /notice %}}

## Post Installation

Now that Dgraph is up and running, to understand how to add and query data to Dgraph, follow [Query Language Spec](/query-language). Also, have a look at [Frequently asked questions](/faq).
