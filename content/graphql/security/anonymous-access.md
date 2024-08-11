+++
title = "Anonymous Access"
weight = 2
[menu.main]
    parent = "gql-auth"
+++

{{% notice "note" %}}
Controlling **anonymous access** of the GraphQL endpoint is only available in Dgraph Cloud.
{{% /notice %}}


## Turn Anonymous Access On and Off

To turn ``/graphql`` endpoint anonymous access off  
1. Go to the [Schema](https://cloud.dgraph.io/_/schema) section of Dgraph Cloud console.
2. Open the  [Access](https://cloud.dgraph.io/_/schema?tab=anon-access) tab.
3. Set ``Anonymous Access`` toggle to ``On`` or ``Off``

With **Anonymous Access** turned ``off``, any client accessing the ``/graphql`` endpoint must pass  a valid client or admin [API Key]({{< relref "cloud/admin/authentication.md" >}}) in ``DG-Auth`` or ``X-Auth-Token`` header.

With **Anonymous Access** turned ``on`` (Default configuration), you need to further define the permission per ``type`` defined in your GraphQL Schema. 
 
 ## Edit GraphQL type operations access permissions
 have a button to "Edit Permissions"
When **Anonymous Access** is ``on``, any newly deployed type will have ``read`` and ``write`` permissions for anonymous users.

To control the anonymous access to operations :

1. Open the  [Access](https://cloud.dgraph.io/_/schema?tab=anon-access) tab in the [Schema](https://cloud.dgraph.io/_/schema) section.
2. Click on ``Edit Permission``
3. For every Type defined in your GraphQL schema, Edit Permissions will show check boxes to enable Anonymous Access to Read and Write.
-- Check ``Read`` to allow anonymous clients to access the `get<Type>` and `query<Type>` operations. 
-- Check ``Write`` to allow anonymous clients to access the `add<Type>`, `update<Type>`, and `delete<Type>` operations.


{{% notice "note" %}}
Anonymous Access works as an access control security one level above the [RBAC (Role Based Access Control)]({{< relref "auth.md" >}}).
{{% /notice %}}


Permission settings only applies to the parent type operations: it is still possible to read/write data of a type that has been set with no read/write permissions if a `parent` type is granted read/write access to anonymous clients.

Consider the following Schema:

```graphql
type User {
  id: ID
  name: String!
  posts: [Post] @hasInverse(field: "author")
}
type Post {
  id: ID
  title: String!
  author: User
}
```

If the Anonymous Access was granted Read and Write for Post but not granted Read and Write for User, it would be possible still to perform the following operation which creates a new ``User``.

```graphql
mutation addPost {
  addPost(input: [{
    title: "New Post Title" @search(by: [hash])
    author: { name: "New User Name" } # creates a new User node.
  }]) {
    numUids
  }
}
```






