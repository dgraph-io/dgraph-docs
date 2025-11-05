+++
title = "Export data"
type = "docs"
keywords = "export, data, self hosted"
weight = 7
[menu.main]
    identifier = "exportdata"
    parent = "migration"
+++

As an `Administrator` you can export data from Dgraph to an an object store, NFS, or a file path.

When you export data, three files are generated:

* `g01.gql_schema.gz`: The GraphQL schema file. This file can be imported using the Schema APIs
* `g01.json.gz` or `g01.rdf.gz`: the data from your instance in JSON format or RDF format. By default, Dgraph exports data in RDF format.
* `g01.schema.gz`: This file is the internal Dgraph schema. If you have set up the Dgraph Cloud instance with a GraphQL schema, then you can ignore this file.

## Export data using  the GraphQL admin endpoint

You can export the entire data by executing a GraphQL mutation on the `/admin` endpoint of any Alpha node.

**Before you begin**:

*  Ensure that there is sufficient space on disk to store the export. Each Dgraph Alpha leader for a group writes output as a gzipped file to the export directory specified through the `--export` flag (defaults to an **export** directory). If any of the groups fail because of insufficient space on the disk, the entire export process is considered failed and an error is returned.

* Make a note of the export directories of the Alpha server nodes. For more information about configuring the Dgraph Alpha server, see [Config]({{< relref "cli/config.md" >}}).

This mutation triggers the export from each of the Alpha leader for a group. Depending on the Dgraph configuration several files are exported. It is recommended that you copy the files from the Alpha server nodes to a safe place when the export is complete.

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
The export data of the group:

* in the Alpha instance is stored in the Alpha.
* in every other group is stored in the Alpha leader of that group.

You need to retrieve the right export files from the Alpha instances in the cluster. Dgraph does not copy all files to the Alpha that initiated the export.

When the export is complete a response similar to this appears:

```
{"data":{
  "export":{
    "response":{
      "message":"Export completed.",
      "code":"Success"
      }
    }
  },
  "extensions":{
    "tracing":{
      "version":1,
      "startTime":"2022-12-14T07:39:51.061712416Z","endTime":"2022-12-14T07:39:51.129431494Z",
      "duration":67719080
      }
    }
  }
```

## Export data format

By default, Dgraph exports data in RDF format. Replace `<FORMAT>`with `json` or `rdf` in this GraphQL mutation:

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

## Export to NFS or a file path

You can override the default folder path by adding the `destination` input field to the directory where you want to export data. Replace `<PATH>` in this GraphQL mutation with the absolute path of the directory to export data.

```graphql
mutation {
  export(input: {
    format: "<FORMAT>"
    destination: "<PATH>"
  }) {
    response {
      message
      code
    }
  }
}
```

## Export to an object store
You can export to an AWS S3, Azure Blob Storage or Google Cloud Storage.

### Example mutation to export to AWS S3

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


### Example mutation to export to MinIO

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

## Export to a MinIO gateway

You can use MinIO as a gateway to other object stores, such as [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/) or [Google Cloud Storage](https://cloud.google.com/storage).

### Azure Blob Storage

You can use [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/) through the [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html).

**Before you begin**:

*  Configure a [storage account](https://docs.microsoft.com/azure/storage/common/storage-account-overview) and a Blob [container](https://docs.microsoft.com/azure/storage/blobs/storage-blobs-introduction#containers) to organize the blobs.
*  Make a note the name of the blob container. It is the `<bucket-name>` when specifying the `destination` in the GraphQL mutation.
* [Retrieve storage accounts keys](https://docs.microsoft.com/azure/storage/common/storage-account-keys-manage) to configure MinIO. Because, [MinIO Azure Gateway](https://docs.min.io/docs/minio-gateway-for-azure.html) uses `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` to correspond to Azure Storage Account `AccountName` and `AccountKey`.

You can access Azure Blob Storage locally using one of these methods:

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
You can use the [MinIO GraphQL mutation]({{< relref "export-data.md#example-mutation-to-export-to-minio" >}}) with MinIO configured as a gateway.

### Google Cloud Storage

You can use [Google Cloud Storage](https://cloud.google.com/storage) through the [MinIO GCS Gateway](https://docs.min.io/docs/minio-gateway-for-gcs.html).

**Before you begin**:
*  Create [storage buckets](https://cloud.google.com/storage/docs/creating-buckets)
*  Create a Service Account key for GCS and get a credentials file. For more information, see [Create a Service Account key](https://github.com/minio/minio/blob/master/docs/gateway/gcs.md#11-create-a-service-account-ey-for-gcs-and-get-the-credentials-file).

When you have a `credentials.json`, you can access GCS locally using one of these methods:

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
You can use the [MinIO GraphQL mutation]({{< relref "export-data.md#example-mutation-to-export-to-minio" >}}) with MinIO configured as a gateway.

## Disable HTTPS for exports to S3 and Minio

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

## Use anonymous credentials

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

## Encrypt exports

Export is available wherever an Alpha is running. To encrypt an export, the Alpha must be configured with the `--encryption key-file=value`.

{{% notice "note" %}}
The `--encryption key-file` was used for [Encryption at Rest]({{< relref "encryption-at-rest" >}}) and will now also be used for encrypted exports.
{{% /notice %}}

## Use `curl` to trigger an export

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
