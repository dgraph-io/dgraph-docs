---
title: Encryption at Rest
description: Encrypt data stored on disk using AES encryption
---

:::note
**Enterprise Feature**: Encryption at Rest requires a Dgraph Enterprise license. See [License](license) for details.
:::

Encryption at Rest encrypts data stored on disk, ensuring sensitive data is not readable without a valid decryption key. Dgraph uses the [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) algorithm for encryption.

Encryption keys can be stored on Hashicorp Vault servers in addition to local file systems.

## Setup

To enable encryption, pass a file containing the data encryption key using the `--encryption key-file=value` option. The key size must be 16, 24, or 32 bytes, determining the AES block size: AES-128, AES-192, or AES-256, respectively.

Generate an encryption key file (set `count` to the desired key size):

```bash
tr -dc 'a-zA-Z0-9' < /dev/urandom | dd bs=1 count=32 of=enc_key_file
```

:::note
On macOS, use `LC_CTYPE=C; tr -dc 'a-zA-Z0-9' < /dev/urandom | dd bs=1 count=32 of=enc_key_file`. To view the key, use `cat enc_key_file`.
:::

Alternatively, use the `--vault` [superflag](../../cli/superflags) options to enable encryption with Hashicorp Vault, as [explained below](#hashicorp-vault-configuration).

## Enable Encryption

Start Zero and Alpha with encryption enabled:

```bash
dgraph zero --my="localhost:5080" --replicas 1 --raft "idx=1"
dgraph alpha --encryption key-file="./enc_key_file" --my="localhost:7080" --zero="localhost:5080"
```

If multiple Alpha nodes are in the cluster, pass the `--encryption key-file` option to each Alpha.

Once encryption is enabled on an Alpha, the encryption key must be provided to start the server. If the Alpha restarts, the `--encryption key-file` option must be set with the key to restart successfully.

### Hashicorp Vault Configuration

You can store the encryption key in [Hashicorp Vault](https://www.vaultproject.io/) K/V Secrets instead of a local file.

**Prerequisites:**

1. Ensure the Vault server is accessible from Dgraph Alpha and configured using URL `http://fqdn[ip]:port`.
2. Enable [AppRole Auth method](https://www.vaultproject.io/docs/auth/approle) and [KV Secrets Engine](https://www.vaultproject.io/docs/secrets/kv).
3. Save the encryption key (16, 24, or 32 bytes) in a KV Secret path ([K/V Version 1](https://www.vaultproject.io/docs/secrets/kv/kv-v1) or [K/V Version 2](https://www.vaultproject.io/docs/secrets/kv/kv-v2)). For example, upload to KV Secrets Engine Version 2 path `secret/data/dgraph/alpha`:
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
4. Create or use a role with an attached policy that grants access to the secret. For example, the following policy grants access to `secret/data/dgraph/alpha`:
   ```hcl
   path "secret/data/dgraph/*" {
     capabilities = [ "read", "update" ]
   }
   ```
5. Using the `role_id` from the previous step, create a corresponding `secret_id`, and copy both to local files (e.g., `./dgraph/vault/role_id` and `./dgraph/vault/secret_id`) for use by Dgraph Alpha nodes.

:::note
The key format for the `enc-field` option can be defined using `enc-format` with values `base64` (default) or `raw`.
:::

### Example: Using Hashicorp Vault

Start Dgraph with a Vault server holding the encryption key:

```bash
## Start Dgraph Zero in a separate terminal
dgraph zero --my=localhost:5080 --replicas 1 --raft "idx=1"

## Start Dgraph Alpha in a separate terminal
dgraph alpha --my="localhost:7080" --zero="localhost:5080" \
  --vault addr="http://localhost:8200";enc-field="enc_key";enc-format="raw";path="secret/data/dgraph/alpha";role-id-file="./role_id";secret-id-file="./secret_id"
```

If multiple Alpha nodes are in the cluster, pass the `--encryption key-file` flag or the `--vault` superflag with appropriate options to each Alpha.

After encryption is enabled on an Alpha, you must provide the encryption key to start the server. If the Alpha restarts, the `--encryption key-file` or `--vault` superflag options must be set with the key to restart successfully.

## Disable Encryption

Use [live loader](../../migration/live-loader) or [bulk loader](../../migration/bulk-loader) to decrypt data during import.

## Key Rotation

The master encryption key set by `--encryption key-file` (or stored in Vault) does not change automatically. The master key encrypts underlying data keys, which are rotated automatically (see the [encryption-at-rest blog post][encblog] for details).

[encblog]: https://dgraph.io/blog/post/encryption-at-rest-dgraph-badger#one-key-to-rule-them-all-many-keys-to-find-them

To rotate the master encryption key, use the `badger rotate` command on both `p` and `w` directories for each Alpha. In HA cluster configurations, rotate keys one Alpha at a time in a rolling manner to maintain availability.

You need both the current key and the new key in separate files. Specify the directory to rotate (`p` or `w`) with `--dir`, the old key with `--old-key-path`, and the new key with `--new-key-path`:

```bash
badger rotate --dir p --old-key-path enc_key_file --new-key-path new_enc_key_file
badger rotate --dir w --old-key-path enc_key_file --new-key-path new_enc_key_file
```

Then start Alpha with the `new_enc_key_file` to use the new key.

