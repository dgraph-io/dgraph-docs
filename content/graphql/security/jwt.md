+++
title = "Handle JWT Token"
[menu.main]
  identifier = "authorization-header"
  parent = "gql-auth"
  weight = 3
+++

When deploying a GraphQL schema, the admin user can set a  ``# Dgraph.Authorization`` line at the bottom of the schema to specify how JWT tokens present in the HTTP header requests are extracted, validated and used.

This line must start with the exact string ``# Dgraph.Authorization`` and be at the bottom of the schema file.


### Configure JWT token handling

To configure how Dgraph should handle JWT token for ``/graphql`` endpoint : 
1. Add a line starting with ``# Dgraph.Authorization`` and with the following parameters at the very end of your GraphQL schema.  
  The `Dgraph.Authorization` object uses the following syntax:

  ```
  # Dgraph.Authorization {"VerificationKey":"<verification-key-here>","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"HS256","Audience":["aud1"],"ClosedByDefault":true}
  ```

Dgraph.Authorization object contains the following parameters:
* `Header` name of the header field used by the client to send the token. 
 {{% notice "note" %}}
 Do not use `Dg-Auth`, `X-Auth-Token` or `Authorization` headers which are used by Dgraph for other purposes.
{{% /notice %}}
* `Namespace` is the key inside the JWT that contains the claims relevant to Dgraph authorization.
* `Algo` is the JWT verification algorithm which can be either `HS256` or `RS256`.
* `VerificationKey` is the string value of the key, with newlines replaced with `\n` and the key string wrapped in `""`:
  * **For asymmetric encryption**: `VerificationKey` contains the public key string.
  * **For symmetric (secret-based) encryption**: `VerificationKey` is the secret key.
* `JWKURL`/`JWKURLs` is the URL for the JSON Web Key sets. If you want to pass multiple URLs, use `JWKURLs` as an array of multiple JWK URLs for the JSON Web Key sets. You can only use one authentication connection method, either JWT (`Header`), a single JWK URL, or multiple JWK URLs.
* `Audience` is used to verify the `aud` field of a JWT, which is used by certain providers to indicate the intended audience for the JWT. When doing authentication with `JWKURL`, this field is mandatory.
* `ClosedByDefault`, if set to `true`, requires authorization for all requests even if the GraphQL type does not specify rules. If omitted, the default setting is `false`.

2. Deploy the GraphQL schema either with a [schema update]({{< relref "graphql/admin.md#using-updategqlschema-to-add-or-modify-a-schema" >}}) or via the Cloud console's [Schema](https://cloud.dgraph.io/_/schema) page.


When the `# Dgraph.Authorization` line is present in the GraphQL schema, Dgraph will use the settings in that line to
- read the specified header in each HTTP request sent on the /graphql endpoint,
- decode that header as a JWT token using the specified algorithm (Algo)
- validate the token signature and the audience
- extract the JWT claims present in the specified namespace and at the root level

These claims will then be accessible to any @auth schema directives (a GraphQL schema directive specific to Dgraph) that are associated with GraphQL types in the schema file. 

See the [RBAC rules]({{< relref "RBAC-rules.md">}}) and [Graph traversal rules]({{< relref "graphtraversal-rules.md">}} for details on how to restrict data access using the @auth directive on a per-type basis.

### Require JWT token
To not only accept but to require the JWT token regardless of @auth directives in your GraphQL schema, set option "ClosedByDefault" to true in the `# Dgraph.Authorization` line.

### Examples


To use a single JWK URL: 

```
# Dgraph.Authorization {"VerificationKey":"","Header":"X-My-App-Auth", "jwkurl":"https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com", "Namespace":"https://xyz.io/jwt/claims","Algo":"","Audience":["fir-project1-259e7", "HhaXkQVRBn5e0K3DmMp2zbjI8i1wcv2e"]}
```

To use multiple JWK URL: 

```
# Dgraph.Authorization {"VerificationKey":"","Header":"X-My-App-Auth","jwkurls":["https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com","https://dev-hr2kugfp.us.auth0.com/.well-known/jwks.json"], "Namespace":"https://xyz.io/jwt/claims","Algo":"","Audience":["fir-project1-259e7", "HhaXkQVRBn5e0K3DmMp2zbjI8i1wcv2e"]}
```

Using HMAC-SHA256 token in `X-My-App-Auth` header and authorization claims in `https://my.app.io/jwt/claims` namespace:


```
# Dgraph.Authorization {"VerificationKey":"secretkey","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"HS256"}
```

Using HMAC-SHA256 token in `X-My-App-Auth` header and authorization claims in `https://my.app.io/jwt/claims` namespace:

```
# Dgraph.Authorization {"VerificationKey":"-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"RS256"}
```

### JWT format

The value of the JWT ``header`` is expected to be in one of the following forms:
* Just the JWT token.  
  For example:
    ```
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJodHRwczovL215LmFwcC5pby9qd3QvY2xhaW1zIjp7fX0.Pjlxpf-3FhH61EtHBRo2g1amQPRi0pNwoLUooGbxIho
    ```

* A Bearer token, e.g., a JWT prepended with `Bearer ` prefix (including space).  
  For example:
    ```
    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJodHRwczovL215LmFwcC5pby9qd3QvY2xhaW1zIjp7fX0.Pjlxpf-3FhH61EtHBRo2g1amQPRi0pNwoLUooGbxIho
    ```

### Error handling

If ClosedByDefault is set to true, and the JWT is not present or if the JWT token does not include the proper audience information, or is not properly encoded, Dgraph replies to requests on `/graphql` endpoint with an error message rejecting the operation similar to:
```
{
   "errors": [
       {
           "message": "couldn't rewrite query queryContact because a valid JWT is required but was not provided",
           "path": [
               "queryContact"
           ]
       }
   ],
   "data": {
       "queryContact": []
   },...
```

