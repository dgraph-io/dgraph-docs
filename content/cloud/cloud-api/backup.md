+++
title = "Backup"
weight = 3
[menu.main]
    parent = "cloud-api"
    identifier = "cloud-backup"
+++

{{% notice "note" %}}
Backup feature is only available for Dedicated Instances. This feature is not available for the Free and Shared Instances. 
{{% /notice %}}

## Periodic Backups

Periodic Backups are created at a given schedule that by default is:
- Full Backup every week 
- Incremental Backups every 4 hours 

You can trigger the Backup on-demand directelly from your Dgraph Cloud Dashboard, simply go to Admin>Setting>Backups and click on "Create Backup" button on the top left. 

In case you would like to change your default Backup schedule please contact us and we will be happy to set you up. 

## List Backups

List all backups of the current backend.

### Cloud Endpoint

```bash
https://${DEPLOYMENT_URL}/admin/slash
```

### API Command

```graphql
query {
    listBackups {
        response {
            type
            backupNum
            folder
            timestamp
        }, errors {
            message
        }
    }
}
```

### Example

{{% tabs %}} {{< tab "request" >}}
```bash
#!/usr/bin/env bash

DEPLOYMENT_URL="polished-violet.us-east-1.aws.cloud.dgraph.io"
DEPLOYMENT_JWT="<deployment-jwt>"

curl "https://${DEPLOYMENT_URL}/admin/slash" \
  -H 'Content-Type: application/json' \
  -H "X-Auth-Token: ${DEPLOYMENT_JWT}" \
  --data-binary '{"query":"{\n listBackups {\n response {\n type\n backupNum\n folder\n timestamp\n }, errors {\n message\n }\n} \n}","variables":{}}' \
  --compressed
```
{{< /tab >}} 

{{% tab "response" %}}
```json
{
  "data": {
    "listBackups": {
      "errors": [],
      "response": [
        [
          {
            "backupNum": 1,
            "folder": "2021-15",
            "timestamp": "2021-04-15T18:00:58+0000",
            "type": "full"
          },
          {
            "backupNum": 2,
            "folder": "2021-15",
            "timestamp": "2021-04-15T18:04:29+0000",
            "type": "incremental"
          }
        ]
      ]
    }
  }
}
```
{{% /tab %}} {{% /tabs %}}

## Export Data

Export data from your backend.

### Cloud Endpoint

```bash
https://${DEPLOYMENT_URL}/admin/slash
```

### API Command

```graphql
mutation {
  export {
    signedUrls
  }
}
```

### Example

{{% tabs %}} {{< tab "request" >}}
```bash
#!/usr/bin/env bash

DEPLOYMENT_URL="polished-violet.us-east-1.aws.cloud.dgraph.io"
DEPLOYMENT_JWT="<deployment-jwt>"

curl "https://${DEPLOYMENT_URL}/admin/slash" \
  -H 'Content-Type: application/json' \
  -H "X-Auth-Token: ${DEPLOYMENT_JWT}" \
  --data-binary '{"query":"mutation {\n export {\n signedUrls\n }\n }","variables":{}}' \
  --compressed
```
{{< /tab >}} 

{{% tab "response" %}}
```json
{
  "data": {
    "export": {
      "signedUrls": [
        "<export-url>",
        "<export-url>",
        "<export-url>"
      ]
    }
  }
}
```
{{% /tab %}} {{% /tabs %}}

## Import Data

Import your data back using Dgraph [Live Loader]({{< relref "cloud/admin/import-export.md#importing-data-with-live-loader" >}}) (requires Docker).

### Shell Command

Live loader command (via Docker):

```sh
docker run -it --rm -v /tmp/file:/tmp/g01.json.gz dgraph/dgraph:v21.03-slash \
  dgraph live --slash_grpc_endpoint=${DEPLOYMENT_URL} -f /tmp/g01.json.gz -t ${DEPLOYMENT_JWT}
```

### Example

{{% tabs %}} {{< tab "request" >}}
```bash
#!/usr/bin/env bash

DEPLOYMENT_URL="lively-dream.grpc.us-east-1.aws.cloud.dgraph.io"
DEPLOYMENT_JWT="<deployment-jwt>"

docker run -it --rm -v /users/dgraph/downloads:/tmp dgraph/dgraph:v21.03-slash \
  dgraph live --slash_grpc_endpoint=${DEPLOYMENT_URL}:443 -f /tmp/1million.rdf.gz -t ${DEPLOYMENT_JWT}
```
{{< /tab >}} 

{{% tab "response" %}}
```json
```
{{% /tab %}} {{% /tabs %}}
