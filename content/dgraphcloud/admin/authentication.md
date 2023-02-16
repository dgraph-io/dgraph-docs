+++
title = "Authentication"
weight = 2   
[menu.main]
    parent = "cloud-admin"
+++

Administrating your Dgraph Cloud using the `/query`, `/mutate`, `/commit`, `/admin`, `/admin/slash`, or `/alter` endpoints on Dgraph Cloud. Also, bypassing Anonymous Access restrictions on the `/graphql` endpoint requires an API key. You can generate a new API key from Dgraph Cloud by selecting the ["Settings" button](https://cloud.dgraph.io/_/settings) from the sidebar, and then clicking the **Add API Key** button. Keep your API key safe, it will not be accessible once you leave the page.

![Dgraph Cloud: Add an API Key](/images/cloud-4.png)

There are two types of API keys: *client* and *admin*.

- **Client API keys** can only be used to perform query, mutation, and commit operations.
- **Admin API keys** can be used to perform both client operations and admin operations like drop data, destroy backend, and update schema.

{{% notice "note" %}}
Either Client API keys or Admin API keys can be used to bypass [Anonymous Access](/security) restrictions.
{{% /notice %}}

![Dgraph Cloud: Select API Key Role](/images/cloud-5.png)
<br>
<br>
All admin API requests must be authenticated by passing the API key as the 'Dg-Auth' header to every HTTP request. You can verify that your API key works by using the following HTTP example.

```
curl 'https://<your-backend>/admin' \
  -H 'Dg-Auth: <your-api-key>' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"{ getGQLSchema { schema } }"}'
```
