---
id: enable-acl
title: Enable ACL
---

Access Control List (ACL) provides access protection to your data stored in Dgraph. When the ACL feature is enabled, a client must authenticate with a username and password before executing any transactions, and is only allowed to access the data permitted by the ACL rules.

:::note
**Enterprise Feature**: ACL requires a Dgraph Enterprise license. See [License](license) for details.
:::

## Enable Enterprise ACL Feature

1. Generate a data encryption key that is 32 bytes long:

   ```bash
   tr -dc 'a-zA-Z0-9' < /dev/urandom | dd bs=1 count=32 of=enc_key_file
   ```
   :::note
   On a macOS you may have to use `LC_CTYPE=C; tr -dc 'a-zA-Z0-9' < /dev/urandom | dd bs=1 count=32 of=enc_key_file`.
   :::

2. To view the secret key value use `cat enc_key_file`.
3. Create a plain text file named `hmac_secret_file`, and store a randomly generated `<SECRET KEY VALUE>` in it. The secret key is used by Dgraph Alpha nodes to sign JSON Web Tokens (JWT).  

   ```bash
   echo '<SECRET KEY VALUE>' > hmac_secret_file
   ```

4. Start all the Dgraph Alpha nodes in your cluster with the option `--acl secret-file="/path/to/secret"`, and make sure that they are all using the same secret key file created in Step 1. Alternatively, you can [store the secret in Hashicorp Vault](#storing-acl-secret-in-hashicorp-vault).

   ```bash
   dgraph alpha --acl "secret-file=/path/to/secret" --security "whitelist=<permitted-ip-addresses>"
   ```


## Storing ACL Secret in Hashicorp Vault

You can save the ACL secret on [Hashicorp Vault](https://www.vaultproject.io/) server instead of saving the secret on the local file system.

### Configuring a Hashicorp Vault Server

Do the following to set up on the [Hashicorp Vault](https://www.vaultproject.io/) server for use with Dgraph:

1. Ensure that the Vault server is accessible from Dgraph Alpha and configured using URL `http://fqdn[ip]:port`.
2. Enable [AppRole Auth method](https://www.vaultproject.io/docs/auth/approle) and enable [KV Secrets Engine](https://www.vaultproject.io/docs/secrets/kv).
3. Save the 256-bits (32 ASCII characters) long ACL secret in a KV Secret path ([K/V Version 1](https://www.vaultproject.io/docs/secrets/kv/kv-v1) or [K/V Version 2](https://www.vaultproject.io/docs/secrets/kv/kv-v2)). For example, you can upload this below to KV Secrets Engine Version 2 path of `secret/data/dgraph/alpha`:
   ```json
   {
     "options": {
       "cas": 0
     },
     "data": {
       "hmac_secret_file": "<SECRET KEY VALUE>"
     }
   }
   ```   
4. Create or use a role with an attached policy that grants access to the secret. For example, the following policy would grant access to `secret/data/dgraph/alpha`:
   ```hcl
   path "secret/data/dgraph/*" {
     capabilities = [ "read", "update" ]
   }
   ```
5. Using the `role_id` generated from the previous step, create a corresponding `secret_id`, and copy the `role_id` and `secret_id` over to local files, like `./dgraph/vault/role_id` and `./dgraph/vault/secret_id`, that will be used by Dgraph Alpha nodes.

:::tip
To learn more about the above steps, see [Dgraph Vault Integration: Docker](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/vault/docker/README.md).
:::

:::note
The key format for the `acl-field` option can be defined using `acl-format` with the values `base64` (default) or `raw`.
:::

## Related Topics

- [User Management and Access Control](../../admin/admin-tasks/user-management-access-control) - Manage users, groups, and ACL rules after enabling ACL


