+++
title = "Overview of Authorization and Authentication with GraphQL"
description = "Dgraph's GraphQL implementation comes with built-in authorization, and supports various authentication methods, so you can annotate your schema with rules that determine who can access or mutate the data."
weight = 1
[menu.main]
    name = "Overview"
    parent = "authorization"
    identifier = "authorization-overview"
+++

Dgraph's GraphQL implementation comes with built-in authorization. This lets you annotate your schema with rules that determine who can query and mutate your data.

First, let's get some concepts defined. There are two important concepts included in what's often called *auth*:

* Authorization: access permissions (what are you allowed to do)
* Authentication: establishment of identity (who you are)

Dgraph lets you use your GraphQL schema to manage both authorization and authentication:
* You set authorization rules by annotating your schema with the `@auth` directive
* You configure authentication methods by providing those settings to Dgraph in the last
line of your schema, in a commented-out `Dgraph.Authorization` object.

Establishing identity and managing identity-based permissions are closely related,
so this page covers both Dgraph's authorization capabilities, and how Dgraph works with
various authentication methods.

## Authorization

You can add authorization rules to your schema using the `@auth` directive. But,
you also need to configure the `Dgraph.Authorization` object (which handles
authentication) on the last line of your schema for the `@auth` directive to
work (as described below).

When authentication and authorization are complete, your schema should look similar to the following:

```graphql
type A @auth(...) {
    ...
}

type B @auth(...) {
    ...
}

# Dgraph.Authorization {"VerificationKey":"","Header":"","Namespace":"","Algo":"","Audience":[]}
```


## Authentication

You can authenticate your users using the following methods:
* A cloud service like OneGraph, Firebase, or Auth0
* Social sign-in options (such as Google authentication)
* Your own custom authentication code

Dgraph's GraphQL implementation is completely flexible about how your app does
authentication; instead, Dgraph focuses on authorization.  

Dgraph's GraphQL endpoint supports both symmetric (secret-based) and asymmetric (public key) 
encryption. The connection between Dgraph and your authentication mechanism can
be a JSON Web Key (JWK) URL or a signed JSON Web Token (JWT). So, you can provide
Dgraph with the public key of the JWT signer (such as Firebase or Auth0) and
Dgraph trusts JWTs signed by the corresponding private key.

{{% notice "tip" %}}
To learn more about adding JWTs from a third-party JWT signer to your app, see
[Auth0 Authentication]({{< relref "graphql/todo-app-tutorial/todo-auth0-jwt" >}}) or [Firebase Authentication]({{< relref "graphql/todo-app-tutorial/todo-firebase-jwt" >}}). {{% /notice %}}

### `Dgraph.Authorization` parameters

To define the authentication connection method, Dgraph uses a commented-out
`Dgraph.Authorization` object that you should add as the last line of your schema.
You can only use one authentication connection method, either JWT, a single JWK
URL, or multiple JWK URLs.

The `Dgraph.Authorization` object uses the following syntax:

```json
{"Header":"", "Namespace":"", "Algo":"", "VerificationKey":"", "JWKURL":"", "Audience":[], "ClosedByDefault": false}
```

This object contains the following values:
* `Header` is the header that requests use to store the signed JWT.
* `Namespace` is the key inside the JWT that contains the claims relevant to Dgraph authorization.
* `Algo` is the JWT verification algorithm which can be either `HS256` or `RS256`.
* `VerificationKey` is the string value of the key, with newlines replaced with `\n` and the key string wrapped in `""`:
  * **For asymmetric encryption**: `VerificationKey` contains the public key string
  * **For symmetric (secret-based) encryption**: `VerificationKey` is the secret key; this can be any secret string you choose, such as one that you generate using a tool like OpenSSL
* `JWKURL`/`JWKURLs` is the URL for the JSON Web Key sets. If you want to pass multiple URLs, use `JWKURLs` as an array of multiple JWK URLs for the JSON Web Key sets.
* `Audience` is used to verify the `aud` field of a JWT, which is used by certain providers to indicate the intended audience for the JWT. When doing authentication with `JWKURL`, this field is mandatory as identity providers share JWKs among multiple tenants.
* `ClosedByDefault`, if set to `true`, requires authorization for all requests even if the type does not specify the [`@auth`]({{< relref "directive.md" >}}) directive. If omitted, the default setting is `false`.

{{% notice "tip" %}}
To pass multiple URLs, use `JWKURLs` as an array of multiple JWK URLs for the JSON Web Key sets.
{{% /notice %}}

To set the authentication connection method, do the following:

* **To use a JWT**: On the last line of your schema, specify a verification key (`VerificationKey`) and encryption algorithm (`Algo`) in the `Dgraph.Authorization` object. Dgraph verifies the JWT against the provided `VerificationKey`. So, your schema should end with a line like the following:

```
# Dgraph.Authorization {"VerificationKey":"<verification-key-here>","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"HS256","Audience":["aud1","aud5"]}
```

* **To use a single JWK URL**: Specify the `JWKURL` and `Audience` arguments in the `Dgraph.Authorization` object. Dgraph fetches the JWK and verifies the token against it. So, your schema should end with a line like the following:

```
# Dgraph.Authorization {"VerificationKey":"","Header":"X-My-App-Auth", "jwkurl":"https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com", "Namespace":"https://xyz.io/jwt/claims","Algo":"","Audience":["fir-project1-259e7", "HhaXkQVRBn5e0K3DmMp2zbjI8i1wcv2e"]}
```

* **To use multiple JWK URLs**: Specify the `JWKURLs` and `Audience` arguments in the `Dgraph.Authorization` object. Dgraph fetches all of the JWKs and verifies the token against one of the JWKs, based on the JWK's kind. So, your schema should end with a line like the following:

```
# Dgraph.Authorization {"VerificationKey":"","Header":"X-My-App-Auth","jwkurls":["https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com","https://dev-hr2kugfp.us.auth0.com/.well-known/jwks.json"], "Namespace":"https://xyz.io/jwt/claims","Algo":"","Audience":["fir-project1-259e7", "HhaXkQVRBn5e0K3DmMp2zbjI8i1wcv2e"]}
```

## Using JWTs and authorization claims

In addition to the examples shown above, you can configure `Dgraph.Authorization` as follows
to use the `X-My-App-Auth` header and use namespace-based authorization claims:

- HMAC-SHA256 JWT with symmetric cryptography (the signing key and verification key are the same):

```
# Dgraph.Authorization {"VerificationKey":"secretkey","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"HS256"}
```

- RSA Signature with SHA-256 asymmetric cryptography (the JWT is signed with the private key and Dgraph checks with the public key):

```
# Dgraph.Authorization {"VerificationKey":"-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----","Header":"X-My-App-Auth","Namespace":"https://my.app.io/jwt/claims","Algo":"RS256"}
```

### Authorization with custom claims

In both of the examples above, the header `X-My-App-Auth` is required and the
JWT is expected to contain a custom claims object (in this case, `"https://my.app.io/jwt/claims": { ... }`) with the claims used in authorization rules.

The value of the `X-My-App-Auth` header is expected to be in one of the following forms:
* Just the JWT token. For example:
    ```txt
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJodHRwczovL215LmFwcC5pby9qd3QvY2xhaW1zIjp7fX0.Pjlxpf-3FhH61EtHBRo2g1amQPRi0pNwoLUooGbxIho
    ```

* A Bearer token, e.g., a JWT prepended with `Bearer ` prefix (including space). For example:
    ```txt
    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJodHRwczovL215LmFwcC5pby9qd3QvY2xhaW1zIjp7fX0.Pjlxpf-3FhH61EtHBRo2g1amQPRi0pNwoLUooGbxIho
    ```

### Authorization with standard claims

Apart from the custom claims belonging to a given namespace, you can use standard claims in the authorization rules, as shown in the following example:

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

The authorization variables include the rest of the given claims along with the claims provided under namespace `https://xyz.io/jwt/claims`.

{{% notice "note" %}}
In cases where the same variable is present in both custom claims and standard claims, the variable value in the custom claim takes precedence.
{{% /notice %}}
