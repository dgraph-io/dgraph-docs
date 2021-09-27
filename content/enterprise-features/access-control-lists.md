+++
date = "2017-03-20T22:25:17+11:00"
title = "Access Control Lists"
description = "In this guide, we explain Access Control Lists on Dgraph, which can be used to provide access protection to your data stored in Dgraph or Dgraph Cloud dedicated instances."
weight = 1
[menu.main]
    parent = "enterprise-features"
+++

Access Control List (ACL) provides access protection to your data stored in
Dgraph. When the ACL feature is enabled, a client, e.g. [dgo](https://github.com/dgraph-io/dgo) or [dgraph4j](https://github.com/dgraph-io/dgraph4j), must
authenticate with a username and password before executing any transactions, and
is only allowed to access the data permitted by the ACL rules.

ACLs are available to Dgraph Cloud users with dedicated instances.

{{% notice "note" %}}
This feature was introduced in [v1.1.0](https://github.com/dgraph-io/dgraph/releases/tag/v1.1.0).
The `dgraph acl` command is deprecated and will be removed in a future release. ACL changes can be made by using the `/admin` GraphQL endpoint on any Alpha node.
{{% /notice %}}

## Enable enterprise ACL feature

The ACL feature can be turned on by following these steps:

1. Create a plain text file, and store a randomly generated secret key in it. The secret
key is used by Dgraph Alpha nodes to sign JSON Web Tokens (JWT).  Keep this secret key secret to avoid data security issues.  The secret key must have at least 256-bits (32 ASCII characters) to support the HMAC-SHA256 signing algorithm.

2. Start all the Dgraph Alpha nodes in your cluster with the option `--acl secret-file="/path/to/secret"`, and
make sure that they are all using the same secret key file created in Step 1.  Alternatively, you can [store the secret in Hashicorp Vault](#storing-acl-secret-in-hashicorp-vault).


   ```bash
   dgraph alpha --acl "secret-file=/path/to/secret" --security "whitelist=<permitted-ip-addresses>"
   ```

{{% notice "tip" %}}
In addition to command line flags `--acl secret-file="/path/to/secret"` and `--security "whitelist=<permitted-ip-addresses>"`, you can also configure Dgraph using a configuration file (`config.yaml`, `config.json`).  You can also use environment variables, i.e. `DGRAPH_ALPHA_ACL="secret-file=</path/to/secret>"` and `DGRAPH_ALPHA_SECURITY="whitelist=<permitted-ip-addresses>"`. See [Config]({{< relref "deploy/config.md" >}}) for more information in general about configuring Dgraph.
{{% /notice %}}

### Example using Dgraph CLI

Here is an example that starts a Dgraph Zero node and a Dgraph Alpha node with the ACL feature turned on.  You can run these commands in a separate terminal tab:

```bash
## Create ACL secret key file with 32 ASCII characters
echo '12345678901234567890123456789012' > hmac_secret_file

## Start Dgraph Zero in different terminal tab or window
dgraph zero --my=localhost:5080 --replicas 1 --raft idx=1

## Start Dgraph Alpha in different terminal tab or window
dgraph alpha --my=localhost:7080 --zero=localhost:5080 \
  --acl secret-file="./hmac_secret_file" \
  --security whitelist="10.0.0.0/8,172.0.0.0/8,192.168.0.0/16"
```

### Example using Docker Compose

If you are using [Docker Compose](https://docs.docker.com/compose/), you can set up a sample Dgraph cluster using this `docker-compose.yaml` configuration:

```yaml
version: '3.5'
services:
  alpha1:
    command: dgraph alpha --my=alpha1:7080 --zero=zero1:5080
    container_name: alpha1
    environment:
      DGRAPH_ALPHA_ACL: secret-file=/dgraph/acl/hmac_secret_file
      DGRAPH_ALPHA_SECURITY: whitelist=10.0.0.0/8,172.0.0.0/8,192.168.0.0/16
    image: dgraph/dgraph:{{< version >}}
    ports:
      - "8080:8080"
    volumes:
      - ./hmac_secret_file:/dgraph/acl/hmac_secret_file
  zero1:
    command: dgraph zero --my=zero1:5080 --replicas 1 --raft idx=1
    container_name: zero1
    image: dgraph/dgraph:{{< version >}}
```

You can run this with:

```bash
## Create ACL secret key file with 32 ASCII characters
echo '12345678901234567890123456789012' > hmac_secret_file

## Start Docker Compose
docker-compose up
```

### Example using Kubernetes Helm Chart

If you deploy Dgraph on [Kubernetes](https://kubernetes.io/), you can configure the ACL feature using the [Dgraph Helm Chart](https://artifacthub.io/packages/helm/dgraph/dgraph).

The first step is to encode the secret with base64:

```bash
## encode a secret without newline character and copy to the clipboard
printf '12345678901234567890123456789012' | base64
```

The next step is that we need to create a [Helm](https://helm.sh/) chart config values file, e.g. `dgraph_values.yaml`.  We want to copy the results of encoded secret as paste this into the `hmac_secret_file` like the example below:

```yaml
## dgraph_values.yaml
alpha:
  acl:
    enabled: true
    file:
      hmac_secret_file: MTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTI=
  configFile:
    config.yaml: |
      acl:
        secret_file: /dgraph/acl/hmac_secret_file
      security:
        whitelist: 10.0.0.0/8,172.0.0.0/8,192.168.0.0/16
```

Now with the Helm chart config values created, we can deploy Dgraph:

```bash
helm repo add "dgraph" https://charts.dgraph.io
helm install "my-release" --values ./dgraph_values.yaml dgraph/dgraph
```

## Storing ACL secret in Hashicorp Vault

You can save the ACL secret on [Hashicorp Vault](https://www.vaultproject.io/) server instead of saving the secret on the local file system.

### Configuring a Hashicorp Vault Server

Do the following to set up on the [Hashicorp Vault](https://www.vaultproject.io/) server for use with Dgraph:

1. Ensure that the Vault server is accessible from Dgraph Alpha and configured using URL `http://fqdn[ip]:port`.
2. Enable [AppRole Auth method](https://www.vaultproject.io/docs/auth/approle) and enable [KV Secrets Engine](https://www.vaultproject.io/docs/secrets/kv).
3. Save the 256-bits (32 ASCII characters) long ACL secret in a KV Secret path ([K/V Version 1](https://www.vaultproject.io/docs/secrets/kv/kv-v1) or [K/V Version 2](https://www.vaultproject.io/docs/secrets/kv/kv-v2)).  For example, you can upload this below to KV Secrets Engine Version 2 path of `secret/data/dgraph/alpha`:
   ```json
   {
     "options": {
       "cas": 0
     },
     "data": {
       "hmac_secret_file": "12345678901234567890123456789012"
     }
   }
   ```   
4. Create or use a role with an attached policy that grants access to the secret.  For example, the following policy would grant access to `secret/data/dgraph/alpha`:
   ```hcl
   path "secret/data/dgraph/*" {
     capabilities = [ "read", "update" ]
   }
   ```
5. Using the `role_id` generated from the previous step, create a corresponding `secret_id`, and copy the `role_id` and `secret_id` over to local files, like `./dgraph/vault/role_id` and `./dgraph/vault/secret_id`, that will be used by Dgraph Alpha nodes.

{{% notice "tip" %}}
To learn more about the above steps, see [Dgraph Vault Integration: Docker](https://github.com/dgraph-io/dgraph/blob/master/contrib/config/vault/docker/README.md).
{{% /notice %}}

{{% notice "note" %}}
The key format for the `acl-field` option can be defined using `acl-format` with the values `base64` (default) or `raw`.
{{% /notice %}}

### Example using Dgraph CLI with Hashicorp Vault configuration

Here is an example of using Dgraph with a Vault server that holds the secret key:

```bash
## Start Dgraph Zero in different terminal tab or window
dgraph zero --my=localhost:5080 --replicas 1 --raft "idx=1"

## Start Dgraph Alpha in different terminal tab or window
dgraph alpha \
  --security whitelist="10.0.0.0/8,172.0.0.0/8,192.168.0.0/16" \
  --vault addr="http://localhost:8200";acl-field="hmac_secret_file";acl-format="raw";path="secret/data/dgraph/alpha";role-id-file="./role_id";secret-id-file="./secret_id"

```

### Example using Docker Compose with Hashicorp Vault configuration

If you are using [Docker Compose](https://docs.docker.com/compose/), you can set up a sample Dgraph cluster using this `docker-compose.yaml` configuration:

```yaml
version: '3.5'
services:
  alpha1:
    command: dgraph alpha --my=alpha1:7080 --zero=zero1:5080
    container_name: alpha1
    environment:
      DGRAPH_ALPHA_VAULT: addr=http://vault:8200;acl-field=hmac_secret_file;acl-format=raw;path=secret/data/dgraph/alpha;role-id-file=/dgraph/vault/role_id;secret-id-file=/dgraph/vault/secret_id
      DGRAPH_ALPHA_SECURITY: whitelist=10.0.0.0/8,172.0.0.0/8,192.168.0.0/16
    image: dgraph/dgraph:{{< version >}}
    ports:
      - "8080:8080"
    volumes:
      - ./role_id:/dgraph/vault/role_id
      - ./secret_id:/dgraph/vault/secret_id
  zero1:
    command: dgraph zero --my=zero1:5080 --replicas 1 --raft idx=1
    container_name: zero1
    image: dgraph/dgraph:{{< version >}}
```

In this example, you will also need to configure a [Hashicorp Vault](https://www.vaultproject.io/) service named `vault` in the above `docker-compose.yaml`, and then run through this sequence:

1. Launch `vault` service: `docker-compose up --detach vault`
2. Unseal and Configure `vault` with the required prerequisites (see [Configuring a Hashicorp Vault Server](#configuring-a-hashicorp-vault-server)).
3. Save role-id and secret-id as `./role_id` and `secret_id`
4. Launch Dgraph Zero and Alpha: `docker-compose up --detach`


### Example using Kubernetes Helm Chart with Hashicorp Vault configuration

If you deploy Dgraph on [Kubernetes](https://kubernetes.io/), you can configure the ACL feature using the [Dgraph Helm Chart](https://artifacthub.io/packages/helm/dgraph/dgraph).

The next step is that we need to create a [Helm](https://helm.sh/) chart config values file, such as `dgraph_values.yaml`.

```yaml
## dgraph_values.yaml
alpha:
  configFile:
    config.yaml: |
      vault:
        addr: http://vault-headless.default.svc.cluster.local:9200
        acl_field: hmac_secret_file
        acl_format: raw
        path: secret/data/dgraph/alpha
        role_id_file: /dgraph/vault/role_id
        secret_id_file: /dgraph/vault/secret_id
      security:
        whitelist: 10.0.0.0/8,172.0.0.0/8,192.168.0.0/16‘
```

To set up this chart, the [Hashicorp Vault](https://www.vaultproject.io/) service must be installed and available. You can use the [Hashicorp Vault Helm Chart](https://www.vaultproject.io/docs/platform/k8s/helm) and configure it to [auto unseal](https://learn.hashicorp.com/collections/vault/auto-unseal) so that the service is immediately available after deployment.

## Accessing secured Dgraph

Before managing users and groups and configuring ACL rules, you will need to login in order to get a token that is needed to access Dgraph.  You will use this token with the `X-Dgraph-AccessToken` header field.

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

Response:

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


### Login using a client

With ACL configured, you need to log in as a user to access data protected by ACL rules. You can do this using the client's `.login(USER_ID, USER_PASSWORD)` method.

Here are some code samples using a client:

* **Go** ([dgo client](https://github.com/dgraph-io/dgo)): example `acl_over_tls_test.go` ([here](https://github.com/dgraph-io/dgraph/blob/master/tlstest/acl/acl_over_tls_test.go))
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

{{% notice "tip" %}}
Parsing JSON results on the command line can be challenging, so you will find some alternatives to extract the desired data using popular tools, such as [the silver searcher](https://github.com/ggreer/the_silver_searcher) or the json query tool [jq](https://stedolan.github.io/jq), embedded in this snippet.
{{% /notice %}}

## User and group administration

The default configuration comes with a user `groot`, with a password of `password`.  The `groot` user is part of administrative group called `guardians` that have access to everything.  You can add more users to the `guardians` group as needed.

### Reset the root password

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

### Create a regular user

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

### Create a group

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

### Assign a user to a group

To assign the user `alice` to both the group `dev` and the group `sre`, the mutation should be

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

### Remove a user from a group

To remove `alice` from the `dev` group, the mutation should be

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

To delete the user `alice`, you should execute

```graphql
mutation {
  deleteUser(filter: { name: { eq: "alice" } }) {
    msg
    numUids
  }
}
```

### Delete a Group

To delete the group `sre`, the mutation should be

```graphql
mutation {
  deleteGroup(filter: { name: { eq: "sre" } }) {
    msg
    numUids
  }
}
```

## ACL rules configuration

You can set up ACL rules using the Dgraph Ratel UI or by using a GraphQL tool, such as [Insomnia](https://insomnia.rest/), [GraphQL Playground](https://github.com/prisma/graphql-playground), [GraphiQL](https://github.com/skevy/graphiql-app), etc. You can set the permissions on a predicate for the group using a pattern similar to the UNIX file permission conventions shown below:

| Permission                  | Value | Binary |
|-----------------------------|-------|--------|
| `READ`                      | `4`   | `100`  |
| `WRITE`                     | `2`   | `010`  |
| `MODIFY`                    | `1`   | `001`  |
| `READ` + `WRITE`            | `6`   | `110`  |
| `READ` + `WRITE` + `MODIFY` | `7`   | `111`  |

These permissions represent the following:

* `READ` - group has permission to read read the predicate
* `WRITE` - group has permission to write or update the predicate
* `MODIFY` - group has permission to change the predicate's schema

The following examples will grant full permissions to predicates to the group `dev`.  If there are no rules for
a predicate, the default behavior is to block all (`READ`, `WRITE` and `MODIFY`) operations.

### Assign predicate permissions to a group

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

In case you have [reverse edges]({{< relref "query-language/schema.md#reverse-edges" >}}), they have to be given the permission to the group as well

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

{{% notice "note" %}}
The permissions assigned to a group `dev` is the union of permissions from `dgraph.all` and permissions for a specific predicate `name`. So if the group is assigned `READ` permission for `dgraph.all` and `WRITE` permission for predicate `name` it will have both, `READ` and `WRITE` permissions for the `name` predicate, as a result of the union. 
{{% /notice %}}


### Remove a rule from a group

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

## Querying users and groups

You can set up ACL rules using the Dgraph Ratel UI or by using a GraphQL tool, such as [Insomnia](https://insomnia.rest/), [GraphQL Playground](https://github.com/prisma/graphql-playground), [GraphiQL](https://github.com/skevy/graphiql-app), etc. The permissions can be set on a predicate for the group using using pattern similar to the UNIX file permission convention:

You can query and get information for users and groups.  These sections show output that will show the user `alice` and the `dev` group along with rules for `friend` and `~friend` predicates.

### Query for users

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

### Get user information

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

### Query for groups

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

The output should include the users in the group as well as the permissions, the
group's ACL rules, e.g.

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

### Get group information

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

The output should include the users in the group as well as the permissions, the
group's ACL rules, e.g.

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

If you have forgotten the password to the `groot` user, then you may reset the `groot` password (or
the password for any user) by following these steps.

1. Stop Dgraph Alpha.
2. Turn off ACLs by removing the `--acl_hmac_secret` config flag in the Alpha config. This leaves
   the Alpha open with no ACL rules, so be sure to restrict access, including stopping request
   traffic to this Alpha.
3. Start Dgraph Alpha.
4. Connect to Dgraph Alpha using Ratel and run the following upsert mutation to update the `groot` password
   to `newpassword` (choose your own secure password):
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
