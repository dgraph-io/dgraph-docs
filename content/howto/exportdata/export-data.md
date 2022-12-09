+++
title = "Export data from Dgraph"
keywords = "export, data, self hosted"
[menu.main]
    parent = "exportdata"
    weight = 3
+++

As an `Administrator` you can export all nodes by executing this GraphQL mutation on the `/admin` endpoint of an Alpha node ( `localhost:8080/admin`) using any GraphQL client.

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

By default, Dgraph exports data in RDF format. Replace `<FORMAT>`with `json` or `rdf` in this GraphQL mutaion:

```graphql
mutation {
  export(input: { format: "<FORMAT>" }) {
    response {
      message
      code
    }
  }
}
```

### Export to NFS or a file path

You can override the default folder path by adding the `destination` input field to the directory where you want to export data. Replace `<PATH>` in this GraphQL mutaion with the absolute path of the directory to export data.

```graphql
mutation {
  export(input: {
    format: "<FORMAT>"
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
You can export to an S3 or MinIO object store by specifying a URL in the `destination` input field.
Use this GraphQL mutation to export data to an object store:

#### Example mutation to export to AWS S3

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


#### Example mutation to export to MinIO

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

### Export to a MinIO gateway

You can use MinIO as a gateway to other object stores, such as [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/) or [Google Cloud Storage](https://cloud.google.com/storage).  You can use the above MinIO GraphQL mutation with MinIO configured as a gateway.

#### Azure Blob Storage

You can use [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/) through the [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html).  You need to configure a [storage account](https://docs.microsoft.com/azure/storage/common/storage-account-overview) and a Blob [container](https://docs.microsoft.com/azure/storage/blobs/storage-blobs-introduction#containers) to organize the blobs. The name of the blob container is what you use for `<bucket-name>` when specifying the `destination` in the GraphQL mutation.

For MinIO configuration, you need to [retrieve storage accounts keys](https://docs.microsoft.com/azure/storage/common/storage-account-keys-manage). The [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html) uses `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` to correspond to Azure Storage Account `AccountName` and `AccountKey`.

When you have the `AccountName` and `AccountKey`, you can access Azure Blob Storage locally using one of these methods:

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

#### Google Cloud Storage

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

### Disable HTTPS for exports to S3 and Minio

By default, Dgraph assumes the destination bucket is using HTTPS. If that is not the case, the export fails. To export to a bucket using HTTP (insecure), set the query parameter `secure=false` with the destination endpoint in the `destination` field:

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

### Use anonymous credentials

When exporting to S3 or MinIO where credentials are not required, can set `anonymous` to true.

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
