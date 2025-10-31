+++
date = "2017-03-20T22:25:17+11:00"
title = "Encryption at Rest"
weight = 6
type = "docs"
[menu.main]
    parent = "enterprise-features"
+++

{{% notice "note" %}}
This feature was introduced in [v1.1.1](https://github.com/dgraph-io/dgraph/releases/tag/v1.1.1).
For migrating unencrypted data to a new Dgraph cluster with encryption enabled, you need to
[export the database]({{< relref "dgraph-administration.md#export-database" >}}) and [import data]({{< relref "import-data.md" >}}),
preferably using the [bulk loader]({{< relref "bulk-loader.md" >}}).
{{% /notice %}}

Encryption at rest refers to the encryption of data that is stored physically in any
digital form. It ensures that sensitive data on disks is not readable by any user
or application without a valid key that is required for decryption. Dgraph provides
encryption at rest as an enterprise feature. If encryption is enabled, Dgraph uses
[Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
algorithm to encrypt the data and secure it.

Prior to v20.07.0, the encryption key file must be present on the local file system.
Starting with [v20.07.0](https://github.com/dgraph-io/dgraph/releases/tag/v20.07.0),
we have added support for encryption keys sitting on Vault servers. This allows an alternate
way to configure the encryption keys needed for encrypting the data at rest.

## Set up Encryption

To enable encryption, we need to pass a file that stores the data encryption key with the option
`--encryption key-file=value`. The key size must be 16, 24, or 32 bytes long, and the key size determines
the corresponding block size for AES encryption ,i.e. AES-128, AES-192, and AES-256, respectively.

You can use the following command to create the encryption key file (set _count_ to the
desired key size):

```bash
tr -dc 'a-zA-Z0-9' < /dev/urandom | dd bs=1 count=32 of=enc_key_file
```
{{% notice "note" %}}
On a macOS you may have to use `LC_CTYPE=C; tr -dc 'a-zA-Z0-9' < /dev/urandom | dd bs=1 count=32 of=enc_key_file`. To view the key use `cat enc_key_file`.
{{% /notice %}}
Alternatively, you can use the `--vault` [superflag's]({{< relref "cli/superflags.md" >}}) options to enable encryption, as [explained below](#example-using-dgraph-cli-with-hashicorp-vault-configuration).

## Turn on Encryption

Here is an example that starts one Zero server and one Alpha server with the encryption feature turned on:

```bash
dgraph zero --my="localhost:5080" --replicas 1 --raft "idx=1"
dgraph alpha --encryption key-file="./enc_key_file" --my="localhost:7080" --zero="localhost:5080"
```

If multiple Alpha nodes are part of the cluster, you will need to pass the `--encryption key-file` option to
each of the Alphas.

Once an Alpha has encryption enabled, the encryption key must be provided in order to start the Alpha server.
If the Alpha server restarts, the `--encryption key-file` option must be set along with the key in order to
restart successfully.

### Storing encryption key secret in Hashicorp Vault

You can save the encryption key secret in [Hashicorp Vault](https://www.vaultproject.io/) K/V Secret instead of as file on Dgraph Alpha.

To use [Hashicorp Vault](https://www.vaultproject.io/), meet the following prerequisites for the Vault Server.

1. Ensure that the Vault server is accessible from Dgraph Alpha and configured using URL `http://fqdn[ip]:port`.
2. Enable [AppRole Auth method](https://www.vaultproject.io/docs/auth/approle) and enable [KV Secrets Engine](https://www.vaultproject.io/docs/secrets/kv).
3. Save the value of the key (16, 24, or 32 bytes long) that Dgraph Alpha will use in a KV Secret path ([K/V Version 1](https://www.vaultproject.io/docs/secrets/kv/kv-v1) or [K/V Version 2](https://www.vaultproject.io/docs/secrets/kv/kv-v2)).  For example, you can upload this below to KV Secrets Engine Version 2 path of `secret/data/dgraph/alpha`:
   ```json
   {
     "options": {
       "cas": 0
     },
     "data": {
       "enc_key": "qIvHQBVUpzsOp74PmMJjHAOfwIA1e6zm%"
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
To learn more about the above steps, see [Dgraph Vault Integration: Docker](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/vault/docker/README.md).
{{% /notice %}}

{{% notice "note" %}}
The key format for the `enc-field` option can be defined using `enc-format` with the values `base64` (default) or `raw`.
{{% /notice %}}

### Example using Dgraph CLI with Hashicorp Vault configuration

The following example shows how to use Dgraph with a Vault server that holds the encryption key:

```bash
## Start Dgraph Zero in different terminal tab or window
dgraph zero --my=localhost:5080 --replicas 1 --raft "idx=1"

## Start Dgraph Alpha in different terminal tab or window
dgraph alpha --my="localhost:7080" --zero="localhost:5080" \
  --vault addr="http://localhost:8200";enc-field="enc_key";enc-format="raw";path="secret/data/dgraph/alpha";role-id-file="./role_id";secret-id-file="./secret_id"

```

If multiple Dgraph Alpha nodes are part of the cluster, you must pass the `--encryption key-file` flag or the `--vault` superflag with appropriate superflag options to each of the Dgraph Alpha nodes.

After an Alpha node has encryption enabled, you must provide the encryption key to start the Alpha server.
If the Alpha server restarts, the `--encryption key-file` or the `--vault` superflag's options must be set along with the key to restart successfully.

## Turn off Encryption

You can use [live loader]({{< relref "live-loader.md" >}}) or [bulk loader]({{< relref "bulk-loader.md" >}}) to decrypt the data while importing.


## Change Encryption Key

The master encryption key set by the `--encryption key-file` option (or one used in Vault KV store) does not change automatically. The master
encryption key encrypts underlying *data keys* which are changed on a regular basis automatically (more info
about this is covered on the encryption-at-rest [blog][encblog] post).

[encblog]: https://dgraph.io/blog/post/encryption-at-rest-dgraph-badger#one-key-to-rule-them-all-many-keys-to-find-them

Changing the existing key to a new one is called key rotation. You can rotate the master encryption key by
using the `badger rotate` command on both p and w directories for each Alpha. To maintain availability in HA
cluster configurations, you can do this rotate the key one Alpha at a time in a rolling manner.

You'll need both the current key and the new key in two different files. Specify the directory you
rotate ("p" or "w") for the `--dir` flag, the old key for the `--old-key-path` flag, and the new key with the
`--new-key-path` flag.

```
badger rotate --dir p --old-key-path enc_key_file --new-key-path new_enc_key_file
badger rotate --dir w --old-key-path enc_key_file --new-key-path new_enc_key_file
```

Then, you can start Alpha with the `new_enc_key_file` key file to use the new key.
