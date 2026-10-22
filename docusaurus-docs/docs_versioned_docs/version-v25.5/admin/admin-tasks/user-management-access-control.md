---
title: User Management and Access Control
---

After enabling ACL, you can manage users, groups, and configure access control rules to protect your data.

## Accessing Secured Dgraph

Before managing users and groups and configuring ACL rules, you will need to login in order to get a token that is needed to access Dgraph. You will use this token with the `X-Dgraph-AccessToken` header field.

### Logging In

To login, send a POST request to `/admin` with the GraphQL mutation. For example, to log in as the root user `groot`:

```graphql
mutation {
  login(userId: "groot", password: "password") {
    response {
      accessJWT
      refreshJWT
    }
  }
}
```

**Response:**

```json
{
  "data": {
    "accessJWT": "<accessJWT>",
    "refreshJWT": "<refreshJWT>"
  }
}
```

#### Access Token

The response includes the access and refresh JWTs which are used for the authentication itself and refreshing the authentication token, respectively. Save the JWTs from the response for later HTTP requests.

You can run authenticated requests by passing the access JWT to a request via the `X-Dgraph-AccessToken` header. Add the header `X-Dgraph-AccessToken` with the `accessJWT` value which you got in the login response in the GraphQL tool which you're using to make the request.

For example, if you were using the GraphQL Playground, you would add this in the headers section:

```json
{ "X-Dgraph-AccessToken" : "<accessJWT>" }
```

And in the main code section, you can add a mutation, such as:

```graphql
mutation {
  addUser(input: [{ name: "alice", password: "whiterabbit" }]) {
    user {
      name
    }
  }
}
```

#### Refresh Token

The refresh token can be used in the `/admin` POST GraphQL mutation to receive new access and refresh JWTs, which is useful to renew the authenticated session once the ACL access TTL expires (controlled by Dgraph Alpha's flag `--acl_access_ttl` which is set to 6h0m0s by default).

```graphql
mutation {
  login(
    userId: "groot"
    password: "password"
    refreshToken: "<refreshJWT>"
  ) {
    response {
      accessJWT
      refreshJWT
    }
  }
}
```

### Login using a Client

With ACL configured, you need to log in as a user to access data protected by ACL rules. You can do this using the client's `.login(USER_ID, USER_PASSWORD)` method.

Here are some code samples using a client:

* **Go** ([dgo client](https://github.com/dgraph-io/dgo)): example `acl_over_tls_test.go` ([here](https://github.com/dgraph-io/dgraph/blob/main/tlstest/acl/acl_over_tls_test.go))
* **Java** ([dgraph4j](https://github.com/dgraph-io/dgraph4j)): example `AclTest.java` ([here](https://github.com/dgraph-io/dgraph4j/blob/master/src/test/java/io/dgraph/AclTest.java))

### Login using curl

If you are using `curl` from the command line, you can use the following with the above [login mutation](#logging-in) saved to `login.graphql`:

```bash
## Login and save results
JSON_RESULT=$(curl http://localhost:8080/admin --silent --request POST \
  --header "Content-Type: application/graphql" \
  --upload-file login.graphql
)

## Extracting a token using GNU grep, perl, the silver searcher, or jq
TOKEN=$(grep -oP '(?<=accessJWT":")[^"]*' <<< $JSON_RESULT)
TOKEN=$(perl -wln -e '/(?<=accessJWT":")[^"]*/ and print $&;' <<< $JSON_RESULT)
TOKEN=$(ag -o '(?<=accessJWT":")[^"]*' <<< $JSON_RESULT)
TOKEN=$(jq -r '.data.login.response.accessJWT' <<< $JSON_RESULT)

## Run a GraphQL query using the token
curl http://localhost:8080/admin --silent --request POST \
  --header "Content-Type: application/graphql" \
  --header "X-Dgraph-AccessToken: $TOKEN" \
  --upload-file some_other_query.graphql
```

:::tip
Parsing JSON results on the command line can be challenging, so you will find some alternatives to extract the desired data using popular tools, such as [the silver searcher](https://github.com/ggreer/the_silver_searcher) or the json query tool [jq](https://stedolan.github.io/jq), embedded in this snippet.
:::

## User and Group Administration

The default configuration comes with a user `groot`, with a password of `password`. The `groot` user is part of administrative group called `guardians` that have access to everything. You can add more users to the `guardians` group as needed.

### Reset the Root Password

You can reset the root password like this example:

```graphql
mutation {
  updateUser(
    input: {
      filter: { name: { eq: "groot" } }
      set: { password: "$up3r$3cr3t1337p@$$w0rd" }
    }
  ) {
    user {
      name
    }
  }
}
```

### Create a Regular User

To create a user `alice`, with password `whiterabbit`, you should execute the following GraphQL mutation:

```graphql
mutation {
  addUser(input: [{name: "alice", password: "whiterabbit"}]) {
    user {
      name
    }
  }
}
```

### Create a Group

To create a group `dev`, you should execute:

```graphql
mutation {
  addGroup(input: [{name: "dev"}]) {
    group {
      name
      users {
        name
      }
    }
  }
}
```

### Assign a User to a Group

To assign the user `alice` to both the group `dev` and the group `sre`, the mutation should be:

```graphql
mutation {
  updateUser(
    input: {
      filter: { name: { eq: "alice" } }
      set: { groups: [{ name: "dev" }, { name: "sre" }] }
    }
  ) {
    user {
      name
      groups {
        name
      }
    }
  }
}
```

### Remove a User from a Group

To remove `alice` from the `dev` group, the mutation should be:

```graphql
mutation {
  updateUser(
    input: {
      filter: { name: { eq: "alice" } }
      remove: { groups: [{ name: "dev" }] }
    }
  ) {
    user {
      name
      groups {
        name
      }
    }
  }
}
```

### Delete a User

To delete the user `alice`, you should execute:

```graphql
mutation {
  deleteUser(filter: { name: { eq: "alice" } }) {
    msg
    numUids
  }
}
```

### Delete a Group

To delete the group `sre`, the mutation should be:

```graphql
mutation {
  deleteGroup(filter: { name: { eq: "sre" } }) {
    msg
    numUids
  }
}
```

## ACL Rules Configuration

You can set up ACL rules using the Dgraph Ratel UI or by using a GraphQL tool, such as [Insomnia](https://insomnia.rest/), [GraphQL Playground](https://github.com/prisma/graphql-playground), [GraphiQL](https://github.com/skevy/graphiql-app), etc. You can set the permissions on a predicate for the group using a pattern similar to the UNIX file permission conventions shown below:

| Permission                  | Value | Binary |
|-----------------------------|-------|--------|
| `READ`                      | `4`   | `100`  |
| `WRITE`                     | `2`   | `010`  |
| `MODIFY`                    | `1`   | `001`  |
| `READ` + `WRITE`            | `6`   | `110`  |
| `READ` + `WRITE` + `MODIFY` | `7`   | `111`  |

These permissions represent the following:

* `READ` - group has permission to read the predicate
* `WRITE` - group has permission to write or update the predicate
* `MODIFY` - group has permission to change the predicate's schema

The following examples will grant full permissions to predicates to the group `dev`. If there are no rules for a predicate, the default behavior is to block all (`READ`, `WRITE` and `MODIFY`) operations.

### Assign Predicate Permissions to a Group

Here we assign a permission rule for the `friend` predicate to the group:

```graphql
mutation {
  updateGroup(
    input: {
      filter: { name: { eq: "dev" } }
      set: { rules: [{ predicate: "friend", permission: 7 }] }
    }
  ) {
    group {
      name
      rules {
        permission
        predicate
      }
    }
  }
}
```

In case you have [reverse edges](../../dql/dql-schema#reverse-predicates), they have to be given the permission to the group as well:

```graphql
mutation {
  updateGroup(
    input: {
      filter: { name: { eq: "dev" } }
      set: { rules: [{ predicate: "~friend", permission: 7 }] }
    }
  ) {
    group {
      name
      rules {
        permission
        predicate
      }
    }
  }
}
```

In some cases, it may be desirable to manage permissions for all the predicates together rather than individual ones. This can be achieved using the `dgraph.all` keyword.

The following example provides `read+write` access to the `dev` group over all the predicates of a given namespace using the `dgraph.all` keyword.

```graphql
mutation {
  updateGroup(
    input: {
      filter: { name: { eq: "dev" } }
      set: { rules: [{ predicate: "dgraph.all", permission: 6 }] }
    }
  ) {
    group {
      name
      rules {
        permission
        predicate
      }
    }
  }
}
```

:::note
The permissions assigned to a group `dev` is the union of permissions from `dgraph.all` and permissions for a specific predicate `name`. So if the group is assigned `READ` permission for `dgraph.all` and `WRITE` permission for predicate `name` it will have both, `READ` and `WRITE` permissions for the `name` predicate, as a result of the union.
:::

### Remove a Rule from a Group

To remove a rule or rules from the group `dev`, the mutation should be:

```graphql
mutation {
  updateGroup(
    input: {
      filter: { name: { eq: "dev" } }
      remove: { rules: [ "friend", "~friend" ] }
    }
  ) {
    group {
      name
      rules {
        predicate
        permission
      }
    }
  }
}
```

## Querying Users and Groups

You can query and get information for users and groups. These sections show output that will show the user `alice` and the `dev` group along with rules for `friend` and `~friend` predicates.

### Query for Users

Let's query for the user `alice`:

```graphql
query {
  queryUser(filter: { name: { eq: "alice" } }) {
    name
    groups {
      name
    }
  }
}
```

The output should show the groups that the user has been added to, e.g.

```json
{
  "data": {
    "queryUser": [
      {
        "name": "alice",
        "groups": [
          {
            "name": "dev"
          }
        ]
      }
    ]
  }
}
```

### Get User Information

We can obtain information about a user with the following query:

```graphql
query {
  getUser(name: "alice") {
    name
    groups {
      name
    }
  }
}
```

The output should show the groups that the user has been added to, e.g.

```json
{
  "data": {
    "getUser": {
      "name": "alice",
      "groups": [
        {
          "name": "dev"
        }
      ]
    }
  }
}
```

### Query for Groups

Let's query for the `dev` group:

```graphql
query {
  queryGroup(filter: { name: { eq: "dev" } }) {
    name
    users {
      name
    }
    rules {
      permission
      predicate
    }
  }
}
```

The output should include the users in the group as well as the permissions, the group's ACL rules, e.g.

```json
{
  "data": {
    "queryGroup": [
      {
        "name": "dev",
        "users": [
          {
            "name": "alice"
          }
        ],
        "rules": [
          {
            "permission": 7,
            "predicate": "friend"
          },
          {
            "permission": 7,
            "predicate": "~friend"
          }
        ]
      }
    ]
  }
}
```

### Get Group Information

To check the `dev` group information:

```graphql
query {
  getGroup(name: "dev") {
    name
    users {
      name
    }
    rules {
      permission
      predicate
    }
  }
}
```

The output should include the users in the group as well as the permissions, the group's ACL rules, e.g.

```json
{
  "data": {
    "getGroup": {
      "name": "dev",
      "users": [
        {
          "name": "alice"
        }
      ],
      "rules": [
        {
          "permission": 7,
          "predicate": "friend"
        },
        {
          "permission": 7,
          "predicate": "~friend"
        }
      ]
    }
  }
}
```

## Reset Groot Password

If you have forgotten the password to the `groot` user, then you may reset the `groot` password (or the password for any user) by following these steps.

1. Stop Dgraph Alpha.
2. Turn off ACLs by removing the `--acl_hmac_secret` config flag in the Alpha config. This leaves the Alpha open with no ACL rules, so be sure to restrict access, including stopping request traffic to this Alpha.
3. Start Dgraph Alpha.
4. Connect to Dgraph Alpha using Ratel and run the following upsert mutation to update the `groot` password to `newpassword` (choose your own secure password):
   ```graphql
   upsert {
     query {
       groot as var(func: eq(dgraph.xid, "groot"))
     }
     mutation {
       set {
         uid(groot) <dgraph.password> "newpassword" .
       }
     }
   }
   ```
5. Restart Dgraph Alpha with ACLs turned on by setting the `--acl_hmac_secret` config flag.
6. Login as groot with your new password.

## Related Topics

- [Enable ACL](../../installation/configuration/enable-acl) - Configure and enable ACL feature
- [Admin Endpoints](../admin-endpoints) - GraphQL Admin API reference

