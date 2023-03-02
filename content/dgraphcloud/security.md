+++
title = "Securing Your GraphQL endpoint"
weight = 6
[menu.main]
    parent = "cloud"
+++

Here are a few tips for securing your Dgraph Cloud Backend

### Allowing Anonymous Access to your GraphQL Endpoint

To help secure your GraphQL API, Dgraph Cloud allows you to choose which GraphQL operations are available to end clients.

You can visit the [access tab on the schema page](https://cloud.dgraph.io/_/schema) and choose the operations that you want to allow/deny for anonymous users.

With Anonymous Access turned off, all GraphQL operations are restricted unless the client provides a valid [API Key]({{< relref "dgraphcloud/admin/authentication.md" >}}). With Anonymous Access turned on (Default configuration), you will have a button to "Edit Permissions"

In Edit Permissions, you will find options to turn on/off Anonymous Access to Lambda functions, custom Queries, and custom Mutations. For every Type defined in your GraphQL schema, Edit Permissions will show check boxes to enable Anonymous Access to Read and Write. Checking Read will allow the anonymous end clients to access the `get<Type>` and `query<Type>` query operations. Checking Write will allow anonymous end clients to access the `add<Type>`, `update<Type>`, and `delete<Type>` mutation operations.

By default all operations are accessible to anonymous clients. However, this behavior will change in the near future. When this behavior is changed, it will apply only to newly created backends. Existing backends will remain unaffected by this future change.

Anonymous Access works as an access control security one level above the [GraphQL `@auth` Directive]({{< relref "auth.md" >}}). When you block anonymous access to your backend, the GraphQL requests from the client will not go through to the Dgraph database. When Anonymous Access is blocked, the GraphQL Auth Rules are not evaluated against the database.

Anonymous Access granted on level types only applies to the parent type operations and is not meant to be a way to secure all data of that type. It is still possible to read/write data of a Type that has been set with no read/write permissions if other types are granted read/write access to anonymous clients.

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

If the Anonymous Access was granted Read and Write for Post but not granted Read and Write for User, it would be possible still to perform the following operations:

```graphql
mutation addPost {
  addPost(input: [{
    title: "New Post Title" @search(by: [hash])
    author: { name: "New User Name" } # creates a new User node.
  }]) {
    numUids
  }
}
mutation removeAuthor {
  updatePost(input: {
    filter: { title: { eq: "New Post Title" } }
    remove: { author: null } # does not delete the User node itself, just the linked reference.
  }) {
    numUids
  }
}
mutation addAuthor {
  updatePost(input: {
    filter: { title: { eq: "New Post Title" } }
    set: { author: { name: "Another New User Name" } } # creates a new User node.
  }) {
    numUids
  }
}
query queryPost {
  queryPost {
    id
    title
    author { # reads the User node.
      id
      name
    }
  }
}
```

The Client and Admin API Keys that you generate on the [settings page](https://cloud.dgraph.io/_/settings) will have full access to all the GraphQL operations. To use an API key to authenticate a client, pass the API key in the `DG-Auth` header while sending your requests to the `/graphql` endpoint of your backend.

Example passing headers using Apollo Client in React:

```Javascript
import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const httpLink = createHttpLink({
  uri: '<your-cloud-endpoint>/graphql',
});

const authLink = setContext((_, { headers }) => {
  // get the authentication token from local storage if it exists
  const token = localStorage.getItem('token'); // JWT token
  // get the API key from local storage if it exists
  const key = localStorage.getItem('key'); // API key
  // return the headers to the context so httpLink can read them
  return {
    headers: {
      ...headers,
      <your-dgraph-authorization-header-key>: token ?? undefined,
      'DG-Auth': key ?? undefined,
    }
  }
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});
```

### Writing Auth Rules

Once a client has been granted access to an operation with either Anonymous Access granted or as an authenticated client using an API Key, the GraphQL query or mutation is then unrestricted by default. In order to further restrict access, please see the [the @auth directive]({{< relref "auth.md" >}}).

### Restricting CORS

Restricting the origins that your Dgraph Cloud responds to is an important step in preventing XSS exploits. By default, we allow requesting code from any origin access to your Dgraph Cloud resources (`Access-Control-Allow-Origin: *`), but by explicitly specifying the permitted origins this default behavior can be overridden.

To allow an origin, add the line `# Dgraph.Allow-Origin` at the end of your GraphQL schema either with a [schema update]({{< relref "graphql/admin.md#using-updategqlschema-to-add-or-modify-a-schema" >}}) or via the Cloud console's [Schema](https://cloud.dgraph.io/_/schema) page. For example, the following will restrict all origins except the ones specified.

```
# Dgraph.Allow-Origin "https://example.com"
# Dgraph.Allow-Origin "https://www.example.com"
```

On adding your first origin, we automatically add `https://cloud.dgraph.io`  as well, so that the API explorer continues to work.

{{% notice "note" %}}
CORS restrictions are not a replacement for writing auth rules, as it is possible for malicious actors to bypass these restrictions.
Also, note that CORS restrictions only apply to browsers, so you should never use CORS as a way to secure your system (CORS can only protect user data).
{{% /notice %}}
