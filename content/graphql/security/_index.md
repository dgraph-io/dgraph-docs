+++
title = "Security"
description = "Dgraph's GraphQL implementation comes with built-in authorization, and supports various authentication methods, so you can annotate your schema with rules that determine who can access or mutate the data."
[menu.main]
  identifier = "gql-auth"
  parent = "graphql"
  weight = 21
+++

When you deploy a GraphQL schema, Dgraph automatically generates the query and mutation operations for each type and exposes them as a GraphQL API on the ``/graphql`` endpoint.


Dgraph's GraphQL authorization features let you specify : 
- if the client requires an API key or notif **anonymous access** is allowed to invoke a specific operation of the API.
- if a client must present an identity in the form of a **JWT token** to use the API.
- **RBAC rules** (Role Based Access Control) at operation level based on the claims included in the client JWT token.
- **Graph traversal rules** at data level.


{{% notice "note" %}}
By default all operations are accessible to anonymous clients, no JWT token is required and no authorization rules are applied.
It is your responsability to correctly configure the authorization for the ``/graphql`` endpoint.
{{% /notice %}}

Refer to the following documentation to set your ``/graphql`` endpoint security :
- [Configure anonymous access]({{< relref "anonymous-access.md" >}})

- [Handle JWT token]({{< relref "jwt.md" >}})

- [RBAC rules]({{< relref "RBAC-rules.md">}})

- [Graph traversal rules]({{< relref "graphtraversal-rules.md">}})

### ``/graphql`` security flow
In summary, the Dgraph security flow on ``/graphql`` endpoint is as follow:

{{<figure class="medium image" src="/images/graphql/RBAC.jpeg" title="graphql endpoint security" alt="graphql endpoint security">}}

### CORS
Additionaly, you can [restrict the origins]({{< relref "cors.md">}}) that ``/graphql`` endpoint responds to.

This is a best practice to prevent XSS exploits.

## Authentication

Dgraph's GraphQL authorization relies on the presence of a valid JWT token in the request. 

Dgraph supports both symmetric (HS256) and asymmetric (RS256) encryption and accepts JSON Web Key (JWK) URL or signed JSON Web Token (JWT).

You can use any authentication method that is capable of generating such JWT token (Auth0, Cognito, Firebase, etc...) including Dgraph login mechanism.


{{% notice "tip" %}}
To learn more about adding JWTs from a third-party JWT signer to your app, see our tutorial 
[Auth0 Authentication]({{< relref "graphql/todo-app-tutorial/todo-auth0-jwt" >}}) or [Firebase Authentication]({{< relref "graphql/todo-app-tutorial/todo-firebase-jwt" >}}). {{% /notice %}}

### ACL
Note that another token will be needed to access the system if ACL security is also enabled, or a “shared” cloud back-end is in use (as any shared back-end is secured by ACLs set up on your behalf by Dgraph). See the [ACLs]({{< relref "access-control-lists.md">}}) section for details. The ACLs are a separate security mechanism.

### JWT Claims

In JSON web tokens (JWTs) (https://www.rfc-editor.org/rfc/rfc7519) , a claim appears as a name/value pair.

When we talk about a claim in the context of a JWT, we are referring to the name (or key). For example, the following JSON object contains three claims ``sub``, ``name`` and ``admin``:
```json
{ 
"sub": "1234567890", 
"name": "John Doe", 
"admin": true 
} 
```

So that different organizations can specify different claims without conflicting, claims typically have a namespace, and it's a good practice to specify the namespace of your claims. put specific claims in a nested structure called a namespace.
```
{
  "https://mycompany.org/jwt/claims": {
    "username": "auth0|63fe77f32cef38f4fa3dab34",
    "role": "Admin"
  },
  "name": "raph@dgraph.io",
  "email": "raph@dgraph.io",
  "email_verified": false,
  "iss": "https://dev-5q3n8cc7nckhu5w8.us.auth0.com/",
  "aud": "aqk1CSVtliyoXUfLaaLKSKUtkaIel6Vd",
  "iat": 1677705681,
  "exp": 1677741681
}
```
This json is a JWT token payload containing a namespace  ``https://mycompany.org/jwt/claims`` having a ``username`` claim and a ``role`` claim.

<style>
  ul.contents {
    display: none;
  }
</style>