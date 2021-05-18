+++
title = "Overview"
description = "Dgraph's GraphQL implementation comes with built-in authorization. This lets you annotate your schema with rules that determine who can access or mutate the data."
weight = 1
[menu.main]
    parent = "authorization"
    identifier = "authorization-overview"
+++

Dgraph's GraphQL implementation comes with built-in authorization. This lets you annotate your schema with rules that determine who can access or mutate the data.

First, let's get some concepts defined. There are two important concepts included in what's often called 'auth':

* authentication: establishment of identity (who you are)
* authorization: access permissions (what are you allowed to do)

## Authentication

You can authenticate your users with a cloud service like OneGraph, Firebase or Auth0, use some social sign-in options, or write bespoke authentication code. Dgraph's GraphQL implementation is completely flexible about how your app does authentication - instead, it focuses on authorization.  

Dgraph's GraphQL implementation supports both symmetric (secret-based) and asymmetric (public key) 
encryption. The connection between Dgraph and your authentication mechanism can be a JSON Web Key URL (JWK URL) or a signed JSON Web Token (JWT). For example, you can provide Dgraph with the public key of the JWT signer (such as Firebase or Auth0) and Dgraph trusts JWTs signed by the corresponding private key.

{{% notice "tip" %}}
To learn more about adding JWTs from a third-party JWT signer to your app, see
[Auth0 Authentication]({{< relref "graphql/todo-app-tutorial/todo-auth0-jwt" >}}) or [Firebase Authentication]({{< relref "graphql/todo-app-tutorial/todo-firebase-jwt" >}}). {{% /notice %}}

#### `Dgraph.Authorization` parameters

To define the connection method, you must set the `# Dgraph.Authorization` object:

```json
{"Header":"", "Namespace":"", "Algo":"", "VerificationKey":"", "JWKURL":"", "Audience":[], "ClosedByDefault": false}
```

This object contains the following values.
* `Header` is the header in which requests will send the signed JWT
* `Namespace` is the key inside the JWT that contains the claims relevant to Dgraph authorization
* `Algo` is the JWT verification algorithm which can be either `HS256` or `RS256`
* `VerificationKey` is the string value of the key, with newlines replaced with `\n` and the key string wrapped in `""`. If you are using asymmetric encryption, `VerificationKey` contains the public key string; if you are using symmetric (secret-based) encryption, `VerificationKey` is the secret key string generated using a tool like OpenSSL.
* `JWKURL`/`JWKURLs` is the URL for the JSON Web Key sets. If you want to pass multiple URLs, use `JWKURLs` as an array of multiple JWK URLs for the JSON Web Key sets
* `Audience` is used to verify the `aud` field of a JWT which might be set by certain providers. It indicates the intended audience for the JWT. When doing authentication with `JWKURL`, this field is mandatory as Identity Providers share JWKs among multiple tenants
* `ClosedByDefault`, if set to `true`, requires authorization for all requests even if the type does not specify the [`@auth`]({{< relref "directive.md" >}}) directive. If omitted, the default setting is `false`.

{{% notice "tip" %}}
If you want to pass multiple URLs, use `JWKURLs` as an array of multiple JWK URLs for the JSON Web Key sets.
{{% /notice %}}

To set up the authentication connection method:

**JSON Web Token (JWT)**
- A (`VerificationKey`, `Algo`) pair must be provided. The server will verify the JWT against the provided `VerificationKey`.

**JSON Web Key URL (JWK URL)**
- `JWKURL` and `Audience` must provided. The server will fetch all the JWKs and verify the token against one of the JWK, based on the JWK's kind.

{{% notice "note" %}}
You can only define one method, either `JWKURL` or `(VerificationKey, Algo)`, but not both.
{{% /notice %}}

### Authorization

With an authentication mechanism set up, you then annotate your schema with the `@auth` directive to define your authorization rules, attach details of your authentication provider to the last line of the schema, and pass the schema to Dgraph.  So your schema will follow this pattern.

```graphql
type A @auth(...) {
    ...
}

type B @auth(...) {
    ...
}

# Dgraph.Authorization {"VerificationKey":"","Header":"","Namespace":"","Algo":"","Audience":[]}
```

Valid `Dgraph.Authorization` examples look like:

```
# Dgraph.Authorization {"VerificationKey":"verificationkey","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"HS256","Audience":["aud1","aud5"]}
```

With a single JWK URL:

```
# Dgraph.Authorization {"VerificationKey":"","Header":"X-My-App-Auth", "jwkurl":"https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com", "Namespace":"https://xyz.io/jwt/claims","Algo":"","Audience":["fir-project1-259e7", "HhaXkQVRBn5e0K3DmMp2zbjI8i1wcv2e"]}
```

With multiple JWK URLs:

```
# Dgraph.Authorization {"VerificationKey":"","Header":"X-My-App-Auth","jwkurls":["https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com","https://dev-hr2kugfp.us.auth0.com/.well-known/jwks.json"], "Namespace":"https://xyz.io/jwt/claims","Algo":"","Audience":["fir-project1-259e7", "HhaXkQVRBn5e0K3DmMp2zbjI8i1wcv2e"]}
```

Without an `Audience` field:

- HMAC-SHA256 JWT with symmetric cryptography (the signing key and verification key are the same):

```
# Dgraph.Authorization {"VerificationKey":"secretkey","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"HS256"}
```

- RSA Signature with SHA-256 asymmetric cryptography (the JWT is signed with the private key and Dgraph checks with the public key):

```
# Dgraph.Authorization {"VerificationKey":"-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"RS256"}
```

#### `X-My-App-Auth` Header

Both cases expect the JWT to be in a header `X-My-App-Auth` and expect the JWT to contain custom claims object `"https://my.app.io/jwt/claims": { ... }` with the claims used in authorization rules.

The value of the `X-My-App-Auth` header is expected to be in one of these two forms:
1. Just the JWT token. For example:
    ```txt
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJodHRwczovL215LmFwcC5pby9qd3QvY2xhaW1zIjp7fX0.Pjlxpf-3FhH61EtHBRo2g1amQPRi0pNwoLUooGbxIho
    ```

2. A Bearer token, e.g., a JWT prepended with `Bearer ` prefix (including space). For example:
    ```txt
    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJodHRwczovL215LmFwcC5pby9qd3QvY2xhaW1zIjp7fX0.Pjlxpf-3FhH61EtHBRo2g1amQPRi0pNwoLUooGbxIho
    ```

#### Using Standard claims

Apart from the custom claims belonging to a given namespace, you can use standard claims in the authorization rules.
For example:

```json
{
   "https://xyz.io/jwt/claims": [
      ....
   ],
  "ROLE": "ADMIN",
  "USERROLE": "user1",
  "email": "random@example.com",
  "email_verified": true,
  "sub": "1234567890",
  "aud": "63do0q16n6ebjgkumu05kkeian",
  "iat": 1611694692,
  "exp": 2611730692
}
```

The auth variables will include the rest of the given claims along with the claims provided under namespace `https://xyz.io/jwt/claims`.

{{% notice "note" %}}
In case the same variable is present in both custom claims and standard claims, the value in the custom claims will take precedence.
{{% /notice %}}
