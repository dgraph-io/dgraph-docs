+++
title = "Schema"
weight = 2
[menu.main]
    parent = "cloud-api"
    identifier = "schema"
+++

## Get Schema

Fetch the schema from your backend.

### Cloud Endpoint

```bash
https://${DEPLOYMENT_URL}/admin
```

### API Command

```graphql
{
  getGQLSchema {
    schema
    generatedSchema
  }
}
```

### Example

{{% tabs %}} {{< tab "request" >}}
```bash
#!/usr/bin/env bash

DEPLOYMENT_URL="polished-violet.us-east-1.aws.cloud.dgraph.io"
DEPLOYMENT_JWT="<deployment-jwt>"

curl "https://${DEPLOYMENT_URL}/admin" \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: ${DEPLOYMENT_JWT}" \
  --data-binary '{"query":"{\n getGQLSchema {\n schema\n generatedSchema\n }\n}","variables":{}}' \
  --compressed
```
{{< /tab >}} 

{{% tab "response" %}}
```json
{
  "data": {
    "getGQLSchema": {
      "schema": "type Person { name: String! }",
      "generatedSchema": "<very-long-string>"
    }
  },
  "extensions": {
    "tracing": {
      "version": 1,
      "startTime": "2021-04-15T19:58:33.412544782Z",
      "endTime": "2021-04-15T19:58:33.412851891Z",
      "duration": 307129,
      "execution": {
        "resolvers": [
          {
            "path": ["getGQLSchema"],
            "parentType": "Query",
            "fieldName": "getGQLSchema",
            "returnType": "GQLSchema",
            "startOffset": 115909,
            "duration": 159961,
            "dgraph": [
              {
                "label": "query",
                "startOffset": 118110,
                "duration": 53165
              }
            ]
          }
        ]
      }
    }
  }
}
```
{{% /tab %}} {{% /tabs %}}

## Update Schema

Update the schema in your backend.

### Cloud Endpoint

```bash
https://${DEPLOYMENT_URL}/admin
```

### API Command

```graphql
mutation($schema: String!) {
  updateGQLSchema(input: { set: { schema: $schema } }) {
    gqlSchema {
      schema
    }
  }
}
```

**Arguments**

- `schema`: your desired schema string in GraphQL format

### Example

{{% tabs %}} {{< tab "request" >}}
```bash
#!/usr/bin/env bash

DEPLOYMENT_URL="polished-violet.us-east-1.aws.cloud.dgraph.io"
DEPLOYMENT_JWT="<deployment-jwt>"

curl "https://${DEPLOYMENT_URL}/admin" \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: ${DEPLOYMENT_JWT}" \
  --data-binary '{"query":"mutation($sch: String!) {\n updateGQLSchema(input: { set: { schema: $sch } })\n {\n gqlSchema {\n schema\n }\n }\n}","variables":{"sch": "type Person { name: String! }"}}' \
  --compressed
```
{{< /tab >}} 

{{% tab "response" %}}
```json
{
  "data": {
    "updateGQLSchema": {
      "gqlSchema": {
        "schema": "type Person { name: String! }"
      }
    }
  },
  "extensions": {
    "tracing": {
      "version": 1,
      "startTime": "2021-04-15T19:53:16.283198298Z",
      "endTime": "2021-04-15T19:53:16.286478152Z",
      "duration": 3279886
    }
  }
}
```
{{% /tab %}} {{% /tabs %}}
