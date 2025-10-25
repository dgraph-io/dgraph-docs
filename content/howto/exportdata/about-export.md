+++
title = "Export data"
type = "docs"
keywords = "export data,"
[menu.main]
    parent = "exportdata"
    weight = 1
+++

## Export

As an `Administrator` you can export data from [Dgraph Cloud]({{< relref "howto/exportdata/export-data-cloud" >}}), using the Cloud console, a GraphQL Client, or the Cloud API. You can also export data from your self-hosted [Dgraph instance]({{< relref "howto/exportdata/export-data" >}}) to NFS or a file path or to an object store.

When you export data, typically three files are generated:

* `g01.gql_schema.gz`: The GraphQL schema file. This file can be imported using the Schema APIs
* `g01.json.gz` or `g01.rdf.gz`: the data from your instance in JSON format or RDF format. By default, Dgraph exports data in RDF format.
* `g01.schema.gz`: This file is the internal Dgraph schema. If you have set up the Dgraph Cloud instance with a GraphQL schema, then you can ignore this file.