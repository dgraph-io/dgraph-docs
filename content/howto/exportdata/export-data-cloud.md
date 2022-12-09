+++
title = "Export data from Dgraph Cloud"
keywords = "export, data, cloud"
[menu.main]
    parent = "exportdata"
    weight = 2
+++

As an `Administrator` from a multi-tenancy feature enabled Dgraph Cloud instance you can export data across the cluster, or a specific namespace depending on the type of administative previleges you have.

## Before you begin

*  Generate API Key for authentication 
*  

### Exporting data from Dgraph Cloud using the console

1. In the `Admin` section of the Dgraph Cloud console, go to `Settings`. 
1. In the `Exports` tab, click `Create Export`.
1. In the `New export` dialog, select the format you want to export.
1. Click  `Create`.

Depending on the format that you chose to create an export, three files are generated.

{{% notice "note" %}}
Ensure that you download these files as soon as possible because the links to download these files expire after 48 hours from the time they were generated..
{{% /notice %}}


### Exporting data from Dgraph Cloud using a GraphQL client

1. Make a note of the GraphQL `<GRAPHQL_ENDPOINT>` for the instance from `Overview` in the Dgraph Cloud console.
1. Authenticate the `admin` API requests by adding the `<APIKEY>` as the `Dg-Auth` header to every HTTP request.
1. To export data you need to send autheticated request to the `admin` endpoint *`<GRAPHQL_ENDPOINT>`/admin/slash*.
1. Export data in JSON or RDF `<FORMAT>` using this mutation:

    ```graphql
    mutation {
      export(input: { format: "<FORMAT>" })
        response { code message }
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
1. Make a note of the `<EXPORT_ID>` and the `<TASK_ID>`.

1. To get the status of export and the signed URLs to download the exported files, use this mutation:
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

   Depending on the format that you chose to create an export, three files are generated.
   
{{% notice "note" %}}
Ensure that you download these files as soon as possible because the signed URLs to download these files expire after 48 hours from the time they were generated. You can use `curl -O <SIGNED_URL>` to download the files to the current directory.
{{% /notice %}}   






   