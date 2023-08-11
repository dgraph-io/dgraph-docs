+++
title = "Export data from Dgraph"
keywords = "export, data, self hosted"
[menu.main]
    parent = "exportdata"
    weight = 3
+++

As an `Administrator` you can export data on all nodes, configure the Alpha server, specify the export format, export to an object store, disable HTTPS for exports, and encrypt exports

## Export data using  the GraphQL admin endpoint

You can export the entire data by executing a GraphQL mutation on the `/admin` endpoint of any Alpha node.

**Before you begin**:

*  Ensure that there is sufficient space on disk to store the export. Each Dgraph Alpha leader for a group writes output as a gzipped file to the export directory specified through the `--export` flag (defaults to an **export** directory). If any of the groups fail because of insufficient space on the disk, the entire export process is considered failed and an error is returned.

* Make a note of the export directories of the Alpha server nodes. For more information about configuring the Dgraph Alpha server, see [Config]({{< relref "config" >}}).

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
The `--encryption key-file` was used for [Encryption at Rest]({{< relref "enterprise-features/encryption-at-rest" >}}) and will now also be used for encrypted exports.
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
