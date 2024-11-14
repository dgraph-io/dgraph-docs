+++
title = "Export data from Dgraph Cloud"
keywords = "export, data, cloud"
[menu.main]
    parent = "exportdata"
    weight = 2
+++

As an `Administrator` you can export data from a Dgraph Cloud shared instance or dedicated instance. On a dedicated instance with multi-tenancy feature enabled you can export data across the cluster, or a specific namespace depending on the type of administrative privileges you have.

## Exporting data from Dgraph Cloud using the console

1. In the `Admin` section of the Dgraph Cloud console, go to `Settings`. 
1. In the `Exports` tab, click `Create Export`.
1. In the `New export` dialog, select the format you want to export.
1. Click  `Create`.

Depending on the format that you chose to create an export, three files are generated.

{{% notice "note" %}}
Ensure that you download these files as soon as possible because the links to download these files expire after 48 hours from the time they were generated.
{{% /notice %}}



### Exporting data from Dgraph Cloud using a GraphQL client

1. Generate API Key for authentication.
1. Make a note of the GraphQL endpoint for the instance from `Overview` in the Dgraph Cloud console. Replace `/graphql` with `/admin/slash`in the GraphQL endpoint to get the `<ADMIN_ENDPOINT>`.
1. Authenticate the `admin` API requests by adding the `<APIKEY>` as the `Dg-Auth` header to every HTTP request.
1. To export data you need to send authenticated request to `<ADMIN_ENDPOINT>`. 
1. Export data in JSON or RDF `<FORMAT>` using this mutation:

    ```graphql
    mutation {
      export(format:"<FORMAT>") {
        response {
          message
          code
        }
        exportId
        taskId
     }
    }
   ``` 
   A response similar to this appears:

   ```{
       "data": {
          "export":"exports/2011-12-08/0x18986fd-558223708",
          "response": {
             "code": "Success",
             "message": "Export queued with ID 0x9d2e13e8a"
          },
          "taskID": "0x9d2e13e8a"
       }
      }
   }
   ```
1. For running a namespace-specific export from a multi-tenant Dgraph cluster, an additional input parameter of `namespace: <NAMESPACE-ID>` must be provided to the `export` mutation. The "Namespaces" view in the Cloud console lists all of the Namespaces created along with their IDs.

    ```graphql
    mutation {
      export(format:"<FORMAT>", namespace:<NAMESPACE-ID>) {
        response {
          message
          code
        }
        exportId
        taskId
     }
    }
   ```

1. Make a note of the `<EXPORT_ID>` and the `<TASK_ID>`.

1. To get the status of export and the signed URLs to download the exported files, run the following GraphQL query:
   ```graphql
   query {
     exportStatus (
       exportId:"<EXPORT_ID>"
       taskId: "<TASK_ID>"
     ){
       kind
       lastUpdated
       signedUrls
       status
     }
   }
   ```
1. Use the `signedUrls` to download the exported files. 
   Depending on the format that you chose to create an export, three files are generated viz., one each for the data RDF/JSON file, the GraphQL schema and the DQL schema.
   
{{% notice "note" %}}
Ensure that you download these files as soon as possible because the signed URLs to download these files expire after 48 hours from the time they were generated. You can use `curl -O <SIGNED_URL>` to download the files to the current directory or access the links using a browser.
{{% /notice %}}   

### Exporting data from Dgraph Cloud programmatically

You can also export data from Dgraph Cloud programmatically using the Dgraph Cloud API. For more information, see [Cloud API documentation](https://dgraph.io/docs/cloud/cloud-api/backup/#export-data).



   
