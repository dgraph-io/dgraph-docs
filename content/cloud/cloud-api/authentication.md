+++
title = "Authentication"
weight = 2
[menu.main]
    parent = "cloud-api"
    identifier = "api-authentication"
+++

## Login

Login will generate a JWT token that can be used to access other Dgraph Cloud
APIs.

This API requires an email address and password. If you have signed up with a
social media provider, you may create a new password by selecting
`Forgot Password` on the login page.

### Cloud Endpoint

```
https://cerebro.cloud.dgraph.io/graphql
```

### API Command

```graphql
query Login($email: String!, $password: String!) {
  login(email: $email, password: $password) {
    token
  }
}
```

**Arguments**

- `email`: your email address
- `password`: your password

### Example

Below is an example request and response. The token below must be passed to all
future API calls as a bearer token in the `Authorization` header.

{{% tabs %}} {{< tab "request" >}}
```bash
curl 'https://cerebro.cloud.dgraph.io/graphql' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"query Login($email: String!, $password: String!) {\n  login(email: $email, password: $password) {    \n    token\n  }\n}","variables":{"email":"<your-email>","password":"<your-password>"}}' \
  --compressed
```
{{< /tab >}} 

{{% tab "response" %}}
```json
{
  "data": {
    "login": {
      "token": "<cerebro-jwt>"
    }
  }
}
```

{{% /tab %}} {{% /tabs %}}

## Using the authentication token

The token returned from the login API must be passed to all future API calls as
a bearer token in the `Authorization` header.
