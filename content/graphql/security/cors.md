+++
title = "Restrict origins"
[menu.main]
  identifier = "authorization-cors"
  parent = "gql-auth"
  weight = 6
+++

To restrict origins of HTTP requests : 

1. Add lines starting with `# Dgraph.Allow-Origin` at the end of your GraphQL schema specifying the origins allowed.
2. Deploy the GraphQL schema either with a [schema update]({{< relref "graphql/admin.md#using-updategqlschema-to-add-or-modify-a-schema" >}}) or via the Cloud console's [Schema](https://cloud.dgraph.io/_/schema) page.

For example, the following will restrict all origins except the ones specified.

```
# Dgraph.Allow-Origin "https://example.com"
# Dgraph.Allow-Origin "https://www.example.com"
```


`https://cloud.dgraph.io` is always allowed so that ``API explorer``, in Dgraph Cloud console, continues to work.

{{% notice "note" %}}
- CORS restrictions only apply to browsers.
- By default, ``/graphql`` endpoint does not limit the request origin (`Access-Control-Allow-Origin: *`).
{{% /notice %}}