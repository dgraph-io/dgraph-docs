+++
title = "API keys"
weight = 2   
[menu.main]
    parent = "cloud-admin"
+++

Client applications accessing the Dgraph Cloud cluster endpoints
- `/query`
- `/mutate`
- `/commit`

must present a valid **client** or **admin** **API key** in the ``Dg-Auth`` or ``X-Auth-Token`` header of every HTTP request.

Client applications accessing the Dgraph Cloud cluster endpoints
- `/admin`
- `/admin/slash`
- `/alter`

must present a valid **admin API key** in the ``Dg-Auth`` or ``X-Auth-Token``  header of every HTTP request.

Client applications accessing the Dgraph Cloud cluster endpoint
- `/graphql`

with [anonymous access]({{< relref "anonymous-access.md">}}) not set on the requested operation, must present a valid **client** or **admin API key** in the ``Dg-Auth`` or ``X-Auth-Token``  header of every HTTP request.


**Client API keys** can only be used to perform query, mutation, and commit operations.
**Admin API keys** can be used to perform both client operations and admin operations like drop data, destroy backend, and update schema.


 ## Generate a new API
 To generate a new API key :
1. Go to the [Settings](https://cloud.dgraph.io/_/settings) section of Dgraph Cloud console.
2. Access ``[API Keys](https://cloud.dgraph.io/_/settings?tab=api-keys)`` tab.
3. Click <kbd>Create New</kbd> button.
4. Give the key a name, and select **Client** or **Admin** type and click <kbd>Create</kbd>
5. Copy the key in a safe place, it will not be accessible once you leave the page.

